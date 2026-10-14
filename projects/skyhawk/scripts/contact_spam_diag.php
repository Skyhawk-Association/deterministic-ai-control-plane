<?php
// READ-ONLY (2026-10-13): where does "TEST MODE" text still come from, what spam protection is available,
// and can user 1 take the Association mailbox address. Prints no personal data.
$db = \Drupal::database();
$mask = fn($s) => preg_replace('/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+/', '[addr]', (string) $s);
echo "== config objects containing 'TEST MODE' or 'adminscoot' ==\n";
foreach ($db->query("SELECT name FROM {config} WHERE data LIKE :a OR data LIKE :b ORDER BY name", [':a' => '%TEST MODE%', ':b' => '%adminscoot%'])->fetchCol() as $n) echo "  $n\n";
echo "== contact webform email handlers ==\n";
$w = \Drupal::entityTypeManager()->getStorage('webform')->load('contact');
foreach ($w->getHandlers() as $id => $h) {
  $c = $h->getConfiguration(); if (($c['id'] ?? '') !== 'email') continue;
  $b = (string) ($c['settings']['body'] ?? '');
  $line = '';
  foreach (preg_split('/\R|<br\s*\/?>|<\/p>/i', $b) as $l) if (stripos($l, 'TEST MODE') !== FALSE || stripos($l, 'adminscoot') !== FALSE) { $line = trim(strip_tags($l)); break; }
  printf("  %-24s body=%s html=%s test_line=%s\n", $id, $b === '_default' ? '_default' : strlen($b) . 'chars', !empty($c['settings']['html']) ? 'y' : 'n', $line !== '' ? '"' . $mask($line) . '"' : 'none');
}
echo "== other hooks: custom module code mentioning TEST MODE ==\n";
$root = DRUPAL_ROOT . '/modules/custom';
$it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($root, FilesystemIterator::SKIP_DOTS));
foreach ($it as $f) {
  if (!preg_match('/\.(php|module|inc|twig|yml)$/', $f->getFilename())) continue;
  foreach (file($f->getPathname()) as $i => $l) if (stripos($l, 'TEST MODE') !== FALSE || stripos($l, 'adminscoot') !== FALSE) echo '  ' . str_replace(DRUPAL_ROOT . '/', '', $f->getPathname()) . ':' . ($i + 1) . ': ' . $mask(trim($l)) . "\n";
}
echo "== spam-protection modules ==\n";
$all = \Drupal::service('extension.list.module')->getList();
foreach (['honeypot', 'antibot', 'captcha', 'recaptcha', 'recaptcha_v3', 'friendlycaptcha', 'cleantalk', 'webform_spam'] as $m) {
  printf("  %-16s in_codebase=%s enabled=%s\n", $m, isset($all[$m]) ? 'yes' : 'no', \Drupal::moduleHandler()->moduleExists($m) ? 'yes' : 'no');
}
$ws = \Drupal::config('webform.settings');
echo '  webform default antispam (honeypot setting in webform.settings): ' . json_encode($ws->get('third_party_settings') ?? []) . "\n";
echo '  contact form third_party_settings: ' . json_encode($w->getThirdPartySettings('honeypot') + $w->getThirdPartySettings('antibot') + $w->getThirdPartySettings('captcha')) . "\n";
echo "== submissions on contact form: last 14 days, gibberish-looking (no spaces in name+subject, >=12 chars) ==\n";
$ss = \Drupal::entityTypeManager()->getStorage('webform_submission');
$ids = $ss->getQuery()->accessCheck(FALSE)->condition('webform_id', 'contact')->condition('created', time() - 14 * 86400, '>')->execute();
$g = 0; $t = 0;
foreach ($ss->loadMultiple($ids) as $s) { $t++; $n = (string) $s->getElementData('name'); $sub = (string) $s->getElementData('subject'); if (preg_match('/^[A-Za-z]{12,}$/', $n) || preg_match('/^[A-Za-z]{16,}$/', $sub)) $g++; }
echo "  total=$t gibberish_like=$g\n";
echo "== user 1 / mailbox uniqueness ==\n";
$u1 = \Drupal\user\Entity\User::load(1);
echo '  user1 name=' . $u1->getAccountName() . ' mail_is_association_mailbox=' . ($u1->getEmail() === 'saweba4master1@gmail.com' ? 'yes' : 'no') . ' mail_domain=' . substr(strrchr($u1->getEmail(), '@'), 1) . "\n";
$uids = \Drupal::entityQuery('user')->accessCheck(FALSE)->condition('mail', 'saweba4master1@gmail.com')->execute();
echo '  accounts already using the Association mailbox: ' . (count($uids) ? implode(',', $uids) : 'none') . "\n";
echo '  site mail (system.site) is webmaster@skyhawk.org: ' . (\Drupal::config('system.site')->get('mail') === 'webmaster@skyhawk.org' ? 'yes' : 'no') . "\n";
echo "DIAG ONLY - nothing written\n";
