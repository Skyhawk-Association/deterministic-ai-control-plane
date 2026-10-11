<?php
// Retire node 48561 "Association e-Mail IDs" (Gene decision 2026-10-11): unpublish as a new revision,
// redirect its public paths to /form/contact (if the redirect module is enabled), report inbound links.
$nid = 48561;
$ns = \Drupal::entityTypeManager()->getStorage('node');
$node = $ns->load($nid);
if (!$node) { echo "ABORT: node $nid not found\n"; return; }
echo "title=\"" . $node->label() . "\" published_before=" . ($node->isPublished() ? 1 : 0) . "\n";
$alias = \Drupal::service('path_alias.manager')->getAliasByPath("/node/$nid");
echo "alias=$alias\n";
$db = \Drupal::database();
// inbound links
$pat = ["%node/$nid\"%", "%node/$nid'%", "%node/$nid?%", "%node/$nid#%"];
if ($alias !== "/node/$nid") { $pat[] = '%' . $db->escapeLike($alias) . '"%'; $pat[] = '%' . $db->escapeLike($alias) . "'%"; }
$in = [];
foreach ($pat as $p) foreach ($db->query('SELECT entity_id FROM {node__body} WHERE deleted = 0 AND entity_id <> :n AND body_value LIKE :p', [':n' => $nid, ':p' => $p])->fetchCol() as $e) $in[$e] = 1;
echo 'inbound_body_links_from_nodes=' . (count($in) ? implode(',', array_keys($in)) : 'none') . "\n";
if ($db->schema()->tableExists('menu_link_content_data')) {
  $ml = $db->query("SELECT id, title, menu_name, enabled FROM {menu_link_content_data} WHERE link__uri IN (:u[])",
    [':u[]' => ["entity:node/$nid", "internal:/node/$nid", "internal:$alias"]])->fetchAll();
  foreach ($ml as $m) echo "menu_link id={$m->id} menu={$m->menu_name} enabled={$m->enabled} title=\"{$m->title}\"\n";
  if (!$ml) echo "menu_links=none\n";
}
// unpublish
if ($node->isPublished()) {
  if ($node->hasField('moderation_state') && $node->get('moderation_state')->value) { echo "ABORT: content moderation in use; not guessing a state\n"; return; }
  $node->setUnpublished();
  $node->setNewRevision(TRUE);
  $node->setRevisionLogMessage('Retired: superseded by the Contact form category routing (2026-10-11).');
  $node->setRevisionCreationTime(\Drupal::time()->getRequestTime());
  $node->setRevisionUserId(1);
  $node->save();
}
$chk = $ns->loadUnchanged($nid);
echo 'published_after=' . ($chk->isPublished() ? 1 : 0) . ' revision=' . $chk->getRevisionId() . "\n";
// redirects
if (\Drupal::moduleHandler()->moduleExists('redirect')) {
  $rs = \Drupal::entityTypeManager()->getStorage('redirect');
  $srcs = array_unique(array_filter([ltrim($alias, '/'), "node/$nid"]));
  foreach ($srcs as $s) {
    $have = $rs->loadByProperties(['redirect_source.path' => $s]);
    if ($have) { $r = reset($have); echo "redirect exists $s -> " . $r->getRedirectUrl()->toString() . "\n"; continue; }
    $r = $rs->create();
    $r->setSource($s);
    $r->setRedirect('/form/contact');
    $r->setStatusCode(301);
    $r->setLanguage('und');
    $r->save();
    echo "redirect created $s -> /form/contact (301) id=" . $r->id() . "\n";
  }
}
else echo "redirect module not enabled; no redirect created\n";
echo ((!$chk->isPublished()) ? "RESULT=PASS" : "RESULT=FAIL") . "\n";
echo "PUBLIC_ALIAS=$alias\n";
