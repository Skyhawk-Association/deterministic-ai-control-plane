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
            args = argparse.Namespace(
                prompt="secret synthetic prompt",
                prompt_file=None,
                expect_exact=None,
                openai_model="o",
                anthropic_model="a",
                max_output_tokens=10,
                timeout=5,
                log_dir=tmp,
                dry_run=True,
            )
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
            args = argparse.Namespace(
                prompt="TOKEN",
                prompt_file=None,
                expect_exact="TOKEN",
                openai_model="o",
                anthropic_model="a",
                max_output_tokens=10,
                timeout=5,
                log_dir=tmp,
                dry_run=False,
            )
            with patch.object(dacp_broker, "call_openai", return_value=self.result("openai", "TOKEN")) as o, patch.object(
                dacp_broker, "call_anthropic", return_value=self.result("anthropic", "TOKEN")
            ) as a:
                rc = dacp_broker.run(args)
            self.assertEqual(rc, 0)
            o.assert_called_once_with("TOKEN", "o", 10, 5)
            a.assert_called_once_with("TOKEN", "a", 10, 5)
            events = [json.loads(line) for line in next(Path(tmp).glob("*.jsonl")).read_text(encoding="utf-8").splitlines()]
            self.assertEqual([e["event"] for e in events], ["run_started", "provider_result", "provider_result", "run_completed"])
            self.assertEqual(events[-1]["terminal_state"], "VERIFIED_MATCH")


if __name__ == "__main__":
    unittest.main()
