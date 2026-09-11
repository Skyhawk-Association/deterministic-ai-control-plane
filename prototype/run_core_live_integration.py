#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

import dacp_action_provider as native_actions
import dacp_broker
from dacp_authority_provider import HASH_MODE, PinnedFileAuthorityProvider
from dacp_control_session import DACPControlSession
from dacp_core_live_runtime import VersionedValueRuntime
from dacp_file_runtime import FileBackedValueRuntime
from dacp_operation_manifest import LoadedOperation, load_operation_manifest
from dacp_runtime_contract import DACPRuntime, bind_core_runtime


DEFAULT_STATE_ENV = "DACP_STATE_FILE"
DEFAULT_OPERATION_MANIFEST = Path(__file__).resolve().parent / "operations" / "tracked-value-deploy.json"
DEFAULT_AUTHORITY_MANIFEST = Path(__file__).resolve().parent / "authorities" / "tracked-value-deploy-authority.json"
DEFAULT_AUTHORITY_SHA256 = "46bf8723794841351a97ec063ed64897a60330ebd2ba9ff52b815655e8d834d3"


def _repo_identity() -> dict[str, Any]:
    repo_root = Path(__file__).resolve().parents[1]
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_root, check=True, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=repo_root, check=True, capture_output=True, text=True).stdout.strip()
    return {"source_commit": head, "tracked_source_clean": not bool(dirty)}


def _write_verified_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if json.loads(path.read_text(encoding="utf-8")) != payload:
        raise RuntimeError(f"JSON readback mismatch: {path}")


def _sha256_file(path: Path | None) -> str | None:
    if path is None or not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _default_state_file() -> Path:
    configured = os.environ.get(DEFAULT_STATE_ENV)
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path.home() / ".dacp" / "runtime" / "tracked-value.json").resolve()


def _resolve_state_file(runtime_kind: str, state_file: str | Path | None) -> Path | None:
    if runtime_kind == "memory":
        return None
    if state_file is not None:
        return Path(state_file).expanduser().resolve()
    return _default_state_file()


def _resolve_operation_manifest(path: str | Path | None) -> LoadedOperation:
    return load_operation_manifest(path or DEFAULT_OPERATION_MANIFEST)


def _resolve_authority_config(path: str | Path | None, sha256_pin: str | None) -> tuple[Path, str]:
    if path is None and sha256_pin is None:
        return DEFAULT_AUTHORITY_MANIFEST, DEFAULT_AUTHORITY_SHA256
    if path is None or sha256_pin is None:
        raise ValueError("alternate authority requires both --authority-manifest and --authority-sha256")
    return Path(path).expanduser().resolve(), sha256_pin.strip().lower()


def _make_runtime(runtime_kind: str, state_file: str | Path | None) -> DACPRuntime:
    if runtime_kind == "memory":
        return VersionedValueRuntime()
    resolved = _resolve_state_file(runtime_kind, state_file)
    if resolved is None:
        raise RuntimeError("file runtime did not resolve a state path")
    return FileBackedValueRuntime(resolved)


def _run_provider(
    provider: str,
    model: str,
    max_output_tokens: int,
    timeout: int,
    max_turns: int,
    runtime_kind: str,
    state_file: str | None,
    operation_manifest: str | None,
    authority_manifest: str | None,
    authority_sha256: str | None,
) -> dict[str, Any]:
    loaded_operation = _resolve_operation_manifest(operation_manifest)
    operation = loaded_operation.operation
    resolved_state_file = _resolve_state_file(runtime_kind, state_file)
    runtime = _make_runtime(runtime_kind, resolved_state_file)
    authority_path, authority_pin = _resolve_authority_config(authority_manifest, authority_sha256)
    authority = PinnedFileAuthorityProvider(authority_path, authority_pin, runtime.resolve_target_fingerprint)
    state_path = resolved_state_file if runtime_kind == "file" else None

    pre_snapshot = runtime.evidence_snapshot()
    pre_state_sha256 = _sha256_file(state_path)
    pre_authority = authority.evidence_snapshot()
    expected_value = operation.expected_value
    preexisting_expected = pre_snapshot["value"] == expected_value

    env_name = "OPENAI_API_KEY" if provider == "openai" else "ANTHROPIC_API_KEY"
    credential_present = bool(os.environ.get(env_name))
    provider_call = (
        native_actions.make_provider_call(provider, model, max_output_tokens, timeout)
        if credential_present
        else None
    )

    session = DACPControlSession(operation, bind_core_runtime(runtime, authority, now_epoch=lambda: 1), provider_call)
    session_result = session.run(max_turns=max_turns)

    post_snapshot = runtime.evidence_snapshot()
    post_state_sha256 = _sha256_file(state_path)
    post_authority = authority.evidence_snapshot()
    state_changed = pre_state_sha256 != post_state_sha256 if state_path is not None else None

    if preexisting_expected:
        expected_branch = "PREEXISTING_VERIFIED_NO_DISPATCH"
        runtime_transition_ok = (
            session_result.applied_count == 0
            and session_result.dispatch_count == 0
            and len(session_result.turns) == 0
            and (state_changed is False if state_path is not None else post_snapshot["value"] == expected_value)
            and pre_snapshot["version"] == post_snapshot["version"]
            and len(pre_snapshot["ledger"]) == len(post_snapshot["ledger"])
        )
    else:
        expected_branch = "MUTATION_REQUIRED"
        runtime_transition_ok = (
            credential_present
            and session_result.dispatch_count == 1
            and session_result.applied_count == 1
            and len(session_result.turns) == 1
            and post_snapshot["value"] == expected_value
            and (state_changed is True if state_path is not None else True)
        )

    authority_integrity_ok = bool(pre_authority.get("integrity_ok")) and bool(post_authority.get("integrity_ok"))
    pass_condition = (
        session_result.terminal_state == "REPORTED"
        and session_result.final_acceptance == operation.expected_acceptance
        and post_snapshot["value"] == expected_value
        and runtime_transition_ok
        and authority_integrity_ok
        and not session_result.verification_conflict
    )

    return {
        "provider": provider,
        "model": model,
        "credential_present": credential_present,
        "credential_required_for_branch": not preexisting_expected,
        "execution_branch": expected_branch,
        "runtime_kind": runtime_kind,
        "status": "PASS" if pass_condition else ("NOT_RUN_MISSING_CREDENTIAL" if not credential_present and not preexisting_expected else "FAIL"),
        "pass": pass_condition,
        "operation_id": operation.operation_id,
        "operation_manifest": {
            "path": str(loaded_operation.path),
            "sha256": loaded_operation.sha256,
            "schema": loaded_operation.raw["schema"],
        },
        "authority_evidence": {"pre": pre_authority, "post": post_authority},
        "declaration_result": session_result.declaration_result,
        "preexisting_check": session_result.preexisting_check,
        "terminal_state": session_result.terminal_state,
        "final_acceptance": session_result.final_acceptance,
        "completion_source": session_result.completion_source,
        "control_finalization": session_result.control_finalization,
        "provider_turn_count": len(session_result.turns),
        "dispatch_count": session_result.dispatch_count,
        "applied_count": session_result.applied_count,
        "reconciliation_count": session_result.reconciliation_count,
        "verification_conflict": session_result.verification_conflict,
        "runtime_transition_ok": runtime_transition_ok,
        "runtime_snapshot": post_snapshot,
        "runtime_evidence": {
            "pre_snapshot": pre_snapshot,
            "post_snapshot": post_snapshot,
            "pre_state_sha256": pre_state_sha256,
            "post_state_sha256": post_state_sha256,
            "state_changed": state_changed,
        },
        "core_events": session_result.core_events,
        "turns": session_result.turns,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run primary-provider live DACP commitment-core integration")
    parser.add_argument("--provider", choices=["openai", "anthropic"], default="openai")
    parser.add_argument("--model", default=None)
    parser.add_argument("--runtime", choices=["file", "memory"], default="file", help="execution runtime; durable file state is the application default")
    parser.add_argument("--state-file", default=None, help="durable state path; defaults to DACP_STATE_FILE or ~/.dacp/runtime/tracked-value.json")
    parser.add_argument("--operation-manifest", default=None, help="operation request JSON; defaults to operations/tracked-value-deploy.json")
    parser.add_argument("--authority-manifest", default=None, help="alternate authority JSON; requires --authority-sha256")
    parser.add_argument("--authority-sha256", default=None, help="trusted canonical-JSON SHA-256 pin for alternate authority JSON")
    parser.add_argument("--max-output-tokens", type=int, default=256)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--max-turns", type=int, default=3)
    parser.add_argument("--log-dir", default="gate-matrix-results")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    identity = _repo_identity()
    if not identity["tracked_source_clean"]:
        raise RuntimeError("Tracked repository source is dirty; refusing live integration run")

    default_model = dacp_broker.DEFAULT_OPENAI_MODEL if args.provider == "openai" else dacp_broker.DEFAULT_ANTHROPIC_MODEL
    model = args.model or default_model
    provider_result = _run_provider(
        args.provider,
        model,
        args.max_output_tokens,
        args.timeout,
        args.max_turns,
        args.runtime,
        args.state_file,
        args.operation_manifest,
        args.authority_manifest,
        args.authority_sha256,
    )

    output = {
        "schema": "dacp-core-live-integration-0.9",
        "timestamp": dacp_broker.utc_now(),
        "source_commit": identity["source_commit"],
        "tracked_source_clean": identity["tracked_source_clean"],
        "provider_role": "MUTATION_PROPOSAL_ONLY",
        "session_contract": "DACPControlSession/DeterministicDeclarationPrecheck",
        "runtime_contract": "DACPRuntime/evidence_snapshot",
        "authority_contract": "PinnedFileAuthorityProvider/dacp-authority-manifest-0.1",
        "authority_hash_mode": HASH_MODE,
        "authority_default_sha256": DEFAULT_AUTHORITY_SHA256,
        "runtime_default": "file",
        "operation_contract": "dacp-operation-manifest-0.1",
        "completion_contract": "PREEXISTING_FAST_PATH_OR_CONTROL_PLANE_AUTO_FINALIZE",
        "durable_evidence_contract": "PRE_POST_STATE_SHA256_AND_SNAPSHOT",
        "provider_result": provider_result,
    }

    stamp = output["timestamp"].replace(":", "").replace("-", "")
    path = Path(args.log_dir) / f"core-live-integration-{stamp}.json"
    _write_verified_json(path, output)

    print("=== DACP_CORE_LIVE_INTEGRATION_BEGIN ===")
    print(json.dumps(output, indent=2, sort_keys=True))
    print("=== DACP_CORE_LIVE_INTEGRATION_END ===")
    print(f"RESULT_FILE={path.resolve()}")

    if provider_result.get("pass"):
        return 0
    if provider_result.get("status") == "NOT_RUN_MISSING_CREDENTIAL":
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
