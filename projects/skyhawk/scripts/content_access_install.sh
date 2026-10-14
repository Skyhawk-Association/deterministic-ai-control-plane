#!/bin/bash
# Gene-authorized (2026-10-13): install + enable drupal/content_access (contrib) - step A of the Ready Room lock.
# No access settings are changed here; enabling alone keeps current visibility. Reports the module's API for step B.
cd ~/drupalbeta || exit 1
T=$(mktemp -d); ln -s /usr/local/bin/php84-skyhawk "$T/php"; export PATH=$T:$PATH
D="vendor/bin/drush"
dirty=$(git status --porcelain composer.json composer.lock)
[ -n "$dirty" ] && { echo "ABORT: composer files not clean:"; echo "$dirty"; git diff --stat composer.json composer.lock; exit 1; }
mkdir -p ~/backups/manual
F=~/backups/manual/skyhawk-pre-content-access-$(date -u +%Y%m%dT%H%M%SZ).sql
$D sql:dump --gzip --structure-tables-list="cache,cache_*" --result-file=$F >/dev/null 2>&1 && gzip -t $F.gz && echo "db backup $(basename $F.gz) $(stat -c %s $F.gz) bytes" || { echo "ABORT: db backup failed"; exit 1; }
composer require drupal/content_access:^2.1 --no-interaction 2>&1 | grep -E 'Installing|Locking|Nothing|Error|error|Problem'
composer show drupal/content_access 2>/dev/null | grep -E '^versions'
$D en content_access -y 2>&1 | tail -3
$D cr >/dev/null 2>&1
$D php:eval 'echo "enabled=" . (\Drupal::moduleHandler()->moduleExists("content_access") ? "yes" : "NO") . " needs_rebuild=" . (node_access_needs_rebuild() ? "yes" : "no") . " node_access_rows=" . \Drupal::database()->query("SELECT COUNT(*) FROM {node_access}")->fetchField() . PHP_EOL;'
echo "public sanity: Brazil Skyhawks anon http=$(curl -s -o /dev/null -w '%{http_code}' https://skyhawk.org/node/473) ; home http=$(curl -s -o /dev/null -w '%{http_code}' https://skyhawk.org/)"
CA=web/modules/contrib/content_access
echo "== content_access API (functions) =="; grep -n '^function ' $CA/content_access.module | cut -c1-160
echo "== src classes =="; find $CA/src -name '*.php' | sed "s#$CA/##" | sort
echo "== config schema =="; cat $CA/config/schema/*.yml 2>/dev/null | head -60
echo "== config objects now =="; $D php:eval 'foreach (\Drupal::configFactory()->listAll("content_access") as $n) echo $n, PHP_EOL;'
if [ -n "$(git status --porcelain composer.json composer.lock)" ]; then
  git add composer.json composer.lock && git -c user.name="Skyhawk VPS" -c user.email="noreply@skyhawk.org" commit -q -m "Add drupal/content_access ^2.1 (Ready Room members-only access, Gene decision 2026-10-13)" && echo "commit $(git rev-parse --short HEAD)"
  timeout 60 git push -q 2>/dev/null && echo "push: OK" || echo "push: FAILED"
fi
rm -rf "$T"
