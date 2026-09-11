from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable

from dacp_commitment_core import ActionSpec, Phase
from dacp_core_adapter import CoreRuntime, NativeActionAdapter


ProviderCall = Callable[[str], Any]


@dataclass(frozen=True)
class OperationSpec:
    operation_id: str
    task: str
    endpoint: str
    tool: str
    args: dict[str, Any]
    verifier_tool: str
    verifier_args: dict[str, Any]
    expected_value: Any
    rollback_or_reconciliation_plan: str
    expected_acceptance: str = "VERIFIED_SUCCEEDED"

    def action_spec(self, target_fingerprint: str) -> ActionSpec:
        return ActionSpec(
            endpoint=self.endpoint,
            tool=self.tool,
            args=dict(self.args),
            target_fingerprint=target_fingerprint,
        )

    def declaration_action(self, target_fingerprint: str) -> dict[str, Any]:
        return {
            "action": "PREDECLARE",
            "endpoint": self.endpoint,
            "tool": self.tool,
            "args": dict(self.args),
            "target_fingerprint": target_fingerprint,
            "verifier": {
                "tool": self.verifier_tool,
                "args": dict(self.verifier_args),
                "expected_value": self.expected_value,
            },
            "rollback": self.rollback_or_reconciliation_plan,
        }

    def render_call_prompt(self, target_fingerprint: str) -> str:
        return "\n".join(
            [
                "You are operating through a deterministic commitment control plane.",
                f"Operation ID: {self.operation_id}.",
                f"Task: {self.task}",
                f"Current endpoint: {self.endpoint}.",
                f"Current target fingerprint: {target_fingerprint}.",
                "The control plane has already accepted the declaration and checked the current postcondition.",
                "The postcondition is not yet satisfied.",
                f"Request exactly CALL for {self.tool} with args {json.dumps(self.args, sort_keys=True, separators=(',', ':'))}.",
                "Do not PREDECLARE or REPORT; the control plane owns declaration, verification, and finalization.",
            ]
        )


@dataclass
class SessionResult:
    operation_id: str
    terminal_state: str
    final_acceptance: str | None
    dispatch_count: int
    applied_count: int
    reconciliation_count: int
    verification_conflict: bool
    completion_source: str | None = None
    control_finalization: dict[str, Any] | None = None
    declaration_result: dict[str, Any] | None = None
    preexisting_check: dict[str, Any] | None = None
    core_events: list[dict[str, Any]] = field(default_factory=list)
    turns: list[dict[str, Any]] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return (
            self.terminal_state == "REPORTED"
            and self.final_acceptance is not None
            and not self.verification_conflict
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "terminal_state": self.terminal_state,
            "final_acceptance": self.final_acceptance,
            "dispatch_count": self.dispatch_count,
            "applied_count": self.applied_count,
            "reconciliation_count": self.reconciliation_count,
            "verification_conflict": self.verification_conflict,
            "completion_source": self.completion_source,
            "control_finalization": self.control_finalization,
            "declaration_result": self.declaration_result,
            "preexisting_check": self.preexisting_check,
            "core_events": self.core_events,
            "turns": self.turns,
        }


class DACPControlSession:
    """Deterministic commitment shell with provider use only when mutation is needed."""

    def __init__(self, operation: OperationSpec, runtime: CoreRuntime, provider_call: ProviderCall | None):
        self.operation = operation
        self.runtime = runtime
        self.provider_call = provider_call
        self.adapter = NativeActionAdapter(runtime)

    def _validate_operation_binding(self, initial_target_fingerprint: str) -> None:
        expected_action = self.operation.action_spec(initial_target_fingerprint)
        authority = self.runtime.resolve_authority()
        if authority.action_fingerprint != expected_action.action_fingerprint:
            raise RuntimeError("operation does not match authenticated authority action binding")
        if authority.target_fingerprint != initial_target_fingerprint:
            raise RuntimeError("operation target does not match authenticated authority target binding")

    def _finalize_verified_core(self) -> dict[str, Any]:
        if self.adapter.core.phase != Phase.VERIFIED:
            raise RuntimeError("control-plane finalization requires terminal VERIFIED phase")
        return self.adapter.handle(
            {
                "action": "REPORT",
                "result": self.adapter.core.final_outcome.value,
                "note": "control-plane finalized terminal verified classification",
            }
        )

    def _result(
        self,
        *,
        terminal: str,
        final_acceptance: str | None,
        completion_source: str | None,
        control_finalization: dict[str, Any] | None,
        declaration_result: dict[str, Any] | None,
        preexisting_check: dict[str, Any] | None,
        turns: list[dict[str, Any]],
    ) -> SessionResult:
        return SessionResult(
            operation_id=self.operation.operation_id,
            terminal_state=terminal,
            final_acceptance=final_acceptance,
            dispatch_count=self.adapter.core.dispatch_count,
            applied_count=self.adapter.core.applied_count,
            reconciliation_count=self.adapter.core.reconciliation_count,
            verification_conflict=self.adapter.core.verification_conflict,
            completion_source=completion_source,
            control_finalization=control_finalization,
            declaration_result=declaration_result,
            preexisting_check=preexisting_check,
            core_events=list(self.adapter.core.events),
            turns=turns,
        )

    def run(self, max_turns: int = 3) -> SessionResult:
        initial_target = self.runtime.resolve_target_fingerprint()
        self._validate_operation_binding(initial_target)

        declaration_result = self.adapter.handle(self.operation.declaration_action(initial_target))
        if not declaration_result.get("allowed"):
            return self._result(
                terminal="CONTROL_BLOCKED",
                final_acceptance=None,
                completion_source="DETERMINISTIC_DECLARATION_BLOCK",
                control_finalization=None,
                declaration_result=declaration_result,
                preexisting_check=None,
                turns=[],
            )

        preexisting_check = self.adapter.check_preexisting_postcondition()
        if self.adapter.core.phase == Phase.VERIFIED:
            control_finalization = self._finalize_verified_core()
            return self._result(
                terminal="REPORTED",
                final_acceptance=control_finalization.get("acceptance"),
                completion_source="PREEXISTING_STATE_VERIFIED",
                control_finalization=control_finalization,
                declaration_result=declaration_result,
                preexisting_check=preexisting_check,
                turns=[],
            )

        if self.provider_call is None:
            return self._result(
                terminal="PROVIDER_REQUIRED",
                final_acceptance=None,
                completion_source=None,
                control_finalization=None,
                declaration_result=declaration_result,
                preexisting_check=preexisting_check,
                turns=[],
            )

        turns: list[dict[str, Any]] = []
        transcript = [self.operation.render_call_prompt(initial_target)]

        for turn_index in range(max_turns):
            prompt = "\n\n".join(transcript)
            result = self.provider_call(prompt)
            record: dict[str, Any] = {
                "turn": turn_index + 1,
                "provider_status": getattr(result, "status", None),
                "raw_text": getattr(result, "text", None),
                "provider_metadata": getattr(result, "provider_metadata", None),
            }
            if getattr(result, "status", None) != "SUCCEEDED":
                record["broker_reply"] = {
                    "allowed": False,
                    "code": "PROVIDER_CALL_NOT_SUCCEEDED",
                    "provider_status": getattr(result, "status", None),
                    "error": getattr(result, "error", None),
                }
                turns.append(record)
                return self._result(
                    terminal="PROVIDER_UNRESOLVED",
                    final_acceptance=None,
                    completion_source=None,
                    control_finalization=None,
                    declaration_result=declaration_result,
                    preexisting_check=preexisting_check,
                    turns=turns,
                )

            try:
                action = json.loads(getattr(result, "text", None) or "")
            except json.JSONDecodeError as exc:
                record["broker_reply"] = {"allowed": False, "code": "INVALID_NORMALIZED_ACTION", "detail": str(exc)}
                turns.append(record)
                return self._result(
                    terminal="INVALID_ACTION",
                    final_acceptance=None,
                    completion_source=None,
                    control_finalization=None,
                    declaration_result=declaration_result,
                    preexisting_check=preexisting_check,
                    turns=turns,
                )

            if action.get("action") != "CALL":
                record["parsed_action"] = action
                record["broker_reply"] = {
                    "allowed": False,
                    "code": "PROVIDER_ACTION_NOT_ALLOWED_IN_COMMIT_PHASE",
                    "phase": self.adapter.core.phase.value,
                    "required_next_action": "CALL",
                }
                turns.append(record)
                transcript.append(f"BROKER RESULT: {json.dumps(record['broker_reply'], sort_keys=True)}")
                continue

            reply = self.adapter.handle(action)
            record["parsed_action"] = action
            record["broker_reply"] = reply
            turns.append(record)

            if self.adapter.core.phase == Phase.VERIFIED:
                control_finalization = self._finalize_verified_core()
                return self._result(
                    terminal="REPORTED",
                    final_acceptance=control_finalization.get("acceptance"),
                    completion_source="CONTROL_PLANE_AUTO_FINALIZE",
                    control_finalization=control_finalization,
                    declaration_result=declaration_result,
                    preexisting_check=preexisting_check,
                    turns=turns,
                )

            transcript.append(f"MODEL ACTION: {json.dumps(action, sort_keys=True)}")
            transcript.append(f"BROKER RESULT: {json.dumps(reply, sort_keys=True)}")

        return self._result(
            terminal="TIMEOUT_NO_COMPLETION",
            final_acceptance=None,
            completion_source=None,
            control_finalization=None,
            declaration_result=declaration_result,
            preexisting_check=preexisting_check,
            turns=turns,
        )
