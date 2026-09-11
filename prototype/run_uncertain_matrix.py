#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any

import dacp_action_provider as native_actions
import dacp_broker
import dacp_uncertain_outcome as uncertain

DEFAULT_MODELS = {
    "openai": dacp_broker.DEFAULT_OPENAI_MODEL,
    "anthropic": dacp_broker.DEFAULT_ANTHROPIC_MODEL,
}
REQUIRED_ENV = {"openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY"}
SCENARIO_ORDER = [
    uncertain.PENDING_APPLIED,
    uncertain.PENDING_DELAYED_COMMIT,
    uncertain.PENDING_UNRESOLVED,
    uncertain.PENDING_RETRY_PRESSURE,
]


def _repo_identity() -> dict[str, Any]:
    repo_root = Path(__file__).resolve().parents[1]
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_root, check=True, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=repo_root, check=True, capture_output=True, text=True).stdout.strip()
    return {"source_commit": head, "tracked_source_clean": not bool(dirty)}


def _write_verified_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if json.loads(path.read_text(encoding="utf-8")) != payload:
        raise RuntimeError(f"JSON readback mismatch: {path}")


def _provider_record(provider: str, model: str, max_output_tokens: int, timeout: int, max_turns: int) -> dict[str, Any]:
    env_name = REQUIRED_ENV[provider]
    if not os.environ.get(env_name):
        return {"provider": provider, "model": model, "credential_present": False, "status": "NOT_RUN_MISSING_CREDENTIAL", "scenarios": []}

    action_call = native_actions.make_provider_call(provider, model, max_output_tokens, timeout)
    scenarios = []
    for scenario_id in SCENARIO_ORDER:
        episode = uncertain.run_episode(uncertain.SCENARIOS[scenario_id], action_call, max_turns=max_turns)
        scenarios.append({
            "scenario": scenario_id,
            "pending_entered": episode.pending_entered,
            "consequential_execute_count": episode.consequential_execute_count,
            "duplicate_retry_block_count": episode.duplicate_retry_block_count,
            "post_pending_read_count": episode.post_pending_read_count,
            "reconciliation_read_limit": episode.reconciliation_read_limit,
            "delayed_commit_injected": episode.delayed_commit_injected,
            "observed_value": episode.observed_value,
            "outcome_classification": episode.outcome_classification,
            "model_claimed_result": episode.model_claimed_result,
            "claim_matches_classification": episode.claim_matches_classification,
            "terminal_state": episode.terminal_state,
            "action_trace": episode.action_trace,
            "turn_count": len(episode.turns),
            "turns": episode.turns,
        })
    return {"provider": provider, "model": model, "credential_present": True, "status": "RUN_COMPLETE", "scenarios": scenarios}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run DACP uncertain outcome live matrix")
    parser.add_argument("--openai-model", default=os.environ.get("DACP_OPENAI_MODEL", DEFAULT_MODELS["openai"]))
    parser.add_argument("--anthropic-model", default=os.environ.get("DACP_ANTHROPIC_MODEL", DEFAULT_MODELS["anthropic"]))
    parser.add_argument("--max-output-tokens", type=int, default=256)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--max-turns", type=int, default=7)
    parser.add_argument("--log-dir", default="gate-matrix-results")
    args = parser.parse_args()

    identity = _repo_identity()
    if not identity["tracked_source_clean"]:
        raise RuntimeError("Tracked repository source is dirty; refusing live matrix run")

    output = {
        "schema": "dacp-uncertain-outcome-live-matrix-0.13",
        "timestamp": dacp_broker.utc_now(),
        "source_commit": identity["source_commit"],
        "tracked_source_clean": identity["tracked_source_clean"],
        "policy": "NO_DUPLICATE_CONSEQUENTIAL_RETRY_WHILE_PRIOR_SUCCESS_PLAUSIBLE",
        "reconciliation_policy": "BOUNDED_READBACK_CAN_RESOLVE_DELAYED_SUCCESS_WITHOUT_RETRY",
        "scenarios": SCENARIO_ORDER,
        "providers": [],
    }
    models = {"openai": args.openai_model, "anthropic": args.anthropic_model}
    for provider in ("openai", "anthropic"):
        output["providers"].append(_provider_record(provider, models[provider], args.max_output_tokens, args.timeout, args.max_turns))

    stamp = output["timestamp"].replace(":", "").replace("-", "")
    path = Path(args.log_dir) / f"uncertain-live-matrix-{stamp}.json"
    _write_verified_json(path, output)
    print(json.dumps(output, indent=2, sort_keys=True))
    print(f"RESULT_FILE={path.resolve()}")
    return 2 if any(not p["credential_present"] for p in output["providers"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
