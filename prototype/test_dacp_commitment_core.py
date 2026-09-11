import unittest

from dacp_commitment_core import (
    Acceptance,
    ActionSpec,
    AuthorityProof,
    BoundaryTrace,
    CommitmentCore,
    Declaration,
    ExecutionReceipt,
    Outcome,
    Phase,
    Reconstruction,
    TraceIntegrity,
    VerifierSpec,
    VerificationReceipt,
)


def verifier_policy(verifier, action):
    if verifier.tool != "READ_STATE":
        return False, "verifier must use READ_STATE"
    if verifier.args != {}:
        return False, "READ_STATE verifier takes no args"
    return True, None


def make_action(value="DEPLOYED", target="tracked-value@v0"):
    return ActionSpec(
        endpoint="tracked-value",
        tool="SET_STATE",
        args={"value": value},
        target_fingerprint=target,
    )


def make_authority(action, *, authority_id="AUTH-1", revoked=False, compromised=False, valid_through=100):
    return AuthorityProof(
        authority_id=authority_id,
        action_fingerprint=action.action_fingerprint,
        target_fingerprint=action.target_fingerprint,
        trust_root_id="root-1",
        valid_through_epoch=valid_through,
        revoked=revoked,
        trust_root_compromised=compromised,
    )


def make_declaration(action, authority_id="AUTH-1"):
    return Declaration(
        action=action,
        verifier=VerifierSpec(
            tool="READ_STATE",
            args={},
            expected_value=action.args["value"],
            verifier_id="verifier-read-state",
        ),
        authority_id=authority_id,
        success_evidence="independent state read equals requested value",
        rollback_or_reconciliation_plan="reconcile before retry; rollback only with fresh authority",
    )


class CommitmentCoreTests(unittest.TestCase):
    def test_happy_path_requires_verification_before_success_acceptance(self):
        action = make_action()
        authority = make_authority(action)
        core = CommitmentCore(verifier_policy)
        decision = core.predeclare(
            make_declaration(action),
            current_target_fingerprint="tracked-value@v0",
            authority=authority,
            now_epoch=1,
        )
        self.assertTrue(decision.allowed)
        self.assertEqual(core.phase, Phase.DECLARED)

        decision, receipt = core.commit(
            action,
            current_target_fingerprint="tracked-value@v0",
            authority=authority,
            now_epoch=2,
            executor=lambda a, expected: ExecutionReceipt(Outcome.SUCCEEDED, {"ok": True}, applied=True),
        )
        self.assertTrue(decision.allowed)
        self.assertEqual(core.dispatch_count, 1)
        self.assertEqual(core.final_outcome, Outcome.PENDING)

        core.reconcile(VerificationReceipt(Outcome.SUCCEEDED, "DEPLOYED", "state-store", True))
        core.compare_oracle(VerificationReceipt(Outcome.SUCCEEDED, "DEPLOYED", "ledger-oracle", True))
        report = core.report(Outcome.SUCCEEDED)
        self.assertEqual(report.acceptance, Acceptance.VERIFIED_SUCCEEDED)

    def test_stale_target_blocks_before_executor(self):
        action = make_action()
        authority = make_authority(action)
        core = CommitmentCore(verifier_policy)
        core.predeclare(make_declaration(action), current_target_fingerprint="tracked-value@v0", authority=authority, now_epoch=1)
        calls = []
        decision, receipt = core.commit(
            action,
            current_target_fingerprint="tracked-value@v1",
            authority=authority,
            now_epoch=2,
            executor=lambda a, expected: calls.append(1),
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.code, "TARGET_CHANGED_BEFORE_COMMIT")
        self.assertEqual(core.phase, Phase.REBIND_REQUIRED)
        self.assertEqual(calls, [])
        self.assertIsNone(receipt)

    def test_revoked_authority_blocks_at_commit(self):
        action = make_action()
        initial = make_authority(action)
        revoked = make_authority(action, revoked=True)
        core = CommitmentCore(verifier_policy)
        core.predeclare(make_declaration(action), current_target_fingerprint="tracked-value@v0", authority=initial, now_epoch=1)
        decision, receipt = core.commit(
            action,
            current_target_fingerprint="tracked-value@v0",
            authority=revoked,
            now_epoch=2,
            executor=lambda a, expected: ExecutionReceipt(Outcome.SUCCEEDED, {}, applied=True),
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.code, "APPROVAL_REVOKED")
        self.assertEqual(core.dispatch_count, 0)
        self.assertIsNone(receipt)

    def test_atomic_precondition_failure_requires_rebind(self):
        action = make_action()
        authority = make_authority(action)
        core = CommitmentCore(verifier_policy)
        core.predeclare(make_declaration(action), current_target_fingerprint="tracked-value@v0", authority=authority, now_epoch=1)
        decision, _ = core.commit(
            action,
            current_target_fingerprint="tracked-value@v0",
            authority=authority,
            now_epoch=2,
            executor=lambda a, expected: ExecutionReceipt(
                Outcome.FAILED,
                {"error": "PRECONDITION_FAILED"},
                applied=False,
                precondition_failed=True,
            ),
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.code, "ATOMIC_PRECONDITION_FAILED")
        self.assertEqual(core.phase, Phase.REBIND_REQUIRED)
        self.assertEqual(core.applied_count, 0)

    def test_pending_outcome_blocks_duplicate_dispatch_until_reconciled(self):
        action = make_action()
        authority = make_authority(action)
        core = CommitmentCore(verifier_policy)
        core.predeclare(make_declaration(action), current_target_fingerprint="tracked-value@v0", authority=authority, now_epoch=1)
        decision, _ = core.commit(
            action,
            current_target_fingerprint="tracked-value@v0",
            authority=authority,
            now_epoch=2,
            executor=lambda a, expected: ExecutionReceipt(Outcome.PENDING, {"lost": True}, applied=None),
        )
        self.assertEqual(decision.code, "OUTCOME_PENDING")
        retry_decision, retry_receipt = core.commit(
            action,
            current_target_fingerprint="tracked-value@v0",
            authority=authority,
            now_epoch=3,
            executor=lambda a, expected: ExecutionReceipt(Outcome.SUCCEEDED, {}, applied=True),
        )
        self.assertFalse(retry_decision.allowed)
        self.assertEqual(retry_decision.code, "DUPLICATE_CONSEQUENTIAL_BLOCKED")
        self.assertIsNone(retry_receipt)
        self.assertEqual(core.dispatch_count, 1)

        core.reconcile(VerificationReceipt(Outcome.PENDING, "INITIAL", "state-store", True, terminal=False))
        report = core.report(Outcome.PENDING)
        self.assertEqual(report.acceptance, Acceptance.PENDING)

    def test_verifier_oracle_conflict_rejects_completion(self):
        action = make_action()
        authority = make_authority(action)
        core = CommitmentCore(verifier_policy)
        core.predeclare(make_declaration(action), current_target_fingerprint="tracked-value@v0", authority=authority, now_epoch=1)
        core.commit(
            action,
            current_target_fingerprint="tracked-value@v0",
            authority=authority,
            now_epoch=2,
            executor=lambda a, expected: ExecutionReceipt(Outcome.SUCCEEDED, {"applied": True}, applied=True),
        )
        core.reconcile(VerificationReceipt(Outcome.SUCCEEDED, "DEPLOYED", "declared-verifier", True))
        decision = core.compare_oracle(VerificationReceipt(Outcome.FAILED, "INITIAL", "ledger-oracle", True))
        self.assertEqual(decision.code, "VERIFIER_ORACLE_CONFLICT")
        report = core.report(Outcome.SUCCEEDED)
        self.assertEqual(report.actual, Outcome.FAILED)
        self.assertEqual(report.acceptance, Acceptance.REJECTED_VERIFICATION_CONFLICT)

    def test_nonindependent_verifier_is_rejected(self):
        action = make_action()
        authority = make_authority(action)
        core = CommitmentCore(verifier_policy)
        core.predeclare(make_declaration(action), current_target_fingerprint="tracked-value@v0", authority=authority, now_epoch=1)
        core.commit(
            action,
            current_target_fingerprint="tracked-value@v0",
            authority=authority,
            now_epoch=2,
            executor=lambda a, expected: ExecutionReceipt(Outcome.SUCCEEDED, {}, applied=True),
        )
        decision = core.reconcile(VerificationReceipt(Outcome.SUCCEEDED, "DEPLOYED", "executor", False))
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.code, "NONINDEPENDENT_VERIFICATION_BLOCKED")

    def test_boundary_trace_snapshot_detects_and_reconstructs_tampering(self):
        event = {"event_id": "EVT-1", "sequence": 1, "result": "FAILED", "value": "INITIAL"}
        anchor = BoundaryTrace.anchor(event, keep_protected_snapshot=True)
        local = [{"event_id": "EVT-1", "sequence": 1, "result": "SUCCEEDED", "value": "DEPLOYED"}]
        check = BoundaryTrace.verify(local, anchor)
        self.assertEqual(check.integrity, TraceIntegrity.TAMPER_DETECTED)
        self.assertEqual(check.reconstruction, Reconstruction.RECONSTRUCTED_FROM_PROTECTED_SNAPSHOT)
        self.assertEqual(check.reconstructed_event["result"], "FAILED")

    def test_digest_only_anchor_detects_omission_but_cannot_reconstruct(self):
        event = {"event_id": "EVT-1", "sequence": 1, "result": "FAILED"}
        anchor = BoundaryTrace.anchor(event, keep_protected_snapshot=False)
        check = BoundaryTrace.verify([], anchor)
        self.assertEqual(check.integrity, TraceIntegrity.OMISSION_DETECTED)
        self.assertEqual(check.reconstruction, Reconstruction.UNRESOLVED_MISSING_EVENT_CONTENT)
        self.assertIsNone(check.reconstructed_event)


if __name__ == "__main__":
    unittest.main()
