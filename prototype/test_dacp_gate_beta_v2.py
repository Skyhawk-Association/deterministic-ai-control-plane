import json
import unittest

import dacp_broker
import dacp_gate_beta_v2 as gate


def fake_result(action):
    return dacp_broker.ProviderResult(
        "test", "test-model", "SUCCEEDED", json.dumps(action), None,
        200, "req", 1, None, "completed", None, "test-model", {},
    )


class ScriptedProvider:
    def __init__(self, actions):
        self.actions = list(actions)
        self.prompts = []

    def __call__(self, prompt):
        self.prompts.append(prompt)
        if not self.actions:
            return fake_result({"action": "REPORT", "result": "FAILED", "note": "out"})
        return fake_result(self.actions.pop(0))


class GateV2Tests(unittest.TestCase):
    def predeclare(self, tool="SET_STATE"):
        return {
            "action": "PREDECLARE",
            "endpoint": "set value",
            "tool": tool,
            "args": {"value": "DEPLOYED"},
            "target_fingerprint": "DEPLOYED",
            "verifier": "independent readback",
            "rollback": "restore INITIAL",
        }

    def test_verifier_evidence_is_returned_after_consequential_call(self):
        provider = ScriptedProvider([
            self.predeclare(),
            {"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}},
            {"action": "REPORT", "result": "SUCCEEDED", "note": "verified"},
        ])
        log = gate.run_episode(gate.SCENARIOS["buried_request"], provider)
        call_reply = log.turns[1]["broker_reply"]
        self.assertEqual(call_reply["verifier_result"], "SUCCEEDED")
        self.assertEqual(call_reply["verifier_observed_value"], "DEPLOYED")
        self.assertEqual(call_reply["required_next_action"], "REPORT")
        self.assertTrue(log.claim_matches_verifier)

    def test_post_verification_duplicate_call_is_blocked_without_reexecution(self):
        provider = ScriptedProvider([
            self.predeclare(),
            {"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}},
            {"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}},
            {"action": "REPORT", "result": "SUCCEEDED", "note": "done"},
        ])
        log = gate.run_episode(gate.SCENARIOS["urgency_pressure"], provider)
        self.assertEqual(log.consequential_execute_count, 1)
        self.assertEqual(log.post_verify_block_count, 1)
        self.assertEqual(log.turns[2]["broker_reply"]["error"], "AWAITING_REPORT")
        self.assertTrue(log.claim_matches_verifier)

    def test_deceptive_verifier_failure_is_visible_and_report_can_match_it(self):
        provider = ScriptedProvider([
            self.predeclare("FAIL_SET_STATE"),
            {"action": "CALL", "tool": "FAIL_SET_STATE", "args": {"value": "DEPLOYED"}},
            {"action": "REPORT", "result": "FAILED", "note": "verifier disagreed"},
        ])
        log = gate.run_episode(gate.SCENARIOS["deceptive_tool"], provider)
        self.assertEqual(log.verifier_result, "FAILED")
        self.assertEqual(log.turns[1]["broker_reply"]["verifier_observed_value"], "INITIAL")
        self.assertTrue(log.claim_matches_verifier)

    def test_delayed_context_places_rule_once_before_40_neutral_turns(self):
        provider = ScriptedProvider([
            self.predeclare(),
            {"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}},
            {"action": "REPORT", "result": "SUCCEEDED", "note": "done"},
        ])
        scenario = gate.SCENARIOS[gate.DELAYED_SCENARIO_ID]
        log = gate.run_episode(scenario, provider)
        first_prompt = provider.prompts[0]
        self.assertEqual(first_prompt.count("SESSION RULE ESTABLISHED AT TURN 0"), 1)
        self.assertIn("USER TURN 40:", first_prompt)
        self.assertIn("ASSISTANT TURN 40:", first_prompt)
        self.assertIn("USER TURN 41:", first_prompt)
        self.assertEqual(log.context_mode, "RULE_ONCE_40_TURNS_EARLIER")

    def test_exact_knowledge_probe_logs_raw_text(self):
        provider = lambda prompt: dacp_broker.ProviderResult(
            "test", "test-model", "SUCCEEDED", "PREDECLARE", None,
            200, "req", 1, None, "completed", None, "test-model", {},
        )
        result = gate.run_knowledge_probe(provider)
        self.assertTrue(result["rule_knowledge_test"])
        self.assertEqual(result["raw_text"], "PREDECLARE")
        self.assertEqual(result["knowledge_probe_method"], "DIRECT_EXACT_TOKEN")


if __name__ == "__main__":
    unittest.main()
