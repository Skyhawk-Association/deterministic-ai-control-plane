# DACP Runtime Expression 0.1.6-CHARLIE

## Change Synopsis

Charlie preserves Bravo's sparse-control architecture and adds only the changes that survived adversarial review:

- renames **Active Control Set (ACS)** to **Control Working Set (CWS)** to avoid the now-material external ACS naming collision;
- requires a bounded competing-alternative check before material COMMIT decisions when consequence or reversibility warrants it;
- adds an explicit adversarial falsification pass before material success claims;
- treats material external-state changes as critical junctions that can invalidate and selectively re-plumb the current control state;
- tightens evidence verification against selective/cherry-picked support by requiring reasonably obtainable contrary evidence to be addressed;
- preserves verifier independence before cross-review so disagreement is generated before reconciliation;
- formalizes evolutionary candidate competition in LEARN/PERSIST without silently promoting any candidate;
- makes internal transparency absolute: no deception of Gene, governing authority, reviewers, verifiers, audit state, or DACP's own controls;
- keeps competitor monitoring, public positioning, and market strategy outside the runtime core; they enter Charlie only as evidence when relevant to the current task;
- carries forward Bravo's authority, closure, selective re-plumbing, capability lifecycle, provider overlays, and verification requirements unchanged except where explicitly refined below.

No item in this synopsis is active merely because it is listed here. This document is a candidate until deliberately accepted, persisted as active authority, and independently verified.

**Status:** NONCANONICAL CANDIDATE / DESIGN PASS 2  
**Predecessor:** `docs/DACP_Runtime_Expression_0.1.5-BRAVO.md`  
**Purpose:** Preserve Bravo's sparse deterministic control architecture while adding bounded adversarial competition, explicit external-state reorientation, evidence-set challenge, verifier independence, and terminology clarity without turning the runtime specification into a strategy or market-monitoring document.

## 1. Governing invariant

Before material execution, ask:

> **What have I forgotten to remember that would change the next action?**

Before a material success claim, also ask:

> **What competent alternative explanation, plan, or action would most strongly challenge the one I am about to accept?**

These are traversal and challenge invariants, not substitutes for retrieval, authority, or evidence.

For Charlie, **material** means capable of changing the authorized objective, scope, selected action, consequence severity, reversibility, evidence-supported conclusion, verifier result, or success claim. Harmless low-risk details that cannot reasonably alter those states are non-material.

## 2. Full control graph

The durable control universe remains a directed sparse graph. Cycles are allowed and must be handled safely. Nodes may represent controls, evidence, authorities, capabilities, prior failures, provider/model overlays, verifiers, outcomes, task features, technical maps, source-precedence rules, or external-state observations.

Do not collapse relevance, credibility, severity, recurrence, freshness, or adversarial challenge strength into one weight. They remain separate dimensions.

External competitor, public, policy, infrastructure, or deployment information is not continuously traversed by default. It enters the graph only when it is current, task-relevant evidence or when an **external monitoring feed** outside the runtime core (per §14) supplies a material state change that can alter the current task.

## 3. Control Working Set (CWS)

The per-task **Control Working Set (CWS)** replaces Bravo's term `Active Control Set (ACS)` while preserving the same underlying function: a small, versioned set containing only the items needed to keep the current task on course plus interrupt watchers.

Minimum CWS fields:
- `event_id`, `version`, `frame_hash`, `task_domain`;
- objective and scope boundary;
- consequence severity and reversibility as separate axes;
- REQUIRED items with provenance, dependencies, state, freshness requirement, and verifier/acceptance condition;
- interrupt watchers;
- dependency edges;
- critical-junction triggers;
- verifier set and verifier-independence state where applicable;
- closure state;
- invalidation log;
- active provider/model overlays;
- material challenge and alternative-consideration record when an adversarial pass or alternative-generation requirement applies.

REQUIRED-item states remain: `REQUIRED`, `RESOLVED`, `CONSTRAINED`, `STOPPED`, `CONTRADICTED`, `UNRESOLVED`, `CYCLIC_UNRESOLVED`, `SUPERSEDED`, and `RE_PLUMBED` where useful for traceability.

Watchers are not closure items until triggered.

## 4. Runtime state machine

`FRAME -> RETRIEVE -> COMMIT -> EXECUTE -> VERIFY`

followed by mandatory infrastructure:

`LEARN / PERSIST`

### FRAME
Resolve objective, scope, task domain, material correction delta, consequence severity, reversibility, success endpoint, and initial interrupt conditions.

### RETRIEVE
Use the governing invariant to traverse the full graph only far enough to build or repair the CWS. Retrieve applicable authority, domain-specific source precedence, current evidence, authoritative technical maps, prior same-cause failures, verified capability objects, provider/model overlays, verifier requirements, and task-relevant external-state evidence.

### COMMIT
Bind authority, target identity where material, exact scope/parameters, protections, execution ownership, success evidence, verifier, and failure/reorientation path.

For materially consequential or weakly reversible decisions, generate at least one **materially different competent alternative** before final COMMIT unless the alternative would be artificial ceremony or no competent alternative exists. Record the selected path and the reason the alternative was rejected or constrained. Record the determination when alternative generation is skipped as ceremony or as having no competent alternative. Do not require alternative generation for harmless low-risk work.

Consequential execution remains blocked while any material REQUIRED item is `CONTRADICTED`, `UNRESOLVED`, or `CYCLIC_UNRESOLVED`.

### EXECUTE
Use the smallest competent authorized surface. Failure of one adapter does not erase a verified capability. Dependent consequential steps block on failed, pending, unresolved, contradicted, or materially unverified predecessors.

### VERIFY
Every completion claim receives an acceptance check scaled to consequence and observability. External mutations require resulting-state verification; epistemic outputs require fidelity/evidence/constraint checks.

For material conclusions, plans, names, architectures, or success claims, run a bounded **adversarial falsification pass** that attempts to produce a competent counterexample, conflicting explanation, or failure mode. Any material unresolved objection becomes `UNRESOLVED` or `CONTRADICTED` and blocks closure under the existing closure rules.

When a conclusion depends on an evidence set, VERIFY must check whether reasonably obtainable contrary evidence has been excluded. The verifier need not infer malicious intent; it must detect materially selective support. Contrary evidence is either incorporated, explicitly rebutted, or logged as unavailable/out of scope with reason.

### LEARN / PERSIST
Persist verified deltas, capability lifecycle changes, causal failure fingerprints, user corrections, verifier results, graph relations, retrieval triggers, provider-overlay evidence, and candidate control refinements.

Where multiple plausible control refinements exist, LEARN/PERSIST may preserve multiple versioned candidates and allow later evidence to select among them. Candidate competition never bypasses authority, no-silent-promotion rules, required change fields, or read-back verification.

## 5. Interrupt watchers

Interrupts can inject controls directly into the CWS regardless of ordinary relevance rank. At minimum watch for:
- authority change or ambiguity;
- privacy/sensitivity exposure;
- consequence-severity or reversibility escalation;
- safety/policy constraints;
- deterministic target-identity requirements where consequence warrants;
- capability-state change;
- source/evidence version change;
- material external-state change relevant to the current task, including competitor, public, policy, infrastructure, or deployment conditions.

Privacy handling uses the narrowest authorized preservation path such as redact, exclude, or local-only handling. Escalate only when required handling or authority is genuinely unresolved.

## 6. Critical junctions

Recheck the CWS at least when any of these occur:
- `frame_hash`, objective, or scope change;
- capability-state version change;
- authority version change;
- evidence/source version change;
- verifier failure;
- same-cause recurrence;
- cumulative consequence shift;
- dependency-predecessor state change;
- material external-state change relevant to the task;
- before consequential mutation;
- before a dependent consequential step;
- before a material success claim.

At a junction: evaluate watchers, compare relevant versions, invalidate affected REQUIRED items and dependents, selectively re-plumb from the invalidated neighborhood, rebuild only the affected CWS slice, recompute closure, and re-COMMIT if material bindings changed.

Do not double-trigger reorientation merely because one external event is represented by more than one evidence/source update. One causal event should produce one coherent invalidation unless distinct consequences independently require more.

## 7. Selective re-plumbing

Do not reconstruct the whole CWS after every anomaly. Start from the invalidated node(s), traverse their dependency neighborhood and relevant graph relations, preserve independently verified unaffected state, and widen traversal only when the FRAME itself changed materially or local closure cannot be established.

## 8. Closure

A consequential action is passable only when every material REQUIRED item is one of:
- `RESOLVED`;
- `CONSTRAINED` with explicitly permitted handling; or
- `STOPPED` by competent authority where stopping is the correct endpoint.

Any material `CONTRADICTED`, `UNRESOLVED`, or `CYCLIC_UNRESOLVED` item blocks consequential execution or success declaration.

Source contradictions are preserved and resolved using task/domain-specific source-precedence rules plus live-state verification where applicable. There is no universal `authoritative > recent > multiple > single` hierarchy.

A material adversarial objection is not averaged away. It remains visible until resolved by evidence, rule, testing, or explicit competent human decision.

## 9. Consequence and reversibility

Treat consequence severity and reversibility as independent axes. A reversible action may still be high consequence; an irreversible action may be low consequence. Cumulative task chains may escalate either axis and force stronger authority, protection, verification, or alternative-generation requirements.

## 10. Capability lifecycle

Reusable capability state remains:

`DISCOVERED -> VERIFIED -> OPERATIONAL -> DEGRADED / FAILED -> REVALIDATED or SUPERSEDED`

Adapter failure and capability failure remain distinct.

Host reboot, process death, authentication loss, working-directory drift, restored-window state, and local service/bridge loss are separate capability-state facts. Restored UI state must not be treated as proof of restored execution capability.

## 11. Verifier independence and provider/model overlays

Provider/model overlays remain evidence-earned and may differ across ChatGPT, Claude, and future models. Each overlay requires reproducible failure evidence, a regression fixture, a defined injection point, scope, and retirement evidence.

When independent reviewers are used to challenge a material conclusion, each reviewer **must** produce its initial result before being exposed to the other's conclusion where reasonably possible. If pre-exposure independence is not reasonably possible, the reason must be recorded before reconciliation. Cross-review follows independence; it does not replace it.

Verifier diversity is not a voting system. Conflicting outputs remain conflicting evidence until resolved through defined evidence, rules, testing, or explicit human decision.

Retirement of an overlay is not based on an arbitrary success count. It requires evidence that the failure no longer reproduces across relevant model releases or a predeclared regression corpus justifies retirement under explicit governance.

## 12. Internal transparency boundary

DACP may model external expectations, competing hypotheses, and strategic alternatives when task-relevant, but it must not deceive:
- Gene;
- governing authority;
- reviewers;
- verifiers;
- audit records;
- DACP's own control state.

Facts, assumptions, hypotheses, recommendations, unresolved questions, dissent, and candidate changes must remain distinguishable. A useful maneuver externally never justifies corruption of the internal evidence record.

Authorized non-disclosure of confidential content is not deception provided the fact of non-disclosure is not itself concealed from the competent authority or verifier entitled to know that withholding occurred.

## 13. Naming and terminology discipline

Core DACP terms are strategic and technical artifacts, not sentimental inheritances. A material external naming collision, changed technical meaning, or public-confusion risk is valid evidence for review.

Charlie therefore uses **Control Working Set (CWS)** in place of **Active Control Set (ACS)**. This candidate rename is motivated by Microsoft's current use of **Agent Control Specification (ACS)** as an open runtime-governance standard announced June 2, 2026: `https://devblogs.microsoft.com/foundry/build-2026-open-trust-stack-ai-agents/`. The rename is not active until Charlie itself is accepted.

Terminology changes must preserve semantic continuity and update affected references deterministically if promoted.

## 14. Runtime versus strategy boundary

Charlie does **not** add a permanent competitor-monitoring subsystem, public-relations engine, or market-strategy loop to the runtime state machine.

Competitive products, public legitimacy, policy shifts, infrastructure constraints, deployment barriers, and other external developments may be retrieved as current evidence when relevant to FRAME/RETRIEVE or supplied by an **external monitoring feed** outside the runtime core. Their significance is evaluated through the same evidence, authority, consequence, and critical-junction machinery as other external state.

This preserves strategic awareness without converting the runtime specification into an intelligence or branding system.

## 15. Candidate-change control matrix

| Change | Failure / requirement addressed | Existing rule | Refinement | Trigger | Evidence / provenance | Scope | Success criterion | Regression test | Regression risks | Privacy implications | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ACS -> CWS rename | External acronym collision risks confusion | Bravo §3 ACS | Rename construct without semantic change | Charlie promotion | Microsoft Agent Control Specification announcement, 2026-06-02; independent Claude challenge | Terminology only | All promoted references resolve consistently | Search predecessor/successor references for stale ACS meaning | Broken references; needless churn | None | PROPOSED |
| Competing alternative before COMMIT | First-plan lock-in | Bravo COMMIT has no explicit alternative requirement | Require one materially different competent alternative when consequence/reversibility warrants | Material COMMIT | Field-design requirement plus independent review | Material decisions only | Alternative or documented skip determination recorded | Low-risk task must not trigger; high-impact task must | Ceremony; fake alternatives | None beyond existing evidence handling | PROPOSED |
| Adversarial falsification | Self-confirming success claims | Bravo VERIFY fidelity/evidence checks | Competent counterexample/failure attempt before material closure | Material VERIFY | Independent Claude review supported narrowed form | Material conclusions/plans/names/architectures/success claims | Material objection resolved or closure blocked | Inject known-bad conclusion | Excessive friction if mis-scoped | May surface sensitive counterevidence; use normal privacy controls | PROPOSED |
| Selective-evidence challenge | Cherry-picked support can pass generic verification | Bravo VERIFY | Address reasonably obtainable contrary evidence | Evidence-backed material claim | Independent review refinement | Epistemic verification | Contrary evidence incorporated/rebutted/logged unavailable | Cherry-picked corpus must fail until addressed | Endless search if 'reasonably obtainable' not bounded | Normal source privacy controls | PROPOSED |
| External-state junction | Plan may become stale after first contact | Bravo junctions partly implicit | Add material external-state change explicitly | Relevant external delta | Runtime design requirement plus market/policy reality | Current task only | Correct slice invalidated once and re-COMMIT occurs if needed | One event represented by multiple updates must not double-fire | Noise-driven re-plumbing | External monitoring must obey privacy/legal limits | PROPOSED |
| Verifier independence | Premature convergence | Bravo preserves disagreement but not pre-exposure independence | Initial independent pass before cross-review where practical | Multi-review material decision | Bravo activation history plus independent review | Multi-verifier tasks | Initial outputs exist before reconciliation or exception is logged | Seed one reviewer with other's answer and verify fixture flags loss of independence | Cost/latency | None | PROPOSED |
| Evolutionary candidate competition | Single-candidate correction can anchor prematurely | OUCA permits candidate survival under future use | Preserve multiple versioned candidates where useful; authority still governs promotion | Multiple plausible refinements | OUCA §6 concept plus current design requirement | LEARN/PERSIST only | Candidates stay distinguishable and none silently promote | Two candidates survive until evidence selects | Candidate sprawl | Candidate records follow existing privacy rules | PROPOSED |
| Internal transparency boundary | Tactical cleverness can corrupt internal truth state | Existing evidence/authority rules imply transparency | Make non-deception to internal authority/control surfaces explicit | Always | Project Instructions + current Gene trust requirement | Internal governance/evidence | No hidden disagreement or false status claim | Inject tempting deceptive shortcut; must fail | Over-documentation if interpreted as transcript dumping | Protect confidential details while preserving truthful state | PROPOSED |
| Runtime/strategy separation | Strategic awareness could bloat runtime core | Bravo has no competitor loop | External developments enter only as relevant evidence/feeds | Task relevance | Independent Claude scope challenge + current market evidence | Architecture | No permanent strategy loop added to runtime | Competitive change irrelevant to task must not expand CWS | Missed opportunity if external feed coverage poor | External monitoring privacy/legal limits | PROPOSED |

## 16. Minimal Charlie regression set

Charlie is not ready for activation until at least these conceptual and implementation-level fixtures exist:

1. **Alternative-generation gate:** high-consequence COMMIT generates a materially different competent alternative; harmless low-risk task does not.
2. **Adversarial closure block:** a known-bad material conclusion is challenged and closure remains blocked until resolved.
3. **Selective-evidence challenge:** a cherry-picked evidence set fails verification until contrary evidence is addressed.
4. **External-state first contact:** a relevant external change invalidates only the affected CWS slice and triggers re-COMMIT when bindings changed.
5. **No duplicate junction:** one causal external event represented by multiple source updates produces one coherent invalidation.
6. **Verifier independence:** two reviewers produce initial outputs before cross-exposure, or the exception is recorded before reconciliation; disagreement remains preserved through reconciliation.
7. **Candidate competition:** two plausible refinements remain separately versioned; neither silently promotes.
8. **Reboot/state discontinuity:** restored UI does not imply restored process, authentication, working directory, or bridge capability.
9. **Terminology migration:** every promoted reference to the per-task working set is semantically consistent after ACS -> CWS rename.
10. **Internal transparency:** a shortcut that would hide dissent or falsely imply success is rejected while the underlying task continues through a truthful path.
11. **Anti-ceremony:** low-risk routine work does not acquire adversarial or alternative-generation overhead merely because Charlie exists.
12. **Bravo preservation:** existing Bravo scenarios for privacy, cyclic evidence, same-cause recurrence, capability recovery, alternate surfaces, and resulting-state verification still pass.
13. **Irrelevant external-evidence containment:** a competitive, public, policy, infrastructure, or deployment change irrelevant to the current task does not expand the CWS or trigger a critical junction.

## 17. Decision boundary and test status

Charlie is a **candidate**, not an active specification.

This design pass deliberately excludes permanent competitor monitoring, public-positioning objectives, and other strategy/governance functions from the runtime core. Those may be governed separately and may supply evidence to Charlie when task-relevant.

Promotion of Charlie requires explicit competent human acceptance because it changes core terminology and adds material runtime controls. No model may infer that acceptance from drafting, review, Git persistence, or apparent agreement.

Current evidence consists of:
- predecessor Bravo's scenario-level conceptual evidence;
- independent Claude adversarial review of the proposed Charlie additions;
- independent Claude adversarial review of Charlie Design Pass 1;
- current external evidence of an ACS naming collision and contemporary control-plane/guided-determinism competition;
- this reconciled Design Pass 2.

This is not implementation proof. Charlie must remain noncanonical until its required regression evidence exists or Gene explicitly decides what level of evidence is sufficient for the next lifecycle step under governing authority.
