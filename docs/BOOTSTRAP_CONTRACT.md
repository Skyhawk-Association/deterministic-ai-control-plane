# Bootstrap Contract

`CURRENT.md` is the stable human-readable bootstrap address. `CURRENT.json` is its machine-readable companion.

Before consequential DACP reliance, a consumer should resolve the current branch and bootstrap, load the listed governing files, and bind the active specification to the Git blob identity stated in `CURRENT.json` when reasonably available.

A stale cached copy, remembered version, local working tree, or mirror is not sufficient proof of current canonical state when the canonical repository is reachable.

## Mandatory staleness check (2026-09-23)

"When reasonably available" is not sufficient: a cached copy can be internally consistent and indistinguishable from current. Therefore:

1. Retrieve CURRENT.md through an uncached path: git clone / git ls-remote, api.github.com, or raw.githubusercontent.com. Rendered github.com /blob/ pages are not bootstrap evidence.
2. Record the main HEAD commit SHA at retrieval.
3. Verify `git rev-parse HEAD:<active spec path>` equals the blob stated in CURRENT.md / CURRENT.json.
4. Mismatch = stale or tampered source: stop and re-resolve. No uncached path = GOVERNED STOP or Gene-supplied HEAD SHA; never fall back to a cached page.

Evidence and regression fixture: authoritative/DACP_Decision_Record_2026-09-23_Executor_Transfer.md.
