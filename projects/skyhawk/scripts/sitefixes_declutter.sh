#!/bin/bash
# Gene-authorized (2026-10-13): move backup clutter out of web/modules/custom/skyhawk_site_fixes.
# Copies every *.bak*, *.backup-*, *.before-* file and the backups/ folder to ~/backups/code/<stamp>/ (paths kept),
# verifies each copy by SHA-256, then removes the originals (git rm for tracked ones), adds .gitignore rules,
# and commits in the drupalbeta repo. Push is attempted; its result is reported, not assumed.
cd ~/drupalbeta || exit 1
M=web/modules/custom/skyhawk_site_fixes
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
DEST=~/backups/code/skyhawk_site_fixes-clutter-$STAMP
[ -n "$(git status --porcelain --untracked-files=no $M)" ] && { echo "ABORT: module has uncommitted changes"; exit 1; }
mapfile -t FILES < <(find "$M" -type f \( -name '*.bak*' -o -name '*.backup-*' -o -name '*.before-*' -o -path "$M/backups/*" \) | sort)
echo "files to move: ${#FILES[@]}"
[ ${#FILES[@]} -eq 0 ] && { echo "nothing to do"; exit 0; }
bad=0
for f in "${FILES[@]}"; do
  mkdir -p "$DEST/$(dirname "$f")"; cp -p "$f" "$DEST/$f"
  [ "$(sha256sum < "$f")" = "$(sha256sum < "$DEST/$f")" ] || { echo "COPY MISMATCH $f"; bad=$((bad+1)); }
done
[ $bad -gt 0 ] && { echo "ABORT: $bad copies did not verify; originals untouched"; exit 1; }
echo "copied and verified: ${#FILES[@]} -> $DEST"
tracked=0; untracked=0
for f in "${FILES[@]}"; do
  if git ls-files --error-unmatch "$f" >/dev/null 2>&1; then git rm -q "$f" && tracked=$((tracked+1)); else rm -f "$f" && untracked=$((untracked+1)); fi
done
printf '*.bak*\n*.backup-*\n*.before-*\n/backups/\n' > "$M/.gitignore"
find "$M/backups" -depth -type d -empty -delete 2>/dev/null
git add "$M/.gitignore"
echo "removed: tracked=$tracked untracked=$untracked"
echo "left in module matching clutter patterns: $(find "$M" -type f \( -name '*.bak*' -o -name '*.backup-*' -o -name '*.before-*' \) | wc -l); backups dir exists: $([ -d "$M/backups" ] && echo yes || echo no)"
git -c user.name="Skyhawk VPS" -c user.email="noreply@skyhawk.org" commit -q -m "skyhawk_site_fixes: move backup clutter out of the module tree (copies in ~/backups/code/skyhawk_site_fixes-clutter-$STAMP); ignore backup patterns" && echo "commit $(git rev-parse --short HEAD)"
echo "module php lint: $( (command -v /usr/local/bin/php84-skyhawk >/dev/null && /usr/local/bin/php84-skyhawk -l $M/skyhawk_site_fixes.module || php -l $M/skyhawk_site_fixes.module) 2>&1 | head -1)"
if timeout 60 git push -q 2>/tmp/declutter-push.$$; then echo "push: OK"; else echo "push: FAILED ($(head -c 200 /tmp/declutter-push.$$ | tr '\n' ' ' | sed -E 's/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+/[addr]/g'))"; fi
rm -f /tmp/declutter-push.$$
echo "ahead of remote: $(git rev-list --count @{u}..HEAD 2>/dev/null || echo unknown)"
