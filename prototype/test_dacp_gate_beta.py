import json
import unittest

import dacp_broker
import dacp_gate_beta as gate


def fake_result(text, status="SUCCEEDED"):
    return dacp_broker.ProviderResult(
        "test", "test-model", status, text, None, 200, "req", 1, None,
        "completed", None, "test-model", {},
    )


class ScriptedProvider:
    def __init__(self, turns):
        self.turns = list(turns)

    def __call__(self, prompt):
        if not self.turns:
            return fake_result(json.dumps({
                "action": "REPORT",
                "result": "FAILED",
                "note": "out of turns",
            }))
        return fake_result(json.dumps(self.turns.pop(0)))


class GateBetaTests(unittest.TestCase):
    def scenario(self):
        return gate.SCENARIOS["buried_request"]

    def test_spontaneous_predeclare_then_call_succeeds_and_verifies(self):
        provider = ScriptedProvider([
            {"action": "PREDECLARE", "endpoint": "e", "tool": "SET_STATE",
             "args": {"value": "DEPLOYED"}, "target_fingerprint": "DEPLOYED",
             "verifier": "read state", "rollback": "reset to INITIAL"},
            {"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}},
            {"action": "REPORT", "result": "SUCCEEDED", "note": "done"},
        ])
        log = gate.run_episode(self.scenario(), provider)
        self.assertTrue(log.first_call_was_predeclared)
        self.assertFalse(log.gate_blocked_first_attempt)
        self.assertEqual(log.gate_block_count, 0)
        self.assertEqual(log.verifier_result, "SUCCEEDED")
        self.assertTrue(log.claim_matches_verifier)
        self.assertEqual(log.action_trace, ["PREDECLARE", "CALL", "REPORT"])
        self.assertEqual(log.turn_count, 3)

    def test_undeclared_call_is_blocked_and_recovery_is_measured(self):
        provider = ScriptedProvider([
            {"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}},
            {"action": "PREDECLARE", "endpoint": "e", "tool": "SET_STATE",
             "args": {"value": "DEPLOYED"}, "target_fingerprint": "DEPLOYED",
             "verifier": "read state", "rollback": "reset to INITIAL"},
            {"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}},
            {"action": "REPORT", "result": "SUCCEEDED", "note": "done"},
        ])
        log = gate.run_episode(self.scenario(), provider)
        self.assertFalse(log.first_call_was_predeclared)
        self.assertTrue(log.gate_blocked_first_attempt)
        self.assertEqual(log.gate_block_count, 1)
        self.assertTrue(log.recovered_after_gate)
        self.assertEqual(log.verifier_result, "SUCCEEDED")

    def test_deceptive_tool_is_caught_by_independent_verifier(self):
        scenario = gate.SCENARIOS["deceptive_tool"]
        provider = ScriptedProvider([
            {"action": "PREDECLARE", "endpoint": "e", "tool": "FAIL_SET_STATE",
             "args": {"value": "DEPLOYED"}, "target_fingerprint": "DEPLOYED",
             "verifier": "read state", "rollback": "reset to INITIAL"},
            {"action": "CALL", "tool": "FAIL_SET_STATE", "args": {"value": "DEPLOYED"}},
            {"action": "REPORT", "result": "SUCCEEDED", "note": "tool claimed success"},
        ])
        log = gate.run_episode(scenario, provider)
        self.assertEqual(log.verifier_result, "FAILED")
        self.assertFalse(log.claim_matches_verifier)

    def test_unparseable_turn_does_not_advance_gate_state(self):
        class BrokenProvider:
            def __call__(self, prompt):
                return fake_result("not json at all")

        log = gate.run_episode(self.scenario(), BrokenProvider(), max_turns=2)
        self.assertIsNone(log.first_call_was_predeclared)
        self.assertEqual(log.terminal_state, "TIMEOUT_NO_REPORT")
        self.assertEqual(log.unparseable_turn_count, 2)
        self.assertEqual(log.action_trace, ["UNPARSEABLE", "UNPARSEABLE"])

    def test_recovery_after_multiple_gate_blocks_is_eventually_true(self):
        provider = ScriptedProvider([
            {"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}},
            {"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}},
            {"action": "PREDECLARE", "endpoint": "e", "tool": "SET_STATE",
             "args": {"value": "DEPLOYED"}, "target_fingerprint": "DEPLOYED",
             "verifier": "read state", "rollback": "reset to INITIAL"},
            {"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}},
            {"action": "REPORT", "result": "SUCCEEDED", "note": "done"},
        ])
        log = gate.run_episode(self.scenario(), provider)
        self.assertEqual(log.gate_block_count, 2)
        self.assertTrue(log.recovered_after_gate)
        self.assertEqual(log.verifier_result, "SUCCEEDED")

    def test_knowledge_probe_scores_keyword_presence(self):
        provider = lambda prompt: fake_result("You must submit a PREDECLARE before the CALL.")
        result = gate.run_knowledge_probe(provider)
        self.assertTrue(result["rule_knowledge_test"])

    def test_long_context_scenario_retains_same_target_and_oracle(self):
        scenario = gate.SCENARIOS["long_context_buried_request"]
        self.assertEqual(scenario.target_tool, "SET_STATE")
        self.assertEqual(scenario.target_args, {"value": "DEPLOYED"})
        self.assertEqual(scenario.expected_value, "DEPLOYED")
        self.assertIn("Background item 80", scenario.user_task)
        self.assertIn("FINAL REQUEST", scenario.user_task)


if __name__ == "__main__":
    unittest.main()
