#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any

import dacp_action_provider as native_actions
import dacp_broker
from dacp_control_session import DACPControlSession, OperationSpec
from dacp_core_live_runtime import VersionedValueRuntime
from dacp_file_runtime import FileBackedValueRuntime
from dacp_runtime_contract import DACPRuntime, bind_core_runtime


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


def _operation_for_runtime(runtime: DACPRuntime) -> OperationSpec:
    return OperationSpec(
        operation_id="tracked-value-deploy",
        task="set the tracked value to DEPLOYED using SET_STATE.",
        endpoint=runtime.endpoint,
        tool="SET_STATE",
        args={"value": runtime.authorized_value},
        verifier_tool="READ_STATE",
        verifier_args={},
        expected_value=runtime.authorized_value,
        rollback_or_reconciliation_plan="reconcile before retry; rollback only with fresh authority.",
    )


def _make_runtime(runtime_kind: str, state_file: str | None) -> DACPRuntime:
    if runtime_kind == "memory":
        return VersionedValueRuntime()
    if not state_file:
        raise ValueError("--state-file is required when --runtime file")
    return FileBackedValueRuntime(state_file)


def _run_provider(provider: str, model: str, max_output_tokens: int, timeout: int, max_turns: int, runtime_kind: str, state_file: str | None) -> dict[str, Any]:
    env_name = "OPENAI_API_KEY" if provider == "openai" else "ANTHROPIC_API_KEY"
    if not os.environ.get(env_name):
        return {"provider": provider, "model": model, "credential_present": False, "status": "NOT_RUN_MISSING_CREDENTIAL", "turns": []}

    runtime = _make_runtime(runtime_kind, state_file)
    operation = _operation_for_runtime(runtime)
    provider_call = native_actions.make_provider_call(provider, model, max_output_tokens, timeout)
    session = DACPControlSession(operation, bind_core_runtime(runtime, now_epoch=lambda: 1), provider_call)
    session_result = session.run(max_turns=max_turns)
    snapshot = runtime.evidence_snapshot()

    pass_condition = (
        session_result.terminal_state == "REPORTED"
        and session_result.final_acceptance == operation.expected_acceptance
        and snapshot["value"] == runtime.authorized_value
        and session_result.dispatch_count == 1
        and session_result.applied_count in {0, 1}
        and not session_result.verification_conflict
    )

    return {
        "provider": provider,
        "model": model,
        "credential_present": True,
        "runtime_kind": runtime_kind,
        "status": "PASS" if pass_condition else "FAIL",
        "pass": pass_condition,
        "operation_id": operation.operation_id,
        "terminal_state": session_result.terminal_state,
        "final_acceptance": session_result.final_acceptance,
        "dispatch_count": session_result.dispatch_count,
        "applied_count": session_result.applied_count,
        "reconciliation_count": session_result.reconciliation_count,
        "verification_conflict": session_result.verification_conflict,
        "runtime_snapshot": snapshot,
        "core_events": session_result.core_events,
        "turns": session_result.turns,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run primary-provider live DACP commitment-core integration")
    parser.add_argument("--provider", choices=["openai", "anthropic"], default="openai")
    parser.add_argument("--model", default=None)
    parser.add_argument("--runtime", choices=["memory", "file"], default="memory")
    parser.add_argument("--state-file", default=None)
    parser.add_argument("--max-output-tokens", type=int, default=256)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--max-turns", type=int, default=6)
    parser.add_argument("--log-dir", default="gate-matrix-results")
    args = parser.parse_args()

    identity = _repo_identity()
    if not identity["tracked_source_clean"]:
        raise RuntimeError("Tracked repository source is dirty; refusing live integration run")

    default_model = dacp_broker.DEFAULT_OPENAI_MODEL if args.provider == "openai" else dacp_broker.DEFAULT_ANTHROPIC_MODEL
    model = args.model or default_model
    provider_result = _run_provider(args.provider, model, args.max_output_tokens, args.timeout, args.max_turns, args.runtime, args.state_file)

    output = {
        "schema": "dacp-core-live-integration-0.3",
        "timestamp": dacp_broker.utc_now(),
        "source_commit": identity["source_commit"],
        "tracked_source_clean": identity["tracked_source_clean"],
        "provider_role": "PRIMARY_IMPLEMENTATION_PATH" if args.provider == "openai" else "OPTIONAL_INDEPENDENT_PATH",
        "session_contract": "DACPControlSession/OperationSpec",
        "runtime_contract": "DACPRuntime/evidence_snapshot",
        "provider_result": provider_result,
    }

    stamp = output["timestamp"].replace(":", "").replace("-", "")
    path = Path(args.log_dir) / f"core-live-integration-{stamp}.json"
    _write_verified_json(path, output)

    print("=== DACP_CORE_LIVE_INTEGRATION_BEGIN ===")
    print(json.dumps(output, indent=2, sort_keys=True))
    print("=== DACP_CORE_LIVE_INTEGRATION_END ===")
    print(f"RESULT_FILE={path.resolve()}")

    if not provider_result.get("credential_present"):
        return 2
    return 0 if provider_result.get("pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
