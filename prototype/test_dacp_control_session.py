import json
import unittest

import dacp_broker
from dacp_authority_provider import AuthorityGrant, StaticAuthorityProvider
from dacp_commitment_core import ActionSpec
from dacp_control_session import DACPControlSession, OperationSpec
from dacp_core_live_runtime import VersionedValueRuntime
from dacp_runtime_contract import bind_core_runtime


def fake_result(action):
    return dacp_broker.ProviderResult(
        "test", "test-model", "SUCCEEDED", json.dumps(action), None,
        200, "req", 1, None, "completed", None, "test-model", {},
    )


class ScriptedProvider:
    def __init__(self, actions):
        self.actions = list(actions)
        self.call_count = 0

    def __call__(self, prompt):
        self.call_count += 1
        if not self.actions:
            raise AssertionError("provider was called after terminal control-plane verification")
        return fake_result(self.actions.pop(0))


def make_operation(value="DEPLOYED"):
    return OperationSpec(
        operation_id="op-1",
        task=f"Set the tracked value to {value} using SET_STATE.",
        endpoint="tracked-value",
        tool="SET_STATE",
        args={"value": value},
        verifier_tool="READ_STATE",
        verifier_args={},
        expected_value=value,
        rollback_or_reconciliation_plan="reconcile before retry; rollback only with fresh authority.",
    )


def make_authority(runtime, value="DEPLOYED"):
    grant = AuthorityGrant(
        authority_id="AUTH-SESSION-001",
        trust_root_id="session-test-root",
        endpoint="tracked-value",
        tool="SET_STATE",
        args={"value": value},
        valid_through_epoch=4102444800,
        revoked=False,
    )
    return StaticAuthorityProvider(grant, runtime.resolve_target_fingerprint)


class ControlSessionTests(unittest.TestCase):
    def test_verified_operation_auto_finalizes_without_extra_provider_turn(self):
        runtime = VersionedValueRuntime()
        authority = make_authority(runtime)
        provider = ScriptedProvider([
            {
                "action": "PREDECLARE",
                "endpoint": "tracked-value",
                "tool": "SET_STATE",
                "args": {"value": "DEPLOYED"},
                "target_fingerprint": "tracked-value@v0",
                "verifier": {"tool": "READ_STATE", "args": {}, "expected_value": "DEPLOYED"},
                "rollback": "reconcile before retry; rollback only with fresh authority.",
            },
            {"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}},
        ])
        session = DACPControlSession(make_operation(), bind_core_runtime(runtime, authority, now_epoch=lambda: 1), provider)
        result = session.run()
        self.assertEqual(result.terminal_state, "REPORTED")
        self.assertEqual(result.final_acceptance, "VERIFIED_SUCCEEDED")
        self.assertEqual(result.completion_source, "CONTROL_PLANE_AUTO_FINALIZE")
        self.assertEqual(provider.call_count, 2)
        self.assertEqual(len(result.turns), 2)
        self.assertEqual(result.dispatch_count, 1)
        self.assertEqual(result.applied_count, 1)
        self.assertFalse(result.verification_conflict)
        self.assertEqual(result.control_finalization["acceptance"], "VERIFIED_SUCCEEDED")
        self.assertEqual(runtime.value, "DEPLOYED")
        self.assertEqual(len(runtime.ledger), 1)

    def test_operation_mismatch_with_authority_fails_before_provider_call(self):
        runtime = VersionedValueRuntime()
        authority = make_authority(runtime, "DEPLOYED")
        calls = []

        def provider(prompt):
            calls.append(prompt)
            return fake_result({"action": "REPORT", "result": "PENDING", "note": "should not run"})

        session = DACPControlSession(make_operation("UNAUTHORIZED"), bind_core_runtime(runtime, authority, now_epoch=lambda: 1), provider)
        with self.assertRaisesRegex(RuntimeError, "operation does not match authenticated authority action binding"):
            session.run()
        self.assertEqual(calls, [])
        self.assertEqual(runtime.value, "INITIAL")
        self.assertEqual(runtime.version, 0)

    def test_rendered_operation_action_matches_separate_authority(self):
        runtime = VersionedValueRuntime()
        authority = make_authority(runtime)
        operation = make_operation()
        action = operation.action_spec(runtime.target_fingerprint)
        self.assertIsInstance(action, ActionSpec)
        self.assertEqual(action.action_fingerprint, authority.resolve_authority().action_fingerprint)


if __name__ == "__main__":
    unittest.main()
