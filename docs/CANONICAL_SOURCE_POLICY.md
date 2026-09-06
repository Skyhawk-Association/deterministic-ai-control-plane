# Canonical Source Policy

## Current phase

The public Git repository is being promoted to the canonical public DACP source only after read-back verification of the active specification and governing files.

## Canonical rule

Once `CURRENT.md` states `ACTIVE GIT CANONICAL` on `main`, the repository named there is the canonical public source for the active DACP specification and public governance files. Drive becomes a convenience mirror and historical migration source rather than a competing source of current truth.

## Conflict handling

If a mirror disagrees with canonical Git, preserve the disagreement and resolve it against the exact Git version/commit/blob plus applicable governing authority. Do not silently average divergent copies.

## Future NAS role

The NAS may later become the protected private operational substrate and backup/recovery surface. That does not automatically displace public Git as the public dissemination/version-control source.
