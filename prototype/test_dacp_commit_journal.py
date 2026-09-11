import tempfile
import unittest
from pathlib import Path

from dacp_commit_journal import DurableCommitJournal, request_fingerprint


class DurableCommitJournalTests(unittest.TestCase):
    def test_unresolved_intent_survives_restart_until_resolved(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "commit-journal.json"
            journal = DurableCommitJournal(path)
            record = journal.record_dispatch_intent(
                operation_id="op-1",
                endpoint="tracked-value",
                tool="SET_STATE",
                args={"value": "DEPLOYED"},
                action_fingerprint="action-v0",
                target_fingerprint="tracked-value@v0",
                authority_id="AUTH-1",
            )
            restarted = DurableCommitJournal(path)
            unresolved = restarted.unresolved_for("op-1")
            self.assertIsNotNone(unresolved)
            self.assertEqual(unresolved["record_id"], record["record_id"])
            restarted.transition(record["record_id"], "RESOLVED_SUCCEEDED")
            self.assertIsNone(DurableCommitJournal(path).unresolved_for("op-1"))

    def test_request_fingerprint_is_stable_across_target_versions(self):
        first = request_fingerprint("tracked-value", "SET_STATE", {"value": "DEPLOYED"})
        second = request_fingerprint("tracked-value", "SET_STATE", {"value": "DEPLOYED"})
        changed = request_fingerprint("tracked-value", "SET_STATE", {"value": "OTHER"})
        self.assertEqual(first, second)
        self.assertNotEqual(first, changed)

    def test_second_intent_does_not_replace_unresolved_prior_intent(self):
        with tempfile.TemporaryDirectory() as tmp:
            journal = DurableCommitJournal(Path(tmp) / "commit-journal.json")
            first = journal.record_dispatch_intent(
                operation_id="op-1",
                endpoint="tracked-value",
                tool="SET_STATE",
                args={"value": "DEPLOYED"},
                action_fingerprint="action-v0",
                target_fingerprint="tracked-value@v0",
                authority_id="AUTH-1",
            )
            second = journal.record_dispatch_intent(
                operation_id="op-1",
                endpoint="tracked-value",
                tool="SET_STATE",
                args={"value": "DEPLOYED"},
                action_fingerprint="action-v1",
                target_fingerprint="tracked-value@v1",
                authority_id="AUTH-1",
            )
            self.assertEqual(first["record_id"], second["record_id"])
            self.assertEqual(len(journal.evidence_snapshot()["records"]), 1)


if __name__ == "__main__":
    unittest.main()
