import tempfile
import unittest
from pathlib import Path

from dacp_file_lock import InterProcessFileLock, LockTimeoutError


class InterProcessFileLockTests(unittest.TestCase):
    def test_second_lock_times_out_while_first_is_held(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "resource.lock"
            with InterProcessFileLock(path, timeout_seconds=0.5):
                with self.assertRaises(LockTimeoutError):
                    with InterProcessFileLock(path, timeout_seconds=0.05, poll_seconds=0.01):
                        pass

    def test_lock_releases_for_subsequent_holder(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "resource.lock"
            with InterProcessFileLock(path, timeout_seconds=0.5):
                pass
            with InterProcessFileLock(path, timeout_seconds=0.5):
                self.assertTrue(path.exists())

    def test_invalid_timing_configuration_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "resource.lock"
            with self.assertRaises(ValueError):
                InterProcessFileLock(path, timeout_seconds=-1)
            with self.assertRaises(ValueError):
                InterProcessFileLock(path, poll_seconds=0)


if __name__ == "__main__":
    unittest.main()
