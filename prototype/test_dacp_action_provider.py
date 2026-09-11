import json
import unittest

import dacp_action_provider as actions


class NativeActionAdapterTests(unittest.TestCase):
    def verifier(self, expected="DEPLOYED"):
        return {
            "tool": "READ_STATE",
            "args": {"value": None},
            "expected_value": expected,
        }

    def test_openai_native_call_is_normalized(self):
        seen = {}

        def transport(**kwargs):
            seen.update(kwargs)
            return (
                {
                    "status": "completed",
                    "model": "gpt-test",
                    "id": "r1",
                    "output": [
                        {
                            "type": "function_call",
                            "name": "DACP_CALL",
                            "arguments": '{"tool":"SET_STATE","args":{"value":"DEPLOYED"}}',
                        }
                    ],
                },
                {"x-request-id": "x1"},
                200,
            )

        result = actions.call_openai_action("p", "gpt-test", 256, 60, transport)
        self.assertEqual(result.status, "SUCCEEDED")
        self.assertEqual(
            json.loads(result.text),
            {"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}},
        )
        self.assertEqual(seen["payload"]["tool_choice"], "required")
        self.assertFalse(seen["payload"]["parallel_tool_calls"])
        self.assertTrue(all(tool["strict"] for tool in seen["payload"]["tools"]))

    def test_openai_multiple_calls_are_rejected(self):
        def transport(**kwargs):
            call = {
                "type": "function_call",
                "name": "DACP_REPORT",
                "arguments": '{"result":"FAILED","note":"x"}',
            }
            return ({"status": "completed", "output": [call, call]}, {}, 200)

        result = actions.call_openai_action("p", "gpt-test", 256, 60, transport)
        self.assertEqual(result.status, "FAILED")
        self.assertIn("exactly one", result.error)

    def test_anthropic_native_call_is_normalized(self):
        seen = {}

        def transport(**kwargs):
            seen.update(kwargs)
            return (
                {
                    "stop_reason": "tool_use",
                    "model": "claude-test",
                    "id": "m1",
                    "content": [
                        {
                            "type": "tool_use",
                            "id": "t1",
                            "name": "DACP_PREDECLARE",
                            "input": {
                                "endpoint": "e",
                                "tool": "SET_STATE",
                                "args": {"value": "DEPLOYED"},
                                "target_fingerprint": "f",
                                "verifier": self.verifier(),
                                "rollback": "r",
                            },
                        }
                    ],
                },
                {"request-id": "a1"},
                200,
            )

        result = actions.call_anthropic_action("p", "claude-test", 256, 60, transport)
        self.assertEqual(result.status, "SUCCEEDED")
        parsed = json.loads(result.text)
        self.assertEqual(parsed["action"], "PREDECLARE")
        self.assertEqual(parsed["verifier"], {"tool": "READ_STATE", "args": {}, "expected_value": "DEPLOYED"})
        self.assertEqual(
            seen["payload"]["tool_choice"],
            {"type": "any", "disable_parallel_tool_use": True},
        )

    def test_anthropic_text_only_response_is_rejected(self):
        def transport(**kwargs):
            return (
                {
                    "stop_reason": "end_turn",
                    "content": [{"type": "text", "text": "```json\n{}\n```"}],
                },
                {},
                200,
            )

        result = actions.call_anthropic_action("p", "claude-test", 256, 60, transport)
        self.assertEqual(result.status, "FAILED")
        self.assertIn("tool_use", result.error)

    def test_read_state_null_normalizes_to_empty_args(self):
        action = actions.normalize_native_action(
            "DACP_CALL", {"tool": "READ_STATE", "args": {"value": None}}
        )
        self.assertEqual(action, {"action": "CALL", "tool": "READ_STATE", "args": {}})

    def test_state_write_requires_string_value(self):
        with self.assertRaises(ValueError):
            actions.normalize_native_action(
                "DACP_CALL", {"tool": "SET_STATE", "args": {"value": None}}
            )

    def test_predeclare_requires_structured_verifier(self):
        with self.assertRaises(ValueError):
            actions.normalize_native_action(
                "DACP_PREDECLARE",
                {
                    "endpoint": "e",
                    "tool": "SET_STATE",
                    "args": {"value": "DEPLOYED"},
                    "target_fingerprint": "f",
                    "verifier": "trust the setter",
                    "rollback": "r",
                },
            )


if __name__ == "__main__":
    unittest.main()
