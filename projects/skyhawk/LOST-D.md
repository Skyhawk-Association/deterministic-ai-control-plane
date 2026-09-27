# LOST-D — Skyhawk.org active work (passdown)

**Canonical passdown for any AI executor (Claude or ChatGPT).** Read this file first in every session:
`https://raw.githubusercontent.com/Skyhawk-Association/deterministic-ai-control-plane/main/projects/skyhawk/LOST-D.md`

**Update rule:** every verified consequential step updates this file (last verified step, next step, open decisions) and pushes it in the same run as the change. The Drupal LOST-D page (node 2479) points here.

**Public file. Never put here:** passwords, SSH/API keys, token links (upload, manage or verify tokens), member personal data (names, email or contact details of attendees or contributors), backup contents, database contents, server IP addresses.

## Governing references (read before acting)
- Skyhawk Working Rules: `projects/skyhawk/RULES.md` in this repository (public URL `https://raw.githubusercontent.com/Skyhawk-Association/deterministic-ai-control-plane/main/projects/skyhawk/RULES.md`). Binding for every executor.
- Drupal Environment Reference: node 49461. GitHub / Source Reconstruction Reference: node 49463. Termux SSH Notes: node 49458. Site Menu Reference: node 49457.
- Squadron Template 49454, Squadron Roadmap 49453 and `skyhawk_site_fixes/data/squadron-template-contract.php`: superseded for new squadron work by Gene (2026-09-27). Ignore them except the lessons listed under Active slice.

## Executors
- Claude and ChatGPT are both authorized executors, one at a time, as Gene chooses. The tunnel (one AI checking the other) happens only when Gene asks for it. Formal record pending: DACP Authorization 0.6.

## Operating facts (non-secret)
- Project root `/home/darwus/drupalbeta`; Drush `/home/darwus/drupalbeta/vendor/bin/drush --root=/home/darwus/drupalbeta/web`.
- Commands are pasted at the A2 prompt; wrap each block in a subshell `( ... )` so a failure never logs Gene out. A2 has no `/dev/fd`: no bash process substitution. A2 throttles rapid SSH connections: wait about 5 minutes if refused.
- Files move by `scp` from Windows (host alias `A2`); Gene's working folder is `C:\Users\genea\dacp-work\vma131`.
- skyhawk.org Git remote is private (`github-skyhawk` identity, account geneatwell). The same identity pushes this DACP repo (clone on A2: `/home/darwus/dacp-repo`). Organization deploy keys are disabled.
- Composer only via `bin/skyhawk-composer` (require or update, then functional check, then `finish`). Its pending marker is git-ignored.
- Configuration: site-wide `config:import` fails validation because of orphaned configuration from old modules and themes. Apply structure through the entity API, then `drush config:export -y`, then commit only the expected files.
- Backups before structural database work: dump to `/home/darwus/skyhawk_backups`, download to the Envy (`Desktop\ChatGPT\pre_update_<version>_<timestamp>\database.sql.gz`), verify SHA-256, then delete the server copy.
- Styling: one global stylesheet `skyhawk_site_fixes/css/skyhawk-global.css` and its semantic vocabulary (skyhawk-focus, -feature, -context, -note, -reference; modifiers -navy, -marine, -joint, -heritage; skyhawk-focus-label).

## Active slice: Squadron CMS, VMA-131 test build
**Last verified step:** Skyhawk Working Rules moved to Git as `projects/skyhawk/RULES.md`, AI-neutral, with the shared-passdown rule (DACP repository, same push as this passdown). Before that: View `squadron_collection`, skyhawk.org commit `1235ae1`.

**State**
- Content type `squadron`: identity, snapshot, story, people, featured story, aircraft, remember and research fields, plus the 14 detailed-record sections. Legacy body kept but hidden. Tabbed edit form (Field Group).
- Display: Field Group panels using the global semantic classes; kickers use `skyhawk-focus-label`; the featured title is an h3.
- Media: vocabulary `unit_collections` (Voices, Research, Visual record, Final Inspection, and the rest). Document and image media carry Unit, Collection, Heading, Order and Description. One media record per placement, named "Title · Collection"; files are never copied. VMA-131 has 14 placements.
- View `squadron_collection` has three EVA displays (Voices, Research, Visual record), filtered by the page's unit and placed inside their panels. Links open in a new window.
- Test node **49779**, unpublished, at `/squadrons/vma-131-test`. The live VMA-131 page, node 49417 at `/article-unit/vma131`, is unchanged until Brian Putney signs off. `/squadrons/vma-131-preview` redirects 301 to it.
- VMA-131 assets: 356 images in `sites/default/files/vma131-preview/images` (with `manifest.tsv`; 1 placeholder photo pending from Brian). Interim section pages are nodes 49770–49777.
- Modules added: field_group 4.0, eva 3.1. Core 11.4.8, webform 6.3.1 (security updates applied 2026-09-27).

**Lessons kept from the old template:** thumbnails open the original in a new window, with a way back to the squadron page; Gabby's Histories is linked with the unit preselected; no large aircraft-assignment tables on the landing page; the complete Commanding Officers list is collapsible on the landing page; scrape the target unit first; never clone another unit's content.

**Next steps (in order)**
0. Governance handoff: point Drupal nodes 49418 (Rules) and 2479 (LOST-D) at Git; move a sanitized Environment Reference (49461) to Git; record DACP Authorization 0.6 (both AIs authorized executors). Then continue with step 1.
1. Shared contribute block: a second EVA view over the node, building the Share a Story, Add Photographs, Send a Correction, photo archive and Gabby buttons from the unit designation.
2. Take `field_sq_assigned_aircraft` off the landing display, with a Gabby link instead.
3. Brian's collections (199 documents, 356 images) as per-placement media, using `vma131_mapping.json` from Gene's working folder. Collection pages via Views at `/squadrons/vma-131/<collection>`.
4. Unit identity on the `skyhawk_units` term (service mapped to the navy, marine, joint or heritage modifier). How the class gets applied is still to be decided.
5. Parity check against node 49417, then Gene's review, Brian's sign-off and cutover.
6. Documentation: the Environment Reference's Squadron CMS section (a draft exists, shelved until 131 is done).

**Open decisions (Gene):** make Rules section 6 (evidence transport) AI-neutral; choose the canonical Windows evidence folder; choose the unit-identity class mechanism; approve orphaned-configuration cleanup; delete node 49778; fix the journal PDF URI error in the logs; send the drafted email to Brian after the page review.

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
