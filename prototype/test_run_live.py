import unittest

import run_core_live_integration
import run_live


class RunLiveSmokeTests(unittest.TestCase):
    def test_run_live_delegates_to_consolidated_core_entrypoint(self):
        self.assertIs(run_live.main, run_core_live_integration.main)


if __name__ == "__main__":
    unittest.main()
