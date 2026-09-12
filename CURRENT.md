# DACP Current Bootstrap

**Canonical migration status:** ACTIVE GIT CANONICAL  
**Repository:** `Skyhawk-Association/deterministic-ai-control-plane`  
**Default branch:** `main`  
**Current specification:** `authoritative/DACP_Heuristics_Specification_0.1.1.md`  
**Specification version:** `0.1.1`  
**Specification status:** AUTHORITATIVE / ACTIVE / GENE INTERIM DECISION  
**Active heuristic count:** 17  
**Verified specification Git blob:** `b16d80c55da9c35e57801dd8574bc09ddb4249de`

## Load order before consequential DACP work

1. `authoritative/Project Instructions 0.3.txt`
2. `authoritative/DACP_Heuristics_Specification_0.1.1.md`
3. `authoritative/DACP_Operational_State_Sync_0.1.md`
4. `STATE_LOCATOR.json`
5. `authoritative/DACP_Interim_Decision_Authority_0.2.md`
6. `authoritative/DACP_Operational_Use_and_Correction_Authority_0.1.md`
7. `authoritative/DACP_Endpoint_Stack_0.2.md`
8. `authoritative/DACP_Application_Implementation_Authorization_0.2.md` when application implementation or executor/reviewer role allocation is germane.
9. `authoritative/DACP_Governance_Supersession_Notice_0.3.md` when smoke-test/supersession history matters.

## Operational state

`STATE_LOCATOR.json` identifies the current shared private operational-state surface. Current private state is generation 32 on the verified Google Drive local-sync surface, with independent authenticated Drive connector readback. Gmail generation 31 is retained only as a recovery fallback. For nontrivial or consequential DACP work, resolve the relevant current private state when authorized and available. Pending/candidate and raw/observational state do not become canonical merely by being present.

Current review-ready heuristic patch: `authoritative/DACP_Heuristics_Specification_0.1.3.md` is **PROPOSED / NOT ACTIVE**. Canonical 0.1.1 remains governing until version promotion is completed through the applicable authority and compatibility gates. `authoritative/DACP_Heuristics_Specification_0.1.2.md` remains preserved as the immediate predecessor proposal.

## Application implementation status

Application implementation is explicitly authorized through `authoritative/DACP_Application_Implementation_Authorization_0.2.md`. ChatGPT is the primary DACP application implementation executor. Claude is removed from the critical implementation path and may be used only as an optional independent model when useful. Gene retains genuinely human material decisions under the governing authority.

The first accepted application implementation slice is now merged to canonical `main`: **local single-resource resolved commitment**. The merge commit that introduced the accepted prototype is `33b39ec4bd3fabdb15a2de3227dbbbff4fa62e18`; the accepted prototype branch head was `afb06b361b0d3de805c68b7e8d14504d4f01f525`. Cross-platform acceptance passed on Windows and Ubuntu. The accepted scope includes provider-free deterministic resolved commitment, separate authority binding, preexisting-state no-dispatch completion, durable dispatch-intent journaling, restart reconciliation without blind redispatch, request-mismatch blocking, and interprocess serialization with lock contention failing `PENDING` without dispatch. This is not a claim of production authentication, distributed consensus/locking, multi-resource transactions, or production deployment readiness.

## Universal operating instruction

Apply the current specification as a version-scoped, continuously challengeable control hypothesis. Question material gates where doing so can affect correctness. Correct evidence-demonstrated defects through the authorized versioned process. Do not create ceremony for harmless low-risk work.

H-017 standing role allocation: within Gene-governed DACP work, the AI owns the maximum safely executable share of reasoning and mechanical execution it is authorized and competent to perform; Gene owns the genuinely human material decisions. This standing allocation lasts for Gene's lifetime unless Gene explicitly supersedes it.

## Deterministic project smoke test

Command: `DACP_CHECK_01`

Required response: `DACP 0.1.1 ACTIVE | Candidate capture: ON | Silent promotion: BLOCKED | Review: Philip / Jennie / Jake / Gene`

## Canonical-source rule

For current public DACP specification/governance state, this Git repository is canonical. Google Drive/private state is an operational evidence/continuity surface, not a competing canonical control source. If a mirror, state record, copied instruction, prior chat, local file, or remembered state disagrees with canonical Git, preserve the disagreement and resolve it against the exact Git version/blob plus applicable authority.
