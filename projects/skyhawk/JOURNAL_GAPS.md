# Skyhawk Journal PDF gaps (website)

**Purpose:** the list of Journal issues missing from skyhawk.org. Every Journal published since 1995 exists as a PDF somewhere (USER-STATED, Gene, 2026-11-01); this file tracks which ones the website lacks and where each is found.

**Verified 2026-11-01 (Claude)** against a read-only listing of both live folders on the InMotion server: `/home/n790725/drupalbeta/web/private/sajournals` (incl. `archive/`) and `/home/n790725/drupalbeta/web/sites/default/files/sajournals`. Naming: `YYYY-V.I.pdf` (volume = year - 1994), plus `-spreads` and `print friendly` variants.

**Which files the /sa-journal page uses (VERIFIED 2026-11-01, drush sql:query, read-only):** the page lists the 105 `journal` nodes. Their `field_pdf` points to `public://sajournals/...` (= `web/sites/default/files/sajournals`) for every issue; `field_pdf_print` is set on 12 nodes, also `public://`, except Spring 2026 (Vol. 32 No. 1), whose only file is `field_pdf_print` = `private://sajournals/Skyhawk-Vol32-1-spreads.pdf` (its `field_pdf` is empty). So the PUBLIC folder is what the page serves; `private/sajournals` is not used by the page apart from that one file. The 20 issues without a node are exactly the 20 gaps below (12 confirmed + 8 if published).

**Assumption, not verified:** four issues per year (the live folders hold .1-.4 for most years). Gene to confirm which issues were actually published.

## Confirmed missing from both live folders (12 of ChatGPT's 15)

| # | Year | Issue | Expected file name | Synology / other copy |
|---|---|---|---|---|
| 1 | 2002 | 8.3 | 2002-8.3.pdf | not yet searched |
| 2 | 2002 | 8.4 | 2002-8.4.pdf | not yet searched |
| 3 | 2003 | 9.2 | 2003-9.2.pdf | not yet searched |
| 4 | 2003 | 9.3 | 2003-9.3.pdf | not yet searched |
| 5 | 2003 | 9.4 | 2003-9.4.pdf | not yet searched |
| 6 | 2004 | 10.1 | 2004-10.1.pdf | not yet searched |
| 7 | 2013 | 19.2 | 2013-19.2.pdf | not yet searched |
| 8 | 2013 | 19.3 | 2013-19.3.pdf | not yet searched |
| 9 | 2015 | 21.2 | 2015-21.2.pdf | not yet searched |
| 10 | 2017 | 23.3 | 2017-23.3.pdf | not yet searched |
| 11 | 2025 | 31.2 | 2025-31.2.pdf, -spreads, print friendly | not yet searched |
| 12 | 2025 | 31.3 | 2025-31.3.pdf, -spreads, print friendly | not yet searched |

## ChatGPT-reported gaps that are NOT missing (3)

| Year | Issue | Present on the live site as |
|---|---|---|
| 2000 | 6.3 | `2000-6.3.pdf` (11,228,184 B, both folders) and combined `2000-6.2-6.3.pdf` / `2000-6.2&6.3.pdf` (22,429,231 B) |
| 2004 | 10.2 | `2004-10.2.pdf` (9,560,374 B, both folders) |
| 2015 | 21.3 | `2015-21.3.pdf` (3,320,899 B, both folders) |

## Further candidates not on ChatGPT's list (8): missing IF they were published

| Year | Issue | Note |
|---|---|---|
| 1995 | 1.2, 1.3, 1.4 | only 1995-1.1 exists |
| 1996 | 2.4 | |
| 2008 | 14.4 | 2008-2011 each have .1-.3 only: possibly three issues a year then |
| 2009 | 15.4 | |
| 2010 | 16.4 | |
| 2011 | 17.4 | |

## Anomalies for Gene

- `Winter 2012-2013.pdf` (14,996,025 B, plus 8 identical `_2`..`_9` copies in each folder): issue number unknown; not identical in size to 2012-18.4 or 2013-19.1.
- `1999-4.1.pdf` (11,772,716 B, public folder): volume 4 is 1998; differs from `1998-4.1.pdf` (12,877,927 B) and `1999-5.1.pdf` (10,848,974 B). Misnamed issue?
- Every .1 issue (1995-2022) exists only in the public folder; that is the folder the page uses, so this is not a defect.
- 2026 32.1 exists only as `private/sajournals/Skyhawk-Vol32-1-spreads.pdf` (thumbnail present in public).

## Verification plan (remaining)
1. Gene: confirm the publication schedule (which candidates above were real issues), identify the Winter 2012-2013 and 1999-4.1 files.
2. Search the old-Synology PDFs (home NAS, read-only) and the Drupal 6 journal records for each confirmed gap; record FOUND (path, size, SHA-256) or NOT FOUND (for Mat Garretson).

## Change log
- 2026-11-01: list created from ChatGPT's report (15 gaps), unverified (Claude).
- 2026-11-01: verified against the live folders: 12 confirmed, 3 not missing, 8 further candidates, 4 anomalies (Claude).
- 2026-11-01: verified the page serves public://sajournals (105 journal nodes); gap set unchanged (Claude).
- 2026-11-01 18:56 ET: live journal PDFs fingerprinted (SHA-256, both folders, exit 0). Content-based Synology scan RUNNING on the home NAS (temporary container `pdfscan`, python:3.12-slim, Synology mounted read-only; results in `skyhawk-d6-recovery/pdf-search/summary.txt` and `candidates.tsv`). Next: read the summary, then record FOUND / NOT FOUND per gap here (Claude).
- 2026-11-02 13:40 ET: USER-STATED (Gene): the content scan of the old-Envy backup was terminated; no results. Gene: no further Synology work. Synology / other copy column stays "not yet searched". Remaining route for the 12 confirmed gaps: other sources (e.g. Mat Garretson, per LOST-D parked item).
