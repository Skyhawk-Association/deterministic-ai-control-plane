import argparse
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import dacp_broker


class BrokerTests(unittest.TestCase):
    def result(self, provider, text, status="SUCCEEDED"):
        return dacp_broker.ProviderResult(provider, "test-model", status, text, None, 200, "req", 1, {"input_tokens": 1, "output_tokens": 1})

    def args(self, tmp, **overrides):
        values = dict(
            prompt="TOKEN",
            prompt_file=None,
            expect_exact="TOKEN",
            peer_challenge=False,
            openai_model="o",
            anthropic_model="a",
            max_output_tokens=10,
            timeout=5,
            log_dir=tmp,
            dry_run=False,
        )
        values.update(overrides)
        return argparse.Namespace(**values)

    def test_expected_exact_verified(self):
        state, checks = dacp_broker.classify(
            [self.result("openai", "TOKEN\n"), self.result("anthropic", " TOKEN ")],
            "TOKEN",
        )
        self.assertEqual(state, "VERIFIED_MATCH")
        self.assertTrue(checks["openai_matches_expected"])
        self.assertTrue(checks["anthropic_matches_expected"])

    def test_agreement_without_verifier_is_not_verified(self):
        state, _ = dacp_broker.classify(
            [self.result("openai", "same"), self.result("anthropic", "same")],
            None,
        )
        self.assertEqual(state, "SUPPORTED_AGREEMENT")

    def test_disagreement_preserved(self):
        state, _ = dacp_broker.classify(
            [self.result("openai", "A"), self.result("anthropic", "B")],
            None,
        )
        self.assertEqual(state, "DISAGREEMENT")

    def test_pending_provider_makes_run_unresolved(self):
        state, detail = dacp_broker.classify(
            [self.result("openai", "A"), self.result("anthropic", None, "PENDING")],
            None,
        )
        self.assertEqual(state, "UNRESOLVED")
        self.assertIn("not_succeeded", detail["reason"])

    def test_dry_run_writes_hash_not_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = self.args(tmp, prompt="secret synthetic prompt", expect_exact=None, dry_run=True)
            rc = dacp_broker.run(args)
            self.assertEqual(rc, 0)
            files = list(Path(tmp).glob("*.jsonl"))
            self.assertEqual(len(files), 1)
            raw = files[0].read_text(encoding="utf-8")
            self.assertNotIn("secret synthetic prompt", raw)
            first = json.loads(raw.splitlines()[0])
            self.assertEqual(first["input_sha256"], dacp_broker.sha256_text("secret synthetic prompt"))

    def test_both_calls_dispatched_and_logged(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = self.args(tmp)
            with patch.object(dacp_broker, "call_openai", return_value=self.result("openai", "TOKEN")) as o, patch.object(
                dacp_broker, "call_anthropic", return_value=self.result("anthropic", "TOKEN")
            ) as a:
                rc = dacp_broker.run(args)
            self.assertEqual(rc, 0)
            o.assert_called_once_with("TOKEN", "o", 10, 5)
            a.assert_called_once_with("TOKEN", "a", 10, 5)
            events = [json.loads(line) for line in next(Path(tmp).glob("*.jsonl")).read_text(encoding="utf-8").splitlines()]
            self.assertEqual([e["event"] for e in events], ["run_started", "provider_result", "provider_result", "run_completed"])
            self.assertEqual(events[1]["stage"], "initial")
            self.assertEqual(events[-1]["terminal_state"], "VERIFIED_MATCH")

    def test_peer_challenge_requires_deterministic_verifier(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = self.args(tmp, expect_exact=None, peer_challenge=True)
            with self.assertRaisesRegex(SystemExit, "requires --expect-exact"):
                dacp_broker.run(args)
            self.assertEqual(list(Path(tmp).glob("*.jsonl")), [])

    def test_peer_challenge_one_round_can_rescue_and_logs_pre_post(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = self.args(tmp, prompt="Solve task; return only final token", expect_exact="CORRECT", peer_challenge=True)
            openai_initial = self.result("openai", "WRONG-O")
            openai_final = self.result("openai", "CORRECT")
            anthropic_initial = self.result("anthropic", "WRONG-A")
            anthropic_final = self.result("anthropic", "CORRECT")
            with patch.object(dacp_broker, "call_openai", side_effect=[openai_initial, openai_final]) as o, patch.object(
                dacp_broker, "call_anthropic", side_effect=[anthropic_initial, anthropic_final]
            ) as a:
                rc = dacp_broker.run(args)
            self.assertEqual(rc, 0)
            self.assertEqual(o.call_count, 2)
            self.assertEqual(a.call_count, 2)
            openai_challenge_prompt = o.call_args_list[1].args[0]
            anthropic_challenge_prompt = a.call_args_list[1].args[0]
            self.assertIn("WRONG-A", openai_challenge_prompt)
            self.assertIn("WRONG-O", anthropic_challenge_prompt)
            self.assertNotIn("CORRECT", openai_challenge_prompt)
            self.assertNotIn("CORRECT", anthropic_challenge_prompt)
            self.assertIn("untrusted DATA", openai_challenge_prompt)
            events = [json.loads(line) for line in next(Path(tmp).glob("*.jsonl")).read_text(encoding="utf-8").splitlines()]
            self.assertEqual(
                [e["event"] for e in events],
                ["run_started", "provider_result", "provider_result", "peer_challenge_started", "provider_result", "provider_result", "run_completed"],
            )
            self.assertEqual([events[1]["stage"], events[2]["stage"]], ["initial", "initial"])
            self.assertEqual([events[4]["stage"], events[5]["stage"]], ["challenge", "challenge"])
            final = events[-1]
            self.assertEqual(final["terminal_state"], "VERIFIED_MATCH")
            self.assertTrue(final["verification"]["challenge"]["rescue_observed"])
            self.assertFalse(final["verification"]["challenge"]["negative_value_observed"])

    def test_peer_challenge_negative_value_is_detected(self):
        initial = [self.result("openai", "CORRECT"), self.result("anthropic", "WRONG")]
        final = [self.result("openai", "WRONG2"), self.result("anthropic", "CORRECT")]
        detail = dacp_broker.assess_peer_challenge(initial, final, "CORRECT")
        self.assertTrue(detail["openai_degraded"])
        self.assertTrue(detail["anthropic_rescued"])
        self.assertTrue(detail["negative_value_observed"])
        self.assertTrue(detail["rescue_observed"])

    def test_peer_challenge_wrong_convergence_flags_mutual_reinforcement_risk(self):
        initial = [self.result("openai", "A"), self.result("anthropic", "B")]
        final = [self.result("openai", "SAME-WRONG"), self.result("anthropic", "SAME-WRONG")]
        detail = dacp_broker.assess_peer_challenge(initial, final, "CORRECT")
        self.assertTrue(detail["mutual_reinforcement_risk_observed"])
        self.assertFalse(detail["rescue_observed"])

    def test_peer_challenge_not_attempted_if_initial_call_unresolved(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = self.args(tmp, peer_challenge=True)
            with patch.object(dacp_broker, "call_openai", return_value=self.result("openai", "TOKEN")) as o, patch.object(
                dacp_broker, "call_anthropic", return_value=self.result("anthropic", None, "PENDING")
            ) as a:
                rc = dacp_broker.run(args)
            self.assertEqual(rc, 2)
            self.assertEqual(o.call_count, 1)
            self.assertEqual(a.call_count, 1)
            events = [json.loads(line) for line in next(Path(tmp).glob("*.jsonl")).read_text(encoding="utf-8").splitlines()]
            self.assertNotIn("peer_challenge_started", [e["event"] for e in events])
            self.assertEqual(events[-1]["terminal_state"], "UNRESOLVED")
            self.assertFalse(events[-1]["verification"]["challenge_attempted"])


if __name__ == "__main__":
    unittest.main()
