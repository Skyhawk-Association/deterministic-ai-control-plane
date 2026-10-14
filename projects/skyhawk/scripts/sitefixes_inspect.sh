#!/bin/bash
# READ-ONLY (2026-10-13): show the skyhawk_site_fixes mail code that still has "TEST MODE: send only to UID 1",
# and inventory the backup clutter inside the module tree. E-mail addresses are masked.
M=~/drupalbeta/web/modules/custom/skyhawk_site_fixes
mask() { sed -E 's/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+/[addr]/g'; }
echo "== module files =="
find "$M" -maxdepth 1 -type f -printf '%f %s bytes\n' | sort
echo "== functions in skyhawk_site_fixes.module =="
grep -n -E '^function |hook_|mail\(|->mail\(|plugin.manager.mail' "$M/skyhawk_site_fixes.module" | mask
echo "== skyhawk_site_fixes.module lines 40-160 =="
sed -n '40,160p' "$M/skyhawk_site_fixes.module" | nl -ba -v40 | mask
echo "== every reference to UID 1 / user load 1 / TEST MODE in the module tree (excluding backups) =="
grep -rn -E 'TEST MODE|User::load\(1\)|load\(1\)|uid.?=.?1\b|adminscoot' "$M" --include='*.php' --include='*.module' --include='*.inc' | grep -v '/backups/' | mask
echo "== backup clutter inside the module tree =="
du -sh "$M/backups" 2>/dev/null; find "$M/backups" -maxdepth 1 -mindepth 1 -printf '  %f\n' 2>/dev/null | sort
find "$M" -name '*.bak*' -printf '  %P %s bytes\n'
echo "== is drupalbeta under git, and are these tracked? =="
cd ~/drupalbeta && if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "git repo: yes, branch $(git rev-parse --abbrev-ref HEAD)"
  echo "tracked files under module backups/: $(git ls-files web/modules/custom/skyhawk_site_fixes/backups | wc -l)"
  echo "tracked .bak files: $(git ls-files 'web/modules/custom/skyhawk_site_fixes/*.bak*' | wc -l)"
  echo "uncommitted changes in module: $(git status --porcelain web/modules/custom/skyhawk_site_fixes | wc -l)"
else echo "git repo: no"; fi
echo "INSPECT ONLY - nothing written"
