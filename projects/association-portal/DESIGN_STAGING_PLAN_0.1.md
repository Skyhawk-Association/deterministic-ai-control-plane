# Association Portal - Design and Staging Plan 0.1

**Status:** PLANNING DRAFT (Claude, 2026-10-10). Not deployment authorization. Every provisioning or mutation step below
requires Gene's explicit go-ahead under Application Implementation Authorization 0.7 and the InMotion reference.
**Inputs:** projects/association-portal/CURRENT.md decisions; platforms/inmotion/OPERATING_REFERENCE_0.1.md (section 4 readiness gates);
projects/skyhawk/LOST-D.md (emconalfa.net DNS on R4L -> VPS; HTTPS fetch completes as of 2026-10-09).
**Fixed decisions (not reopened):** Drupal, not WordPress; skyhawk.org remains the archive; emconalfa.net is a second, independent
Drupal installation; same InMotion VPS; design for additional organizations.

## 1. Architecture

| Layer | Plan | Why |
|---|---|---|
| Hosting account | **Recommended:** a separate CWP user account for emconalfa.net (its own Linux user, home directory, PHP-FPM pool and database user). | File-level isolation from skyhawk.org. The same VPS still shares CPU, RAM and disk (InMotion reference R4). |
| Code | A separate Composer project with its own Git repository, mirroring the Skyhawk Composer discipline. | Independent updates and rollback. |
| Organizations | **Group module** (drupal/group): each association is a Group; content and documents belong to a Group; roles are scoped per Group. | "Design for additional organizations" without cloning sites. Confirm the Drupal 11-compatible release at build time. |
| Group roles | Member, Director, Officer, Secretary, Treasurer, Group Admin. | Maps to board, officer workspaces and records ownership. |
| Public content | Article/Blog content type, published to anonymous users; moderated comments with antispam (Honeypot/Antibot). | Public blogs. |
| Board discussion | "Topic" content type (group-private) plus core Comments; one topic per subject; searchable. | Replaces reply-all chains. Casual discussion is not a formal vote. |
| Official records | Minutes, Resolution and Policy types, using core Content Moderation (draft -> review -> approved) with revisions; the Secretary owns the transition to approved. | Version history and a clear official record. |
| Documents | Media "Document" type stored in **private://** (outside the webroot), with access via the parent group entity. Direct-URL access must be denied to unauthorized users (tested). | Protected document storage. |
| Officer workspaces | A group-private section restricted to the Officer/Treasurer/Secretary roles, with Treasurer-only financial folders. | Restricted financial records. |
| Notifications | Rule-based email (ECA module, or Message + Message Subscribe/Notify): new topic, reply, document version, record approved; per-user immediate or daily-digest choice. Email carries a link, not the attachment. | One authoritative copy. |
| Authentication | Individual accounts only; TFA (two-factor) required for Director roles and above; no shared logins. | Protects private material. |
| Mail delivery | Site mail sent from the VPS with SPF/DKIM aligned for the sending domain (as done for skyhawk.org), or an SMTP relay. **No mailboxes hosted on the VPS** (Gene direction 2026-10-10). | Notification deliverability without self-hosted mailboxes. |
| Backups | Nightly database plus files (including private://) per site, pulled off-host to the Mac like the Skyhawk pattern; a restore test before launch. | Gate 6. |

## 2. Staging approach

Nothing runs on emconalfa.net yet, so build **in place behind an access gate**: HTTP basic auth plus `noindex`, which forms the staging
phase. Launch = removing the gate only after all section 4 gates pass. A permanent `staging.` subdomain is created later for safe
updates once the portal is in use.

## 3. Phases and gates

| Phase | Work | Exit evidence | Gene action |
|---|---|---|---|
| P0 Decisions | Section 5 below. | Recorded answers. | Decide. |
| P1 Provision | CWP account/vhost for emconalfa.net + www; TLS; empty database and user; PHP version matching the Skyhawk runtime; free-space check at commit time. | HTTPS with a valid certificate for both hostnames; vhost document root proven; no change to skyhawk.org (still HTTP 200). | Authorize; root-prompt steps where required. |
| P2 Base install | Composer project, Drupal 11, settings with private path, Group/TFA/notification modules, behind basic auth. | Login works; status report clean; `composer.lock` committed. | None beyond P1 authorization. |
| P3 Structure | Content types, group types and roles, workflows, menus; Skyhawk as Group #1. | Permission matrix test: anonymous, member, director, officer and treasurer each see exactly their scope. | Review the matrix. |
| P4 Documents and notifications | private:// documents, version history, mail. | Direct-URL denial test; a real notification delivered to an external inbox with SPF/DKIM pass. | None. |
| P5 Pilot | Gene plus pilot users Gene selects use it for one real topic. | Feedback captured; backup and restore demonstrated. | Use it. |
| P6 Board rollout | Accounts and TFA enrollment; short how-to page. | All directors logged in once. | Announce. |
| P7 Second organization | Add Group #2 from a template. | No cross-group visibility (tested). | When needed. |

These phases implement InMotion reference section 4 gates 1-7. Any failed gate = **NOT READY** with that gate named.

## 4. Known constraints

- Shared VPS resources: a runaway portal process can affect skyhawk.org. Mitigate with separate PHP-FPM pool limits and backup scheduling offset from Skyhawk.
- Free disk was about 22 GB at the 2026-10-10 reading (volatile). Recheck at P1/P2 commit time; a Drupal base install is small, and documents grow slowly.
- Succession: the portal needs a named technical administrator and the Secretary as records owner; record both before P6.

## 5. Open decisions for Gene

1. Separate CWP account for emconalfa.net (recommended) or the same account as Skyhawk?
2. Group-module multi-organization model: accept?
3. Notification sender address/domain (for example notices@emconalfa.net) and whether Board replies-by-email are wanted (adds complexity; recommend no at first).
4. Is emconalfa.net the long-term public name, or a working host until a better domain is chosen? (Drupal is host-agnostic; changing later is cheap.)
5. Two-factor required for all directors (recommended) or officers only?
