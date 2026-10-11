#!/bin/bash
# Runs retire_48561.php, clears cache, then checks the public side anonymously. Run as n790725 from the script dir.
S=$(cd "$(dirname "$0")" && pwd)
cd ~/drupalbeta || exit 1
T=$(mktemp -d); ln -s /usr/local/bin/php84-skyhawk "$T/php"
OUT=$(PATH=$T:$PATH vendor/bin/drush php:script "$S/retire_48561.php" 2>&1); echo "$OUT"
PATH=$T:$PATH vendor/bin/drush cr 2>&1
A=$(echo "$OUT" | sed -n 's/^PUBLIC_ALIAS=//p')
echo "== public check (anonymous) =="
for p in /node/48561 "$A"; do
  [ -n "$p" ] || continue
  printf '%s -> %s\n' "$p" "$(curl -s -o /dev/null --max-time 30 -w '%{http_code} %{redirect_url}' "https://skyhawk.org$p")"
done
rm -rf "$T"
