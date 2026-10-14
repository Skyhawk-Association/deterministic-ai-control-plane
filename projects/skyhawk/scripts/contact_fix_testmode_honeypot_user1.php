<?php
// Gene-authorized fix (2026-10-13):
//  1. remove "TEST MODE: Delivered only to adminscoot." from every contact-webform email body;
//  2. turn on Honeypot (hidden field + time restriction) for the contact webform;
//  3. set user 1 e-mail to the Association mailbox (verified unused by any other account).
$st = \Drupal::entityTypeManager()->getStorage('webform');
$w = $st->load('contact');
$fail = 0; $changed = 0;
foreach ($w->getHandlers() as $id => $h) {
  $c = $h->getConfiguration(); if (($c['id'] ?? '') !== 'email') continue;
  $b = (string) ($c['settings']['body'] ?? '');
  if (stripos($b, 'TEST MODE') === FALSE) continue;
  $nb = preg_replace('/TEST MODE:\s*Delivered only to adminscoot\.?/i', '', $b);
  // drop wrappers left empty by the removal
  for ($i = 0; $i < 3; $i++) $nb = preg_replace('#<(p|em|strong|b|i|span|div)[^>]*>(\s|&nbsp;|<br\s*/?>)*</\1>#i', '', $nb);
  $c['settings']['body'] = $nb; $h->setConfiguration($c); $changed++;
}
$w->setThirdPartySetting('honeypot', 'honeypot', TRUE);
$w->setThirdPartySetting('honeypot', 'time_restriction', TRUE);
$w->save();
$w = $st->loadUnchanged('contact');
foreach ($w->getHandlers() as $id => $h) {
  $c = $h->getConfiguration(); if (($c['id'] ?? '') !== 'email') continue;
  $b = (string) ($c['settings']['body'] ?? '');
  $bad = stripos($b, 'TEST MODE') !== FALSE || stripos($b, 'adminscoot') !== FALSE;
  if ($bad) $fail++;
  printf("  %-24s test_text_left=%s body_len=%d\n", $id, $bad ? 'YES' : 'no', strlen($b));
}
echo "handlers_changed=$changed\n";
$hp = $w->getThirdPartySettings('honeypot');
echo 'honeypot=' . json_encode($hp) . "\n";
if (empty($hp['honeypot']) || empty($hp['time_restriction'])) $fail++;
$sample = (string) $w->getHandler('email_notification')->getConfiguration()['settings']['body'];
echo 'notification body now starts: ' . preg_replace('/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+/', '[addr]', substr(preg_replace('/\s+/', ' ', strip_tags($sample)), 0, 140)) . "\n";
// user 1
$taken = \Drupal::entityQuery('user')->accessCheck(FALSE)->condition('mail', 'saweba4master1@gmail.com')->condition('uid', 1, '<>')->execute();
if ($taken) { echo "user1: SKIPPED, address used by uid " . implode(',', $taken) . "\n"; $fail++; }
else {
  $u = \Drupal\user\Entity\User::load(1);
  $u->setEmail('saweba4master1@gmail.com');
  $u->_skipProtectedUserFieldConstraint = TRUE; // CLI has no current password; admin change
  $v = $u->validate();
  $errs = [];
  foreach ($v as $e) if ($e->getPropertyPath() === 'mail' || str_starts_with($e->getPropertyPath(), 'mail.')) $errs[] = (string) $e->getMessage();
  if ($errs) { echo 'user1: VALIDATION FAILED ' . implode('; ', $errs) . "\n"; $fail++; }
  else { $u->save(); $chk = \Drupal::entityTypeManager()->getStorage('user')->loadUnchanged(1);
    echo 'user1 mail is Association mailbox: ' . ($chk->getEmail() === 'saweba4master1@gmail.com' ? 'yes' : 'NO') . "\n";
    if ($chk->getEmail() !== 'saweba4master1@gmail.com') $fail++; }
}
echo $fail ? "RESULT=FAIL ($fail)\n" : "RESULT=PASS\n";
