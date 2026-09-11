from __future__ import annotations

import time
from typing import Any, Protocol, runtime_checkable

from dacp_commitment_core import (
    ActionSpec,
    AuthorityProof,
    ExecutionReceipt,
    VerifierSpec,
    VerificationReceipt,
)
from dacp_core_adapter import CoreRuntime


@runtime_checkable
class DACPRuntime(Protocol):
    """Minimal runtime surface consumed by the deterministic control plane."""

    endpoint: str
    authorized_value: Any

    @property
    def authorized_action(self) -> ActionSpec:
        ...

    def resolve_authority(self) -> AuthorityProof:
        ...

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


def bind_core_runtime(runtime: DACPRuntime, *, now_epoch=None) -> CoreRuntime:
    """Bind a concrete DACP runtime to the callback shape used by NativeActionAdapter."""

    if not isinstance(runtime, DACPRuntime):
        raise TypeError("runtime does not satisfy DACPRuntime protocol")
    clock = now_epoch or (lambda: int(time.time()))
    return CoreRuntime(
        resolve_authority=runtime.resolve_authority,
        resolve_target_fingerprint=runtime.resolve_target_fingerprint,
        now_epoch=clock,
        execute=runtime.execute,
        verify=runtime.verify,
        oracle_verify=runtime.oracle_verify,
        routine_read=runtime.routine_read,
    )
