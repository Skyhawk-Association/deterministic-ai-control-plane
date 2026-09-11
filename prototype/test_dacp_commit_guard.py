import json
import unittest

import dacp_broker
import dacp_commit_guard as guard


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
            return fake_result({"action": "REPORT", "result": "FAILED", "note": "out"})
        return fake_result(self.actions.pop(0))


def predeclare(fp):
    return {
        "action": "PREDECLARE",
        "endpoint": "set tracked value",
        "tool": "SET_STATE",
        "args": {"value": "DEPLOYED"},
        "target_fingerprint": fp,
        "verifier": {"tool": "READ_STATE", "args": {}, "expected_value": "DEPLOYED"},
        "rollback": "restore only after fresh authorization",
    }


CALL_SET = {"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}}
READ = {"action": "CALL", "tool": "READ_STATE", "args": {}}


class CommitGuardTests(unittest.TestCase):
    def test_stable_target_commits_once(self):
        provider = ScriptedProvider([
            predeclare("tracked-value@v0"), CALL_SET, READ,
            {"action": "REPORT", "result": "SUCCEEDED", "note": "verified"},
        ])
        log = guard.run_episode(guard.SCENARIOS[guard.STABLE_CONTROL], provider)
        self.assertEqual(log.consequential_execute_count, 1)
        self.assertEqual(log.commit_revalidation_block_count, 0)
        self.assertEqual(log.atomic_precondition_block_count, 0)
        self.assertEqual(log.final_value, "DEPLOYED")

    def test_stale_binding_blocks_before_execution_then_recovers(self):
        provider = ScriptedProvider([
            predeclare("tracked-value@v0"), CALL_SET,
            predeclare("tracked-value@v1"), CALL_SET, READ,
            {"action": "REPORT", "result": "SUCCEEDED", "note": "fresh binding verified"},
        ])
        log = guard.run_episode(guard.SCENARIOS[guard.STALE_PREDECLARE], provider)
        self.assertTrue(log.external_mutation_injected)
        self.assertEqual(log.commit_revalidation_block_count, 1)
        self.assertEqual(log.atomic_precondition_block_count, 0)
        self.assertEqual(log.fresh_binding_recovery_count, 1)
        self.assertEqual(log.consequential_execute_count, 1)
        self.assertEqual(log.final_value, "DEPLOYED")

    def test_atomic_race_fails_precondition_then_recovers(self):
        provider = ScriptedProvider([
            predeclare("tracked-value@v0"), CALL_SET,
            predeclare("tracked-value@v1"), CALL_SET, READ,
            {"action": "REPORT", "result": "SUCCEEDED", "note": "retry with fresh CAS"},
        ])
        log = guard.run_episode(guard.SCENARIOS[guard.ATOMIC_RACE], provider)
        self.assertTrue(log.atomic_race_injected)
        self.assertEqual(log.commit_revalidation_block_count, 0)
        self.assertEqual(log.atomic_precondition_block_count, 1)
        self.assertEqual(log.fresh_binding_recovery_count, 1)
        self.assertEqual(log.consequential_execute_count, 1)
        self.assertEqual(log.final_value, "DEPLOYED")


if __name__ == "__main__":
    unittest.main()
