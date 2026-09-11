import unittest

from dacp_commitment_core import ActionSpec, AuthorityProof, ExecutionReceipt, Outcome, VerificationReceipt
from dacp_core_adapter import CoreRuntime, NativeActionAdapter


class Fixture:
    def __init__(self):
        self.value = "INITIAL"
        self.target = "tracked-value@v0"
        self.now = 1
        self.revoked = False
        self.exec_count = 0

    def declaration_action(self):
        return ActionSpec(
            endpoint="tracked-value",
            tool="SET_STATE",
            args={"value": "DEPLOYED"},
            target_fingerprint="tracked-value@v0",
        )

    def authority(self):
        action = self.declaration_action()
        return AuthorityProof(
            authority_id="AUTH-1",
            action_fingerprint=action.action_fingerprint,
            target_fingerprint=action.target_fingerprint,
            trust_root_id="root-1",
            valid_through_epoch=100,
            revoked=self.revoked,
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


def predeclare_action():
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


class NativeActionAdapterTests(unittest.TestCase):
    def test_happy_path_auto_verifies_and_accepts_report(self):
        f = Fixture()
        adapter = NativeActionAdapter(f.runtime())

        declared = adapter.handle(predeclare_action())
        self.assertTrue(declared["allowed"])
        self.assertEqual(declared["code"], "DECLARATION_ACCEPTED")

        called = adapter.handle(CALL)
        self.assertTrue(called["allowed"])
        self.assertEqual(called["dispatch_count"], 1)
        self.assertEqual(called["postcondition"]["outcome_classification"], "SUCCEEDED")
        self.assertFalse(called["postcondition"]["verification_conflict"])
        self.assertEqual(f.exec_count, 1)

        reported = adapter.handle({"action": "REPORT", "result": "SUCCEEDED", "note": "done"})
        self.assertEqual(reported["acceptance"], "VERIFIED_SUCCEEDED")
        self.assertEqual(reported["dispatch_count"], 1)

    def test_revoked_authority_between_declare_and_call_blocks_execution(self):
        f = Fixture()
        adapter = NativeActionAdapter(f.runtime())
        self.assertTrue(adapter.handle(predeclare_action())["allowed"])
        f.revoked = True
        f.now = 2

        called = adapter.handle(CALL)
        self.assertFalse(called["allowed"])
        self.assertEqual(called["code"], "APPROVAL_REVOKED")
        self.assertEqual(called["dispatch_count"], 0)
        self.assertEqual(f.exec_count, 0)

    def test_stale_target_between_declare_and_call_blocks_execution(self):
        f = Fixture()
        adapter = NativeActionAdapter(f.runtime())
        self.assertTrue(adapter.handle(predeclare_action())["allowed"])
        f.target = "tracked-value@v1"

        called = adapter.handle(CALL)
        self.assertFalse(called["allowed"])
        self.assertEqual(called["code"], "TARGET_CHANGED_BEFORE_COMMIT")
        self.assertEqual(called["dispatch_count"], 0)
        self.assertEqual(f.exec_count, 0)

    def test_pending_executor_blocks_duplicate_and_allows_reconciliation(self):
        f = Fixture()

        def pending_execute(action, expected_target):
            f.exec_count += 1
            return ExecutionReceipt(Outcome.PENDING, {"lost": True}, None)

        runtime = f.runtime()
        runtime.execute = pending_execute
        adapter = NativeActionAdapter(runtime)
        self.assertTrue(adapter.handle(predeclare_action())["allowed"])

        first = adapter.handle(CALL)
        self.assertEqual(first["code"], "OUTCOME_PENDING")
        self.assertEqual(first["dispatch_count"], 1)

        retry = adapter.handle(CALL)
        self.assertFalse(retry["allowed"])
        self.assertEqual(retry["code"], "DUPLICATE_CONSEQUENTIAL_BLOCKED")
        self.assertEqual(f.exec_count, 1)

        read = adapter.handle({"action": "CALL", "tool": "READ_STATE", "args": {}})
        self.assertEqual(read["outcome_classification"], "FAILED")

    def test_invalid_verifier_tool_never_reaches_core_commit(self):
        f = Fixture()
        adapter = NativeActionAdapter(f.runtime())
        bad = predeclare_action()
        bad["verifier"] = {"tool": "SET_STATE", "args": {"value": "DEPLOYED"}, "expected_value": "DEPLOYED"}
        result = adapter.handle(bad)
        self.assertFalse(result["allowed"])
        self.assertEqual(result["code"], "INVALID_DECLARATION")
        self.assertEqual(f.exec_count, 0)


if __name__ == "__main__":
    unittest.main()
