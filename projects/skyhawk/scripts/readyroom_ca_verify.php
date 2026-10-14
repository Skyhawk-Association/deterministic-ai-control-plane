<?php
// Verify the Ready Room lock (content_access): anonymous live HTTP, member access via grants, and anonymous search.
$public = [473, 76, 78, 80, 693, 79, 82];
$ns = \Drupal::entityTypeManager()->getStorage('node');
$nids = \Drupal::entityQuery('node')->accessCheck(FALSE)->condition('type', 'article_readyroom')->execute();
$mids = \Drupal::entityQuery('user')->accessCheck(FALSE)->condition('status', 1)->condition('roles', 'authorized_user')->condition('uid', 1, '>')->range(0, 1)->execute();
$member = $mids ? \Drupal\user\Entity\User::load(reset($mids)) : NULL;
$anon = \Drupal\user\Entity\User::getAnonymousUser();
$http = \Drupal::httpClient();
$fail = 0;
foreach ($ns->loadMultiple($nids) as $n) {
  $want_public = in_array((int) $n->id(), $public, TRUE);
  $api_anon = $n->access('view', $anon);
  $api_mem = $member ? $n->access('view', $member) : NULL;
  $code = 0;
  if ($n->isPublished()) {
    $url = 'https://skyhawk.org' . \Drupal::service('path_alias.manager')->getAliasByPath('/node/' . $n->id());
    try { $code = $http->get($url, ['http_errors' => FALSE, 'allow_redirects' => FALSE, 'timeout' => 30])->getStatusCode(); } catch (\Throwable $e) { $code = -1; }
  }
  $ok = !$n->isPublished() || ($want_public ? ($code === 200 && $api_anon) : ($code !== 200 && !$api_anon));
  if ($member && $n->isPublished() && !$api_mem) $ok = FALSE;
  if (!$ok) $fail++;
  printf("%-4s nid=%-6d %-7s published=%d anon_http=%d anon_api=%s member_api=%s \"%s\"\n", $ok ? 'OK' : 'BAD', $n->id(), $want_public ? 'PUBLIC' : 'LOCKED',
    $n->isPublished() ? 1 : 0, $code, $api_anon ? 'allow' : 'deny', $api_mem === NULL ? 'n/a' : ($api_mem ? 'allow' : 'deny'), mb_substr($n->label(), 0, 50));
}
echo 'member test account available: ' . ($member ? 'yes' : 'NO') . "\n";
// spot check: an ordinary public page elsewhere still visible
$c = $http->get('https://skyhawk.org/node/72', ['http_errors' => FALSE, 'allow_redirects' => TRUE, 'timeout' => 30])->getStatusCode();
echo "ordinary public page (VA-12) anon http=$c\n"; if ($c !== 200) $fail++;
// anonymous search for a locked title term
$r = $http->get('https://skyhawk.org/search/node?keys=152101', ['http_errors' => FALSE, 'allow_redirects' => TRUE, 'timeout' => 30]);
$body = (string) $r->getBody();
echo 'anon search "152101": http=' . $r->getStatusCode() . ' locked_title_shown=' . (stripos($body, 'BuNo 152101 History') !== FALSE ? 'YES' : 'no') . "\n";
if (stripos($body, 'BuNo 152101 History') !== FALSE) $fail++;
$realms = \Drupal::database()->query('SELECT realm, COUNT(*) c FROM {node_access} GROUP BY realm')->fetchAllKeyed();
echo 'node_access realms: ' . json_encode($realms) . ' needs_rebuild=' . (node_access_needs_rebuild() ? 'yes' : 'no') . "\n";
echo $fail ? "RESULT=FAIL ($fail)\n" : "RESULT=PASS\n";
