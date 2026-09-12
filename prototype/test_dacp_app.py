from __future__ import annotations

import json
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from dacp_app import APP_NAME, APP_VERSION, DACPHTTPServer


class DACPAppTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.state_file = str(Path(self.tempdir.name) / "state.json")
        self.server = DACPHTTPServer(("127.0.0.1", 0), self.state_file, 1.0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)
        self.tempdir.cleanup()

    def _json(self, path: str, method: str = "GET") -> tuple[int, dict]:
        request = Request(self.base + path, method=method)
        try:
            with urlopen(request, timeout=5) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            return exc.code, json.loads(exc.read().decode("utf-8"))

    def test_health_and_status(self) -> None:
        status, health = self._json("/health")
        self.assertEqual(status, 200)
        self.assertEqual(health, {"app": APP_NAME, "status": "ok", "version": APP_VERSION})
        status, app_status = self._json("/status")
        self.assertEqual(status, 200)
        self.assertEqual(app_status["app"], APP_NAME)
        self.assertFalse(app_status["state_exists"])

    def test_authorized_operation_mutates_once_then_replays_without_dispatch(self) -> None:
        status, first = self._json("/operations/tracked-value-deploy", method="POST")
        self.assertEqual(status, 200)
        self.assertTrue(first["pass"])
        self.assertEqual(first["dispatch_count"], 1)
        self.assertEqual(first["applied_count"], 1)
        status, second = self._json("/operations/tracked-value-deploy", method="POST")
        self.assertEqual(status, 200)
        self.assertTrue(second["pass"])
        self.assertEqual(second["dispatch_count"], 0)
        self.assertEqual(second["applied_count"], 0)
        self.assertEqual(second["execution_branch"], "PREEXISTING_VERIFIED_NO_DISPATCH")

    def test_unknown_route_is_404(self) -> None:
        status, payload = self._json("/nope")
        self.assertEqual(status, 404)
        self.assertEqual(payload["error"], "not_found")


if __name__ == "__main__":
    unittest.main()
