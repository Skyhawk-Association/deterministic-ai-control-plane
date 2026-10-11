#!/bin/bash
# READ-ONLY scan (2026-10-11) of archived A2 database dumps on InMotion for old Join-Us data.
# Prints ONLY file names, form ids, counts and dates - never names, addresses or submission values.
echo "== candidate A2 dumps =="
mapfile -t F < <(find ~/skyhawk-migration ~/backups -maxdepth 3 -type f \( -name '*.sql.gz' -o -name '*.sql.gz.gz' -o -name '*.sql' \) 2>/dev/null | grep -Ei 'a2|darwus|cutover' | sort)
for f in "${F[@]}"; do printf '%s  %s bytes  %s\n' "$f" "$(stat -c %s "$f")" "$(date -r "$f" +%F)"; done
[ ${#F[@]} -eq 0 ] && { echo "no A2 dumps found"; exit 0; }
cat_any() { # decompress any number of gzip layers
  local f="$1"; local cmd="cat \"$f\""
  local t; t=$(eval "$cmd" | head -c 2 | od -An -tx1 | tr -d ' ')
  while [ "$t" = "1f8b" ]; do cmd="$cmd | gzip -dc"; t=$(eval "$cmd" 2>/dev/null | head -c 2 | od -An -tx1 | tr -d ' '); done
  eval "$cmd"
}
for f in "${F[@]}"; do
  echo "================ $(basename "$f")"
  cat_any "$f" | python3 -c '
import re, sys, collections
wf = collections.Counter(); wfd = {}; cm = collections.Counter(); cfg = set(); nodes = []
re_wf  = re.compile(r"\((\d+),\x27([a-z0-9_]+)\x27,\x27[0-9a-f-]{36}\x27")
re_cm  = re.compile(r"\((\d+),\x27([a-z0-9_]+)\x27,\x27[0-9a-f-]{36}\x27,\x27[a-z]{2,3}\x27")
re_cfg = re.compile(r"\x27(webform\.webform\.[a-z0-9_]+|contact\.form\.[a-z0-9_]+)\x27")
re_ts  = re.compile(r"\((\d+),\x27([a-z0-9_]+)\x27,\x27[0-9a-f-]{36}\x27,[^)]*?,(1[0-9]{9}),")
for line in sys.stdin.buffer:
    if not line.startswith(b"INSERT INTO"): continue
    s = line.decode("utf-8", "replace")
    tbl = s[13:s.find("`", 13)]
    if tbl == "webform_submission":
        for m in re_wf.finditer(s): wf[m.group(2)] += 1
        for m in re_ts.finditer(s):
            k = m.group(2); t = int(m.group(3)); a, b = wfd.get(k, (t, t)); wfd[k] = (min(a, t), max(b, t))
    elif tbl == "contact_message":
        for m in re_cm.finditer(s): cm[m.group(2)] += 1
    elif tbl == "config":
        cfg.update(m.group(1) for m in re_cfg.finditer(s))
    elif tbl == "node_field_data":
        for m in re.finditer(r"\x27([^\x27]*(?:[Jj]oin|[Mm]embership [Aa]pplic)[^\x27]*)\x27", s): nodes.append(m.group(1)[:80])
import datetime as d
fmt = lambda t: d.datetime.fromtimestamp(t, d.timezone.utc).strftime("%Y-%m-%d")
print("webform/contact config objects:", ", ".join(sorted(cfg)) or "none")
print("webform submissions by form:")
for k, v in wf.most_common():
    a, b = (fmt(wfd[k][0]), fmt(wfd[k][1])) if k in wfd else ("?", "?")
    print(f"  {k:32s} {v:6d}  {a} .. {b}")
print("contact messages by form:", dict(cm) or "none")
print("join-like node titles:", sorted(set(nodes))[:20] or "none")
'
done
echo "SCAN ONLY - nothing written"
