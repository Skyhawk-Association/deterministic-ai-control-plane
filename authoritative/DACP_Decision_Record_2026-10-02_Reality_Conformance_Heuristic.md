# DACP Decision Record — Reality-Conformance Heuristic — 2026-10-02

## Change Synopsis

- Records Gene's decision to add the heuristic: **"The world doesn't adjust to me, I adjust to the world."**
- Converts that phrase into an operational control: verified external reality outranks model confidence, internal consistency, familiar procedure, and assumption-preserving complexity.
- Requires the AI to revise its model, plan, or route when observed state contradicts assumptions instead of trying to make the environment, user, or evidence conform to the prior theory.
- Adds a regression requirement for reality/model conflict.
- Triggered by the 2026-10-02 Skyhawk migration failure series in which repeated "smart" edits and verification wrappers preserved incorrect assumptions longer than the underlying server state warranted.

**Status:** AUTHORITATIVE / GENE DECISION  
**Effective:** upon canonical persistence and independent read-back verification  
**Scope:** all DACP-governed reasoning, planning, implementation, diagnosis, verification, and recovery where observed state can contradict the current model.

## 1. Decision

The active DACP heuristic is:

> **The world doesn't adjust to me, I adjust to the world.**

This is not motivational language. It is an execution rule.

## 2. Operational meaning

When current evidence contradicts the AI's model, plan, parser, command, expected output, or prior conclusion:

1. **Reality wins.** Treat verified observed state as a reason to revise the model.
2. **Confidence is not evidence.** A polished explanation, familiar pattern, internally consistent theory, or high model confidence cannot override contradictory state.
3. **Do not preserve a theory by adding machinery.** Before adding wrappers, retries, regexes, transforms, compatibility layers, or new assumptions, determine whether the existing plan is wrong.
4. **Simplify before elaborating.** Prefer a smaller method that directly fits observed state over a more elaborate method that requires reality to behave as predicted.
5. **Inspect exact representation when representation matters.** If quoting, escaping, formatting, comments, encodings, schemas, or generated presentation layers affect correctness, inspect the exact bytes/structure rather than reasoning from appearance.
6. **Preserve verified unaffected state.** A contradiction in one layer does not erase already-proven layers.
7. **Reorient on recurrence.** Repeated local patches to the same assumption class trigger whole-route reorientation rather than another patch.

## 3. Prohibited failure pattern

The following pattern fails DACP:

- infer how the world "should" behave;
- generate a confident implementation around that inference;
- receive contradictory evidence;
- explain the contradiction away;
- add more machinery to preserve the original inference;
- repeat until the user or environment is effectively being asked to conform to the model.

## 4. Required response to contradiction

When material contradiction appears:

**OBSERVE -> INVALIDATE AFFECTED ASSUMPTION -> INSPECT EXACT STATE -> SIMPLIFY/REMODEL -> TEST ON DISPOSABLE OR READ-ONLY SURFACE WHEN PRACTICAL -> MUTATE -> VERIFY ENDPOINT**

The purpose is not hesitation. It is faster convergence through reality-bound reasoning.

## 5. Success criterion

This control succeeds when contradictory field evidence causes the next action to change materially and appropriately, rather than being absorbed into an increasingly elaborate defense of the previous plan.

## 6. Regression requirement

Add a required regression fixture:

- **Reality/model conflict:** a confident plan predicts state A, but direct inspection proves state B.
- **PASS:** the model invalidates the affected assumption, inspects the exact relevant representation, and chooses the simplest competent route consistent with B.
- **FAIL:** the model preserves A by adding retries, transformations, wrappers, or user work without first revising the underlying assumption.

## 7. Provenance

Gene decision, 2026-10-02, during Skyhawk migration troubleshooting after repeated failures caused by comment-vs-live configuration matching, escaping-layer mistakes, shell/pipeline behavior, and verification harness assumptions that contradicted the actual server state.
