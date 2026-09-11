import json
import tempfile
import unittest
from pathlib import Path

from dacp_authority_provider import HASH_MODE, PinnedFileAuthorityProvider, canonical_authority_sha256
from dacp_commitment_core import ActionSpec


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


def canonical_sha(data):
    return canonical_authority_sha256(data)


class PinnedAuthorityProviderTests(unittest.TestCase):
    def write_manifest(self, path: Path, data, newline="\n"):
        text = json.dumps(data, indent=2, sort_keys=True) + "\n"
        path.write_bytes(text.replace("\n", newline).encode("utf-8"))

    def test_exact_pin_issues_current_target_bound_proof(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "authority.json"
            data = manifest()
            self.write_manifest(path, data)
            target = {"value": "tracked-value@v0"}
            provider = PinnedFileAuthorityProvider(path, canonical_sha(data), lambda: target["value"])

            first = provider.resolve_authority()
            expected = ActionSpec("tracked-value", "SET_STATE", {"value": "DEPLOYED"}, "tracked-value@v0")
            self.assertEqual(first.action_fingerprint, expected.action_fingerprint)
            self.assertEqual(first.target_fingerprint, "tracked-value@v0")
            self.assertFalse(first.trust_root_compromised)
            self.assertEqual(provider.evidence_snapshot()["hash_mode"], HASH_MODE)

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

    def test_crlf_and_lf_preserve_same_authority_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            lf_path = Path(tmp) / "authority-lf.json"
            crlf_path = Path(tmp) / "authority-crlf.json"
            data = manifest()
            pin = canonical_sha(data)
            self.write_manifest(lf_path, data, "\n")
            self.write_manifest(crlf_path, data, "\r\n")

            lf = PinnedFileAuthorityProvider(lf_path, pin, lambda: "tracked-value@v0")
            crlf = PinnedFileAuthorityProvider(crlf_path, pin, lambda: "tracked-value@v0")
            self.assertTrue(lf.evidence_snapshot()["integrity_ok"])
            self.assertTrue(crlf.evidence_snapshot()["integrity_ok"])
            self.assertEqual(lf.evidence_snapshot()["observed_sha256"], pin)
            self.assertEqual(crlf.evidence_snapshot()["observed_sha256"], pin)

    def test_semantic_change_still_quarantines_trust_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "authority.json"
            original = manifest()
            self.write_manifest(path, original)
            pin = canonical_sha(original)
            provider = PinnedFileAuthorityProvider(path, pin, lambda: "tracked-value@v0")

            self.write_manifest(path, manifest(value="PWNED"), "\r\n")
            proof = provider.resolve_authority()
            self.assertTrue(proof.trust_root_compromised)
            expected_original = ActionSpec("tracked-value", "SET_STATE", {"value": "DEPLOYED"}, "tracked-value@v0")
            self.assertEqual(proof.action_fingerprint, expected_original.action_fingerprint)
            self.assertFalse(provider.evidence_snapshot()["integrity_ok"])

    def test_revoked_manifest_issues_revoked_proof(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "authority.json"
            data = manifest(revoked=True)
            self.write_manifest(path, data)
            provider = PinnedFileAuthorityProvider(path, canonical_sha(data), lambda: "tracked-value@v0")
            self.assertTrue(provider.resolve_authority().revoked)


if __name__ == "__main__":
    unittest.main()
