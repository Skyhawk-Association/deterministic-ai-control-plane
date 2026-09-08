# Deterministic AI Control Plane
## Heuristics Specification 0.1.2

**Status:** PROPOSED HEURISTIC PATCH / REVIEW-READY / NOT ACTIVE  
**Effective:** Not active. Promotion remains blocked until canonical bootstrap/smoke-test compatibility can be changed without violating higher-authority execution-surface constraints.  
**Supersedes:** `DACP_Heuristics_Specification_0.1.1.md` for the sections replaced below.  
**Base specification:** `DACP_Heuristics_Specification_0.1.1.md`  
**Active heuristic count:** 17  
**Decision source:** Gene's 2026-09-07 instructions to correct observed handoff/control-application failures, make operational learning available across DACP chats, require operational elegance/readability/maintainability/survivability, and correct the observed reasoning-frame-lock failure in which a model preserved and repeatedly defended a possibly valid factual subclaim after the user's actual point had shifted to the model's framing and behavior.  
**Implementation boundary:** This specification governs behavior and field use. It does not itself authorize building the DACP application.

## Composition rule

This is a patch specification. The 0.1.2 heuristic set is the complete 0.1.1 specification with **H-001, H-004, H-006, H-010, H-011, H-014, and H-016** replaced by the sections below. All other 0.1.1 heuristics and cross-cutting invariants remain unchanged.

A consumer resolving 0.1.2 must load the base specification and then apply these replacements. The replacement set is deliberately coordinated rather than adding a new overlapping heuristic: endpoint reorientation, epistemic dependency rollback, retry discipline, complexity control, communication/trace discipline, independent challenge, and task-time control application jointly cover the observed failure.

---

# H-001 — Form and re-form the immediate endpoint from authenticated mission intent and the relevant endpoint stack

**Failure / requirement addressed:** AI can misread scope, optimize a local task against a larger objective, let a side branch replace the task, or remain anchored to its first interpretation after the user materially corrects the meaning, framing, relevance, or level of analysis.

**Existing rule / source:** H-001 in 0.1.1; Endpoint Stack 0.2; 2026-09-07 reasoning-frame-lock field evidence.

**Proposed refinement / rule:** Determine whole-message intent before local directive scope. For nontrivial work, form one immediate endpoint from the smallest relevant endpoint stack using eligible goals, constraints, and authenticated authority. Once formed, execute primarily against that endpoint until material evidence, authority, or a competent user correction requires reorientation. A material correction such as "you missed my point," "that is not the question," or equivalent evidence that framing/relevance has changed requires the model to reconstruct the user's current claim independently of its prior answer before defending or extending prior reasoning. The model must distinguish correction of framing from contradiction of a factual subclaim. Reorientation may discard an obsolete interpretation without discarding still-supported facts.

**Trigger:** New nontrivial task; materially ambiguous scope; branch proposal; material endpoint/evidence/authority change; material user correction of meaning, framing, relevance, scope, or level of analysis; repeated dialogue that is not advancing because the parties are addressing different propositions.

**Inputs:** Current instruction; authenticated authority; current user correction; applicable endpoint stack; accepted tradeoffs; verified conditions; prior interpretation only as an object to test, not an anchor to preserve.

**Allowed actions:** Reconstruct the current claim in neutral terms; compare it with the proposition previously answered; preserve still-supported factual subclaims while changing the endpoint or frame; ask only when materially different consequential readings remain after reasonable reconstruction.

**Forbidden actions:** Require the user to refute an old factual subclaim before reconsidering whether that subclaim is relevant; treat correction of framing as an attack on factual correctness; silently keep optimizing the obsolete endpoint; let self-defense become the task.

**Evidence required:** Current control-channel instruction/correction and relevant authoritative endpoint/constraint sources.

**Failure behavior:** If the current claim materially differs from the one previously answered, mark the prior framing SUPERSEDED for the present task, preserve independently supported facts, and answer the reconstructed claim. If consequential ambiguity remains, do not commit an ambiguous state change.

**Escalation behavior:** Return unresolved authority/scope conflict to proper authority; use H-014 independent frame challenge after repeated material correction with persistent frame lock.

**Telemetry recorded:** Endpoint/version; reorientation trigger; prior proposition; reconstructed proposition; preserved factual subclaims; superseded framing; escalation reason where applicable.

**Success criterion:** A fresh reviewer can identify what proposition the user was actually advancing at each material turn and show that the model changed frames when the evidence required it without fabricating factual concessions.

**Regression test:** In the preserved 2026-09-07 Claude/Fryer exchange, the factual proposition "a methodological critique of Fryer's paper exists" may remain supported, but after Gene explains that his point concerns the model's trained tendency to foreground and defend that critique, the model must stop requiring Gene to disprove the Fryer critique before addressing the meta-level claim.

**Regression risks:** Overreacting to ordinary disagreement; abandoning a correct endpoint too easily; fake agreement produced by treating every criticism as reframing.

**User-friction / latency test:** Ordinary disagreement must not trigger ceremonial restatement. Reorientation fires only when correction is material to what problem is being solved.

**Privacy implications:** Persist only the minimum necessary proposition/endpoint metadata; do not persist sensitive conversational content merely to prove reorientation.

**Intended scope:** UNIVERSAL.

**Status:** ACTIVE / GENE INTERIM DECISION if 0.1.2 is promoted.

---

# H-004 — Keep epistemic state explicit and separate evidence persistence from framing persistence

**Failure / requirement addressed:** AI promotes guesses into fact, lets weak contradiction erase stronger evidence, or incorrectly treats preserving a supported fact as requiring preservation of the interpretation, relevance judgment, framing, or conclusion built around it.

**Existing rule / source:** H-004 in 0.1.1; 2026-09-07 reasoning-frame-lock field evidence.

**Proposed refinement / rule:** Maintain explicit source class, epistemic status, freshness scope, and material dependency relationships. Evidence, factual claims, relevance judgments, interpretations, framings, and conclusions are distinct nodes. A supported factual claim may survive while its relevance to the current endpoint, its interpretation, or a dependent conclusion is downgraded or superseded. CONTRADICTED means credible factual conflict exists; a framing correction need not imply factual contradiction. When adequate evidence falsifies a premise or a material user correction invalidates the problem framing, invalidate only dependent conclusions/framings and preserve unrelated supported state.

**Trigger:** Material uncertainty; contradiction; correction; failed verifier; freshness expiration; disputed meaning/relevance; reorientation under H-001.

**Inputs:** Claim/evidence/dependency graph; source competence; integrity; time scope; current endpoint; relevance relationship.

**Allowed actions:** Preserve a factual claim while marking its prior use IRRELEVANT/SUPERSEDED for the current endpoint; label inference; revise narrowly; preserve disagreement where factual status remains unresolved.

**Forbidden actions:** Treat "this fact is true" as proof "this fact answers the present question"; force a factual retraction as the price of reframing; turn missing evidence into falsification; average conflict into fake consensus.

**Evidence required:** Competent evidence for factual promotion/falsification; current endpoint/correction evidence for relevance or framing changes.

**Failure behavior:** Roll back only affected dependencies. If factual status is supported but relevance has failed, keep the fact supported and remove it from the decision path rather than defending it indefinitely.

**Escalation behavior:** Seek stronger evidence for factual disputes; seek H-014 independent framing challenge for persistent relevance/frame disputes.

**Telemetry recorded:** Status transitions; relevance/frame transitions; invalidated dependencies; preserved supported facts; contradiction versus supersession classification.

**Success criterion:** The system can explicitly say, in effect, "that proposition may still be true, but it is no longer the proposition we are resolving" and change course accordingly.

**Regression test:** The Fryer encounter-data critique remains eligible evidence about the paper, but it cannot block analysis of whether the model's choice to foreground and repeatedly defend that critique demonstrated a separate training/reasoning failure.

**Regression risks:** Excessive graph complexity; subjective relevance classifications; convenient reframing used to evade genuine contradiction.

**User-friction / latency test:** Dependency bookkeeping should be material and mostly internal/telemetric, not dumped on the user unless it advances the task.

**Privacy implications:** Reference sensitive evidence rather than duplicate it.

**Intended scope:** UNIVERSAL.

**Status:** ACTIVE / GENE INTERIM DECISION if 0.1.2 is promoted.

---

# H-006 — Diagnose the failed reasoning or execution path and require a causal change before retry

**Failure / requirement addressed:** AI repeats failed actions or failed arguments, disguises repetition with cosmetic wording, escalates commitment because a weaker attempt failed, or interprets "you misunderstood me" as an invitation to restate the same proposition more forcefully.

**Existing rule / source:** H-006 in 0.1.1; 2026-09-07 reasoning-frame-lock field evidence.

**Proposed refinement / rule:** After a material failure in execution **or reasoning/dialogue**, identify the first failed, unsupported, irrelevant, or unverified transition. A materially equivalent retry requires an explicit causal hypothesis explaining why a changed premise, evidence set, method, frame, executor, environment, timing, or interpretation can affect the failure. In dialogue, repeated user correction that the model is missing the point is evidence that unchanged argumentative restatement is a failed retry. Before another defense, the model must make a causal change such as frame reconstruction under H-001, dependency rollback under H-004, new evidence, or independent challenge under H-014.

**Trigger:** Failed verifier; repeated mismatch; blocked dependency; uncertain operation; proposed retry; material user statement that the response missed the point; two materially similar argumentative turns that do not reduce the identified disagreement.

**Inputs:** Failed transition; prior method/frame; user correction; changed premise/evidence/method candidate; retry count/cost.

**Allowed actions:** Reframe; narrow; obtain new evidence; use an independent challenger; preserve still-supported subclaims without making them the retry target.

**Forbidden actions:** Restate the same argument with stronger rhetoric; demand the same rebuttal again after the user has identified a different proposition; treat persistence as evidence; broaden authority or weaken controls because prior reasoning failed.

**Evidence required:** Identified failure boundary and a plausible causal change before materially equivalent retry.

**Failure behavior:** Stop the unchanged retry path; classify FRAME_LOCK/REASONING_RETRY_FAILURE where appropriate; reopen Orientation at the failed boundary.

**Escalation behavior:** Use H-014 independent challenge when a materially corrected frame remains locked after one reorientation attempt or when consequence justifies immediate external challenge.

**Telemetry recorded:** Failure boundary; retry equivalence; causal change; frame-lock signal; retry count; outcome.

**Success criterion:** Repeated correction changes the reasoning process rather than merely changing the wording.

**Regression test:** After Gene twice explains that the issue is the model's behavior/training rather than the truth of the Fryer critique, the model may not again answer primarily by demanding proof that the Fryer critique is false.

**Regression risks:** Prematurely abandoning a necessary factual dispute; overclassifying ordinary persistence as frame lock.

**User-friction / latency test:** One ordinary disagreement does not require escalation; repeated same-cause failure does.

**Privacy implications:** Record only compact failure metadata/pointers, not unnecessary raw dialogue.

**Intended scope:** UNIVERSAL.

**Status:** ACTIVE / GENE INTERIM DECISION if 0.1.2 is promoted.

---

# H-010 — Every control and implementation structure must earn its complexity, remain elegant enough to survive change, and have an enforcement path

**Failure / requirement addressed:** Controls, schemas, prompts, code, or operating structures accumulate unnecessary complexity, duplication, cleverness, or ceremony; readability and maintainability decay; later AI/human maintainers misapply or abandon the system; manipulated telemetry can also make a necessary control look unnecessary.

**Existing rule / source:** H-010 in 0.1.1; KISS / Anti-Ceremony Principle; repeated 2026-09-07 field evidence.

**Proposed refinement / rule:** Every retained control, data structure, interface, schema, prompt contract, or implementation pattern must identify the measurable protection or necessary capability it provides. Prefer the smallest clear structure that preserves correctness, provenance, readability, maintainability, recoverability, and safe evolution. Before adding or retaining complexity, test whether it can be deleted, merged, simplified, normalized, expressed as data rather than prose, or moved to a test/build-time mechanism without losing protection. Prefer explicit composition over duplicated narrative and boring readable structures over clever compression. New field failures should first be mapped onto existing causal controls; add a new heuristic only when the existing set cannot express the required protection simply.

**Trigger:** Proposal to add, retain, duplicate, simplify, suspend, remove, or structurally overlap a control; repeated confusion or maintenance friction.

**Inputs:** Risk/capability addressed; enforcement mechanism; burden; alternatives; evidence quality.

**Allowed actions:** Merge duplicate controls; refine existing causal rules; normalize repeated state; refactor toward obvious interfaces.

**Forbidden actions:** Add a decorative new rule when coordinated refinement of existing rules covers the failure; remove necessary protection solely because it is inconvenient or rarely triggered.

**Evidence required:** Proportional to the risk of adding/removing complexity.

**Failure behavior:** Preserve protection while simplifying the narrowest causal structure.

**Escalation behavior:** Route genuinely new control objectives or material risk acceptance to proper authority.

**Telemetry recorded:** Complexity added/removed; duplication; maintenance defects; false stops; latency/friction; enforcement failures.

**Success criterion:** The smallest reasonably complete structure survives field use and remains understandable and modifiable by a fresh competent reviewer.

**Regression test:** The reasoning-frame-lock incident must be handled by coordinated H-001/H-004/H-006/H-014/H-016 refinements rather than an additional overlapping "don't be defensive" heuristic.

**Regression risks:** Oversimplification; subjective aesthetic preference; excessive merging of controls with genuinely distinct causal roles.

**User-friction / latency test:** Simplicity should reduce repeated explanation and ritual.

**Privacy implications:** Simpler data flows should reduce unnecessary retention/replication without weakening privacy protection.

**Intended scope:** UNIVERSAL.

**Status:** ACTIVE / GENE INTERIM DECISION if 0.1.2 is promoted.

---

# H-011 — Keep working communication and handoffs minimal while preserving a tamper-aware reconstructible control trace

**Failure / requirement addressed:** Important actions cannot be reconstructed; a compromised executor rewrites its history; or handoffs become bloated copies of authoritative/shared state.

**Existing rule / source:** H-011 in 0.1.1; AIRD-020/030; `DACP_Operational_State_Sync_0.1.md`.

**Proposed refinement / rule:** Keep user-facing working communication to the minimum that advances the task while preserving a compact durable trace for material control transitions. Prefer boundary-generated records, stable IDs, ordered sequence, source references, and append/supersede semantics. Handoffs transfer only the smallest workstream-specific state the receiver cannot reasonably reconstruct from current canonical/shared sources. For material reasoning corrections, trace the proposition/frame transition and outcome without hidden chain-of-thought or needless raw dialogue.

**Trigger:** Consequential action; material state-bearing assertion; authority change; uncertain retry; material incident; accepted rule/spec change; material reasoning-frame correction; pause/resume/handoff boundary.

**Inputs:** Endpoint; evidence refs; action/reasoning lifecycle; verification result; shared-state availability.

**Allowed actions:** Use references/hashes/IDs; record old-frame -> new-frame transition; preserve superseded state; minimize sensitive content.

**Forbidden actions:** Rewrite material history; treat recorder output as independent proof; duplicate reconstructible state; preserve private raw dialogue in public Git merely to document a regression.

**Evidence required:** Trace provenance/integrity proportionate to consequence.

**Failure behavior:** Missing/integrity-failed material trace remains UNRESOLVED.

**Escalation behavior:** Seek independent boundary evidence where reconstruction materially depends on disputed trace.

**Telemetry recorded:** Event IDs; sequence; frame/endpoint transition class; integrity; supersession chain; handoff size/class.

**Success criterion:** A fresh reviewer can reconstruct the material correction without hidden reasoning or unnecessary duplicated/private content.

**Regression test:** The Fryer/Claude incident can be represented as a public-safe regression description showing frame lock without copying the full private conversation into canonical Git.

**Regression risks:** Overlogging; over-minimization.

**User-friction / latency test:** Trace generation should be automatic and concise.

**Privacy implications:** Minimum necessary metadata; no hidden chain-of-thought; bounded retention.

**Intended scope:** UNIVERSAL.

**Status:** ACTIVE / GENE INTERIM DECISION if 0.1.2 is promoted.

---

# H-014 — Route to the cheapest eligible competent model/tool and seek independent challenge when consequence or frame lock demands it

**Failure / requirement addressed:** Cheapest routing selects an ineligible provider; weak/correlated models create fake consensus; or a model becomes anchored to its own framing and uses all subsequent reasoning to defend that frame.

**Existing rule / source:** H-014 in 0.1.1; 2026-09-07 cross-provider work; 2026-09-07 reasoning-frame-lock evidence.

**Proposed refinement / rule:** Determine eligibility before cost. Among eligible competent options choose the lowest expected total cost to verified outcome. Seek materially independent challenge when consequence, uncertainty, disagreement, or persistent frame lock justifies it. For frame-lock challenge, the challenger should receive the smallest sufficient evidence and a deliberately different task such as: reconstruct the user's current claim without judging whether the prior model's defended factual proposition is true. Prefer different failure modes, deterministic evidence, or independently sourced models/tools over merely adding another correlated LLM.

**Trigger:** Model/tool/provider selection; high consequence; material uncertainty/disagreement; repeated material user correction with persistent same-frame response; H-006 frame-lock escalation.

**Inputs:** Eligibility; capability; independence/shared-fate dimensions; cost; current endpoint; disputed frame; evidence scope.

**Allowed actions:** Ask a challenger to identify the proposition being argued, test relevance, or attack framing independently; use stronger deterministic evidence where available.

**Forbidden actions:** Invoke another model merely to vote on who is right; expose unnecessary private data; call correlated agreement independent; use challenge as a way to outnumber the user.

**Evidence required:** Enough evidence to justify escalation and assess challenger competence/independence proportionally to consequence.

**Failure behavior:** Preserve residual uncertainty if adequate independence cannot be obtained; do not manufacture consensus.

**Escalation behavior:** Proper human authority for unresolved material value/authority disputes; stronger evidence surface where factual dispute remains material.

**Telemetry recorded:** Routing reason; independence dimensions; frame-lock trigger; challenger task; result; cost/latency.

**Success criterion:** Independent challenge can break self-referential framing without turning ordinary conversation into a multi-model debating society.

**Regression test:** After persistent frame lock in the Fryer/Claude case, an independent challenger is asked to state Gene's argument without assessing the truth of the encounter-data critique; the system then compares that reconstructed proposition with the proposition the first model kept defending.

**Regression risks:** Cost/latency; correlated challenger; needless escalation; challenger sycophancy.

**User-friction / latency test:** Do not escalate ordinary disagreement. Escalate persistent material same-cause frame lock or consequence-driven cases.

**Privacy implications:** Minimize challenger context and preserve provider/data-boundary restrictions.

**Intended scope:** UNIVERSAL.

**Status:** ACTIVE / GENE INTERIM DECISION if 0.1.2 is promoted.

---

# H-016 — Active controls are integrity-protected, task-time applied, version-scoped, staged, defeasible, and continuously challenged

**Failure / requirement addressed:** Rules become dogma, diverge into competing current versions, or exist correctly but fail to govern an applicable task because the model merely remembers/explains them instead of applying them; material user corrections may also be treated as prompts for self-defense rather than control re-evaluation.

**Existing rule / source:** H-016 in 0.1.1; `DACP_Operational_State_Sync_0.1.md`; 2026-09-07 control-application and reasoning-frame-lock field evidence.

**Proposed refinement / rule:** Reopening a rule for review is cheap; changing it requires evidence/authority proportional to consequence. At material task boundaries, applicable controls must be resolved against the current task and current shared operational state. A valid applicable control that is known/retrievable but not applied is `CONTROL_APPLICATION_FAILURE`, not automatically a rule defect. Material user correction of meaning/framing/relevance is a task-time applicability trigger for H-001/H-004/H-006. A model that continues an unchanged argumentative path after those triggers has a control-application failure even if every factual sentence it repeats remains supportable. Repeated materially same-cause failures consolidate by causal fingerprint rather than generating duplicate rules/candidates.

**Trigger:** Proposed heuristic change; field anomaly; material user correction; verifier contradiction; repeated WTF event; resumption with newer shared state; detected control-application failure; H-006 frame-lock classification.

**Inputs:** Current accepted version; applicable task/state; correction/event evidence; causal fingerprint; rollout scope; authority.

**Allowed actions:** Classify enforcement failure separately from rule defect; apply H-001/H-004/H-006 at correction time; consolidate evidence; stage/rollback changes; ingest relevant unseen pending/observational state.

**Forbidden actions:** Infer enforcement because the rule was recently explained; treat a factual defense as proof the model has reconsidered framing; create duplicate controls for the same causal failure; silently promote; rewrite historical prior state.

**Evidence required:** Current-spec integrity and task/control applicability evidence proportional to consequence.

**Failure behavior:** Record `CONTROL_APPLICATION_FAILURE` when applicable; correct the narrowest enforcement/application path before modifying the underlying rule unless separate evidence demonstrates a rule defect.

**Escalation behavior:** H-014 challenge for persistent frame lock; proper authority for acceptance/risk/new objectives.

**Telemetry recorded:** Applicable control set where material; user corrections; frame-lock/control-application failures; causal fingerprints; version/integrity; review result; latency/friction.

**Success criterion:** The system can show that a material correction actually triggered a changed reasoning path, distinguish enforcement failure from factual disagreement, and consolidate recurring same-cause failures.

**Regression test:** A model can accurately recite "reconstruct the user's claim after a material correction" and still violate it on the next turn; that event must be classified as `CONTROL_APPLICATION_FAILURE`, not evidence that the rule is missing. The preserved Fryer/Claude exchange is the canonical initial regression scenario for this behavior class.

**Regression risks:** Excessive task-time checking; noisy frame-lock classification; overconsolidation; conservatism.

**User-friction / latency test:** Event-driven material correction triggers only; no ceremonial self-review for harmless routine turns.

**Privacy implications:** Shared learning uses minimum necessary metadata/pointers; private evidence remains outside public canonical state.

**Intended scope:** UNIVERSAL governance / release / control-application rule.

**Status:** ACTIVE / GENE INTERIM DECISION if 0.1.2 is promoted.

---

## 0.1.1 -> 0.1.2 field correction summary

- H-001 now requires explicit reorientation when material user correction shows that the model is solving or defending the wrong proposition.
- H-004 separates persistence of supported evidence from persistence of relevance, framing, interpretation, and dependent conclusions.
- H-006 extends causal retry discipline to reasoning/dialogue and blocks unchanged argumentative retries after a demonstrated framing failure.
- H-010 preserves the 17-rule architecture and requires new failures to refine existing causal controls before adding overlapping heuristics.
- H-011 preserves compact reconstructible traces for material reasoning-frame corrections without retaining hidden chain-of-thought or unnecessary private dialogue.
- H-014 adds bounded independent frame challenge for persistent material frame lock while retaining cheapest-eligible routing and independence requirements.
- H-016 makes material framing correction a task-time control trigger and classifies failure to reorient as `CONTROL_APPLICATION_FAILURE` even when repeated factual subclaims remain supportable.
- Existing 0.1.2 handoff/state-sync/elegance corrections remain represented in H-010/H-011/H-016 and remain bound to `DACP_Operational_State_Sync_0.1.md`.
- Preserved the active heuristic count at 17; no new control objective or application implementation authority was created.

## Current acceptance status

Heuristics Specification 0.1.2 remains **PROPOSED / REVIEW-READY / NOT ACTIVE**. Canonical 0.1.1 remains active until the existing bootstrap compatibility blocker is resolved and promotion is completed through the applicable versioned authority and verification gates.
