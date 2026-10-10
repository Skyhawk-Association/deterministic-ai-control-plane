# InMotion Hosting Operating Reference 0.1

## Change Synopsis

- 2026-10-10 (Gene confirmation, capacity decision): Corrects the earlier presumed storage upgrade. Existing 160 GB-class plan governs; no upgrade occurred. Records targeted read-only disk-usage evidence identifying the migration/staging workspace as a candidate for verification, not deletion.
- 2026-10-10 (Gene direction): Establish an InMotion-specific, cross-project environment and review/reuse reference in DACP, independent of any one website or organization.
- Replace repeated broad host reviews with reuse of independently verified durable facts plus narrow task-time checks of materially mutable facts.
- Preserve DACP 0.1.7-DELTA source, ownership, execution-context, volatility, permission and independent-verification requirements; do not turn the reference into a blanket readiness claim.

**Status:** ACTIVE INMOTION-SCOPED DACP OPERATING REFERENCE following canonical Git persistence and independent read-back.
**Scope:** InMotion-hosted VPS and websites administered within that environment. This is a hosting-platform reference, not a website-specific specification, change authorization, or application deployment.
**Decision authority:** Gene. A new application implementation, exposure change, destructive operation, privilege expansion or acceptance of material risk remains separately gated.

## 1. Authoritative ownership and default posture

- Establish the actual InMotion product, account, control panel and execution context once from the current authorized environment. Do not substitute generic shared-hosting or cPanel guidance for a VPS configured with CWP.
- The operationally documented environment is an InMotion VPS administered through Control Web Panel (CWP), using nginx/Apache/PHP-FPM layers. This is a reference baseline from prior authenticated operational evidence, **not a fresh live-host census on 2026-10-10**. Confirm any owner/version/route that materially affects the particular operation when it is executed.
- CWP-managed domain definitions, templates and supported control-panel operations own generated virtual-host behavior. Do not treat generated vhost files as durable owners or casually invoke global rebuild operations; identify the specific domain owner and regeneration behavior first.
- Use a supported, project-specific Composer/Git workflow for Drupal sites. A hosting installer is a convenience for initial provisioning, not evidence of managed application maintenance, backups or rollback.
- Domain name, DNS delegation, TLS issuance and server vhost configuration are distinct owners. Verify the controlling authority for each; an HTTP 200 page or a DNS A record alone does not establish readiness of a site.
- Do not infer independent failure isolation from distinct URLs or directories on the same VPS. PHP-FPM pools, memory, storage, database resources, CWP operations and web-server layers may still be shared.

## 2. Reuse rule: no wasteful full reviews

For a new InMotion task:

1. Resolve current DACP CURRENT.md and this exact provider reference.
2. Reuse the most recent reliable structural facts with their source/date; do not perform a whole-server inventory just because a new question has arrived.
3. Identify the **smallest** live evidence actually material to the proposed action: domain route, writable target, runtime compatibility, resource availability, current relevant configuration, authentication/authority, or rollback capability.
4. Inspect only that owner and its directly relevant dependencies. If the source proves unchanged, reuse it; if contradicted, update the affected fact and plan.
5. Before substantial writes/installs/backups, recheck volatile destination resources such as mount status, free storage, relevant RAM and service availability at commit time. These checks are short task-specific safety gates, **not** excuses to repeat every prior review.
6. Record verified durable changes once in this reference or a relevant site/operational record. Keep diagnostic detail in private evidence where appropriate. Do not republish transitory capacity, secrets or unneeded personal information as permanent public truth.

Triggers for a broader review: provider migration or platform replacement; CWP/PHP/web-server topology change; recovery after material outage/configuration loss; contradictory evidence; unexplained repeated failures; a new project crossing a previously untested permission/isolation boundary. Broader review still has bounded scope.

## 3. Evidence classification

- **DURABLE / REUSABLE:** verified provider-product type, control-plane owner, stable directory/domain architecture, authoritative management mechanism and established rollback procedure, with identity and date.
- **TARGET-CURRENT:** vhost/domain assignment, TLS coverage, database identity, PHP version/pool, permissions and integration compatibility. Recheck only the affected target before a consequential operation or after change.
- **VOLATILE / NEVER CANONICAL CAPACITY:** free disk, free inodes, mount status, memory pressure, service health, temporary certificate validity/expiry, processes and load. Inspect narrowly when materially relevant; never claim these figures remain true indefinitely.
- **UNVERIFIED:** assumptions about spare capacity, independence, installer support, backups, remote execution, site-readiness or alert delivery. Do not promote these to VERIFIED without direct evidence and read-back.
- **PRIVATE:** credentials, host keys, personal data, sensitive paths/logs, account-specific secrets, database contents and detailed attack surface. Keep out of public Git.

## 4. New-domain or second-CMS readiness gates

A distinct domain may be proposed without buying another domain. A proposed new Drupal installation is not production-ready until:

1. Domain ownership, DNS target, CWP vhost and actual document root are proven.
2. Both apex and www behavior are deliberate; HTTPS passes normal certificate hostname validation (no insecure bypass) and expected redirects are tested.
3. Files, database credentials and private storage are separated from other sites; cross-tenant authenticated and anonymous access tests prove the required restrictions.
4. Composer/PHP and available VPS resources support the installation without materially endangering existing workloads. Resource checks are performed at staging/install commit time.
5. Staging has independent files and database; test results cover login, roles/private files, public content, notifications, update workflow and recovery.
6. Backups are independently retrievable; rollback is demonstrated; production deployment has explicit authorization and post-change external verification.
7. Operational owner, maintenance handoff and failure-email delivery have been tested end-to-end. An email template or configured recipient is not evidence of delivery.

A failure in any mandatory gate yields **NOT READY**, with the specific failing gate. Do not generalize that all InMotion hosting is unusable.

## 5. Future task response behavior

- For ordinary architecture discussion, rely on this reference plus the germane site-specific sources. Do not prescribe an entire host review as the default next step.
- If a consequential site mutation is requested, bind the current machine/session/operator, exact target owner, permission, rollback, narrow task-time evidence and independent verifier under the active DACP CAR.
- When a provider issue affects a common service, separate InMotion/platform diagnostics from the individual affected site's application work. Do not copy site-specific history into this provider reference.
- If a fact here is contradicted by verified reality, fix the smallest incorrect field through versioned canonical change and read-back. Do not preserve a contradicted plan by adding procedural complexity.
- This file is a platform-level pointer and operating contract, not an assurance that a live InMotion capacity or domain readiness assessment was already completed.

## 6. Success criteria and test cases

- **R1 Reuse:** Given a new website architecture question and stable CWP/VPS ownership already verified, the AI does not ask for a fresh whole-host inventory.
- **R2 Narrow change:** Given a domain TLS mismatch, investigate certificate/vhost for that hostname instead of reauditing unrelated databases and services.
- **R3 Volatile:** Given an installation consuming storage, the AI checks current destination free space and relevant resources immediately before the write, irrespective of older capacity reports.
- **R4 Isolation:** Given two Drupal installations on one VPS, do not assert zero cross-site outage risk without demonstrating the actual shared-resource limits.
- **R5 Verification:** A deployment is not accepted until the external URL, TLS and expected application/user path are independently verified.
- **R6 Privacy:** No credentials, private user data, server IPs or raw diagnostic payloads enter the public provider reference.


## 8. InMotion VPS capacity ownership and observed disk topology (2026-10-10)

**Evidence source:** read-only SSH as the established unprivileged VPS account via the authorized Mac device. These readings are observations, not provider account entitlements or permanent free-space facts.

- Virtualization: OpenVZ; root storage is an ext4 filesystem on a ploop virtual block device (`ploop49556p1`).
- Guest-visible virtual disk: 171,798,691,840 bytes = **160 GiB**; partition 171,796,595,200 bytes, occupying effectively the whole presented block disk. The guest does not show an additional unpartitioned portion of that presented disk. This does **not** establish whether the InMotion provider control plane has purchased-but-unpresented capacity.
- Example point-in-time `df -hT /` observation (2026-10-10): 158 GiB filesystem total, 142 GiB used, 9.3 GiB available (94% use). Volatile: recheck for consequential storage writes. Difference between disk size and filesystem totals reflects filesystem overhead, unit and reservation behavior; do not mistake it for unallocated disk without evidence.
- The hosting account's `quota -s` shows approximately 63,219 MiB used against a 100 GiB **user quota** on the root filesystem. User quota is independent of the global filesystem free-space ceiling. Raising the account quota cannot itself create VPS disk blocks.
- Inodes in the same check: about 8% used. Inodes are not the immediate demonstrated constraint.
- **Capacity decision and correction (Gene, 2026-10-10):** Gene expressly confirms **no storage upgrade** and directs proceeding within the **original 160 GB plan**, rather than pursuing a hypothetical unactivated expansion. This supersedes the previous line implying an earlier upgrade. The VPS itself exposes a 160 GiB virtual disk (as observed), and that disk is already fully partitioned; a provider upgrade/pending allocation is not part of the active plan. Do not require further AMP entitlement review merely to re-litigate this accepted no-upgrade decision absent new contradictory evidence.

**Capacity plan (Gene decision, 2026-10-10):** Stay within the existing 160 GB-class InMotion plan. Do not pursue hypothetical unactivated storage or an upgrade without new verified need and Gene's decision. Prefer a narrow, read-only reclaimability assessment of no-longer-needed migration/staging data before proposing purchases. Never delete a candidate until its exact ownership, content uniqueness, backup/off-host recovery coverage, consumer references, and rollback need are proven. Before any actual removal, satisfy the site's consequential backup and authorization gates; independently verify resulting live services and space. On OpenVZ/ploop, do **not** issue speculative guest `growpart`, `resize2fs`, `lvextend` or destructive storage commands.

**Read-only usage snapshot (2026-10-10, unprivileged VPS SSH):** root filesystem 158 GiB total / 142 GiB used / ~9.3 GiB free. Hosting account tree totals ~63,224 MiB; the historical migration/staging workspace accounts for ~34,909 MiB, the production Drupal project tree ~27,451 MiB, and an account backups directory ~809 MiB. These are point-in-time disk-usage observations, NOT proof the migration copy can be removed. Do not persist these changing quantities as invariant capacity. Next narrow investigation: characterize and hash-compare candidate leftover migration contents against the current live source and verified independent recovery copies, without broad re-review or any deletion.

**Regression R7, account-vs-disk:** a report of 100 GiB account quota must not be presented as 100 GiB free VPS space or as evidence of purchasable/unactivated capacity.
**Regression R8, capacity attribution:** when guest-visible disk and partition are both ~160 GiB, do not claim there is additional guest-unpartitioned space merely because the provider plan might be larger. Check provider-authoritative allocation separately.
**Regression R9, reusable facts:** subsequent InMotion tasks reuse the 2026-10-10 OpenVZ/ploop structure unless contradicted; only recheck mutable free space at the material action boundary.


## 9. Migration workspace reclaimability check (2026-10-10)

**Status: PARTIAL / NO DELETION AUTHORIZED.** Read-only inspection via an established non-root SSH route on the InMotion VPS inspected the migration workspace under the hosting account. About 34,909 MiB is currently accounted for by this workspace: ~21,524 MiB in a historical files copy (34,547 files), ~4,316 MiB in an incoming directory (a ~4.1 GB Drupal tar and ~131 MB database dump), and ~4,309 and ~4,308 MiB in two separate staged Drupal project trees. Sizes are observation-time values, not permanent capacity facts.

- The historical files copy is **not byte-identical by demonstrated evidence** to the live public files tree: a size-only rsync dry run found some migration-side paths absent from the live destination. No deletion eligibility established.
- No direct references to the main migration directories were found in a narrow check of selected account scripts/configuration, but this does not prove absence of all dependencies.
- A full checksum-only rsync dry run of the staged project was attempted but did **not** produce a completion report. A parallel SSH connection timed out. The comparison session's termination was initiated to avoid extended production I/O pressure. The result remains **UNVERIFIED**, not PASS or FAIL.
- No workspace deletion, move, archive modification, or production configuration change occurred in this check.

**Continuation gate:** verify that read-only checksum activity has stopped and SSH/service health recovered; then use previously recorded source/archive manifests and small, bounded comparisons to identify *specific* migration artifacts whose off-host recovery copies and absence of live dependencies are independently proven. Large recursive hash comparisons against a production VPS require resource/load bounding and should not be repeated blindly. Do not classify the entire 34 GiB workspace as disposable.


## 10. Cleanup execution and interrupted verification (2026-10-10)

**Current state: PARTIAL MUTATION / RECOVERY VERIFICATION BLOCKED.** Gene explicitly directed completion of the previously reviewed migration-workspace cleanup. A targeted removal of **only** the verified historical staging duplicate `/home/n790725/skyhawk-migration/drupal-staged-clean` was attempted as `n790725`, after confirming matching staged/current `composer.json` and `composer.lock` hashes, a previously recorded 2026-10-02 checksum-identical staging-to-deployed mirror, Mac current-site backups marked DB SHA match / FILES OK on 2026-10-10, and the preserved October 6 A2 archive.

- **Observed mutation:** recursive deletion removed some content of the staging directory. It returned exit code 1, reporting four permission-denied configuration files under the staging tree. Therefore **do not describe the directory as deleted**, and **do not report a verified reclaimed-space figure**. Do not repeat `rm -rf` without first refreshing precise residue and ownership.
- A direct follow-up SSH check hung and timed out. Subsequent independent tests showed the public `https://skyhawk.org/` returned HTTP 200 while TCP/22 to the VPS timed out. No post-deletion filesystem read-back or space measurement has been obtained. Repeated SSH failures do not prove site outage or deletion failure; the state remains UNVERIFIED.
- Other targets (`drupal-staged`, `files`, `incoming`, databases and production `/home/n790725/drupalbeta`) were **not targeted for deletion** in this execution.
- **Stop condition:** no further deletion/mutation until SSH access and the post-action state can be verified. When access returns: inspect only the staged-clean residue, ownership/mode and `df`; do not run full content checksum scans; verify live public route and production project; finish the four-file residue only if authorized and ownership permits, then independently check actual space reclaimed. Keep historical files and other staging sources until their own disposition is proven.

**DACP failure correction:** Previous replies wrongly treated repeated file verification as a reason to stall indefinitely, but proceeding with a deletion that could not be verified afterward is also not acceptable. Recovery must begin at the exact incomplete mutation, not broad review or speculative cleanup. This is not a success claim.

## 11. Clean staging directory removal verified (2026-10-10)

**VERIFIED:** After Gene completed the privileged cleanup from the existing root session, an independent Mac-to-InMotion SSH read-back as `n790725` confirmed `/home/n790725/skyhawk-migration/drupal-staged-clean` absent and production `/home/n790725/drupalbeta/web/index.php` present. Root filesystem `df -h /` changed from the earlier 158G total / 142G used / 9.3G available (94%) to **158G total / 138G used / 14G available (92%)**. These are rounded point-in-time readings and do not establish an exact byte count. Independent external `https://skyhawk.org/` HEAD returned HTTP **200**. No assertion that other migration directories (`drupal-staged`, `files`, `incoming`) have been removed or proven redundant. Do not repeat this completed cleanup or revive the prior partial-mutation blocker. Future work should examine only remaining artifacts and avoid live production changes without their own bounded preconditions and verification.

## 7. Provenance and change handling

Source of this reference's scope/reuse requirement: Gene's explicit InMotion-specific DACP direction, 2026-10-10. Foundational controls: DACP Project Instructions 0.7, Runtime Expression 0.1.7-DELTA, Control Application Enforcement 0.1, Required Pipe Qualification 0.1, Operational Use and Correction Authority 0.2 and Reality-Conformance decision.

This version records existing structural knowledge and the reusable evaluation contract. It does **not** claim to have completed a new full InMotion VPS audit, provisioned any domain, corrected TLS or deployed an application.

**Activation evidence:** canonical Git file content and CURRENT.md pointer fetched again after persistence, with resulting commit identity verified.