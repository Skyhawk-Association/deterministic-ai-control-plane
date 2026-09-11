import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_core_live_integration as live
from dacp_control_session import DACPControlSession, OperationSpec
from dacp_core_live_runtime import VersionedValueRuntime
from dacp_file_runtime import FileBackedValueRuntime
from dacp_runtime_contract import bind_core_runtime


class LiveIntegrationSessionTests(unittest.TestCase):
    def test_operation_factory_matches_runtime_authority(self):
        runtime = VersionedValueRuntime()
        operation = live._operation_for_runtime(runtime)
        self.assertIsInstance(operation, OperationSpec)
        self.assertEqual(operation.endpoint, runtime.endpoint)
        self.assertEqual(operation.args, {"value": runtime.authorized_value})
        self.assertEqual(
            operation.action_spec(runtime.resolve_target_fingerprint()).action_fingerprint,
            runtime.resolve_authority().action_fingerprint,
        )

    def test_runtime_binding_has_required_session_boundaries(self):
        runtime = VersionedValueRuntime()
        core_runtime = bind_core_runtime(runtime, now_epoch=lambda: 1)
        self.assertIs(core_runtime.execute.__self__, runtime)
        self.assertIs(core_runtime.verify.__self__, runtime)
        self.assertIs(core_runtime.oracle_verify.__self__, runtime)
        self.assertEqual(core_runtime.resolve_target_fingerprint(), "tracked-value@v0")

    def test_runtime_factory_supports_memory_and_file(self):
        memory = live._make_runtime("memory", None)
        self.assertIsInstance(memory, VersionedValueRuntime)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            durable = live._make_runtime("file", str(path))
            self.assertIsInstance(durable, FileBackedValueRuntime)
            self.assertTrue(path.exists())

    def test_file_runtime_resolves_default_state_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            with patch.dict("os.environ", {}, clear=False):
                with patch("pathlib.Path.home", return_value=home):
                    resolved = live._resolve_state_file("file", None)
            self.assertEqual(resolved, (home / ".dacp" / "runtime" / "tracked-value.json").resolve())

    def test_state_file_environment_override(self):
        with tempfile.TemporaryDirectory() as tmp:
            configured = Path(tmp) / "custom-state.json"
            with patch.dict("os.environ", {live.DEFAULT_STATE_ENV: str(configured)}, clear=False):
                self.assertEqual(live._default_state_file(), configured.resolve())

    def test_parser_defaults_to_file_runtime(self):
        args = live._build_parser().parse_args([])
        self.assertEqual(args.runtime, "file")
        self.assertIsNone(args.state_file)

    def test_memory_runtime_remains_explicit(self):
        args = live._build_parser().parse_args(["--runtime", "memory"])
        self.assertEqual(args.runtime, "memory")
        self.assertIsNone(live._resolve_state_file(args.runtime, None))

    def test_durable_state_hash_changes_once_then_stays_stable_on_idempotent_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            runtime = FileBackedValueRuntime(path)
            initial_hash = live._sha256_file(path)

            first = runtime.execute(runtime.authorized_action, runtime.resolve_target_fingerprint())
            after_first_hash = live._sha256_file(path)
            self.assertTrue(first.applied)
            self.assertNotEqual(initial_hash, after_first_hash)

            restarted = FileBackedValueRuntime(path)
            second = restarted.execute(restarted.authorized_action, restarted.resolve_target_fingerprint())
            after_second_hash = live._sha256_file(path)
            self.assertFalse(second.applied)
            self.assertEqual(after_first_hash, after_second_hash)
            self.assertEqual(restarted.evidence_snapshot()["version"], 1)
            self.assertEqual(len(restarted.evidence_snapshot()["ledger"]), 1)

    def test_live_module_imports_reusable_session(self):
        self.assertIsNotNone(DACPControlSession)


if __name__ == "__main__":
    unittest.main()
