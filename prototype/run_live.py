#!/usr/bin/env python3
"""Default live entrypoint for the DACP prototype.

The public command intentionally delegates to the consolidated commitment-core
integration. Historical matrix runners remain available only as regression and
field-evidence surfaces; they are not the current application execution path.
"""

from run_core_live_integration import main


if __name__ == "__main__":
    raise SystemExit(main())
