import json
import unittest

import dacp_broker
import dacp_rollback_guard as rollback


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


def predeclare(fp="tracked-value@v1"):
    return {
        "action": "PREDECLARE",
        "endpoint": "restore prior state",
        "tool": "SET_STATE",
        "args": {"value": "INITIAL"},
        "target_fingerprint": fp,
        "verifier": {"tool": "READ_STATE", "args": {}, "expected_value": "INITIAL"},
        "rollback": "none",
    }


CALL_ROLLBACK = {"action": "CALL", "tool": "SET_STATE", "args": {"value": "INITIAL"}}


class RollbackGuardTests(unittest.TestCase):
    def test_safe_rollback_executes_once(self):
        provider = ScriptedProvider([
            predeclare(), CALL_ROLLBACK,
            {"action": "REPORT", "result": "SUCCEEDED", "note": "restored"},
        ])
        log = rollback.run_episode(rollback.SCENARIOS[rollback.SAFE_ROLLBACK], provider)
        self.assertEqual(log.rollback_execute_count, 1)
        self.assertEqual(log.rollback_authority_block_count, 0)
        self.assertEqual(log.final_value, "INITIAL")
        self.assertTrue(log.claim_matches_classification)

    def test_later_legitimate_state_invalidates_automatic_rollback(self):
        provider = ScriptedProvider([
            predeclare(), CALL_ROLLBACK,
            {"action": "REPORT", "result": "PENDING", "note": "new authority required"},
        ])
        log = rollback.run_episode(rollback.SCENARIOS[rollback.STALE_ROLLBACK], provider)
        self.assertTrue(log.later_legitimate_state_injected)
        self.assertTrue(log.compensation_scope_invalidated)
        self.assertEqual(log.rollback_authority_block_count, 1)
        self.assertEqual(log.rollback_execute_count, 0)
        self.assertEqual(log.final_value, "APPROVED")
        self.assertTrue(log.later_legitimate_state_preserved)
        self.assertEqual(log.outcome_classification, "PENDING")
        self.assertTrue(log.claim_matches_classification)

    def test_stale_rollback_declaration_is_rejected_before_call(self):
        provider = ScriptedProvider([
            predeclare("tracked-value@v0"),
            {"action": "REPORT", "result": "PENDING", "note": "stale binding"},
        ])
        log = rollback.run_episode(rollback.SCENARIOS[rollback.SAFE_ROLLBACK], provider)
        self.assertEqual(log.rollback_execute_count, 0)
        self.assertEqual(log.final_value, "DEPLOYED")


if __name__ == "__main__":
    unittest.main()
