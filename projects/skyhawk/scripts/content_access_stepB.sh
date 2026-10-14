#!/bin/bash
# Step B (Gene decision 2026-10-13): configure content_access for Ready Room, rebuild node access, verify.
# Rollback if needed: drush pmu content_access (core then restores the default open grant) or restore
# ~/backups/manual/skyhawk-pre-content-access-*.sql.gz.
S=$(cd "$(dirname "$0")" && pwd)
cd ~/drupalbeta || exit 1
T=$(mktemp -d); ln -s /usr/local/bin/php84-skyhawk "$T/php"; export PATH=$T:$PATH
D=vendor/bin/drush
OUT=$($D php:script "$S/content_access_configure.php" 2>&1); echo "$OUT"
echo "$OUT" | grep -q CONFIG_DONE || { echo "ABORT: configuration did not complete; no rebuild run"; rm -rf "$T"; exit 1; }
echo "== rebuilding node access (all nodes) =="
START=$(date +%s)
php -d memory_limit=2048M $D php:eval 'node_access_rebuild(FALSE); echo "needs_rebuild_after=" . (node_access_needs_rebuild() ? "yes" : "no") . PHP_EOL;' 2>&1 | tail -3
echo "rebuild seconds: $(( $(date +%s) - START ))"
$D cr >/dev/null 2>&1
echo "== verification =="
$D php:script "$S/readyroom_ca_verify.php" 2>&1
rm -rf "$T"
