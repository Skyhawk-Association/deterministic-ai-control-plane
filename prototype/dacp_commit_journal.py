from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


SCHEMA = "dacp-commit-journal-0.1"
RESOLVED_PHASES = {"RESOLVED_SUCCEEDED", "RESOLVED_FAILED"}


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _sha256_json(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def request_fingerprint(endpoint: str, tool: str, args: dict[str, Any]) -> str:
    """Stable operation identity that intentionally excludes mutable target version."""
    return _sha256_json({"endpoint": endpoint, "tool": tool, "args": args})


class DurableCommitJournal:
    """Atomic local journal for consequential dispatch uncertainty across restart."""

    def __init__(self, path: str | Path):
        self.path = Path(path).expanduser().resolve()
        if not self.path.exists():
            self._write({"schema": SCHEMA, "sequence": 0, "records": []})
        self._read()

    def _read(self) -> dict[str, Any]:
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if set(data) != {"schema", "sequence", "records"} or data["schema"] != SCHEMA:
            raise RuntimeError("commit journal shape/schema is invalid")
        if not isinstance(data["sequence"], int) or data["sequence"] < 0:
            raise RuntimeError("commit journal sequence is invalid")
        if not isinstance(data["records"], list):
            raise RuntimeError("commit journal records are invalid")
        return data

    def _write(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(data, indent=2, sort_keys=True) + "\n"
        fd, temp_name = tempfile.mkstemp(prefix=self.path.name + ".", suffix=".tmp", dir=str(self.path.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, self.path)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
        if self._read() != data:
            raise RuntimeError("commit journal readback mismatch after atomic replace")

    def evidence_snapshot(self) -> dict[str, Any]:
        data = self._read()
        return {
            "schema": data["schema"],
            "path": str(self.path),
            "sequence": data["sequence"],
            "records": data["records"],
        }

    def unresolved_for(self, operation_id: str) -> dict[str, Any] | None:
        data = self._read()
        for record in reversed(data["records"]):
            if record.get("operation_id") == operation_id and record.get("phase") not in RESOLVED_PHASES:
                return dict(record)
        return None

    def record_dispatch_intent(
        self,
        *,
        operation_id: str,
        endpoint: str,
        tool: str,
        args: dict[str, Any],
        action_fingerprint: str,
        target_fingerprint: str,
        authority_id: str,
    ) -> dict[str, Any]:
        existing = self.unresolved_for(operation_id)
        if existing is not None:
            return existing
        data = self._read()
        next_sequence = data["sequence"] + 1
        stable_request_fingerprint = request_fingerprint(endpoint, tool, args)
        record_id = _sha256_json(
            {
                "operation_id": operation_id,
                "request_fingerprint": stable_request_fingerprint,
                "action_fingerprint": action_fingerprint,
                "target_fingerprint": target_fingerprint,
                "sequence": next_sequence,
            }
        )
        record = {
            "record_id": record_id,
            "operation_id": operation_id,
            "request_fingerprint": stable_request_fingerprint,
            "action_fingerprint": action_fingerprint,
            "target_fingerprint": target_fingerprint,
            "authority_id": authority_id,
            "phase": "DISPATCH_INTENT",
            "history": [{"sequence": next_sequence, "phase": "DISPATCH_INTENT"}],
        }
        data["sequence"] = next_sequence
        data["records"].append(record)
        self._write(data)
        return dict(record)

    def transition(self, record_id: str, phase: str, *, detail: dict[str, Any] | None = None) -> dict[str, Any]:
        data = self._read()
        record = next((r for r in data["records"] if r.get("record_id") == record_id), None)
        if record is None:
            raise RuntimeError("commit journal record not found")
        next_sequence = data["sequence"] + 1
        record["phase"] = phase
        event: dict[str, Any] = {"sequence": next_sequence, "phase": phase}
        if detail is not None:
            event["detail"] = detail
        record.setdefault("history", []).append(event)
        data["sequence"] = next_sequence
        self._write(data)
        return dict(record)
