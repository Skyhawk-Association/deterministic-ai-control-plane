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
- Claude and ChatGPT are both authorized executors, one at a time, as Gene chooses. The tunnel (one AI checking the other) happens only when Gene asks for it. Formal record: `authoritative/DACP_Application_Implementation_Authorization_0.7.md`. Gene authorized a controlled VPS administration path on 2026-09-30 for Skyhawk migration and ongoing administration, bounded by current DACP/Skyhawk authority, provider policy, least privilege, auditability, and full pipe qualification.

## Operating facts (non-secret)
- VPS administration path: AUTHORIZED BUT NOT YET QUALIFIED. Do not rely on it until end-to-end request, execution, result read-back, and verification have passed for the assigned executor. Provider-policy compliance is a hard gate.
- Project root `/home/darwus/drupalbeta`; Drush `/home/darwus/drupalbeta/vendor/bin/drush --root=/home/darwus/drupalbeta/web`.
- Commands are pasted at the A2 prompt; wrap each block in a subshell `( ... )` so a failure never logs Gene out. A2 has no `/dev/fd`: no bash process substitution. A2 throttles rapid SSH connections: wait about 5 minutes if refused.
- A2 is a shared hosting server: no AI gets direct access, ever. Gene runs every A2 command.
- HOSTS (Gene 2026-09-30): production skyhawk.org is served by s19522.use2.stableserver.net (the Envy ssh alias A2). mi3-ts4.a2hosting.com is a SEPARATE A2 Hosting account holding an older copy of drupalbeta (max node 49356; no ai-report); the Mac reached it with darwus_backup_key on a non-standard port. NEVER target mi3-ts4 for Skyhawk work. First line of every A2 block should confirm the host (hostname must start s19522).
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
**Last verified step:** Reunion photo actions styling VERIFIED 2026-09-30. `field_reunion_photos_link` and `field_reunion_upload_link` remain on reunion_event node 49466 with their established routes (`/reunions/2026/photos` and `/form/reunion-2026-photo-upload`). The single maintained global stylesheet `skyhawk_site_fixes/css/skyhawk-global.css` was rewritten coherently so the photo-action rules live inside the existing Reunion V2 section rather than as a stray appended block. skyhawk.org commit `f50d215b0b7f706060361c2c01e2ff752ee0c7ec`; AI report `20260930T164313Z-reunion-photo-css-integrate`. Independent public verification confirmed both links, the `skyhawk-reunion-links` group, and the new rules in the CSS aggregate actually served by the Reunion page. OPEN: finish the brisk/airy Reunion landing-page presentation; download and verify backup pre_reunion_landing.sql.gz (+ .sha256) to the Envy, then delete from A2; photo upload failure symptom still not captured.

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


### Reunion photo links — CLOSED 2026-09-30
- CLOSED: the 2026 Reunion page now exposes the two requested photo actions in a sensible grouped location: `View Reunion Photos` -> `/reunions/2026/photos` and `Upload Reunion Photos` -> `/form/reunion-2026-photo-upload`.
- Independent public verification returned HTTP 200 for both destinations. The gallery is the live `reunion_2026_photos` View and the upload destination is the live `reunion_2026_photo_upload` Webform.
- Independent managed-file smoke testing successfully uploaded a synthetic PNG through the public Webform and Drupal returned temporary FID 62444 with no form/upload error. The test stopped before final submission, so no junk public Media was created.
- Existing accepted multi-photo Webform/Media bridge evidence remains valid. No current upload-path failure is reproduced.
- Do not reopen this placement/upload objective without new contradictory evidence from a real contributor failure or a broken public endpoint.

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
- LIVE 2026-09-28, skyhawk.org `cc8b5c4`: `ReunionReadyRoomController` now enforces scoped Reunion management as current `authorized_user` owner UID OR the one assigned `field_reunion_worker` UID. Owner eligibility remains member-gated; a Worker Bee may be a nonmember. No global reunion-event edit permission or administrator bypass was added.
- KISS field model: keep owner identity in Drupal's existing node author/UID; add only one optional single-value user-reference field for the Worker Bee. Do not add a duplicate owner field.
- `ReunionRequestForm` marker `SKYHAWK_REUNION_SOURCE_INTAKE_V1` is the newer self-service intake direction: an active authenticated member may upload one source document or paste source text; Drupal preserves the source, creates an unpublished `reunion_event` draft owned by that account, records source provenance/hash in the revision log, verifies persistence, creates no token and activates no authority.
- Durable authority is account-based, not token-based. The Worker Bee should be a normal Drupal identity whose email control is verified using Drupal core account creation/one-time-login behavior; assignment to one Reunion grants the scoped management authority. Token/verification links may establish identity during transition but are not durable Reunion authority.
- Transitional membership rule, Gene decision 2026-09-28: the Secretary's current membership roster remains the eventual authoritative source for current Association membership, but its delayed availability does not block Reunion implementation. Pending reconciliation against that roster, the existing Drupal user population is accepted as the current dues-paying member baseline because Drupal accounts have historically been issued only to dues-paying members. `authorized_user` is the intended Drupal member-authorization marker to normalize against that existing population. This is a temporary operational proxy, not a replacement for the Secretary's roster. New nonmember Worker Bee accounts must not receive `authorized_user` merely because they can authenticate.
- DONE 2026-09-28, skyhawk.org `cc8b5c4`: the built-in Drupal `Authenticated User` role was reduced to the verified universal logged-in baseline, member-only capabilities were moved/ensured on `authorized_user`, and the accepted pre-Worker-Bee active account population was normalized to `authorized_user`. Institutional powers remain on the narrower existing officer/admin roles. Existing `Reunion Staff` is not used for Worker Bee authority.
- LIVE CUTOVER 2026-09-28, skyhawk.org `cc8b5c4`: the optional single-value user-reference `field_reunion_worker` now exists on `reunion_event`, remains hidden from the generic node edit form, and the owner-only Worker Bee assignment route/source is deployed. A2 PHP lint, cache rebuild, role/field/member-gate verification, Git commit/push, remote SHA read-back, and committed runtime verification all passed. No Worker Bee account has yet been created or assigned; end-to-end assignment/revocation/replacement acceptance remains pending. Evidence: `evidence/skyhawk/20260928-reunion-member-worker-cutover.txt`.
- SOURCE CORRECTION 2026-09-29, skyhawk.org `f9a54901e0257581dc0fcb63c4b03485e52288de`: `ReunionWorkerForm` now verifies Drupal 11.4 `_user_mail_notify('register_admin_created', ...)` using its actual boolean return contract instead of incorrectly treating the return value as a mail-result array. A2 lint, commit/push and remote read-back completed successfully. Prior mail-path failure classifications generated from the bad array assumption are invalid as transport evidence and must not be used to claim mail failure.
- WORKER EMAIL-CONTROL ACCEPTANCE 2026-09-29: the controlled test Worker Bee received Drupal account-created mail and successfully used a one-time-login link after CLI mail generation was run with the explicit production URI `https://skyhawk.org`. Earlier CLI-generated links used Drush's default request host and were unusable. Authentication mechanics are therefore proven through mailbox control and successful login for the test account. A separate UX defect remains: Drupal's stock login/one-time-link error/help messaging is too technical and unhelpful for ordinary members and Worker Bees, so authentication UX should be improved without replacing Drupal core authentication.
- AUTH UX VOICE DECISION 2026-09-29: login, password-reset, one-time-link, and related authentication guidance should use clear plain language with light A-4 / Naval Aviation humor appropriate to the Skyhawk Association. Humor must never obscure the corrective action. Example approved direction for a normal login failure: “We couldn't sign you in with those credentials, but we did sign you up for the midnight watch. Check the creds or use ‘Reset your password’ below.”
- AUTH UX IMPLEMENTED 2026-09-29, skyhawk.org `d8c843ba6e6c6d7d691f0bcb617462b05485ef70`: `skyhawk_site_fixes` now provides presentation-only Naval Aviation authentication guidance for normal login, password reset, and one-time-login flows while leaving Drupal core authentication, flood control, tokens, password handling, privacy behavior, and account state untouched. Installed-core ownership inspection passed before mutation; PHP lint, cache rebuild, runtime read-back of the custom messages/form text, Git commit/push, remote SHA read-back, and final lint/cache rebuild all passed. Human browser acceptance of the actual wrong-credentials, password-reset, and expired/used-link surfaces remains the next UX gate.
- AUTH UX ACCEPTANCE STATUS 2026-09-29: OPEN / NOT ACCEPTED. Browser testing proved a fresh `/user/login` does not show failure guidance before submission, while a failed login does show the custom Paddles-oriented failure text. Gene rejected the current combined/layout presentation as still wrong. Desired failed-login presentation is two distinct pieces: `Paddles sent you around. Watch the ball next time around!` plus `We couldn't sign you in with those credentials. Check the creds or use Reset your password.` where `Reset your password` is the link and ends the sentence; do not append `below`. Preserve Drupal's single generic authentication-failure semantics so unknown-user and wrong-password cases remain indistinguishable. Subsequent attempts to split the presentation were not verified/accepted; one heredoc attempt was aborted with Ctrl-C before execution, so do not infer its mutation state. Repeated manual failure testing triggered Drupal flood control after more than five attempts, producing the stock `Login failed` temporary-block page; Gene considers that page bland but explicitly does not want this slice widened tonight. Before any further edit, inspect live `skyhawk_site_fixes.module`, live Git HEAD/status, and actual browser behavior. Keep core authentication, flood control, privacy/account-enumeration protection, tokens, and password handling untouched.
- AUTH UX MESSAGE MAP (Gene 2026-09-29; code skyhawk.org 54f67f1; BROWSER ACCEPTANCE PENDING): /user/login before submit = Password field description "Passwords are case-sensitive. Caps Lock has ruined more approaches than anyone cares to admit." (kept). After a failed login (unknown user and wrong password stay indistinguishable) = red error "Push Tanker, watch the ball on your next approach." plus separate plain guidance "We couldn't sign you in with those credentials. Check the creds or use [Reset your password]." (link ends the sentence; no "below"). Also live: user_pass help ("Need new credentials?..."), user_pass_reset help ("First time aboard?...", button "Check in"), expired-link rewording ("That launch window has closed..."). Flood page out of scope. Login UX remains the active unfinished slice.
- 403/404 UX ACCEPTED 2026-09-29: Drupal-owned Basic pages are live and wired through `system.site` as the real 403 and 404 handlers at `/access-denied` and `/page-not-found`. Gene edited the page text and added photos in Drupal, then browser-tested the actual error routes and accepted both as good to go. These pages are now normal Drupal content and should be maintained through Drupal rather than custom PHP.
- LOGIN UX ROOT CAUSE 2026-09-29: skyhawk.org commit `9c51f8aa39d9c311b999c6ee24712a105993bd65` is NOT browser-accepted. It successfully removed the Username field-level error styling, but `#disable_inline_form_errors = TRUE` caused Drupal core's parent `FormErrorHandler` to send the remaining form error to Messenger; Bootstrap Barrio is explicitly configured with `bootstrap_barrio_messages_widget: toasts`, so the desired `Push Tanker...` text appeared as the upper-right `Error message` toast. This was a control-application/ownership failure: the prior patch targeted Inline Form Errors without resolving the full render owner chain. Verified route now is `UserLoginForm validation -> form_error_handler -> Messenger -> bootstrap_barrio status messages -> Toasts`. Next repair must preserve a form error so submission remains blocked, keep it off Username, render the red headline plus plain recovery guidance inside the form, and suppress only that exact failed-login Messenger message from the status-message output on `user.login`. Do not globally change Barrio's toast setting or disturb other site messages.
- `ReunionNewsletterUpdateForm` marker `SKYHAWK_REUNION_READY_ROOM_UPDATE_V1` is presently an acceptance fixture limited to Event 49464 and its authenticated owner. It preserves newsletter history, verifies private-to-public copy/hash/persistence and HTTP retrieval, and explicitly labels the general current-member gate as deferred. Do not generalize that fixture by assumption.
- Older token-era routes/forms still exist: `/community/event-submission/{token}`, `/reunion/verify/{token}`, `/reunion/manage/{token}` and the token admin. They are transitional only and are to be retired in toto after the account-based owner/Worker-Bee path is proven.

**Reunion next steps**
1. DONE 2026-09-28 (report 20260928T155448Z-reunion-live-reinspection): all 9 Reunion main-menu links enabled (Reunions, Submit a Reunion /node/49349, My Reunion Events, Request a Reunion, 2026 Reunion, Reunion Photos, Upload Photos, Ready Room x2). Events: 49466 published (2026 hub), 49464 unpublished; 150 persons, 150 attendance. Photo webform open, 29 submissions, 57 contributed-photo media. Ready Room routes 403 for anonymous (correct).
2. DONE 2026-09-28: scalable Reunion front door applied and independently read back from public /reunions. Node 49769 now leads with the general Reunion identity and planning actions. Drupal View reunion_index supplies Current & Upcoming and Reunion Archive blocks. Optional `field_registration_link` is an outbound organizer/provider link; Skyhawk.org is not the registration processor. Follow-up title/date defects are resolved (evidence/skyhawk/20260928-reunion-view-display-fix.txt; skyhawk.org 736bce1).
3. DONE 2026-09-28: legacy token compatibility restored and independently verified (evidence/skyhawk/20260928-reunion-legacy-token-compatibility.txt; skyhawk.org d5c9688). The actual stored historical upload token returns HTTP 200; invalid upload and manage tokens return 404; invalid verify token returns 302. No token value is recorded. Token-format assumptions are removed; exact `hash_equals()` comparison to Drupal state is retained. Legacy token machinery remains transitional only pending account-based owner/Worker-Bee replacement.
4. DONE 2026-09-28: live role/account audit completed, real admin authority was preserved, the built-in `Authenticated User` role was reduced to the safe baseline, and the accepted pre-Worker-Bee active population was normalized to `authorized_user` in skyhawk.org `cc8b5c4`.
5. DONE THROUGH LIVE CUTOVER 2026-09-28: skyhawk.org `cc8b5c4` deployed the safe Authenticated baseline, member normalization, `field_reunion_worker`, current-member owner gate, owner-or-worker Ready Room access, and owner-only Worker Bee assignment surface. End-to-end Worker Bee account/assignment/revocation/replacement/one-Reunion acceptance remains the next gate.
6. APPLIED 2026-09-28: the Secretary's membership roster remains the eventual authoritative membership source and reconciliation is deferred until supplied. The accepted pre-Worker-Bee Drupal account population has now been normalized to the transitional `authorized_user` member-authorization role. New nonmember Worker Bee accounts must remain outside `authorized_user`.
7. Use Drupal core administrator-created-account / one-time-login email flow to establish Worker Bee account/email control; do not invent a second authentication mechanism. Source correction `f9a5490` fixed the Worker Bee form's bad `_user_mail_notify()` return-value verification; determine the actual state of the already-created test Worker Bee account/mail before sending any further account-created notification.
8. Prove owner and Worker Bee end-to-end, including replacement/revocation and one-event-only access. Then retire token routes, token admin, token fields/storage, token controllers/forms/classes, and the remaining node-body link to the token path in one controlled removal.
9. Preserve the accepted 2026 multi-photo Webform/Media architecture. Generalize only the hard-coded Event 49466 binding when a real second-Reunion use case requires it.
10. Keep Reunion work separate from VMA-131/Squadron CMS review; neither is a prerequisite for the other.

**Half-done:** the safe Authenticated baseline, transitional member normalization, scoped Worker Bee field, member-only accountable-owner gate and owner-or-worker Ready Room source are now live and committed. Remaining Reunion activation work is end-to-end Worker Bee account/assignment/revocation/replacement/one-Reunion acceptance, followed by controlled retirement of the superseded Reunion token machinery. Secretary-roster reconciliation remains deferred and is not an activation blocker. The 2026 photo upload remains accepted working infrastructure.

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
