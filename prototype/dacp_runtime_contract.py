from __future__ import annotations

import time
from typing import Any, Protocol, runtime_checkable

from dacp_authority_provider import AuthorityProvider
from dacp_commitment_core import ActionSpec, ExecutionReceipt, VerifierSpec, VerificationReceipt
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


def bind_core_runtime(runtime: DACPRuntime, authority: AuthorityProvider, *, now_epoch=None) -> CoreRuntime:
    """Bind separate execution and authority boundaries to NativeActionAdapter."""

    if not isinstance(runtime, DACPRuntime):
        raise TypeError("runtime does not satisfy DACPRuntime protocol")
    if not isinstance(authority, AuthorityProvider):
        raise TypeError("authority does not satisfy AuthorityProvider protocol")
    clock = now_epoch or (lambda: int(time.time()))
    return CoreRuntime(
        resolve_authority=authority.resolve_authority,
        resolve_target_fingerprint=runtime.resolve_target_fingerprint,
        now_epoch=clock,
        execute=runtime.execute,
        verify=runtime.verify,
        oracle_verify=runtime.oracle_verify,
        routine_read=runtime.routine_read,
    )
