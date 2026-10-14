<?php
// Sets the Ready Room public allowlist (Gene decision 2026-10-13) and verifies access for anonymous
// visitors (live HTTP) and for a member account (Drupal access API). Prints ids/titles/flags only.
$public = [473, 76, 78, 80, 693, 79, 82];   // Brazil Skyhawks, Al Carpenter, Hotrod, Marine Flight School Primer, Story of the Skyhawk, Loss of Verdin, Hal Vincent
\Drupal::state()->set('skyhawk_readyroom_public_nids', $public);
\Drupal\Core\Cache\Cache::invalidateTags(['skyhawk_readyroom_public', 'node_list']);
echo 'hook present: ' . (function_exists('skyhawk_site_fixes_node_access') ? 'yes' : 'NO') . "\n";
echo 'public allowlist: ' . implode(',', \Drupal::state()->get('skyhawk_readyroom_public_nids')) . "\n";
$ns = \Drupal::entityTypeManager()->getStorage('node');
$nids = \Drupal::entityQuery('node')->accessCheck(FALSE)->condition('type', 'article_readyroom')->execute();
// a member account for the logged-in check
$mids = \Drupal::entityQuery('user')->accessCheck(FALSE)->condition('status', 1)->condition('roles', 'authorized_user')->range(0, 1)->execute();
$member = $mids ? \Drupal\user\Entity\User::load(reset($mids)) : NULL;
$anon = \Drupal\user\Entity\User::getAnonymousUser();
$http = \Drupal::httpClient();
$fail = 0;
foreach ($ns->loadMultiple($nids) as $n) {
  $want_public = in_array((int) $n->id(), $public, TRUE);
  $api_anon = $n->access('view', $anon);
  $api_mem = $member ? $n->access('view', $member) : NULL;
  $url = 'https://skyhawk.org' . \Drupal::service('path_alias.manager')->getAliasByPath('/node/' . $n->id());
  $code = 0;
  if ($n->isPublished()) {
    try { $code = $http->get($url, ['http_errors' => FALSE, 'allow_redirects' => FALSE, 'timeout' => 30])->getStatusCode(); } catch (\Throwable $e) { $code = -1; }
  }
  $ok = !$n->isPublished() || ($want_public ? ($code === 200 && $api_anon) : ($code !== 200 && !$api_anon));
  if ($member && $n->isPublished() && !$api_mem) $ok = FALSE;
  if (!$ok) $fail++;
  printf("%-4s nid=%-6d %-7s published=%d anon_http=%d anon_api=%s member_api=%s \"%s\"\n", $ok ? 'OK' : 'BAD', $n->id(), $want_public ? 'PUBLIC' : 'LOCKED',
    $n->isPublished() ? 1 : 0, $code, $api_anon ? 'allow' : 'deny', $api_mem === NULL ? 'n/a' : ($api_mem ? 'allow' : 'deny'), mb_substr($n->label(), 0, 50));
}
echo 'member test account available: ' . ($member ? 'yes' : 'NO (member check skipped)') . "\n";
echo $fail ? "RESULT=FAIL ($fail)\n" : "RESULT=PASS\n";
