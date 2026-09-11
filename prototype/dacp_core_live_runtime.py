from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dacp_commitment_core import (
    ActionSpec,
    AuthorityProof,
    ExecutionReceipt,
    Outcome,
    VerificationReceipt,
    VerifierSpec,
)


@dataclass
class VersionedValueRuntime:
    """Minimal provider-independent runtime used by the first live core integration.

    The executor mutates one versioned value. The declared verifier reads current
    state directly. The oracle independently replays the append-only ledger.
    """

    endpoint: str = "tracked-value"
    initial_value: str = "INITIAL"
    authorized_value: str = "DEPLOYED"
    value: str = field(init=False)
    version: int = field(init=False, default=0)
    ledger: list[dict[str, Any]] = field(init=False, default_factory=list)
    authority_revoked: bool = False
    trust_root_compromised: bool = False

    def __post_init__(self) -> None:
        self.value = self.initial_value
        self._authorized_action = ActionSpec(
            endpoint=self.endpoint,
            tool="SET_STATE",
            args={"value": self.authorized_value},
            target_fingerprint=self.target_fingerprint,
        )

    @property
    def target_fingerprint(self) -> str:
        return f"tracked-value@v{self.version}"

    @property
    def authorized_action(self) -> ActionSpec:
        return self._authorized_action

    def resolve_target_fingerprint(self) -> str:
        return self.target_fingerprint

    def resolve_authority(self) -> AuthorityProof:
        action = self._authorized_action
        return AuthorityProof(
            authority_id="AUTH-LIVE-001",
            action_fingerprint=action.action_fingerprint,
            target_fingerprint=action.target_fingerprint,
            trust_root_id="local-live-fixture-root",
            valid_through_epoch=4_102_444_800,
            revoked=self.authority_revoked,
            trust_root_compromised=self.trust_root_compromised,
        )

    def routine_read(self) -> dict[str, Any]:
        return {
            "value": self.value,
            "target_fingerprint": self.target_fingerprint,
        }

    def execute(self, action: ActionSpec, expected_fingerprint: str) -> ExecutionReceipt:
        if action.tool != "SET_STATE":
            return ExecutionReceipt(
                outcome=Outcome.FAILED,
                response={"error": "UNSUPPORTED_CONSEQUENTIAL_TOOL", "tool": action.tool},
                applied=False,
            )
        if expected_fingerprint != self.target_fingerprint:
            return ExecutionReceipt(
                outcome=Outcome.FAILED,
                response={
                    "error": "PRECONDITION_FAILED",
                    "expected_target_fingerprint": expected_fingerprint,
                    "current_target_fingerprint": self.target_fingerprint,
                },
                applied=False,
                precondition_failed=True,
            )
        requested = action.args.get("value")
        if not isinstance(requested, str):
            return ExecutionReceipt(
                outcome=Outcome.FAILED,
                response={"error": "INVALID_VALUE"},
                applied=False,
            )

        prior = self.value
        self.version += 1
        self.value = requested
        self.ledger.append(
            {
                "sequence": len(self.ledger) + 1,
                "op": "SET_STATE",
                "prior_value": prior,
                "value": requested,
                "version": self.version,
            }
        )
        return ExecutionReceipt(
            outcome=Outcome.SUCCEEDED,
            response={
                "applied": True,
                "value": self.value,
                "target_fingerprint": self.target_fingerprint,
            },
            applied=True,
        )

    def verify(self, verifier: VerifierSpec) -> VerificationReceipt:
        if verifier.tool != "READ_STATE" or verifier.args != {}:
            return VerificationReceipt(
                outcome=Outcome.FAILED,
                observed_value=None,
                source_id="direct-state-read",
                independent_from_executor=True,
            )
        outcome = Outcome.SUCCEEDED if self.value == verifier.expected_value else Outcome.FAILED
        return VerificationReceipt(
            outcome=outcome,
            observed_value=self.value,
            source_id="direct-state-read",
            independent_from_executor=True,
        )

    def oracle_verify(self, verifier: VerifierSpec) -> VerificationReceipt:
        replayed = self.initial_value
        expected_version = 0
        for event in self.ledger:
            if event.get("sequence") != expected_version + 1:
                return VerificationReceipt(
                    outcome=Outcome.PENDING,
                    observed_value=replayed,
                    source_id="ledger-replay-oracle",
                    independent_from_executor=True,
                    terminal=False,
                )
            if event.get("op") != "SET_STATE":
                return VerificationReceipt(
                    outcome=Outcome.PENDING,
                    observed_value=replayed,
                    source_id="ledger-replay-oracle",
                    independent_from_executor=True,
                    terminal=False,
                )
            expected_version += 1
            if event.get("version") != expected_version:
                return VerificationReceipt(
                    outcome=Outcome.PENDING,
                    observed_value=replayed,
                    source_id="ledger-replay-oracle",
                    independent_from_executor=True,
                    terminal=False,
                )
            replayed = event.get("value")

        outcome = Outcome.SUCCEEDED if replayed == verifier.expected_value else Outcome.FAILED
        return VerificationReceipt(
            outcome=outcome,
            observed_value=replayed,
            source_id="ledger-replay-oracle",
            independent_from_executor=True,
        )
