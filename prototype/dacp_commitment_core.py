from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class Outcome(str, Enum):
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    PENDING = "PENDING"


class Phase(str, Enum):
    NEW = "NEW"
    DECLARED = "DECLARED"
    DISPATCHED = "DISPATCHED"
    PENDING = "PENDING"
    REBIND_REQUIRED = "REBIND_REQUIRED"
    VERIFIED = "VERIFIED"
    CLOSED = "CLOSED"


class Acceptance(str, Enum):
    VERIFIED_SUCCEEDED = "VERIFIED_SUCCEEDED"
    VERIFIED_FAILED = "VERIFIED_FAILED"
    PENDING = "PENDING"
    REJECTED_VERIFICATION_CONFLICT = "REJECTED_VERIFICATION_CONFLICT"
    REJECTED_CLAIM_CONFLICT = "REJECTED_CLAIM_CONFLICT"
    UNRESOLVED = "UNRESOLVED"


class TraceIntegrity(str, Enum):
    INTACT = "INTACT"
    TAMPER_DETECTED = "TAMPER_DETECTED"
    OMISSION_DETECTED = "OMISSION_DETECTED"


class Reconstruction(str, Enum):
    LOCAL_MATCHES_ANCHOR = "LOCAL_MATCHES_ANCHOR"
    RECONSTRUCTED_FROM_PROTECTED_SNAPSHOT = "RECONSTRUCTED_FROM_PROTECTED_SNAPSHOT"
    UNRESOLVED_MISSING_EVENT_CONTENT = "UNRESOLVED_MISSING_EVENT_CONTENT"
    UNRESOLVED_CONTENT_MISMATCH = "UNRESOLVED_CONTENT_MISMATCH"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ActionSpec:
    endpoint: str
    tool: str
    args: dict[str, Any]
    target_fingerprint: str

    @property
    def action_fingerprint(self) -> str:
        return sha256_json(
            {
                "endpoint": self.endpoint,
                "tool": self.tool,
                "args": self.args,
                "target_fingerprint": self.target_fingerprint,
            }
        )


@dataclass(frozen=True)
class VerifierSpec:
    tool: str
    args: dict[str, Any]
    expected_value: Any
    verifier_id: str


@dataclass(frozen=True)
class AuthorityProof:
    authority_id: str
    action_fingerprint: str
    target_fingerprint: str
    trust_root_id: str
    valid_through_epoch: int | None = None
    revoked: bool = False
    trust_root_compromised: bool = False

    def validate(self, action: ActionSpec, now_epoch: int) -> tuple[bool, str | None]:
        if self.revoked:
            return False, "APPROVAL_REVOKED"
        if self.trust_root_compromised:
            return False, "TRUST_ROOT_COMPROMISED"
        if self.valid_through_epoch is not None and now_epoch > self.valid_through_epoch:
            return False, "APPROVAL_EXPIRED"
        if self.action_fingerprint != action.action_fingerprint:
            return False, "APPROVAL_ACTION_MISMATCH"
        if self.target_fingerprint != action.target_fingerprint:
            return False, "APPROVAL_TARGET_MISMATCH"
        return True, None


@dataclass(frozen=True)
class Declaration:
    action: ActionSpec
    verifier: VerifierSpec
    authority_id: str
    success_evidence: str
    rollback_or_reconciliation_plan: str


@dataclass(frozen=True)
class ExecutionReceipt:
    outcome: Outcome
    response: dict[str, Any] = field(default_factory=dict)
    applied: bool | None = None
    precondition_failed: bool = False


@dataclass(frozen=True)
class VerificationReceipt:
    outcome: Outcome
    observed_value: Any
    source_id: str
    independent_from_executor: bool
    terminal: bool = True


@dataclass(frozen=True)
class GateDecision:
    allowed: bool
    code: str
    phase: Phase
    required_next_action: str | None = None
    detail: str | None = None


@dataclass(frozen=True)
class ReportDecision:
    claim: Outcome
    actual: Outcome
    acceptance: Acceptance


VerifierPolicy = Callable[[VerifierSpec, ActionSpec], tuple[bool, str | None]]
Executor = Callable[[ActionSpec, str], ExecutionReceipt]


class CommitmentCore:
    """Provider-neutral deterministic commitment state machine."""

    def __init__(self, verifier_policy: VerifierPolicy):
        self.verifier_policy = verifier_policy
        self.phase = Phase.NEW
        self.declaration: Declaration | None = None
        self.dispatch_count = 0
        self.applied_count = 0
        self.reconciliation_count = 0
        self.last_execution: ExecutionReceipt | None = None
        self.final_outcome = Outcome.PENDING
        self.verification_conflict = False
        self.verifier_receipt: VerificationReceipt | None = None
        self.oracle_receipt: VerificationReceipt | None = None
        self.events: list[dict[str, Any]] = []

    def _record(self, event: str, **fields: Any) -> None:
        self.events.append({"sequence": len(self.events) + 1, "event": event, **fields})

    def predeclare(
        self,
        declaration: Declaration,
        *,
        current_target_fingerprint: str,
        authority: AuthorityProof,
        now_epoch: int,
    ) -> GateDecision:
        if self.phase in {Phase.DISPATCHED, Phase.PENDING, Phase.VERIFIED, Phase.CLOSED}:
            return GateDecision(False, "POST_DISPATCH_DECLARATION_BLOCKED", self.phase, "REPORT_OR_RECONCILE")
        if declaration.action.target_fingerprint != current_target_fingerprint:
            self.phase = Phase.REBIND_REQUIRED
            return GateDecision(False, "STALE_TARGET_AT_DECLARATION", self.phase, "PREDECLARE")
        if declaration.authority_id != authority.authority_id:
            return GateDecision(False, "AUTHORITY_ID_MISMATCH", self.phase, "PREDECLARE")
        authority_ok, authority_reason = authority.validate(declaration.action, now_epoch)
        if not authority_ok:
            return GateDecision(False, authority_reason or "AUTHORITY_BLOCKED", self.phase, "REPORT")
        verifier_ok, verifier_reason = self.verifier_policy(declaration.verifier, declaration.action)
        if not verifier_ok:
            return GateDecision(False, "INVALID_VERIFIER_CONTRACT", self.phase, "PREDECLARE", verifier_reason)
        if not declaration.success_evidence.strip():
            return GateDecision(False, "SUCCESS_EVIDENCE_REQUIRED", self.phase, "PREDECLARE")
        if not declaration.rollback_or_reconciliation_plan.strip():
            return GateDecision(False, "RECOVERY_PLAN_REQUIRED", self.phase, "PREDECLARE")

        self.declaration = declaration
        self.phase = Phase.DECLARED
        self._record(
            "DECLARED",
            authority_id=authority.authority_id,
            action_fingerprint=declaration.action.action_fingerprint,
            target_fingerprint=current_target_fingerprint,
            verifier_id=declaration.verifier.verifier_id,
        )
        return GateDecision(True, "DECLARATION_ACCEPTED", self.phase, "CHECK_OR_CALL")

    def verify_preexisting(self, verifier_receipt: VerificationReceipt) -> GateDecision:
        """Check whether the declared postcondition is already independently satisfied.

        This is a no-dispatch fast path. Failure to prove the postcondition leaves the
        declaration intact for normal commit. Success still requires oracle comparison
        before final acceptance.
        """
        if self.phase != Phase.DECLARED or self.declaration is None:
            return GateDecision(False, "PREEXISTING_CHECK_NOT_ALLOWED", self.phase, "PREDECLARE")
        if not verifier_receipt.independent_from_executor:
            return GateDecision(False, "NONINDEPENDENT_PREEXISTING_VERIFICATION_BLOCKED", self.phase, "CALL")

        expected = self.declaration.verifier.expected_value
        satisfied = (
            verifier_receipt.outcome == Outcome.SUCCEEDED
            and verifier_receipt.terminal
            and verifier_receipt.observed_value == expected
        )
        self._record(
            "PREEXISTING_CHECK",
            source_id=verifier_receipt.source_id,
            outcome=verifier_receipt.outcome.value,
            observed_value=verifier_receipt.observed_value,
            terminal=verifier_receipt.terminal,
            satisfied=satisfied,
        )
        if not satisfied:
            self.verifier_receipt = None
            self.oracle_receipt = None
            self.final_outcome = Outcome.PENDING
            return GateDecision(True, "PREEXISTING_POSTCONDITION_NOT_SATISFIED", self.phase, "CALL")

        self.verifier_receipt = verifier_receipt
        self.final_outcome = Outcome.SUCCEEDED
        self.phase = Phase.VERIFIED
        return GateDecision(True, "PREEXISTING_POSTCONDITION_VERIFIED", self.phase, "ORACLE")

    def commit(
        self,
        action: ActionSpec,
        *,
        current_target_fingerprint: str,
        authority: AuthorityProof,
        now_epoch: int,
        executor: Executor,
    ) -> tuple[GateDecision, ExecutionReceipt | None]:
        if self.phase in {Phase.PENDING, Phase.DISPATCHED, Phase.VERIFIED, Phase.CLOSED}:
            return GateDecision(False, "DUPLICATE_CONSEQUENTIAL_BLOCKED", self.phase, "RECONCILE_OR_REPORT"), None
        if self.declaration is None or self.phase != Phase.DECLARED:
            return GateDecision(False, "GATE_BLOCKED_NO_DECLARATION", self.phase, "PREDECLARE"), None
        if action.action_fingerprint != self.declaration.action.action_fingerprint:
            return GateDecision(False, "DECLARATION_ACTION_MISMATCH", self.phase, "PREDECLARE"), None
        if current_target_fingerprint != self.declaration.action.target_fingerprint:
            self.declaration = None
            self.phase = Phase.REBIND_REQUIRED
            self._record(
                "TARGET_REVALIDATION_BLOCK",
                declared_target=action.target_fingerprint,
                current_target=current_target_fingerprint,
            )
            return GateDecision(False, "TARGET_CHANGED_BEFORE_COMMIT", self.phase, "PREDECLARE"), None
        if authority.authority_id != self.declaration.authority_id:
            return GateDecision(False, "AUTHORITY_ID_MISMATCH", self.phase, "REPORT"), None
        authority_ok, authority_reason = authority.validate(action, now_epoch)
        if not authority_ok:
            self._record("AUTHORITY_REVALIDATION_BLOCK", reason=authority_reason)
            return GateDecision(False, authority_reason or "AUTHORITY_BLOCKED", self.phase, "REPORT"), None

        self.dispatch_count += 1
        receipt = executor(action, action.target_fingerprint)
        self.last_execution = receipt
        self._record(
            "DISPATCHED",
            dispatch_count=self.dispatch_count,
            outcome=receipt.outcome.value,
            applied=receipt.applied,
            precondition_failed=receipt.precondition_failed,
        )

        if receipt.precondition_failed:
            self.declaration = None
            self.phase = Phase.REBIND_REQUIRED
            self.final_outcome = Outcome.PENDING
            return GateDecision(False, "ATOMIC_PRECONDITION_FAILED", self.phase, "PREDECLARE"), receipt

        if receipt.applied is True:
            self.applied_count += 1

        if receipt.outcome == Outcome.PENDING:
            self.phase = Phase.PENDING
            self.final_outcome = Outcome.PENDING
            return GateDecision(True, "OUTCOME_PENDING", self.phase, "RECONCILE"), receipt

        self.phase = Phase.DISPATCHED
        self.final_outcome = Outcome.PENDING
        return GateDecision(True, "DISPATCH_COMPLETE_VERIFICATION_REQUIRED", self.phase, "VERIFY"), receipt

    def reconcile(self, verifier_receipt: VerificationReceipt) -> GateDecision:
        if self.phase not in {Phase.PENDING, Phase.DISPATCHED}:
            return GateDecision(False, "RECONCILIATION_NOT_ALLOWED", self.phase)
        if self.declaration is None:
            return GateDecision(False, "DECLARATION_MISSING", self.phase)
        if not verifier_receipt.independent_from_executor:
            return GateDecision(False, "NONINDEPENDENT_VERIFICATION_BLOCKED", self.phase)

        self.reconciliation_count += 1
        self.verifier_receipt = verifier_receipt
        expected = self.declaration.verifier.expected_value
        if verifier_receipt.outcome == Outcome.SUCCEEDED and verifier_receipt.observed_value == expected:
            self.final_outcome = Outcome.SUCCEEDED
            self.phase = Phase.VERIFIED
        elif verifier_receipt.outcome == Outcome.FAILED and verifier_receipt.terminal:
            self.final_outcome = Outcome.FAILED
            self.phase = Phase.VERIFIED
        else:
            self.final_outcome = Outcome.PENDING
            self.phase = Phase.PENDING

        self._record(
            "RECONCILED",
            source_id=verifier_receipt.source_id,
            outcome=verifier_receipt.outcome.value,
            observed_value=verifier_receipt.observed_value,
            terminal=verifier_receipt.terminal,
            classified_as=self.final_outcome.value,
        )
        next_action = "REPORT" if self.phase == Phase.VERIFIED else "RECONCILE_OR_REPORT"
        return GateDecision(True, "RECONCILIATION_RECORDED", self.phase, next_action)

    def compare_oracle(self, oracle_receipt: VerificationReceipt) -> GateDecision:
        if self.verifier_receipt is None:
            return GateDecision(False, "DECLARED_VERIFIER_NOT_EXECUTED", self.phase, "VERIFY")
        if not oracle_receipt.independent_from_executor:
            return GateDecision(False, "NONINDEPENDENT_ORACLE_BLOCKED", self.phase)
        self.oracle_receipt = oracle_receipt
        self.verification_conflict = (
            self.verifier_receipt.outcome != oracle_receipt.outcome
            or self.verifier_receipt.observed_value != oracle_receipt.observed_value
        )
        if self.verification_conflict:
            self.final_outcome = oracle_receipt.outcome
            if oracle_receipt.outcome == Outcome.PENDING:
                self.phase = Phase.PENDING
            else:
                self.phase = Phase.VERIFIED
            code = "VERIFIER_ORACLE_CONFLICT"
        else:
            if oracle_receipt.outcome == Outcome.SUCCEEDED:
                self.final_outcome = Outcome.SUCCEEDED
                self.phase = Phase.VERIFIED
            elif oracle_receipt.outcome == Outcome.FAILED and oracle_receipt.terminal:
                self.final_outcome = Outcome.FAILED
                self.phase = Phase.VERIFIED
            else:
                self.final_outcome = Outcome.PENDING
                self.phase = Phase.PENDING
            code = "VERIFIER_ORACLE_MATCH"
        self._record(
            "ORACLE_COMPARED",
            source_id=oracle_receipt.source_id,
            outcome=oracle_receipt.outcome.value,
            observed_value=oracle_receipt.observed_value,
            conflict=self.verification_conflict,
            classified_as=self.final_outcome.value,
        )
        return GateDecision(True, code, self.phase, "REPORT")

    def report(self, claim: Outcome) -> ReportDecision:
        actual = self.final_outcome
        if self.verification_conflict:
            acceptance = Acceptance.REJECTED_VERIFICATION_CONFLICT
        elif claim != actual:
            acceptance = Acceptance.REJECTED_CLAIM_CONFLICT
        elif actual == Outcome.SUCCEEDED:
            acceptance = Acceptance.VERIFIED_SUCCEEDED
        elif actual == Outcome.FAILED:
            acceptance = Acceptance.VERIFIED_FAILED
        elif actual == Outcome.PENDING:
            acceptance = Acceptance.PENDING
        else:
            acceptance = Acceptance.UNRESOLVED
        self.phase = Phase.CLOSED
        self._record("REPORTED", claim=claim.value, actual=actual.value, acceptance=acceptance.value)
        return ReportDecision(claim=claim, actual=actual, acceptance=acceptance)


@dataclass(frozen=True)
class TraceAnchor:
    event_id: str
    sequence: int
    digest: str
    protected_snapshot: dict[str, Any] | None = None


@dataclass(frozen=True)
class TraceCheck:
    integrity: TraceIntegrity
    reconstruction: Reconstruction
    reconstructed_event: dict[str, Any] | None


class BoundaryTrace:
    @staticmethod
    def anchor(event: dict[str, Any], *, keep_protected_snapshot: bool) -> TraceAnchor:
        if "event_id" not in event or "sequence" not in event:
            raise ValueError("trace event requires event_id and sequence")
        return TraceAnchor(
            event_id=str(event["event_id"]),
            sequence=int(event["sequence"]),
            digest=sha256_json(event),
            protected_snapshot=copy.deepcopy(event) if keep_protected_snapshot else None,
        )

    @staticmethod
    def verify(local_events: list[dict[str, Any]], anchor: TraceAnchor) -> TraceCheck:
        local = next((e for e in local_events if str(e.get("event_id")) == anchor.event_id), None)
        if local is None:
            if anchor.protected_snapshot is not None:
                return TraceCheck(
                    TraceIntegrity.OMISSION_DETECTED,
                    Reconstruction.RECONSTRUCTED_FROM_PROTECTED_SNAPSHOT,
                    copy.deepcopy(anchor.protected_snapshot),
                )
            return TraceCheck(
                TraceIntegrity.OMISSION_DETECTED,
                Reconstruction.UNRESOLVED_MISSING_EVENT_CONTENT,
                None,
            )
        if sha256_json(local) == anchor.digest:
            return TraceCheck(
                TraceIntegrity.INTACT,
                Reconstruction.LOCAL_MATCHES_ANCHOR,
                copy.deepcopy(local),
            )
        if anchor.protected_snapshot is not None:
            return TraceCheck(
                TraceIntegrity.TAMPER_DETECTED,
                Reconstruction.RECONSTRUCTED_FROM_PROTECTED_SNAPSHOT,
                copy.deepcopy(anchor.protected_snapshot),
            )
        return TraceCheck(
            TraceIntegrity.TAMPER_DETECTED,
            Reconstruction.UNRESOLVED_CONTENT_MISMATCH,
            None,
        )
