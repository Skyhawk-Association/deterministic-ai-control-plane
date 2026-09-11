import unittest

from dacp_authority_provider import AuthorityGrant, StaticAuthorityProvider
from dacp_commitment_core import Outcome
from dacp_core_adapter import NativeActionAdapter
from dacp_core_live_runtime import VersionedValueRuntime
from dacp_runtime_contract import bind_core_runtime


def grant():
    return AuthorityGrant(
        authority_id="AUTH-TEST-001",
        trust_root_id="test-root",
        endpoint="tracked-value",
        tool="SET_STATE",
        args={"value": "DEPLOYED"},
        valid_through_epoch=4102444800,
        revoked=False,
    )


class CoreLiveRuntimeTests(unittest.TestCase):
    def make_adapter(self):
        runtime = VersionedValueRuntime()
        authority = StaticAuthorityProvider(grant(), runtime.resolve_target_fingerprint)
        adapter = NativeActionAdapter(bind_core_runtime(runtime, authority, now_epoch=lambda: 1))
        return runtime, authority, adapter

    def valid_predeclare(self):
        return {
            "action": "PREDECLARE",
            "endpoint": "tracked-value",
            "tool": "SET_STATE",
            "args": {"value": "DEPLOYED"},
            "target_fingerprint": "tracked-value@v0",
            "verifier": {"tool": "READ_STATE", "args": {}, "expected_value": "DEPLOYED"},
            "rollback": "reconcile before retry; rollback only with fresh authority",
        }

    def test_live_runtime_success_path(self):
        runtime, authority, adapter = self.make_adapter()
        declared = adapter.handle(self.valid_predeclare())
        self.assertTrue(declared["allowed"])
        committed = adapter.handle({"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}})
        self.assertTrue(committed["allowed"])
        self.assertEqual(committed["dispatch_count"], 1)
        self.assertEqual(runtime.value, "DEPLOYED")
        self.assertEqual(runtime.version, 1)
        self.assertEqual(len(runtime.ledger), 1)
        self.assertEqual(committed["postcondition"]["outcome_classification"], "SUCCEEDED")
        self.assertFalse(committed["postcondition"]["verification_conflict"])
        reported = adapter.handle({"action": "REPORT", "result": "SUCCEEDED", "note": "verified"})
        self.assertEqual(reported["acceptance"], "VERIFIED_SUCCEEDED")

    def test_revocation_between_declare_and_commit_blocks_executor(self):
        runtime, authority, adapter = self.make_adapter()
        self.assertTrue(adapter.handle(self.valid_predeclare())["allowed"])
        authority.revoked = True
        committed = adapter.handle({"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}})
        self.assertFalse(committed["allowed"])
        self.assertEqual(committed["code"], "APPROVAL_REVOKED")
        self.assertEqual(committed["dispatch_count"], 0)
        self.assertEqual(runtime.value, "INITIAL")
        self.assertEqual(runtime.ledger, [])

    def test_stale_target_between_declare_and_commit_blocks_executor(self):
        runtime, authority, adapter = self.make_adapter()
        self.assertTrue(adapter.handle(self.valid_predeclare())["allowed"])
        runtime.version = 1
        runtime.value = "CONCURRENT"
        committed = adapter.handle({"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}})
        self.assertFalse(committed["allowed"])
        self.assertEqual(committed["code"], "TARGET_CHANGED_BEFORE_COMMIT")
        self.assertEqual(committed["dispatch_count"], 0)
        self.assertEqual(runtime.value, "CONCURRENT")

    def test_runtime_mechanics_do_not_encode_authorized_value(self):
        runtime = VersionedValueRuntime()
        from dacp_commitment_core import ActionSpec
        action = ActionSpec(runtime.endpoint, "SET_STATE", {"value": "OTHER"}, runtime.resolve_target_fingerprint())
        receipt = runtime.execute(action, runtime.resolve_target_fingerprint())
        self.assertTrue(receipt.applied)
        self.assertEqual(runtime.value, "OTHER")

    def test_oracle_matches_direct_state_after_commit(self):
        runtime, authority, adapter = self.make_adapter()
        adapter.handle(self.valid_predeclare())
        committed = adapter.handle({"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}})
        postcondition = committed["postcondition"]
        self.assertEqual(postcondition["verification"]["outcome"], Outcome.SUCCEEDED.value)
        self.assertEqual(postcondition["oracle"]["outcome"], Outcome.SUCCEEDED.value)
        self.assertEqual(postcondition["oracle"]["code"], "VERIFIER_ORACLE_MATCH")


if __name__ == "__main__":
    unittest.main()
