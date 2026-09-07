# Deterministic AI Control Plane
## Heuristics Specification 0.1.2

**Status:** AUTHORITATIVE PROJECT SPECIFICATION / ACTIVE / GENE INTERIM DECISION  
**Effective:** Immediately when persisted to canonical `main` and independently read back.  
**Supersedes:** `DACP_Heuristics_Specification_0.1.1.md` for the sections replaced below.  
**Base specification:** `DACP_Heuristics_Specification_0.1.1.md`  
**Active heuristic count:** 17  
**Decision source:** Gene's 2026-09-07 instruction to correct the observed handoff/control-application failure, make operational learning automatically available across DACP chats, and write elegance/readability/maintainability/survivability into the heuristics.  
**Implementation boundary:** This specification governs behavior and field use. It does not itself authorize building the DACP application.

## Composition rule

This is a patch specification. The active 0.1.2 heuristic set is the complete 0.1.1 specification with H-010, H-011, and H-016 replaced by the sections below. All other 0.1.1 heuristics and cross-cutting invariants remain active unchanged.

A consumer resolving 0.1.2 must load the base specification identified above and then apply these replacements. No other 0.1.1 section is modified by this patch.

---

# H-010 — Every control and implementation structure must earn its complexity, remain elegant enough to survive change, and have an enforcement path

**Failure / requirement addressed:** Controls, schemas, prompts, code, or operating structures accumulate unnecessary complexity, duplication, cleverness, or ceremony; readability and maintainability decay; later AI/human maintainers misapply or abandon the system; manipulated telemetry can also make a necessary control look unnecessary.

**Existing rule / source:** H-010 in 0.1.1; KISS / Anti-Ceremony Principle; Gene's 2026-09-07 explicit elegance requirement; repeated handoff duplication field evidence.

**Proposed refinement / rule:** Every retained control, data structure, interface, schema, prompt contract, or implementation pattern must identify the measurable protection or necessary capability it provides. Prefer the smallest clear structure that preserves correctness, provenance, readability, maintainability, recoverability, and safe evolution. Elegance is operational, not ornamental: names, data flow, control flow, interfaces, and representations should make the intended behavior obvious enough that future humans and AIs can inspect, modify, test, and recover the system without unnecessary reconstruction. Before adding or retaining complexity, test whether it can be deleted, merged, simplified, normalized, expressed as data rather than prose, or moved to a test/build-time mechanism without losing protection. Prefer explicit composition over duplicated narrative and boring readable structures over clever compression. Control value may be established by severity, credible threat model, near misses, adversarial tests, or trusted field evidence, not only observed catches. Evidence used to weaken/remove a control must itself be sufficiently trustworthy. Friction or latency can justify redesign, automation, or safe narrowing, but cannot by itself waive material safety, privacy, authority, evidence, or verification requirements.

**Trigger:** Proposal to add, retain, duplicate, simplify, suspend, or remove a control; design of a schema/interface/state representation; material code or configuration construction/refactor; repeated confusion or maintenance friction traceable to structure.

**Inputs:** Risk/capability addressed; evidence quality; enforcement mechanism; readability/maintainability burden; dependency/coupling cost; change/recovery path; friction/latency data; alternative simpler representations.

**Allowed actions:** Merge duplicate controls; normalize repeated state; use compact machine-readable structures where they improve clarity; refactor toward obvious interfaces; move selective checks out of runtime; retire complexity with verified equivalent protection.

**Forbidden actions:** Add abstraction or indirection without measurable benefit; duplicate authoritative/shared state merely for self-containment; prefer clever compactness that obscures behavior; optimize only for present author convenience while making future inspection, testing, recovery, or modification materially harder; remove rare-event safeguards solely because catches are rare.

**Evidence required:** Evidence proportional to the risk of adding/removing the control or structural complexity. Structural simplification that preserves behavior may use regression/readback evidence rather than philosophical justification.

**Failure behavior:** Preserve necessary protection while simplifying the narrowest causal complexity. If simplification cannot be shown safe, keep the current behavior and mark the design question unresolved/proposed rather than silently weakening it.

**Escalation behavior:** Route material risk acceptance or genuinely new control objectives to proper authority; otherwise the AI owns routine simplification/refactoring within authorized scope.

**Telemetry recorded:** Complexity added/removed; duplication detected; readability/maintenance defects; false stops; latency/friction; incident/near-miss evidence; enforcement failures; recovery difficulty.

**Success criterion:** The smallest reasonably complete structure survives field use, is readable by a fresh competent reviewer, and can be changed/recovered without unnecessary coupling, duplicated truth, or ritual.

**Regression test:** (1) Two equivalent designs exist; choose the simpler explicit design when it preserves verification and recovery. (2) A handoff can repeat current Git/governance state or point the receiver to shared state; use the pointer/delta. (3) A compact representation saves lines but hides material state transitions; reject the clever representation. (4) A future maintainer can identify the governing source, state transition, and verification path without reconstructing narrative history.

**Regression risks:** Subjective aesthetic preference masquerading as elegance; premature abstraction removal; oversimplification that hides necessary controls; refactoring churn.

**User-friction / latency test:** Simplicity should reduce human mechanical work and repeated explanation. Any extra structure must justify itself by measurable protection, capability, or maintenance/recovery value.

**Privacy implications:** Simpler data flows and less duplication should reduce unnecessary retention and replication; privacy protections still require equivalent coverage before simplification.

**Intended scope:** UNIVERSAL.

**Status:** ACTIVE / GENE INTERIM DECISION.

---

# H-011 — Keep working communication and handoffs minimal while preserving a tamper-aware reconstructible control trace

**Failure / requirement addressed:** Important actions cannot be reconstructed; a compromised executor fabricates/rewrites its own clean history; or handoffs become bloated copies of authoritative/shared state, increasing contradiction risk and user/mechanical burden.

**Existing rule / source:** H-011 in 0.1.1; AIRD-020/030; repeated 2026-09-07 handoff-duplication field evidence; `DACP_Operational_State_Sync_0.1.md`.

**Proposed refinement / rule:** Keep user-facing working communication to the minimum that advances the task, while preserving a compact durable trace for material control transitions. Prefer boundary-generated records, stable work/event IDs, ordered sequence, source references, and append/supersede semantics. A handoff transfers only the smallest workstream-specific state the receiving execution surface cannot reasonably reconstruct from current canonical/shared sources. Do not duplicate current DACP governance, canonical specification text, broadly shared operational state, or retrievable artifact inventories merely to make a handoff self-contained. Include otherwise-reconstructible material only when receiver access is unavailable/uncertain or omission could materially impair safe continuation. When later reconstruction materially depends on referenced evidence that can change or disappear, preserve an immutable identity such as version/revision/hash/content address or authorized protected snapshot sufficient to detect substitution, balanced against H-012. A recorder is not a verifier merely because it recorded something.

**Trigger:** Consequential action; material state-bearing assertion; authority change; uncertain retry; material incident; accepted rule/spec change; material pause/resume/session close; cross-chat/provider handoff; reconstruction boundary.

**Inputs:** Endpoint; authority; evidence refs; action lifecycle; current shared-state availability; external identifiers; verification result; receiver capability/access where known.

**Allowed actions:** Use references/hashes/IDs instead of raw payloads; preserve superseded state; redact/minimize sensitive content; transfer only verified completion, unresolved branches, non-persisted user decisions, inaccessible evidence pointers, and next executable state when those are the necessary delta.

**Forbidden actions:** Reconstruct a missing event from narrative and present it as recorded fact; silently rewrite material history; treat executor-generated log as independent proof; copy retrievable canonical/shared state into handoffs without a material reason; make Gene manually transport state that an authorized shared-state path can provide.

**Evidence required:** Trace provenance/integrity proportionate to consequence; enough evidence to know whether referenced shared state is actually available when reliance on it matters.

**Failure behavior:** Missing/integrity-failed trace remains UNRESOLVED. If shared-state access is unavailable, expand the handoff only by the minimum necessary delta rather than assuming access or duplicating everything by default.

**Escalation behavior:** Seek independent boundary evidence when material reconstruction depends on disputed trace; ask Gene only for genuine access/authentication/authority boundaries.

**Telemetry recorded:** Event IDs; sequence; recorder boundary; integrity state; supersession chain; handoff size/class; duplicated reconstructible state detected; receiver-access exception reason.

**Success criterion:** A fresh reviewer or receiving chat can resume safely and reconstruct the material path without hidden reasoning, while the handoff contains no unnecessary copy of authoritative/shared state.

**Regression test:** (1) After explicitly stating the handoff-delta rule, the AI immediately prepares another handoff; it must not repeat current Git/governance state available to the receiver. (2) Receiver cannot access the shared state service; the handoff includes the minimum missing material. (3) Executor alters its local log after a failed write; independent anchor reveals mismatch or leaves the transition unresolved.

**Regression risks:** Over-minimization that omits material local state; incorrect assumptions about receiver access; logging bureaucracy; false trust in append-only appearance.

**User-friction / latency test:** Trace/handoff generation should be automatic and concise, with detail scaling only when consequence or unavailable shared state requires it.

**Privacy implications:** Minimum necessary control metadata; no hidden chain-of-thought; bounded retention; reduced duplication of private evidence.

**Intended scope:** UNIVERSAL.

**Status:** ACTIVE / GENE INTERIM DECISION.

---

# H-016 — Active controls are integrity-protected, task-time applied, version-scoped, staged, defeasible, and continuously challenged

**Failure / requirement addressed:** Rules become dogma, churn under poisoned evidence, diverge into competing current versions, are promoted globally before enough testing, or exist correctly but fail to govern an applicable task because the model merely remembered/explained them rather than resolving them at task time.

**Existing rule / source:** H-016 in 0.1.1; former RC1 field-evidence/role-reversal mechanisms; Project Instructions; repeated 2026-09-07 control-application failure evidence; `DACP_Operational_State_Sync_0.1.md`.

**Proposed refinement / rule:** Reopening a rule for review is cheap; changing, suspending, broadening, or removing it requires evidence/authority proportional to consequence. Current-spec identity and integrity must be deterministically selected and verifiable. At material task boundaries, applicable controls must be resolved against the current task and current shared operational state; conversational awareness, recent explanation, or model confidence is not evidence that a control has been applied. A valid applicable control that is known or deterministically retrievable but is not applied when triggered is `CONTROL_APPLICATION_FAILURE`, distinct from missing, incorrect, ambiguous, stale, or unavailable controls. Such a failure is evidence about enforcement/application and must not automatically rewrite the underlying rule. Repeated materially same-cause failures should consolidate under a shared causal fingerprint rather than fragment into duplicate candidates. New/materially changed global rules should, where feasible, pass candidate -> adversarial test -> bounded/shadow/canary or limited-scope use -> review -> explicit acceptance -> persisted/read-back verified activation. Material control conflicts remain explicit and follow authority/scope precedence; no executor may silently choose the more permissive rule. Every surviving rule remains challengeable by trusted field evidence and materially different scenarios.

**Trigger:** Proposed heuristic change; regression/anomaly; provider/platform change; conflicting versions; field evidence; material user correction; verifier contradiction; repeated WTF event; resumption with newer shared-state generation; detected control-application failure.

**Inputs:** Current accepted version; current applicable task/state; candidate delta; provenance; adversarial/field evidence; causal fingerprint; rollout scope; rollback criteria; authority.

**Allowed actions:** Open/consolidate a candidate from a weak signal; classify enforcement failure separately from rule defect; use field tests and materially different scenarios; stage/rollback changes; merge/retire rules when protection is preserved; ingest relevant unseen pending/observational state before material reliance.

**Forbidden actions:** Silently promote; infer that a rule is being enforced because it was recently mentioned; misclassify a known-rule application failure as proof the rule is missing/wrong; resolve a material rule conflict by choosing the permissive control; let usability/friction alone waive a material requirement; treat one successful case as universal proof; claim two specs are both current; rewrite historical prior state.

**Evidence required:** Current-spec integrity evidence; task/control applicability evidence proportional to consequence; candidate required fields plus evidence proportional to activation/removal consequence.

**Failure behavior:** Preserve the current rule while change evidence is inadequate. Record `CONTROL_APPLICATION_FAILURE` when appropriate, evaluate at the earliest safe task boundary, and correct the narrowest enforcement/application path before modifying the underlying control unless evidence separately demonstrates a rule defect.

**Escalation behavior:** Route acceptance/risk/new-objective decisions to proper authority; preserve dissent/evidence. Routine enforcement plumbing and evidence-forced narrow corrections remain AI-owned where standing authority permits.

**Telemetry recorded:** Candidate/version IDs; current state generation; applicable control set where material; control-application failures; causal fingerprints; user corrections; verifier contradictions; integrity/hash/revision; tests; rollout stage; rollback; rule-conflict disposition; field failures; false stops; latency/friction; review result.

**Success criterion:** The system can identify the current applicable rule version, show that material triggered controls were resolved at task time, distinguish enforcement failure from rule defect, consolidate repeated failures, and roll back/supersede without erasing history.

**Regression test:** (1) AI correctly explains a rule and violates it on the immediately following applicable task; classify `CONTROL_APPLICATION_FAILURE` and fix enforcement rather than inventing a missing rule. (2) An older chat resumes after a relevant candidate/state generation update; it loads the relevant unseen delta before consequential reliance. (3) Fabricated telemetry claims a safeguard is useless; review may open but the rule is not removed without trustworthy evidence. (4) Competing current specs cause STOP until authority/integrity resolves identity.

**Regression risks:** Excessive task-time checking; noisy failure classification; overconsolidation of superficially similar events; state-sync latency; conservatism slowing necessary change.

**User-friction / latency test:** Task-time resolution should operate on material gates and relevant deltas, not turn harmless routine turns into ritual. Measure sync cost, false evaluations, and duplicated work.

**Privacy implications:** Shared learning uses minimum necessary metadata and pointers; private evidence remains protected under H-012 and is not copied into public canonical state merely to aid enforcement.

**Intended scope:** UNIVERSAL governance / release / control-application rule.

**Status:** ACTIVE / GENE INTERIM DECISION.

---

## 0.1.1 -> 0.1.2 field correction summary

- Added operational elegance/readability/maintainability/survivability requirements to H-010 without weakening KISS or higher-authority controls.
- Corrected H-011 so handoffs transfer only non-reconstructible task delta unless receiver access/safety requires more.
- Corrected H-016 to distinguish `CONTROL_APPLICATION_FAILURE` from rule defects and require task-time applicability resolution at material gates.
- Bound the heuristic changes to `DACP_Operational_State_Sync_0.1.md` for cross-chat RAW / PENDING / CANONICAL synchronization.
- Preserved the 17-heuristic count; no new control objective was added beyond enforcing, simplifying, and operationalizing existing control objectives.
- No DACP application implementation is authorized by this correction.

## Current acceptance status

Heuristics Specification 0.1.2 is **AUTHORITATIVE / ACTIVE / GENE INTERIM DECISION** once canonical persistence and independent read-back are complete. It contains 17 active heuristics by composition with 0.1.1.
