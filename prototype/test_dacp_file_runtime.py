import tempfile
import unittest
from pathlib import Path

from dacp_commitment_core import Outcome, VerifierSpec
from dacp_file_runtime import FileBackedValueRuntime
from dacp_runtime_contract import DACPRuntime, bind_core_runtime


class FileBackedValueRuntimeTests(unittest.TestCase):
    def test_runtime_satisfies_contract_and_survives_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            runtime = FileBackedValueRuntime(path)
            self.assertIsInstance(runtime, DACPRuntime)
            core_runtime = bind_core_runtime(runtime, now_epoch=lambda: 1)
            action = runtime.authorized_action
            receipt = core_runtime.execute(action, runtime.resolve_target_fingerprint())
            self.assertEqual(receipt.outcome, Outcome.SUCCEEDED)
            self.assertTrue(receipt.applied)

            restarted = FileBackedValueRuntime(path)
            observation = restarted.routine_read()
            self.assertEqual(observation["value"], "DEPLOYED")
            self.assertEqual(observation["target_fingerprint"], "tracked-value@v1")

            verifier = VerifierSpec("READ_STATE", {}, "DEPLOYED", "verifier-read-state")
            self.assertEqual(restarted.verify(verifier).outcome, Outcome.SUCCEEDED)
            self.assertEqual(restarted.oracle_verify(verifier).outcome, Outcome.SUCCEEDED)

    def test_repeated_operation_after_restart_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            first_runtime = FileBackedValueRuntime(path)
            first = first_runtime.execute(first_runtime.authorized_action, "tracked-value@v0")
            self.assertTrue(first.applied)

            restarted = FileBackedValueRuntime(path)
            before = restarted._read_state()
            second = restarted.execute(restarted.authorized_action, restarted.resolve_target_fingerprint())
            after = restarted._read_state()

            self.assertEqual(second.outcome, Outcome.SUCCEEDED)
            self.assertFalse(second.applied)
            self.assertTrue(second.response.get("already_satisfied"))
            self.assertEqual(after, before)
            self.assertEqual(len(after["ledger"]), 1)
            self.assertEqual(after["version"], 1)

    def test_stale_precondition_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            runtime = FileBackedValueRuntime(path)
            action = runtime.authorized_action
            first = runtime.execute(action, "tracked-value@v0")
            self.assertTrue(first.applied)
            stale = runtime.execute(action, "tracked-value@v0")
            self.assertFalse(stale.applied)
            self.assertTrue(stale.precondition_failed)
            self.assertEqual(runtime.routine_read()["value"], "DEPLOYED")
            self.assertEqual(runtime.routine_read()["target_fingerprint"], "tracked-value@v1")

    def test_ledger_tamper_becomes_pending_oracle(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            runtime = FileBackedValueRuntime(path)
            runtime.execute(runtime.authorized_action, "tracked-value@v0")
            state = runtime._read_state()
            state["ledger"][0]["version"] = 99
            runtime._write_state(state)

            verifier = VerifierSpec("READ_STATE", {}, "DEPLOYED", "verifier-read-state")
            receipt = runtime.oracle_verify(verifier)
            self.assertEqual(receipt.outcome, Outcome.PENDING)
            self.assertFalse(receipt.terminal)


if __name__ == "__main__":
    unittest.main()
