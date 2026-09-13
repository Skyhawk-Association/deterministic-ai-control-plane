from __future__ import annotations

import os
import signal
import socket
import sys
import time
import unittest

from start_dacp import _probe, ensure_running


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class StartDACPTests(unittest.TestCase):
    def test_launcher_starts_then_reuses_same_instance(self) -> None:
        port = _free_port()
        pid = None
        try:
            state, pid = ensure_running("127.0.0.1", port)
            self.assertEqual(state, "STARTED")
            self.assertIsNotNone(pid)
            self.assertEqual(_probe("127.0.0.1", port)["status"], "ok")
            state2, pid2 = ensure_running("127.0.0.1", port)
            self.assertEqual(state2, "ALREADY_RUNNING")
            self.assertIsNone(pid2)
        finally:
            if pid:
                if sys.platform == "win32":
                    os.kill(pid, signal.SIGTERM)
                else:
                    os.kill(pid, signal.SIGTERM)
                time.sleep(0.2)
