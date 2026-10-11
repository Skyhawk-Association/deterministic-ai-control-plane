<?php
// Old-alias -> Contact-form link replacement on node bodies (Gene-authorized workstream, 2026-10-11).
// Default: PREVIEW (writes nothing). Set environment ALIAS_APPLY=1 to write.
// Writing: each changed node gets a NEW REVISION (revertable in the UI); moderation state, status and format are preserved.
// Skips node 48561 (Association e-Mail IDs page) and any node whose latest revision is not its default revision.
require __DIR__ . '/alias_lib.php';
$apply = getenv('ALIAS_APPLY') === '1';
$skip = [48561];
$rx = '@(a4skyhawk[.](org|net)|skyhawk[.]org|darw[.]it)';
$etm = \Drupal::entityTypeManager();
$ns = $etm->getStorage('node');
$w = $etm->getStorage('webform')->load('contact');
$units = [];
foreach ($w->getElementDecoded('unit')['#options'] as $k => $v) { if (is_array($v)) { foreach ($v as $kk => $vv) $units[$kk] = 1; } else $units[$k] = 1; }
$db = \Drupal::database();
$nids = $db->query('SELECT DISTINCT entity_id FROM {node__body} WHERE deleted = 0 AND (body_value REGEXP :r1 OR body_summary REGEXP :r2) ORDER BY entity_id',
  [':r1' => $rx, ':r2' => $rx])->fetchCol();
echo ($apply ? 'MODE=APPLY' : 'MODE=PREVIEW (nothing written)') . ' candidates=' . count($nids) . "\n";
$T = ['changed' => 0, 'mailto' => 0, 'bare' => 0, 'skipped' => 0, 'failed' => 0, 'unmapped' => []];
foreach ($nids as $nid) {
  $nid = (int) $nid;
  $node = $ns->load($nid);
  if (!$node) { echo "FAIL $nid not loadable\n"; $T['failed']++; continue; }
  $title = $node->label();
  if (in_array($nid, $skip, TRUE)) { echo "SKIP $nid \"$title\" (handled separately)\n"; $T['skipped']++; continue; }
  $latest = $ns->getLatestRevisionId($nid);
  if ((int) $latest !== (int) $node->getRevisionId()) { echo "SKIP $nid \"$title\" (pending draft revision $latest)\n"; $T['skipped']++; continue; }
  if ($node->get('body')->count() !== 1) { echo "SKIP $nid \"$title\" (body has " . $node->get('body')->count() . " items)\n"; $T['skipped']++; continue; }
  $tok = strtoupper(preg_split('#[\s/]+#', trim($title))[0] ?? '');
  $unit = isset($units[$tok]) ? $tok : '';
  $item = $node->get('body')->first()->getValue();
  $new = alias_transform($item['value'] ?? '', $unit, $st);
  $newsum = alias_transform($item['summary'] ?? '', $unit, $st2);
  foreach (array_merge($st['unmapped'], $st2['unmapped']) as $u) $T['unmapped'][$u] = ($T['unmapped'][$u] ?? 0) + 1;
  $n = $st['mailto'] + $st['bare'] + $st2['mailto'] + $st2['bare'];
  if ($n === 0) { echo "NOCHANGE $nid \"$title\"\n"; continue; }
  $T['mailto'] += $st['mailto'] + $st2['mailto']; $T['bare'] += $st['bare'] + $st2['bare'];
  printf("NODE %d \"%s\" unit=%s mailto=%d bare=%d%s\n", $nid, $title, $unit ?: '-', $st['mailto'] + $st2['mailto'], $st['bare'] + $st2['bare'],
    $st['unmapped'] ? ' UNMAPPED=' . implode(',', array_unique($st['unmapped'])) : '');
  $off = 0;
  for ($k = 0; $k < 2 && ($p = strpos($new, '/form/contact?', $off)) !== FALSE; $k++) {
    echo '   ...' . preg_replace('/\s+/', ' ', substr($new, max(0, $p - 70), 170)) . "...\n";
    $off = $p + 15;
  }
  if (!$apply) { $T['changed']++; continue; }
  try {
    $status = $node->isPublished();
    $mod = $node->hasField('moderation_state') ? $node->get('moderation_state')->value : NULL;
    $item['value'] = $new; $item['summary'] = $newsum;
    $node->set('body', [$item]);
    $node->setNewRevision(TRUE);
    $node->setRevisionLogMessage('Replaced dead Association e-mail aliases with Contact-form links (2026-10-11).');
    $node->setRevisionCreationTime(\Drupal::time()->getRequestTime());
    $node->setRevisionUserId(1);
    if ($mod !== NULL) $node->set('moderation_state', $mod);
    $node->save();
    $chk = $ns->loadUnchanged($nid);
    $b = $chk->get('body')->first()->getValue();
    $left = preg_match_all(ALIAS_RE, ($b['value'] ?? '') . ' ' . ($b['summary'] ?? ''));
    $ok = $left === 0 && $chk->isPublished() === $status && ($b['format'] ?? '') === ($item['format'] ?? '') && $chk->getRevisionId() != $latest;
    echo '   ' . ($ok ? 'SAVED' : 'CHECK-FAILED') . " rev $latest -> " . $chk->getRevisionId() . " old_addresses_left=$left published=" . ($chk->isPublished() ? 1 : 0) . "\n";
    if ($ok) $T['changed']++; else $T['failed']++;
  }
  catch (\Throwable $e) { echo '   FAIL ' . $e->getMessage() . "\n"; $T['failed']++; }
}
$remain = (int) $db->query('SELECT COUNT(DISTINCT entity_id) FROM {node__body} WHERE deleted = 0 AND entity_id NOT IN (:s[]) AND (body_value REGEXP :r1 OR body_summary REGEXP :r2)',
  [':s[]' => $skip, ':r1' => $rx, ':r2' => $rx])->fetchField();
printf("TOTAL %s=%d mailto=%d bare=%d skipped=%d failed=%d unmapped=%s\n", $apply ? 'saved' : 'would_change', $T['changed'], $T['mailto'], $T['bare'], $T['skipped'], $T['failed'], json_encode($T['unmapped']));
echo "NODES_STILL_WITH_OLD_ADDRESSES (excluding skip list) = $remain\n";
echo $apply ? (($T['failed'] === 0 && $remain === 0) ? "RESULT=PASS\n" : "RESULT=FAIL\n") : "RESULT=PREVIEW\n";
