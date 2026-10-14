<?php
// Step B part 1 (Gene decision 2026-10-13), using content_access's own API (read from installed 2.1.0 source):
//  - article_readyroom: view limited to member/leadership roles; per-node control on.
//  - 7 public Ready Room stories: per-node view for every role incl. anonymous.
$type = 'article_readyroom';
$public = [473, 76, 78, 80, 693, 79, 82];
$member_roles = ['admin', 'co', 'xo', 'board', 'sectreas', 'journal', 'modeling', 'sdo_coordinator', 'sdo', 'authorized_user', 'blade'];
$all_roles = array_keys(\Drupal\user\Entity\Role::loadMultiple());
$missing = array_diff($member_roles, $all_roles);
if ($missing) { echo 'ABORT: roles not found: ' . implode(',', $missing) . "\n"; return; }
$s = content_access_get_settings('all', $type);
echo 'type settings before: ' . json_encode(['view' => $s['view'] ?? NULL, 'per_node' => $s['per_node'] ?? NULL]) . "\n";
$s['view'] = $member_roles;
$s['per_node'] = TRUE;
content_access_set_settings($s, $type);
$a = content_access_get_settings('all', $type);
echo 'type settings after:  ' . json_encode(['view' => $a['view'], 'per_node' => $a['per_node']]) . "\n";
$ns = \Drupal::entityTypeManager()->getStorage('node');
foreach ($public as $nid) {
  $n = $ns->load($nid);
  if (!$n || $n->bundle() !== $type) { echo "ABORT: nid $nid is not a $type node\n"; return; }
  $pn = content_access_get_per_node_settings($n);
  $pn['view'] = $all_roles;
  content_access_save_per_node_settings($n, $pn);
  $chk = content_access_get_per_node_settings($n);
  printf("per-node public nid=%d view_includes_anonymous=%s \"%s\"\n", $nid, in_array('anonymous', $chk['view'] ?? [], TRUE) ? 'yes' : 'NO', mb_substr($n->label(), 0, 50));
}
echo "CONFIG_DONE\n";
