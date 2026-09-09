# DACP Application Implementation Authorization 0.1

**Status:** AUTHORITATIVE PROJECT DECISION / ACTIVE / GENE DECISION  
**Effective:** When merged to canonical `main` and independently read back.  
**Source:** Gene's current instruction of 2026-09-08.  
**Scope:** DACP application implementation and its implementation/review role allocation.

## 1. Authorization

DACP application implementation is authorized to resume.

This authorization satisfies the separate implementation gate in `authoritative/Project Instructions 0.3.txt` and the implementation boundary in the active heuristics specification for work performed within the scope of this decision.

## 2. Role allocation

- **Claude is the primary implementation executor.** Claude owns the maximum safely executable share of application coding, routine technical design needed to execute an already authorized endpoint, local implementation, tests, debugging, recovery, and preparation of versioned changes that it is authorized and competent to perform.
- **ChatGPT is the independent reviewer / control-plane verifier.** ChatGPT reviews exact versioned artifacts, diffs, tests, control applicability, verification evidence, regressions, and material implementation claims independently enough for the consequence.
- **Gene retains genuinely human material decisions.** Gene decides mission/endpoints, material value judgments and tradeoffs, governance, permission or irreversible-authority expansion, acceptance of material unresolved risk, and other decisions reserved by governing authority.

The standing H-017 rule remains controlling: mechanical work is not to be returned to Gene merely because it can be described as instructions.

## 3. Implementation operating model

1. Begin consequential implementation work from `CURRENT.md`, then load the germane authoritative files it identifies.
2. Resolve the current implementation target and existing repository/runtime state from deterministic evidence rather than remembered chat state.
3. Prefer the smallest executable implementation slice that advances the authorized endpoint and can be tested and independently reviewed.
4. Claude should make implementation changes on versioned branches/commits rather than treating local edits or UI acknowledgement as completion.
5. ChatGPT should review the exact resulting Git identities/diffs and relevant test/runtime evidence before a consequential implementation success claim is accepted.
6. Preserve executor/reviewer disagreement until resolved by evidence, testing, governing rules, or Gene's reserved decision authority.
7. When a human-only boundary ends, AI execution resumes without returning routine supervision to Gene.

## 4. Limits of this authorization

This decision does **not** by itself:

- expand credentials, data access, privacy scope, or external-service permissions;
- authorize destructive or irreversible production actions beyond existing governing authority;
- accept material unresolved risk;
- weaken evidence, verification, privacy, safety, legal, or public/private-boundary controls;
- make local or private application data suitable for the public repository;
- silently promote proposed heuristic changes.

Any such expansion or acceptance remains subject to the applicable DACP authority and control gates.

## 5. Shared implementation evidence

Git should be used as the durable shared surface for public-safe source, diffs, tests, and implementation provenance wherever suitable. Private or confidential runtime evidence must remain on an authorized private surface under the public/private boundary.

The implementation executor's self-report is not sufficient proof of a consequential result. Verification must observe the resulting state or a sufficiently independent proxy proportional to the consequence.

## 6. Success criterion

This authorization is operational when:

1. it is persisted on canonical `main`;
2. its resulting content is independently read back from GitHub;
3. `CURRENT.md` exposes the implementation authorization so a fresh Claude or ChatGPT execution surface can discover the active role allocation without Gene manually transporting it.
