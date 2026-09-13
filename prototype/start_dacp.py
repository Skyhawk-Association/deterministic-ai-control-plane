#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8876
STARTUP_TIMEOUT = 8.0


def _url(host: str, port: int, path: str = "/") -> str:
    return f"http://{host}:{port}{path}"


def _probe(host: str, port: int) -> dict | None:
    try:
        with urlopen(_url(host, port, "/health"), timeout=1.0) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, URLError, ValueError):
        return None
    if payload.get("app") != "DACP" or payload.get("version") != "0.1" or payload.get("status") != "ok":
        return None
    return payload


def _port_in_use(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0


def _spawn(host: str, port: int) -> subprocess.Popen:
    app = Path(__file__).with_name("dacp_app.py")
    creationflags = 0
    kwargs: dict = {}
    if sys.platform == "win32":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
        kwargs["creationflags"] = creationflags
    else:
        kwargs["start_new_session"] = True
    return subprocess.Popen(
        [sys.executable, str(app), "--host", host, "--port", str(port)],
        cwd=str(app.parent),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        **kwargs,
    )


def ensure_running(host: str, port: int) -> tuple[str, int | None]:
    if _probe(host, port):
        return "ALREADY_RUNNING", None
    if _port_in_use(host, port):
        raise RuntimeError(f"port {port} is occupied by a non-DACP service; refusing to replace it")
    proc = _spawn(host, port)
    deadline = time.monotonic() + STARTUP_TIMEOUT
    while time.monotonic() < deadline:
        if _probe(host, port):
            return "STARTED", proc.pid
        if proc.poll() is not None:
            raise RuntimeError(f"DACP exited during startup with code {proc.returncode}")
        time.sleep(0.15)
    raise RuntimeError("DACP did not become healthy before the startup timeout")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Start or reuse the local DACP 0.1 control room")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--no-browser", action="store_true")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        state, pid = ensure_running(args.host, args.port)
    except RuntimeError as exc:
        print(f"DACP_START_FAILED: {exc}", file=sys.stderr)
        return 2
    target = _url(args.host, args.port)
    if not args.no_browser:
        webbrowser.open(target)
    print(json.dumps({"status": state, "pid": pid, "url": target}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
