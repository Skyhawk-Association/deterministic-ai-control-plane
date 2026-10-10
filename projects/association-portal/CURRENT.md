# Association Portal

Status: PLANNING. Existing Skyhawk Drupal website remains separate. Proposed second Drupal installation: emconalfa.net. WordPress excluded. Public blogs, private board discussions, protected documents, officer workspaces, and email notifications are proposed. No portal has been deployed. Email to Mark is open and its contents unverified. See platforms/inmotion/OPERATING_REFERENCE_0.1.md for verified hosting facts.

## Direction and product requirements

Gene selected two principal Drupal installations on the InMotion VPS rather than four: the existing skyhawk.org history/archive and a separate emconalfa.net portal for public communications, restricted board operations and eventual additional associations. Public blogs, board discussions, document library and officer areas belong in the portal, not in separate CMS installations. The specific organization/permission model remains to be designed. This does not represent a live application deployment.

Desired capabilities from the supplied discussion: authenticated individual director accounts; board-only topic discussions and searchable history; minutes, bylaws, financial materials and resolutions with version history; private Drupal file delivery protected at the direct URL; officers' restricted financial workspaces; public articles; role-based document uploads/downloads; notification emails linking to the single authoritative copy rather than multiplying attachments. The Secretary should own official records. Casual discussions are not formal votes. Email attachments may be supported but are neither revocable nor the primary channel for confidential documents. Any public comments need moderation.

Use Drupal under CWP with proper isolation of the new database, application files, private files, accounts and backups. The two websites share VPS resources, so failure isolation is not absolute. Composer, compatible PHP, HTTPS hostname coverage, notification delivery, account permissions, independent backup/restore and staged user tests are design/deployment gates. No WordPress, bbPress or cPanel-only controls should be introduced based on the earlier exploratory suggestions.
