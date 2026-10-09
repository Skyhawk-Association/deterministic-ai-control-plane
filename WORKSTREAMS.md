# DACP Workstream Registry

**Status:** CANONICAL PUBLIC-SAFE NAVIGATION INDEX

Git is the canonical owner of this registry. Local copies on Gene's Envy, Mac, and Pixel are mirrors only and never override Git.

This file is a navigation index. It does not replace CURRENT.md, project-specific authoritative references, or verified live state.

## Status vocabulary

- **ACTIVE** - work presently being executed.
- **WAITING** - blocked on an external response, event, or dependency.
- **OPEN** - valid unfinished work available to resume.
- **PARKED** - intentionally not being worked now.
- **CLOSED** - accepted complete unless new evidence reopens it.
- **REFERENCE** - retained for context/tooling history, not active work.

## Evidence classes

- **VERIFIED** - established by current live evidence or authoritative source.
- **USER-STATED-EXPLICIT** - explicitly stated by Gene but not independently verified.
- **INFERRED** - navigation judgment from available evidence.
- **UNRESOLVED** - insufficient, contradictory, ambiguous, or stale evidence.

INFERRED is useful for navigation but is not operational fact. Before consequential work resumes on an INFERRED workstream, verify its current endpoint from authoritative sources, current user-provided evidence, or live system state.

## Workstreams

### DACP - Deterministic AI Control Plane

- **Status:** ACTIVE
- **Evidence:** VERIFIED
- **Canonical sources:** CURRENT.md; active authoritative controls; STATE_LOCATOR.json.
- **Scope:** DACP governance, control enforcement, state/evidence pipes, executor behavior, implementation, and handoff integrity.
- **Source chats represented:** Bootstrap DACP Plan; Reconstruct Project State; Skyhawk State Handoff; Resolve Documentation Owner; Verify And Repair DACP; DACP Landscape Scan; DACP Competition Watch; Infrastructure Planning Summary; related DACP handoffs.
- **Resume rule:** CURRENT.md first, then germane authoritative files and current private operational state.
- **Next:** Continue only from current canonical Git and current private state. Older chats are provenance, not governing authority.

### IM - Skyhawk / InMotion migration and hosting closeout

- **Status:** WAITING
- **Evidence:** VERIFIED
- **Canonical source:** projects/skyhawk/LOST-D.md.
- **Scope:** InMotion VPS production state, provider support, PHP 8.4 native runtime defect, CWP configuration consistency, TLS/vhost state, migration closeout, A2 retirement gates.
- **Current external dependency:** InMotion ticket #143036800.
- **Source chats represented:** Migration Handoff Summary; Skyhawk migration final update; A2 Backup Cleanup; SSH Setup for Backup; Drupal Login Error Troubleshooting; System Update Summary; related migration/support chats.
- **Resume rule:** Read projects/skyhawk/RULES.md and LOST-D.md, then independently verify any provider claim or server change.
- **Next:** Await InMotion response. Site reachability alone does not close the native PHP or configuration investigation.
- **503 handling inspection (VERIFIED, 2026-10-08):** No active Skyhawk-specific 503 handler/template exists. Drupal maintenance mode cannot cover PHP-FPM/backend loss. The graceful-failure owner is the front web-server layer. Next is a CWP-compatible, regeneration-safe static 503 design and non-disruptive test; no implementation has yet been made.
- **HTTP error handling map (VERIFIED / DISCUSSION, 2026-10-08):** 404 currently reaches Drupal and renders the branded Bolter! page, so normal application-level 404 belongs to Drupal. Front-layer 403 is currently a generic nginx page; nginx/ModSecurity also generate security-layer 403 responses before Drupal, so those belong at the front web/security layer. Hard 5xx failures that can occur when PHP/Drupal is unavailable (500/502/503/504) also belong at the front web-server layer with static fallbacks. Application-level 403/404 may remain Drupal-owned when Drupal is healthy.
- **Alerting design candidate (INFERRED, 2026-10-08):** Do not email on every 403/404. In the latest 5,000 access-log entries there were 143 404s and 139 403s, much of which is normal scanning/bot traffic. Prefer external uptime monitoring for site-down/5xx detection, plus local log/event aggregation for diagnosis. Candidate policy: immediate alert on repeated 502/503/504 or sustained 5xx; threshold/digest treatment for 403/404; optional targeted alert for known high-value URLs. No alerting implementation has been made yet.
- **Error/alert design (USER-STATED-EXPLICIT + VERIFIED DESIGN, 2026-10-08):** Gene approved design. Canonical design: projects/skyhawk/HTTP_ERROR_HANDLING.md. Implementation has not started. Exact regeneration-safe CWP template owner/path remains UNRESOLVED pending root-capable inspection; generated vhosts must not be edited as the durable mechanism.
- **Status update (VERIFIED, 2026-10-09):** supersedes "implementation has not started" above. Static 5xx fallback and scoped static 403 are live via the CWP skyhawk-errors template; UptimeRobot is the verified primary external monitor; DKIM/SPF/DMARC pass; public diagnostic leftovers quarantined. Only InMotion ticket #143036800 remains external. Details: projects/skyhawk/LOST-D.md.


### NAS - NAS, archive, and backup architecture

- **Status:** OPEN
- **Evidence:** INFERRED
- **Source chats represented:** Update NAS checkpoint; NAS build overview; Mac as Master Archive; Search Synology Drive PDFs; Mac mini setup guide.
- **Scope:** NAS design/use, archive ownership, backup placement, searchable document storage, and Mac/archive interaction.
- **Resume rule:** Inspect the latest NAS checkpoint and current device/storage state before changing architecture or declaring completion.
- **Next verification:** Determine the latest accepted NAS topology and unfinished tasks.

### SITE - Skyhawk site backlog and Drupal presentation/content work

- **Status:** PARKED
- **Evidence:** INFERRED
- **Authoritative sources when resumed:** projects/skyhawk/LOST-D.md; projects/skyhawk/RULES.md; germane subject references; live Drupal state.
- **Source chats represented:** Modeling Page Recommendations; Skyhawk Songs Drupal Issue; Drupal Views Grid Fix; Website code recommendations; Skyhawk Photo Upload; Reunion Page Setup.
- **Scope:** Drupal Views, page/modeling presentation, songs/content issues, photo/reunion features, and site modernization not on the migration critical path.
- **Resume rule:** Inspect the current Drupal owner/configuration/live behavior before modifying anything.
- **Next verification:** Select the next backlog slice and establish its current owner and live state.

### AVI - Joint aviation platform / organizational future

- **Status:** PARKED
- **Evidence:** INFERRED
- **Source chats represented:** App for Skyhawk.org; Joint Naval Aviation Platform; Organizational vs Tech Strategy; Aviation Organization Naming; VMA131 Integration with Skyhawk; Create Aviation Logo.
- **Scope:** Future cross-aircraft/joint aviation organization and app/platform strategy, unit-material integration, branding, and organizational structure.
- **Resume rule:** Separate accepted decisions from brainstorming before implementation.
- **Next verification:** Establish the current approved mission/scope and latest accepted platform concept.

### PIPE - Photo and file-transfer pipeline

- **Status:** OPEN
- **Evidence:** VERIFIED
- **Source chats represented:** Pipeline File Transfer Issues and related photo-organization/file-transfer work.
- **Scope:** Photo import, organization, transfer, device-to-computer pipeline, and related scripts/workflows.
- **Bedrock decision 2026-10-09:** The Mac Pixel archive workflow is the authoritative foundation for future photo/file-transfer work. The Windows/Envy pipeline remains historical comparison evidence only unless deliberately reintroduced.
- **Verified Mac implementation:** `/Users/m4/Scripts/pixel_archive_sync.py` (engine) plus `/Users/m4/Scripts/pixel_archive_resilient_runner.py` (runner, Mac-local state) and `/Users/m4/Scripts/pixel_sms_prune.py`, launched through `/Users/m4/Applications/Pixel Archive Monitor.app` (polls about every 15 s). The workflow never silently overwrites archive files (changed files land as `__pixel_<sha8>` copies), SHA-256 verifies transfers, skips identical cataloged content, and resumes large files in 256 MiB chunks. The only phone deletion is the approved SMS rule below. Backups of every replaced script are in `~/Scripts/Archive/` (`*.pre-20261009-*`, `*.pre-cachefix-*`, `*.pre-smsprune-*`, `*.pre-snapfix-*`).
- **Bedrock validation 2026-10-09 (Claude): ACHIEVED.**
  - Delta: the 17,815-row plan resolved to 6,483 verified and present, 10,794 duplicates present, 5 trivial missing duplicate targets, and 532 new or changed (37.7 GB). After the approved rules that became 185 (18.6 GB). A 200-file archive re-hash sample showed 0 mismatches.
  - Prior unresolved items: the 4 failed rows (SMS Aug 17, Oct 2 and Oct 3, plus calls Oct 3) are no longer on the phone and are superseded by newer full backups. They remain `failed` in state as historical rows. The Oct 3 failure mechanism was ArchiveSSD dropping off the UGREEN dock at 09:48:50, then the phone at 10:00.
  - Gene-approved changes: (1) ArchiveSSD unmount guard, which pauses and preserves progress; (2) Android app-cache exclusion (any path part containing `cache`, e.g. spotifycache); (3) only the newest SMS/calls full backup is archived per session; (4) 4 orphaned staging partials deleted by exact name and size (15.36 GiB).
  - Defects found and fixed: (a) the runner's 1-second adb-state cache started at monotonic 0, and `time.monotonic()` is about 0 per process on this Mac, so every run, including every `--auto` run, saw the phone as "not connected" during its first second. Automatic transfer could never have copied anything. Fixed by initializing the cache timestamp to -inf. (b) The runner wrote a 16 MB state snapshot to ArchiveSSD after every 15-second monitor pass (717 byte-identical duplicates, 11.1 GiB). It now snapshots only after a real transfer run, and the duplicates were removed with the 7 distinct snapshots kept.
  - Controlled live run 2026-10-09 12:38-13:07 EDT: COMPLETE, verified=4,668, duplicate=10,665, failed=0. This run wrote 160 rows (146 newly copied, 14 duplicates skipped), including sms-20261009005805.xml (19.8 GB) and calls-20261009005805.xml. The transfer continued normally with the phone screen locked.
  - Independent verification: 160/160 archive files re-hashed match the recorded SHA-256 (18.59 GiB re-read), 146/146 phone-side `sha256sum` match, and staging is empty. `automatic_transfer_approved` was then restored; the paused marker is gone.
- **SMS phone-pruning rule (Gene decision 2026-10-09):** delete from the Pixel only `SMS Backup/sms-<14 digits>.xml` and `calls-<14 digits>.xml` files that are older than the newest same-kind file recorded verified in state AND re-proven by size plus SHA-256 on both the phone and ArchiveSSD. The newest is never deleted. Any check failure means nothing is deleted for that kind. It runs only after a real transfer run. Backup frequency stays nightly (Gene decision). First application on 2026-10-09 deleted the Oct 8 sms and calls pair (19.83 GB). The phone now holds only the Oct 9 pair.
- **Mac power (verified via pmset):** `sleep 0`, `standby 0`, `displaysleep 10`, `ttyskeepawake 1`, `womp 1`, `tcpkeepalive 1`, `autorestart 1`. The Mac does not idle-sleep, so unattended runs are safe while it stays powered and ArchiveSSD stays docked.
- **Side findings (not acted on):** the archive already holds about 6.9 GB of Spotify cache (2,444 files) copied before the cache rule. SMS Backup & Restore writes a full ~19.8 GB XML nightly (the MMS media is the bulk).
- **Current safety state:** automatic transfer is ENABLED. The monitor runs one transfer per connected session, so while the phone stays plugged in, new files (including the nightly SMS backup) wait until the next unplug and replug.
- **Next:** (1) watch the first unattended session after the next nightly SMS backup, then confirm the prune log removes the prior day's pair; (2) decide on purging the archived Spotify cache; (3) fold Mac and Envy "away from the computer" resilience into the NAS transition (Gene, 2026-10-09: the NAS is meant to enable this).
- **Evidence:** `evidence/pipe/20261009T173500Z-mac-pixel-bedrock-validation.txt`; raw reports in Mac `~/ai-reports/pixel-*-20261009_*`.

### TOOL - Computer, network, and ChatGPT tooling reference

- **Status:** REFERENCE
- **Evidence:** INFERRED
- **Source chats represented:** PowerShell chats; Codex UI Troubleshooting; GitHub login issue; Chat Token Limit Issue; Assistant settings summary; ChatGPT instance visibility; Business accounts comparison; RJ45 Command Line Check; LAN subnet change advice; UniFi AP Group Setup; related workstation/network troubleshooting.
- **Scope:** Environment/tooling history that may become germane when a matching operational problem returns.
- **Resume rule:** Reinspect the current device/product/network before relying on old troubleshooting steps.
- **Next:** None while no matching problem is active.

## Mirror and access model

**Canonical owner:** Git repository main branch.

**Intended mirrors:**
- Envy - local Git clone.
- Mac - local Git clone.
- Pixel - local Git clone to be established and qualified.

A mirror is current only when its checked-out commit matches canonical Git main and WORKSTREAMS.md matches the canonical content for that commit.

## Update discipline

When workstream truth changes:

1. Update the workstream's authoritative/current-state source first when one exists.
2. Update this registry only to reflect the new navigation/status truth.
3. Preserve the correct evidence class.
4. Commit to Git.
5. Independently read back canonical Git.
6. Refresh device mirrors and verify commit/content identity before calling them current.

Do not make independent edits on multiple devices and reconcile later. Git is the owner; devices consume it.
