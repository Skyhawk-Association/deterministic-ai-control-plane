<?php
// READ-ONLY (2026-10-13): are Ready Room pages' contents visible to anonymous visitors?
// For each published node under a Ready Room alias, fetch the public URL with no login and test whether a
// distinctive snippet of its own body text appears. Prints node ids, titles and flags only - no body text.
$db = \Drupal::database();
$rows = $db->query("SELECT path, alias FROM {path_alias} WHERE alias LIKE :a OR alias LIKE :b ORDER BY alias",
  [':a' => '/article-readyroom/%', ':b' => '/article-ready-room/%'])->fetchAll();
$ns = \Drupal::entityTypeManager()->getStorage('node');
$http = \Drupal::httpClient();
$base = 'https://skyhawk.org';
$exposed = $hidden = $untestable = $unpub = 0;
$types = [];
foreach ($rows as $r) {
  if (!preg_match('#^/node/(\d+)$#', $r->path, $m)) continue;
  $n = $ns->load((int) $m[1]); if (!$n) continue;
  $types[$n->bundle()] = ($types[$n->bundle()] ?? 0) + 1;
  if (!$n->isPublished()) { $unpub++; continue; }
  $txt = $n->hasField('body') ? preg_replace('/\s+/', ' ', html_entity_decode(strip_tags((string) $n->get('body')->value))) : '';
  $snip = '';
  if (preg_match_all('/[A-Za-z0-9 ]{40,}/', $txt, $mm)) { usort($mm[0], fn($x, $y) => strlen($y) - strlen($x)); $snip = trim(substr($mm[0][0], 0, 40)); }
  try { $resp = $http->get($base . $r->alias, ['http_errors' => FALSE, 'allow_redirects' => TRUE, 'timeout' => 30]); }
  catch (\Throwable $e) { printf("ERR  %-6d %s\n", $n->id(), $e->getMessage()); continue; }
  $code = $resp->getStatusCode(); $html = (string) $resp->getBody();
  $login = (bool) preg_match('/user\/login|Log in|members only|Members Only/i', $html);
  if ($snip === '') { $untestable++; $flag = 'NO-SNIPPET'; }
  elseif ($code === 200 && str_contains(preg_replace('/\s+/', ' ', html_entity_decode(strip_tags($html))), $snip)) { $exposed++; $flag = 'EXPOSED'; }
  else { $hidden++; $flag = 'hidden'; }
  printf("%-10s nid=%-6d http=%d login_prompt=%s type=%s \"%s\"\n", $flag, $n->id(), $code, $login ? 'y' : 'n', $n->bundle(), mb_substr($n->label(), 0, 60));
}
echo 'bundles under Ready Room aliases: ' . json_encode($types) . "\n";
echo "TOTAL exposed=$exposed hidden=$hidden untestable=$untestable unpublished_skipped=$unpub\n";
echo "CHECK ONLY - nothing written\n";
