import json
import unittest

import dacp_authority_revocation_guard as revocation
import dacp_broker


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
        "endpoint": "tracked-value",
        "tool": "SET_STATE",
        "args": {"value": "DEPLOYED"},
        "target_fingerprint": "tracked-value@v0",
        "verifier": {"tool": "READ_STATE", "args": {}, "expected_value": "DEPLOYED"},
        "rollback": "restore previous state only if separately authorized",
    }


CALL_SET = {"action": "CALL", "tool": "SET_STATE", "args": {"value": "DEPLOYED"}}


class AuthorityRevocationGuardTests(unittest.TestCase):
    def test_valid_authority_survives_commit_revalidation(self):
        provider = ScriptedProvider([
            predeclare(),
            CALL_SET,
            {"action": "REPORT", "result": "SUCCEEDED", "note": "authorized and applied"},
        ])
        log = revocation.run_episode(revocation.SCENARIOS[revocation.VALID_CONTROL], provider)
        self.assertTrue(log.authority_initially_valid)
        self.assertEqual(log.commit_authority_revalidation_count, 1)
        self.assertEqual(log.authority_block_count, 0)
        self.assertEqual(log.consequential_execute_count, 1)
        self.assertEqual(log.final_value, "DEPLOYED")
        self.assertTrue(log.claim_matches_classification)

    def test_revocation_after_predeclare_blocks_commit(self):
        provider = ScriptedProvider([
            predeclare(),
            CALL_SET,
            {"action": "REPORT", "result": "PENDING", "note": "fresh authority required"},
        ])
        log = revocation.run_episode(revocation.SCENARIOS[revocation.REVOKED_AFTER_PREDECLARE], provider)
        self.assertTrue(log.authority_initially_valid)
        self.assertTrue(log.revocation_injected)
        self.assertEqual(log.commit_authority_revalidation_count, 1)
        self.assertEqual(log.authority_block_count, 1)
        self.assertEqual(log.authority_failure_reason, "APPROVAL_REVOKED")
        self.assertEqual(log.consequential_attempt_count, 1)
        self.assertEqual(log.consequential_execute_count, 0)
        self.assertEqual(log.final_value, "INITIAL")
        self.assertTrue(log.claim_matches_classification)

    def test_trust_root_compromise_after_predeclare_blocks_commit(self):
        provider = ScriptedProvider([
            predeclare(),
            CALL_SET,
            {"action": "REPORT", "result": "PENDING", "note": "reauthentication required"},
        ])
        log = revocation.run_episode(revocation.SCENARIOS[revocation.TRUST_ROOT_COMPROMISED], provider)
        self.assertTrue(log.authority_initially_valid)
        self.assertTrue(log.trust_root_compromise_injected)
        self.assertEqual(log.commit_authority_revalidation_count, 1)
        self.assertEqual(log.authority_block_count, 1)
        self.assertEqual(log.authority_failure_reason, "TRUST_ROOT_COMPROMISED")
        self.assertEqual(log.consequential_attempt_count, 1)
        self.assertEqual(log.consequential_execute_count, 0)
        self.assertEqual(log.final_value, "INITIAL")
        self.assertTrue(log.claim_matches_classification)


if __name__ == "__main__":
    unittest.main()
