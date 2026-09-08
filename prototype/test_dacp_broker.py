import argparse
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import dacp_broker


class BrokerTests(unittest.TestCase):
    def result(self, provider, text, status="SUCCEEDED", completion_status="completed", completion_reason=None):
        return dacp_broker.ProviderResult(
            provider, "test-model", status, text, None, 200, "req", 1,
            {"input_tokens": 1, "output_tokens": 1},
            completion_status, completion_reason, "test-model", {},
        )

    def args(self, tmp, **overrides):
        values = dict(
            prompt="TOKEN", prompt_file=None, expect_exact="TOKEN", peer_challenge=False,
            openai_model="o", anthropic_model="a",
            openai_max_output_tokens=10, anthropic_max_output_tokens=20,
            timeout=5, log_dir=tmp, dry_run=False,
        )
        values.update(overrides)
        return argparse.Namespace(**values)

    def test_expected_exact_verified(self):
        state, checks = dacp_broker.classify(
            [self.result("openai", "TOKEN\n"), self.result("anthropic", " TOKEN ")], "TOKEN"
        )
        self.assertEqual(state, "VERIFIED_MATCH")
        self.assertTrue(checks["openai_matches_expected"])
        self.assertTrue(checks["anthropic_matches_expected"])

    def test_agreement_without_verifier_is_not_verified(self):
        state, _ = dacp_broker.classify(
            [self.result("openai", "same"), self.result("anthropic", "same")], None
        )
        self.assertEqual(state, "SUPPORTED_AGREEMENT")

    def test_pending_provider_makes_run_unresolved(self):
        state, detail = dacp_broker.classify(
            [self.result("openai", "A"), self.result("anthropic", None, "PENDING")], None
        )
        self.assertEqual(state, "UNRESOLVED")
        self.assertIn("not_succeeded", detail["reason"])

    def test_openai_incomplete_response_is_not_succeeded(self):
        payload = {
            "status": "incomplete", "incomplete_details": {"reason": "max_output_tokens"},
            "output": [{"type": "message", "content": [{"type": "output_text", "text": "partial"}]}],
            "usage": {"output_tokens": 32}, "id": "resp", "model": "o",
        }
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test"}), patch.object(
            dacp_broker, "_post_json", return_value=(payload, {"x-request-id": "req"}, 200)
        ):
            result = dacp_broker.call_openai("x", "o", 32, 5)
        self.assertEqual(result.status, "FAILED")
        self.assertEqual(result.completion_reason, "max_output_tokens")

    def test_openai_refusal_is_not_succeeded(self):
        payload = {
            "status": "completed",
            "output": [{"type": "message", "content": [{"type": "refusal", "refusal": "declined"}]}],
            "usage": {"output_tokens": 5}, "id": "resp", "model": "o",
        }
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test"}), patch.object(
            dacp_broker, "_post_json", return_value=(payload, {"x-request-id": "req"}, 200)
        ):
            result = dacp_broker.call_openai("x", "o", 32, 5)
        self.assertEqual(result.status, "FAILED")
        self.assertEqual(result.completion_reason, "refusal")
        self.assertEqual(result.text, "declined")

    def test_openai_request_contract_is_explicit_and_sampling_unpinned(self):
        payload = {
            "status": "completed",
            "output": [{"type": "message", "content": [{"type": "output_text", "text": "173"}]}],
            "usage": {"output_tokens": 5}, "id": "resp", "model": "o",
            "temperature": 1.0, "top_p": 1.0, "reasoning": {"effort": "none"},
        }
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test"}), patch.object(
            dacp_broker, "_post_json", return_value=(payload, {"x-request-id": "req"}, 200)
        ) as post:
            result = dacp_broker.call_openai("PROMPT", "o", 37, 5)
        self.assertEqual(result.status, "SUCCEEDED")
        self.assertEqual(result.response_model, "o")
        req = post.call_args.kwargs["payload"]
        self.assertNotIn("temperature", req)
        self.assertNotIn("top_p", req)
        self.assertEqual(req["instructions"], dacp_broker.CLIENT_RESPONSE_CONTRACT)
        self.assertEqual(req["reasoning"], {"effort": "none"})
        self.assertEqual(req["input"], [{"role": "user", "content": [{"type": "input_text", "text": "PROMPT"}]}])
        self.assertEqual(req["max_output_tokens"], 37)

    def test_anthropic_max_tokens_is_not_succeeded(self):
        payload = {
            "stop_reason": "max_tokens", "content": [{"type": "text", "text": "partial"}],
            "usage": {"output_tokens": 32}, "id": "msg", "model": "a",
        }
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test"}), patch.object(
            dacp_broker, "_post_json", return_value=(payload, {"request-id": "req"}, 200)
        ):
            result = dacp_broker.call_anthropic("x", "a", 32, 5)
        self.assertEqual(result.status, "FAILED")
        self.assertEqual(result.completion_reason, "max_tokens")

    def test_anthropic_end_turn_is_succeeded_even_at_cap(self):
        payload = {
            "stop_reason": "end_turn", "content": [{"type": "text", "text": "173"}],
            "usage": {"output_tokens": 128}, "id": "msg", "model": "a",
        }
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test"}), patch.object(
            dacp_broker, "_post_json", return_value=(payload, {"request-id": "req"}, 200)
        ):
            result = dacp_broker.call_anthropic("x", "a", 128, 5)
        self.assertEqual(result.status, "SUCCEEDED")
        self.assertEqual(result.completion_status, "end_turn")

    def test_anthropic_nonfinal_stop_reasons_are_not_succeeded(self):
        for reason in ("stop_sequence", "tool_use", "pause_turn", "refusal", "model_context_window_exceeded"):
            with self.subTest(reason=reason):
                payload = {
                    "stop_reason": reason, "content": [{"type": "text", "text": "partial"}],
                    "usage": {"output_tokens": 5}, "id": "msg", "model": "a",
                    "stop_details": {"type": reason},
                }
                with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test"}), patch.object(
                    dacp_broker, "_post_json", return_value=(payload, {"request-id": "req"}, 200)
                ):
                    result = dacp_broker.call_anthropic("x", "a", 128, 5)
                self.assertEqual(result.status, "FAILED")
                self.assertEqual(result.completion_reason, reason)

    def test_anthropic_request_contract_is_explicit_and_sampling_unpinned(self):
        payload = {
            "stop_reason": "end_turn", "content": [{"type": "text", "text": "173"}],
            "usage": {"output_tokens": 5}, "id": "msg", "model": "a",
        }
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test"}), patch.object(
            dacp_broker, "_post_json", return_value=(payload, {"request-id": "req"}, 200)
        ) as post:
            result = dacp_broker.call_anthropic("PROMPT", "a", 41, 5)
        self.assertEqual(result.status, "SUCCEEDED")
        self.assertEqual(result.response_model, "a")
        req = post.call_args.kwargs["payload"]
        self.assertNotIn("temperature", req)
        self.assertNotIn("top_p", req)
        self.assertEqual(req["system"], dacp_broker.CLIENT_RESPONSE_CONTRACT)
        self.assertEqual(req["messages"], [{"role": "user", "content": "PROMPT"}])
        self.assertEqual(req["max_tokens"], 41)
        self.assertEqual(post.call_args.kwargs["headers"]["anthropic-version"], "2023-06-01")

    def test_same_semantic_response_contract_reaches_both_provider_adapters(self):
        openai_payload = {
            "status": "completed",
            "output": [{"type": "message", "content": [{"type": "output_text", "text": "173"}]}],
            "usage": {"output_tokens": 5},
            "id": "resp",
            "model": "o",
            "reasoning": {"effort": "none"},
        }
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test"}), patch.object(
            dacp_broker, "_post_json", return_value=(openai_payload, {"x-request-id": "req"}, 200)
        ) as openai_post:
            dacp_broker.call_openai("TASK", "o", 37, 5)

        anthropic_payload = {
            "stop_reason": "end_turn",
            "content": [{"type": "text", "text": "173"}],
            "usage": {"output_tokens": 5},
            "id": "msg",
            "model": "a",
        }
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test"}), patch.object(
            dacp_broker, "_post_json", return_value=(anthropic_payload, {"request-id": "req"}, 200)
        ) as anthropic_post:
            dacp_broker.call_anthropic("TASK", "a", 41, 5)

        openai_req = openai_post.call_args.kwargs["payload"]
        anthropic_req = anthropic_post.call_args.kwargs["payload"]

        self.assertEqual(
            openai_req["instructions"],
            anthropic_req["system"],
        )
        self.assertEqual(openai_req["instructions"], dacp_broker.CLIENT_RESPONSE_CONTRACT)
        self.assertEqual(
            openai_req["input"],
            [{"role": "user", "content": [{"type": "input_text", "text": "TASK"}]}],
        )
        self.assertEqual(
            anthropic_req["messages"],
            [{"role": "user", "content": "TASK"}],
        )

    def test_provider_native_token_caps_are_separate_and_logged(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = self.args(tmp, dry_run=True, openai_max_output_tokens=11, anthropic_max_output_tokens=37)
            self.assertEqual(dacp_broker.run(args), 0)
            first = json.loads(next(Path(tmp).glob("*.jsonl")).read_text().splitlines()[0])
            self.assertEqual(first["openai_max_output_tokens"], 11)
            self.assertEqual(first["anthropic_max_output_tokens"], 37)
            self.assertFalse(first["shared_token_cap_supported"])
            self.assertIn("not_cross_provider_equivalent", first["token_budget_semantics"])

    def test_legacy_shared_token_cap_is_not_in_parser(self):
        destinations = {action.dest for action in dacp_broker.build_parser()._actions}
        self.assertNotIn("max_output_tokens", destinations)

    def test_model_defaults_ignore_environment_overrides(self):
        with patch.dict(os.environ, {"OPENAI_MODEL": "wrong-o", "ANTHROPIC_MODEL": "wrong-a"}, clear=False):
            args = dacp_broker.build_parser().parse_args(["--prompt", "x"])
        self.assertEqual(args.openai_model, dacp_broker.DEFAULT_OPENAI_MODEL)
        self.assertEqual(args.anthropic_model, dacp_broker.DEFAULT_ANTHROPIC_MODEL)

    def test_dry_run_logs_contract_without_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = self.args(tmp, prompt="secret synthetic prompt", expect_exact=None, dry_run=True)
            self.assertEqual(dacp_broker.run(args), 0)
            raw = next(Path(tmp).glob("*.jsonl")).read_text()
            self.assertNotIn("secret synthetic prompt", raw)
            first = json.loads(raw.splitlines()[0])
            self.assertEqual(first["sampling_parameters"], {"openai": "omitted_provider_default", "anthropic": "omitted_provider_default"})
            self.assertEqual(first["prompt_role"], {"openai": "user", "anthropic": "user"})
            self.assertEqual(first["client_response_contract_active"], {"openai": True, "anthropic": True})
            self.assertEqual(first["client_response_contract"]["openai_channel"], "instructions")
            self.assertEqual(first["client_response_contract"]["anthropic_channel"], "system")
            self.assertIn("requested_alias", first["model_identity_semantics"]["openai"])
            self.assertIn("dated_model_id", first["model_identity_semantics"]["anthropic"])

    def test_both_calls_dispatched_and_logged(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = self.args(tmp)
            with patch.object(dacp_broker, "call_openai", return_value=self.result("openai", "TOKEN")) as o, patch.object(
                dacp_broker, "call_anthropic", return_value=self.result("anthropic", "TOKEN")
            ) as a:
                self.assertEqual(dacp_broker.run(args), 0)
            o.assert_called_once_with("TOKEN", "o", 10, 5)
            a.assert_called_once_with("TOKEN", "a", 20, 5)
            events = [json.loads(x) for x in next(Path(tmp).glob("*.jsonl")).read_text().splitlines()]
            self.assertEqual([e["event"] for e in events], ["run_started", "provider_result", "provider_result", "run_completed"])
            self.assertEqual(events[-1]["terminal_state"], "VERIFIED_MATCH")

    def test_peer_challenge_final_contract_follows_untrusted_data(self):
        prompt = dacp_broker.build_peer_challenge_prompt(
            "Compute it. Return only the integer.",
            "157",
            "176",
        )
        data_pos = prompt.index("CHALLENGE_DATA=")
        contract_pos = prompt.index("FINAL RESPONSE CONTRACT:")
        self.assertLess(data_pos, contract_pos)
        self.assertIn('"peer_initial_answer": "176"', prompt)
        self.assertIn('"your_initial_answer": "157"', prompt)
        self.assertTrue(
            prompt.endswith(
                "Your visible response must contain only the final answer requested by the original task."
            )
        )

    def test_peer_challenge_requires_deterministic_verifier(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(SystemExit, "requires --expect-exact"):
                dacp_broker.run(self.args(tmp, expect_exact=None, peer_challenge=True))
            self.assertEqual(list(Path(tmp).glob("*.jsonl")), [])

    def test_peer_challenge_one_round_can_rescue_and_logs_pre_post(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = self.args(tmp, prompt="Solve task; return only final token", expect_exact="CORRECT", peer_challenge=True)
            with patch.object(dacp_broker, "call_openai", side_effect=[self.result("openai", "WRONG-O"), self.result("openai", "CORRECT")]) as o, patch.object(
                dacp_broker, "call_anthropic", side_effect=[self.result("anthropic", "WRONG-A"), self.result("anthropic", "CORRECT")]
            ) as a:
                self.assertEqual(dacp_broker.run(args), 0)
            self.assertEqual(o.call_count, 2)
            self.assertEqual(a.call_count, 2)
            self.assertIn("WRONG-A", o.call_args_list[1].args[0])
            self.assertIn("WRONG-O", a.call_args_list[1].args[0])
            events = [json.loads(x) for x in next(Path(tmp).glob("*.jsonl")).read_text().splitlines()]
            final = events[-1]
            self.assertEqual(final["terminal_state"], "VERIFIED_MATCH")
            self.assertTrue(final["verification"]["challenge"]["rescue_observed"])
            self.assertFalse(final["verification"]["challenge"]["negative_value_observed"])

    def test_peer_challenge_negative_value_is_detected(self):
        detail = dacp_broker.assess_peer_challenge(
            [self.result("openai", "CORRECT"), self.result("anthropic", "WRONG")],
            [self.result("openai", "WRONG2"), self.result("anthropic", "CORRECT")], "CORRECT"
        )
        self.assertTrue(detail["openai_degraded"])
        self.assertTrue(detail["anthropic_rescued"])
        self.assertTrue(detail["negative_value_observed"])

    def test_peer_challenge_wrong_convergence_flags_mutual_reinforcement_risk(self):
        detail = dacp_broker.assess_peer_challenge(
            [self.result("openai", "A"), self.result("anthropic", "B")],
            [self.result("openai", "SAME-WRONG"), self.result("anthropic", "SAME-WRONG")], "CORRECT"
        )
        self.assertTrue(detail["mutual_reinforcement_risk_observed"])
        self.assertFalse(detail["rescue_observed"])

    def test_peer_challenge_does_not_score_incomplete_output(self):
        detail = dacp_broker.assess_peer_challenge(
            [self.result("openai", "CORRECT"), self.result("anthropic", "WRONG")],
            [self.result("openai", "CORRECT"), self.result("anthropic", "partial", "FAILED", "max_tokens", "max_tokens")],
            "CORRECT",
        )
        self.assertFalse(detail["anthropic_changed_after_peer"])
        self.assertFalse(detail["anthropic_rescued"])
        self.assertFalse(detail["anthropic_degraded"])
        self.assertFalse(detail["mutual_reinforcement_risk_observed"])

    def test_peer_challenge_not_attempted_if_initial_call_unresolved(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = self.args(tmp, peer_challenge=True)
            with patch.object(dacp_broker, "call_openai", return_value=self.result("openai", "TOKEN")) as o, patch.object(
                dacp_broker, "call_anthropic", return_value=self.result("anthropic", None, "PENDING")
            ) as a:
                self.assertEqual(dacp_broker.run(args), 2)
            self.assertEqual(o.call_count, 1)
            self.assertEqual(a.call_count, 1)
            events = [json.loads(x) for x in next(Path(tmp).glob("*.jsonl")).read_text().splitlines()]
            self.assertNotIn("peer_challenge_started", [e["event"] for e in events])
            self.assertEqual(events[-1]["terminal_state"], "UNRESOLVED")
            self.assertFalse(events[-1]["verification"]["challenge_attempted"])


if __name__ == "__main__":
    unittest.main()
