# InMotion Hosting Operating Reference 0.1

## Change Synopsis

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
- The user states the storage allocation was previously upgraded once. **Upgrade event: USER-REPORTED, not independently verified against provider billing/provisioning in this check**. Do not infer the amount purchased or whether further capacity is pending.

**Capacity resolution order:** (1) compare the actual InMotion VPS service specification/purchased storage to the 160 GiB guest-visible ploop disk; (2) if provider storage exceeds the guest disk, ask/perform the supported provider-side presentation/expansion route and independently recheck disk, partition, filesystem, backups and service health; (3) if purchased storage is 160 GiB, evaluate safe cleanup and/or authorized storage expansion; (4) only after enough free space and rollback margin are verified, proceed with another Drupal installation. On OpenVZ/ploop, do **not** issue speculative guest `growpart`, `resize2fs`, `lvextend` or destructive storage commands without proving the actual supported owner and allocated block size.

**Regression R7, account-vs-disk:** a report of 100 GiB account quota must not be presented as 100 GiB free VPS space or as evidence of purchasable/unactivated capacity.
**Regression R8, capacity attribution:** when guest-visible disk and partition are both ~160 GiB, do not claim there is additional guest-unpartitioned space merely because the provider plan might be larger. Check provider-authoritative allocation separately.
**Regression R9, reusable facts:** subsequent InMotion tasks reuse the 2026-10-10 OpenVZ/ploop structure unless contradicted; only recheck mutable free space at the material action boundary.

## 7. Provenance and change handling

Source of this reference's scope/reuse requirement: Gene's explicit InMotion-specific DACP direction, 2026-10-10. Foundational controls: DACP Project Instructions 0.7, Runtime Expression 0.1.7-DELTA, Control Application Enforcement 0.1, Required Pipe Qualification 0.1, Operational Use and Correction Authority 0.2 and Reality-Conformance decision.

This version records existing structural knowledge and the reusable evaluation contract. It does **not** claim to have completed a new full InMotion VPS audit, provisioned any domain, corrected TLS or deployed an application.

**Activation evidence:** canonical Git file content and CURRENT.md pointer fetched again after persistence, with resulting commit identity verified.