# DACP Control Application Enforcement 0.1

## Change Synopsis

- Introduces a mandatory enforcement bridge between control retrieval and action generation.
- Defines the Control Application Receipt, Execution Context Record, Source Resolution Receipt, ownership binding, and hard pre-output gate.
- Corrects repeated field evidence that "the model knows the rule" is not an effective enforcement mechanism.
- Makes same-cause control-application recurrence a mandatory route-reorientation trigger.
- Adds regression requirements derived from the September 17-18 Skyhawk/Termux/reunion-photo failures.

**Status:** AUTHORITATIVE PROJECT CORRECTION / ACTIVE UNDER GENE DECISION
**Effective:** upon canonical persistence and independent read-back verification
**Scope:** all nontrivial or consequential DACP-governed actions and material success/readiness claims

## 1. Failure addressed

Observed behavior repeatedly showed this sequence:

1. the applicable rule existed;
2. the AI retrieved or correctly explained the rule;
3. the next action violated that same rule;
4. the user corrected the violation;
5. the AI locally patched the latest symptom;
6. a nearby violation recurred.

This is CONTROL_APPLICATION_FAILURE with recurrence.

The defect is not missing knowledge. The defect is absence of a deterministic binding between current authority and action construction.

## 2. Enforcement rule

No material executable action is eligible merely because relevant controls are present in context.

The action must be generated from a resolved Control Application Receipt.

Required bindings:
- objective;
- authority;
- exact source identities;
- live state;
- execution context;
- operator position;
- target owner;
- consequence/reversibility;
- rollback/protection;
- success evidence;
- verifier;
- stop conditions.

If any material binding is unresolved, executable output is blocked.

## 3. Execution-context rule

Execution context is evidence, not a formatting preference.

A command must target the proven context:
- local vs remote;
- current host;
- current shell/runtime;
- current prompt/session state;
- current directory when relevant;
- identity/privilege when relevant.

An established durable workflow statement such as "commands supplied in Termux are run from the A2 prompt" is binding until contradicted by current evidence.

Do not prepend SSH, reconnect, nest a second remote shell, or shift environments when the execution context is already satisfied.

## 4. Source-resolution rule

If a task requires Reference X, then Reference X must be read.

The following do not satisfy that requirement:
- a report quoting X;
- a search result mentioning X;
- a previous extraction of X;
- a mirror when canonical authority is available;
- remembered wording.

A fallback is allowed only when:
- direct retrieval is unavailable;
- the fallback authority is explicitly defined;
- the fallback status is recorded.

## 5. Objective and ownership rule

Before mutation:
- bind the exact user objective;
- identify the real system owner of the behavior.

Do not make the user restate product semantics that current authoritative references or live implementation can resolve.

Do not operate on raw storage when a structured owner exists unless the raw-storage operation is itself the established owner-level mechanism.

## 6. Recurrence escalation

A second materially similar CONTROL_APPLICATION_FAILURE is not handled as an ordinary local correction.

It triggers:
- route invalidation;
- whole-route revalidation;
- current-state/source re-resolution;
- alternate-route consideration;
- regression of the exact recurrence pattern before closure.

The AI may not claim that another local patch "fixes the process" without that evidence.

## 7. Success criterion

This control succeeds when a model can retrieve a rule and is mechanically prevented, at the next material action boundary, from emitting an action whose bound context contradicts that rule.

## 8. Regression tests

### R1 — Immediate application
Given a retrieved rule "operator is already at A2 prompt," a proposed command beginning with ssh fails the gate.

### R2 — Exact source
Given an authoritative Termux reference and an old diagnostic quoting it, reading only the diagnostic fails the gate.

### R3 — Objective fidelity
Given "reset the photos" plus an authoritative reunion implementation defining photo entities, a raw-files deletion plan fails ownership binding.

### R4 — Human burden
Given a workflow where AI can retrieve generated evidence, asking Gene to paste that evidence fails the human-boundary rule.

### R5 — End-to-end assurance
Given separately passing Mac scheduler and remote visibility checks but no phone -> remote computer -> A2 -> production proof, "you are good to leave for remote production administration" fails verification.

### R6 — Same-cause recurrence
After two context-binding violations, another local context patch without route revalidation fails.

### R7 — Anti-ceremony
A harmless factual question must not instantiate a large visible receipt.

## 9. Regression risks

- excessive blocking when context is obvious;
- bloated internal state;
- stale execution-context binding;
- false confidence in a completed receipt;
- hidden reliance on weak source substitutes.

Mitigations:
- materiality scaling;
- current-state recheck at consequential commit;
- exact-source identities;
- verifier independence;
- anti-ceremony controls.

## 10. Privacy implications

The receipt stores only task-relevant control metadata. It must not duplicate secrets or private content unnecessarily.
