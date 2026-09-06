# Repository Integrity and Verification

## Required success evidence for material repository changes

1. The intended target repository and branch are re-resolved before commit.
2. The change is committed with an identifiable Git commit.
3. The expected paths exist after the branch update.
4. Material files are read back from GitHub, not merely trusted from the write response.
5. The active specification's Git blob SHA matches the bootstrap manifest.
6. Public-read claims are tested through a public GitHub/raw retrieval path when public accessibility matters.
7. Previous active specification state remains preserved in history or otherwise immutably reachable.

## Failure states

- Write failed and no state change is plausible: `FAILED`.
- Write outcome is uncertain: `PENDING`; do not retry blindly.
- Write succeeded but read-back/integrity check failed: `UNVERIFIED`; do not claim active canonical state.
- Branch or target moved unexpectedly: reopen Orientation before commit/retry.
