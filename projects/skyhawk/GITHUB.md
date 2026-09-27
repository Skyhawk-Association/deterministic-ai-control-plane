# GitHub / Source Reconstruction Reference (skyhawk.org)

**Canonical copy:** this file (`projects/skyhawk/GITHUB.md`, public DACP repository). Drupal node 49463 points here.

**Migrated** 2026-09-27 from Drupal node 49463 revision 67878. Sanitized for publication: 0 server address(es) and 0 email address(es) removed. Otherwise verbatim.

---

GitHub / Source Reconstruction Reference

Purpose: Define the off-host, version-controlled representation of Skyhawk.org application architecture. GitHub supports reconstruction, rollback, migration and disaster recovery. It does not replace normal database/files backups.

## Current State

- GitHub organization: Skyhawk-Association.

- Canonical private repository: Skyhawk-Association/skyhawk.org.

- Organization owner/admin identity used for repository authentication: geneatwell.

- A2 repository root: /home/darwus/drupalbeta.

- Local branch: main.

- Origin: git@github-skyhawk:Skyhawk-Association/skyhawk.org.git.

- A2 dedicated SSH private key: ~/.ssh/skyhawk_github_ed25519.

- A2 SSH alias: github-skyhawk, targeting GitHub with the dedicated A2 key.

- The corresponding public key is authorized on the existing GitHub owner account; the private key remains only on A2.

- GitHub SSH authentication and private-repository access have been successfully proven from A2.

- Current first-import staging contains 3292 files, including 737 exported configuration files.

## What Belongs in Git

- composer.json and composer.lock.

- Current Skyhawk custom modules, CSS, JavaScript and other maintained site-specific application assets.

- Drupal exported configuration from the current sync directory: sites/default/files/config_Ubo9gqxEHpoMEZNKbhJkVBUc9sN2NnzSV17M10F5hE7w77uws5OFNHtqnAAjUCO9dChbQn6-2A/sync.

- Drupal scaffold/application files needed for reconstruction.

- External libraries currently required by the working Drupal application when they are not otherwise reconstructed automatically by Composer.

- Small reconstruction documentation and project metadata such as .gitignore, .gitattributes, .editorconfig and appropriate Drupal recipe/scaffold material.

## What Does Not Belong in Git

- Database dumps.

- Passwords, API keys, private keys, credentials, environment secrets or live settings.php.

- Drupal public user-upload storage.

- Drupal private files.

- Temporary files, caches, logs and generated debug evidence.

- Ordinary server/database backups.

- Composer-generated vendor, Drupal core and contributed module/theme trees that are reconstructed from Composer.

- Historical preservation mirrors, completed diagnostic workspaces, obsolete patch archives and one-time maintenance debris.

- Journal preservation material or other historical assets merely because they happen to reside beneath the Drupal project tree.

## Authentication Architecture

- A2 uses a dedicated Ed25519 key specifically named for Skyhawk GitHub access.

- The key is selected through SSH alias github-skyhawk.

- The public key is registered to the existing GitHub account that owns/administers the Skyhawk Association organization.

- The repository remains private.

- Do not publish, copy into documentation, or expose the private SSH key.

## Normal Update Workflow

- Read LOST-D, Rules and this reference.

- Make and verify the actual Drupal/application change using the appropriate subject reference.

- Update durable documentation when current truth changes.

- Review git status and the proposed staged set.

- Ensure secrets, runtime files, uploads, private files, backups and unrelated preservation material are excluded.

- Stage only accepted architecture.

- Inspect staged content before commit.

- Create a concise commit describing the proven change.

- Push to the private Association repository.

- Verify the remote repository reflects the intended commit.

## Reconstruction / Migration Model

- Provision a compatible host with PHP, database and required server capabilities.

- Clone the private Skyhawk-Association/skyhawk.org repository.

- Run Composer from the project root to reconstruct Drupal core, contributed projects and PHP dependencies from composer.json and composer.lock.

- Restore environment-specific settings and secrets outside Git.

- Restore the separately maintained Drupal database backup.

- Restore separately maintained public/private site files.

- Ensure the configuration sync path is available and reconcile Drupal configuration as appropriate to the restored database/state.

- Run Drupal database updates/cache rebuild as required.

- Verify the production site, custom modules, Views, routes, libraries, uploads and critical user paths before cutover.

## Relationship to Backups

GitHub protects application architecture and change history. Database and file backups protect content and uploaded assets. Both are required for full recovery; neither substitutes for the other.

## Maintenance Principle

Keep this reference concise and current. Record durable repository architecture and reconstruction facts here. Generate transient Git status, commit hashes, update availability and diagnostics when needed rather than accumulating them as prose.

## Baseline Repository State

- The initial reconstructable Skyhawk.org application baseline has been committed and pushed successfully to the private Skyhawk-Association/skyhawk.org repository.

- Branch: main.

- Initial baseline commit: 3246c05ddc10f310e676a9310ceb96697b202dd0.

- The A2 local HEAD, upstream origin/main, and GitHub remote branch were independently verified to match after the push.

- Future application changes follow the normal inspect, stage, review, commit, push and remote-verification workflow documented on this page.

## Composer Maintenance Integration

- Composer does not update GitHub by itself. Skyhawk mutating dependency maintenance uses /home/darwus/drupalbeta/bin/skyhawk-composer.

- skyhawk-composer update performs the normal full update; package names may follow for targeted updates.

- Mutating work enters a pending state after Composer, Drupal database updates and cache rebuild.

- finish is the human acceptance/publication step.

- finish requires zero Drupal configuration drift, safety-checks staged files, validates Composer state, commits, pushes and proves local/remote parity.

### Interactive Composer Safety

- Interactive Composer mutation handling is independent of the operator's current directory.

- The canonical project root is /home/darwus/drupalbeta.

- Direct interactive mutation is intercepted and defaults to No.

- Any deliberately authorized direct Composer execution first enters the canonical project root.

- The supported structured mutating-maintenance path remains /home/darwus/drupalbeta/bin/skyhawk-composer.

- Automation must use explicit executable paths and canonical directories rather than inheriting human shell state.
