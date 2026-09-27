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
- Large outputs: `( commands ) 2>&1 | ~/bin/ai-report "task"` pushes a secret-scanned report to evidence/skyhawk/ in this repository; paste only its one-line result.
- skyhawk.org Git remote is private (`github-skyhawk` identity, account geneatwell). The same identity pushes this DACP repo (clone on A2: `/home/darwus/dacp-repo`). Organization deploy keys are disabled.
- Composer only via `bin/skyhawk-composer` (require or update, then functional check, then `finish`). Its pending marker is git-ignored.
- Never pipe or `tail` a command that asks a question (`skyhawk-composer finish`, anything without `-y`): the prompt is hidden and Enter answers No.
- Configuration: site-wide `config:import` fails validation because of orphaned configuration from old modules and themes. Apply structure through the entity API, then `drush config:export -y`, then commit only the expected files.
- Backups before structural database work: dump to `/home/darwus/skyhawk_backups`, download to the Envy (`Desktop\ChatGPT\pre_update_<version>_<timestamp>\database.sql.gz`), verify SHA-256, then delete the server copy.
- Styling: one global stylesheet `skyhawk_site_fixes/css/skyhawk-global.css` and its semantic vocabulary (skyhawk-focus, -feature, -context, -note, -reference; modifiers -navy, -marine, -joint, -heritage; skyhawk-focus-label).

## Active slice: Squadron CMS, VMA-131 test build
**Last verified step:** Step 3b: designated reviewer access verified 2026-09-27. The reviewer account is active, has the CO role, and Drupal access checks returned YES for the unpublished CMS test node 49779 and the related review nodes. Step 3a visual result was accepted by Gene as "much better". Skyhawk.org styling commit: 7eafd3d.

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
4. Unit identity on the `skyhawk_units` term. Read-only menu crawl completed 2026-09-27 from the four Units branches: 214 menu links, 212 unique article-unit URLs; 139 Navy, 50 Marine, 18 non-U.S.A. military, 7 civilian links. Two legacy pages are cross-listed across Navy/Marine (`/article-unit/fagu` and `/article-unit/naf-willow-grove`), proving menu placement is classification input rather than a permanent identity key. Stable unit identity must remain separate from historical designation/lineage. No Drupal mutation yet; exact term fields/class mechanism still to be decided.
5. Parity check against node 49417, then Gene's review, Brian's sign-off and cutover.
6. Documentation: the Environment Reference's Squadron CMS section (a draft exists, shelved until 131 is done).

**Open decisions (Gene):** choose the canonical Windows evidence folder; choose the unit-identity class mechanism; approve orphaned-configuration cleanup; delete node 49778; fix the journal PDF URI error in the logs.

**Half-done:** none.

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
