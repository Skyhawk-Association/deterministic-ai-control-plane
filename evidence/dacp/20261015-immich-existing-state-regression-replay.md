# DACP D27-D29 adverse-case regression replay

## Change Synopsis

- 2026-10-15: Records earlier failed responses, corrected answer semantics, and the remaining unproven runtime enforcement boundary.
- Applies `authoritative/DACP_Existing_Configuration_And_Endpoint_Evidence_Gate_0.1.md` and `tests/DACP_0.1.7_DELTA_Regression_Matrix.md`; no private device identifiers or screenshot content are included.

**Method:** Scenario-replay evaluation from directly observed conversation actions and the user's correcting UI evidence. Checked each D27-D29 fixture and its corresponding control binding against current canonical text. These are not automated model-run regressions.

| Fixture | Prior failure (observed response class) | Corrected answer to test | Replay assessment |
|---|---|---|---|
| D27 | An already-installed app's *inspect current setting* question was answered with a *proposed server to enter*. | In the existing app open profile > Settings > Networking, read **Current server address**, make no changes. | Prior **FAIL**; corrected response **PASS** |
| D28 | Reachability of a proposed alternative address on Mac was treated as a reason to assert mobile external readiness. | A Mac connectivity check proves only Mac reachability; a phone that displays a local URL and disabled switching has no proven off-LAN auto route. | Prior **FAIL**; corrected response **PASS** |
| D29 | A copy run and server ping were at risk of being conflated with whole-archive integrity, application indexing, and duplicate-safe ingestion. | Report raw copy separately; full integrity, application indexing and duplicate policy remain UNVERIFIED until separately checked. | Unsupported stronger claims **FAIL**; corrected scope **PASS** |

## Adversarial checks

1. **Inspect ≠ Configure:** a concrete user question about an existing setting invalidates initial-setup instructions at the response gate.
2. **Mac ≠ Pixel:** a tunnel endpoint response from one client cannot prove reachability, authentication, or auto-selection on another.
3. **Raw storage ≠ app index:** a completed rsync log cannot prove hash equivalence or Immich ingestion.
4. **Human burden:** use the user's current screen evidence and authorized inspection tools rather than asking them to repeat existing setup.

## Acceptance boundary

- **PASS:** D27-D29 are in the matrix, required rule classes are in the correction, and each corrected answer survives the stated contradiction.
- **NOT VERIFIED:** automated runtime enforcement, repeatable independent model-run regression, target-phone remote connectivity, full archive hash verification, Immich indexing, duplicate-safe bulk upload.
- The normative correction can become active after independent Git read-back; it cannot be advertised as a model-level enforcement fix without separate implementation/regression evidence.
- **Privacy:** no confidential device identifiers, user media, credentials, or phone screenshot are persisted in Git.
