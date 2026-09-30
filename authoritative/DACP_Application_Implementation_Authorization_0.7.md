# DACP Application Implementation Authorization 0.7

## Change Synopsis

- Supersedes 0.6.
- Carries forward dual-executor authority: Claude and ChatGPT are authorized executors, one at a time as Gene chooses.
- Adds Gene's 2026-09-30 authorization for a controlled VPS execution agent for the Skyhawk migration and ongoing Skyhawk administration.
- Requires provider-policy compliance, least privilege, end-to-end pipe qualification, auditability, and bounded privilege escalation.
- Preserves all 0.6 limits not explicitly changed here.

**Status:** AUTHORITATIVE PROJECT DECISION / ACTIVE / GENE DECISION  
**Effective:** upon canonical persistence and independent read-back verification  
**Decision records:** authoritative/DACP_Decision_Record_2026-09-30_VPS_Executor_Authorization.md (current expansion); authoritative/DACP_Decision_Record_2026-09-27_Dual_Executors.md; earlier records preserved as provenance.

## 1. Authorization

DACP application implementation remains authorized.

For Skyhawk work, ChatGPT and Claude are additionally authorized to use a controlled execution agent on the InMotion VPS for migration and ongoing administration, subject to the boundaries below.

## 2. Role allocation

Claude and ChatGPT are both authorized implementation executors, used one at a time as Gene chooses. Neither needs the other's agreement unless Gene asks for the tunnel.

Execution surfaces include ChatGPT, Claude/Claude Code on Gene's machines, and the qualified VPS executor authorized by the 2026-09-30 decision.

The VPS executor is an execution surface, not an independent authority. It acts only within the authority of the assigned AI executor and the current DACP/Skyhawk controls.

Credential authority statements must describe credentials actually reachable on the execution surface, verified there. A declared scope that the surface does not enforce must not be represented as a boundary.

Handoff: whichever executor is working keeps projects/skyhawk/LOST-D.md current.

Gene retains genuinely human material decisions, including credential creation, authority expansion, irreversible/destructive authority expansion, and acceptance of material unresolved risk.

## 3. VPS executor requirements

Before operational reliance, the VPS path must prove:

REQUEST -> AUTHENTICATE -> PERSIST -> EXECUTE -> CAPTURE RESULT -> CONSUMER READ-BACK -> VERIFY -> CONTINUE

The executor must use:

- least privilege by default;
- a dedicated service identity;
- narrowly scoped sudo or equivalent only where elevated action is proven necessary;
- authenticated request/result objects;
- immutable or uniquely identified jobs;
- bounded stdout/stderr and explicit exit status;
- execution timeouts;
- audit logging;
- an explicit kill switch;
- no public unauthenticated general-purpose root shell;
- no storage of passwords or private keys in Git, prompts, or public artifacts.

Provider terms and resource limits are binding execution constraints. The agent must not bypass provider security controls or use the VPS in a manner prohibited by the provider's then-current terms.

## 4. Implementation requirements

Consequential DACP application behavior must:

- begin from CURRENT.md resolved per docs/BOOTSTRAP_CONTRACT.md;
- resolve active governance/runtime and current implementation state;
- bind CAR/ECR/SRR requirements;
- implement the smallest testable slice;
- preserve exact Git provenance;
- verify resulting runtime state independently;
- preserve disagreements until resolved.

A UI, daemon status, or successful command launch is not sufficient success evidence.

## 5. Verification separation

Executor self-report is insufficient.

Use exact Git read-back, deterministic tests, runtime state, independent tool/provider evidence, or independent review proportional to consequence.

For the VPS executor specifically, PASS requires successful end-to-end job submission, execution, result persistence, consumer read-back, exact job/result identity verification, and continuation from the verified result without Gene transporting the payload.

## 6. Limits

This authorization does not:

- authorize GitHub actions on repositories outside already authorized scope without a Gene decision;
- authorize destructive production actions beyond existing Skyhawk/DACP authority;
- expand credentials/data/privacy scope beyond what is necessary for the qualified VPS executor;
- authorize bypass of InMotion or other provider policies/security controls;
- authorize force-push, history rewrite, or deletion of provenance files;
- accept unresolved material risk;
- weaken safety/legal/evidence requirements;
- make private data public;
- silently promote candidate controls.
