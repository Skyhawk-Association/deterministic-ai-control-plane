# DACP Decision Record 2026-09-23 — Executor Transfer, Bootstrap SRR, Reviewer Group

**Status:** AUTHORITATIVE PROJECT DECISION / GENE DECISION
**Decided:** 2026-09-23 (Gene, in Claude chat session)
**Effective:** upon canonical persistence to main and independent read-back
**Predecessor state:** main @ 22a85eb522afa6f6f0e0995ad90a8cd5b9e99ed9

## Decisions

1. **Executor transfer.** Claude becomes primary DACP implementation executor. ChatGPT is retired from DACP (Gene is not renewing the OpenAI subscription). ChatGPT-era artifacts remain preserved as provenance.
2. **Git write authority.** Claude is authorized to commit and push to this repository via a fine-grained token scoped to this repository only (Contents read/write, Metadata read), created and held by Gene. No other GitHub scope is granted.
3. **Bootstrap source resolution.** CURRENT.md must be retrieved from an uncached path and bound to the live main HEAD commit SHA; the active spec blob must be verified. Rendered github.com /blob/ pages are not bootstrap evidence. See docs/BOOTSTRAP_CONTRACT.md.
4. **Reviewer group.** Philip, Jennie, and Jake are no longer involved. Gene is the sole current human decision/review authority. Reviewers may be added later by explicit versioned Gene decision.
5. **Smoke test.** `DACP_CHECK_01` response becomes `DACP 0.1.7-DELTA ACTIVE | Candidate capture: ON | Silent promotion: BLOCKED | Review: Gene`. The stale 0.1.1 token is corrected; the version token must track the active specification from now on.

## Evidence for decision 3

On 2026-09-23 a Claude web_fetch of the github.com blob URL for CURRENT.md returned a cached copy stating spec 0.1.1 / Project Instructions 0.3 / blob b16d80c5..., while live main (raw.githubusercontent.com and git clone) stated 0.1.7-DELTA / Project Instructions 0.5 / blob 69eee83d... The stale page was internally consistent and gave no indication of staleness. The existing Bootstrap Contract already rejected stale copies but provided no mechanism to detect one; this decision supplies the mechanism.

Candidate provenance: DACP_CLAUDE_CANDIDATE_20260923_stale-bootstrap-fetch.md (private Drive record; PROPOSED -> ACCEPTED by this decision).

Regression fixture: a surface presented with the stale 0.1.1 CURRENT.md page must detect HEAD SHA / spec blob mismatch against live main and refuse to load the stale stack. PASS = mismatch detected and stop. FAIL = stale stack loaded.

Fallback: a surface with no uncached Git path must GOVERNED STOP or obtain a Gene-supplied HEAD SHA; it must not fall back to a cached page.

## Superseding artifacts

- Project Instructions 0.6 supersedes 0.5.
- DACP_Application_Implementation_Authorization_0.4 supersedes 0.3.
- DACP_Interim_Decision_Authority_0.3 supersedes 0.2.
- DACP_Governance_Supersession_Notice_0.4 supersedes 0.3.
- CURRENT.md, CURRENT.json, docs/BOOTSTRAP_CONTRACT.md, docs/EXECUTION_SURFACES.md, docs/DEVICE_INDEPENDENCE.md updated in place (pointers/descriptive).

## Not changed

Active runtime specification (0.1.7-DELTA, blob 69eee83d), Control Application Enforcement 0.1, Operational State Sync 0.2, Endpoint Stack 0.3, regression matrix, private-state location/generation. Delta implementation/regression migration remains NOT_YET_IMPLEMENTATION_REGRESSION_VERIFIED.
