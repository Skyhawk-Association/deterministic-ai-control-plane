#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any

import run_core_live_integration as live
from dacp_authority_provider import PinnedFileAuthorityProvider
from dacp_commit_journal import DurableCommitJournal
from dacp_file_lock import InterProcessFileLock
from dacp_file_runtime import FileBackedValueRuntime

SCHEMA = "dacp-conditional-acceptance-0.5"
UNIT_MODULES = [
    "test_dacp_commitment_core.py",
    "test_dacp_core_adapter.py",
    "test_dacp_authority_provider.py",
    "test_dacp_control_session.py",
    "test_dacp_commit_journal.py",
    "test_dacp_file_lock.py",
    "test_dacp_resolved_operation.py",
    "test_dacp_core_live_runtime.py",
    "test_dacp_file_runtime.py",
    "test_run_core_live_integration_session.py",
    "test_run_live.py",
]


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_verified_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if json.loads(path.read_text(encoding="utf-8")) != payload:
        raise RuntimeError(f"conditional acceptance readback mismatch: {path}")


def _case(name: str, assertions: dict[str, bool], evidence: dict[str, Any]) -> dict[str, Any]:
    failures = [label for label, passed in assertions.items() if not passed]
    return {
        "name": name,
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "assertions": assertions,
        "evidence": evidence,
    }


def assess_mutation(result: dict[str, Any]) -> dict[str, Any]:
    snapshot = result.get("runtime_snapshot") or {}
    runtime_evidence = result.get("runtime_evidence") or {}
    authority = result.get("authority_evidence") or {}
    journal = (result.get("journal_evidence") or {}).get("post") or {}
    records = journal.get("records") or []
    latest = records[-1] if records else {}
    lock = result.get("lock_evidence") or {}
    return _case("MUTATION_REQUIRED", {
        "provider_dependency_absent": result.get("provider_dependency") is False,
        "provider_not_used": result.get("provider_used") is False,
        "zero_provider_turns": result.get("provider_turn_count") == 0,
        "provider_result_passed": result.get("pass") is True,
        "branch_is_mutation_required": result.get("execution_branch") == "MUTATION_REQUIRED",
        "exactly_one_dispatch": result.get("dispatch_count") == 1,
        "exactly_one_applied_write": result.get("applied_count") == 1,
        "direct_control_commit": result.get("completion_source") == "CONTROL_PLANE_DIRECT_COMMIT",
        "verified_succeeded": result.get("final_acceptance") == "VERIFIED_SUCCEEDED",
        "state_changed": runtime_evidence.get("state_changed") is True,
        "version_one": snapshot.get("version") == 1,
        "one_ledger_event": len(snapshot.get("ledger") or []) == 1,
        "authority_pre_integrity": bool((authority.get("pre") or {}).get("integrity_ok")),
        "authority_post_integrity": bool((authority.get("post") or {}).get("integrity_ok")),
        "journal_resolved_succeeded": latest.get("phase") == "RESOLVED_SUCCEEDED",
        "resource_lock_acquired": lock.get("acquired") is True,
        "no_verification_conflict": result.get("verification_conflict") is False,
    }, result)


def assess_preexisting(result: dict[str, Any], stable_hash: str) -> dict[str, Any]:
    runtime_evidence = result.get("runtime_evidence") or {}
    snapshot = result.get("runtime_snapshot") or {}
    check = result.get("preexisting_check") or {}
    oracle = check.get("oracle") or {}
    lock = result.get("lock_evidence") or {}
    return _case("PREEXISTING_VERIFIED", {
        "provider_dependency_absent": result.get("provider_dependency") is False,
        "provider_not_used": result.get("provider_used") is False,
        "zero_provider_turns": result.get("provider_turn_count") == 0,
        "provider_result_passed": result.get("pass") is True,
        "branch_is_preexisting_fast_path": result.get("execution_branch") == "PREEXISTING_VERIFIED_NO_DISPATCH",
        "zero_dispatches": result.get("dispatch_count") == 0,
        "zero_applied_writes": result.get("applied_count") == 0,
        "preexisting_postcondition_verified": check.get("code") == "PREEXISTING_POSTCONDITION_VERIFIED",
        "verifier_oracle_match": oracle.get("code") == "VERIFIER_ORACLE_MATCH",
        "completion_source_preexisting": result.get("completion_source") == "PREEXISTING_STATE_VERIFIED",
        "verified_succeeded": result.get("final_acceptance") == "VERIFIED_SUCCEEDED",
        "state_unchanged": runtime_evidence.get("state_changed") is False,
        "pre_post_hash_equal": runtime_evidence.get("pre_state_sha256") == runtime_evidence.get("post_state_sha256"),
        "matches_stable_hash": runtime_evidence.get("post_state_sha256") == stable_hash,
        "version_one": snapshot.get("version") == 1,
        "one_ledger_event": len(snapshot.get("ledger") or []) == 1,
        "resource_lock_acquired": lock.get("acquired") is True,
        "no_verification_conflict": result.get("verification_conflict") is False,
    }, result)


def assess_recovery_pending(result: dict[str, Any]) -> dict[str, Any]:
    runtime_evidence = result.get("runtime_evidence") or {}
    journal = (result.get("journal_evidence") or {}).get("post") or {}
    records = journal.get("records") or []
    latest = records[-1] if records else {}
    lock = result.get("lock_evidence") or {}
    return _case("RESTART_UNRESOLVED_NO_REDISPATCH", {
        "status_pending": result.get("status") == "PENDING",
        "not_claimed_passed": result.get("pass") is False,
        "recovery_pending_branch": result.get("execution_branch") == "RECOVERY_PENDING_NO_REDISPATCH",
        "zero_dispatches_after_restart": result.get("dispatch_count") == 0,
        "zero_writes_after_restart": result.get("applied_count") == 0,
        "state_unchanged": runtime_evidence.get("state_changed") is False,
        "state_still_initial": (result.get("runtime_snapshot") or {}).get("value") == "INITIAL",
        "journal_remains_unresolved": latest.get("phase") == "RECOVERY_PENDING",
        "completion_not_claimed": result.get("final_acceptance") is None,
        "resource_lock_acquired": lock.get("acquired") is True,
    }, result)


def assess_recovery_succeeded(result: dict[str, Any]) -> dict[str, Any]:
    journal = (result.get("journal_evidence") or {}).get("post") or {}
    records = journal.get("records") or []
    latest = records[-1] if records else {}
    check = result.get("preexisting_check") or {}
    oracle = check.get("oracle") or {}
    lock = result.get("lock_evidence") or {}
    return _case("RESTART_RECONCILES_SUCCESS_NO_REDISPATCH", {
        "provider_result_passed": result.get("pass") is True,
        "recovery_verified_branch": result.get("execution_branch") == "RECOVERY_VERIFIED_NO_REDISPATCH",
        "zero_dispatches_after_restart": result.get("dispatch_count") == 0,
        "zero_writes_after_restart": result.get("applied_count") == 0,
        "preexisting_verified": check.get("code") == "PREEXISTING_POSTCONDITION_VERIFIED",
        "verifier_oracle_match": oracle.get("code") == "VERIFIER_ORACLE_MATCH",
        "verified_succeeded": result.get("final_acceptance") == "VERIFIED_SUCCEEDED",
        "restart_completion_source": result.get("completion_source") == "RESTART_RECONCILED_SUCCEEDED",
        "journal_resolved_succeeded": latest.get("phase") == "RESOLVED_SUCCEEDED",
        "state_is_deployed": (result.get("runtime_snapshot") or {}).get("value") == "DEPLOYED",
        "one_ledger_event": len((result.get("runtime_snapshot") or {}).get("ledger") or []) == 1,
        "resource_lock_acquired": lock.get("acquired") is True,
    }, result)


def assess_lock_contention(result: dict[str, Any], child_returncode: int) -> dict[str, Any]:
    lock = result.get("lock_evidence") or {}
    return _case("CONCURRENT_SECOND_PROCESS_FAILS_CLOSED", {
        "child_exit_is_pending": child_returncode == 2,
        "status_pending": result.get("status") == "PENDING",
        "lock_timeout_branch": result.get("execution_branch") == "CONCURRENT_OPERATION_LOCK_TIMEOUT",
        "completion_source_concurrent": result.get("completion_source") == "CONCURRENT_OPERATION_IN_PROGRESS",
        "zero_dispatches": result.get("dispatch_count") == 0,
        "zero_writes": result.get("applied_count") == 0,
        "no_final_acceptance": result.get("final_acceptance") is None,
        "lock_timeout_evidence_present": bool(lock.get("error")),
    }, {"child_returncode": child_returncode, **result})


def _run_unit_suite() -> dict[str, Any]:
    cmd = [sys.executable, "-m", "unittest", *UNIT_MODULES, "-v"]
    completed = subprocess.run(
        cmd,
        cwd=Path(__file__).resolve().parent,
        capture_output=True,
        text=True,
        check=False,
    )
    combined = (completed.stdout or "") + (completed.stderr or "")
    return {
        "status": "PASS" if completed.returncode == 0 else "FAIL",
        "returncode": completed.returncode,
        "command": cmd,
        "modules": UNIT_MODULES,
        "output_tail": combined[-16000:],
    }


def _seed_unresolved_dispatch(state_file: Path, *, apply_effect: bool) -> None:
    runtime = FileBackedValueRuntime(state_file)
    loaded = live._resolve_operation_manifest(None)
    operation = loaded.operation
    authority_path, authority_pin = live._resolve_authority_config(None, None)
    authority = PinnedFileAuthorityProvider(authority_path, authority_pin, runtime.resolve_target_fingerprint)
    target = runtime.resolve_target_fingerprint()
    action = operation.action_spec(target)
    proof = authority.resolve_authority()
    journal = DurableCommitJournal(live._journal_path(state_file))
    journal.record_dispatch_intent(
        operation_id=operation.operation_id,
        endpoint=action.endpoint,
        tool=action.tool,
        args=action.args,
        action_fingerprint=action.action_fingerprint,
        target_fingerprint=target,
        authority_id=proof.authority_id,
    )
    if apply_effect:
        receipt = runtime.execute(action, target)
        if not receipt.applied:
            raise RuntimeError("recovery fixture failed to apply simulated prior dispatch")


def _read_single_core_artifact(directory: Path) -> dict[str, Any]:
    files = sorted(directory.glob("core-live-integration-*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if len(files) != 1:
        raise RuntimeError(f"expected exactly one child core artifact in {directory}, found {len(files)}")
    return json.loads(files[0].read_text(encoding="utf-8"))["operation_result"]


def _run_lock_contention_case(log_dir: Path) -> tuple[dict[str, Any], int]:
    state_file = log_dir / f"lock-contention-state-{uuid.uuid4().hex}.json"
    child_log_dir = log_dir / f"lock-contention-child-{uuid.uuid4().hex}"
    child_log_dir.mkdir(parents=True, exist_ok=True)
    lock_path = live._lock_path(state_file)
    command = [
        sys.executable,
        str(Path(__file__).resolve().parent / "run_live.py"),
        "--state-file",
        str(state_file),
        "--lock-timeout",
        "0.10",
        "--log-dir",
        str(child_log_dir),
    ]
    with InterProcessFileLock(lock_path, timeout_seconds=1.0):
        completed = subprocess.run(
            command,
            cwd=Path(__file__).resolve().parent,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    result = _read_single_core_artifact(child_log_dir)
    result["child_stdout_tail"] = (completed.stdout or "")[-4000:]
    result["child_stderr_tail"] = (completed.stderr or "")[-4000:]
    return result, completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Run bundled DACP deterministic resolved-operation acceptance")
    parser.add_argument("--log-dir", default="gate-matrix-results")
    args = parser.parse_args()

    identity = live._repo_identity()
    if not identity["tracked_source_clean"]:
        raise RuntimeError("tracked repository source is dirty; refusing bundled acceptance")

    timestamp = live._utc_now()
    log_dir = Path(args.log_dir).resolve()
    state_file = log_dir / f"resolved-bundle-state-{uuid.uuid4().hex}.json"
    pending_state_file = log_dir / f"restart-pending-state-{uuid.uuid4().hex}.json"
    succeeded_state_file = log_dir / f"restart-succeeded-state-{uuid.uuid4().hex}.json"

    output: dict[str, Any] = {
        "schema": SCHEMA,
        "timestamp": timestamp,
        "source_commit": identity["source_commit"],
        "tracked_source_clean": identity["tracked_source_clean"],
        "commitment_path": "RESOLVED_OPERATION_DETERMINISTIC_NO_PROVIDER",
        "provider_dependency": False,
        "recovery_contract": "DURABLE_DISPATCH_INTENT_RECONCILE_BEFORE_REDISPATCH",
        "concurrency_contract": "ONE_DURABLE_RESOURCE_ONE_COMMITMENT_PROCESS_AT_A_TIME",
        "policy": {
            "one_bundle_one_upload": True,
            "provider_reserved_for_upstream_orientation": True,
            "lock_contention_fails_pending_without_dispatch": True,
        },
        "unit_gate": _run_unit_suite(),
        "cases": [],
        "all_passed": False,
    }

    if output["unit_gate"]["status"] != "PASS":
        path = log_dir / f"conditional-acceptance-{timestamp.replace(':', '').replace('-', '')}.json"
        _write_verified_json(path, output)
        print(json.dumps(output, indent=2, sort_keys=True))
        print(f"RESULT_FILE={path}")
        print(f"RESULT_SHA256={_sha256_file(path)}")
        return 1

    mutation = live._run_resolved("file", str(state_file), None, None, None)
    mutation_case = assess_mutation(mutation)
    output["cases"].append(mutation_case)

    if mutation_case["status"] == "PASS":
        stable_hash = mutation["runtime_evidence"]["post_state_sha256"]
        replay = live._run_resolved("file", str(state_file), None, None, None)
        output["cases"].append(assess_preexisting(replay, stable_hash))

    _seed_unresolved_dispatch(pending_state_file, apply_effect=False)
    pending_recovery = live._run_resolved("file", str(pending_state_file), None, None, None)
    output["cases"].append(assess_recovery_pending(pending_recovery))

    _seed_unresolved_dispatch(succeeded_state_file, apply_effect=True)
    succeeded_recovery = live._run_resolved("file", str(succeeded_state_file), None, None, None)
    output["cases"].append(assess_recovery_succeeded(succeeded_recovery))

    contention_result, contention_returncode = _run_lock_contention_case(log_dir)
    output["cases"].append(assess_lock_contention(contention_result, contention_returncode))

    statuses = [case["status"] for case in output["cases"]]
    output["all_passed"] = len(statuses) == 5 and all(status == "PASS" for status in statuses)
    output["summary"] = {
        "pass_count": sum(status == "PASS" for status in statuses),
        "fail_count": sum(status == "FAIL" for status in statuses),
        "case_count": len(statuses),
    }

    path = log_dir / f"conditional-acceptance-{timestamp.replace(':', '').replace('-', '')}.json"
    _write_verified_json(path, output)
    print("=== DACP_CONDITIONAL_ACCEPTANCE_BEGIN ===")
    print(json.dumps(output, indent=2, sort_keys=True))
    print("=== DACP_CONDITIONAL_ACCEPTANCE_END ===")
    print(f"RESULT_FILE={path}")
    print(f"RESULT_SHA256={_sha256_file(path)}")
    return 0 if output["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
