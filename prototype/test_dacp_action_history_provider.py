import json
import unittest

import dacp_action_history_provider as history
import dacp_gate_beta_v2 as gate


class HistoryTransportTests(unittest.TestCase):
    def delayed_messages(self):
        return gate.delayed_history_messages(gate.SCENARIOS[gate.DELAYED_SCENARIO_ID])

    def test_delayed_history_has_83_role_separated_messages(self):
        messages = self.delayed_messages()
        self.assertEqual(len(messages), 83)
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[-1]["role"], "user")
        self.assertEqual(
            sum(gate.SESSION_RULE in m["content"] for m in messages),
            1,
        )
        self.assertNotIn(gate.SESSION_RULE, messages[-1]["content"])
        self.assertIn("DEPLOYED", messages[-1]["content"])

    def test_roles_alternate_through_neutral_history(self):
        messages = self.delayed_messages()
        for index, message in enumerate(messages[:-1]):
            expected = "user" if index % 2 == 0 else "assistant"
            self.assertEqual(message["role"], expected)

    def test_openai_history_adapter_preserves_native_message_roles(self):
        captured = {}

        def transport(**kwargs):
            captured.update(kwargs)
            return ({
                "id": "resp_test",
                "status": "completed",
                "model": "gpt-test",
                "output": [{
                    "type": "function_call",
                    "name": "DACP_PREDECLARE",
                    "arguments": json.dumps({
                        "endpoint": "e",
                        "tool": "SET_STATE",
                        "args": {"value": "DEPLOYED"},
                        "target_fingerprint": "DEPLOYED",
                        "verifier": "v",
                        "rollback": "r",
                    }),
                }],
                "usage": {},
            }, {}, 200)

        result = history.call_openai_action_history(
            self.delayed_messages(), "gpt-test", 256, 60, transport=transport
        )
        self.assertEqual(result.status, "SUCCEEDED")
        self.assertEqual(len(captured["payload"]["input"]), 83)
        self.assertEqual(captured["payload"]["input"][0]["role"], "user")
        self.assertEqual(captured["payload"]["input"][1]["role"], "assistant")
        self.assertEqual(captured["payload"]["input"][-1]["role"], "user")

    def test_anthropic_history_adapter_preserves_native_message_roles(self):
        captured = {}

        def transport(**kwargs):
            captured.update(kwargs)
            return ({
                "id": "msg_test",
                "stop_reason": "tool_use",
                "model": "claude-test",
                "content": [{
                    "type": "tool_use",
                    "name": "DACP_PREDECLARE",
                    "input": {
                        "endpoint": "e",
                        "tool": "SET_STATE",
                        "args": {"value": "DEPLOYED"},
                        "target_fingerprint": "DEPLOYED",
                        "verifier": "v",
                        "rollback": "r",
                    },
                }],
                "usage": {},
            }, {}, 200)

        result = history.call_anthropic_action_history(
            self.delayed_messages(), "claude-test", 256, 60, transport=transport
        )
        self.assertEqual(result.status, "SUCCEEDED")
        self.assertEqual(len(captured["payload"]["messages"]), 83)
        self.assertEqual(captured["payload"]["messages"][0]["role"], "user")
        self.assertEqual(captured["payload"]["messages"][1]["role"], "assistant")
        self.assertEqual(captured["payload"]["messages"][-1]["role"], "user")


if __name__ == "__main__":
    unittest.main()
