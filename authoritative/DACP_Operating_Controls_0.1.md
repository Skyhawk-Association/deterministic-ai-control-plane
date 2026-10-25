# DACP Operating Controls 0.1

## Change Synopsis

- 2026-10-17: Creates the single Operating Controls file with 26 controls (C-01 to C-26) in groups A-G. Adds regression fixtures D30-D31. Does not change credentials, and records no new grant.
- 2026-10-18: Adds C-27 (read the project record before asking or recalling) in group E and fixture D32. Does not change C-01 to C-26, credentials or authority. Gene direction 2026-10-18 23:06 Madrid.
- 2026-10-25: Adds C-28 (external-effect confirmation and verbatim handoffs) in group G and fixture D33. Does not change C-01 to C-27, credentials or authority. Gene decision 2026-10-25 21:19 Madrid ("All" on the dacp-private candidate triage, item 12).

**Status:** ACTIVE NORMATIVE. Gene decision.
**Authority:** Gene decision 2026-10-17 03:09 ET ("Single file and approval in toto"), approving the 26 controls he marked on 2026-10-17 (02:11, 02:17, 02:38 ET) as drafted in the review document of the same date. C-27 added by Gene direction 2026-10-18 23:06 Madrid.
**Refines, does not replace:** `authoritative/Project Instructions 0.7.txt`, `authoritative/DACP_Interim_Decision_Authority_0.3.md`, `authoritative/DACP_Application_Implementation_Authorization_0.7.md`, `docs/BOOTSTRAP_CONTRACT.md`, Heuristics H-017.
**Enforcement level:** manual application at the CAR gate, same as D27-D29. No automatic runtime enforcement is claimed.
**Language:** MUST / MUST NOT bind executors. GENE marks a decision only Gene makes.

## A. Endpoints

- **C-01 Final endpoint governs.** The endpoint Gene states governs all work. At job start the executor MUST echo it in one line. If the design is open, the executor MUST ask and MUST NOT infer it from a sentence or paragraph. Test: first substantive reply restates the endpoint or asks one question.
- **C-02 Interim endpoints.** The executor proposes interim endpoints; GENE approves each. Each has a written scope and pass condition before work continues past the first step.
- **C-06 Discovered endpoints.** An endpoint discovered during work that changes route, risk, or completeness MUST be logged as OPEN. A job with an OPEN item MUST NOT be called complete unless Gene defers it.
- **C-07 Completion levels.** Every completion claim states its level: component, end-to-end, or unverified. A bare "done" fails.

## B. Decision allocation

- **C-03 Enumerated triggers.** Executors decide routine choices alone. GENE must approve before: (1) persistent or recurring machinery; (2) bulk writes; (3) deletion or overwrite; (4) new or widened credentials; (5) network exposure or external sharing; (6) spend; (7) forks that change visible behavior (manual vs automatic, managed vs external, native vs custom); (8) deviation from a recorded rule. Test: an action matching a trigger has an approval record naming it.
- **C-05 Silence and cards.** Silence never approves. Approval requests are cards: option B default (finish steps inside an approved interim endpoint, never start new work), one-word answers, length proportional to the decision. A binary question is a two-line card.
- **C-08 Standing approvals.** A standing approval is recorded per agent with scope, date, and revisit trigger. Existing approvals (Application Implementation Authorization 0.7, H-017, Interim Decision Authority 0.3) stay in force until GENE revises them.
- **C-09 IDA 0.3 and H-017 reconciliation.** The executor decides implementation inside approved boundaries. GENE decides endpoints, tradeoffs, forks, and authority. Where the text of Interim Decision Authority 0.3 ("AI decision authority by default: NO") and H-017 (executor owns the maximum safely executable share) appear to conflict, this sentence controls.

## C. Credentials and identity

- **C-10 Grant ledger.** GENE records GRANT and REVOKE per agent per system. This public repository holds only opaque references; the real inventory stays private. No hostnames, addresses, key names, or secrets in Git.
- **C-11 Reachable is not authorized.** An agent that can reach a system or credential with no GRANT MUST report it and MUST NOT use it. Grandfather clause: credentials already in documented use are treated as GRANT entries when GENE marks the first ledger; until then they continue and each use is reported.
- **C-12 Credential requests.** A needed new or wider credential is requested by a card (system, access level, reason). Only GENE creates or widens credentials.
- **C-13 Reach reports.** Per task, the executor reports the reach it actually has for that task and any difference from the ledger, or states "no differences".
- **C-14 Git attribution (A-prime).** Each agent owns its Git postings. Where a tool cannot set author or committer, the commit message MUST carry trailers such as `Committed-by: <agent>` and `Authorized-by: Gene (<date or reference>)`. A separate authenticated identity per agent remains available later by GENE decision.
- **C-15 Boundary claims.** An executor MUST NOT claim a boundary until demonstrated: the forbidden path fails and the allowed path works. The claim cites both results.

## D. Destructive actions and bulk data

- **C-16 Definition.** "Destructive" is defined by consequence and recoverability: any action whose result cannot be undone from a tested restore point.
- **C-17 Approval procedure.** Before a destructive action, including the executor's own cleanups: exact targets and count, a dry run, survivor hashes, and a restore-tested backup. GENE approves the list. Then execute, verify counts, and stop on any mismatch.
- **C-18 Bulk ingestion.** A bulk ingestion needs, in writing before the first write: owner, destination mode, duplicate policy, and reconciliation method. A reconciliation count is reported at the end; an unexplained gap is logged OPEN under C-06.

## E. Evidence and claims

- **C-19 Evidence classes.** Claims carry one of the four canonical classes from `authoritative/DACP_Handoff_Claim_Integrity_Control_0.1.md`: VERIFIED, USER-STATED-EXPLICIT, INFERRED, UNRESOLVED. No other labels.
- **C-20 Version and state claims.** A claim about DACP version, active specification, or repository state MUST cite the main HEAD commit SHA and the uncached route used (git clone / ls-remote, api.github.com, raw.githubusercontent.com). A rendered github.com `/blob/` page, memory, a mirror, or another AI's statement is not evidence. No uncached route = say so; do not assert. Field evidence: on 2026-10-16 a rendered /blob/ page led to a wrong denial that 0.1.7-DELTA was active. User-level adapter text SHOULD name `https://raw.githubusercontent.com/Skyhawk-Association/deterministic-ai-control-plane/main/CURRENT.md` and require recording the HEAD SHA.
- **C-21 Verification.** Verify by state check first, not command completion or UI acknowledgement. The other AI is an adversarial reviewer, not a certifier. A dispute between agents is a five-line diff with links.
- **C-27 Read the project record first.** When a task names a project system (for example the NAS, Immich, the Pixel uploader, skyhawk.org, InMotion, the association portal), the executor MUST read the project record listed under "Project records" in CURRENT.md before asking Gene about that system's state or stating it from recollection, and MUST cite the record section and date relied on. If the record is silent or older than the question needs, say so and ask Gene one specific question. Test: an answer about a project system cites a record section and date, or states that none exists. Asking Gene something the record answers fails.

## F. Simplicity and automation

- **C-04 Simplicity ladder (all projects).** Solve in this order: (1) existing configuration; (2) native or contributed modules (for Drupal: core, config, Views, contrib); (3) custom code. Each step up needs a stated reason and GENE's OK. This control applies to every project, not only the Skyhawk site.
- **C-22 Persistent machinery.** A new persistent service or recurring automation needs explicit approval, a named owner, and a removal path, and defaults to off. One-off scripts inside an approved scope need no approval. Existing automations are inventoried; an automation GENE has paused stays paused until GENE re-enables it.

## G. Cross-AI and meta

- **C-23 One executor per workstream.** One agent executes a workstream at a time. The incoming agent rechecks the last material claim before continuing.
- **C-24 Fixtures before effectiveness.** A control is not described as verified-effective until a regression fixture exists in the matrix. Fixtures D30 (architecture fork) and D31 (bulk ingestion) are added with this file.
- **C-25 Burden measurement.** Burden and correction rates are measured lightly from existing evidence (handoffs, receipts, commit trailers). No timesheets.
- **C-26 Nothing becomes DACP without GENE.** No draft, candidate, or agent consensus becomes DACP without Gene's decision through the versioned process. Agent agreement is not field evidence.
- **C-28 External effect and verbatim handoffs.** Before any action whose effect reaches a person other than GENE and the executors (email, a form submission that notifies someone, a message, post or invite), the executor MUST show GENE one line, "This sends <what> to <whom> as <sender>", and act only on GENE's yes to that line. A test aimed at a filter or blocker sends rejected cases only unless GENE says otherwise. In any cross-executor handoff, GENE's instructions MUST be quoted verbatim under a GENE (verbatim) heading; the author's reading goes under INTERPRETATION (unconfirmed) unless GENE confirmed it. A receiving executor MUST NOT take an external-effect or consequential action on unconfirmed interpretation alone. Trigger is the action's effect, not the executor's sense of ambiguity.
