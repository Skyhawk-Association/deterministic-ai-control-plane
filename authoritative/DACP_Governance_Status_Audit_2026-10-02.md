# DACP Governance Status Audit — 2026-10-02

**Status:** AUTHORITATIVE STATUS CORRECTION / ACTIVE UNDER DACP OPERATIONAL USE AND CORRECTION AUTHORITY 0.2  
**Purpose:** Remove ambiguity between active authority, historical candidate language, and genuinely reserved Gene decisions.

## Evidence basis

- Live `main` was resolved before correction.
- `CURRENT.md` governs current public DACP state.
- Heuristics Specification 0.1.4 explicitly records Gene's 2026-09-13 approval and active status.
- Application Implementation Authorization 0.7 explicitly supersedes 0.6.
- Private operational state generation 38 was read from the verified local-sync filesystem. Its pending/candidate section contains no itemized pointers and states that generation 36 carried only a generation number.
- The older shared candidate register contains historical proposed material, but its substance is substantially represented in later active Delta controls and it does not itself create a current approval gate.
- Historical Candidate AI Operating Rule Delta Register 0.12 is dated 2026-09-06, states CANDIDATE / NOT AUTHORITATIVE, and cannot establish a later live Gene approval requirement.

## Classification

### A. Already authorized / active

- DACP Runtime Expression 0.1.7-DELTA.
- Project Instructions 0.7.
- Heuristics Specification 0.1.4.
- Operational Use and Correction Authority 0.2.
- Interim Decision Authority 0.3.
- Application Implementation Authorization 0.7.
- Required Pipe Qualification 0.1.
- Reality-Conformance heuristic and D23 regression.
- Dual ChatGPT / Claude executor authorization, one at a time as Gene chooses.
- Controlled Skyhawk VPS administration authority within Authorization 0.7.

### B. Candidate/proposed material not requiring a new approval loop when it is merely evidence-forced correction within existing authority

Operational Use and Correction Authority 0.2 permits immediate versioned corrections when current evidence directly demonstrates a defect, the accepted objective and authority are preserved, safeguards are not weakened, regression covers the failure, and corrected state is persisted and independently read back.

Historical candidate wording does not create a new approval requirement where the active corpus already implements the same objective or where the change is only a status/pointer correction under that standing authority.

### C. Genuinely awaiting Gene decision

No specific live proposal requiring Gene's decision is established by current canonical Git, private state generation 38, or the surviving historical candidate registers inspected in this audit.

The remembered Claude-originated conversation about programming restrictions / refusal to engage conversationally is not deterministically reconstructible from these persisted sources. Therefore no approval is inferred, denied, or fabricated from recollection.

If a later retrievable artifact identifies that proposal, apply the reserved-decision test in Operational Use and Correction Authority 0.2 section 4. Gene decision is required only if it changes project endpoints, decision governance, permissions/irreversible authority, weakens safety/privacy/legal/evidence requirements, creates a new material control objective, or accepts material unresolved risk.

### D. Stale / superseded status text corrected by this audit

- Heuristics Specification 0.1.3 remains provenance only; its REVIEW-READY / NOT ACTIVE label does not survive 0.1.4's explicit approval and activation.
- `authoritative/README.md` incorrectly listed Heuristics 0.1.4 as superseded and Application Implementation Authorization 0.6 as active. Corrected.
- Project Instructions 0.7 synopsis incorrectly pointed current executor assignment to Authorization 0.6. Corrected to 0.7.
- Historical candidate registers remain non-authoritative provenance and must not be scanned as if every PROPOSED item were a current Gene decision queue.

## Status rule

When status labels conflict, resolve in this order:

1. live `main` / `CURRENT.md`;
2. newest applicable authoritative decision/specification identified by `CURRENT.md`;
3. active private operational state for continuity/evidence only;
4. historical candidate/provenance artifacts.

Lower-precedence historical labels cannot reopen an approval gate closed by later authoritative evidence.

## Regression

D24 in `tests/DACP_0.1.7_DELTA_Regression_Matrix.md` tests this status-precedence failure mode.

This audit changes no project endpoint, permission, irreversible authority, safety/privacy/legal/evidence requirement, or material control objective.
