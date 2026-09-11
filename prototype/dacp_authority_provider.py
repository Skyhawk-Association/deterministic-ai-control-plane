from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Protocol, runtime_checkable

from dacp_commitment_core import ActionSpec, AuthorityProof


SCHEMA = "dacp-authority-manifest-0.1"
TARGET_BINDING = "RESOLVE_CURRENT_AT_USE"
HASH_MODE = "CANONICAL_JSON_SHA256"
_REQUIRED_KEYS = {
    "schema",
    "authority_id",
    "trust_root_id",
    "scope",
    "target_binding",
    "valid_through_epoch",
    "revoked",
}
_SCOPE_KEYS = {"endpoint", "tool", "args"}
TargetResolver = Callable[[], str]


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def canonical_authority_sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key in authority manifest: {key}")
        result[key] = value
    return result


def _decode_manifest(payload: bytes) -> dict[str, Any]:
    try:
        data = json.loads(payload.decode("utf-8"), object_pairs_hook=_reject_duplicate_keys)
    except UnicodeDecodeError as exc:
        raise ValueError("authority manifest must be UTF-8") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid authority manifest JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("authority manifest must be a JSON object")
    return data


def _require_nonblank_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a nonblank string")
    return value


@dataclass(frozen=True)
class AuthorityGrant:
    authority_id: str
    trust_root_id: str
    endpoint: str
    tool: str
    args: dict[str, Any]
    valid_through_epoch: int | None
    revoked: bool
    target_binding: str = TARGET_BINDING

    def action_for_target(self, target_fingerprint: str) -> ActionSpec:
        return ActionSpec(
            endpoint=self.endpoint,
            tool=self.tool,
            args=dict(self.args),
            target_fingerprint=target_fingerprint,
        )


@runtime_checkable
class AuthorityProvider(Protocol):
    def resolve_authority(self) -> AuthorityProof:
        ...

    def evidence_snapshot(self) -> dict[str, Any]:
        ...


class StaticAuthorityProvider:
    """Separate authority source for deterministic tests and bounded fixtures."""

    def __init__(self, grant: AuthorityGrant, target_resolver: TargetResolver):
        self.grant = grant
        self.target_resolver = target_resolver
        self.revoked = grant.revoked
        self.trust_root_compromised = False

    def resolve_authority(self) -> AuthorityProof:
        target = self.target_resolver()
        action = self.grant.action_for_target(target)
        return AuthorityProof(
            authority_id=self.grant.authority_id,
            action_fingerprint=action.action_fingerprint,
            target_fingerprint=target,
            trust_root_id=self.grant.trust_root_id,
            valid_through_epoch=self.grant.valid_through_epoch,
            revoked=self.revoked,
            trust_root_compromised=self.trust_root_compromised,
        )

    def evidence_snapshot(self) -> dict[str, Any]:
        return {
            "authority_kind": "static",
            "schema": SCHEMA,
            "authority_id": self.grant.authority_id,
            "trust_root_id": self.grant.trust_root_id,
            "target_binding": self.grant.target_binding,
            "revoked": self.revoked,
            "trust_root_compromised": self.trust_root_compromised,
        }


class PinnedFileAuthorityProvider:
    """Authority source authenticated by a canonical-JSON SHA-256 pin.

    The pin covers parsed authority semantics rather than platform-specific file bytes,
    so CRLF/LF conversion, insignificant whitespace, and object key order do not alter
    trust identity. Duplicate keys are rejected. Any semantic change, malformed content,
    missing file, or unreadable file causes integrity failure. The trusted grant is
    cached after initialization so later tampering cannot become new authority.
    """

    def __init__(self, path: str | Path, expected_sha256: str, target_resolver: TargetResolver):
        self.path = Path(path).expanduser().resolve()
        self.expected_sha256 = expected_sha256.strip().lower()
        if len(self.expected_sha256) != 64 or any(c not in "0123456789abcdef" for c in self.expected_sha256):
            raise ValueError("authority SHA-256 pin must be 64 hex characters")
        self.target_resolver = target_resolver

        payload = self.path.read_bytes()
        data = _decode_manifest(payload)
        grant = self._parse_grant(data)
        observed = canonical_authority_sha256(data)
        if observed != self.expected_sha256:
            raise ValueError("authority manifest canonical SHA-256 pin mismatch at initialization")
        self._grant = grant
        self._trusted_sha256 = observed

    @staticmethod
    def _parse_grant(data: dict[str, Any]) -> AuthorityGrant:
        if set(data) != _REQUIRED_KEYS:
            missing = sorted(_REQUIRED_KEYS - set(data))
            extra = sorted(set(data) - _REQUIRED_KEYS)
            raise ValueError(f"authority manifest fields mismatch; missing={missing} extra={extra}")
        if data.get("schema") != SCHEMA:
            raise ValueError(f"unsupported authority manifest schema: {data.get('schema')!r}")
        if data.get("target_binding") != TARGET_BINDING:
            raise ValueError(f"unsupported target binding: {data.get('target_binding')!r}")

        authority_id = _require_nonblank_string(data["authority_id"], "authority_id")
        trust_root_id = _require_nonblank_string(data["trust_root_id"], "trust_root_id")
        scope = data["scope"]
        if not isinstance(scope, dict) or set(scope) != _SCOPE_KEYS:
            raise ValueError("scope must contain exactly endpoint, tool, args")
        endpoint = _require_nonblank_string(scope["endpoint"], "scope.endpoint")
        tool = _require_nonblank_string(scope["tool"], "scope.tool")
        if not isinstance(scope["args"], dict):
            raise ValueError("scope.args must be a JSON object")
        valid_through = data["valid_through_epoch"]
        if valid_through is not None and (not isinstance(valid_through, int) or valid_through < 0):
            raise ValueError("valid_through_epoch must be a nonnegative integer or null")
        if not isinstance(data["revoked"], bool):
            raise ValueError("revoked must be boolean")

        return AuthorityGrant(
            authority_id=authority_id,
            trust_root_id=trust_root_id,
            endpoint=endpoint,
            tool=tool,
            args=dict(scope["args"]),
            valid_through_epoch=valid_through,
            revoked=data["revoked"],
        )

    def _observed_sha256(self) -> str | None:
        try:
            data = _decode_manifest(self.path.read_bytes())
            self._parse_grant(data)
            return canonical_authority_sha256(data)
        except (OSError, ValueError):
            return None

    def resolve_authority(self) -> AuthorityProof:
        observed = self._observed_sha256()
        compromised = observed != self.expected_sha256
        target = self.target_resolver()
        action = self._grant.action_for_target(target)
        return AuthorityProof(
            authority_id=self._grant.authority_id,
            action_fingerprint=action.action_fingerprint,
            target_fingerprint=target,
            trust_root_id=self._grant.trust_root_id,
            valid_through_epoch=self._grant.valid_through_epoch,
            revoked=self._grant.revoked,
            trust_root_compromised=compromised,
        )

    def evidence_snapshot(self) -> dict[str, Any]:
        observed = self._observed_sha256()
        return {
            "authority_kind": "pinned_file",
            "schema": SCHEMA,
            "hash_mode": HASH_MODE,
            "path": str(self.path),
            "expected_sha256": self.expected_sha256,
            "observed_sha256": observed,
            "integrity_ok": observed == self.expected_sha256,
            "authority_id": self._grant.authority_id,
            "trust_root_id": self._grant.trust_root_id,
            "target_binding": self._grant.target_binding,
            "revoked": self._grant.revoked,
        }
