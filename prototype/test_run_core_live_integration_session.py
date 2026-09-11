import unittest

import run_core_live_integration as live
from dacp_control_session import DACPControlSession, OperationSpec
from dacp_core_live_runtime import VersionedValueRuntime


class LiveIntegrationSessionTests(unittest.TestCase):
    def test_operation_factory_matches_runtime_authority(self):
        runtime = VersionedValueRuntime()
        operation = live._operation_for_runtime(runtime)
        self.assertIsInstance(operation, OperationSpec)
        self.assertEqual(operation.endpoint, runtime.endpoint)
        self.assertEqual(operation.args, {"value": runtime.authorized_value})
        self.assertEqual(
            operation.action_spec(runtime.target_fingerprint).action_fingerprint,
            runtime.resolve_authority().action_fingerprint,
        )

    def test_core_runtime_has_required_session_boundaries(self):
        runtime = VersionedValueRuntime()
        core_runtime = live._core_runtime(runtime)
        self.assertIs(core_runtime.execute.__self__, runtime)
        self.assertIs(core_runtime.verify.__self__, runtime)
        self.assertIs(core_runtime.oracle_verify.__self__, runtime)
        self.assertEqual(core_runtime.resolve_target_fingerprint(), "tracked-value@v0")

    def test_live_module_imports_reusable_session(self):
        self.assertIsNotNone(DACPControlSession)


if __name__ == "__main__":
    unittest.main()
