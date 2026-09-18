# DACP Operational State Sync 0.2

## Change Synopsis

- Supersedes Operational State Sync 0.1.
- Preserves CANONICAL / PENDING-CANDIDATE / RAW-OBSERVATIONAL separation.
- Adds current CAR/ECR/SRR schema awareness to operational state.
- Makes repeated CONTROL_APPLICATION_FAILURE a first-class causal series with recurrence count and last-failed binding.
- Requires the state head to expose unresolved control-application failure pointers when present.
- Requires task bootstrap to ingest relevant unresolved recurrence evidence before material action.

**Status:** AUTHORITATIVE PROJECT DECISION / ACTIVE / GENE DECISION
**Effective:** upon canonical persistence and independent read-back verification

## 1. State layers

1. CANONICAL — governing Git authority.
2. PENDING / CANDIDATE — unresolved reusable learning.
3. RAW / OBSERVATIONAL — evidence and field events.

No silent promotion is permitted.

## 2. Bootstrap

For nontrivial or consequential work:

1. resolve CURRENT.md / CURRENT.json;
2. load active runtime and germane authoritative controls;
3. resolve STATE_LOCATOR.json;
4. resolve current private state head when authorized;
5. ingest relevant unseen candidate/observation deltas;
6. specifically check for unresolved same-cause CONTROL_APPLICATION_FAILURE affecting the current task domain, execution surface, source-resolution path, or verifier.

## 3. Required state-head fields

The private state head should include:
- schema;
- monotonic generation;
- timestamp;
- canonical bootstrap;
- pending/candidate generation and pointers;
- observational generation and pointers;
- unresolved failure-series pointers;
- storage/migration status;
- known gaps.

A current state head that omits known unresolved failure-series pointers is incomplete.

## 4. Failure-series record

A recurring control-application failure record should contain:
- causal fingerprint;
- first/last observed time;
- recurrence count;
- affected task domains;
- affected controls;
- failed CAR field(s);
- execution surfaces/providers;
- user corrections;
- verifier contradictions;
- human-friction consequence;
- current candidate/correction status;
- regression fixture pointer.

Same-cause events consolidate rather than fragment.

## 5. Evaluation triggers

Evaluate learning when:
- Gene corrects a control violation;
- a retrieved rule is violated in the next applicable action;
- the same causal control-application failure recurs;
- a verifier contradicts executor state;
- an unexpected/partial/uncertain outcome occurs;
- a material task handoff or resumption occurs;
- a candidate changes lifecycle state;
- an execution context proves different from the action's assumptions;
- an end-to-end assurance claim is disproved by a missing link.

## 6. Promotion

OBSERVED -> EVIDENCE CHECK -> CAUSAL DIAGNOSIS -> VERSIONED CORRECTION -> PERSISTED -> READ-BACK VERIFIED -> ACTIVE

A recurrence may justify immediate correction under standing authority when evidence is direct and the correction preserves existing objective/authority.

## 7. Success criteria

A fresh execution surface must be able to discover:
- active canonical controls;
- current private state;
- unresolved same-cause failure series;
- current correction/regression status;

without Gene manually reconstructing the failure history.

## 8. Regression

1. A known control is violated, recorded, and then violated again. The second task bootstrap must retrieve the recurrence before action.
2. A failure record is corrected canonically. State must point to the active correction and regression evidence.
3. Raw evidence remains non-authoritative until promoted.
4. Private evidence remains private; public Git stores only public-safe governance/correction material.
