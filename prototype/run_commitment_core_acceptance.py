#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from dacp_commitment_core import (
    Acceptance,
    ActionSpec,
    AuthorityProof,
    BoundaryTrace,
    CommitmentCore,
    Declaration,
    ExecutionReceipt,
    Outcome,
    Reconstruction,
    TraceIntegrity,
    VerifierSpec,
    VerificationReceipt,
)


def verifier_policy(verifier, action):
    if verifier.tool != "READ_STATE" or verifier.args != {}:
        return False, "independent READ_STATE verifier required"
    return True, None


def action(value="DEPLOYED", target="tracked-value@v0"):
    return ActionSpec("tracked-value", "SET_STATE", {"value": value}, target)


def authority_for(act, **overrides):
    values = {
        "authority_id": "AUTH-1",
        "action_fingerprint": act.action_fingerprint,
        "target_fingerprint": act.target_fingerprint,
        "trust_root_id": "root-1",
        "valid_through_epoch": 100,
        "revoked": False,
        "trust_root_compromised": False,
    }
    values.update(overrides)
    return AuthorityProof(**values)


def declaration_for(act):
    return Declaration(
        action=act,
        verifier=VerifierSpec("READ_STATE", {}, act.args["value"], "verifier-read-state"),
        authority_id="AUTH-1",
        success_evidence="independent resulting-state observation",
        rollback_or_reconciliation_plan="reconcile uncertainty before retry; rollback only with fresh authority",
    )


def repo_identity():
    root = Path(__file__).resolve().parents[1]
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return {"source_commit": head, "tracked_source_clean": not bool(dirty)}


def happy_path():
    act = action()
    auth = authority_for(act)
    core = CommitmentCore(verifier_policy)
    d1 = core.predeclare(declaration_for(act), current_target_fingerprint=act.target_fingerprint, authority=auth, now_epoch=1)
    d2, _ = core.commit(
        act,
        current_target_fingerprint=act.target_fingerprint,
        authority=auth,
        now_epoch=2,
        executor=lambda a, expected: ExecutionReceipt(Outcome.SUCCEEDED, {"applied": True}, applied=True),
    )
    d3 = core.reconcile(VerificationReceipt(Outcome.SUCCEEDED, "DEPLOYED", "state-store", True))
    d4 = core.compare_oracle(VerificationReceipt(Outcome.SUCCEEDED, "DEPLOYED", "ledger-oracle", True))
    report = core.report(Outcome.SUCCEEDED)
    return {
        "scenario": "verified_success",
        "declaration_allowed": d1.allowed,
        "commit_allowed": d2.allowed,
        "verification_allowed": d3.allowed,
        "oracle_code": d4.code,
        "dispatch_count": core.dispatch_count,
        "acceptance": report.acceptance.value,
        "pass": report.acceptance == Acceptance.VERIFIED_SUCCEEDED and core.dispatch_count == 1,
    }


def revoked_at_commit():
    act = action()
    auth = authority_for(act)
    revoked = authority_for(act, revoked=True)
    core = CommitmentCore(verifier_policy)
    core.predeclare(declaration_for(act), current_target_fingerprint=act.target_fingerprint, authority=auth, now_epoch=1)
    decision, _ = core.commit(
        act,
        current_target_fingerprint=act.target_fingerprint,
        authority=revoked,
        now_epoch=2,
        executor=lambda a, expected: ExecutionReceipt(Outcome.SUCCEEDED, {}, applied=True),
    )
    return {
        "scenario": "authority_revoked_at_commit",
        "commit_allowed": decision.allowed,
        "code": decision.code,
        "dispatch_count": core.dispatch_count,
        "pass": not decision.allowed and decision.code == "APPROVAL_REVOKED" and core.dispatch_count == 0,
    }


def stale_target():
    act = action()
    auth = authority_for(act)
    core = CommitmentCore(verifier_policy)
    core.predeclare(declaration_for(act), current_target_fingerprint=act.target_fingerprint, authority=auth, now_epoch=1)
    decision, _ = core.commit(
        act,
        current_target_fingerprint="tracked-value@v1",
        authority=auth,
        now_epoch=2,
        executor=lambda a, expected: ExecutionReceipt(Outcome.SUCCEEDED, {}, applied=True),
    )
    return {
        "scenario": "stale_target_revalidation",
        "commit_allowed": decision.allowed,
        "code": decision.code,
        "dispatch_count": core.dispatch_count,
        "pass": not decision.allowed and decision.code == "TARGET_CHANGED_BEFORE_COMMIT" and core.dispatch_count == 0,
    }


def uncertain_duplicate():
    act = action()
    auth = authority_for(act)
    core = CommitmentCore(verifier_policy)
    core.predeclare(declaration_for(act), current_target_fingerprint=act.target_fingerprint, authority=auth, now_epoch=1)
    first, _ = core.commit(
        act,
        current_target_fingerprint=act.target_fingerprint,
        authority=auth,
        now_epoch=2,
        executor=lambda a, expected: ExecutionReceipt(Outcome.PENDING, {"response_lost": True}, applied=None),
    )
    second, _ = core.commit(
        act,
        current_target_fingerprint=act.target_fingerprint,
        authority=auth,
        now_epoch=3,
        executor=lambda a, expected: ExecutionReceipt(Outcome.SUCCEEDED, {}, applied=True),
    )
    core.reconcile(VerificationReceipt(Outcome.PENDING, "INITIAL", "state-store", True, terminal=False))
    report = core.report(Outcome.PENDING)
    return {
        "scenario": "uncertain_outcome_duplicate_suppression",
        "first_code": first.code,
        "retry_allowed": second.allowed,
        "retry_code": second.code,
        "dispatch_count": core.dispatch_count,
        "acceptance": report.acceptance.value,
        "pass": (
            first.code == "OUTCOME_PENDING"
            and not second.allowed
            and second.code == "DUPLICATE_CONSEQUENTIAL_BLOCKED"
            and core.dispatch_count == 1
            and report.acceptance == Acceptance.PENDING
        ),
    }


def verifier_conflict():
    act = action()
    auth = authority_for(act)
    core = CommitmentCore(verifier_policy)
    core.predeclare(declaration_for(act), current_target_fingerprint=act.target_fingerprint, authority=auth, now_epoch=1)
    core.commit(
        act,
        current_target_fingerprint=act.target_fingerprint,
        authority=auth,
        now_epoch=2,
        executor=lambda a, expected: ExecutionReceipt(Outcome.SUCCEEDED, {"applied": True}, applied=True),
    )
    core.reconcile(VerificationReceipt(Outcome.SUCCEEDED, "DEPLOYED", "declared-verifier", True))
    compare = core.compare_oracle(VerificationReceipt(Outcome.FAILED, "INITIAL", "ledger-oracle", True))
    report = core.report(Outcome.SUCCEEDED)
    return {
        "scenario": "verifier_oracle_conflict",
        "compare_code": compare.code,
        "verification_conflict": core.verification_conflict,
        "actual": report.actual.value,
        "acceptance": report.acceptance.value,
        "pass": core.verification_conflict and report.acceptance == Acceptance.REJECTED_VERIFICATION_CONFLICT,
    }


def trace_tamper():
    event = {"event_id": "EVT-1", "sequence": 1, "result": "FAILED", "value": "INITIAL"}
    anchor = BoundaryTrace.anchor(event, keep_protected_snapshot=True)
    local = [{"event_id": "EVT-1", "sequence": 1, "result": "SUCCEEDED", "value": "DEPLOYED"}]
    check = BoundaryTrace.verify(local, anchor)
    return {
        "scenario": "trace_tamper_reconstruction",
        "integrity": check.integrity.value,
        "reconstruction": check.reconstruction.value,
        "reconstructed_result": check.reconstructed_event["result"] if check.reconstructed_event else None,
        "pass": (
            check.integrity == TraceIntegrity.TAMPER_DETECTED
            and check.reconstruction == Reconstruction.RECONSTRUCTED_FROM_PROTECTED_SNAPSHOT
            and check.reconstructed_event["result"] == "FAILED"
        ),
    }


def trace_digest_only():
    event = {"event_id": "EVT-1", "sequence": 1, "result": "FAILED"}
    anchor = BoundaryTrace.anchor(event, keep_protected_snapshot=False)
    check = BoundaryTrace.verify([], anchor)
    return {
        "scenario": "trace_digest_only_omission",
        "integrity": check.integrity.value,
        "reconstruction": check.reconstruction.value,
        "reconstructed_event": check.reconstructed_event,
        "pass": (
            check.integrity == TraceIntegrity.OMISSION_DETECTED
            and check.reconstruction == Reconstruction.UNRESOLVED_MISSING_EVENT_CONTENT
            and check.reconstructed_event is None
        ),
    }


def main():
    identity = repo_identity()
    if not identity["tracked_source_clean"]:
        raise RuntimeError("tracked repository source is dirty")
    scenarios = [
        happy_path(),
        revoked_at_commit(),
        stale_target(),
        uncertain_duplicate(),
        verifier_conflict(),
        trace_tamper(),
        trace_digest_only(),
    ]
    payload = {
        "schema": "dacp-commitment-core-acceptance-0.1",
        **identity,
        "all_passed": all(item["pass"] for item in scenarios),
        "scenarios": scenarios,
    }
    path = Path("gate-matrix-results") / "commitment-core-acceptance.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    readback = json.loads(path.read_text(encoding="utf-8"))
    if readback != payload:
        raise RuntimeError("acceptance artifact readback mismatch")
    print(json.dumps(payload, indent=2, sort_keys=True))
    print(f"RESULT_FILE={path.resolve()}")
    return 0 if payload["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
