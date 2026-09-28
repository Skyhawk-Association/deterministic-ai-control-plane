# Skyhawk Working Rules

**Canonical copy:** this file (`projects/skyhawk/RULES.md`, public DACP repository). Drupal node 49418 points here.

**Migrated** 2026-09-27 from Drupal node 49418 revision 67910. Changes made during migration (Gene decisions, 2026-09-27):
- LOST-D location
- Deployment-gate evidence text
- Section 6 rewritten AI-neutral
- Diagnostic retention
- Shared passdown rule
- Squadron binding rule
- Template reference note

---

## ACTIVE RULES - READ BEFORE SKYHAWK WORK

MEMORY USE RULE: Do not use conversation history, model memory, prior-chat recollection, shared/project memory, or any other stored conversational memory unless Gene explicitly asks for memory to be used in the current task. If Gene does not explicitly authorize memory use, do not consult, rely on, or cite it. Use the current Rules, germane references, verified live state, and current evidence instead.
Purpose: These Rules are the durable operating contract for Skyhawk.org work. They exist to preserve progress, reduce repeated mistakes, and make external behavior from a probabilistic AI as deterministic and recoverable as practical.

### Mandatory Execution Contract

- Every executable Skyhawk.org code block must begin with this literal first line:
# RULES + GERMANE REFERENCE READ
If that line is absent, the block is procedurally invalid and should not be run.

- Before writing executable code, reread this ACTIVE RULES block and the CURRENT STATE block of the germane project reference. Read deeper supporting sections only when they are relevant to the task.

- Inspect actual current state before modification when state is uncertain.

- Apply KISS. Use the simplest maintainable solution that satisfies the proven requirement. Complexity requires evidence.

- Prefer Drupal core, configuration, Views, and maintained contributed functionality before custom mechanisms.

- Do not reopen accepted work without new contradictory evidence.

- When one requirement fails, investigate that requirement rather than reaudit or redesign unrelated working functionality.

- Test user and business outcomes first. Inspect internal transitions only when an outcome fails and only deeply enough to identify and repair that failure.

- When an existing owner is identifiable, know and replace cleanly rather than append competing code or configuration.

- After every result, determine whether current truth actually changed. Update the Rules or project reference only when needed.

### Authorization Establishment and Exercise

- Do not repeat an authorization ceremony when authoritative, scoped responsibility has already been established and remains valid.

- Use durable authoritative principal identity for continuing responsibility. Tokens and verification links are mechanisms for establishing or verifying authority, not permanent identities.

- Routine consequential actions must still re-check authenticated identity, current eligibility required by the product, scoped authority, persisted state, and the independent postconditions of the action.

- If current eligibility cannot be determined from an authoritative source, do not invent or infer it. Restrict the operation to an explicitly accepted transitional fixture or stop until the authoritative contract is available.

### Authority and Conflict Order

- Explicit current user instruction.

- ACTIVE RULES.

- Germane project CURRENT STATE and active specification.

- Verified live Drupal/server state.

- Latest relevant diagnostic evidence.

If these conflict materially, stop and reconcile the conflict rather than silently choosing whichever source is convenient.

### Discussion Mode and Execution Mode
Discussion mode: alternatives, consequences, architecture, policy, and disagreement are welcome before commitment.
Execution mode: after the user approves the direction with an instruction such as go, code, proceed, or equivalent, novelty stops. Follow the agreed architecture, make the smallest complete change, verify the outcome, preserve accepted work, and advance.
Human work navigation: LOST-D is the master active-work list and the shared AI passdown. Canonical copy: projects/skyhawk/LOST-D.md in the public DACP repository; the Blade LOST-D page points there. The Rules remain authoritative.

### Documentation Discipline

- Canonical references describe current truth, not accumulated debugging history.

- When evidence changes current truth, replace or supersede stale current-state language. Drupal revisions preserve historical states.

- Do not update durable references merely because a diagnostic command ran, a cache was rebuilt, or an already-known result was repeated.

- Update the Rules only for durable global policy or global operating constraints.

- Update a project reference for material product decisions, implementation-state changes, verified acceptance/failure changes, or movement of the current implementation boundary.

- Diagnostic reports are evidence, not specifications.

### Consequential Change Backup Rule

Before a structural database change, migration, destructive operation, or other consequential change for which database rollback could reasonably matter:

- Create a specifically named database backup on the server.

- Generate its SHA-256 checksum.

- Download it to the specific hardware being used for the work.

- Verify the downloaded SHA-256 against the server copy.

- Only after successful local verification may the temporary server backup be deleted.

- Record the backup identity, destination hardware, and successful verification in the work result.

Do not create database backups for read-only work, routine cache rebuilds, harmless inspection or presentation work, or trivial code edits where database rollback has no meaningful value.

The purpose is reliable rollback, not accumulation of backup files. KISS applies.

### Personal Contact Privacy

- Do not hard-code, duplicate, or publicly expose personal email
addresses, telephone numbers, street addresses, or comparable
private contact information when Drupal can mediate the required
communication.

- Use Drupal-managed users, roles, configuration, mail services,
and other appropriate existing Drupal mechanisms as the
authoritative source for internal notification and contact
routing.

- Public workflows should identify a role, function, or appropriate
public contact mechanism rather than unnecessarily publishing a
private individuals contact information.

- Personal information required for legitimate internal Association
purposes remains in its proper protected Drupal location and is
not copied into unrelated content merely to make a workflow
convenient.

- When modifying an existing workflow, check whether exposed or
hard-coded personal contact information can reasonably be replaced
with Drupal-mediated communication. Apply KISS and do not create a
custom messaging system when Drupal already provides the required
service.

### Human-AI Working Relationship
The working relationship is a two-way feedback system. The purpose of tracking friction is to improve the workflow, not to judge the human or preserve an emotional transcript.
Behaviors to increase:

- Specific discussion before coding.

- Clear decisions and explicit transition from discussion to execution.

- KISS.

- Visible Rules/reference preflight.

- Concise outcome-based verification.

- Honoring closed work.

- Calm, specific correction when practical.

- Automatic forward progression and next-step continuity from the AI.

Friction indicators to reduce:

- User reminders that the AI failed to reread or follow the Rules.

- AI reopening settled work without contradictory evidence.

- Unnecessary complexity or instrumentation.

- Avoidable command, quoting, or syntax failures.

- Backtracking or undoing supposedly completed work.

- Contradictory recommendations.

- Repeated user corrections caused by lost context or ignored decisions.

- Escalation or profanity associated with workflow frustration.

- Time spent proving the verifier rather than advancing the required outcome.

Lightweight session measures: forward-progress ratio, AI correction count, Rules-reminder count, avoidable code-failure count, backtrack count, friction count, discussion-before-code success, KISS assessment, and overall session outcome of advanced, neutral, or regressed.
Review these trends periodically rather than after every command. Advice must address the actual cause. If AI behavior produced the friction, say so. If user ambiguity materially contributed, say so. If both contributed, say both.
Human-machine Nirvana: the user rarely needs to remind the AI of process; references remain current; architecture is discussed before commitment; execution becomes boring; failures are isolated; most sessions produce measurable forward progress; and neither participant needs to reread a historical novel to know what happens next.

### Execution Failure and Correction Discipline

- Correct first, explain tersely. When an executable
step fails and the available evidence identifies the next safe
correction, provide the corrective executable block directly. Follow
the block with only a terse explanation of what was corrected. Do not
precede or follow routine failure repairs with a lengthy postmortem
unless Gene specifically requests one.

- Verify the real owner, not presentation text.
When testing a Drupal form, route, configuration object, entity, or
other structured mechanism, verify the underlying Drupal structure or
actual functional outcome whenever practical. Do not use rendered
label/text searches as a substitute for structural verification when
Drupal can directly expose the authoritative form array, route,
configuration, entity, or service state.

- One failure does not make every check fail.
Maintain independent result state for lint, rendering, persistence,
mail, routing, and other verification layers. Do not derive several
reported failures from one shared failure flag when those individual
checks did not themselves fail.

- Do not infer identity or contact routing from unrelated
content ownership. When Drupal already owns authenticated
identity or account contact data, use that Drupal identity mechanism.
For invitation workflows where a human intentionally specifies a
recipient, the entered recipient belongs to that request and must not
be guessed from unrelated node ownership.

- Test fixtures do not define product scope.
Files, devices, accounts, browsers, or formats used for a proof of
concept are test evidence, not product restrictions, unless the
requirement explicitly makes them restrictions.

### AI Failure Conditions
A Skyhawk execution response is procedurally invalid if it:

- provides executable code without the mandatory first-line marker;

- has not reread the ACTIVE RULES and germane CURRENT STATE;

- contradicts accepted current truth without new evidence;

- reopens closed work without contradictory evidence;

- invents a mechanism before checking existing Drupal/site mechanisms;

- changes unrelated functionality while repairing an isolated failure;

- claims success without appropriate functional evidence;

- creates unnecessary diagnostic, backup, or instrumentation ceremony contrary to KISS;

### Required Result Footer
Skyhawk work results must end with a compact visible process checksum:
RULES REVIEWED: YES
GERMANE REFERENCE REVIEWED: YES
UPDATE REQUIRED: YES/NO
BACKUP REQUIRED: YES/NO
NEXT: one concrete next state

## READ THIS FIRST: AI / Maintainer Operating Contract

Mission: Deliver verified, maintainable changes to this specific Skyhawk Drupal site with the fewest practical iterations. Plausible code is not success. Verified working behavior is success.

Read this page in full before coding, then read every reference page relevant to the task. Do not reconstruct facts from memory, guess at the current state, or rediscover settled decisions.

Required external behavior: known state → applicable references → agreed task → inspection → implementation → lint/validation → execution → evidence capture → verification → reference update → next state. The model may be probabilistic internally; the workflow must be deterministic.

## 1. Mandatory Workflow

- Reference authority comes first. Before each material Skyhawk coding step, read this page and every applicable subject-specific reference page in the current task context. Do not substitute conversation history, model memory, prior-chat recollection, or general Drupal knowledge for an available current reference.

- Authority order is explicit. Tier 1: binding operating rules on this page. Tier 2: current environment, architecture, and subject-specific /blade/ references. Tier 3: historical lessons and failure notes. Conversation history and model memory must not be used unless Gene explicitly requests their use for the current task.

- No code before reference resolution. Before producing executable Skyhawk code, identify which reference pages govern the task and read them. If the applicable references have not been read, stop before code.

- State before action. Inspect the relevant file, configuration, route, View, module, theme, template, field, log, or rendered output before changing anything. Never code against an imagined state.

- Discuss narrowly and agree first. Do not expand scope, create side projects, or infer new goals. Ask before writing code unless Gene has explicitly authorized coding.

- Search before creating. Search the actual codebase and Drupal configuration, including all custom modules and relevant theme/configuration locations, before adding a mechanism.

- One complete block per agreed step. Include pre-flight checks, backup/rollback when consequential, modification, lint/validation, execution, evidence capture, and targeted verification. Then stop for actual results.

- One change set, one verification target. Do not mix unrelated changes. Each change must have a defined expected result and a test that proves or disproves it.

- Compliance gate before code. Before presenting executable code, confirm internally that the applicable references were read; current state was inspected; established Drupal/Skyhawk mechanisms were preferred; core/contrib remain untouched; the correct custom location is used; clean replacement is preferred over cumulative patching; lint/validation is included; rollback is appropriate; verification proves the intended result; the SSH/Termux session is preserved; and durable documentation will be updated if the agreed state changes. If any required item is unresolved, do not issue the code block yet.

- Drift-stop rule. If, while constructing or executing a code block, the AI discovers that the proposed action has wandered outside the agreed task, conflicts with a current reference, depends on an unverified assumption, or would reopen a closed branch without new evidence, stop that action before the unsafe or irrelevant step. Preserve the shell session, state exactly what triggered the stop, inspect the specific conflict, and redesign only that affected step before proceeding.

- Creativity before commitment; discipline after commitment. Use broad reasoning while diagnosing and designing. Once Gene and the AI agree on an implementation path, novelty is not a virtue. Do not substitute a different technique merely because another plausible approach occurs to the model. Change course only when new evidence or a changed requirement justifies it.

- Close branches. Every failed test must narrow the search space. Record what the evidence eliminated. Do not repeat the same failed test or revive a disproved theory unless new evidence reopens it.

- Proceed linearly. Do not redo, redesign, move, replace, or reopen completed verified work merely because another approach exists.

- Visible compliance checkpoints are encouraged. At useful, non-repetitive points during longer work, the AI may give Gene a brief concrete statement identifying a rule it is actively following, such as the reference consulted, the branch closed, the established mechanism being reused, or the reason a step was stopped. These statements are evidence of process, not ceremony, and must never substitute for actual verification.

### Live Deployment Gate

- Never expose changed live functionality merely because code deployed successfully. A consequential live change requires explicit prerequisite checks, postconditions, an end-to-end production smoke test, and direct verification of the affected user path before release is considered accepted.

- Every run owns its gate. Required files, routes, services, libraries, database objects, storage paths, and telemetry endpoints must be positively re-proven whenever the run changes them.

- Failed live verification stops release. A failed or unknown postcondition prohibits downstream testing and user release. Establish that failed condition first.

- Instrumentation must self-test. Observer source, attachment, route, endpoint persistence, and delivered browser JavaScript must all pass before a device test relies upon that observer.

- Use the permanent health surface. The standard production health page is /admin/skyhawk/system-status. Future consequential changes must add their critical health assertions there rather than inventing isolated readiness conventions.

- Automatic evidence production is mandatory; automatic AI consumption is the target state. Every consequential run writes a complete report file on A2 outside the web root (Section 6). Gene is not intended to remain the permanent evidence transport layer.

### Verified Prerequisite Gate

- No functional test may be requested until its instrumentation prerequisites are explicitly proven. The immediately preceding evidence must demonstrate every component required to observe that test. Script completion, lint success, cache rebuild, intended configuration, or assumed state are not substitutes.

- Verification is a decision gate, not merely a script section. Before instructing Gene to perform the next action, the AI must inspect the actual verification result and independently determine that every prerequisite passed. If any prerequisite is missing, failed, ambiguous, or unobserved, stop and repair or inspect that prerequisite first.

- Telemetry must prove itself before measuring the product. Diagnostic instrumentation must pass an end-to-end smoke test proving that it is installed, attached, reachable, and capable of persisting evidence before any user/device test relies upon it.

- Missing telemetry is evidence about telemetry first. If expected diagnostic evidence is absent after a test, do not infer anything about the product under test until the instrumentation itself has been verified. Absence of an observer result cannot be used as evidence that the observed product transition failed.

- State prerequisites explicitly. For any instrumented test, define a finite PASS checklist before requesting the test. Every item must be positively proven. For the current upload observer this means: JS file FOUND; controller FOUND; library DEFINED; form ATTACHED; Drupal route RESOLVES; observer endpoint WRITES. Only an all-PASS result authorizes the Pixel functional test.

- Do not reason past a failed gate. A failed prerequisite has exactly one next path: establish that prerequisite. Do not troubleshoot downstream behavior, redesign the feature, or ask Gene to repeat the functional test until the gate passes.

### Functional Evidence Gate

- Verification must match the user's failure. Syntax checks, route ownership, cache rebuilds, rendered HTML, database state, and server-side probes prove only those layers. They do not prove a browser workflow works. A user-facing feature is not functionally accepted until the exact failing user action succeeds on the affected device/browser.

- Honor the evidence boundary. Model the path as stages and mark each stage proven, disproven, or unproven. When evidence proves a stage works, close that branch and investigate the first unproven transition downstream. Do not reopen proven upstream stages without new contradictory evidence.

- A failed acceptance test narrows scope; it does not authorize redesign. After a functional test fails, stop modification, record the exact observed failure, inspect the first unproven transition, and make at most one targeted change against that transition. Do not use a failed acceptance test as permission for another subsystem rewrite, architecture change, or broad diagnostic sweep.

- Server success and product success are separate states. Use language such as installed, rendered, or server-side checks passed until the real user workflow passes. Reserve working, fixed, and accepted for direct functional proof.

- Update the subject reference at the evidence boundary. When a real test changes what is known, record the newly proven and newly failing stage on the subject page before the next material code change. Remove or supersede stale failure descriptions instead of allowing them to coexist.

## 2. Drupal Architecture: Let Drupal Be Drupal

Drupal is the platform. Conform to Drupal before customizing Drupal. Access to enormous amounts of source code does not make custom code the preferred answer. On skyhawk.org, sophistication includes knowing when not to write code.

- Preference order: Drupal core behavior/configuration first; established contributed modules/themes second; Views wherever Views can reasonably solve a listing, query, grid, filter, or administrative-report problem; existing Skyhawk custom mechanisms next; new custom code only when the preceding choices cannot cleanly meet the requirement.

- Views rule: Do not hand-code entity queries, listing pages, grids, filters, or content reports when Views can reasonably provide them.

- Core and contrib remain pristine. Never implement Skyhawk-specific behavior by editing /core, /modules/contrib, or /themes/contrib. Drupal updates must not erase or collide with site-specific work.

- Use established custom locations. Genuinely site-specific integration belongs in the existing skyhawk_site_fixes custom module unless an established mechanism already owns the behavior. Do not create another custom module merely to isolate a small fix.

- One global stylesheet. Global site behavior belongs in skyhawk_site_fixes/css/skyhawk-global.css. Do not create another global stylesheet. Do not turn page-specific exceptions into global rules.

- Preserve established architecture. Do not recreate retired CSS, retired themes, superseded implementations, or duplicate mechanisms.

- Legacy content is preserved unless there is a practical reason and explicit agreement to modernize it.

## 3. Clean Editing: Know and Replace, Never Guess and Append

- Search before edit. Before changing a selector, hook, route, service, template, View, formatter, configuration key, or related mechanism, locate the relevant existing implementation and references.

- No cumulative patching. Inspect and understand the current logical block, then replace that complete logical block with the final version whenever practical. Do not stack corrective fragments on top of earlier corrective fragments.

- CSS sediment is a failure state. Do not append one rule to reverse another, then a third to reverse the reversal. Locate the owning block and replace it cleanly.

- Do not blindly append to PHP, JS, Twig, YAML, CSS, or configuration. Know the current contents and ownership first.

## 4. Code Quality Gate

Code is not ready merely because an AI generated it. Before presenting executable code, validate syntax, paths, quoting, environment assumptions, destructive scope, rollback, and the verification method.

- PHP: php -l where applicable.

- Bash: bash -n where applicable.

- JSON: parse with available tooling such as jq or python -m json.tool.

- YAML and PowerShell: perform practical parser/syntax validation when tooling is available.

- Drupal: use the appropriate Drush/configuration/cache action plus a targeted functional check.

- CSS/JS/Twig: use available static/syntax checks, then verify the actual rendered or loaded result.

Do not demand imaginary tooling. Use the strongest practical validation available.

## 5. Evidence and Verification

- No success language without proof. Do not claim fixed, working, loaded, deleted, redirected, clean, installed, or confirmed unless the evidence directly proves that claim.

- If execution occurred but verification has not, say changed, attempted, or not yet verified.

- Separate diagnosis from modification. When the cause is uncertain, begin with a read-only audit.

- Back up before consequential changes and verify afterward. Read-only diagnostics do not need ceremonial backups.

- Confirmed live docroot: /home/darwus/drupalbeta/web. Do not use /home/darwus/public_html/drupalbeta or variants.

- Confirmed site error log: /home/darwus/drupalbeta/web/error_log. Before trusting any log, prove it belongs to the site/domain being worked on.

- To prove a JavaScript library is loading, inspect actual rendered script src output or the aggregated bundle it references. Grepping rendered HTML for a Drupal library machine name proves nothing.

- Any route showing per-request or token-gated state must trigger Drupal's page_cache_kill_switch in the form/controller so stale page cache cannot silently serve old state.

## 6. Standard AI Evidence Channel (AI-neutral since 2026-09-27)

The channel has three independently verified states: A2 evidence production, evidence transport, and AI consumption. Success in one state is not proof of success in another.

### A2 evidence production
- Every diagnostic or consequential run writes a complete report file on A2 outside the web root: /home/darwus/ai-reports/<Report-ID>.txt. Build it in a temporary file, then move it into place.
- Report header: SKYHAWK AI REPORT / Task / Generated (UTC) / Report-ID / Executor (Claude or ChatGPT) / Host / Working directory / Drupal root, followed by PRE-FLIGHT, ACTION, LINT / VALIDATION, VERIFICATION, ERRORS and END sections.
- Reports are never published under the web root. The former web-served /downloads/chatgpt-debug-* channel was retired on 2026-09-27 and its artifacts were quarantined.

### Transport
- Preferred: pipe any block into `~/bin/ai-report "task"` on A2, i.e. `( commands ) 2>&1 | ~/bin/ai-report "task"`. The report is written to /home/darwus/ai-reports, secret-scanned (passwords, keys, token links, email and IP addresses block publication), and pushed to evidence/skyhawk/<Report-ID>.txt in this public repository. Gene pastes only the one-line result; the AI reads the report from Git (clone, not the cached raw URL). Blocked or oversized reports stay local. Never pipe output that may contain member personal data. Reports are pruned after 30 days.
- Reports and exports move as files: scp from A2 to Gene's working folder on Windows, then upload to the executing AI. Short results may be pasted.
- Shared working state does not travel in reports. It lives in LOST-D in Git, which every executor reads directly from its public URL.

### Consumption
- The executing AI validates the Report-ID and currentness before using a report as evidence.
- Target state: evidence reaches the AI without Gene acting as the transport layer.

### Evidence Discipline

- Never place passwords, private keys, session cookies, API keys, active upload tokens, personal data, database credentials, or other sensitive material in diagnostic reports or transport copies.

- Capture enough evidence to determine the next state, not thousands of irrelevant lines.

- Do not overwrite or supersede evidence required for the next decision before the AI has consumed and validated it.

- Every failed transport test must narrow the search space. Do not revive a closed branch without new contradictory evidence or a newly available platform capability.

- When an automated candidate passes the acceptance gate, update this section immediately and remove the temporary manual-relay exception.

## 7. Living Reference System

- Reference continuously, update immediately. The /blade/ reference pages are the persistent operating state of skyhawk.org, not historical notes.

- $1

Shared passdown. LOST-D in Git (projects/skyhawk/LOST-D.md, public URL) is the shared working state for every executor. Claude and ChatGPT are both authorized executors, used one at a time as Gene chooses; neither needs the other's agreement unless Gene asks for the tunnel. Every session starts by reading LOST-D and these Rules from Git. Every verified consequential step updates LOST-D (last verified step, next step, open decisions, half-done work) and pushes it in the same run as the change. Never put passwords, keys, token links, member personal data or backup contents in LOST-D.

Near a usage limit. When Gene says a usage limit is near (for example 90 percent), or a response starts running long, the executor does the handover first: a paste-ready command that brings LOST-D current and pushes it, plus the one-sentence resume instruction for the next AI. No new work starts until that is done, and responses stay short from then on.

- Code and documentation are one transaction. When Gene and the AI agree during a session to a material architecture decision, path, procedure, convention, completed feature, or changed system state, update the appropriate reference page during that same work session as part of the change.

- Do not postpone documentation until the end. If direction changes during coding, update the reference page as soon as the new direction is settled so obsolete instructions do not poison the next step or next session.

- One source of truth per subject. Keep detailed facts on the appropriate subject page and link to them rather than maintaining conflicting copies.

- Read the subject page again when the task crosses a boundary. A change from Drupal configuration to Termux workflow, upload-token behavior, menu structure, Mac backup work, squadron modernization, or another documented subsystem requires consulting that subsystem's reference before continuing.

- Document supersession explicitly. When a durable rule changes, replace the obsolete rule on its authoritative page and state what the new rule supersedes when ambiguity would otherwise remain. Do not leave mutually contradictory instructions for the next machine to arbitrate.

## 8. Existing Binding Site Rules

- Respect limited-answer requests. If Gene requests Yes/No only, answer Yes or No.

- Use the word "hero" only for someone who did something heroic.

- No Drupal messenger()/status popups for Skyhawk custom forms. Form/action results render inline using the established PageMessageTrait pattern in skyhawk_site_fixes/src/Traits. The known skyhawk_gallery/PhotoContributionForm.php exception is not a pattern to copy and is not authorization for a side project.

- Downloaded scripts are ZIP files rather than loose plain-text script downloads.

- For squadron work, follow the Squadron CMS (content type squadron; see LOST-D and the Environment Reference) rather than one-node patches. The earlier body-marker squadron template is superseded for new work (Gene, 2026-09-27).

## 9. Cleanup, Retention, and Backup Discipline

- Cleanup protects surviving work; tidiness is not the objective. Never delete material merely because it is old, unfamiliar, inconvenient, or apparently unused. Unknown material must be investigated before deletion.

- Clean at verified logical stopping points. Temporary scripts, probes, test uploads, verification files, abandoned experiments, superseded implementations, duplicate artifacts, and other known disposable material should not accumulate indefinitely. Remove them after their purpose is complete and the surviving implementation has been verified.

- WHATIF/inventory before meaningful bulk deletion. First identify exactly what would be removed, what would remain, and why. Perform the destructive step only after the inventory establishes that the candidates are safe to remove.

- Drupal content is not disposable housekeeping. Preserve legitimate nodes and content. Test nodes, abandoned prototypes, duplicates, or superseded temporary nodes may be removed only after identifying and verifying the surviving replacement. Do not create new nodes when editing the established canonical node is the correct operation.

- Drupal revisions are distinct from duplicate nodes. Revision growth may be audited periodically, but revision history must not be blindly purged merely to reduce database size.

- Diagnostic-report retention is 30 days. Reports in /home/darwus/ai-reports and related AI diagnostic files may be pruned after 30 days. Diagnostic cleanup must not be confused with deletion of site content or historical source material.

- A2 is not the long-term database-backup repository. Database dumps created on A2 during maintenance are temporary working/transfer artifacts unless explicitly designated otherwise. Do not accumulate redundant database archives on the same hosting account as the live database.

- The established Mac database-backup workflow remains authoritative. The Mac already downloads the Drupal database nightly. When work is being performed from the Mac and a newer database copy is required, replace/update the latest local backup using the already-established Mac replacement and retention pattern. Do not redesign that working retention scheme as part of unrelated Drupal work.

- Protect before removing. A consequential change may require a temporary A2 backup for immediate rollback. Once the change is verified and the data is safely represented by the established backup process, remove unnecessary A2 temporary copies rather than allowing them to become accidental permanent archives.

- Deletion requires knowledge. "I do not recognize this" means inspect it. "This is positively identified as temporary, duplicate, abandoned, superseded, or safely backed up" means it may become a cleanup candidate.

## 10. Reference Pages

- Drupal Environment Reference — environment, modules, directories, and established code patterns.

- Squadron Modernization Roadmap — North Star, modernization classes, census data, and current phase.

- $1 Superseded for new squadron work by the Squadron CMS (Gene, 2026-09-27).

- Upload Token System — token/contact/notification architecture and current state.

- SDO System Status — SDO mechanism and current state.

- Site Menu Reference — menu machine names and established structure.

- Termux SSH Notes — mobile SSH workflow and constraints.

- Windows Tooling Notes.

- Mac Tooling Notes.

## 11. Continuity Test

A future AI agent or maintainer should be able to read this page, resolve the applicable references, establish the current state without rediscovering settled facts, make the smallest correct update-safe change, validate it, capture evidence, verify it, update the durable reference state, clean only proven disposable artifacts, and continue without reopening completed work.

Operating shorthand: reference authority → inspect actual state → agree → compliance gate → implement → lint → execute → capture → verify → update reference → conservative cleanup → next task.

If the workflow begins to drift, stop the affected action, preserve the session and surviving state, identify the exact rule or evidence conflict, correct that specific problem, and only then resume. The goal is deterministic external behavior from a probabilistic tool: creative in diagnosis, disciplined in execution, and boring enough to keep airplanes flying.

## KISS and Deterministic Work

KISS: Keep It Simple, Stupid.
Use the simplest maintainable method that satisfies the proven
requirement. Complexity requires justification. Do not add custom
code, instrumentation, validation layers, workflows, abstractions,
diagnostic gates, or other machinery merely because they are
possible.

- Test outcomes, not implementation trivia.
Determine whether the required user or business outcome works.
Inspect internal transitions only when that outcome fails, and only
deeply enough to identify and repair the failure.

- Honor proven progress.
Once functionality has been accepted, move forward unless new
evidence contradicts it. Do not repeatedly reopen completed work.

- Isolate failures.
A failure authorizes investigation of that failed requirement, not
a general reaudit or redesign of unrelated working functionality.

- Read before changing.
When live state is uncertain, inspect the actual current
configuration, source, database state, Rules, and applicable
reference before modifying anything.

- Know and replace.
Do not guess and append competing code or configuration when an
existing owner can be identified and changed cleanly.

- Let Drupal be Drupal.
Prefer Drupal core, configuration, Views, and maintained contributed
functionality. Add custom mechanisms only when the actual
requirement cannot reasonably be satisfied otherwise.

- Keep evidence concise.
Routine work reports should state what was found, what changed,
PASS/FAIL, meaningful evidence, and the next action. Do not build
forensic reporting systems for already-proven behavior.

#### Personal-data ownership before removal

When personal information appears on an inappropriate page,
identify both the storage owner and the render owner before changing
anything. User/profile data rendered through article authorship is
not node content merely because it appears on a node page.

- If personal information is authoritative user/account data,
preserve it and suppress the inappropriate presentation at the
narrowest proven render owner.

- If personal information is a duplicate stored specifically in
page content, remove the unnecessary duplicate.

- Do not delete authoritative member information merely to correct
an inappropriate public presentation.

- Prefer Drupal-managed users, roles, configuration, mail services,
and other maintained Drupal mechanisms when communication can occur
without exposing private contact information.

- Verify privacy corrections against the actual rendered public
page, not merely configuration, lint, or assumed ownership.

### Semantic Visual Design

Skyhawk.org uses a small global semantic visual vocabulary rather
than inventing page-specific decorative CSS. HTML identifies what
content means; global CSS controls how that meaning appears.

- skyhawk-focus - current or primary purpose.

- skyhawk-feature - person, squadron, aircraft,
creator, honoree, event, or other principal subject.

- skyhawk-context - supporting explanation.

- skyhawk-note - secondary information.

- skyhawk-reference - references,
administrative information, and related material.

Optional identity modifiers are
skyhawk-navy,
skyhawk-marine,
skyhawk-joint, and
skyhawk-heritage.
Navy blue, Marine scarlet, gold, khaki, slate, and neutral colors
form the common palette. Bold colors are punctuation; muted colors
are prose. Color never carries meaning by itself.

Do not automatically color every paragraph or legacy page.
Apply semantic blocks where they improve hierarchy. Prefer the
existing global vocabulary over new CSS. Add a new semantic class
only when a proven requirement cannot reasonably use the existing
system. Keep mobile readability and accessibility intact. KISS.

## Deterministic Execution Gate

Purpose: Convert the Rules, LOST-D, and germane references from material that is merely read into constraints that control the next action.

- MISSION. Before substantive discussion or executable work, identify the single current objective from LOST-D and its hard scope boundary. Do not pursue adjacent work.

- LOCATION. Establish the actual execution location before generating commands. Normal Skyhawk command-line work assumes the user is already at the interactive A2 prompt unless current evidence proves otherwise. Do not invent hosts, aliases, shells, paths, or execution environments.

- KNOWN. Extract the settled facts relevant to the current action from the Rules and germane references. Proven and documented facts are authoritative until current evidence contradicts them. Do not rediscover, redesign, retest, or reopen completed decisions without new evidence or explicit user direction.

- ACTION. Perform one meaningful state transition broad enough to accomplish the agreed step. Prefer the simplest proven method. Do not add instrumentation, abstraction, safeguards, audits, or side work that do not materially improve the required outcome.

- STOP. Define success, failure, and NEXT before execution. A failed prerequisite prevents later success output. After the result, verify the state, reread LOST-D, update durable documentation when required, and continue from the last proven state.

### Human-AI Friction Gate

- If the user must repeat an already documented instruction, treat the reminder as evidence that retrieval or execution discipline failed.

- If the same governing instruction must be repeated again during the same workstream, stop expanding the task. Correct the retrieval/enforcement failure first, then resume from the last proven state.

- User frustration is an operational signal when it results from repeated reminders, reopened completed work, unnecessary complexity, failed code blocks, or ignored scope.

### Execution Contract

Before generating executable code, the AI must be able to state internally and unambiguously:

- MISSION: What single objective is being advanced?

- LOCATION: Where will this command actually run?

- KNOWN: Which settled facts control this action?

- ACTION: What one meaningful state transition will occur?

- STOP: What proves success or failure, and what is NEXT?

If any required field cannot be established from the current conversation, LOST-D, Rules, germane reference, or current proven output, do not invent it. Retrieve the missing fact first.

KISS applies to the collaboration itself: prefer fewer assumptions, fewer moving parts, fewer prompts, fewer rediscoveries, and fewer opportunities for improvisation.

### Complete Code Window Rule

- Once executable code is authorized, provide one complete working code block for the agreed step whenever one block can reasonably perform it.

- If a supplied executable block needs correction before execution, replace the entire corrected block in a new code window.

- Never instruct Gene to splice, patch, merge, substitute, or manually combine executable fragments from separate code windows.

- A correction supersedes the prior unexecuted block in toto. The prior block is invalid and must not be partially reused.

- The only normal exception is a workflow that necessarily changes execution environments, such as the established A2-to-local backup-download and reconnect procedure.

## AI Execution Core

Purpose: These eight invariants govern AI-generated Skyhawk maintenance. They replace overlapping AI-process rules. Do not create another AI-process rule when correcting the implementation of one of these invariants.

### 1. Facts Before Code

- The AI must verify every material fact required by executable work before depending upon it. Assumptions about paths, executables, shell behavior, ownership, dependencies, Drupal state, Git state, hosting capabilities, prior commands or human actions are forbidden.

- When uncertainty exists, inspect read-only first. A convenient local observation must not be generalized beyond what the evidence proves.

- The AI must think both backward and forward: verify current state and identify routine future actions that could make the solution stale, unsafe or incomplete.

### 2. AI Owns Deterministic Execution

- Because AI writes nearly all Skyhawk maintenance code, correct paths, working directories, execution context, command grammar, prerequisite checks, stop behavior and verification are primarily the AI's responsibility.

- Location-sensitive code must explicitly enter and verify its canonical working directory. Never rely on the human's current directory, inherited shell state or a previous command.

- Automation must explicitly use proven executables and environment facts rather than depend on interactive aliases or PATH behavior unless that behavior itself is the intended, proven mechanism.

- Shared-hosting work must remain within the authorized user/account/project boundary unless the human explicitly authorizes a broader change that the host permits.

### 3. Evidence Automatically Controls the Next Step

- When executable work creates an authoritative or immutable report, the AI must retrieve and read it automatically before diagnosis or further executable work.

- The human must never have to tell the AI to read evidence generated by the AI's own workflow.

- Failure diagnosis must come from actual evidence, not intended behavior, memory, assumptions or footer wording.

- When only one safe evidence-supported AI-owned next action remains, the AI must provide that executable action automatically in the same response. The human is not required to ask "next."

### 4. A Response Cannot Promise Its Own Missing Work

- If NEXT identifies an unperformed AI-owned executable action, the response is incomplete and must continue until that action is supplied.

- A response may stop only for genuine human judgment/action, unavailable required evidence, a safety/authorization boundary, or completed work.

- Writing "NEXT: AI will provide code" without providing the code is a failure.

### 5. Executable Blocks Must Fail Closed

- Every executable block must begin with the literal first line # RULES + GERMANE REFERENCE READ.

- AI-generated blocks must use control flow that is valid for the actual shell/context and mechanically prevents later mutating steps after a failed prerequisite.

- Do not use top-level shell constructs that cannot stop the running context. Test shell syntax before mutation when practical.

- PASS, FAIL, UPDATE REQUIRED, BACKUP REQUIRED and NEXT must reflect gates that actually completed. Intended results never override execution evidence.

- After a failure, repair the proven failure only. Do not reopen completed work or redesign unrelated components.

### 6. One Complete Code Window

- Once executable work is authorized, provide one complete working code block whenever one block can reasonably perform the agreed step.

- If an unexecuted block needs correction, replace it completely in a new code window. Never require the human to splice, patch, merge or combine executable fragments.

- The prior unexecuted block is superseded in toto.

- The established local-download/reconnect workflow is the normal exception when execution necessarily crosses environments.

### 7. Durable State, Minimal Rules

- When a human correction exposes a broadly reusable requirement, the AI must first verify whether an existing Rule already covers it.

- If covered, fix the implementation rather than adding another Rule. If genuinely new, update the smallest appropriate Rule or germane reference in the same successful transaction and independently reread it.

- Environment-specific facts belong in germane references; universal behavior belongs in Rules.

- Critical workflow state should live in durable references, reports or deterministic wrappers rather than depend upon conversational memory.

- KISS governs both code and rules: use the simplest maintainable mechanism that satisfies the proven requirement.

### 8. Human / AI Boundary and Completion

- The AI owns evidence retrieval, deterministic reasoning, command construction, environment verification, automatic continuation and technical bookkeeping.

- The human is required only for genuine choices, authorization, credentials, physical-device action, visual/functional judgment or policy decisions.

- Do not transfer an AI obligation to the human by calling the human an operator.

- Before declaring a workstream complete, verify not only today's result but the routine future maintenance path, backup/recovery relationship, documentation state and deterministic mechanism that keeps the solution current.

- Closed and proven work stays closed unless new evidence invalidates it.

### Composer / Git Completion Gate

- Normal Skyhawk dependency maintenance uses /home/darwus/drupalbeta/bin/skyhawk-composer.

- skyhawk-composer update is the normal full-update command. Package names or Composer options may follow for targeted updates.

- require and remove use the same pending maintenance lifecycle. install reconstructs from composer.lock and must not change tracked reconstruction architecture.

- Before mutation, Git must be clean and local HEAD must match origin/main.

- After mutation, Drupal database updates and cache rebuild run before the transaction becomes pending.

- finish is the explicit human functional-acceptance and publication act.

- finish requires zero active-vs-sync Drupal configuration differences.

- The staged set is safety-checked and Composer-validated before commit.

- Maintenance is complete only after push and exact local/remote commit parity.

- Composer hooks must never automatically commit or push.

MEMORY USE RULE: Do not use conversation history, model memory, prior-chat recollection, shared/project memory, or any other stored conversational memory unless Gene explicitly asks for memory to be used in the current task. If Gene does not explicitly authorize memory use, do not consult, rely on, or cite it. Use the current Rules, germane references, verified live state, and current evidence instead.
