# DACP Current Bootstrap

## Change Synopsis

- 2026-09-23 credential scope correction (authoritative/DACP_Decision_Record_2026-09-23_Credential_Scope_Correction.md): Application Implementation Authorization 0.5 replaces the repo-scoped-token claim with the actual credential model.
- 2026-09-23 (Gene decision; authoritative/DACP_Decision_Record_2026-09-23_Executor_Transfer.md): Claude becomes primary executor, ChatGPT retired; Project Instructions 0.6, Application Implementation Authorization 0.4, Interim Decision Authority 0.3, Supersession Notice 0.4 activated; bootstrap must bind live main HEAD SHA; reviewer group removed. Active runtime specification unchanged.

### 0.1.7-DELTA activation (2026-09-18)

- Activates 0.1.7-DELTA as the successor to 0.1.6-CHARLIE after repeated field evidence showed that retrieval/awareness of valid controls did not reliably cause their application to the next action.
- Activates Project Instructions 0.5 and Control Application Enforcement 0.1.
- Replaces awareness-based compliance with task-time Control Application Receipts, execution-context binding, exact-source resolution, ownership binding, and a hard pre-output gate for material executable actions.
- Makes repeated CONTROL_APPLICATION_FAILURE a mandatory whole-route reorientation trigger.
- Activates Operational State Sync 0.2, Operational Use and Correction Authority 0.2, Endpoint Stack 0.3, and Application Implementation Authorization 0.3.
- Preserves Charlie and earlier artifacts as provenance.
- Does not claim that every existing DACP application slice already implements Delta; implementation/regression migration remains a separate evidence requirement.

**Canonical migration status:** ACTIVE GIT CANONICAL
**Repository:** Skyhawk-Association/deterministic-ai-control-plane
**Default branch:** main
**Current specification:** docs/DACP_Runtime_Expression_0.1.7-DELTA.md
**Specification version:** 0.1.7-DELTA
**Specification status:** AUTHORITATIVE / ACTIVE / GENE DECISION
**Activation decision:** authoritative/DACP_0.1.7_DELTA_Activation_2026-09-18.md
**Verified specification Git blob:** 69eee83df64bd0a36e394ea38176348de2834938

**Predecessor specification:** docs/DACP_Runtime_Expression_0.1.6-CHARLIE.md
**Predecessor status:** SUPERSEDED AS ACTIVE / PRESERVED AS PROVENANCE

## Bootstrap source resolution

Retrieve this file uncached (git clone / git ls-remote, api.github.com, or raw.githubusercontent.com). Record the main HEAD commit SHA and verify the active specification blob (`git rev-parse HEAD:docs/DACP_Runtime_Expression_0.1.7-DELTA.md` must equal the blob below). A rendered github.com /blob/ page is not bootstrap evidence. No uncached path = GOVERNED STOP or Gene-supplied HEAD SHA. See docs/BOOTSTRAP_CONTRACT.md.

## Load order before consequential DACP work

1. authoritative/Project Instructions 0.6.txt
2. docs/DACP_Runtime_Expression_0.1.7-DELTA.md
3. authoritative/DACP_0.1.7_DELTA_Activation_2026-09-18.md
4. authoritative/DACP_Control_Application_Enforcement_0.1.md
5. authoritative/DACP_Operational_State_Sync_0.2.md
6. STATE_LOCATOR.json
7. authoritative/DACP_Interim_Decision_Authority_0.3.md
8. authoritative/DACP_Operational_Use_and_Correction_Authority_0.2.md
9. authoritative/DACP_Path_Viability_Revalidation_Control_0.1.md when path-viability provenance/detail is germane.
10. authoritative/DACP_Continuous_Execution_and_Human_Boundary_Control_0.1.md when continuation/human-boundary provenance/detail is germane.
11. authoritative/DACP_Endpoint_Stack_0.3.md
12. authoritative/DACP_Application_Implementation_Authorization_0.5.md when application implementation is germane.
13. tests/DACP_0.1.7_DELTA_Regression_Matrix.md when action-gating/regression evidence is germane.
14. authoritative/DACP_Governance_Supersession_Notice_0.4.md when smoke-test history matters.
15. predecessor specifications only for provenance/comparison.

## Operational state

STATE_LOCATOR.json identifies the private operational-state surface. Current private state remains generation 36 on the verified Google Drive local-sync surface at this activation boundary. Private state is evidence/continuity, not competing canonical governance.

For nontrivial or consequential work, resolve current private state when authorized and available, including unresolved same-cause CONTROL_APPLICATION_FAILURE pointers once the private state schema is migrated to Operational State Sync 0.2.

## Active runtime

Delta's governing distinction is:

**retrieved control != applied control**

For every material executable action, external mutation, destructive action, or material readiness/success claim, bind a Control Application Receipt. Resolve exact authority, source identity, current state, execution context/operator position, target owner, consequence/reversibility, human boundary, success evidence, verifier, and stop behavior before action.

If a material binding is unresolved or contradicted, executable output is blocked.

When an established operational reference defines the operator's current position, generated commands begin from that position. Do not invent reconnects, nested remote sessions, environment transitions, or generic setup.

When the same causal control-application failure recurs, invalidate the local action plan and perform whole-route reorientation before further consequential mutation.

## Application implementation status

Application implementation remains authorized through authoritative/DACP_Application_Implementation_Authorization_0.5.md.

Claude is primary implementation executor (Claude Code on Gene's machine, Gene's GitHub credentials, policy-bounded authority). ChatGPT is retired from DACP; its work remains provenance.

Delta corpus activation does not itself prove that existing application code enforces CAR/ECR/SRR. That migration must be implemented and regression-tested separately.

## Deterministic project smoke test

Command: DACP_CHECK_01

Required response:

DACP 0.1.7-DELTA ACTIVE | Candidate capture: ON | Silent promotion: BLOCKED | Review: Gene

and nothing else.

H01CHECK is retired.

## Canonical-source rule

Canonical Git governs current public DACP specification/governance state. Mirrors, prior chats, summaries, remembered state, private state, and diagnostics do not override it.
