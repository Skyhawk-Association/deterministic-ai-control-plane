# LOST-D — Skyhawk.org active work (passdown)

**Canonical passdown for any AI executor (Claude or ChatGPT).** Read this file first in every session:
`https://raw.githubusercontent.com/Skyhawk-Association/deterministic-ai-control-plane/main/projects/skyhawk/LOST-D.md`

**Freshness:** the raw URL can lag a few minutes behind a push; right after a push, verify with git (clone or ls-remote).

**Update rule:** every verified consequential step updates this file (last verified step, next step, open decisions) and pushes it in the same run as the change. The Drupal LOST-D page (node 2479) points here.

**Public file. Never put here:** passwords, SSH/API keys, token links (upload, manage or verify tokens), member personal data (names, email or contact details of attendees or contributors), backup contents, database contents, server IP addresses.

## Governing references (read before acting)
- Skyhawk Working Rules: `projects/skyhawk/RULES.md` in this repository (public URL `https://raw.githubusercontent.com/Skyhawk-Association/deterministic-ai-control-plane/main/projects/skyhawk/RULES.md`). Binding for every executor.
- Environment Reference: `projects/skyhawk/ENVIRONMENT.md` in this repository (Drupal node 49461 points here). GitHub / Source Reconstruction Reference: `projects/skyhawk/GITHUB.md`. Termux SSH Notes: `projects/skyhawk/TERMUX.md`. Site Menu Reference: `projects/skyhawk/SITE_MENU.md`. (Their Drupal pages 49463, 49458 and 49457 point here.)
- Squadron Template 49454, Squadron Roadmap 49453 and `skyhawk_site_fixes/data/squadron-template-contract.php`: superseded for new squadron work by Gene (2026-09-27). Ignore them except the lessons listed under Active slice.

## Executors
- Claude and ChatGPT are both authorized executors, one at a time, as Gene chooses. The tunnel (one AI checking the other) happens only when Gene asks for it. Formal record: `authoritative/DACP_Application_Implementation_Authorization_0.6.md`.

## Operating facts (non-secret)
- Project root `/home/darwus/drupalbeta`; Drush `/home/darwus/drupalbeta/vendor/bin/drush --root=/home/darwus/drupalbeta/web`.
- Commands are pasted at the A2 prompt; wrap each block in a subshell `( ... )` so a failure never logs Gene out. A2 has no `/dev/fd`: no bash process substitution. A2 throttles rapid SSH connections: wait about 5 minutes if refused.
- A2 is a shared hosting server: no AI gets direct access, ever. Gene runs every A2 command.
- Files move by `scp` from Windows (host alias `A2`); Gene's working folder is `C:\Users\genea\dacp-work\vma131`.
- A2 transport (Gene 2026-09-28): never chain scp and ssh on one line; copy and connect are separate commands, each with -o ConnectTimeout=20; keep A2 connections per step to a minimum (backups: A2 writes the checksum beside the dump, one scp brings both down, compare on Windows, delete in the next A2 block). A2 is fragile until the hosting move.
- Large outputs: `( commands ) 2>&1 | ~/bin/ai-report "task"` pushes a secret-scanned report to evidence/skyhawk/ in this repository; paste only its one-line result.
- skyhawk.org Git remote is private (`github-skyhawk` identity, account geneatwell). The same identity pushes this DACP repo (clone on A2: `/home/darwus/dacp-repo`). Organization deploy keys are disabled.
- Composer only via `bin/skyhawk-composer` (require or update, then functional check, then `finish`). Its pending marker is git-ignored.
- Never pipe or `tail` a command that asks a question (`skyhawk-composer finish`, anything without `-y`): the prompt is hidden and Enter answers No.
- Configuration: site-wide `config:import` fails validation because of orphaned configuration from old modules and themes. Apply structure through the entity API, then `drush config:export -y`, then commit only the expected files.
- Backups before structural database work: dump to `/home/darwus/skyhawk_backups`, download to the Envy (`Desktop\ChatGPT\pre_update_<version>_<timestamp>\database.sql.gz`), verify SHA-256, then delete the server copy.
- Styling: one global stylesheet `skyhawk_site_fixes/css/skyhawk-global.css` and its semantic vocabulary (skyhawk-focus, -feature, -context, -note, -reference; modifiers -navy, -marine, -joint, -heritage; skyhawk-focus-label).

## Active slice: Squadron CMS, VMA-131 test build
**Last verified step:** Squadron identity tint DONE (skyhawk.org e844788, verified visually by Gene 2026-09-28): invisible unit marker from the hidden unit taxonomy (View squadron_actions, eva_identity) + SQUADRON IDENTITY TINT section in skyhawk-global.css. DECIDED: U.S. Marine Corps = scarlet and gold; every other affiliation (Navy, Foreign, Civilian, Joint, Reference) = blue and gold. Lesson: do not verify served CSS through the anonymous home page (page-cached); verify on the target page after Ctrl+F5.

**State**
- Content type `squadron`: identity, snapshot, story, people, featured story, aircraft, remember and research fields, plus the 14 detailed-record sections. Legacy body kept but hidden. Tabbed edit form (Field Group).
- Display: Field Group panels using the global semantic classes inside the wrapper group_sq_page (`skyhawk-squadron-cms`, styled by SQUADRON FAMILY (CMS) in skyhawk-global.css); kickers use `skyhawk-focus-label`; the featured title is an h3; hero photo field `field_sq_hero_image`; jump bar EVA `eva_jump`.
- Media: vocabulary `unit_collections` (Voices, Research, Visual record, Final Inspection, and the rest). Document and image media carry Unit, Collection, Heading, Order and Description. One media record per placement, named "Title · Collection"; files are never copied. VMA-131 has 14 placements.
- View `squadron_collection` has three EVA displays (Voices, Research, Visual record), filtered by the page's unit and placed inside their panels. Links open in a new window.
- Test node **49779**, unpublished, at `/squadrons/vma-131-test`. The live VMA-131 page, node 49417 at `/article-unit/vma131`, is unchanged until Brian Putney signs off. `/squadrons/vma-131-preview` redirects 301 to it.
- VMA-131 assets: 356 images in `sites/default/files/vma131-preview/images` (with `manifest.tsv`; 1 placeholder photo pending from Brian). Interim section pages are nodes 49770–49777.
- Modules added: field_group 4.0, eva 3.1, views_field_view 1.0. Core 11.4.8, webform 6.3.1 (security updates applied 2026-09-27).

**Lessons kept from the old template:** thumbnails open the original in a new window, with a way back to the squadron page; Gabby's Histories is linked with the unit preselected; no large aircraft-assignment tables on the landing page; the complete Commanding Officers list is collapsible on the landing page; scrape the target unit first; never clone another unit's content.

**Next steps (in order)**
1. Done: shared contribute block and Gabby link (skyhawk.org 87737c5).
2. Done: Skyhawks Assigned off the landing display (skyhawk.org 7ab995a).
3. Brian’s collections. DECIDED by Gene 2026-09-27: (a) collection sections as taxonomy terms (unit, collection, heading, order, Brian’s text as rich text), with document and photo placements pointing at their section; (b) Brian’s text sits at the top of each section (exact text/file interleaving not kept; explain to Brian). Then: backup (Rules), vocabulary and fields, sections and document placements, photo placements, collection View with test pages at /squadrons/vma-131-test/<collection>. About 220 documents, 356 photos, 60 sections. Progress: 3.1 done (skyhawk.org 0bec5cb); 3.2, 3.3 and 3.4 done: test collection pages at /squadrons-test/vma-131/{squadron-home, final-inspection, diamondback-stories, usmc-stories, us-military-stories, tails-of-aviation, aircraft-photos, squadron-mates, archives}. Explore menu and back links done (2421be1). at cutover the paths become /squadrons/<unit>/<slug> and the interim nodes 49770-49777 retire.
3a. Done and visually accepted by Gene 2026-09-27 (skyhawk.org 7eafd3d): SQUADRON FAMILY (CMS) section in skyhawk-global.css, scoped to the outer Field Group wrapper group_sq_page (class skyhawk-squadron-cms): hero over the unit photo (new field field_sq_hero_image, Identity tab) with the unit patch small, navy snapshot band, jump bar (EVA eva_jump on squadron_actions, links only to bands with content), alternating section bands, gold kickers, two-column image and text, Explore as cards. Node 49779: hero shows the unit patch only; station and group patches are in the record. squadron.css stays legacy-only for the three old pages.
3b. Done 2026-09-27: designated reviewer account is active with CO role; Drupal access checks returned YES for node 49779 and related review nodes. The main CMS test node remains unpublished.
3c. Done 2026-09-27: review email sent with instructions to log in and review /squadrons/vma-131-test and its collection pages. Status: AWAITING REVIEWER RESPONSE. Brian's sign-off remains the gate for cutover.
4. Unit identity on the `skyhawk_units` term. PRINCIPLE (Gene 2026-09-28): the unit taxonomy is hidden metadata for automatic lists, filters, preselection and tagging; pages stand on their own content; designations are internal. VALUES WRITTEN 2026-09-28 (see last verified step); next: the class mechanism (decision open), then show identity on squadron pages. Read-only mapping/derivation completed 2026-09-27 for 213 sources, then Gene resolved all 15 exception rows. Final broad affiliation map: 137 U.S. Navy, 49 U.S. Marine Corps, 18 Foreign Military, 7 Civilian, 1 Joint Navy/Marine compendium, plus `/node/49222` as a reference-only source covering various civilian and non-U.S. operators. Specific clarifications include: A-4LLC -> Sky Resources; Discover Air -> Top Aces; FAGU -> Navy; NAF Willow Grove page -> Marine unit compendium at a Joint Reserve Base; HU-2 page -> evenly split Navy/Marine; NAS Chase Field -> Navy trainer facility; NAS Quonset Point -> Navy facility with Navy aircraft. Foreign rows remain further derived to specific service/operator where supported by the menu/page label (10 operators, 2 evaluation pages, 6 proposal pages). Remaining review rows: 0. Stable unit identity remains separate from menu placement and historical designation/lineage. Rollback gate verified 2026-09-28: `pre_unit_taxonomy_20260928T010141Z.sql.gz` is on the Envy and its SHA-256 exactly matches the A2 copy. Dump-growth analysis shows current serialized table-data sections at about 986 MB; `watchdog` is about 366 MB, while the rapid same-day growth is dominated by Drupal cache tables. The structure script was corrected so the new `field_unit_kind` is optional until terms are populated, then staged to A2 through the authorized file-transfer route with matching local/remote SHA-256. No Drupal mutation had been verified at the time of this record; next is A2 lint, live-owner precheck, entity-API structure apply, postcheck and config export. RESOLVED 2026-09-28: structure applied and committed (4003276). Mapping in Git 2026-09-28: projects/skyhawk/data/unit-taxonomy-reviewed-213.tsv (source of truth; derived-213 kept for provenance). Next: page-to-term match report, then backup, then term values. Former gate text: re-inspect the live A2/Drupal `skyhawk_units` structure and the A2 `skyhawk.org` Git working tree. Canonical Git does not independently prove that the preceding no-mutation statement still matches current live server state. Treat live mutation/config state as UNRESOLVED until read back; do not assume the structure is either applied or unapplied.
5. Parity check against node 49417, then Gene's review, Brian's sign-off and cutover.
6. Documentation: the Environment Reference's Squadron CMS section (a draft exists, shelved until 131 is done).

**Open decisions (Gene):** choose the canonical Windows evidence folder; unit-identity tint CLOSED (Marines scarlet and gold, all others blue and gold; e844788); history: colours DECIDED by Gene 2026-09-28: U.S. Navy = blue and gold; U.S. Marine Corps = scarlet and gold; tint is an optional use of the hidden unit taxonomy; joint-use stations later); approve orphaned-configuration cleanup; delete node 49778; fix the journal PDF URI error in the logs.

## Active slice: Reunion system

**Source continuity:** Gene authorized project-chat reconstruction on 2026-09-28. Relevant prior project chat: `Reunion Page Setup`. The durable statements below are cross-checked against current `skyhawk.org` source/config on `origin/main`; chat history is continuity evidence, not authority.

**Verified working 2026 photo path**
- Webform `reunion_2026_photo_upload` is open and accepts up to 20 images per submission. Contributor identity/person, public credit, rights consent and optional batch caption are shared across the batch.
- `skyhawk_gallery` marker `SKYHAWK_REUNION_WEBFORM_MEDIA_BRIDGE_V1` converts every submitted FID into exactly one `skyhawk_contributed_photo` Media entity and is idempotent by `field_media_image.target_id`.
- Current bridge binds the 2026 Reunion Event directly to node 49466. Media carries Reunion Event, Reunion Person, public credit, caption and rights consent.
- Acceptance already proved one six-photo submission persisted all six FIDs and mapped them one-to-one to Media, followed by a fresh successful multi-photo submission. This architecture is accepted reusable Reunion infrastructure; before reuse for another Reunion, resolve the event context instead of cloning the hard-coded 2026 event ID.
- Public gallery View `reunion_2026_photos` is at `/reunions/2026/photos`, 30 items/page, newest first, filtered to published contributed-photo Media for Event 49466. Detail View `reunion_2026_photo_detail` serves `/reunions/2026/photos/{mid}`.
- Do not replace this working Webform/Media bridge with the older token-upload path merely because token-era Reunion classes/routes remain in the codebase.

**Historical production provenance (sanitized)**
- A read-only production baseline captured 2026-09-14 exists privately on the Envy/Drive as `derived/reunion_2026_production_baseline_20260914T025036Z.json` with matching SHA-256 sidecar. The raw file is NOT suitable for public Git because it contains credentials and member-level data.
- That baseline proves the Reunion system was already materially in production by 2026-09-14: 2 `reunion_event` nodes, 150 `reunion_person` nodes, 150 `reunion_attendance` nodes, 7 contributed-photo Media records, and 7 submissions to `reunion_2026_photo_upload` at capture time. Treat those counts as historical evidence only, not current counts.
- The same baseline showed enabled menu entry points for Reunions, Submit a Reunion, My Reunion Events, Request a Reunion, 2026 Reunion, Reunion Photos and Upload Photos. This establishes that the newer Ready Room/request surfaces were not merely dead source files by that date, while still requiring current live reinspection before mutation.
- Event 49466 was already the published 2026 Reunion hub with registration/hotel links, Reunion documents, photo-gallery/upload links and durable post-event wording; its 2026 photo/gallery role therefore predates the later multi-photo bridge acceptance.

**Current Reunion-management direction**
- Authenticated Ready Room routes exist at `/ready-room/reunions`, `/ready-room/reunion/{node}`, `/ready-room/reunion/{node}/newsletter` and `/ready-room/reunions/request`.
- Gene decision 2026-09-28: each Reunion has at most two human participants in the authority model: (1) one accountable current Skyhawk Association member, represented by the `reunion_event` owner UID, and (2) at most one optional Worker Bee who may or may not be a member and is authorized only for that one Reunion. There is no permanent third continuity-contact participant.
- The accountable member may do all work personally or appoint/revoke the Worker Bee. The Worker Bee never becomes the accountable owner merely by doing the work. If the accountable member later becomes unavailable, normal Association/Drupal administration may reassign ownership to another verified member.
- `ReunionReadyRoomController` currently binds management authority to the authenticated owner of the `reunion_event`; the agreed next architecture is to extend that exact scoped access test to owner UID OR the one assigned Worker Bee UID, rather than grant global reunion-event edit permission.
- KISS field model: keep owner identity in Drupal's existing node author/UID; add only one optional single-value user-reference field for the Worker Bee. Do not add a duplicate owner field.
- `ReunionRequestForm` marker `SKYHAWK_REUNION_SOURCE_INTAKE_V1` is the newer self-service intake direction: an active authenticated member may upload one source document or paste source text; Drupal preserves the source, creates an unpublished `reunion_event` draft owned by that account, records source provenance/hash in the revision log, verifies persistence, creates no token and activates no authority.
- Durable authority is account-based, not token-based. The Worker Bee should be a normal Drupal identity whose email control is verified using Drupal core account creation/one-time-login behavior; assignment to one Reunion grants the scoped management authority. Token/verification links may establish identity during transition but are not durable Reunion authority.
- Transitional membership rule, Gene decision 2026-09-28: the Secretary's current membership roster remains the eventual authoritative source for current Association membership, but its delayed availability does not block Reunion implementation. Pending reconciliation against that roster, the existing Drupal user population is accepted as the current dues-paying member baseline because Drupal accounts have historically been issued only to dues-paying members. `authorized_user` is the intended Drupal member-authorization marker to normalize against that existing population. This is a temporary operational proxy, not a replacement for the Secretary's roster. New nonmember Worker Bee accounts must not receive `authorized_user` merely because they can authenticate.
- Security prerequisite discovered 2026-09-28: the current Drupal `Authenticated User` role is not a safe external-account baseline because it presently carries institutional permissions including `administer users` and `administer permissions`. Existing `Reunion Staff` is also too broad. Before Worker Bee accounts are enabled, audit and reduce Authenticated User to truly universal logged-in permissions while preserving legitimate institutional powers through proper officer/staff roles.
- Source-only Worker Bee preparation completed 2026-09-28 in skyhawk.org commits `1f545b5` and `b18414c`. The Ready Room source now supports owner UID OR optional `field_reunion_worker` UID without changing owner behavior before the field exists, and an owner-only Worker Bee assignment form is prepared. The Worker Bee field is hidden from the generic Ready Room node-edit form so the Worker Bee cannot alter that authority relationship. This is NOT live acceptance: `field_reunion_worker` does not yet exist on production, Windows had no PHP runtime for lint, and no production role/config/account/mail mutation has been performed. Prep evidence: `evidence/skyhawk/20260928-reunion-worker-bee-unattended-prep.txt`.
- `ReunionNewsletterUpdateForm` marker `SKYHAWK_REUNION_READY_ROOM_UPDATE_V1` is presently an acceptance fixture limited to Event 49464 and its authenticated owner. It preserves newsletter history, verifies private-to-public copy/hash/persistence and HTTP retrieval, and explicitly labels the general current-member gate as deferred. Do not generalize that fixture by assumption.
- Older token-era routes/forms still exist: `/community/event-submission/{token}`, `/reunion/verify/{token}`, `/reunion/manage/{token}` and the token admin. They are transitional only and are to be retired in toto after the account-based owner/Worker-Bee path is proven.

**Reunion next steps**
1. DONE 2026-09-28 (report 20260928T155448Z-reunion-live-reinspection): all 9 Reunion main-menu links enabled (Reunions, Submit a Reunion /node/49349, My Reunion Events, Request a Reunion, 2026 Reunion, Reunion Photos, Upload Photos, Ready Room x2). Events: 49466 published (2026 hub), 49464 unpublished; 150 persons, 150 attendance. Photo webform open, 29 submissions, 57 contributed-photo media. Ready Room routes 403 for anonymous (correct).
2. DONE 2026-09-28: scalable Reunion front door applied and independently read back from public /reunions. Node 49769 now leads with the general Reunion identity and planning actions. Drupal View reunion_index supplies Current & Upcoming and Reunion Archive blocks. Optional `field_registration_link` is an outbound organizer/provider link; Skyhawk.org is not the registration processor. Follow-up title/date defects are resolved (evidence/skyhawk/20260928-reunion-view-display-fix.txt; skyhawk.org 736bce1).
3. DONE 2026-09-28: legacy token compatibility restored and independently verified (evidence/skyhawk/20260928-reunion-legacy-token-compatibility.txt; skyhawk.org d5c9688). The actual stored historical upload token returns HTTP 200; invalid upload and manage tokens return 404; invalid verify token returns 302. No token value is recorded. Token-format assumptions are removed; exact `hash_equals()` comparison to Drupal state is retained. Legacy token machinery remains transitional only pending account-based owner/Worker-Bee replacement.
4. Audit the current `Authenticated User` permissions and user-role population before creating Worker Bee accounts. Verify Gene's own administrative account has durable real-admin authority before removing institutional permissions from the base role.
5. PREPARED / NOT LIVE 2026-09-28: source support for the optional single Worker Bee relationship, owner-or-worker Ready Room access, and owner-only Worker Bee assignment is committed in skyhawk.org `b18414c`. Production still requires safe Authenticated User cleanup, verified backup, Drupal entity/config API creation of `field_reunion_worker`, A2 PHP lint/cache rebuild, and end-to-end owner/Worker Bee acceptance.
6. DECIDED 2026-09-28: the Secretary's membership roster is the eventual authoritative membership source, but reconciliation is deferred until the spreadsheet is supplied. For current Reunion implementation, the existing Drupal user population is accepted as the transitional dues-paying-member baseline and will be normalized to the `authorized_user` member-authorization role before nonmember Worker Bee accounts are introduced.
7. Use Drupal core administrator-created-account / one-time-login email flow to establish Worker Bee account/email control; do not invent a second authentication mechanism.
8. Prove owner and Worker Bee end-to-end, including replacement/revocation and one-event-only access. Then retire token routes, token admin, token fields/storage, token controllers/forms/classes, and the remaining node-body link to the token path in one controlled removal.
9. Preserve the accepted 2026 multi-photo Webform/Media architecture. Generalize only the hard-coded Event 49466 binding when a real second-Reunion use case requires it.
10. Keep Reunion work separate from VMA-131/Squadron CMS review; neither is a prerequisite for the other.

**Half-done:** Reunion self-service activation is intentionally incomplete pending (a) safe Authenticated User baseline cleanup and normalization of the existing member population to `authorized_user`, and (b) scoped Worker Bee implementation. Secretary-roster reconciliation is deferred and is no longer a Reunion activation blocker. The 2026 photo upload remains accepted working infrastructure.

## Previous LOST-D (Drupal node 2479, verbatim at migration, 2026-09-27T14:26Z)

```
LOST-D

Current implementation slice: Journal modernization. Raven-derived article metadata is already live as 534 skyhawk_association_journal_inde records covering Summer 2004 through Winter 2019. Active work is to create maintainable procedures for future Journal uploads and separately complete article metadata for Journals from 1995 through the second Journal of 2004.

For the Raven-indexed historical period, do not rediscover or overwrite existing title, author, issue, year, journal number, page, category, record, or PDF-access metadata merely because a Journal PDF is processed again. The existing Drupal article-index records are the baseline unless a reviewed correction is accepted.




Skyhawk Working Rules
- authoritative human/AI operating contract. Intentionally not
required in the Blade navigation menu.




Generic Intake System
- current state and specification for reusable file intake.




Drupal Environment Reference
- durable environment facts when germane.






How LOST-D Is Used


LOST-D contains active human-facing work and navigation. Project
references contain current project truth. The Rules govern how work
is performed. Completed or superseded debugging history does not
remain in the active list merely because it once consumed oxygen.





Legacy LOST-D content

The material below is preserved from the prior LOST-D page for
historical context. Its presence here does not make completed,
obsolete, or superseded items active work.






	h1 {
		color: blue;
		font-size: 40px;
		margin: 0px;
		text-align: center;
	}

	h6 {
		color: #1275d1;
		font-size: 20px;
		margin: 0px;
		background: #f5f33c;
		text-align: center;
	}


	Items with dashes through text indicate total or partial completion.


	
		

		Convert site to Composer Compliance

		

		Perform all Updates via Composer-Frequent and ongoing.

		

		Create Menu entry for Gabby's Histories.

		

		Clean data from Gabby's gigantic spreadsheet to reduce errors. Uploaded!

		

		Create Menu entry for Journal Index.
			
				Clean data from Raven's Excel file for upload to site to reduce errors and create proper data format for uploading to site.

				Create new procedures for uploading future Journals to website and share with Hide.

			
		

		

		Association Photos.
			
				Protect photos with lettering and watermarking.

				Align photos so they don't look like raggedy-assed Marines. I agree with Jigger on this one.

			
		

		

		Solicit member recommendations for both. In progress.

		

		Learn Atom Editor-Ongoing Forever.

		

		Disable second database and Views Database Connector to increase performance of the site.

		

		Create new page for YouTube Videos.

		

		Create new user fields to allow for all members to input their info and approve or disapprove of receiving emails from other dues paying members.

		

		Create a page for new members to register online. This will have a verification associated with it to reduce robots from spamming the site.

		

		Use Board Members as Guinea Pigs to test methods in order to reduce member confusion once this new information is uploaded and will then require member verification.

		

		Create pages to allow logged in members to directly email other members without divulging the email of the person receiving the e-mail.

		

		Rearrange all Staff member communications to eliminate e-mail trolling.

		

		Need somebody to revisit all Journals from 1995 until the second Journal in 2004 and create a spreadsheet with Authors, Article names, etc to be included here.

		

		Create this page. Update when necessary to add member recommendations.

		

		Your Desire Here?

	

	Items with dashes through text indicate total or partial completion.










GitHub / Composer Infrastructure Closeout


The private Skyhawk-Association/skyhawk.org GitHub repository contains the accepted Skyhawk reconstruction architecture.

The A2 SSH identity is proven against the repository and local main is verified against remote origin/main.

The live Drupal configuration is authoritative and has been exported to the tracked configuration sync tree with zero active-vs-sync drift.

Normal mutating dependency maintenance uses /home/darwus/drupalbeta/bin/skyhawk-composer.

The interactive user-level Composer guard warns before direct update, require, remove, or install and defaults to No.

The Composer wrapper uses explicit proven PHP, Composer, Drush, Drupal-root, Git and project-root paths and does not depend on shell aliases or current directory.

Mutating Composer maintenance is not complete until functional acceptance, zero Drupal configuration drift, safety validation, Git commit/push, and exact local/remote parity.

This infrastructure workstream is closed. Reopen only if new evidence proves a defect or a future maintenance requirement changes.
```
