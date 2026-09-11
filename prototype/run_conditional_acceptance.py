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

SCHEMA = "dacp-conditional-acceptance-0.3"
UNIT_MODULES = [
    "test_dacp_commitment_core.py",
    "test_dacp_core_adapter.py",
    "test_dacp_authority_provider.py",
    "test_dacp_control_session.py",
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
    return {"name": name, "status": "PASS" if not failures else "FAIL", "failures": failures, "assertions": assertions, "evidence": evidence}


def assess_mutation(result: dict[str, Any]) -> dict[str, Any]:
    snapshot = result.get("runtime_snapshot") or {}
    runtime_evidence = result.get("runtime_evidence") or {}
    authority = result.get("authority_evidence") or {}
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
        "no_verification_conflict": result.get("verification_conflict") is False,
    }, result)


def assess_preexisting(result: dict[str, Any], stable_hash: str) -> dict[str, Any]:
    runtime_evidence = result.get("runtime_evidence") or {}
    snapshot = result.get("runtime_snapshot") or {}
    check = result.get("preexisting_check") or {}
    oracle = check.get("oracle") or {}
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
        "no_verification_conflict": result.get("verification_conflict") is False,
    }, result)


def _run_unit_suite() -> dict[str, Any]:
    cmd = [sys.executable, "-m", "unittest", *UNIT_MODULES, "-v"]
    completed = subprocess.run(cmd, cwd=Path(__file__).resolve().parent, capture_output=True, text=True, check=False)
    combined = (completed.stdout or "") + (completed.stderr or "")
    return {
        "status": "PASS" if completed.returncode == 0 else "FAIL",
        "returncode": completed.returncode,
        "command": cmd,
        "modules": UNIT_MODULES,
        "output_tail": combined[-12000:],
    }


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

    output: dict[str, Any] = {
        "schema": SCHEMA,
        "timestamp": timestamp,
        "source_commit": identity["source_commit"],
        "tracked_source_clean": identity["tracked_source_clean"],
        "commitment_path": "RESOLVED_OPERATION_DETERMINISTIC_NO_PROVIDER",
        "provider_dependency": False,
        "policy": {"one_bundle_one_upload": True, "provider_reserved_for_upstream_orientation": True},
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

    statuses = [case["status"] for case in output["cases"]]
    output["all_passed"] = len(statuses) == 2 and all(status == "PASS" for status in statuses)
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
