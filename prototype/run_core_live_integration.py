#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dacp_authority_provider import HASH_MODE, PinnedFileAuthorityProvider
from dacp_commit_journal import DurableCommitJournal
from dacp_core_live_runtime import VersionedValueRuntime
from dacp_file_lock import InterProcessFileLock, LockTimeoutError
from dacp_file_runtime import FileBackedValueRuntime
from dacp_operation_manifest import LoadedOperation, load_operation_manifest
from dacp_resolved_operation import DACPResolvedOperation
from dacp_runtime_contract import DACPRuntime, bind_core_runtime

DEFAULT_STATE_ENV = "DACP_STATE_FILE"
DEFAULT_OPERATION_MANIFEST = Path(__file__).resolve().parent / "operations" / "tracked-value-deploy.json"
DEFAULT_AUTHORITY_MANIFEST = Path(__file__).resolve().parent / "authorities" / "tracked-value-deploy-authority.json"
DEFAULT_AUTHORITY_SHA256 = "46bf8723794841351a97ec063ed64897a60330ebd2ba9ff52b815655e8d834d3"
DEFAULT_LOCK_TIMEOUT_SECONDS = 10.0


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


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


def _journal_path(state_path: Path) -> Path:
    return state_path.with_name(state_path.name + ".commit-journal.json")


def _lock_path(state_path: Path) -> Path:
    return state_path.with_name(state_path.name + ".commit.lock")


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


def _run_resolved_locked(
    runtime_kind: str,
    resolved_state_file: Path | None,
    operation_manifest: str | None,
    authority_manifest: str | None,
    authority_sha256: str | None,
) -> dict[str, Any]:
    loaded_operation = _resolve_operation_manifest(operation_manifest)
    operation = loaded_operation.operation
    runtime = _make_runtime(runtime_kind, resolved_state_file)
    authority_path, authority_pin = _resolve_authority_config(authority_manifest, authority_sha256)
    authority = PinnedFileAuthorityProvider(authority_path, authority_pin, runtime.resolve_target_fingerprint)
    state_path = resolved_state_file if runtime_kind == "file" else None
    journal = DurableCommitJournal(_journal_path(state_path)) if state_path is not None else None

    pre_snapshot = runtime.evidence_snapshot()
    pre_state_sha256 = _sha256_file(state_path)
    pre_authority = authority.evidence_snapshot()
    pre_journal = journal.evidence_snapshot() if journal is not None else None
    preexisting_expected = pre_snapshot["value"] == operation.expected_value

    core_runtime = bind_core_runtime(
        runtime,
        authority,
        now_epoch=lambda: 1,
        dispatch_journal=journal,
        operation_id=operation.operation_id if journal is not None else None,
    )
    resolved = DACPResolvedOperation(operation, core_runtime, commit_journal=journal)
    result = resolved.run()

    post_snapshot = runtime.evidence_snapshot()
    post_state_sha256 = _sha256_file(state_path)
    post_authority = authority.evidence_snapshot()
    post_journal = journal.evidence_snapshot() if journal is not None else None
    state_changed = pre_state_sha256 != post_state_sha256 if state_path is not None else None

    if result.execution_branch == "RECOVERY_PENDING_NO_REDISPATCH":
        runtime_transition_ok = (
            result.dispatch_count == 0
            and result.applied_count == 0
            and post_snapshot == pre_snapshot
            and (state_changed is False if state_path is not None else True)
        )
        pass_condition = False
    elif result.execution_branch == "RECOVERY_VERIFIED_NO_REDISPATCH":
        runtime_transition_ok = (
            result.dispatch_count == 0
            and result.applied_count == 0
            and post_snapshot["value"] == operation.expected_value
            and (state_changed is False if state_path is not None else True)
        )
        pass_condition = (
            result.terminal_state == "REPORTED"
            and result.final_acceptance == operation.expected_acceptance
            and runtime_transition_ok
            and not result.verification_conflict
        )
    elif result.execution_branch == "RECOVERY_REQUEST_MISMATCH_BLOCKED":
        runtime_transition_ok = (
            result.dispatch_count == 0
            and result.applied_count == 0
            and post_snapshot == pre_snapshot
            and (state_changed is False if state_path is not None else True)
        )
        pass_condition = False
    elif preexisting_expected:
        runtime_transition_ok = (
            result.execution_branch == "PREEXISTING_VERIFIED_NO_DISPATCH"
            and result.dispatch_count == 0
            and result.applied_count == 0
            and (state_changed is False if state_path is not None else post_snapshot["value"] == operation.expected_value)
            and pre_snapshot["version"] == post_snapshot["version"]
            and len(pre_snapshot["ledger"]) == len(post_snapshot["ledger"])
        )
        pass_condition = (
            result.terminal_state == "REPORTED"
            and result.final_acceptance == operation.expected_acceptance
            and runtime_transition_ok
            and not result.verification_conflict
        )
    else:
        runtime_transition_ok = (
            result.execution_branch == "MUTATION_REQUIRED"
            and result.dispatch_count == 1
            and result.applied_count == 1
            and post_snapshot["value"] == operation.expected_value
            and (state_changed is True if state_path is not None else True)
        )
        pass_condition = (
            result.terminal_state == "REPORTED"
            and result.final_acceptance == operation.expected_acceptance
            and runtime_transition_ok
            and not result.verification_conflict
        )

    authority_integrity_ok = bool(pre_authority.get("integrity_ok")) and bool(post_authority.get("integrity_ok"))
    pass_condition = pass_condition and authority_integrity_ok

    return {
        "provider_dependency": False,
        "provider_used": False,
        "provider_turn_count": 0,
        "execution_branch": result.execution_branch,
        "runtime_kind": runtime_kind,
        "status": "PASS" if pass_condition else ("PENDING" if result.terminal_state == "PENDING" else "FAIL"),
        "pass": pass_condition,
        "operation_id": operation.operation_id,
        "operation_manifest": {
            "path": str(loaded_operation.path),
            "sha256": loaded_operation.sha256,
            "schema": loaded_operation.raw["schema"],
        },
        "authority_evidence": {"pre": pre_authority, "post": post_authority},
        "journal_evidence": {"pre": pre_journal, "post": post_journal},
        "declaration_result": result.declaration_result,
        "preexisting_check": result.preexisting_check,
        "commit_result": result.commit_result,
        "pending_reconciliation": result.pending_reconciliation,
        "recovery_record": result.recovery_record,
        "terminal_state": result.terminal_state,
        "final_acceptance": result.final_acceptance,
        "completion_source": result.completion_source,
        "control_finalization": result.control_finalization,
        "dispatch_count": result.dispatch_count,
        "applied_count": result.applied_count,
        "reconciliation_count": result.reconciliation_count,
        "rebind_count": result.rebind_count,
        "verification_conflict": result.verification_conflict,
        "runtime_transition_ok": runtime_transition_ok,
        "runtime_snapshot": post_snapshot,
        "runtime_evidence": {
            "pre_snapshot": pre_snapshot,
            "post_snapshot": post_snapshot,
            "pre_state_sha256": pre_state_sha256,
            "post_state_sha256": post_state_sha256,
            "state_changed": state_changed,
        },
        "core_events": result.core_events,
    }


def _run_resolved(
    runtime_kind: str,
    state_file: str | None,
    operation_manifest: str | None,
    authority_manifest: str | None,
    authority_sha256: str | None,
    *,
    lock_timeout_seconds: float = DEFAULT_LOCK_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    resolved_state_file = _resolve_state_file(runtime_kind, state_file)
    if runtime_kind == "memory":
        return _run_resolved_locked(
            runtime_kind,
            resolved_state_file,
            operation_manifest,
            authority_manifest,
            authority_sha256,
        )

    if resolved_state_file is None:
        raise RuntimeError("file runtime did not resolve a state path")

    lock_path = _lock_path(resolved_state_file)
    try:
        with InterProcessFileLock(lock_path, timeout_seconds=lock_timeout_seconds):
            result = _run_resolved_locked(
                runtime_kind,
                resolved_state_file,
                operation_manifest,
                authority_manifest,
                authority_sha256,
            )
    except LockTimeoutError as exc:
        return {
            "provider_dependency": False,
            "provider_used": False,
            "provider_turn_count": 0,
            "execution_branch": "CONCURRENT_OPERATION_LOCK_TIMEOUT",
            "runtime_kind": runtime_kind,
            "status": "PENDING",
            "pass": False,
            "terminal_state": "PENDING",
            "final_acceptance": None,
            "completion_source": "CONCURRENT_OPERATION_IN_PROGRESS",
            "dispatch_count": 0,
            "applied_count": 0,
            "reconciliation_count": 0,
            "rebind_count": 0,
            "verification_conflict": False,
            "runtime_transition_ok": True,
            "lock_evidence": {
                "path": str(lock_path),
                "timeout_seconds": lock_timeout_seconds,
                "error": str(exc),
            },
        }

    result["lock_evidence"] = {
        "path": str(lock_path),
        "timeout_seconds": lock_timeout_seconds,
        "acquired": True,
    }
    return result


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run DACP deterministic resolved-operation commitment")
    parser.add_argument("--runtime", choices=["file", "memory"], default="file")
    parser.add_argument("--state-file", default=None)
    parser.add_argument("--operation-manifest", default=None)
    parser.add_argument("--authority-manifest", default=None)
    parser.add_argument("--authority-sha256", default=None)
    parser.add_argument("--lock-timeout", type=float, default=DEFAULT_LOCK_TIMEOUT_SECONDS)
    parser.add_argument("--log-dir", default="gate-matrix-results")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    identity = _repo_identity()
    if not identity["tracked_source_clean"]:
        raise RuntimeError("Tracked repository source is dirty; refusing live integration run")

    operation_result = _run_resolved(
        args.runtime,
        args.state_file,
        args.operation_manifest,
        args.authority_manifest,
        args.authority_sha256,
        lock_timeout_seconds=args.lock_timeout,
    )

    output = {
        "schema": "dacp-core-live-integration-1.3",
        "timestamp": _utc_now(),
        "source_commit": identity["source_commit"],
        "tracked_source_clean": identity["tracked_source_clean"],
        "application_mode": "RESOLVED_OPERATION_COMMITMENT",
        "provider_dependency": False,
        "commitment_path": "RESOLVED_OPERATION_DETERMINISTIC_NO_PROVIDER",
        "recovery_contract": "DURABLE_DISPATCH_INTENT_RECONCILE_BEFORE_REDISPATCH",
        "concurrency_contract": "ONE_DURABLE_RESOURCE_ONE_COMMITMENT_PROCESS_AT_A_TIME",
        "runtime_contract": "DACPRuntime/evidence_snapshot",
        "authority_contract": "PinnedFileAuthorityProvider/dacp-authority-manifest-0.1",
        "authority_hash_mode": HASH_MODE,
        "authority_default_sha256": DEFAULT_AUTHORITY_SHA256,
        "runtime_default": "file",
        "operation_contract": "dacp-operation-manifest-0.1",
        "commit_journal_contract": "dacp-commit-journal-0.1",
        "completion_contract": "DETERMINISTIC_PRECHECK_DIRECT_COMMIT_VERIFY_FINALIZE",
        "durable_evidence_contract": "PRE_POST_STATE_SHA256_AND_COMMIT_JOURNAL",
        "operation_result": operation_result,
    }

    stamp = output["timestamp"].replace(":", "").replace("-", "")
    path = Path(args.log_dir) / f"core-live-integration-{stamp}.json"
    _write_verified_json(path, output)
    print("=== DACP_CORE_LIVE_INTEGRATION_BEGIN ===")
    print(json.dumps(output, indent=2, sort_keys=True))
    print("=== DACP_CORE_LIVE_INTEGRATION_END ===")
    print(f"RESULT_FILE={path.resolve()}")
    if operation_result.get("status") == "PENDING":
        return 2
    return 0 if operation_result.get("pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
