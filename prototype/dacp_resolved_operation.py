from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dacp_commitment_core import Phase
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
    rebind_count: int = 0
    core_events: list[dict[str, Any]] = field(default_factory=list)


class DACPResolvedOperation:
    """Execute an already-resolved operation without a probabilistic commitment step.

    The operation manifest supplies exact requested action data. Authenticated authority,
    target revalidation, commit admission, exactly-once dispatch, postcondition checks,
    oracle comparison, and final acceptance remain deterministic control-plane duties.
    """

    def __init__(self, operation: OperationSpec, runtime: CoreRuntime, *, max_rebinds: int = 1):
        if max_rebinds < 0:
            raise ValueError("max_rebinds must be nonnegative")
        self.operation = operation
        self.runtime = runtime
        self.max_rebinds = max_rebinds
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
            rebind_count=rebind_count,
            core_events=list(self.adapter.core.events),
        )

    def run(self) -> ResolvedOperationResult:
        rebind_count = 0
        declaration_result: dict[str, Any] | None = None
        preexisting_check: dict[str, Any] | None = None
        commit_result: dict[str, Any] | None = None
        pending_reconciliation: dict[str, Any] | None = None

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
                    rebind_count=rebind_count,
                )

            preexisting_check = self.adapter.check_preexisting_postcondition()
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
                    rebind_count=rebind_count,
                )

            commit_result = self.adapter.handle(
                {
                    "action": "CALL",
                    "tool": self.operation.tool,
                    "args": dict(self.operation.args),
                }
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
                        rebind_count=rebind_count,
                    )
                rebind_count += 1
                continue

            if self.adapter.core.phase == Phase.PENDING:
                pending_reconciliation = self.adapter.handle(
                    {"action": "CALL", "tool": "READ_STATE", "args": {}}
                )

            if self.adapter.core.phase == Phase.VERIFIED:
                finalization = self._finalize()
                return self._result(
                    execution_branch="MUTATION_REQUIRED",
                    terminal_state="REPORTED",
                    completion_source="CONTROL_PLANE_DIRECT_COMMIT",
                    finalization=finalization,
                    declaration_result=declaration_result,
                    preexisting_check=preexisting_check,
                    commit_result=commit_result,
                    pending_reconciliation=pending_reconciliation,
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
                rebind_count=rebind_count,
            )
