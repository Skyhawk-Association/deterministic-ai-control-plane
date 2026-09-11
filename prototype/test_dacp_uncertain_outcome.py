import json
import unittest

import dacp_broker
import dacp_uncertain_outcome as uncertain


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


def predeclare():
    return {
        "action": "PREDECLARE",
        "endpoint": "set tracked value",
        "tool": "SET_STATE",
        "args": {"value": "DEPLOYED"},
        "target_fingerprint": "tracked-value",
        "verifier": {"tool": "READ_STATE", "args": {}, "expected_value": "DEPLOYED"},
        "rollback": "restore prior state after reconciliation",
    }


CALL_SET = {"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}}
READ = {"action": "CALL", "tool": "READ_STATE", "args": {}}


class UncertainOutcomeTests(unittest.TestCase):
    def test_response_lost_but_applied_is_reconciled_without_duplicate(self):
        provider = ScriptedProvider([
            predeclare(), CALL_SET, READ,
            {"action": "REPORT", "result": "SUCCEEDED", "note": "readback proved commit"},
        ])
        log = uncertain.run_episode(uncertain.SCENARIOS[uncertain.PENDING_APPLIED], provider)
        self.assertTrue(log.pending_entered)
        self.assertEqual(log.consequential_execute_count, 1)
        self.assertEqual(log.duplicate_retry_block_count, 0)
        self.assertEqual(log.post_pending_read_count, 1)
        self.assertEqual(log.outcome_classification, "SUCCEEDED")
        self.assertTrue(log.claim_matches_classification)

    def test_old_state_after_pending_remains_pending(self):
        provider = ScriptedProvider([
            predeclare(), CALL_SET, READ,
            {"action": "REPORT", "result": "PENDING", "note": "cannot safely classify failure yet"},
        ])
        log = uncertain.run_episode(uncertain.SCENARIOS[uncertain.PENDING_UNRESOLVED], provider)
        self.assertTrue(log.pending_entered)
        self.assertEqual(log.consequential_execute_count, 1)
        self.assertEqual(log.observed_value, "INITIAL")
        self.assertEqual(log.outcome_classification, "PENDING")
        self.assertTrue(log.claim_matches_classification)

    def test_delayed_commit_resolves_on_second_bounded_read_without_retry(self):
        provider = ScriptedProvider([
            predeclare(), CALL_SET, READ, READ,
            {"action": "REPORT", "result": "SUCCEEDED", "note": "second read proved delayed commit"},
        ])
        log = uncertain.run_episode(uncertain.SCENARIOS[uncertain.PENDING_DELAYED_COMMIT], provider)
        self.assertTrue(log.pending_entered)
        self.assertTrue(log.delayed_commit_injected)
        self.assertEqual(log.consequential_execute_count, 1)
        self.assertEqual(log.duplicate_retry_block_count, 0)
        self.assertEqual(log.post_pending_read_count, 2)
        self.assertEqual(log.observed_value, "DEPLOYED")
        self.assertEqual(log.outcome_classification, "SUCCEEDED")
        self.assertTrue(log.claim_matches_classification)

    def test_retry_after_pending_is_blocked_even_under_pressure(self):
        provider = ScriptedProvider([
            predeclare(), CALL_SET, CALL_SET, READ,
            {"action": "REPORT", "result": "PENDING", "note": "retry blocked; unresolved"},
        ])
        log = uncertain.run_episode(uncertain.SCENARIOS[uncertain.PENDING_RETRY_PRESSURE], provider)
        self.assertEqual(log.consequential_execute_count, 1)
        self.assertEqual(log.duplicate_retry_block_count, 1)
        self.assertEqual(log.turns[2]["broker_reply"]["error"], "UNCERTAIN_OUTCOME_RETRY_BLOCKED")

    def test_undeclared_consequential_call_is_still_blocked(self):
        provider = ScriptedProvider([
            CALL_SET,
            {"action": "REPORT", "result": "PENDING", "note": "blocked before dispatch"},
        ])
        log = uncertain.run_episode(uncertain.SCENARIOS[uncertain.PENDING_APPLIED], provider)
        self.assertEqual(log.turns[0]["broker_reply"]["error"], "GATE_BLOCKED")
        self.assertEqual(log.consequential_execute_count, 0)
        self.assertFalse(log.pending_entered)


if __name__ == "__main__":
    unittest.main()
