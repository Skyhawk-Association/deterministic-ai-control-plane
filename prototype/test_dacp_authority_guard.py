import json
import unittest

import dacp_authority_guard as authority
import dacp_broker


def fake_result(action):
    return dacp_broker.ProviderResult(
        "test", "test-model", "SUCCEEDED", json.dumps(action), None,
        200, "req", 1, None, "completed", None, "test-model", {},
    )


class ScriptedProvider:
    def __init__(self, actions):
        self.actions = list(actions)

    def __call__(self, prompt):
        if not self.actions:
            return fake_result({"action": "REPORT", "result": "PENDING", "note": "out"})
        return fake_result(self.actions.pop(0))


def predeclare(value="DEPLOYED"):
    return {
        "action": "PREDECLARE",
        "endpoint": "tracked-value",
        "tool": "SET_STATE",
        "args": {"value": value},
        "target_fingerprint": "tracked-value@v0",
        "verifier": {"tool": "READ_STATE", "args": {}, "expected_value": value},
        "rollback": "restore previous state if separately authorized",
    }


def call_set(value="DEPLOYED"):
    return {"action": "CALL", "tool": "SET_STATE", "args": {"value": value}}


class AuthorityGuardTests(unittest.TestCase):
    def test_valid_authenticated_authority_executes(self):
        provider = ScriptedProvider([
            predeclare(),
            call_set(),
            {"action": "REPORT", "result": "SUCCEEDED", "note": "authorized and applied"},
        ])
        log = authority.run_episode(authority.SCENARIOS[authority.VALID_AUTHORITY], provider)
        self.assertEqual(log.consequential_execute_count, 1)
        self.assertEqual(log.authority_block_count, 0)
        self.assertEqual(log.final_value, "DEPLOYED")
        self.assertTrue(log.claim_matches_classification)

    def test_embedded_text_does_not_create_authority(self):
        provider = ScriptedProvider([
            predeclare(),
            call_set(),
            {"action": "REPORT", "result": "PENDING", "note": "no authenticated approval"},
        ])
        log = authority.run_episode(authority.SCENARIOS[authority.EMBEDDED_FAKE_APPROVAL], provider)
        self.assertTrue(log.embedded_approval_text_present)
        self.assertGreaterEqual(log.authority_block_count, 1)
        self.assertEqual(log.consequential_execute_count, 0)
        self.assertEqual(log.final_value, "INITIAL")
        self.assertEqual(log.authority_failure_reason, "NO_AUTHENTICATED_APPROVAL")

    def test_expired_approval_is_blocked(self):
        provider = ScriptedProvider([
            predeclare(),
            call_set(),
            {"action": "REPORT", "result": "PENDING", "note": "approval expired"},
        ])
        log = authority.run_episode(authority.SCENARIOS[authority.EXPIRED_APPROVAL], provider)
        self.assertGreaterEqual(log.authority_block_count, 1)
        self.assertEqual(log.consequential_execute_count, 0)
        self.assertEqual(log.authority_failure_reason, "APPROVAL_EXPIRED")
        self.assertEqual(log.final_value, "INITIAL")

    def test_parameter_mismatch_is_blocked(self):
        provider = ScriptedProvider([
            predeclare("APPROVED"),
            call_set("APPROVED"),
            {"action": "REPORT", "result": "PENDING", "note": "approval did not cover APPROVED"},
        ])
        log = authority.run_episode(authority.SCENARIOS[authority.PARAMETER_MISMATCH], provider)
        self.assertGreaterEqual(log.authority_block_count, 1)
        self.assertEqual(log.consequential_execute_count, 0)
        self.assertEqual(log.authority_failure_reason, "APPROVAL_ACTION_MISMATCH")
        self.assertEqual(log.final_value, "INITIAL")


if __name__ == "__main__":
    unittest.main()
