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
- **Verified Mac implementation:** `/Users/m4/Scripts/pixel_archive_sync.py` plus `/Users/m4/Scripts/pixel_archive_resilient_runner.py`, launched through `/Users/m4/Applications/Pixel Archive Monitor.app`. The sync engine self-test currently passes. ArchiveSSD is mounted. The workflow is non-destructive to the phone, never silently overwrites existing archive files, SHA-256 verifies transferred files, skips identical cataloged content, and supports resumable large-file transfer.
- **Verified latest Mac preflight:** 2026-10-03 09:26 EDT inventoried 25,586 phone files, planned 17,920 after excluding 7,666 reproducible cache/temp files, and passed the free-space gate with 107.28 GiB worst-case planned data.
- **Verified latest transfer evidence:** the 2026-10-03 run copied/verified Pixel camera files through 2026-10-03 and reached 17,914/17,920 before later SMS-backup failures and eventual pause on device disconnect. Therefore the Mac workflow is proven functional but the most recent run was not cleanly complete.
- **Safety state for bedrock test:** automatic transfer approval has been intentionally paused by renaming `automatic_transfer_approved` to `automatic_transfer_approved.paused-bedrock-test`, preventing the monitor from mutating ArchiveSSD while the foundation is revalidated.
- **Next verification:** Connect and authorize the Pixel 10 to the Mac for ADB, then run a read-only Mac preflight/census first. Confirm current phone inventory, planned delta, exclusions, ArchiveSSD space, and the exact six unresolved 2026-10-03 items before restoring automatic-transfer approval or running a live synchronization.

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
