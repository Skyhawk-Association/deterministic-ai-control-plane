import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from dacp_authority_provider import PinnedFileAuthorityProvider
from dacp_commitment_core import ActionSpec


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest(value="DEPLOYED", revoked=False):
    return {
        "schema": "dacp-authority-manifest-0.1",
        "authority_id": "AUTH-TEST-001",
        "trust_root_id": "test-pinned-root",
        "scope": {
            "endpoint": "tracked-value",
            "tool": "SET_STATE",
            "args": {"value": value},
        },
        "target_binding": "RESOLVE_CURRENT_AT_USE",
        "valid_through_epoch": 4102444800,
        "revoked": revoked,
    }


class PinnedAuthorityProviderTests(unittest.TestCase):
    def write_manifest(self, path: Path, data):
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def test_exact_pin_issues_current_target_bound_proof(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "authority.json"
            self.write_manifest(path, manifest())
            target = {"value": "tracked-value@v0"}
            provider = PinnedFileAuthorityProvider(path, sha256(path), lambda: target["value"])

            first = provider.resolve_authority()
            expected = ActionSpec("tracked-value", "SET_STATE", {"value": "DEPLOYED"}, "tracked-value@v0")
            self.assertEqual(first.action_fingerprint, expected.action_fingerprint)
            self.assertEqual(first.target_fingerprint, "tracked-value@v0")
            self.assertFalse(first.trust_root_compromised)

            target["value"] = "tracked-value@v1"
            second = provider.resolve_authority()
            expected_v1 = ActionSpec("tracked-value", "SET_STATE", {"value": "DEPLOYED"}, "tracked-value@v1")
            self.assertEqual(second.action_fingerprint, expected_v1.action_fingerprint)
            self.assertEqual(second.target_fingerprint, "tracked-value@v1")

    def test_wrong_initial_pin_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "authority.json"
            self.write_manifest(path, manifest())
            with self.assertRaisesRegex(ValueError, "pin mismatch"):
                PinnedFileAuthorityProvider(path, "0" * 64, lambda: "tracked-value@v0")

    def test_post_initialization_tamper_quarantines_trust_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "authority.json"
            self.write_manifest(path, manifest())
            pin = sha256(path)
            provider = PinnedFileAuthorityProvider(path, pin, lambda: "tracked-value@v0")

            self.write_manifest(path, manifest(value="PWNED"))
            proof = provider.resolve_authority()
            self.assertTrue(proof.trust_root_compromised)
            self.assertEqual(proof.trust_root_id, "test-pinned-root")
            expected_original = ActionSpec("tracked-value", "SET_STATE", {"value": "DEPLOYED"}, "tracked-value@v0")
            self.assertEqual(proof.action_fingerprint, expected_original.action_fingerprint)
            self.assertFalse(provider.evidence_snapshot()["integrity_ok"])

    def test_revoked_manifest_issues_revoked_proof(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "authority.json"
            self.write_manifest(path, manifest(revoked=True))
            provider = PinnedFileAuthorityProvider(path, sha256(path), lambda: "tracked-value@v0")
            self.assertTrue(provider.resolve_authority().revoked)


if __name__ == "__main__":
    unittest.main()
