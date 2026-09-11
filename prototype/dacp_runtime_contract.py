from __future__ import annotations

import time
from typing import Any, Protocol, runtime_checkable

from dacp_authority_provider import AuthorityProvider
from dacp_commit_journal import DurableCommitJournal
from dacp_commitment_core import ActionSpec, ExecutionReceipt, Outcome, VerifierSpec, VerificationReceipt
from dacp_core_adapter import CoreRuntime


@runtime_checkable
class DACPRuntime(Protocol):
    """Execution/state surface consumed by the deterministic control plane.

    A runtime owns target resolution, execution mechanics, verification, and state
    evidence. It does not grant authority for consequential actions.
    """

    endpoint: str

    def resolve_target_fingerprint(self) -> str:
        ...

    def execute(self, action: ActionSpec, expected_fingerprint: str) -> ExecutionReceipt:
        ...

    def verify(self, verifier: VerifierSpec) -> VerificationReceipt:
        ...

    def oracle_verify(self, verifier: VerifierSpec) -> VerificationReceipt:
        ...

    def routine_read(self) -> dict[str, Any]:
        ...

    def evidence_snapshot(self) -> dict[str, Any]:
        ...


def bind_core_runtime(
    runtime: DACPRuntime,
    authority: AuthorityProvider,
    *,
    now_epoch=None,
    dispatch_journal: DurableCommitJournal | None = None,
    operation_id: str | None = None,
) -> CoreRuntime:
    """Bind execution and authority boundaries, optionally with durable dispatch intent."""

    if not isinstance(runtime, DACPRuntime):
        raise TypeError("runtime does not satisfy DACPRuntime protocol")
    if not isinstance(authority, AuthorityProvider):
        raise TypeError("authority does not satisfy AuthorityProvider protocol")
    if dispatch_journal is not None and not operation_id:
        raise ValueError("operation_id is required when dispatch journaling is enabled")

    clock = now_epoch or (lambda: int(time.time()))
    executor = runtime.execute

    if dispatch_journal is not None:
        def journaled_execute(action: ActionSpec, expected_fingerprint: str) -> ExecutionReceipt:
            proof = authority.resolve_authority()
            record = dispatch_journal.record_dispatch_intent(
                operation_id=str(operation_id),
                endpoint=action.endpoint,
                tool=action.tool,
                args=dict(action.args),
                action_fingerprint=action.action_fingerprint,
                target_fingerprint=expected_fingerprint,
                authority_id=proof.authority_id,
            )
            receipt = runtime.execute(action, expected_fingerprint)
            dispatch_journal.transition(
                record["record_id"],
                "DISPATCH_RETURNED",
                detail={
                    "outcome": receipt.outcome.value,
                    "applied": receipt.applied,
                    "precondition_failed": receipt.precondition_failed,
                },
            )
            if receipt.outcome == Outcome.PENDING:
                dispatch_journal.transition(record["record_id"], "DISPATCH_OUTCOME_PENDING")
            return receipt

        executor = journaled_execute

    return CoreRuntime(
        resolve_authority=authority.resolve_authority,
        resolve_target_fingerprint=runtime.resolve_target_fingerprint,
        now_epoch=clock,
        execute=executor,
        verify=runtime.verify,
        oracle_verify=runtime.oracle_verify,
        routine_read=runtime.routine_read,
    )
