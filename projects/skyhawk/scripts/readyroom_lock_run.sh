#!/bin/bash
# Gene-authorized (2026-10-13): add members-only access for Ready Room pages (public allowlist kept), verify, commit.
S=$(cd "$(dirname "$0")" && pwd)
cd ~/drupalbeta || exit 1
M=web/modules/custom/skyhawk_site_fixes/skyhawk_site_fixes.module
PHP=/usr/local/bin/php84-skyhawk
T=$(mktemp -d); ln -s "$PHP" "$T/php"
[ -n "$(git status --porcelain --untracked-files=no web/modules/custom/skyhawk_site_fixes)" ] && { echo "ABORT: module has uncommitted changes"; exit 1; }
grep -q 'function skyhawk_site_fixes_node_access' "$M" && { echo "ABORT: hook_node_access already exists in module"; exit 1; }
mkdir -p ~/backups/code
B=~/backups/code/skyhawk_site_fixes.module.pre-readyroom-access-$(date -u +%Y%m%dT%H%M%SZ)
cp -p "$M" "$B" && echo "backup $(basename "$B") sha=$(sha256sum < "$B" | cut -c1-16)"
cat "$S/readyroom_access_hook.php.txt" >> "$M"
if ! "$PHP" -l "$M" >/dev/null 2>&1; then cp -p "$B" "$M"; echo "ABORT: lint failed, module restored"; exit 1; fi
echo "module lint OK"
PATH=$T:$PATH vendor/bin/drush cr
OUT=$(PATH=$T:$PATH vendor/bin/drush php:script "$S/readyroom_lock_verify.php" 2>&1); echo "$OUT"
if echo "$OUT" | grep -q 'RESULT=PASS'; then
  git add "$M" && git -c user.name="Skyhawk VPS" -c user.email="noreply@skyhawk.org" commit -q -m "skyhawk_site_fixes: Ready Room pages members-only via hook_node_access, public allowlist in state (Gene decision 2026-10-13)" && echo "commit $(git rev-parse --short HEAD)"
  if timeout 60 git push -q 2>/dev/null; then echo "push: OK"; else echo "push: FAILED"; fi
else
  echo "verification did not PASS: code left in place (site safer locked) but NOT committed; review before commit"
fi
rm -rf "$T"
