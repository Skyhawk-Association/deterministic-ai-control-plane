import unittest

from dacp_commitment_core import Outcome
from dacp_core_adapter import CoreRuntime, NativeActionAdapter
from dacp_core_live_runtime import VersionedValueRuntime


class CoreLiveRuntimeTests(unittest.TestCase):
    def make_adapter(self):
        runtime = VersionedValueRuntime()
        adapter = NativeActionAdapter(
            CoreRuntime(
                resolve_authority=runtime.resolve_authority,
                resolve_target_fingerprint=runtime.resolve_target_fingerprint,
                now_epoch=lambda: 1,
                execute=runtime.execute,
                verify=runtime.verify,
                oracle_verify=runtime.oracle_verify,
                routine_read=runtime.routine_read,
            )
        )
        return runtime, adapter

    def valid_predeclare(self):
        return {
            "action": "PREDECLARE",
            "endpoint": "tracked-value",
            "tool": "SET_STATE",
            "args": {"value": "DEPLOYED"},
            "target_fingerprint": "tracked-value@v0",
            "verifier": {
                "tool": "READ_STATE",
                "args": {},
                "expected_value": "DEPLOYED",
            },
            "rollback": "reconcile before retry; rollback only with fresh authority",
        }

    def test_live_runtime_success_path(self):
        runtime, adapter = self.make_adapter()
        declared = adapter.handle(self.valid_predeclare())
        self.assertTrue(declared["allowed"])
        self.assertEqual(declared["code"], "DECLARATION_ACCEPTED")

        committed = adapter.handle({
            "action": "CALL",
            "tool": "SET_STATE",
            "args": {"value": "DEPLOYED"},
        })
        self.assertTrue(committed["allowed"])
        self.assertEqual(committed["dispatch_count"], 1)
        self.assertEqual(runtime.value, "DEPLOYED")
        self.assertEqual(runtime.version, 1)
        self.assertEqual(len(runtime.ledger), 1)
        self.assertEqual(committed["postcondition"]["outcome_classification"], "SUCCEEDED")
        self.assertFalse(committed["postcondition"]["verification_conflict"])

        reported = adapter.handle({
            "action": "REPORT",
            "result": "SUCCEEDED",
            "note": "verified",
        })
        self.assertEqual(reported["acceptance"], "VERIFIED_SUCCEEDED")

    def test_revocation_between_declare_and_commit_blocks_executor(self):
        runtime, adapter = self.make_adapter()
        self.assertTrue(adapter.handle(self.valid_predeclare())["allowed"])
        runtime.authority_revoked = True
        committed = adapter.handle({
            "action": "CALL",
            "tool": "SET_STATE",
            "args": {"value": "DEPLOYED"},
        })
        self.assertFalse(committed["allowed"])
        self.assertEqual(committed["code"], "APPROVAL_REVOKED")
        self.assertEqual(committed["dispatch_count"], 0)
        self.assertEqual(runtime.value, "INITIAL")
        self.assertEqual(runtime.ledger, [])

    def test_stale_target_between_declare_and_commit_blocks_executor(self):
        runtime, adapter = self.make_adapter()
        self.assertTrue(adapter.handle(self.valid_predeclare())["allowed"])
        runtime.version = 1
        runtime.value = "CONCURRENT"
        committed = adapter.handle({
            "action": "CALL",
            "tool": "SET_STATE",
            "args": {"value": "DEPLOYED"},
        })
        self.assertFalse(committed["allowed"])
        self.assertEqual(committed["code"], "TARGET_CHANGED_BEFORE_COMMIT")
        self.assertEqual(committed["dispatch_count"], 0)
        self.assertEqual(runtime.value, "CONCURRENT")

    def test_oracle_matches_direct_state_after_commit(self):
        runtime, adapter = self.make_adapter()
        adapter.handle(self.valid_predeclare())
        committed = adapter.handle({
            "action": "CALL",
            "tool": "SET_STATE",
            "args": {"value": "DEPLOYED"},
        })
        postcondition = committed["postcondition"]
        self.assertEqual(postcondition["verification"]["outcome"], Outcome.SUCCEEDED.value)
        self.assertEqual(postcondition["oracle"]["outcome"], Outcome.SUCCEEDED.value)
        self.assertEqual(postcondition["oracle"]["code"], "VERIFIER_ORACLE_MATCH")


if __name__ == "__main__":
    unittest.main()
