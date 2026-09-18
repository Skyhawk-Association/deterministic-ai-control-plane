# DACP Operational Use and Correction Authority 0.2

## Change Synopsis

- Supersedes 0.1.
- Preserves standing authority for evidence-forced corrections that do not change project endpoints or expand authority.
- Explicitly authorizes corpus-wide enforcement correction when repeated same-cause CONTROL_APPLICATION_FAILURE demonstrates that the active control architecture is not applying its own rules.
- Requires regression of the demonstrated failure pattern before activation.
- Prohibits treating reviewer agreement as sufficient evidence when both models fail the same operational case.

**Status:** AUTHORITATIVE PROJECT DECISION / ACTIVE / GENE DECISION
**Effective:** upon canonical persistence and independent read-back verification

## 1. Active posture

Use the active runtime in real work and attack it through evidence.

A valid control remains governing until superseded, but evidence that the control architecture cannot reliably apply valid controls is a specification-level defect.

## 2. Standing delegated correction authority

The AI may perform immediate versioned corrections without another approval loop when:
- current evidence directly demonstrates a material defect;
- correction preserves accepted objective and authority;
- correction does not weaken higher safety/privacy/legal/evidence constraints;
- required change fields are recorded;
- prior state is preserved;
- regression covers the demonstrated failure;
- corrected state is persisted and independently read back.

## 3. Corpus-level correction trigger

A corpus-level correction is authorized when:
- the same causal control-application failure recurs across multiple turns/actions;
- the failure survives explicit rereading of the relevant rules;
- local rule additions/patches have not prevented recurrence;
- the defect therefore concerns enforcement architecture rather than missing wording.

In that case, "correct the narrowest causal point" may mean replacing the runtime enforcement bridge rather than adding another isolated rule.

## 4. Human decisions still reserved to Gene

Explicit Gene decision remains required for:
- project endpoint changes;
- decision-governance changes;
- expanded permissions or irreversible authority;
- weakening safety/privacy/legal/evidence requirements;
- new material control objectives;
- acceptance of material unresolved risk.

## 5. Reviewer limits

Independent model review is evidence, not authority.

If ChatGPT and Claude agree on a design but field evidence later shows both missed the same defect, agreement does not protect the design from replacement.

Operational evidence outranks reviewer consensus on whether the mechanism actually works.

## 6. Lifecycle

OBSERVED -> EVIDENCE CHECK -> CAUSAL DIAGNOSIS -> VERSIONED CORRECTION -> REGRESSION -> PERSISTED -> READ-BACK VERIFIED -> ACTIVE

If regression is absent, the correction remains candidate even if prose appears convincing.

## 7. Anti-ceremony

Correction should reduce future burden. Do not respond to enforcement failure by merely adding more prose that still relies on the model remembering to obey it.
