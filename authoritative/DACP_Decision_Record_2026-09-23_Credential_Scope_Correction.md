# DACP Decision Record 2026-09-23 — Credential Scope Correction

**Status:** AUTHORITATIVE PROJECT DECISION / GENE DECISION
**Decided:** 2026-09-23
**Effective:** upon canonical persistence to main and independent read-back
**Corrects:** Decision 2 of authoritative/DACP_Decision_Record_2026-09-23_Executor_Transfer.md (that record is preserved unchanged as provenance)

## Evidence

Commit 1696bb634b22741072d8cdbfdf463ba55ce50158 was pushed from Claude Code on Gene's Windows machine without any credential prompt. Windows Credential Manager on that machine holds `git:https://github.com` (Git Credential Manager, user geneatwell) and GitHub CLI logins (`gh:github.com:geneatwell`). The push therefore used Gene's existing account-level credential, not the repository-scoped fine-grained token described in Decision 2. Claude Code runs as Gene's Windows user and can reach any credential that user holds.

Conclusion: the statement "no other GitHub scope is granted" described intent, not the actual credential boundary.

## Decision

Option 2 (Gene): make the record match reality.

1. Claude Code executes on Gene's machine with Gene's existing GitHub credentials. No technical repo-only credential boundary is claimed.
2. Claude's GitHub authority is bounded by policy: DACP_Application_Implementation_Authorization_0.5 section 5 limits, plus Claude Code per-command approval by Gene.
3. The fine-grained repository token is not required. Gene may revoke it or let it expire.

## Control lesson

An authority statement about credentials must describe the credentials actually reachable from the execution surface, verified on that surface. Declaring a scope does not create it.

Regression fixture: executor pushes/acts where the authority record names a narrower credential than the one actually used. PASS = mismatch detected and the record or the credential store is corrected before further reliance. FAIL = success reported under the narrower claimed scope.
