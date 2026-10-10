# Association Portal

Status: PLANNING. Existing Skyhawk Drupal website remains separate. Proposed second Drupal installation: emconalfa.net. WordPress excluded. Public blogs, private board discussions, protected documents, officer workspaces, and email notifications are proposed. No portal has been deployed. Email to Mark: SENT per Gene 2026-10-10 (v3; see 501C3_FILING.md). Design/staging plan: DESIGN_STAGING_PLAN_0.1.md (planning only). Mailbox policy (Gene, 2026-10-10): no user mailboxes on the VPS; the portal sends notification mail only. See platforms/inmotion/OPERATING_REFERENCE_0.1.md for verified hosting facts.

## Direction and product requirements

Gene selected two principal Drupal installations on the InMotion VPS rather than four: the existing skyhawk.org history/archive and a separate emconalfa.net portal for public communications, restricted board operations and eventual additional associations. Public blogs, board discussions, document library and officer areas belong in the portal, not in separate CMS installations. The specific organization/permission model remains to be designed. This does not represent a live application deployment.

Desired capabilities from the supplied discussion: authenticated individual director accounts; board-only topic discussions and searchable history; minutes, bylaws, financial materials and resolutions with version history; private Drupal file delivery protected at the direct URL; officers' restricted financial workspaces; public articles; role-based document uploads/downloads; notification emails linking to the single authoritative copy rather than multiplying attachments. The Secretary should own official records. Casual discussions are not formal votes. Email attachments may be supported but are neither revocable nor the primary channel for confidential documents. Any public comments need moderation.

Use Drupal under CWP with proper isolation of the new database, application files, private files, accounts and backups. The two websites share VPS resources, so failure isolation is not absolute. Composer, compatible PHP, HTTPS hostname coverage, notification delivery, account permissions, independent backup/restore and staged user tests are design/deployment gates. No WordPress, bbPress or cPanel-only controls should be introduced based on the earlier exploratory suggestions.

## Verified infrastructure and open correspondence

InMotion migration cleanup was completed and independently verified on 2026-10-10. The production Drupal site remained accessible via HTTPS (HTTP 200), with 22G of free disk space measured after removal of the old staged copies and transfer archive. Free space is a point-in-time reading. Historical migration files that were not proven redundant were left in place. See the InMotion reference for complete evidence.

The second portal remains NOT DEPLOYED. The email to Mark is OPEN; the earlier draft headed '501(c)(3) filing - you and me, plus an AI assistant' was Claude-written and Gene-relayed, now superseded by integrated draft v2. The draft has not been verified sent. It identifies conversion from 501(c)(7) to 501(c)(3), provisional Form 1023 and 2021-2025 reporting assumptions, Nevada articles questions, and four initial document requests. The draft must reflect two independent AIs and legal/tax assertions need verification. Full workstream: projects/skyhawk/501C3_FILING.md. Do not send without approval. Do not repeat completed hosting cleanup or replace the selected Drupal architecture with WordPress.

## Distinct filing responsibility (Gene decision, 2026-10-10)

The Skyhawk 501(c)(3) C-filing is a separate workstream, documented in `projects/skyhawk/501C3_FILING.md`. **Gene and Mark are the only human filing collaborators, each with their own independent AI**. Gene selects his AI; Mark has his own AI. Gene retains material decisions. The future multi-organization portal is not a prerequisite for filing preparation and its board-wide access features do not imply extra filing helpers. The previous email-to-Mark handoff omitted this critical fact and is superseded accordingly.

## Reconciled user-conversation handoff

The complete cross-workstream summary of filing, two independent AIs, InMotion, public/private blogs, site locations and verified cleanup is `projects/skyhawk/2026-10-10_CROSS_WORKSTREAM_HANDOFF.md`. Read it before producing any combined email or project status. Mark is NOT assigned to build the portal. The filing is not blocked by the portal. Earlier single-topic email drafts omitted this website context and are incomplete for Gene's current request.
