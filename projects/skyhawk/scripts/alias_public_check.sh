#!/bin/bash
# Public-side (anonymous) check of the 54 pages changed by alias_apply.php on 2026-10-11. Read-only.
BASE="https://skyhawk.org"
NIDS="4 24 25 32 39 41 72 85 86 88 90 91 92 97 98 100 101 102 104 110 111 121 123 124 132 136 157 158 163 165 166 169 204 205 208 214 216 218 226 233 234 240 248 253 254 257 323 340 478 712 714 715 720 49221"
OLD='[A-Za-z0-9._%+-]+@(a4skyhawk\.(org|net)|skyhawk\.org|darw\.it)'
T=$(mktemp -d); bad=0; n=0
for nid in $NIDS; do
  n=$((n+1))
  read -r code url < <(curl -s -L --max-time 30 -o "$T/p" -w '%{http_code} %{url_effective}' "$BASE/node/$nid")
  old=$(grep -Eoi "$OLD" "$T/p" | grep -vic '^webmaster@skyhawk\.org$')
  links=$(grep -o 'href="/form/contact?category=[^"]*"' "$T/p" | wc -l)
  dup=$(grep -Eoi '\b(the|contact|e-?mail)(\s|&nbsp;)+(the(\s|&nbsp;)+)?<a href="/form/contact[^"]*">the Contact form' "$T/p" | wc -l)
  flag=OK
  if [ "$code" = "200" ]; then { [ "$old" -gt 0 ] || [ "$links" -lt 1 ] || [ "$dup" -gt 0 ]; } && flag=CHECK
  elif [ "$code" = "403" ]; then flag=MEMBERS-ONLY
  else flag=CHECK; fi
  [ "$flag" = CHECK ] && bad=$((bad+1))
  printf '%-6s http=%s old=%s contact_links=%s awkward=%s %s %s\n' "$nid" "$code" "$old" "$links" "$dup" "$flag" "${url#$BASE}"
done
echo "== footer/global check: plain webmaster@skyhawk.org occurrences on node/72 (site-wide template text, not page body) =="
curl -s -L --max-time 30 "$BASE/node/72" | grep -oi 'webmaster@skyhawk\.org' | wc -l
echo "== prepopulate check =="
curl -s -L --max-time 30 "$BASE/form/contact?category=history&unit=VA-12" -o "$T/f"
echo "http=$(curl -s -o /dev/null -w '%{http_code}' "$BASE/form/contact?category=history&unit=VA-12")"
grep -Eo '<option value="(history|VA-12)"[^>]*>' "$T/f" | sort -u
rm -rf "$T"
echo "PAGES=$n NEED_CHECK=$bad"
[ "$bad" -eq 0 ] && echo "RESULT=PASS" || echo "RESULT=REVIEW"
