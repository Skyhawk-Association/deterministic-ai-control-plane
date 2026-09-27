# Termux SSH Notes (skyhawk.org)

**Canonical copy:** this file (`projects/skyhawk/TERMUX.md`, public DACP repository). Drupal node 49458 points here.

**Migrated** 2026-09-27 from Drupal node 49458 revision 67817. Sanitized for publication: 1 server address(es) and 0 email address(es) removed. Otherwise verbatim.

---

## Confirmed Gotchas

- Bash '!' history expansion mangles inline drush php:eval "..." strings containing !$variable syntax. Fix: write to a temp file and run via drush php:script instead of inline eval.

- .install files are not autoloaded outside actual install/update hook execution. A drush php:script or php:eval calling a hook_schema()-defined function must include_once the .install file explicitly first.

- JuiceSSH has failed on heredocs in this session; Termux's real bash shell has not shown the same failure — prefer Termux for any heredoc-heavy work.

## Pixel / A2 Working Method

- Normal Skyhawk command-line work assumes the user is already at the interactive A2 prompt.

- Canonical Pixel Termux connection: ssh -p 22 darwus@[server address removed; use the A2 alias].

- Do not invent or assume an SSH alias.

- Do not use non-interactive Pixel-to-A2 SSH to perform ordinary Drupal/Drush work. Connect interactively to A2 first, then run Drupal/Drush commands there.

- Do not exit the A2 session during ordinary work.

- Sole routine exception: when a generated backup must be downloaded to the Pixel, finish the A2 preparation, intentionally exit to the Pixel prompt, download with scp -P 22, compare A2 and Pixel SHA-256 values, and reconnect interactively to A2 after a successful match.

- Executable blocks must actually stop after a failed prerequisite. Never emit a success result after a failed gate.
