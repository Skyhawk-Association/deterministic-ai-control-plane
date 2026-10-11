<?php
// Shared transform: old Skyhawk alias addresses -> Contact-form links. Pure function, no Drupal.
const ALIAS_MAP = [
  'webmaster' => 'website', 'a4modelers' => 'modeling', 'sa-journal-editor' => 'journal',
  'sa-a4-research' => 'research', 'historical-research' => 'research',
  'rr-access' => 'membership_login', 'rr-acess' => 'membership_login',
  'sa-contact-losses' => 'history', 'membership-paypal' => 'membership_paypal',
  'sa-patch' => 'patch_orders', 'a4join' => 'membership_login',
];
const ALIAS_RE = '/[A-Za-z0-9._%+-]+@(?:a4skyhawk\.(?:org|net)|skyhawk\.org|darw\.it)\b/i';

function alias_url($addr, $unit) {
  $local = strtolower(explode('@', $addr)[0]);
  if (!isset(ALIAS_MAP[$local])) return NULL;
  $q = 'category=' . ALIAS_MAP[$local];
  if ($unit !== '') $q .= '&amp;unit=' . rawurlencode($unit);
  return '/form/contact?' . $q;
}

function alias_transform($html, $unit, &$st) {
  $st = ['mailto' => 0, 'bare' => 0, 'unmapped' => []];
  // 1. mailto anchors
  $html = preg_replace_callback('#<a\b([^>]*?)href\s*=\s*(["\'])\s*mailto:([^"\'?]+)[^"\']*\2([^>]*)>(.*?)</a>#is',
    function ($m) use ($unit, &$st) {
      $addr = trim(rawurldecode($m[3]));
      if (!preg_match(ALIAS_RE, $addr)) return $m[0];
      $url = alias_url($addr, $unit);
      if ($url === NULL) { $st['unmapped'][] = strtolower($addr); return $m[0]; }
      $st['mailto']++;
      $text = $m[5];
      if (preg_match('/@/', strip_tags($text)) || trim(strip_tags($text)) === '') $text = 'the Contact form';
      return '<a href="' . $url . '">' . $text . '</a>';
    }, $html);
  // 2. bare addresses in text (not inside tags, not inside other anchors)
  $parts = preg_split('/(<[^>]*>)/', $html, -1, PREG_SPLIT_DELIM_CAPTURE);
  $inA = 0;
  foreach ($parts as $i => $p) {
    if ($p !== '' && $p[0] === '<') {
      if (preg_match('#^<a\b#i', $p)) $inA++;
      elseif (preg_match('#^</a\s*>#i', $p)) $inA = max(0, $inA - 1);
      continue;
    }
    $parts[$i] = preg_replace_callback(ALIAS_RE, function ($m) use ($unit, &$st, $inA) {
      $url = alias_url($m[0], $unit);
      if ($url === NULL) { $st['unmapped'][] = strtolower($m[0]); return $m[0]; }
      $st['bare']++;
      return $inA ? 'the Contact form' : '<a href="' . $url . '">the Contact form</a>';
    }, $p);
  }
  return implode('', $parts);
}
