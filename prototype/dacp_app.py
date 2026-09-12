#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from run_core_live_integration import _default_state_file, _run_resolved

APP_NAME = "DACP"
APP_VERSION = "0.1"
SCHEMA = "dacp-app-api-0.1"
UI_FILE = Path(__file__).with_name("dacp_ui.html")


def _status_payload(state_file: str | None = None) -> dict[str, Any]:
    state_path = Path(state_file).expanduser().resolve() if state_file else _default_state_file()
    return {
        "schema": SCHEMA,
        "app": APP_NAME,
        "version": APP_VERSION,
        "mode": "LOCAL_SINGLE_RESOURCE_RESOLVED_COMMITMENT",
        "provider_dependency": False,
        "state_file": str(state_path),
        "state_exists": state_path.exists(),
    }


def _state_payload(state_file: str | None = None) -> dict[str, Any]:
    state_path = Path(state_file).expanduser().resolve() if state_file else _default_state_file()
    if not state_path.exists():
        return {"exists": False, "value": None, "version": None}
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"exists": True, "value": None, "version": None, "status": "UNREADABLE"}
    return {
        "exists": True,
        "value": data.get("value"),
        "version": data.get("version"),
        "ledger_entries": len(data.get("ledger", [])) if isinstance(data.get("ledger"), list) else None,
    }


def execute_default_operation(state_file: str | None = None, lock_timeout: float = 10.0) -> dict[str, Any]:
    return _run_resolved(
        "file",
        state_file,
        None,
        None,
        None,
        lock_timeout_seconds=lock_timeout,
    )


class DACPRequestHandler(BaseHTTPRequestHandler):
    server_version = "DACP/0.1"

    def _send_bytes(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self._send_bytes(status, body, "application/json; charset=utf-8")

    def do_GET(self) -> None:
        if self.path == "/":
            try:
                body = UI_FILE.read_bytes()
            except OSError:
                self._send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "ui_unavailable"})
                return
            self._send_bytes(HTTPStatus.OK, body, "text/html; charset=utf-8")
            return
        if self.path == "/health":
            self._send_json(HTTPStatus.OK, {"status": "ok", "app": APP_NAME, "version": APP_VERSION})
            return
        if self.path == "/status":
            self._send_json(HTTPStatus.OK, _status_payload(self.server.state_file))
            return
        if self.path == "/state":
            self._send_json(HTTPStatus.OK, _state_payload(self.server.state_file))
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

    def do_POST(self) -> None:
        if self.path != "/operations/tracked-value-deploy":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return
        result = execute_default_operation(self.server.state_file, self.server.lock_timeout)
        status = HTTPStatus.OK if result.get("pass") else HTTPStatus.ACCEPTED if result.get("status") == "PENDING" else HTTPStatus.CONFLICT
        self._send_json(status, result)

    def log_message(self, format: str, *args: Any) -> None:
        return


class DACPHTTPServer(ThreadingHTTPServer):
    def __init__(self, server_address: tuple[str, int], state_file: str | None, lock_timeout: float):
        super().__init__(server_address, DACPRequestHandler)
        self.state_file = state_file
        self.lock_timeout = lock_timeout


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local DACP 0.1 application shell")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--state-file", default=None)
    parser.add_argument("--lock-timeout", type=float, default=10.0)
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    server = DACPHTTPServer((args.host, args.port), args.state_file, args.lock_timeout)
    print(f"DACP 0.1 listening on http://{args.host}:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
