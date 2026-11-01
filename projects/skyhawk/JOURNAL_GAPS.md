# Skyhawk Journal PDF gaps (website)

**Purpose:** the list of Journal issues missing from skyhawk.org. Every Journal published since 1995 exists as a PDF somewhere (USER-STATED, Gene, 2026-11-01); this file tracks which ones the website lacks and where each is found.

**Status of this list: UNVERIFIED.** The 15 gaps below were reported by ChatGPT on 2026-11-01 (relayed by Gene in the Claude session). ChatGPT did not show its source listing or commit it (its write to dacp-private failed). Claude has not checked any entry against the live `sajournals` folder. Treat each line as a candidate gap until verified.

**Naming on the live site:** journals sit under `private://sajournals/` (and `sajournals/archive/`), file names like `1995-1.1.pdf` (year-volume.issue). Exact file names for the gaps were not provided, except where noted.

| # | Year | Issue | Variants | Live site | Synology / other copy | Notes |
|---|---|---|---|---|---|---|
| 1 | 2000 | 6.3 | | missing (reported) | not yet searched | May be inside `2000-6.2&6.3.pdf` (combined issue?) |
| 2 | 2002 | 8.3 | | missing (reported) | not yet searched | |
| 3 | 2002 | 8.4 | | missing (reported) | not yet searched | |
| 4 | 2003 | 9.2 | | missing (reported) | not yet searched | |
| 5 | 2003 | 9.3 | | missing (reported) | not yet searched | |
| 6 | 2003 | 9.4 | | missing (reported) | not yet searched | |
| 7 | 2004 | 10.1 | | missing (reported) | not yet searched | |
| 8 | 2004 | 10.2 | | missing (reported) | not yet searched | |
| 9 | 2013 | 19.2 | | missing (reported) | not yet searched | |
| 10 | 2013 | 19.3 | | missing (reported) | not yet searched | |
| 11 | 2015 | 21.2 | | missing (reported) | not yet searched | |
| 12 | 2015 | 21.3 | | missing (reported) | not yet searched | |
| 13 | 2017 | 23.3 | | missing (reported) | not yet searched | |
| 14 | 2025 | 31-2 | Spreads, Print-friendly | missing (reported) | not yet searched | |
| 15 | 2025 | 31-3 | Spreads, Print-friendly | missing (reported) | not yet searched | |

**Related (LOST-D, parked 2026-10-09):** "missing journal issues awaiting digital copies (Mat Garretson)".

## Verification plan
1. Read-only listing of the live `sajournals` folders, to confirm each gap and record exact file names.
2. Search the old-Synology PDF list (home NAS, `skyhawk-d6-recovery/pdf-search/`) and the Drupal 6 journal records for each issue.
3. Update the two right-hand columns per issue: FOUND (path, size, SHA-256) or NOT FOUND (for Mat Garretson).

## Change log
- 2026-11-01: list created from ChatGPT's report (15 gaps), unverified (Claude).
