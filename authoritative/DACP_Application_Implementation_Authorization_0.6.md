# DACP Application Implementation Authorization 0.6

## Change Synopsis

- Supersedes 0.5.
- Claude and ChatGPT are both authorized executors, used one at a time as Gene chooses (Gene decision 2026-09-27). This replaces 0.5's retirement of ChatGPT.
- Shared state for handoff: LOST-D in Git (projects/skyhawk/LOST-D.md), kept current by whichever executor is working.
- All other provisions of 0.5 carried forward unchanged.

**Status:** AUTHORITATIVE PROJECT DECISION / ACTIVE / GENE DECISION
**Effective:** upon canonical persistence and independent read-back verification
**Decision records:** authoritative/DACP_Decision_Record_2026-09-27_Dual_Executors.md (current); authoritative/DACP_Decision_Record_2026-09-23_Executor_Transfer.md and authoritative/DACP_Decision_Record_2026-09-23_Credential_Scope_Correction.md (provenance)

## 1. Authorization

DACP application implementation remains authorized.

## 2. Role allocation

Claude and ChatGPT are both authorized implementation executors, used one at a time as Gene chooses. Each may plan, write and change the projects it is used on. Neither needs the other's agreement unless Gene asks for the tunnel (one AI checking the other).

Execution surfaces: claude.ai and Claude Code on Gene's machines; ChatGPT. Commands on the Skyhawk A2 server are run by Gene at the A2 prompt; A2 pushes Git with the existing `github-skyhawk` SSH identity (account geneatwell). Organization deploy keys are disabled.

Credential authority statements must describe credentials actually reachable on the execution surface, verified there. A declared scope that the surface does not enforce must not be represented as a boundary.

Handoff: whichever executor is working keeps projects/skyhawk/LOST-D.md current, as required by the "Shared passdown" rule in projects/skyhawk/RULES.md, so the other executor can continue from it without reconstruction.

Gene retains genuinely human material decisions, including credential creation and any expansion of authority.

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
- authorize GitHub actions on any repository other than this one without a Gene decision for that task (skyhawk.org work is governed by projects/skyhawk/RULES.md);
- give either AI direct access to the Skyhawk production server or any other system (production commands are run by Gene);
- expand credentials/data/privacy scope beyond the above;
- authorize destructive production actions beyond existing authority;
- authorize force-push, history rewrite, or deletion of provenance files;
- accept unresolved material risk;
- weaken safety/legal/evidence requirements;
- make private data public;
- silently promote candidate controls.
