# DACP Application Implementation Authorization 0.4

## Change Synopsis

- Supersedes 0.3.
- Claude becomes primary implementation executor; ChatGPT is retired from DACP (Gene decision 2026-09-23).
- Grants repository-scoped Git write via a Gene-held fine-grained token.
- Updates governing reference to Project Instructions 0.6.
- All other requirements and limits carried forward from 0.3 unchanged.

**Status:** AUTHORITATIVE PROJECT DECISION / ACTIVE / GENE DECISION
**Effective:** upon canonical persistence and independent read-back verification
**Decision record:** authoritative/DACP_Decision_Record_2026-09-23_Executor_Transfer.md

## 1. Authorization

DACP application implementation remains authorized.

## 2. Role allocation

Claude is the primary implementation executor. Primary execution surface for repository work: Claude Code on Gene's machine, authenticated with a fine-grained token scoped to Skyhawk-Association/deterministic-ai-control-plane only (Contents read/write, Metadata read).

ChatGPT is retired from DACP. Its prior work remains provenance.

Gene retains genuinely human material decisions, including credential creation and any expansion of authority beyond this repository.

## 3. Implementation requirements

Consequential DACP application behavior must:
- begin from CURRENT.md, resolved per docs/BOOTSTRAP_CONTRACT.md;
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

Use exact Git readback (fresh clone, commit SHA, blob SHA), deterministic tests, runtime state, independent tool/provider evidence, or independent review proportional to consequence.

## 5. Limits

This authorization does not:
- grant GitHub scope beyond this repository;
- grant access to the Skyhawk production server or any other system;
- expand credentials/data/privacy scope beyond the above;
- authorize destructive production actions beyond existing authority;
- authorize force-push, history rewrite, or deletion of provenance files;
- accept unresolved material risk;
- weaken safety/legal/evidence requirements;
- make private data public;
- silently promote candidate controls.
