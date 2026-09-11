from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from dacp_commitment_core import ActionSpec, AuthorityProof, ExecutionReceipt, Outcome, VerificationReceipt, VerifierSpec


class FileBackedValueRuntime:
    """Durable single-resource runtime with atomic replace and readback verification."""

    def __init__(self, path: str | Path, *, endpoint: str = "tracked-value", authorized_value: str = "DEPLOYED"):
        self.path = Path(path)
        self.endpoint = endpoint
        self.authorized_value = authorized_value
        if not self.path.exists():
            self._write_state({"value": "INITIAL", "version": 0, "ledger": []})
        state = self._read_state()
        self._authorized_action = ActionSpec(
            endpoint=self.endpoint,
            tool="SET_STATE",
            args={"value": self.authorized_value},
            target_fingerprint=self._fingerprint(state["version"]),
        )

    @property
    def authorized_action(self) -> ActionSpec:
        return self._authorized_action

    @staticmethod
    def _fingerprint(version: int) -> str:
        return f"tracked-value@v{version}"

    def _read_state(self) -> dict[str, Any]:
        raw = self.path.read_text(encoding="utf-8")
        data = json.loads(raw)
        if set(data) != {"value", "version", "ledger"}:
            raise RuntimeError("state document shape is invalid")
        if not isinstance(data["version"], int) or data["version"] < 0:
            raise RuntimeError("state version is invalid")
        if not isinstance(data["ledger"], list):
            raise RuntimeError("state ledger is invalid")
        return data

    def _write_state(self, state: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(state, indent=2, sort_keys=True) + "\n"
        fd, temp_name = tempfile.mkstemp(prefix=self.path.name + ".", suffix=".tmp", dir=str(self.path.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, self.path)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
        if self._read_state() != state:
            raise RuntimeError("state readback mismatch after atomic replace")

    def resolve_target_fingerprint(self) -> str:
        state = self._read_state()
        return self._fingerprint(state["version"])

    def resolve_authority(self) -> AuthorityProof:
        return AuthorityProof(
            authority_id="AUTH-FILE-001",
            action_fingerprint=self._authorized_action.action_fingerprint,
            target_fingerprint=self._authorized_action.target_fingerprint,
            trust_root_id="local-file-runtime-root",
            valid_through_epoch=4_102_444_800,
            revoked=False,
            trust_root_compromised=False,
        )

    def routine_read(self) -> dict[str, Any]:
        state = self._read_state()
        return {"value": state["value"], "target_fingerprint": self._fingerprint(state["version"])}

    def evidence_snapshot(self) -> dict[str, Any]:
        state = self._read_state()
        return {
            "runtime_kind": "file",
            "path": str(self.path.resolve()),
            "value": state["value"],
            "version": state["version"],
            "target_fingerprint": self._fingerprint(state["version"]),
            "ledger": list(state["ledger"]),
        }

    def execute(self, action: ActionSpec, expected_fingerprint: str) -> ExecutionReceipt:
        state = self._read_state()
        current_fingerprint = self._fingerprint(state["version"])
        if expected_fingerprint != current_fingerprint:
            return ExecutionReceipt(
                outcome=Outcome.FAILED,
                response={"error": "PRECONDITION_FAILED", "current_target_fingerprint": current_fingerprint},
                applied=False,
                precondition_failed=True,
            )
        if action.tool != "SET_STATE" or action.args != {"value": self.authorized_value}:
            return ExecutionReceipt(
                outcome=Outcome.FAILED,
                response={"error": "UNAUTHORIZED_OR_UNSUPPORTED_ACTION"},
                applied=False,
            )
        if state["value"] == self.authorized_value:
            return ExecutionReceipt(
                outcome=Outcome.SUCCEEDED,
                response={"applied": False, "already_satisfied": True, "value": state["value"], "target_fingerprint": current_fingerprint},
                applied=False,
            )
        next_version = state["version"] + 1
        event = {
            "sequence": len(state["ledger"]) + 1,
            "op": "SET_STATE",
            "prior_value": state["value"],
            "value": self.authorized_value,
            "version": next_version,
        }
        next_state = {"value": self.authorized_value, "version": next_version, "ledger": [*state["ledger"], event]}
        self._write_state(next_state)
        return ExecutionReceipt(
            outcome=Outcome.SUCCEEDED,
            response={"applied": True, "value": self.authorized_value, "target_fingerprint": self._fingerprint(next_version)},
            applied=True,
        )

    def verify(self, verifier: VerifierSpec) -> VerificationReceipt:
        state = self._read_state()
        observed = state["value"]
        outcome = Outcome.SUCCEEDED if verifier.tool == "READ_STATE" and verifier.args == {} and observed == verifier.expected_value else Outcome.FAILED
        return VerificationReceipt(outcome, observed, "file-state-read", True)

    def oracle_verify(self, verifier: VerifierSpec) -> VerificationReceipt:
        state = self._read_state()
        replayed = "INITIAL"
        expected_version = 0
        for index, event in enumerate(state["ledger"], start=1):
            if event.get("sequence") != index or event.get("op") != "SET_STATE":
                return VerificationReceipt(Outcome.PENDING, replayed, "file-ledger-replay", True, terminal=False)
            expected_version += 1
            if event.get("version") != expected_version:
                return VerificationReceipt(Outcome.PENDING, replayed, "file-ledger-replay", True, terminal=False)
            replayed = event.get("value")
        if expected_version != state["version"] or replayed != state["value"]:
            return VerificationReceipt(Outcome.PENDING, replayed, "file-ledger-replay", True, terminal=False)
        outcome = Outcome.SUCCEEDED if replayed == verifier.expected_value else Outcome.FAILED
        return VerificationReceipt(outcome, replayed, "file-ledger-replay", True)
