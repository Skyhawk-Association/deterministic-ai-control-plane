<?php
// Create the members-only Ready Room page "Who Handles What" (Gene decision 2026-10-13).
// Names come from a private file (~/whw_names.json) so no personal names live in public Git.
// The page is an article_readyroom node: locked to members by content_access by default (no per-node exception).
$f = getenv('HOME') . '/whw_names.json';
$n = json_decode((string) @file_get_contents($f), TRUE);
$need = ['terry', 'mark', 'joe', 'editor', 'dave', 'gp', 'stender', 'linder', 'gene'];
if (!is_array($n) || array_diff($need, array_keys($n))) { echo "ABORT: names file missing or incomplete\n"; return; }
$h = fn($k) => htmlspecialchars($n[$k], ENT_QUOTES);
$title = 'Who Handles What';
$dupe = \Drupal::entityQuery('node')->accessCheck(FALSE)->condition('type', 'article_readyroom')->condition('title', $title)->execute();
if ($dupe) { echo 'ABORT: page already exists nid=' . implode(',', $dupe) . "\n"; return; }
$link = fn($cat, $label) => '<a href="/form/contact?category=' . $cat . '">' . $label . '</a>';
$rows = [
  [$link('membership_login', 'Membership / Login'), $h('terry')],
  [$link('membership_paypal', 'Membership / PayPal'), $h('terry') . ', ' . $h('mark')],
  [$link('patch_orders', 'Patch Orders'), $h('terry')],
  [$link('modeling', 'Modeling'), $h('joe')],
  [$link('journal', 'Journal'), $h('editor')],
  [$link('research', 'Research') . ', ' . $link('history', 'Historical Information') . ', ' . $link('correction', 'Correction (dates, names, facts)') . ', ' . $link('story', 'Story / Memory'), $h('dave') . ', ' . $h('gp')],
  [$link('former_member', 'Former Squadron Member'), $h('stender') . ', ' . $h('linder')],
  [$link('photos', 'Photos') . ', ' . $link('website', 'Website / Contributions') . ', ' . $link('other', 'Other'), $h('gene') . ' (Webmaster)'],
];
$body = '<p>Messages sent through the <a href="/form/contact">Contact form</a> go to the people below, based on the category the sender chooses. '
  . 'Every message is also copied to the Association mailbox. Click a category to open the form with it already selected.</p>'
  . '<table><thead><tr><th>Contact form category</th><th>Handled by</th></tr></thead><tbody>';
foreach ($rows as [$a, $b]) $body .= "<tr><td>$a</td><td>$b</td></tr>";
$body .= '</tbody></table>'
  . '<h3>Email groups</h3><ul>'
  . '<li><strong>Skyhawk Board</strong> (skyhawk-bod@googlegroups.com): the Board of Directors. Members of the group can write to the whole Board at this one address.</li>'
  . '<li><strong>A4 Join</strong> (a4join@googlegroups.com): membership inquiries, handled by ' . $h('terry') . ', ' . $h('mark') . ' and ' . $h('gene') . '.</li>'
  . '</ul><p>Personal e-mail addresses are deliberately not listed. The Contact form and the group addresses deliver to the right people.</p>'
  . '<p><em>Last updated October 13, 2026. To change who handles a category, contact the Webmaster through the ' . $link('website', 'Contact form') . '.</em></p>';
$node = \Drupal\node\Entity\Node::create([
  'type' => 'article_readyroom', 'title' => $title, 'uid' => 1, 'status' => 1,
  'body' => ['value' => $body, 'format' => 'full_html'],
  'path' => ['alias' => '/article-readyroom/who-handles-what', 'pathauto' => 0],
]);
$node->save();
$nid = (int) $node->id();
$alias = \Drupal::service('path_alias.manager')->getAliasByPath("/node/$nid");
echo "created nid=$nid alias=$alias\n";
$per = content_access_get_per_node_settings($node);
echo 'per-node public exception: ' . (empty($per) ? 'none (locked by type default)' : json_encode(array_keys($per))) . "\n";
\Drupal::service('cache_tags.invalidator')->invalidateTags(['node:' . $nid]);
$anon = \Drupal\user\Entity\User::getAnonymousUser();
$mids = \Drupal::entityQuery('user')->accessCheck(FALSE)->condition('status', 1)->condition('roles', 'authorized_user')->condition('uid', 1, '>')->range(0, 1)->execute();
$mem = \Drupal\user\Entity\User::load(reset($mids));
$code = \Drupal::httpClient()->get('https://skyhawk.org' . $alias, ['http_errors' => FALSE, 'allow_redirects' => FALSE, 'timeout' => 30])->getStatusCode();
$ok = !$node->access('view', $anon) && $node->access('view', $mem) && $code === 403;
printf("anon_api=%s member_api=%s anon_http=%d\n", $node->access('view', $anon) ? 'allow' : 'deny', $node->access('view', $mem) ? 'allow' : 'deny', $code);
echo 'contact links in page: ' . substr_count($body, '/form/contact') . "\n";
echo $ok ? "RESULT=PASS\n" : "RESULT=FAIL\n";
