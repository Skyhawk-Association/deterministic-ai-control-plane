#!/bin/bash
# READ-ONLY diagnostic (2026-10-14): does an AUTHENTICATED request for the Ready Room article succeed server-side?
# Discriminates article ACL vs browser/session/host/cache. Creates one throwaway session per test account via a
# one-time login link (never printed), fetches the page on both hostnames, then deletes ONLY that session.
# Prints statuses, cache headers, uids/roles and yes/no content markers - no tokens, cookies, names or addresses.
cd ~/drupalbeta || exit 1
T=$(mktemp -d); ln -s /usr/local/bin/php84-skyhawk "$T/php"; export PATH=$T:$PATH
D=vendor/bin/drush
P=/article-readyroom/who-handles-what
hdrs() { grep -iE '^(HTTP/|cache-control|vary|expires|age:|x-drupal-cache|x-drupal-dynamic-cache|x-cache|x-proxy-cache|x-fastcgi-cache|location)' "$1" | tr -d '\r' | sed 's/^/     /'; }
probe() { # $1 label, $2 host, $3 jar-or-empty
  local H=$T/h B=$T/b; local opt=(); [ -n "$3" ] && opt=(-b "$3")
  curl -s -D "$H" -o "$B" --max-time 30 "${opt[@]}" "https://$2$P"
  echo "  [$1] host=$2 article_title_present=$(grep -q 'Who Handles What' "$B" && echo yes || echo no) waveoff=$(grep -qi 'Wave-off' "$B" && echo yes || echo no) login_link=$(grep -q 'href="/user/login' "$B" && echo yes || echo no) logout_link=$(grep -q '/user/logout' "$B" && echo yes || echo no)"
  hdrs "$H"
}
echo "== node behind the alias"
$D php:eval '$p=\Drupal::service("path_alias.manager")->getPathByAlias("/article-readyroom/who-handles-what"); echo "path=$p"; if(preg_match("#/node/(\d+)#",$p,$m)){$n=\Drupal\node\Entity\Node::load($m[1]); echo " type=".$n->bundle()." published=".(int)$n->isPublished();} echo PHP_EOL;'
NID=$($D php:eval 'echo (int) preg_replace("#\\D#", "", \Drupal::service("path_alias.manager")->getPathByAlias("/article-readyroom/who-handles-what"));')
echo "nid=$NID"
echo "== anonymous"
probe anon skyhawk.org ""
probe anon www.skyhawk.org ""
# test accounts: Gene's blade-role account (else uid 1) and one ordinary member (authorized_user only, no admin/blade)
read -r GENE MEMBER < <($D php:eval '$q=fn()=>\Drupal::entityQuery("user")->accessCheck(FALSE)->condition("status",1);
$g=$q()->condition("roles","blade")->range(0,1)->execute(); $g=$g?reset($g):1;
$m=$q()->condition("roles","authorized_user")->condition("uid",1,">")->execute(); $mm=0;
foreach(\Drupal\user\Entity\User::loadMultiple($m) as $u){ $r=$u->getRoles(); if(!array_intersect($r,["admin","blade","board","xo","co"])){$mm=$u->id();break;} }
echo "$g $mm";')
for U in $GENE $MEMBER; do
  [ "$U" = "0" ] && continue
  echo "== authenticated test uid=$U roles=$($D php:eval "echo implode(',', \Drupal\user\Entity\User::load($U)->getRoles());") drupal_access=$($D php:eval "echo \Drupal\node\Entity\Node::load($NID)->access('view', \Drupal\user\Entity\User::load($U)) ? 'allow' : 'deny';")"
  J=$T/jar.$U
  URL=$($D user:login --uid=$U --no-browser --uri=https://skyhawk.org 2>/dev/null | tail -1)
  curl -s -L -c "$J" -b "$J" -o /dev/null --max-time 30 "$URL"
  echo "  session cookie set for host: $(awk '$6 ~ /^S?SESS/ {print $1}' "$J" | sort -u | tr '\n' ' ')"
  probe "uid$U" skyhawk.org "$J"
  probe "uid$U-same-cookie" www.skyhawk.org "$J"
  SV=$(awk '$6 ~ /^S?SESS/ {print $7}' "$J" | head -1)
  if [ -n "$SV" ]; then SV="$SV" $D php:eval '$h=\Drupal\Component\Utility\Crypt::hashBase64(getenv("SV")); $n=\Drupal::database()->delete("sessions")->condition("sid",$h)->execute(); echo "  test session removed: $n".PHP_EOL;'; fi
  unset URL SV
done
rm -rf "$T"
echo "DIAG ONLY - no site changes (throwaway test sessions removed)"
