import unittest

from dacp_authority_provider import AuthorityGrant, StaticAuthorityProvider
from dacp_control_session import OperationSpec
from dacp_core_live_runtime import VersionedValueRuntime
from dacp_resolved_operation import DACPResolvedOperation
from dacp_runtime_contract import bind_core_runtime


def operation(value="DEPLOYED"):
    return OperationSpec(
        operation_id="resolved-op",
        task=f"Set tracked value to {value}.",
        endpoint="tracked-value",
        tool="SET_STATE",
        args={"value": value},
        verifier_tool="READ_STATE",
        verifier_args={},
        expected_value=value,
        rollback_or_reconciliation_plan="reconcile before retry; rollback only with fresh authority.",
    )


def authority(runtime, value="DEPLOYED"):
    grant = AuthorityGrant(
        authority_id="AUTH-RESOLVED-001",
        trust_root_id="resolved-test-root",
        endpoint="tracked-value",
        tool="SET_STATE",
        args={"value": value},
        valid_through_epoch=4102444800,
        revoked=False,
    )
    return StaticAuthorityProvider(grant, runtime.resolve_target_fingerprint)


class ResolvedOperationTests(unittest.TestCase):
    def test_unsatisfied_operation_commits_directly_without_provider(self):
        runtime = VersionedValueRuntime()
        result = DACPResolvedOperation(
            operation(), bind_core_runtime(runtime, authority(runtime), now_epoch=lambda: 1)
        ).run()
        self.assertEqual(result.execution_branch, "MUTATION_REQUIRED")
        self.assertEqual(result.terminal_state, "REPORTED")
        self.assertEqual(result.final_acceptance, "VERIFIED_SUCCEEDED")
        self.assertEqual(result.completion_source, "CONTROL_PLANE_DIRECT_COMMIT")
        self.assertEqual(result.dispatch_count, 1)
        self.assertEqual(result.applied_count, 1)
        self.assertFalse(result.verification_conflict)
        self.assertEqual(runtime.value, "DEPLOYED")

    def test_preexisting_operation_uses_zero_dispatches(self):
        runtime = VersionedValueRuntime(initial_value="DEPLOYED")
        result = DACPResolvedOperation(
            operation(), bind_core_runtime(runtime, authority(runtime), now_epoch=lambda: 1)
        ).run()
        self.assertEqual(result.execution_branch, "PREEXISTING_VERIFIED_NO_DISPATCH")
        self.assertEqual(result.final_acceptance, "VERIFIED_SUCCEEDED")
        self.assertEqual(result.dispatch_count, 0)
        self.assertEqual(result.applied_count, 0)

    def test_mismatched_authority_blocks_before_dispatch(self):
        runtime = VersionedValueRuntime()
        result = DACPResolvedOperation(
            operation("UNAUTHORIZED"),
            bind_core_runtime(runtime, authority(runtime, "DEPLOYED"), now_epoch=lambda: 1),
        ).run()
        self.assertEqual(result.execution_branch, "CONTROL_BLOCKED")
        self.assertEqual(result.dispatch_count, 0)
        self.assertEqual(result.applied_count, 0)
        self.assertEqual(runtime.value, "INITIAL")


if __name__ == "__main__":
    unittest.main()
