# DACP Application Implementation Authorization 0.5

## Change Synopsis

- Supersedes 0.4.
- Corrects the credential model: Claude Code uses Gene's existing GitHub credentials on Gene's machine; authority is policy-bounded, not token-scoped (Gene decision 2026-09-23, credential scope correction).
- Adds: credential authority statements must match credentials actually reachable on the execution surface.
- All other provisions of 0.4 carried forward unchanged.

**Status:** AUTHORITATIVE PROJECT DECISION / ACTIVE / GENE DECISION
**Effective:** upon canonical persistence and independent read-back verification
**Decision records:** authoritative/DACP_Decision_Record_2026-09-23_Executor_Transfer.md; authoritative/DACP_Decision_Record_2026-09-23_Credential_Scope_Correction.md

## 1. Authorization

DACP application implementation remains authorized.

## 2. Role allocation

Claude is the primary implementation executor. Primary execution surface for repository work: Claude Code on Gene's machine, running as Gene's Windows user with Gene's existing GitHub credentials.

Claude's GitHub authority is bounded by policy, not by credential scope: the limits in section 5, plus Claude Code per-command approval by Gene. Claude acts only on Skyhawk-Association/deterministic-ai-control-plane unless Gene decides otherwise for a defined task.

Credential authority statements must describe credentials actually reachable on the execution surface, verified there. A declared scope that the surface does not enforce must not be represented as a boundary.

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
- authorize GitHub actions on any repository other than this one without a Gene decision for that task;
- grant access to the Skyhawk production server or any other system;
- expand credentials/data/privacy scope beyond the above;
- authorize destructive production actions beyond existing authority;
- authorize force-push, history rewrite, or deletion of provenance files;
- accept unresolved material risk;
- weaken safety/legal/evidence requirements;
- make private data public;
- silently promote candidate controls.
