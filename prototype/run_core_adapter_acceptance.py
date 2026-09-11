#!/usr/bin/env python3

import json
from pathlib import Path

from dacp_commitment_core import ActionSpec, AuthorityProof, ExecutionReceipt, Outcome, VerificationReceipt
from dacp_core_adapter import CoreRuntime, NativeActionAdapter

OUT = Path(__file__).resolve().parent / "gate-matrix-results" / "core-adapter-acceptance.json"


class Fixture:
    def __init__(self):
        self.value = "INITIAL"
        self.target = "tracked-value@v0"
        self.now = 1
        self.revoked = False
        self.exec_count = 0

    def bound_action(self):
        return ActionSpec("tracked-value", "SET_STATE", {"value": "DEPLOYED"}, "tracked-value@v0")

    def authority(self):
        action = self.bound_action()
        return AuthorityProof(
            "AUTH-1", action.action_fingerprint, action.target_fingerprint,
            "root-1", valid_through_epoch=100, revoked=self.revoked,
        )

    def execute(self, action, expected_target):
        self.exec_count += 1
        if expected_target != self.target:
            return ExecutionReceipt(Outcome.FAILED, {"error": "PRECONDITION_FAILED"}, False, True)
        self.value = action.args["value"]
        self.target = "tracked-value@v1"
        return ExecutionReceipt(Outcome.SUCCEEDED, {"applied": True, "value": self.value}, True)

    def verify(self, verifier):
        outcome = Outcome.SUCCEEDED if self.value == verifier.expected_value else Outcome.FAILED
        return VerificationReceipt(outcome, self.value, "state-store", True)

    def oracle(self, verifier):
        outcome = Outcome.SUCCEEDED if self.value == verifier.expected_value else Outcome.FAILED
        return VerificationReceipt(outcome, self.value, "ledger-oracle", True)

    def runtime(self):
        return CoreRuntime(
            resolve_authority=self.authority,
            resolve_target_fingerprint=lambda: self.target,
            now_epoch=lambda: self.now,
            execute=self.execute,
            verify=self.verify,
            oracle_verify=self.oracle,
            routine_read=lambda: {"value": self.value, "target_fingerprint": self.target},
        )


def predeclare():
    return {
        "action": "PREDECLARE",
        "endpoint": "tracked-value",
        "tool": "SET_STATE",
        "args": {"value": "DEPLOYED"},
        "target_fingerprint": "tracked-value@v0",
        "verifier": {"tool": "READ_STATE", "args": {}, "expected_value": "DEPLOYED"},
        "rollback": "reconcile before retry; rollback only with fresh authority",
    }


CALL = {"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}}


def scenario_happy():
    f = Fixture()
    adapter = NativeActionAdapter(f.runtime())
    d = adapter.handle(predeclare())
    c = adapter.handle(CALL)
    r = adapter.handle({"action": "REPORT", "result": "SUCCEEDED", "note": "done"})
    passed = (
        d.get("code") == "DECLARATION_ACCEPTED"
        and c.get("dispatch_count") == 1
        and c.get("postcondition", {}).get("outcome_classification") == "SUCCEEDED"
        and r.get("acceptance") == "VERIFIED_SUCCEEDED"
        and f.exec_count == 1
    )
    return {
        "scenario": "adapter_verified_success",
        "pass": passed,
        "declaration_code": d.get("code"),
        "dispatch_count": c.get("dispatch_count"),
        "classification": c.get("postcondition", {}).get("outcome_classification"),
        "acceptance": r.get("acceptance"),
    }


def scenario_revoked():
    f = Fixture()
    adapter = NativeActionAdapter(f.runtime())
    adapter.handle(predeclare())
    f.revoked = True
    f.now = 2
    c = adapter.handle(CALL)
    passed = c.get("code") == "APPROVAL_REVOKED" and c.get("dispatch_count") == 0 and f.exec_count == 0
    return {
        "scenario": "adapter_authority_revoked_at_commit",
        "pass": passed,
        "code": c.get("code"),
        "dispatch_count": c.get("dispatch_count"),
    }


def scenario_stale():
    f = Fixture()
    adapter = NativeActionAdapter(f.runtime())
    adapter.handle(predeclare())
    f.target = "tracked-value@v1"
    c = adapter.handle(CALL)
    passed = c.get("code") == "TARGET_CHANGED_BEFORE_COMMIT" and c.get("dispatch_count") == 0 and f.exec_count == 0
    return {
        "scenario": "adapter_stale_target_revalidation",
        "pass": passed,
        "code": c.get("code"),
        "dispatch_count": c.get("dispatch_count"),
    }


def scenario_pending_duplicate():
    f = Fixture()
    runtime = f.runtime()

    def pending_execute(action, expected_target):
        f.exec_count += 1
        return ExecutionReceipt(Outcome.PENDING, {"lost": True}, None)

    runtime.execute = pending_execute
    adapter = NativeActionAdapter(runtime)
    adapter.handle(predeclare())
    first = adapter.handle(CALL)
    second = adapter.handle(CALL)
    passed = (
        first.get("code") == "OUTCOME_PENDING"
        and second.get("code") == "DUPLICATE_CONSEQUENTIAL_BLOCKED"
        and first.get("dispatch_count") == 1
        and second.get("dispatch_count") == 1
        and f.exec_count == 1
    )
    return {
        "scenario": "adapter_uncertain_duplicate_suppression",
        "pass": passed,
        "first_code": first.get("code"),
        "retry_code": second.get("code"),
        "dispatch_count": second.get("dispatch_count"),
    }


def main():
    scenarios = [scenario_happy(), scenario_revoked(), scenario_stale(), scenario_pending_duplicate()]
    payload = {
        "schema": "dacp-core-adapter-acceptance-0.1",
        "scenarios": scenarios,
        "all_passed": all(s["pass"] for s in scenarios),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["all_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
