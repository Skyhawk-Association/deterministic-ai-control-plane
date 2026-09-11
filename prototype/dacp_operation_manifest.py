from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dacp_control_session import OperationSpec


SCHEMA = "dacp-operation-manifest-0.1"
_REQUIRED_KEYS = {
    "schema",
    "operation_id",
    "task",
    "endpoint",
    "tool",
    "args",
    "verifier",
    "rollback_or_reconciliation_plan",
    "expected_acceptance",
}
_VERIFIER_KEYS = {"tool", "args", "expected_value"}


@dataclass(frozen=True)
class LoadedOperation:
    path: Path
    sha256: str
    operation: OperationSpec
    raw: dict[str, Any]


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _require_nonblank_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a nonblank string")
    return value


def _validate_manifest(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("operation manifest must be a JSON object")
    if set(data) != _REQUIRED_KEYS:
        missing = sorted(_REQUIRED_KEYS - set(data))
        extra = sorted(set(data) - _REQUIRED_KEYS)
        raise ValueError(f"operation manifest fields mismatch; missing={missing} extra={extra}")
    if data.get("schema") != SCHEMA:
        raise ValueError(f"unsupported operation manifest schema: {data.get('schema')!r}")

    _require_nonblank_string(data["operation_id"], "operation_id")
    _require_nonblank_string(data["task"], "task")
    _require_nonblank_string(data["endpoint"], "endpoint")
    _require_nonblank_string(data["tool"], "tool")
    _require_nonblank_string(data["rollback_or_reconciliation_plan"], "rollback_or_reconciliation_plan")
    _require_nonblank_string(data["expected_acceptance"], "expected_acceptance")

    if not isinstance(data["args"], dict):
        raise ValueError("args must be a JSON object")
    verifier = data["verifier"]
    if not isinstance(verifier, dict) or set(verifier) != _VERIFIER_KEYS:
        raise ValueError("verifier must contain exactly tool, args, expected_value")
    _require_nonblank_string(verifier["tool"], "verifier.tool")
    if not isinstance(verifier["args"], dict):
        raise ValueError("verifier.args must be a JSON object")
    return data


def load_operation_manifest(path: str | Path) -> LoadedOperation:
    resolved = Path(path).expanduser().resolve()
    payload = resolved.read_bytes()
    try:
        data = json.loads(payload.decode("utf-8"))
    except UnicodeDecodeError as exc:
        raise ValueError("operation manifest must be UTF-8") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid operation manifest JSON: {exc}") from exc

    data = _validate_manifest(data)
    verifier = data["verifier"]
    operation = OperationSpec(
        operation_id=data["operation_id"],
        task=data["task"],
        endpoint=data["endpoint"],
        tool=data["tool"],
        args=dict(data["args"]),
        verifier_tool=verifier["tool"],
        verifier_args=dict(verifier["args"]),
        expected_value=verifier["expected_value"],
        rollback_or_reconciliation_plan=data["rollback_or_reconciliation_plan"],
        expected_acceptance=data["expected_acceptance"],
    )
    return LoadedOperation(path=resolved, sha256=_sha256_bytes(payload), operation=operation, raw=data)
