import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_core_live_integration as live
from dacp_authority_provider import PinnedFileAuthorityProvider
from dacp_control_session import DACPControlSession, OperationSpec
from dacp_core_live_runtime import VersionedValueRuntime
from dacp_file_runtime import FileBackedValueRuntime
from dacp_operation_manifest import SCHEMA, load_operation_manifest
from dacp_runtime_contract import bind_core_runtime


class _ProviderShouldNotRun:
    def __init__(self):
        self.called = False

    def __call__(self, prompt):
        self.called = True
        raise AssertionError("provider must not be called when operation authority binding fails")


class LiveIntegrationSessionTests(unittest.TestCase):
    def test_default_operation_manifest_matches_separate_authority(self):
        runtime = VersionedValueRuntime()
        loaded = live._resolve_operation_manifest(None)
        operation = loaded.operation
        authority_path, authority_pin = live._resolve_authority_config(None, None)
        authority = PinnedFileAuthorityProvider(authority_path, authority_pin, runtime.resolve_target_fingerprint)
        self.assertIsInstance(operation, OperationSpec)
        self.assertEqual(loaded.raw["schema"], SCHEMA)
        self.assertEqual(operation.endpoint, runtime.endpoint)
        self.assertEqual(
            operation.action_spec(runtime.resolve_target_fingerprint()).action_fingerprint,
            authority.resolve_authority().action_fingerprint,
        )

    def test_manifest_hash_is_exact_file_hash(self):
        loaded = live._resolve_operation_manifest(None)
        self.assertEqual(loaded.sha256, live._sha256_file(loaded.path))

    def test_default_authority_pin_is_exact_file_hash(self):
        self.assertEqual(live.DEFAULT_AUTHORITY_SHA256, live._sha256_file(live.DEFAULT_AUTHORITY_MANIFEST))

    def test_mismatched_manifest_fails_before_provider_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "operation.json"
            source = json.loads(live.DEFAULT_OPERATION_MANIFEST.read_text(encoding="utf-8"))
            source["args"] = {"value": "UNAUTHORIZED"}
            source["verifier"]["expected_value"] = "UNAUTHORIZED"
            path.write_text(json.dumps(source), encoding="utf-8")
            loaded = load_operation_manifest(path)
            runtime = VersionedValueRuntime()
            authority_path, authority_pin = live._resolve_authority_config(None, None)
            authority = PinnedFileAuthorityProvider(authority_path, authority_pin, runtime.resolve_target_fingerprint)
            provider = _ProviderShouldNotRun()
            session = DACPControlSession(
                loaded.operation,
                bind_core_runtime(runtime, authority, now_epoch=lambda: 1),
                provider,
            )
            with self.assertRaises(RuntimeError):
                session.run()
            self.assertFalse(provider.called)

    def test_runtime_binding_has_separate_authority_and_execution_boundaries(self):
        runtime = VersionedValueRuntime()
        authority_path, authority_pin = live._resolve_authority_config(None, None)
        authority = PinnedFileAuthorityProvider(authority_path, authority_pin, runtime.resolve_target_fingerprint)
        core_runtime = bind_core_runtime(runtime, authority, now_epoch=lambda: 1)
        self.assertIs(core_runtime.execute.__self__, runtime)
        self.assertIs(core_runtime.verify.__self__, runtime)
        self.assertIs(core_runtime.resolve_authority.__self__, authority)
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

    def test_parser_defaults_to_file_runtime_default_operation_and_authority(self):
        args = live._build_parser().parse_args([])
        self.assertEqual(args.runtime, "file")
        self.assertIsNone(args.state_file)
        self.assertIsNone(args.operation_manifest)
        self.assertIsNone(args.authority_manifest)
        self.assertIsNone(args.authority_sha256)

    def test_alternate_authority_requires_path_and_pin_together(self):
        with self.assertRaises(ValueError):
            live._resolve_authority_config("authority.json", None)
        with self.assertRaises(ValueError):
            live._resolve_authority_config(None, "0" * 64)

    def test_memory_runtime_remains_explicit(self):
        args = live._build_parser().parse_args(["--runtime", "memory"])
        self.assertEqual(args.runtime, "memory")
        self.assertIsNone(live._resolve_state_file(args.runtime, None))

    def test_durable_state_hash_changes_once_then_stays_stable_on_idempotent_replay(self):
        from dacp_commitment_core import ActionSpec
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            runtime = FileBackedValueRuntime(path)
            initial_hash = live._sha256_file(path)
            first_action = ActionSpec(runtime.endpoint, "SET_STATE", {"value": "DEPLOYED"}, runtime.resolve_target_fingerprint())
            first = runtime.execute(first_action, runtime.resolve_target_fingerprint())
            after_first_hash = live._sha256_file(path)
            self.assertTrue(first.applied)
            self.assertNotEqual(initial_hash, after_first_hash)

            restarted = FileBackedValueRuntime(path)
            second_action = ActionSpec(restarted.endpoint, "SET_STATE", {"value": "DEPLOYED"}, restarted.resolve_target_fingerprint())
            second = restarted.execute(second_action, restarted.resolve_target_fingerprint())
            after_second_hash = live._sha256_file(path)
            self.assertFalse(second.applied)
            self.assertEqual(after_first_hash, after_second_hash)
            self.assertEqual(restarted.evidence_snapshot()["version"], 1)
            self.assertEqual(len(restarted.evidence_snapshot()["ledger"]), 1)

    def test_live_module_imports_reusable_session(self):
        self.assertIsNotNone(DACPControlSession)


if __name__ == "__main__":
    unittest.main()
