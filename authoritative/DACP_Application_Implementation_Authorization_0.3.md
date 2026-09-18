# DACP Application Implementation Authorization 0.3

## Change Synopsis

- Supersedes 0.2.
- Updates governing references to Project Instructions 0.5 and Delta.
- Preserves ChatGPT as primary implementation executor and Claude as optional, non-critical-path independent model.
- Requires application slices that enforce DACP to consume the active CAR/ECR/SRR contracts rather than rely on conversational awareness.
- Preserves Gene's material decision authority and existing permission/privacy limits.

**Status:** AUTHORITATIVE PROJECT DECISION / ACTIVE / GENE DECISION
**Effective:** upon canonical persistence and independent read-back verification

## 1. Authorization

DACP application implementation remains authorized.

## 2. Role allocation

ChatGPT is the primary implementation executor.

Claude may be used for independent challenge/review when useful but is not a standing approval gate and is not on the critical implementation path.

Gene retains genuinely human material decisions.

## 3. Implementation requirements

Consequential DACP application behavior must:
- begin from CURRENT.md;
- resolve active governance/runtime;
- resolve current implementation state deterministically;
- implement the smallest testable slice;
- preserve exact Git provenance;
- verify resulting runtime state;
- preserve disagreements until resolved.

Any application slice responsible for action gating must expose or internally enforce the active CAR/ECR/SRR contracts.

A UI showing a rule or status is not evidence that the rule is applied.

## 4. Verification separation

Executor self-report is insufficient for consequential implementation claims.

Use exact Git readback, deterministic tests, runtime state, independent tool/provider evidence, or independent review proportional to consequence.

## 5. Limits

This authorization does not:
- expand credentials/data/privacy scope;
- authorize destructive production actions beyond existing authority;
- accept unresolved material risk;
- weaken safety/legal/evidence requirements;
- make private data public;
- silently promote candidate controls.
