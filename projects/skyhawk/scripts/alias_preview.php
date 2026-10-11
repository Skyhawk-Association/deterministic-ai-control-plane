<?php
// Read-only preview of old-alias -> Contact-form link replacement (2026-10-11). Writes nothing.
require __DIR__ . '/alias_lib.php';
$skip = [48561];
$etm = \Drupal::entityTypeManager();
$w = $etm->getStorage('webform')->load('contact');
$units = [];
foreach ($w->getElementDecoded('unit')['#options'] as $k => $v) { if (is_array($v)) { foreach ($v as $kk => $vv) $units[$kk] = 1; } else $units[$k] = 1; }
$db = \Drupal::database();
$rx = '@(a4skyhawk[.](org|net)|skyhawk[.]org|darw[.]it)';
$rows = $db->query("SELECT entity_id, body_value, body_summary, body_format FROM {node__body} WHERE deleted = 0 AND (body_value REGEXP :r1 OR body_summary REGEXP :r2) ORDER BY entity_id",
  [':r1' => $rx, ':r2' => $rx])->fetchAll();
$T = ['nodes' => 0, 'mailto' => 0, 'bare' => 0, 'residual' => 0, 'unmapped' => []];
$formats = [];
foreach ($rows as $r) {
  $nid = (int) $r->entity_id;
  $node = $etm->getStorage('node')->load($nid);
  $title = $node ? $node->label() : '?';
  if (in_array($nid, $skip, TRUE)) { echo "SKIP $nid \"$title\" (Association e-Mail IDs page, handled separately)\n"; continue; }
  $tok = strtoupper(preg_split('#[\s/]+#', trim($title))[0] ?? '');
  $unit = isset($units[$tok]) ? $tok : '';
  $new = alias_transform($r->body_value ?? '', $unit, $st);
  preg_match_all(ALIAS_RE, strip_tags($new) . ' ' . $new, $res);
  $resid = count(array_unique(array_map('strtolower', $res[0])));
  $sumhits = preg_match_all(ALIAS_RE, $r->body_summary ?? '');
  $T['nodes']++; $T['mailto'] += $st['mailto']; $T['bare'] += $st['bare']; $T['residual'] += $resid;
  foreach ($st['unmapped'] as $u) $T['unmapped'][$u] = ($T['unmapped'][$u] ?? 0) + 1;
  $formats[$r->body_format] = ($formats[$r->body_format] ?? 0) + 1;
  printf("NODE %d \"%s\" unit=%s format=%s mailto=%d bare=%d residual_distinct=%d summary_hits=%d%s\n", $nid, $title, $unit ?: '-', $r->body_format,
    $st['mailto'], $st['bare'], $resid, $sumhits, $st['unmapped'] ? ' UNMAPPED=' . implode(',', array_unique($st['unmapped'])) : '');
  $p = strpos($new, '/form/contact?');
  if ($p !== FALSE) echo "   after: ..." . preg_replace('/\s+/', ' ', substr($new, max(0, $p - 90), 200)) . "...\n";
}
echo "== other node text fields with old addresses (not handled by this pass) ==\n";
$colsql = 'SELECT TABLE_NAME AS t, COLUMN_NAME AS c FROM information_schema.COLUMNS'
  . ' WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME LIKE :tl AND TABLE_NAME <> :tb'
  . ' AND COLUMN_NAME LIKE :cl AND DATA_TYPE IN (:t1, :t2, :t3, :t4)';
$cols = $db->query($colsql, [':tl' => 'node\\_\\_%', ':tb' => 'node__body', ':cl' => '%\\_value',
  ':t1' => 'text', ':t2' => 'mediumtext', ':t3' => 'longtext', ':t4' => 'varchar'])->fetchAll();
$other = 0;
foreach ($cols as $c) {
  if (!preg_match('/^[a-z0-9_]+$/', $c->t . $c->c)) continue;
  $n = $db->query('SELECT COUNT(*) FROM ' . $c->t . ' WHERE ' . $c->c . ' REGEXP :r', [':r' => $rx])->fetchField();
  if ($n) { echo "  {$c->t}.{$c->c}: $n rows\n"; $other += $n; }
}
echo "  total other rows: $other\n";
printf("TOTAL nodes=%d mailto_links=%d bare_addresses=%d residual_after=%d formats=%s\n", $T['nodes'], $T['mailto'], $T['bare'], $T['residual'], json_encode($formats));
echo "UNMAPPED: " . json_encode($T['unmapped']) . "\n";
echo "PREVIEW ONLY - nothing written\n";
