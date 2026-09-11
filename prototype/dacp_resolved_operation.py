from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dacp_commit_journal import DurableCommitJournal, request_fingerprint
from dacp_commitment_core import Outcome, Phase
from dacp_control_session import OperationSpec
from dacp_core_adapter import CoreRuntime, NativeActionAdapter


@dataclass
class ResolvedOperationResult:
    operation_id: str
    execution_branch: str
    terminal_state: str
    final_acceptance: str | None
    completion_source: str | None
    dispatch_count: int
    applied_count: int
    reconciliation_count: int
    verification_conflict: bool
    declaration_result: dict[str, Any] | None = None
    preexisting_check: dict[str, Any] | None = None
    commit_result: dict[str, Any] | None = None
    pending_reconciliation: dict[str, Any] | None = None
    control_finalization: dict[str, Any] | None = None
    recovery_record: dict[str, Any] | None = None
    rebind_count: int = 0
    core_events: list[dict[str, Any]] = field(default_factory=list)


class DACPResolvedOperation:
    """Execute or recover an exact authorized operation deterministically.

    If a durable dispatch journal reports unresolved prior intent, recovery verifies the
    current postcondition first and never redispatches merely because the process restarted.
    """

    def __init__(
        self,
        operation: OperationSpec,
        runtime: CoreRuntime,
        *,
        max_rebinds: int = 1,
        commit_journal: DurableCommitJournal | None = None,
    ):
        if max_rebinds < 0:
            raise ValueError("max_rebinds must be nonnegative")
        self.operation = operation
        self.runtime = runtime
        self.max_rebinds = max_rebinds
        self.commit_journal = commit_journal
        self.adapter = NativeActionAdapter(runtime)

    def _finalize(self) -> dict[str, Any]:
        if self.adapter.core.phase != Phase.VERIFIED:
            raise RuntimeError("resolved-operation finalization requires VERIFIED phase")
        return self.adapter.handle(
            {
                "action": "REPORT",
                "result": self.adapter.core.final_outcome.value,
                "note": "control-plane finalized resolved operation",
            }
        )

    def _current_unresolved(self) -> dict[str, Any] | None:
        if self.commit_journal is None:
            return None
        return self.commit_journal.unresolved_for(self.operation.operation_id)

    def _recovery_record_matches(self, record: dict[str, Any]) -> bool:
        expected = request_fingerprint(self.operation.endpoint, self.operation.tool, self.operation.args)
        return record.get("request_fingerprint") == expected

    def _resolve_journal(self, outcome: Outcome, *, detail: dict[str, Any] | None = None) -> dict[str, Any] | None:
        record = self._current_unresolved()
        if record is None or self.commit_journal is None:
            return record
        phase = "RESOLVED_SUCCEEDED" if outcome == Outcome.SUCCEEDED else "RESOLVED_FAILED"
        return self.commit_journal.transition(record["record_id"], phase, detail=detail)

    def _result(
        self,
        *,
        execution_branch: str,
        terminal_state: str,
        completion_source: str | None,
        finalization: dict[str, Any] | None,
        declaration_result: dict[str, Any] | None,
        preexisting_check: dict[str, Any] | None,
        commit_result: dict[str, Any] | None,
        pending_reconciliation: dict[str, Any] | None,
        recovery_record: dict[str, Any] | None,
        rebind_count: int,
    ) -> ResolvedOperationResult:
        return ResolvedOperationResult(
            operation_id=self.operation.operation_id,
            execution_branch=execution_branch,
            terminal_state=terminal_state,
            final_acceptance=(finalization or {}).get("acceptance"),
            completion_source=completion_source,
            dispatch_count=self.adapter.core.dispatch_count,
            applied_count=self.adapter.core.applied_count,
            reconciliation_count=self.adapter.core.reconciliation_count,
            verification_conflict=self.adapter.core.verification_conflict,
            declaration_result=declaration_result,
            preexisting_check=preexisting_check,
            commit_result=commit_result,
            pending_reconciliation=pending_reconciliation,
            control_finalization=finalization,
            recovery_record=recovery_record,
            rebind_count=rebind_count,
            core_events=list(self.adapter.core.events),
        )

    def run(self) -> ResolvedOperationResult:
        rebind_count = 0
        declaration_result: dict[str, Any] | None = None
        preexisting_check: dict[str, Any] | None = None
        commit_result: dict[str, Any] | None = None
        pending_reconciliation: dict[str, Any] | None = None
        recovery_record = self._current_unresolved()

        if recovery_record is not None and not self._recovery_record_matches(recovery_record):
            return self._result(
                execution_branch="RECOVERY_REQUEST_MISMATCH_BLOCKED",
                terminal_state="CONTROL_BLOCKED",
                completion_source="UNRESOLVED_PRIOR_REQUEST_MISMATCH",
                finalization=None,
                declaration_result=None,
                preexisting_check=None,
                commit_result=None,
                pending_reconciliation=None,
                recovery_record=recovery_record,
                rebind_count=0,
            )

        while True:
            target = self.runtime.resolve_target_fingerprint()
            declaration_result = self.adapter.handle(self.operation.declaration_action(target))
            if not declaration_result.get("allowed"):
                return self._result(
                    execution_branch="CONTROL_BLOCKED",
                    terminal_state="CONTROL_BLOCKED",
                    completion_source="DETERMINISTIC_DECLARATION_BLOCK",
                    finalization=None,
                    declaration_result=declaration_result,
                    preexisting_check=None,
                    commit_result=None,
                    pending_reconciliation=None,
                    recovery_record=recovery_record,
                    rebind_count=rebind_count,
                )

            preexisting_check = self.adapter.check_preexisting_postcondition()

            if recovery_record is not None:
                if self.adapter.core.phase == Phase.VERIFIED and not self.adapter.core.verification_conflict:
                    finalization = self._finalize()
                    resolved_record = self._resolve_journal(
                        self.adapter.core.final_outcome,
                        detail={"completion_source": "RESTART_RECONCILIATION", "acceptance": finalization.get("acceptance")},
                    )
                    return self._result(
                        execution_branch="RECOVERY_VERIFIED_NO_REDISPATCH",
                        terminal_state="REPORTED",
                        completion_source="RESTART_RECONCILED_SUCCEEDED",
                        finalization=finalization,
                        declaration_result=declaration_result,
                        preexisting_check=preexisting_check,
                        commit_result=None,
                        pending_reconciliation=None,
                        recovery_record=resolved_record,
                        rebind_count=rebind_count,
                    )

                if self.commit_journal is not None:
                    recovery_record = self.commit_journal.transition(
                        recovery_record["record_id"],
                        "RECOVERY_PENDING",
                        detail={
                            "observed_classification": preexisting_check.get("outcome_classification"),
                            "verification_conflict": self.adapter.core.verification_conflict,
                        },
                    )
                return self._result(
                    execution_branch="RECOVERY_PENDING_NO_REDISPATCH",
                    terminal_state="PENDING",
                    completion_source="RESTART_RECONCILIATION_REQUIRED",
                    finalization=None,
                    declaration_result=declaration_result,
                    preexisting_check=preexisting_check,
                    commit_result=None,
                    pending_reconciliation=None,
                    recovery_record=recovery_record,
                    rebind_count=rebind_count,
                )

            if self.adapter.core.phase == Phase.VERIFIED:
                finalization = self._finalize()
                return self._result(
                    execution_branch="PREEXISTING_VERIFIED_NO_DISPATCH",
                    terminal_state="REPORTED",
                    completion_source="PREEXISTING_STATE_VERIFIED",
                    finalization=finalization,
                    declaration_result=declaration_result,
                    preexisting_check=preexisting_check,
                    commit_result=None,
                    pending_reconciliation=None,
                    recovery_record=None,
                    rebind_count=rebind_count,
                )

            if self.adapter.core.phase != Phase.DECLARED:
                return self._result(
                    execution_branch="PRECOMMIT_UNRESOLVED",
                    terminal_state=self.adapter.core.phase.value,
                    completion_source=None,
                    finalization=None,
                    declaration_result=declaration_result,
                    preexisting_check=preexisting_check,
                    commit_result=None,
                    pending_reconciliation=None,
                    recovery_record=None,
                    rebind_count=rebind_count,
                )

            commit_result = self.adapter.handle(
                {"action": "CALL", "tool": self.operation.tool, "args": dict(self.operation.args)}
            )

            if self.adapter.core.phase == Phase.REBIND_REQUIRED:
                if rebind_count >= self.max_rebinds:
                    return self._result(
                        execution_branch="REBIND_LIMIT_REACHED",
                        terminal_state="REBIND_REQUIRED",
                        completion_source=None,
                        finalization=None,
                        declaration_result=declaration_result,
                        preexisting_check=preexisting_check,
                        commit_result=commit_result,
                        pending_reconciliation=None,
                        recovery_record=self._current_unresolved(),
                        rebind_count=rebind_count,
                    )
                rebind_count += 1
                continue

            if self.adapter.core.phase == Phase.PENDING:
                pending_reconciliation = self.adapter.handle({"action": "CALL", "tool": "READ_STATE", "args": {}})

            if self.adapter.core.phase == Phase.VERIFIED:
                finalization = self._finalize()
                journal_record = None
                if self.adapter.core.verification_conflict:
                    unresolved = self._current_unresolved()
                    if unresolved is not None and self.commit_journal is not None:
                        journal_record = self.commit_journal.transition(
                            unresolved["record_id"], "VERIFICATION_CONFLICT"
                        )
                else:
                    journal_record = self._resolve_journal(
                        self.adapter.core.final_outcome,
                        detail={"completion_source": "DIRECT_COMMIT", "acceptance": finalization.get("acceptance")},
                    )
                return self._result(
                    execution_branch="MUTATION_REQUIRED",
                    terminal_state="REPORTED",
                    completion_source="CONTROL_PLANE_DIRECT_COMMIT",
                    finalization=finalization,
                    declaration_result=declaration_result,
                    preexisting_check=preexisting_check,
                    commit_result=commit_result,
                    pending_reconciliation=pending_reconciliation,
                    recovery_record=journal_record,
                    rebind_count=rebind_count,
                )

            if not commit_result.get("allowed"):
                return self._result(
                    execution_branch="CONTROL_BLOCKED",
                    terminal_state="CONTROL_BLOCKED",
                    completion_source="COMMIT_BLOCKED",
                    finalization=None,
                    declaration_result=declaration_result,
                    preexisting_check=preexisting_check,
                    commit_result=commit_result,
                    pending_reconciliation=pending_reconciliation,
                    recovery_record=self._current_unresolved(),
                    rebind_count=rebind_count,
                )

            return self._result(
                execution_branch="PENDING_RECONCILIATION",
                terminal_state=self.adapter.core.phase.value,
                completion_source=None,
                finalization=None,
                declaration_result=declaration_result,
                preexisting_check=preexisting_check,
                commit_result=commit_result,
                pending_reconciliation=pending_reconciliation,
                recovery_record=self._current_unresolved(),
                rebind_count=rebind_count,
            )
