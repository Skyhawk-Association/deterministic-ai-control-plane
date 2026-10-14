#!/bin/bash
# Runs contact_fix_testmode_honeypot_user1.php with a config backup first, clears cache, then checks the public form.
S=$(cd "$(dirname "$0")" && pwd)
cd ~/drupalbeta || exit 1
T=$(mktemp -d); ln -s /usr/local/bin/php84-skyhawk "$T/php"
mkdir -p ~/backups/config
B=~/backups/config/webform.contact.pre-testmode-fix-$(date -u +%Y%m%dT%H%M%SZ).yml
PATH=$T:$PATH vendor/bin/drush cget webform.webform.contact --format=yaml > "$B" && echo "backup $(basename "$B") $(wc -l < "$B") lines" || { echo "ABORT: backup failed"; exit 1; }
PATH=$T:$PATH vendor/bin/drush php:script "$S/contact_fix_testmode_honeypot_user1.php"
PATH=$T:$PATH vendor/bin/drush cr
echo "== public form check (anonymous) =="
H=$(curl -s -L --max-time 30 "https://skyhawk.org/form/contact")
echo "form loads: $(curl -s -o /dev/null -w '%{http_code}' https://skyhawk.org/form/contact)"
echo "honeypot markers in form HTML: $(echo "$H" | grep -oiE 'honeypot|url-textfield|honeypot_time' | sort | uniq -c | tr '\n' ' ')"
rm -rf "$T"
