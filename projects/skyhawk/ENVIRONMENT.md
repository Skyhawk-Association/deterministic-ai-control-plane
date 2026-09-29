# Drupal Environment Reference (skyhawk.org)

**Canonical copy:** this file (`projects/skyhawk/ENVIRONMENT.md`, public DACP repository). Drupal node 49461 points here.

**Migrated** 2026-09-27 from Drupal node 49461 revision 68216. Sanitized for publication: 3 server address(es) and 0 email address(es) removed; 2 version line(s) updated to 11.4.8. The section “Current truth added at migration” records changes not yet reflected in the migrated text. File listings are carried over verbatim.

---

## Directory / Build

- Real docroot: /home/darwus/drupalbeta/web (NOT /home/darwus/public_html/drupalbeta or any variant)

- Drupal version: 11.4.8

- PHP version: 8.4.20 (binary: /opt/alt/php84/usr/bin/php)

- Database: darwus_beta (MySQL/MariaDB)

- Public files: sites/default/files

- Private files: /home/darwus/drupalbeta/web/private

- Custom modules directory: web/modules/custom/

- Real error log: /home/darwus/drupalbeta/web/error_log (there are other error_log files on this account belonging to unrelated sites — e.g. drupaltest.emconalfa.net — do not trust a log without confirming which site it belongs to)

## Custom Modules

- skyhawk_site_fixes — primary site-specific integration module. Contains the upload token system, mail hooks, reunion system, journal upload, PageMessageTrait.

- skyhawk_gallery — renders dir_listing nodes as filesystem image galleries. Contains PhotoContributionForm.php — the established working pattern for managed_file uploads on this site. Still uses Drupal messenger() popups (not yet converted to PageMessageTrait) — do not copy that part of the pattern.

- yp_memorial — displays YP memorial memories from Webform submissions.

- skyhawk_sdo_contact.zip, skyhawk_sdo_contact_patch.zip, skyhawk_sdo_router.zip — present on disk, not extracted/audited. See /blade/sdo-system-status.

## Key Contrib Modules Installed (partial list, direct deps)

- drupal/dropzonejs — installed and enabled, but confirmed unused anywhere in custom code or config as of 2026-08-24. Do not assume it's wired into anything.

- drupal/webform, drupal/pathauto, drupal/token, drupal/redirect, drupal/simple_sitemap, drupal/simplenews

- drupal/entity_browser, drupal/entity_browser_block, drupal/entity_embed, drupal/embed

- drupal/views_bootstrap, drupal/views_bulk_operations, drupal/views_data_export, drupal/views_infinite_scroll

- drupal/ctools, drupal/devel, drupal/upgrade_status

- drupal/csv_importer, drupal/csv_serialization

- drupal/image_effects, drupal/file_mdm, drupal/sophron

- drupal/layout_builder_restrictions, drupal/layout_builder_styles

## Established Patterns to Reuse

- File upload: Drupal's native managed_file form element with #multiple => TRUE, #upload_location, #upload_validators — see skyhawk_gallery/PhotoContributionForm.php and skyhawk_site_fixes/UploadTokenForm.php.

- Inline one-shot messages (no Drupal messenger popup): skyhawk_site_fixes/src/Traits/PageMessageTrait.php.

- Email sending: hook_mail() in skyhawk_site_fixes.module, dispatched via \Drupal::service('plugin.manager.mail')->mail().

- Per-request/token-gated routes: always call \Drupal::service('page_cache_kill_switch')->trigger() to prevent Drupal's page cache (default max-age 3600) from serving stale state.

## A2 Command-Line Access

- Host: [server address removed; use the A2 alias in the SSH config on Gene’s machines]; user: darwus; SSH port: 22.

- Windows canonical connection when a reconnect is required: `ssh -o ConnectTimeout=20 -a A2` (20-second connection timeout added because A2 currently has intermittent connection-delay/failure behavior). Do not reconnect when already at the A2 prompt. Windows file transfers use the configured host alias, for example `scp SOURCE A2:DESTINATION`.

- Pixel connection: ssh -p 22 darwus@[server address removed; use the A2 alias in the SSH config on Gene’s machines].

- Normal command-line work occurs interactively at the A2 prompt. Pixel-to-A2 non-interactive SSH is not the normal Drupal/Drush execution method.

- Backup-download exception and Pixel operational details are maintained in Termux Notes. Database backup policy remains governed by the Rules.

## AI Evidence Transport - Current State

- A2 immutable diagnostic-report production is reliable. The canonical immutable report is /home/darwus/drupalbeta/web/downloads/chatgpt-debug-<Report-ID>.txt; chatgpt-debug-latest.txt is the transient convenience copy.

- Direct ChatGPT retrieval of newly published Skyhawk public TXT or HTML diagnostic objects is not reliable and is not an accepted automatic transport.

- /usr/sbin/sendmail is present on A2. On 2026-09-04, A2-to-Gmail-to-ChatGPT transport succeeded end-to-end once using Report-ID 20260904T003436Z-1007053. ChatGPT independently retrieved and read the complete message body with the matching Report-ID and SHA-256.

- Email relay is proven transport capability but is not the normal workflow because the current ChatGPT Business environment does not expose an automatic Gmail-arrival trigger. It therefore still requires human initiation and adds inbox clutter.

- Google Drive to ChatGPT read is proven. No authenticated A2-to-Google-Drive write path has been proven.

- The current interim AI evidence handoff is manual copy/paste from the immutable report URL into the active chat, followed by AI validation of the current Report-ID. This is temporary pending a proven automatic transport.

## PDF / Python Tooling

- Canonical PDF-processing Python runtime: /home/darwus/virtualenv/skyhawk_py310/3.10/bin/python3.10.

- Verified Python version: 3.10.20.

- pdfminer / pdfminer.six is available in that virtualenv; verified version 20260107.

- The same virtualenv also exposes python, python3, and python3.10; use the explicit python3.10 path in durable procedures.

- pypdf, PyPDF2, and fitz / PyMuPDF are not installed.

- Poppler command-line tools pdfinfo, pdftotext, and pdfimages are not available.

- For current PDF inspection or text extraction, use the documented Python 3.10 virtualenv and pdfminer. Do not issue procedures that depend on unavailable PDF libraries or command-line tools unless their installation is separately authorized, verified, and this reference is updated.

## Journal Index Architecture

- Authoritative live Journal article-index bundle: skyhawk_association_journal_inde; verified node count: 534.

- The nominal journal_index content type has 0 nodes and is not the live article-index owner.

- The Public Skyhawk Journal Index and Skyhawk Journal Index Views use skyhawk_association_journal_inde.

- Historical Raven source data is retained at /home/darwus/drupalbeta/journal_index_work/raven_journal_index_534.csv. The former standalone raw SQL journal_index table remains retired.

- Verified Raven-derived indexed boundaries are record 1, Summer 2004, through record 534, Winter 2019.

- The live article-index records already provide Article, Author Last Name, First Name, Category, Issue, Year, Journal Number, Page, PDF Access, and Record fields.

- For the indexed historical period, existing Drupal article metadata is the baseline. Processing a Journal PDF must not rediscover or overwrite that metadata unless a reviewed correction is explicitly accepted.

- Journals from 1995 through the second Journal of 2004 remain outside the Raven-derived indexed coverage and require separate article-metadata completion.

## Drupal Environment - Live Technical Map
Purpose: Durable current architecture needed to continue Skyhawk.org work without rediscovery. Transient diagnostics and rapidly aging update availability are generated when needed rather than stored here.

### Runtime and Platform

- Drupal core: 11.4.8

- PHP: 8.4.20

- Drush:

- Composer: Composer version 2.9.4 2026-01-22 14:08:50

- Drupal document root: /home/darwus/drupalbeta/web

- Database driver: mysql; server version: 11.4.11-MariaDB

- Current Drupal DB-session isolation: REPEATABLE-READ

- HTTP server header: server: LiteSpeed

### Command-Line Access

- Normal command-line work occurs interactively at the A2 prompt.

- Canonical Pixel connection: ssh -p 22 darwus@[server address removed; use the A2 alias in the SSH config on Gene’s machines].

- Windows command-line access uses the established SSH config host alias A2: interactive connection ssh -a A2; Windows file transfers use A2: as the remote host. Pixel access remains separate and uses the explicit host/user/port documented above.

- Normal work leaves the A2 session open. Exit/reconnect is reserved for required local downloads such as verified database backups.

### Themes and Asset Delivery

- Default theme: bootstrap_barrio

- Admin theme: bootstrap_barrio

- CSS aggregation: enabled; JS aggregation: enabled.

- Aggregated browser filenames are delivery artifacts and are not authoritative evidence of source ownership.

Installed/enabled themes (2)
- Bootstrap Barrio [bootstrap_barrio] | themes/contrib/bootstrap_barrio | DEFAULT, ADMIN

- Claro [claro] | core/themes/claro

### Canonical Skyhawk CSS / JS Ownership

- Global Skyhawk CSS owner: modules/custom/skyhawk_site_fixes/css/skyhawk-global.css - present.

- Site-specific integration belongs under modules/custom/skyhawk_site_fixes, not inside contributed projects.

- Semantic visual vocabulary: skyhawk-focus, skyhawk-feature, skyhawk-context, skyhawk-note, skyhawk-reference, skyhawk-navy, skyhawk-marine, skyhawk-joint, skyhawk-heritage.

- Bold colors are punctuation; muted colors are prose. Color is never the sole indicator of meaning.

- LOST-D is the proving page for the semantic visual system.

Custom CSS / JS files (27)
- modules/custom/skyhawk_site_fixes/backups/attach-managed-file-queue-20260825T215707Z-3404996/managed_file_queue.js

- modules/custom/skyhawk_site_fixes/backups/core-handoff-20260825T194442Z-3404996/serial_managed_file_upload.js

- modules/custom/skyhawk_site_fixes/backups/deployment-gate-reconcile-20260825T145100Z-2795997/upload_transition_observer.js

- modules/custom/skyhawk_site_fixes/backups/fix-two-proven-defects-20260825T205540Z-3404996/upload_token_public.css

- modules/custom/skyhawk_site_fixes/backups/live-observer-integration-20260825T145539Z-2795997/upload_transition_observer.js

- modules/custom/skyhawk_site_fixes/backups/native-serial-cleanup-20260825T202106Z-3404996/serial_managed_file_upload.js

- modules/custom/skyhawk_site_fixes/backups/observer-execution-proof-20260825T150130Z-2795997/upload_transition_observer.js

- modules/custom/skyhawk_site_fixes/backups/observer-standalone-20260825T150751Z-2795997/upload_transition_observer.js

- modules/custom/skyhawk_site_fixes/backups/pixel-picker-transition-20260825T151419Z-2795997/pixel_execution_probe.js

- modules/custom/skyhawk_site_fixes/backups/remove-serializer-20260825T203611Z-3404996/serial_managed_file_upload.js

- modules/custom/skyhawk_site_fixes/backups/remove-serializer-artifacts-20260825T203955Z-3404996/serial_managed_file_upload.js

- modules/custom/skyhawk_site_fixes/backups/serial-three-trace-20260825T195352Z-3404996/serial_managed_file_upload.js

- modules/custom/skyhawk_site_fixes/backups/trace-prereq-20260825T195657Z-3404996/serial_managed_file_upload.js

- modules/custom/skyhawk_site_fixes/backups/universal-uploader-20260825T233305Z-3404996/managed_file_queue.js

- modules/custom/skyhawk_site_fixes/backups/universal-uploader-20260825T234003Z/managed_file_queue.js

- modules/custom/skyhawk_site_fixes/backups/upload-product-replacement-20260825T005953Z-2471164/upload_token_mobile_fix.js

- modules/custom/skyhawk_site_fixes/backups/upload-product-replacement-20260825T013552Z-2471164/upload_token_mobile_fix.js

- modules/custom/skyhawk_site_fixes/css/legacy.css

- modules/custom/skyhawk_site_fixes/css/model-build.css

- modules/custom/skyhawk_site_fixes/css/modeling-review.css

- modules/custom/skyhawk_site_fixes/css/skyhawk-global.css

- modules/custom/skyhawk_site_fixes/css/squadron.css

- modules/custom/skyhawk_site_fixes/css/upload_token_public.css

- modules/custom/skyhawk_site_fixes/js/gabby-unit-autocomplete.js

- modules/custom/skyhawk_site_fixes/js/pixel_execution_probe.js

- modules/custom/skyhawk_site_fixes/js/squadron.js

- modules/custom/skyhawk_site_fixes/js/upload_transition_observer.js

### Enabled Drupal Modules
Descriptions below come from the installed extension metadata. Current update availability is intentionally not stored here; query Composer/Drupal live.
Enabled modules (99)
- Actions Permissions [actions_permissions] | Views Bulk Operations | Adds access permissions on all actions allowing admins to restrict access on a per-role basis.

- Automated Cron [automated_cron] | Core | Provides an automated way to run cron jobs, by executing them at the end of a server response.

- Automatic Entity Labels [auto_entitylabel] | Entity | Allows hiding of entity label fields and automatic label creation.

- Ban [ban] | Core | Allows banning visits from specific IP addresses.

- BigPipe [big_pipe] | Core | Sends pages using the BigPipe technique that allows browsers to show them much faster.

- Block Content [block_content] | Core | Allows the creation of content blocks and block types.

- Block [block] | Core | Allows users to configure blocks (containing content, forms, etc.) and to place them in the regions of a theme.

- Breakpoint [breakpoint] | Core | Manages breakpoints and breakpoint groups for responsive designs.

- Chaos Tools [ctools] | Chaos tool suite | Provides a number of utility and helper APIs for Drupal developers and site builders.

- CKEditor5 Table Fix [ckeditor5_table_fix] | CKEditor 5 | Adds support for tables in CKEditor5, including and other elements.

- CKEditor 5 [ckeditor5] | Core | Provides the CKEditor 5 rich text editor.

- Configuration Manager [config] | Core | Allows importing and exporting configuration changes.

- Contact storage [contact_storage] | Other | Provides storage and edit capability for contact messages.

- Contact [contact] | Core | Provides site-wide contact forms and forms to contact individual users.

- Content Moderation [content_moderation] | Core | Provides additional publication states that can be used by other modules to moderate content.

- Contextual Links [contextual] | Core | Provides contextual links to directly access tasks related to page elements.

- CSV Importer [csv_importer] | CSV | Import content from CSV.

- Custom Menu Links [menu_link_content] | Core | Allows users to create menu links.

- Database Logging [dblog] | Core | Logs system events in the database.

- Datetime Range [datetime_range] | Field types | Provides the ability to store end dates.

- Datetime [datetime] | Field types | Defines field types for storing dates and times.

- Devel [devel] | Development | Various blocks, pages, and functions for developers.

- DropzoneJS entity browser widget [dropzonejs_eb_widget] | Media | DropzoneJS Entity browser widget.

- dropzonejs [dropzonejs] | Media | The Drupal integration for DropzoneJS.

- Embed [embed] | Filters | Provides a framework for different types of embeds in text editors.

- Entity Browser Block [entity_browser_block] | Media | Derives block plugins for every Entity Browser on your site

- Entity Browser [entity_browser] | Media | Provide a generic entity browser/picker/selector.

- Entity Embed [entity_embed] | Filters | Allows entities to be embedded using a text editor.

- Entity Mask [ctools_entity_mask] | Other | Allows an entity type to borrow the fields and display configuration of another entity type.

- Entity [entity] | Other | Provides expanded entity APIs, which will be moved to Drupal core one day.

- Feeds [feeds] | Feeds | Aggregates RSS/Atom/RDF feeds, imports CSV files and more.

- Field UI [field_ui] | Core | Provides a user interface for the Field module.

- Field [field] | Core | Provides the capabilities to add fields to entities.

- File Download Link Media [file_download_link_media] | Field | Adds field formatter to render Media reference fields as download link very directly.

- File Download Link [file_download_link] | Field | Adds field formatter to render file field as configurable download link.

- File metadata - EXIF [file_mdm_exif] | File metadata | Provides a file metadata plugin for EXIF image information.

- File metadata - Font [file_mdm_font] | File metadata | Provides a file metadata plugin for TTF/OTF/WOFF font information.

- File metadata manager [file_mdm] | File metadata | Provides a service to manage file metadata.

- File [file] | Field types | Provides a field type for files and defines a "managed_file" Form API element.

- Filter [filter] | Core | Filters text content in preparation for display.

- Image Effects [image_effects] | Media | Provides effects and operations for the Image API.

- Image [image] | Field types | Defines a field type for image media and provides display configuration tools.

- Inline Entity Form [inline_entity_form] | Fields | Provides a widget for inline management (creation, modification, removal) of referenced entities.

- Inline Form Errors [inline_form_errors] | Core | Places error messages adjacent to form inputs, for improved usability and accessibility.

- Internal Dynamic Page Cache [dynamic_page_cache] | Core | Caches pages, including those with dynamic content, for all users.

- Internal Page Cache [page_cache] | Core | Caches pages for anonymous users and can be used when external page cache is not available.

- Layout Builder Expose All Field Blocks [layout_builder_expose_all_field_blocks] | Core | When enabled, this module exposes all fields for all entity view displays. When disabled, only entity type bundles that have layout builder enabled will have their fields exposed. Enabling this module could significantly decrease performance on sites with a large number of entity types and bundles.

- Layout Builder Restrictions [layout_builder_restrictions] | Layout Builder | Manage which fields & layouts are available in Layout Builder

- Layout Builder Styles [layout_builder_styles] | Layout Builder | Apply styles to blocks in Layout Builder.

- Layout Builder [layout_builder] | Core | Allows users to add and arrange blocks and content fields directly on the content.

- Layout Discovery [layout_discovery] | Core | Provides a way for modules or themes to register layouts.

- Libraries [libraries] | Other | Allows version-dependent and shared usage of external libraries.

- Link [link] | Field types | Provides a field type for internal and external URLs.

- Media Library [media_library] | Core | Enhances the media list with additional features to more easily find and use existing media items.

- Media [media] | Core | Manages the creation, configuration, and display of media items.

- Menu UI [menu_ui] | Core | Provides a user interface for managing menus.

- MySQL [mysql] | Core | Provides the MySQL database driver.

- Node [node] | Core | Manages the creation, configuration, and display of the main site content.

- Options [options] | Field types | Defines field types with select lists, checkboxes, and radio buttons to select values from fixed lists of options.

- Password Compatibility [phpass] | Core | Provides the password checking algorithm for user accounts created with Drupal prior to version 10.1.0.

- Path alias [path_alias] | Core | Provides the API allowing to rename URLs.

- Pathauto [pathauto] | Other | Provides a mechanism for modules to automatically generate aliases for the content they manage.

- Path [path] | Core | Allows users to create custom URLs for existing paths on the site.

- Redirect [redirect] | Other | Allows users to redirect from old URLs to new URLs.

- RESTful Web Services [rest] | Web services | Provides a framework for exposing REST resources.

- Search node [search_node] | Core | Provides a search plugin for searching content.

- Search [search] | Core | Allows users to create search pages based on plugins provided by other modules.

- Serialization (CSV) [csv_serialization] | Web services | Provides CSV as a serialization format.

- Serialization [serialization] | Web services | Provides a service for converting data to and from formats such as JSON and XML.

- Serial [serial] | Field types | Defines atomic auto increment (serial) field type.

- Simplenews [simplenews] | Mail | Send newsletters to subscribed email addresses. For uninstall go to Configuration > Web services > Simplenews > Settings and hit "Prepare uninstall".

- Simple XML Sitemap [simple_sitemap] | SEO | Generates standard-compliant hreflang XML sitemaps to enhance your site's SEO, notifies search engines of website changes via IndexNow and sitemap ping protocols, and provides a framework for developing other sitemap types.

- Skyhawk Gallery [skyhawk_gallery] | Custom | Renders dir_listing nodes as filesystem image galleries.

- Skyhawk Site Fixes [skyhawk_site_fixes] | Custom | Site-specific CSS fixes for Skyhawk Drupal 10.

- Sophron [sophron] | Other | Provides an extensive MIME types management API.

- Standard [standard] | Other | Install with commonly used features pre-configured.

- Syslog [syslog] | Core | Logs events to the web server's system log.

- System [system] | Core | Provides user interfaces for core systems.

- Taxonomy [taxonomy] | Core | Enables the categorization of content.

- Telephone [telephone] | Field types | Defines a field type for telephone numbers.

- Text Editor [editor] | Core | Provides a framework to associate text editors (like WYSIWYGs) and toolbars with text formats.

- Text [text] | Field types | Defines field types for short and long text with optional summaries.

- Token Filter [token_filter] | Other | Allows token values to be used as filters.

- Token [token] | Other | Provides a user interface for the Token API and some missing core tokens.

- Toolbar [toolbar] | Core | Provides an administration toolbar to display links provided by modules.

- Typed Data [typed_data] | Other | Extends the core Typed Data API with new APIs and features.

- Update Status [update] | Core | Checks for updates and can notify users if there are new releases available.

- User [user] | Core | Allows users to register and log in, and manages user roles and permissions.

- Video Embed Field [video_embed_field] | Video Embed Field | Provides a field type for displaying videos from 3rd party providers such as YouTube and Vimeo.

- Views Bootstrap 5 [views_bootstrap] | Views | Allows for different styles to be used in views to work with Bootstrap 5 components.

- Views Bulk Operations [views_bulk_operations] | Views | Adds an ability to perform bulk operations on selected entities from view results.

- Views Data Export [views_data_export] | Views | Plugin to export views data into various file formats.

- Views Infinite Scroll [views_infinite_scroll] | Views | A pager which allows an infinite scroll effect for views.

- Views UI [views_ui] | Core | Provides a user interface for creating and managing views.

- Views [views] | Core | Provides a framework to fetch information from the database and to display it in different formats.

- Webform UI [webform_ui] | Webform | Provides a user interface for building and maintaining webforms.

- Webform [webform] | Webform | Enables the creation of webforms and questionnaires.

- Workflows [workflows] | Core | Provides an interface to create workflows with transitions between different states (for example publication or user status) provided by other modules.

- YP Memorial [yp_memorial] | Custom | Displays YP memorial memories from Webform submissions.

### Custom Modules and Purpose

- Skyhawk Gallery [skyhawk_gallery] - Renders dir_listing nodes as filesystem image galleries. - modules/custom/skyhawk_gallery

- Skyhawk Site Fixes [skyhawk_site_fixes] - Site-specific CSS fixes for Skyhawk Drupal 10. - modules/custom/skyhawk_site_fixes

- YP Memorial [yp_memorial] - Displays YP memorial memories from Webform submissions. - modules/custom/yp_memorial

Custom architecture files (57)
- modules/custom/skyhawk_gallery/skyhawk_gallery.info.yml

- modules/custom/skyhawk_gallery/skyhawk_gallery.module

- modules/custom/skyhawk_gallery/skyhawk_gallery.permissions.yml

- modules/custom/skyhawk_gallery/skyhawk_gallery.routing.yml

- modules/custom/skyhawk_gallery/skyhawk_gallery.services.yml

- modules/custom/skyhawk_site_fixes/backups/attach-managed-file-queue-20260825T215707Z-3404996/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/core-handoff-20260825T194442Z-3404996/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/core-managed-file-control-20260825T165546Z-3404996/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/backups/deployment-gate-20260825T144330Z-2795997/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/deployment-gate-20260825T144330Z-2795997/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/backups/deployment-gate-reconcile-20260825T145100Z-2795997/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/deployment-gate-reconcile-20260825T145100Z-2795997/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/backups/fix-two-proven-defects-20260825T205540Z-3404996/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/generic-uploader-reconcile-20260826T012923Z-1245077/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/live-observer-integration-20260825T145539Z-2795997/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/live-observer-integration-20260825T145539Z-2795997/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/backups/managed-file-queue-20260825T215118Z-3404996/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/managed-file-server-trace-20260825T210301Z-3404996/skyhawk_site_fixes.module

- modules/custom/skyhawk_site_fixes/backups/multipart-ingress-20260825T182043Z-3404996/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/backups/native-serial-cleanup-20260825T202106Z-3404996/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/native-serial-cleanup-20260825T202106Z-3404996/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/backups/observer-execution-proof-20260825T150130Z-2795997/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/observer-execution-proof-20260825T150130Z-2795997/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/backups/observer-standalone-20260825T150751Z-2795997/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/pixel-direct-probe-20260825T151003Z-2795997/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/backups/pixel-observer-20260825T140951Z-2676184/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/pixel-observer-20260825T140951Z-2676184/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/backups/pixel-picker-transition-20260825T151419Z-2795997/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/public-upload-inline-status-20260826T023619Z-1245077/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/backups/public-upload-three-failures-20260826T030142Z-1245077/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/backups/public-upload-ux-owner-fix-20260826T025756Z-1245077/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/backups/remove-serializer-20260825T203611Z-3404996/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/remove-serializer-artifacts-20260825T203955Z-3404996/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/request-size-probe-20260825T181121Z-3404996/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/backups/rollback-ingress-observer-20260825T212918Z-3404996/skyhawk_site_fixes.services.yml

- modules/custom/skyhawk_site_fixes/backups/runtime-route-rebuild-20260825T145745Z-2795997/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/backups/serial-managed-file-20260825T184306Z-3404996/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/serial-three-trace-20260825T195352Z-3404996/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/trace-discovery-fix-20260825T195928Z-3404996/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/trace-discovery-fix-20260825T195928Z-3404996/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/backups/trace-prereq-20260825T195657Z-3404996/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/trace-prereq-20260825T195657Z-3404996/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/backups/universal-uploader-20260825T233305Z-3404996/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/universal-uploader-20260825T234003Z/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/upload-product-replacement-20260825T005953Z-2471164/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/upload-product-replacement-20260825T005953Z-2471164/skyhawk_site_fixes.module

- modules/custom/skyhawk_site_fixes/backups/upload-product-replacement-20260825T005953Z-2471164/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/backups/upload-product-replacement-20260825T013552Z-2471164/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/backups/upload-product-replacement-20260825T013552Z-2471164/skyhawk_site_fixes.module

- modules/custom/skyhawk_site_fixes/backups/upload-product-replacement-20260825T013552Z-2471164/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.info.yml

- modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.libraries.yml

- modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.module

- modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.routing.yml

- modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.services.yml

- modules/custom/yp_memorial/yp_memorial.info.yml

- modules/custom/yp_memorial/yp_memorial.routing.yml

Custom routes (14)
- skyhawk_gallery.photo_contribute | modules/custom/skyhawk_gallery/skyhawk_gallery.routing.yml

- skyhawk_gallery.photo_review | modules/custom/skyhawk_gallery/skyhawk_gallery.routing.yml

- skyhawk_gallery.unknowns | modules/custom/skyhawk_gallery/skyhawk_gallery.routing.yml

- skyhawk_site_fixes.journal_upload | modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.routing.yml

- skyhawk_site_fixes.managed_file_core_control | modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.routing.yml

- skyhawk_site_fixes.reunion_manage | modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.routing.yml

- skyhawk_site_fixes.reunion_token_admin | modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.routing.yml

- skyhawk_site_fixes.reunion_upload | modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.routing.yml

- skyhawk_site_fixes.reunion_verify | modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.routing.yml

- skyhawk_site_fixes.system_status | modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.routing.yml

- skyhawk_site_fixes.upload_token_admin | modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.routing.yml

- skyhawk_site_fixes.upload_token_view | modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.routing.yml

- skyhawk_site_fixes.upload_transition_observation | modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.routing.yml

- yp_memorial.memories | modules/custom/yp_memorial/yp_memorial.routing.yml

Custom services (0)
Custom libraries (8)
- skyhawk_site_fixes/gabby_unit_autocomplete | modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.libraries.yml

- skyhawk_site_fixes/global | modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.libraries.yml

- skyhawk_site_fixes/legacy | modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.libraries.yml

- skyhawk_site_fixes/model_build | modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.libraries.yml

- skyhawk_site_fixes/modeling_review | modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.libraries.yml

- skyhawk_site_fixes/squadron | modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.libraries.yml

- skyhawk_site_fixes/upload_token_public | modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.libraries.yml

- skyhawk_site_fixes/upload_transition_observer | modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.libraries.yml

### Content Architecture
Node content types (26)
- 155242-155289 [155242_155289]

- Article [article]

- Article-Board [article_board]

- Article-Journal-Private [article_journal_private]

- Article-Journal-Public [article_journal_public]

- article-modeling [article_modeling]

- article-readyroom [article_readyroom]

- article-unit [article_unit]

- Attendee Memory [attendee_memory]

- Book page [book]

- BuNo Purchase Batch [buno_batch]

- Bureau Numbers [bureau_numbers]

- Directory listing [dir_listing]

- Gabby's Histories [gabby_s_histories]

- Journal [journal]

- Journal Index [journal_index]

- Model Build [model_build]

- Modeling Review Page [modeling_review_page]

- Newsletter Issue [newsletter_issue]

- Basic page [page]

- PDF [pdf]

- Reunion Event [reunion_event]

- Newsletter Issue [simplenews_issue]

- Skyhawk Association Journal Index [skyhawk_association_journal_inde]

- Song [song]

- State Abbreviations [state_abbreviations]

Node fields by bundle (92)
- 155242_155289 | body | text_with_summary | Body

- 155242_155289 | feeds_item | feeds_item | Feeds item

- 155242_155289 | field_buno_image | image | Buno Image

- article_board | body | text_with_summary | Body

- article_journal_private | body | text_with_summary | Body

- article_journal_public | body | text_with_summary | Body

- article_modeling | body | text_with_summary | Body

- article_readyroom | body | text_with_summary | Body

- article_unit | body | text_with_summary | Body

- article | body | text_with_summary | Body

- attendee_memory | field_attendee_name | string | Your Name

- attendee_memory | field_memory_photo | image | Photo

- attendee_memory | field_memory_story | text_long | Memory

- book | body | text_with_summary | Body

- buno_batch | field_batch_end | integer | field_batch_end

- buno_batch | field_batch_start | integer | field_batch_start

- buno_batch | field_batch_variant | string | field_batch_variant

- bureau_numbers | body | text_with_summary | Body

- bureau_numbers | field_bureau_number | list_integer | Bureau Number

- dir_listing | body | text_with_summary | Body

- dir_listing | field_directory_uri | string | Directory URI

- gabby_s_histories | body | text_with_summary | Body

- gabby_s_histories | feeds_item | feeds_item | Feeds item

- gabby_s_histories | field_buno | string | BUNO

- gabby_s_histories | field_count | serial | Count

- gabby_s_histories | field_custodian | string | Custodian

- gabby_s_histories | field_date | datetime | Date

- gabby_s_histories | field_description | string | Description

- gabby_s_histories | field_location | string | Location

- gabby_s_histories | field_manufacturer_serial_number | integer | Manufacturer Serial Number

- gabby_s_histories | field_model | string | Model

- gabby_s_histories | field_notes | string | Notes

- gabby_s_histories | field_record | integer | Record

- journal_index | field_journal_index | list_string | Journal Index

- journal | body | text_with_summary | Body

- journal | field_journal_issue | integer | Issue

- journal | field_journal_is_print | boolean | Print-Friendly Version

- journal | field_journal_label | string | Season Label

- journal | field_journal_thumbnail | image | Cover Thumbnail

- journal | field_journal_volume | integer | Volume

- journal | field_journal_year | integer | Year

- journal | field_pdf_print | file | Spreads PDF

- journal | field_pdf | file | PDF

- modeling_review_page | body | text_with_summary | Review Content

- model_build | body | text_with_summary | Description / Build Notes

- model_build | field_aircraft_variant | string | Aircraft Variant

- model_build | field_bureau_number | list_integer | BuNo / Serial Number

- model_build | field_carrier | string | Carrier

- model_build | field_kit_manufacturer | string | Kit Manufacturer

- model_build | field_model_builder | string | Builder

- model_build | field_model_event_year | string | Event / Year

- model_build | field_model_images | image | Model Photographs

- model_build | field_model_scale | string | Scale

- model_build | field_squadron_operator | string | Squadron / Operator

- newsletter_issue | field_issue_date | datetime | Issue Date

- newsletter_issue | field_issue_pdf | file | Newsletter PDF

- page | body | text_with_summary | Body

- pdf | body | text_with_summary | Body

- pdf | field_journal_index | list_string | Journal Index

- pdf | field_journal_pdf | file | Journal PDF

- pdf | field_pdf_thumbnail | entity_reference | PDF Thumbnail

- pdf | layout_builder__layout | layout_section | Layout

- reunion_event | body | text_with_summary | Body

- reunion_event | field_event_date | datetime | Event Date

- reunion_event | field_event_location | string | Location

- reunion_event | field_hotel_link | link | Hotel Booking Link

- reunion_event | field_lost_comm | text_long | Lost Comm List

- reunion_event | field_manage_token | string | Management Token

- reunion_event | field_organizer_email | email | Organizer Email

- reunion_event | field_registration_link | link | Registration Link

- reunion_event | field_reunion_newsletter | file | Newsletter PDF

- reunion_event | field_taps | text_long | Taps

- reunion_event | field_verify_expiry | integer | Verification Expiry

- reunion_event | field_verify_token | string | Verification Token

- simplenews_issue | body | text_with_summary | Body

- simplenews_issue | simplenews_issue | simplenews_issue | Newsletter

- skyhawk_association_journal_inde | body | text_with_summary | Body

- skyhawk_association_journal_inde | field_article | string | Article

- skyhawk_association_journal_inde | field_author_last_name | string | Author Last Name

- skyhawk_association_journal_inde | field_category | list_string | Category

- skyhawk_association_journal_inde | field_first_name | string | First Name

- skyhawk_association_journal_inde | field_issue | list_string | Issue

- skyhawk_association_journal_inde | field_journal_number | list_float | Journal Number

- skyhawk_association_journal_inde | field_page | integer | Page

- skyhawk_association_journal_inde | field_pdf_access | link | PDF Access

- skyhawk_association_journal_inde | field_record | integer | Record

- skyhawk_association_journal_inde | field_year | list_integer | Year

- song | body | text_with_summary | Lyrics

- song | field_song_audio | entity_reference | Audio

- song | field_song_byline | string | Byline

- state_abbreviations | body | text_with_summary | Body

- state_abbreviations | field_two_letter_state_id_s | list_string | Two Letter State ID's

Taxonomy vocabularies (1)
- Skyhawk Units [skyhawk_units]

Enabled Views and exposed paths (30)
- BuNo Search [buno_search] | /buno-search

- Bureau Number 159778-159790 [bureau_number_159778_159790] | /bureau-number-159778-159790

- Contact messages [contact_messages] | /admin/structure/contact/messages

- Content [content] | /admin/content/node, /admin/content/node/edit

- Drupal 10 Gabby's Histories [drupal_10_gabby_s_histories] | /gabby-s-histories, /gabby-s-histories/rest

- Duplicate of People [duplicate_of_people] | /admin/people/list

- Files [files] | /admin/content/files, /admin/content/files/usage/%

- Gabby's Histories [gabby_s_histories] | /gabby-s-histories, /gabby-s-histories/rest

- Glossary [glossary] | /site-glossary

- Journal Grid [journal_grid] | /journals

- Mailing Lists [mailing_lists] | /mailing-lists

- Media library [media_library] | /admin/content/media-grid, /admin/content/media-widget, /admin/content/media-widget-table

- Media [media] | /admin/content/media

- Modeling Builds [modeling_builds_review] | /modeling/builds

- Moderated content [moderated_content] | /admin/content/moderated

- Newsletter issues [simplenews_newsletters] | /admin/content/simplenews

- PDF Image Entity [pdf_image_entity] | /admin/media-pdf-thumbnail/settings/list

- People [user_admin_people] | /admin/people/list

- Public Skyhawk Journal Index [public_skyhawk_journal_index] | /download/views, /skyhawk-public-journal-index, /skyhawk-public-journal-index-page2

- Redirect [redirect] | /admin/config/search/redirect

- Reunion Index [reunion_index] | /reunion

- SA Journal Grid [sa_journal_grid] | /sa-journal

- SDO Directory Review [sdo_directory_review] | /admin/people/sdo-directory-review

- SDO User Email Reference [sdo_user_email_reference]

- Skyhawk Journal Index [skyhawk_journal_index] | /skyhawk-journal-index

- Skyhawk Songs [skyhawk_songs] | /skyhawk-songs

- Skyhawk Videos [skyhawk_videos]

- Subscribers [simplenews_subscribers] | /admin/people/simplenews

- Watchdog [watchdog] | /admin/reports/dblog

- Webform submissions [webform_submissions]

Image styles (12)
- full960 [full960]

- Journal Cover (480px no watermark) [journal_cover]

- Journal Thumb (160px no watermark) [journal_thumb]

- Media Library thumbnail (220×220) [media_library]

- onehalf480 [onehalf480]

- onethird320 [onethird320]

- skyhawk_gallery_large [skyhawk_gallery_large]

- skyhawk_gallery_thumb [skyhawk_gallery_thumb]

- thumbnail192 [thumbnail192]

- thumbnail [thumbnail]

- twothirds640 [twothirds640]

- Watermark [watermark]

### Storage and Configuration

- Public files: sites/default/files

- Private files: /home/darwus/drupalbeta/web/private

- Temporary files: /tmp

- Configuration sync: sites/default/files/config_Ubo9gqxEHpoMEZNKbhJkVBUc9sN2NnzSV17M10F5hE7w77uws5OFNHtqnAAjUCO9dChbQn6-2A/sync

- Maintenance/debug reports: web/downloads/chatgpt-debug*.txt. These are operational artifacts, not architecture.

### Composer and Reconstruction

- composer.json: present.

- composer.lock: present.

- Composer-managed code and the lock file define reconstructable Drupal/core/contrib dependencies.

- Do not store rapidly aging latest-version or update-availability lists here. Generate them with Composer when maintenance begins.

- Do not patch Drupal core or contributed projects for permanent Skyhawk customization.

### Backup Architecture

- A2 maintenance database-backup directory: /home/darwus/skyhawk_backups - present.

- Before destructive or material database work, create a full A2 database backup, download it to the local machine being used, compare SHA-256 hashes, and require an exact match before mutation.

- After successful local SHA verification, temporary/superseded A2 database backups are removed; the verified local copy is the rollback copy for that maintenance operation.

- Normal database/files backups remain separate from future Git version control.

### Journal Index Architecture

- Authoritative live Journal article-index bundle: skyhawk_association_journal_inde; verified node count: 534.

- The nominal journal_index content type has 0 nodes and is not the live article-index owner.

- The Public Skyhawk Journal Index and Skyhawk Journal Index Views use skyhawk_association_journal_inde.

- Historical Raven source data is retained at /home/darwus/drupalbeta/journal_index_work/raven_journal_index_534.csv. The former standalone raw SQL journal_index table remains retired.

- Verified Raven-derived indexed boundaries are record 1, Summer 2004, through record 534, Winter 2019.

- The live article-index records already provide Article, Author Last Name, First Name, Category, Issue, Year, Journal Number, Page, PDF Access, and Record fields.

- For the indexed historical period, existing Drupal article metadata is the baseline. Processing a Journal PDF must not rediscover or overwrite that metadata unless a reviewed correction is explicitly accepted.

- Journals from 1995 through the second Journal of 2004 remain outside the Raven-derived indexed coverage and require separate article-metadata completion.

### Generated on Demand - Do Not Maintain as Prose

- Composer/Drupal update availability.

- Current cache state and temporary diagnostics.

- Disk usage and transient file counts.

- Current log entries, warnings, token activity, request traces, and temporary report filenames/hashes.

### Architecture Rules That Prevent Rediscovery

- Let Drupal be Drupal: prefer core, established contrib, fields, taxonomy, Views, Webform, revisions, permissions, services, configuration and themes before custom mechanisms.

- KISS governs architecture and collaboration.

- Know and replace in toto rather than layering conflicting CSS/configuration.

- Preserve completed decisions unless new evidence or explicit direction requires reopening them.

- Use LOST-D for unfinished work and NEXT; use this reference for durable technical truth.

Last live reconciliation: 2026-08-28 17:05:12 UTC.

### A2 Shell Execution Constraints

- Normal Skyhawk command-line work occurs interactively at the A2 prompt.

- On this A2 environment, do not use Bash process substitution such as < <(...) for Skyhawk work. It has repeatedly failed through /dev/fd/*.

- When a loop needs generated input, write the input to an ordinary temporary file and read that file with done < file, or use a simple compatible pipeline where shell state does not need to survive the pipeline.

- A shell incompatibility that has been proven once is settled environment knowledge. Do not reintroduce the failed mechanism unless new evidence explicitly proves the environment changed.

### Source Reconstruction

Skyhawk.org application source and exported configuration are maintained in the private Skyhawk-Association/skyhawk.org Git repository. GitHub provides off-host application architecture, change history, rollback and migration support; it does not replace database or site-file backups.

Repository structure, authentication, exclusions, update procedure and reconstruction steps are maintained in the GitHub / Source Reconstruction Reference.

### Drush Resolution

- Skyhawk.org uses project-local Drush at /home/darwus/drupalbeta/vendor/bin/drush.

- The normal interactive shell aliases drush to that project executable with Drupal root /home/darwus/drupalbeta/web.

- Automation must address the executable and Drupal root explicitly rather than depend on interactive aliases or PATH.

- The obsolete user-installed Composer-global Drush 9 installation was proven unused by normal shell startup, PATH, user cron and targeted automation locations, then removed through Composer.

### Command Resolution for Automation

- Normal interactive shell aliases are convenient for humans but must not be assumed by automation.

- PHP used for current Skyhawk automation: /opt/alt/php84/usr/bin/php.

- Composer PHAR: /home/darwus/composer/composer.phar, invoked explicitly through the proven PHP executable.

- Project Drush: /home/darwus/drupalbeta/vendor/bin/drush.

- Drupal root supplied explicitly to automated Drush: /home/darwus/drupalbeta/web.

- The obsolete Composer-global Drush 9 installation was proven isolated and removed.

- Before automating a command that previously worked interactively, determine how every material executable in the chain is resolved rather than assuming shell aliases or PATH behavior.

### Interactive Composer Guard

- The Composer guard exists only in the darwus user's interactive shell on the shared A2 server; no host-global configuration is changed.

- The canonical Composer/Git project root is /home/darwus/drupalbeta.

- composer-raw explicitly enters the canonical project root before invoking /opt/alt/php84/usr/bin/php /home/darwus/composer/composer.phar.

- The interactive composer guard intercepts update, require, remove and install; the default answer is No.

- Read-only Composer commands remain available through the guard.

- Correctness does not depend on the human's current working directory.

- AI-generated automation must independently enter and verify canonical directories and must not depend on interactive aliases, functions or PATH assumptions.

### Drupal Configuration Sync Path

- The configured config_sync_directory may be returned by Drupal as a path relative to the Drupal web root rather than as an absolute filesystem path.

- For this installation the Drupal web root is /home/darwus/drupalbeta/web.

- AI-generated filesystem checks must detect whether the returned sync path is absolute or relative. A relative value must be resolved against the proven Drupal web root before filesystem access.

- Do not assume a Drupal-reported filesystem setting is directly usable from the Git project root or the caller's current directory.

### Composer Maintenance Interface

- Canonical wrapper: /home/darwus/drupalbeta/bin/skyhawk-composer.

- Normal full update: skyhawk-composer update.

- Targeted update: skyhawk-composer update package-name [options].

- Supported lifecycle commands: check, config-status, update, require, remove, install, finish, abort, and help.

- The wrapper explicitly uses the proven PHP, Composer PHAR, project Drush, Drupal root, Git executable and canonical project root.

- finish refuses publication while Drupal configuration differs from sync.

## Reunion Multi-Photo Upload Architecture

SKYHAWK_REUNION_MULTIPHOTO_ARCHITECTURE_V1

Status: VERIFIED WORKING / ACCEPTED CURRENT STATE

- Current Webform owner: reunion_2026_photo_upload.

- Photo element type: webform_image_file.

- Configured cardinality: #multiple = 20.

- One submission may contain multiple reunion photos.

- Contributor identity/person, public credit, rights consent, and batch caption are shared across the submitted batch.

- Webform persistence was verified to retain all selected file IDs in one submission.

### Media bridge

- Implementation owner: modules/custom/skyhawk_gallery/skyhawk_gallery.module.

- Marker: SKYHAWK_REUNION_WEBFORM_MEDIA_BRIDGE_V1.

- Each submitted photo FID creates exactly one skyhawk_contributed_photo Media entity.

- The bridge is idempotent by field_media_image.target_id; an existing Media record for a FID is not duplicated.

- Each Media entity binds the image to Reunion Event, Reunion Person, public credit, caption, and rights consent.

### Acceptance evidence

- Webform submission SID 40 retained six photo FIDs: 61819 through 61824.

- FID 61819 already mapped to Media 317.

- Backfill created Media 319 through 323 for FIDs 61820 through 61824.

- Verification result: all six FIDs mapped one-to-one to exactly one Media entity.

- A fresh subsequent multi-photo submission completed successfully end to end.

### Reuse boundary

This architecture is intended as reusable Reunion infrastructure, not a 2026-only product pattern.
The current bridge still binds the active 2026 Reunion Event directly.
Before reuse for another reunion, replace that event-specific binding with resolved reunion context rather than cloning another hard-coded event ID.
Preserve the one-submission / many-FIDs / one-Media-per-FID contract.

## Current truth added at migration (2026-09-27)

- Drupal core 11.4.8; webform 6.3.1 (security updates applied 2026-09-27 through bin/skyhawk-composer).
- Contributed modules added 2026-09-27: field_group 4.0 and eva 3.1 (Entity Views Attachment), both through bin/skyhawk-composer.
- Squadron CMS: content type `squadron` (structured fields, Field Group panels using the skyhawk-global.css semantic vocabulary), vocabulary `unit_collections`, per-placement media, and View `squadron_collection` (EVA). State, test node and next steps: see LOST-D.
- Git access: organization deploy keys are disabled. A2 pushes both skyhawk.org (private) and this DACP repository with the existing `github-skyhawk` SSH identity (account geneatwell).
- Configuration: site-wide `config:import` currently fails validation on orphaned configuration from removed modules and themes. Apply structure through the entity API, `drush config:export -y`, and commit only the expected files.
- A2 shell: no `/dev/fd` (no bash process substitution); wrap pasted blocks in a subshell `( ... )`; rapid SSH connections are throttled for a few minutes.
- Evidence: AI reports go to /home/darwus/ai-reports (not web-served). The former web-served diagnostics and web/info.php were moved to ~/quarantine on 2026-09-27.
- Public raw GitHub URLs can lag a few minutes behind a push. Right after a push, verify with git (clone or ls-remote), not the raw URL.
