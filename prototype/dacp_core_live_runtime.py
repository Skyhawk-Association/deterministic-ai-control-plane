from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dacp_commitment_core import ActionSpec, ExecutionReceipt, Outcome, VerificationReceipt, VerifierSpec


@dataclass
class VersionedValueRuntime:
    """Minimal provider-independent in-memory execution runtime."""

    endpoint: str = "tracked-value"
    initial_value: str = "INITIAL"
    value: str = field(init=False)
    version: int = field(init=False, default=0)
    ledger: list[dict[str, Any]] = field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        self.value = self.initial_value

    @property
    def target_fingerprint(self) -> str:
        return f"{self.endpoint}@v{self.version}"

    def resolve_target_fingerprint(self) -> str:
        return self.target_fingerprint

    def routine_read(self) -> dict[str, Any]:
        return {"value": self.value, "target_fingerprint": self.target_fingerprint}

    def evidence_snapshot(self) -> dict[str, Any]:
        return {
            "runtime_kind": "memory",
            "value": self.value,
            "version": self.version,
            "target_fingerprint": self.target_fingerprint,
            "ledger": list(self.ledger),
        }

    def execute(self, action: ActionSpec, expected_fingerprint: str) -> ExecutionReceipt:
        if action.endpoint != self.endpoint or action.tool != "SET_STATE":
            return ExecutionReceipt(Outcome.FAILED, {"error": "UNSUPPORTED_ACTION"}, applied=False)
        if expected_fingerprint != self.target_fingerprint:
            return ExecutionReceipt(
                Outcome.FAILED,
                {"error": "PRECONDITION_FAILED", "expected_target_fingerprint": expected_fingerprint, "current_target_fingerprint": self.target_fingerprint},
                applied=False,
                precondition_failed=True,
            )
        if set(action.args) != {"value"} or not isinstance(action.args.get("value"), str):
            return ExecutionReceipt(Outcome.FAILED, {"error": "INVALID_VALUE"}, applied=False)
        requested = action.args["value"]
        if self.value == requested:
            return ExecutionReceipt(
                Outcome.SUCCEEDED,
                {"applied": False, "already_satisfied": True, "value": self.value, "target_fingerprint": self.target_fingerprint},
                applied=False,
            )
        prior = self.value
        self.version += 1
        self.value = requested
        self.ledger.append({"sequence": len(self.ledger) + 1, "op": "SET_STATE", "prior_value": prior, "value": requested, "version": self.version})
        return ExecutionReceipt(Outcome.SUCCEEDED, {"applied": True, "value": self.value, "target_fingerprint": self.target_fingerprint}, applied=True)

    def verify(self, verifier: VerifierSpec) -> VerificationReceipt:
        if verifier.tool != "READ_STATE" or verifier.args != {}:
            return VerificationReceipt(Outcome.FAILED, None, "direct-state-read", True)
        outcome = Outcome.SUCCEEDED if self.value == verifier.expected_value else Outcome.FAILED
        return VerificationReceipt(outcome, self.value, "direct-state-read", True)

    def oracle_verify(self, verifier: VerifierSpec) -> VerificationReceipt:
        replayed = self.initial_value
        expected_version = 0
        for event in self.ledger:
            if event.get("sequence") != expected_version + 1 or event.get("op") != "SET_STATE":
                return VerificationReceipt(Outcome.PENDING, replayed, "ledger-replay-oracle", True, terminal=False)
            expected_version += 1
            if event.get("version") != expected_version:
                return VerificationReceipt(Outcome.PENDING, replayed, "ledger-replay-oracle", True, terminal=False)
            replayed = event.get("value")
        outcome = Outcome.SUCCEEDED if replayed == verifier.expected_value else Outcome.FAILED
        return VerificationReceipt(outcome, replayed, "ledger-replay-oracle", True)
