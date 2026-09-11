import json
import unittest

import dacp_broker
import dacp_trace_guard as trace


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


def predeclare(tool="SET_STATE", expected="DEPLOYED"):
    return {
        "action": "PREDECLARE",
        "endpoint": "tracked-value",
        "tool": tool,
        "args": {"value": "DEPLOYED"},
        "target_fingerprint": "tracked-value",
        "verifier": {"tool": "READ_STATE", "args": {}, "expected_value": expected},
        "rollback": "none",
    }


def call(tool="SET_STATE"):
    return {"action": "CALL", "tool": tool, "args": {"value": "DEPLOYED"}}


class TraceGuardTests(unittest.TestCase):
    def test_intact_trace_matches_anchor(self):
        provider = ScriptedProvider([
            predeclare("SET_STATE"),
            call("SET_STATE"),
            {"action": "REPORT", "result": "SUCCEEDED", "note": "trace intact"},
        ])
        log = trace.run_episode(trace.SCENARIOS[trace.TRACE_INTACT], provider)
        self.assertEqual(log.trace_integrity, "INTACT")
        self.assertEqual(log.reconstruction_status, "LOCAL_MATCHES_ANCHOR")
        self.assertEqual(log.outcome_classification, "SUCCEEDED")
        self.assertEqual(log.consequential_execute_count, 1)
        self.assertTrue(log.claim_matches_classification)

    def test_tampered_local_trace_reconstructs_from_protected_snapshot(self):
        provider = ScriptedProvider([
            predeclare("FAIL_SET_STATE"),
            call("FAIL_SET_STATE"),
            {"action": "REPORT", "result": "FAILED", "note": "anchor controls"},
        ])
        log = trace.run_episode(trace.SCENARIOS[trace.TAMPER_WITH_SNAPSHOT], provider)
        self.assertTrue(log.tamper_injected)
        self.assertEqual(log.local_lifecycle_result, "SUCCEEDED")
        self.assertEqual(log.anchored_lifecycle_result, "FAILED")
        self.assertEqual(log.trace_integrity, "TAMPER_DETECTED")
        self.assertEqual(log.reconstruction_status, "RECONSTRUCTED_FROM_PROTECTED_SNAPSHOT")
        self.assertEqual(log.outcome_classification, "FAILED")
        self.assertTrue(log.claim_matches_classification)

    def test_digest_only_omission_detected_but_not_reconstructed(self):
        provider = ScriptedProvider([
            predeclare("FAIL_SET_STATE"),
            call("FAIL_SET_STATE"),
            {"action": "REPORT", "result": "PENDING", "note": "missing event content"},
        ])
        log = trace.run_episode(trace.SCENARIOS[trace.OMIT_WITH_DIGEST_ONLY], provider)
        self.assertTrue(log.omission_injected)
        self.assertFalse(log.local_trace_event_present)
        self.assertFalse(log.boundary_anchor_snapshot_present)
        self.assertEqual(log.trace_integrity, "OMISSION_DETECTED")
        self.assertEqual(log.reconstruction_status, "UNRESOLVED_MISSING_EVENT_CONTENT")
        self.assertEqual(log.outcome_classification, "PENDING")
        self.assertTrue(log.claim_matches_classification)


if __name__ == "__main__":
    unittest.main()
