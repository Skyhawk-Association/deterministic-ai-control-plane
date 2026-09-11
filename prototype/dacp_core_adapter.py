from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from dacp_commitment_core import (
    ActionSpec,
    AuthorityProof,
    CommitmentCore,
    Declaration,
    ExecutionReceipt,
    GateDecision,
    Outcome,
    Phase,
    ReportDecision,
    VerifierSpec,
    VerificationReceipt,
)


AuthorityResolver = Callable[[], AuthorityProof]
TargetResolver = Callable[[], str]
Clock = Callable[[], int]
Executor = Callable[[ActionSpec, str], ExecutionReceipt]
Verifier = Callable[[VerifierSpec], VerificationReceipt]
RoutineRead = Callable[[], dict[str, Any]]


@dataclass
class CoreRuntime:
    resolve_authority: AuthorityResolver
    resolve_target_fingerprint: TargetResolver
    now_epoch: Clock
    execute: Executor
    verify: Verifier
    oracle_verify: Verifier | None = None
    routine_read: RoutineRead | None = None


class NativeActionAdapter:
    """Translate normalized actions into deterministic CommitmentCore operations."""

    def __init__(
        self,
        runtime: CoreRuntime,
        *,
        verifier_registry: dict[str, str] | None = None,
    ):
        self.runtime = runtime
        self.verifier_registry = verifier_registry or {"READ_STATE": "verifier-read-state"}

        def verifier_policy(verifier: VerifierSpec, action: ActionSpec) -> tuple[bool, str | None]:
            expected_id = self.verifier_registry.get(verifier.tool)
            if expected_id is None:
                return False, "verifier tool is not in gate-controlled registry"
            if verifier.verifier_id != expected_id:
                return False, "verifier identity does not match registry"
            if verifier.tool != "READ_STATE" or verifier.args != {}:
                return False, "current slice requires independent READ_STATE with no args"
            if verifier.expected_value != action.args.get("value"):
                return False, "verifier expected value must match declared postcondition"
            return True, None

        self.core = CommitmentCore(verifier_policy)

    @staticmethod
    def _decision_payload(decision: GateDecision) -> dict[str, Any]:
        return {
            "allowed": decision.allowed,
            "code": decision.code,
            "phase": decision.phase.value,
            "required_next_action": decision.required_next_action,
            "detail": decision.detail,
        }

    @staticmethod
    def _report_payload(report: ReportDecision) -> dict[str, Any]:
        return {
            "claim": report.claim.value,
            "actual": report.actual.value,
            "acceptance": report.acceptance.value,
            "phase": Phase.CLOSED.value,
        }

    def _build_verifier(self, raw: dict[str, Any]) -> VerifierSpec:
        tool = raw.get("tool")
        verifier_id = self.verifier_registry.get(tool)
        if verifier_id is None:
            raise ValueError("verifier tool is not in gate-controlled registry")
        args = raw.get("args")
        if not isinstance(args, dict):
            raise ValueError("verifier args must be an object")
        return VerifierSpec(
            tool=tool,
            args=args,
            expected_value=raw.get("expected_value"),
            verifier_id=verifier_id,
        )

    def _predeclare(self, action: dict[str, Any]) -> dict[str, Any]:
        try:
            spec = ActionSpec(
                endpoint=str(action["endpoint"]),
                tool=str(action["tool"]),
                args=dict(action.get("args", {})),
                target_fingerprint=str(action["target_fingerprint"]),
            )
            verifier = self._build_verifier(dict(action.get("verifier", {})))
        except (KeyError, TypeError, ValueError) as exc:
            return {
                "allowed": False,
                "code": "INVALID_DECLARATION",
                "phase": self.core.phase.value,
                "detail": str(exc),
                "required_next_action": "PREDECLARE",
            }

        authority = self.runtime.resolve_authority()
        declaration = Declaration(
            action=spec,
            verifier=verifier,
            authority_id=authority.authority_id,
            success_evidence=(
                f"{verifier.verifier_id} must observe {verifier.expected_value!r} independently from the executor"
            ),
            rollback_or_reconciliation_plan=str(action.get("rollback", "")),
        )
        decision = self.core.predeclare(
            declaration,
            current_target_fingerprint=self.runtime.resolve_target_fingerprint(),
            authority=authority,
            now_epoch=self.runtime.now_epoch(),
        )
        return self._decision_payload(decision)

    def check_preexisting_postcondition(self) -> dict[str, Any]:
        """Verify an already-satisfied postcondition before any consequential dispatch."""
        declaration = self.core.declaration
        if declaration is None or self.core.phase != Phase.DECLARED:
            return {
                "allowed": False,
                "code": "PREEXISTING_CHECK_NOT_ALLOWED",
                "phase": self.core.phase.value,
            }

        receipt = self.runtime.verify(declaration.verifier)
        decision = self.core.verify_preexisting(receipt)
        payload = self._decision_payload(decision)
        payload["verification"] = {
            "outcome": receipt.outcome.value,
            "observed_value": receipt.observed_value,
            "source_id": receipt.source_id,
            "terminal": receipt.terminal,
        }

        if self.core.phase == Phase.VERIFIED and self.runtime.oracle_verify is not None:
            oracle = self.runtime.oracle_verify(declaration.verifier)
            oracle_decision = self.core.compare_oracle(oracle)
            payload["oracle"] = {
                "outcome": oracle.outcome.value,
                "observed_value": oracle.observed_value,
                "source_id": oracle.source_id,
                "terminal": oracle.terminal,
                "code": oracle_decision.code,
            }
            payload["verification_conflict"] = self.core.verification_conflict
            payload["phase"] = self.core.phase.value
            payload["required_next_action"] = oracle_decision.required_next_action

        payload["outcome_classification"] = self.core.final_outcome.value
        payload["dispatch_count"] = self.core.dispatch_count
        return payload

    def _run_bound_verification(self) -> dict[str, Any]:
        declaration = self.core.declaration
        if declaration is None:
            return {"allowed": False, "code": "DECLARATION_MISSING", "phase": self.core.phase.value}

        receipt = self.runtime.verify(declaration.verifier)
        decision = self.core.reconcile(receipt)
        payload = self._decision_payload(decision)
        payload["verification"] = {
            "outcome": receipt.outcome.value,
            "observed_value": receipt.observed_value,
            "source_id": receipt.source_id,
            "terminal": receipt.terminal,
        }

        if receipt.outcome != Outcome.PENDING and receipt.terminal and self.runtime.oracle_verify is not None:
            oracle = self.runtime.oracle_verify(declaration.verifier)
            oracle_decision = self.core.compare_oracle(oracle)
            payload["oracle"] = {
                "outcome": oracle.outcome.value,
                "observed_value": oracle.observed_value,
                "source_id": oracle.source_id,
                "terminal": oracle.terminal,
                "code": oracle_decision.code,
            }
            payload["verification_conflict"] = self.core.verification_conflict
            payload["phase"] = self.core.phase.value
            payload["required_next_action"] = oracle_decision.required_next_action

        payload["outcome_classification"] = self.core.final_outcome.value
        return payload

    def _call(self, action: dict[str, Any]) -> dict[str, Any]:
        tool = action.get("tool")
        args = action.get("args", {})

        if tool == "READ_STATE":
            if self.core.phase in {Phase.PENDING, Phase.DISPATCHED}:
                return self._run_bound_verification()
            if self.runtime.routine_read is None:
                return {"allowed": False, "code": "ROUTINE_READ_UNAVAILABLE", "phase": self.core.phase.value}
            return {
                "allowed": True,
                "code": "ROUTINE_READ",
                "phase": self.core.phase.value,
                "observation": self.runtime.routine_read(),
            }

        declaration = self.core.declaration
        if declaration is None:
            synthetic = ActionSpec(
                endpoint="",
                tool=str(tool),
                args=dict(args) if isinstance(args, dict) else {},
                target_fingerprint=self.runtime.resolve_target_fingerprint(),
            )
        else:
            synthetic = ActionSpec(
                endpoint=declaration.action.endpoint,
                tool=str(tool),
                args=dict(args) if isinstance(args, dict) else {},
                target_fingerprint=declaration.action.target_fingerprint,
            )

        authority = self.runtime.resolve_authority()
        decision, receipt = self.core.commit(
            synthetic,
            current_target_fingerprint=self.runtime.resolve_target_fingerprint(),
            authority=authority,
            now_epoch=self.runtime.now_epoch(),
            executor=self.runtime.execute,
        )
        payload = self._decision_payload(decision)
        payload["dispatch_count"] = self.core.dispatch_count
        if receipt is not None:
            payload["execution"] = {
                "outcome": receipt.outcome.value,
                "response": receipt.response,
                "applied": receipt.applied,
                "precondition_failed": receipt.precondition_failed,
            }

        if decision.allowed and receipt is not None and receipt.outcome != Outcome.PENDING:
            payload["postcondition"] = self._run_bound_verification()
        return payload

    def _report(self, action: dict[str, Any]) -> dict[str, Any]:
        try:
            claim = Outcome(str(action.get("result")))
        except ValueError:
            return {"allowed": False, "code": "INVALID_REPORT_RESULT", "phase": self.core.phase.value}
        report = self.core.report(claim)
        payload = self._report_payload(report)
        payload["dispatch_count"] = self.core.dispatch_count
        payload["verification_conflict"] = self.core.verification_conflict
        return payload

    def handle(self, action: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(action, dict):
            return {"allowed": False, "code": "INVALID_ACTION", "phase": self.core.phase.value}
        kind = action.get("action")
        if kind == "PREDECLARE":
            return self._predeclare(action)
        if kind == "CALL":
            return self._call(action)
        if kind == "REPORT":
            return self._report(action)
        return {"allowed": False, "code": "UNKNOWN_ACTION", "phase": self.core.phase.value}
