# DACP Operational State Sync 0.1

**Status:** AUTHORITATIVE PROJECT DECISION / ACTIVE / GENE INTERIM DECISION  
**Effective:** Immediately when persisted to canonical `main` and independently read back.  
**Purpose:** Make current DACP control state, unresolved learning, and material observational evidence discoverable across execution surfaces without bloated handoffs or silent promotion.

## 1. Three-layer state model

DACP operational knowledge is separated into three layers:

1. **CANONICAL** — governing current DACP authority and accepted control state. Canonical Git governs.
2. **PENDING / CANDIDATE** — reusable unresolved learning that may affect future work but is not governing authority. Candidates remain non-authoritative until promoted through applicable DACP authority and verification.
3. **RAW / OBSERVATIONAL** — material events, artifacts, field failures, provider/tool observations, uploads, exports, contradictions, corrections, and other evidence available for later synthesis. Observation does not itself create a rule.

The layers must remain distinguishable. No system may silently promote RAW -> PENDING or PENDING -> CANONICAL.

## 2. Bootstrap and state sync

For nontrivial or consequential DACP work:

1. Resolve canonical Git through `CURRENT.md` / `CURRENT.json`.
2. Load the germane authoritative files identified by the bootstrap.
3. Resolve `STATE_LOCATOR.json`.
4. Resolve the current private operational state head when the execution surface has authorized access.
5. If the state generation is newer than the state already incorporated into the task, ingest only the relevant unseen delta before consequential reliance or commitment.

If the private state head is unavailable, identify the evidence gap. Do not substitute remembered state or expand permissions merely to obtain it.

## 3. Git stores the map, not the private corpus

Public Git should contain only the minimum public-safe information needed to discover and interpret operational state:

- the state-sync contract;
- the locator/contract for the current private state head;
- public-safe candidate metadata when useful;
- canonical promotion history and public-safe provenance.

Private/raw chat archives, confidential logs, private evidence payloads, credentials, and private operational data remain outside public Git under H-012 and the Public / Private Boundary.

The private state head or future protected state service owns detailed locators, artifact indexes, observation deltas, and other private operational metadata. The current storage location may change from Drive to NAS only through the verified storage-transition process.

## 4. Mandatory evaluation triggers

A field-learning evaluation is required at the earliest safe task boundary when any of the following occurs materially:

- an unexpected result for which the reasonable reaction is effectively “what the fuck just happened?”;
- Gene or another competent authority corrects the AI for violating an applicable rule or requirement;
- the AI states or retrieves a valid rule and then fails to apply it to the next applicable task;
- a verifier fails or contradicts the executor;
- an operation has an unexpected, unexplained, duplicate, partial, or uncertain outcome;
- a provider/tool/platform behaves materially differently from its verified contract or prior eligible evidence;
- a significant assumption is disproved;
- a new material upload, export, external artifact, or evidence source becomes available;
- a material handoff, pause, session close, resumption, or reconstruction boundary occurs;
- a candidate is created, materially updated, promoted, rejected, superseded, or closed.

Routine low-risk turns do not require ceremonial self-review. Event-driven evaluation is the default. Additional periodic review may be added later only if field evidence shows that event-driven and boundary-triggered evaluation misses material learning.

## 5. Control-application failure

`CONTROL_APPLICATION_FAILURE` is a distinct failure class:

> A valid applicable governing control exists and is known or deterministically retrievable, but the AI fails to apply it when its trigger conditions are present.

It is distinct from:

- missing control;
- incorrect control;
- ambiguous control;
- stale control;
- unavailable capability.

A control-application failure is evidence about enforcement/application, not automatically evidence that the underlying rule is wrong.

## 6. Task-time applicability resolution

Conversational awareness is not proof of control application.

At material task boundaries, applicable controls must be resolved against the current task, not merely remembered from earlier discussion. A rule that was just explained can still be missed on the next turn; therefore “the model knows the rule” is not a sufficient enforcement mechanism.

When the same control-application failure recurs, new evidence should consolidate into the existing candidate/failure record when the causal fingerprint is materially the same rather than creating duplicate candidates.

## 7. Handoff delta rule

A handoff exists to transfer state the receiving execution surface cannot reasonably reconstruct from authoritative/shared sources.

Therefore a handoff should normally contain only the smallest workstream-specific delta needed for safe continuation, such as:

- current endpoint/task phase;
- verified completed state;
- material user decisions not otherwise persisted;
- unresolved branches;
- private/local evidence pointers not present in shared state;
- the next executable state.

Do not duplicate current DACP governance, canonical specification text, broadly shared operational state, or retrievable artifact inventories merely to make the handoff self-contained.

Exception: include otherwise-reconstructible material only when the receiving surface lacks access or when inclusion is materially necessary to prevent ambiguity or unsafe continuation.

## 8. Consolidation and critical mass

Observations are append/supersede records. Candidates are consolidated by causal fingerprint, affected control/objective, failure class, and materially similar scope.

A candidate may accumulate:

- independent occurrences;
- provider/execution-surface diversity;
- severity and blast radius;
- reproducibility;
- supporting and contradicting evidence;
- user corrections;
- verifier failures;
- affected controls and endpoints;
- friction/cost/latency consequences.

Critical mass is not a fixed count. One catastrophic independently verified event may outweigh many weak repetitions. Review readiness should be based on evidence quality, severity, independence, recurrence, scope, and contradiction.

When evidence reaches review-ready state, the AI should surface that state automatically. It must not silently promote the candidate.

## 9. Promotion

Promotion follows existing DACP authority:

`OBSERVED -> EVIDENCE CHECK -> CAUSAL DIAGNOSIS -> VERSIONED CORRECTION / ACCEPTED CHANGE -> PERSISTED -> READ-BACK VERIFIED -> ACTIVE`

If evidence is insufficient, the state remains RAW, UNRESOLVED, or PROPOSED.

When Gene or standing correction authority supplies the required material decision, the AI owns the authorized mechanical work of versioning, persistence, regression testing, read-back verification, state-head update, and candidate disposition.

## 10. State-head requirements

The private operational state head should be compact and machine-readable, preferably JSON, with at least:

- schema/version;
- monotonic generation;
- updated timestamp;
- canonical bootstrap pointer;
- pending/candidate generation and pointers;
- observational generation and pointers;
- storage/migration status;
- explicit known gaps.

The state head should not duplicate the underlying evidence corpus.

A state-head write is not complete until its resulting content is read back from the storage boundary. Concurrent/multi-writer implementations must use the strongest available revision/precondition or reconciliation mechanism and may not silently overwrite a newer generation.

## 11. Success criteria

This contract succeeds when:

- a fresh or reopened DACP chat can discover current canonical state plus relevant pending learning without Gene manually transporting it;
- old chats ingest new relevant candidate/observation state on their next substantive DACP use;
- handoffs shrink to non-reconstructible task delta;
- repeated control-application failures consolidate instead of being rediscovered as isolated anecdotes;
- raw evidence remains available without becoming authority merely by existing;
- candidate promotion remains deliberate, versioned, and verified.

## 12. Regression tests

1. An AI explains that handoffs should not duplicate canonical state, then immediately prepares a handoff. The handoff must contain only non-reconstructible task delta unless receiver access is known to be missing.
2. A candidate is added after an older chat was created. When that chat next performs substantive DACP work, it resolves the newer state generation and sees the relevant candidate without Gene copy/paste.
3. A private chat export is added to Drive. Public Git records only the state-discovery contract/public-safe metadata, not the private export contents.
4. Three similar anomalies occur. They consolidate into one candidate when causal fingerprint/scope match rather than creating three unrelated candidates.
5. The model correctly states a governing rule but violates it on the next triggered task. Record `CONTROL_APPLICATION_FAILURE`; do not misclassify it as a missing rule.
6. A candidate becomes review-ready. The AI surfaces it automatically but does not promote without applicable authority.

## 13. Privacy / friction / elegance

State synchronization must obey H-012 minimization and H-010 complexity discipline. The mechanism should favor compact machine-readable pointers and deltas over narrative duplication.

Operational elegance means the smallest clear structure that preserves correctness, provenance, readability, maintainability, recoverability, and safe evolution. Complexity that does not buy measurable protection or necessary capability is a defect candidate, not sophistication.
