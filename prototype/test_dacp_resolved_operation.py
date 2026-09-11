import tempfile
import unittest
from pathlib import Path

from dacp_authority_provider import AuthorityGrant, StaticAuthorityProvider
from dacp_commit_journal import DurableCommitJournal
from dacp_control_session import OperationSpec
from dacp_core_live_runtime import VersionedValueRuntime
from dacp_file_runtime import FileBackedValueRuntime
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


def seed_intent(journal, runtime, op, auth):
    target = runtime.resolve_target_fingerprint()
    action = op.action_spec(target)
    proof = auth.resolve_authority()
    return journal.record_dispatch_intent(
        operation_id=op.operation_id,
        endpoint=action.endpoint,
        tool=action.tool,
        args=action.args,
        action_fingerprint=action.action_fingerprint,
        target_fingerprint=target,
        authority_id=proof.authority_id,
    )


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

    def test_restart_with_unresolved_intent_and_no_observed_effect_does_not_redispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            journal_path = Path(tmp) / "commit-journal.json"
            op = operation()
            runtime = FileBackedValueRuntime(state_path)
            auth = authority(runtime)
            journal = DurableCommitJournal(journal_path)
            seed_intent(journal, runtime, op, auth)

            restarted_runtime = FileBackedValueRuntime(state_path)
            restarted_auth = authority(restarted_runtime)
            restarted_journal = DurableCommitJournal(journal_path)
            result = DACPResolvedOperation(
                op,
                bind_core_runtime(
                    restarted_runtime,
                    restarted_auth,
                    now_epoch=lambda: 1,
                    dispatch_journal=restarted_journal,
                    operation_id=op.operation_id,
                ),
                commit_journal=restarted_journal,
            ).run()

            self.assertEqual(result.execution_branch, "RECOVERY_PENDING_NO_REDISPATCH")
            self.assertEqual(result.terminal_state, "PENDING")
            self.assertEqual(result.dispatch_count, 0)
            self.assertEqual(result.applied_count, 0)
            self.assertEqual(restarted_runtime.evidence_snapshot()["value"], "INITIAL")
            self.assertEqual(restarted_journal.unresolved_for(op.operation_id)["phase"], "RECOVERY_PENDING")

    def test_restart_with_unresolved_intent_and_verified_effect_closes_without_redispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            journal_path = Path(tmp) / "commit-journal.json"
            op = operation()
            runtime = FileBackedValueRuntime(state_path)
            auth = authority(runtime)
            journal = DurableCommitJournal(journal_path)
            target = runtime.resolve_target_fingerprint()
            action = op.action_spec(target)
            seed_intent(journal, runtime, op, auth)
            applied = runtime.execute(action, target)
            self.assertTrue(applied.applied)

            restarted_runtime = FileBackedValueRuntime(state_path)
            restarted_auth = authority(restarted_runtime)
            restarted_journal = DurableCommitJournal(journal_path)
            result = DACPResolvedOperation(
                op,
                bind_core_runtime(
                    restarted_runtime,
                    restarted_auth,
                    now_epoch=lambda: 1,
                    dispatch_journal=restarted_journal,
                    operation_id=op.operation_id,
                ),
                commit_journal=restarted_journal,
            ).run()

            self.assertEqual(result.execution_branch, "RECOVERY_VERIFIED_NO_REDISPATCH")
            self.assertEqual(result.final_acceptance, "VERIFIED_SUCCEEDED")
            self.assertEqual(result.completion_source, "RESTART_RECONCILED_SUCCEEDED")
            self.assertEqual(result.dispatch_count, 0)
            self.assertEqual(result.applied_count, 0)
            self.assertEqual(restarted_runtime.evidence_snapshot()["value"], "DEPLOYED")
            self.assertIsNone(restarted_journal.unresolved_for(op.operation_id))


if __name__ == "__main__":
    unittest.main()
