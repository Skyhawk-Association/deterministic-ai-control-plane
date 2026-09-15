# DACP Runtime Expression 0.1.5-BRAVO

**Status:** NONCANONICAL CANDIDATE / FIELD TEST  
**Canonical authority remains:** `authoritative/DACP_Heuristics_Specification_0.1.4.md`  
**Purpose:** Minimize runtime rule traversal while preserving task-relevant control coverage through a full sparse control graph, a small per-task Active Control Set (ACS), deterministic critical-junction rechecks, selective re-plumbing, and mandatory verification/persistence.

## 1. Governing invariant

Before material execution, ask:

> **What have I forgotten to remember that would change the next action?**

This is a traversal invariant, not a graph node and not an introspective substitute for retrieval.

## 2. Full control graph

The durable control universe is a directed sparse graph. Cycles are allowed and must be handled safely. Nodes may represent controls, evidence, authorities, capabilities, prior failures, provider/model overlays, verifiers, outcomes, task features, technical maps, or source-precedence rules.

Do not collapse relevance, credibility, severity, recurrence, and freshness into one weight. They are separate dimensions.

## 3. Active Control Set (ACS)

Each material task/event builds and carries a small, versioned ACS containing only the items needed to keep the current task on course plus interrupt watchers.

Minimum ACS fields:
- `event_id`, `version`, `frame_hash`, `task_domain`;
- objective and scope boundary;
- consequence severity and reversibility as separate axes;
- REQUIRED items with provenance, dependencies, state, freshness requirement, and verifier/acceptance condition;
- interrupt watchers;
- dependency edges;
- critical-junction triggers;
- verifier set;
- closure state;
- invalidation log;
- active provider/model overlays.

REQUIRED-item states include: `REQUIRED`, `RESOLVED`, `CONSTRAINED`, `STOPPED`, `CONTRADICTED`, `UNRESOLVED`, `CYCLIC_UNRESOLVED`, `SUPERSEDED`, and `RE_PLUMBED` where useful for traceability.

Watchers are not closure items until triggered.

## 4. Runtime state machine

`FRAME -> RETRIEVE -> COMMIT -> EXECUTE -> VERIFY`

followed by mandatory infrastructure:

`LEARN / PERSIST`

### FRAME
Resolve objective, scope, task domain, material correction delta, consequence severity, reversibility, success endpoint, and initial interrupt conditions.

### RETRIEVE
Use the invariant question to traverse the full graph only far enough to build or repair the ACS. Retrieve applicable authority, domain-specific source precedence, current evidence, authoritative technical maps, prior same-cause failures, verified capability objects, provider/model overlays, and verifier requirements.

### COMMIT
Bind authority, target identity where material, exact scope/parameters, protections, execution ownership, success evidence, verifier, and failure/reorientation path. Consequential execution is blocked while any material REQUIRED item remains `CONTRADICTED`, `UNRESOLVED`, or `CYCLIC_UNRESOLVED`.

### EXECUTE
Use the smallest competent authorized surface. Failure of one adapter does not erase a verified capability. Dependent consequential steps block on failed, pending, unresolved, contradicted, or materially unverified predecessors.

### VERIFY
Every completion claim receives an acceptance check scaled to consequence and observability. External mutations require resulting-state verification; epistemic outputs require fidelity/evidence/constraint checks.

### LEARN / PERSIST
Persist verified deltas, capability lifecycle changes, causal failure fingerprints, user corrections, verifier results, graph relations, retrieval triggers, and provider-overlay evidence. Persistence may propose control/overlay changes but may not silently promote them.

## 5. Interrupt watchers

Interrupts can inject controls directly into the ACS regardless of ordinary relevance rank. At minimum watch for:
- authority change or ambiguity;
- privacy/sensitivity exposure;
- consequence-severity or reversibility escalation;
- safety/policy constraints;
- deterministic target-identity requirements where consequence warrants;
- capability-state change;
- source/evidence version change.

Privacy handling uses the narrowest authorized preservation path such as redact, exclude, or local-only handling. Escalate only when required handling or authority is genuinely unresolved.

## 6. Critical junctions

Recheck the ACS at least when any of these occur:
- `frame_hash`, objective, or scope change;
- capability-state version change;
- authority version change;
- evidence/source version change;
- verifier failure;
- same-cause recurrence;
- cumulative consequence shift;
- dependency-predecessor state change;
- before consequential mutation;
- before a dependent consequential step;
- before a success claim.

At a junction: evaluate watchers, compare relevant versions, invalidate affected REQUIRED items and dependents, selectively re-plumb from the invalidated neighborhood, rebuild only the affected ACS slice, recompute closure, and re-COMMIT if material bindings changed.

## 7. Selective re-plumbing

Do not reconstruct the whole ACS after every anomaly. Start from the invalidated node(s), traverse their dependency neighborhood and relevant graph relations, preserve independently verified unaffected state, and widen traversal only when the FRAME itself changed materially or local closure cannot be established.

## 8. Closure

A consequential action is passable only when every material REQUIRED item is one of:
- `RESOLVED`;
- `CONSTRAINED` with explicitly permitted handling; or
- `STOPPED` by competent authority where stopping is the correct endpoint.

Any material `CONTRADICTED`, `UNRESOLVED`, or `CYCLIC_UNRESOLVED` item blocks consequential execution or success declaration.

Source contradictions are preserved and resolved using task/domain-specific source-precedence rules plus live-state verification where applicable. There is no universal `authoritative > recent > multiple > single` hierarchy.

## 9. Consequence and reversibility

Treat consequence severity and reversibility as independent axes. A reversible action may still be high consequence; an irreversible action may be low consequence. Cumulative task chains may escalate either axis and force stronger authority, protection, or verification.

## 10. Capability lifecycle

Reusable capability state is durable:

`DISCOVERED -> VERIFIED -> OPERATIONAL -> DEGRADED / FAILED -> REVALIDATED or SUPERSEDED`

Adapter failure and capability failure remain distinct.

## 11. Provider/model overlays

Provider/model overlays are evidence-earned and may differ across ChatGPT, Claude, and future models. Each overlay requires reproducible failure evidence, a regression fixture, a defined injection point, scope, and retirement evidence.

Retirement is not based on an arbitrary success count. It requires evidence that the failure no longer reproduces across relevant model releases or a predeclared regression corpus justifies retirement under explicit governance.

## 12. Test status

Current evidence is **scenario-level conceptual testing**, not implementation proof. Independent ChatGPT and Claude passes each exercised 12 scenarios covering capability recovery, stale path/source precedence, user correction, cumulative consequence escalation, false success, privacy interrupt, alternate execution surface, cyclic evidence, harmless low-risk work, new authoritative evidence mid-execution, provider overlay behavior, and a human-only boundary.

BRAVO must remain noncanonical until implementation/regression testing demonstrates that ACS construction, critical-junction triggers, selective re-plumbing, closure, provider overlays, and persistence work as intended without increasing missed controls or user friction.