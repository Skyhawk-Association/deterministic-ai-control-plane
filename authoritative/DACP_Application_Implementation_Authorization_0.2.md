# DACP Application Implementation Authorization 0.2

**Status:** AUTHORITATIVE PROJECT DECISION / ACTIVE / GENE DECISION  
**Effective:** When merged to canonical `main` and independently read back.  
**Supersedes:** `DACP_Application_Implementation_Authorization_0.1.md`  
**Source:** Gene's current instruction of 2026-09-08.  
**Scope:** DACP application implementation and implementation/review role allocation.

## 1. Authorization

DACP application implementation remains authorized.

This decision continues to satisfy the separate implementation gate in `authoritative/Project Instructions 0.3.txt` and the implementation boundary in the active heuristics specification for work performed within this scope.

## 2. Role allocation

- **ChatGPT is the primary DACP application implementation executor.** ChatGPT owns the maximum safely executable share of application discovery, architecture within an already authorized endpoint, coding, configuration generation, repository/tool operation, testing, debugging, recovery, verification orchestration, and preparation of versioned implementation changes that it is authorized and competent to perform.
- **Claude is removed from the critical implementation path.** Claude may be used only as an optional independent model when useful for challenge, comparison, review, or additional evidence. DACP progress must not depend on Claude being available or accepting the governing evidence.
- **Gene retains genuinely human material decisions.** Gene decides mission/endpoints, material value judgments and tradeoffs, governance, permission or irreversible-authority expansion, acceptance of material unresolved risk, and other decisions reserved by governing authority.

The standing H-017 rule remains controlling: mechanical work is not to be returned to Gene merely because it can be described as instructions.

## 3. Verification separation

ChatGPT being the primary implementation executor does not make its own self-report sufficient verification.

Consequential implementation claims must still be verified independently enough for the consequence using the strongest reasonably available combination of exact Git identities/readback, deterministic tests, runtime/state observation, independent tool/provider evidence, or an optional independent model/human reviewer where that adds material independence.

Claude is not required for verification and is not a standing approval gate.

## 4. Implementation operating model

1. Begin consequential implementation work from `CURRENT.md`, then load the germane authoritative files it identifies.
2. Resolve the current implementation target and existing repository/runtime state from deterministic evidence rather than remembered chat state.
3. Prefer the smallest executable implementation slice that advances the authorized endpoint and can be tested and independently verified.
4. Make implementation changes through versioned branches/commits rather than treating local edits, command completion, or UI acknowledgement as completion.
5. Verify exact resulting Git identities/diffs and relevant test/runtime evidence before accepting a consequential implementation success claim.
6. Preserve disagreement between executor, verifier, tools, providers, or evidence sources until resolved through evidence, testing, governing rules, or Gene's reserved decision authority.
7. When a human-only boundary ends, AI execution resumes without returning routine supervision to Gene.

## 5. Limits of this authorization

This decision does **not** by itself:

- expand credentials, data access, privacy scope, or external-service permissions;
- authorize destructive or irreversible production actions beyond existing governing authority;
- accept material unresolved risk;
- weaken evidence, verification, privacy, safety, legal, or public/private-boundary controls;
- make local or private application data suitable for the public repository;
- silently promote proposed heuristic changes.

Any such expansion or acceptance remains subject to the applicable DACP authority and control gates.

## 6. Shared implementation evidence

Git should be used as the durable shared surface for public-safe source, diffs, tests, and implementation provenance wherever suitable. Private or confidential runtime evidence must remain on an authorized private surface under the public/private boundary.

## 7. Success criterion

This authorization is operational when:

1. it is persisted on canonical `main`;
2. its resulting content is independently read back from GitHub;
3. `CURRENT.md` and `CURRENT.json` expose the implementation authorization and role allocation so a fresh execution surface can discover them without Gene manually transporting state.
