<?php
// READ-ONLY inventory (2026-10-11): where could old "Join Us" submissions / notification e-mails be recorded?
// Prints ONLY structure, counts and dates - never names, addresses or submission values (output goes to public Git).
$etm = \Drupal::entityTypeManager();
$db = \Drupal::database();
$mask = fn($s) => preg_replace('/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+/', '[addr]', (string) $s);
echo "== webforms (all) ==\n";
foreach ($etm->getStorage('webform')->loadMultiple() as $id => $w) {
  $q = $db->query('SELECT COUNT(*) c, MIN(created) a, MAX(created) b FROM {webform_submission} WHERE webform_id = :w', [':w' => $id])->fetchObject();
  $h = [];
  foreach ($w->getHandlers() as $hid => $hd) {
    $c = $hd->getConfiguration();
    $h[] = $hid . ($c['id'] === 'email' ? '(to=' . $mask($c['settings']['to_mail'] ?? '') . ')' : '');
  }
  printf("%-32s status=%-6s subs=%d first=%s last=%s title=\"%s\" handlers=%s\n", $id, $w->get('status'), $q->c,
    $q->a ? date('Y-m-d', $q->a) : '-', $q->b ? date('Y-m-d', $q->b) : '-', $w->label(), implode(',', $h) ?: 'none');
}
echo "== join-like webform element keys (field names only) ==\n";
foreach ($etm->getStorage('webform')->loadMultiple() as $id => $w) {
  if (!preg_match('/join|member|applic|renew|signup|sign_up/i', $id . ' ' . $w->label())) continue;
  echo "$id: " . implode(', ', array_keys($w->getElementsDecodedAndFlattened())) . "\n";
}
echo "== core contact forms / stored messages ==\n";
foreach ($etm->getStorage('contact_form')->loadMultiple() as $id => $f) {
  printf("contact_form %-20s label=\"%s\" recipients=%d\n", $id, $f->label(), count($f->getRecipients()));
}
echo 'contact_message table: ' . ($db->schema()->tableExists('contact_message') ? 'yes rows=' . $db->query('SELECT COUNT(*) FROM {contact_message}')->fetchField() : 'no (messages were never stored)') . "\n";
echo "== nodes with join-like titles ==\n";
foreach ($db->query("SELECT nid, type, status, title FROM {node_field_data} WHERE title REGEXP :r ORDER BY nid", [':r' => '[Jj]oin|[Mm]embership [Aa]pplic|[Rr]enew'])->fetchAll() as $n) {
  printf("node %d type=%s published=%d \"%s\"\n", $n->nid, $n->type, $n->status, $n->title);
}
echo "== watchdog mail-type history (counts only) ==\n";
foreach ($db->query("SELECT type, COUNT(*) c, MIN(timestamp) a, MAX(timestamp) b FROM {watchdog} WHERE type IN ('mail','webform','contact') GROUP BY type")->fetchAll() as $r) {
  printf("%-8s rows=%d first=%s last=%s\n", $r->type, $r->c, date('Y-m-d', $r->a), date('Y-m-d', $r->b));
}
echo "INVENTORY ONLY - nothing written\n";
