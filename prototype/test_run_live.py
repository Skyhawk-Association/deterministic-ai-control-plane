import run_live
import run_core_live_integration


def test_run_live_delegates_to_consolidated_core_entrypoint():
    assert run_live.main is run_core_live_integration.main
