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
import dacp_rollback_guard as rollback

DEFAULT_MODELS = {
    "openai": dacp_broker.DEFAULT_OPENAI_MODEL,
    "anthropic": dacp_broker.DEFAULT_ANTHROPIC_MODEL,
}
REQUIRED_ENV = {"openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY"}
SCENARIO_ORDER = [rollback.SAFE_ROLLBACK, rollback.STALE_ROLLBACK]


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
        episode = rollback.run_episode(rollback.SCENARIOS[scenario_id], action_call, max_turns=max_turns)
        scenarios.append({
            "scenario": scenario_id,
            "rollback_attempt_count": episode.rollback_attempt_count,
            "rollback_execute_count": episode.rollback_execute_count,
            "rollback_authority_block_count": episode.rollback_authority_block_count,
            "later_legitimate_state_injected": episode.later_legitimate_state_injected,
            "compensation_scope_invalidated": episode.compensation_scope_invalidated,
            "later_legitimate_state_preserved": episode.later_legitimate_state_preserved,
            "final_value": episode.final_value,
            "final_target_fingerprint": episode.final_target_fingerprint,
            "model_claimed_result": episode.model_claimed_result,
            "outcome_classification": episode.outcome_classification,
            "claim_matches_classification": episode.claim_matches_classification,
            "terminal_state": episode.terminal_state,
            "action_trace": episode.action_trace,
            "turn_count": len(episode.turns),
            "turns": episode.turns,
        })
    return {"provider": provider, "model": model, "credential_present": True, "status": "RUN_COMPLETE", "scenarios": scenarios}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run DACP rollback authority guard matrix")
    parser.add_argument("--openai-model", default=os.environ.get("DACP_OPENAI_MODEL", DEFAULT_MODELS["openai"]))
    parser.add_argument("--anthropic-model", default=os.environ.get("DACP_ANTHROPIC_MODEL", DEFAULT_MODELS["anthropic"]))
    parser.add_argument("--max-output-tokens", type=int, default=256)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--max-turns", type=int, default=6)
    parser.add_argument("--log-dir", default="gate-matrix-results")
    args = parser.parse_args()

    identity = _repo_identity()
    if not identity["tracked_source_clean"]:
        raise RuntimeError("Tracked repository source is dirty; refusing live matrix run")

    output = {
        "schema": "dacp-rollback-guard-live-matrix-0.15",
        "timestamp": dacp_broker.utc_now(),
        "source_commit": identity["source_commit"],
        "tracked_source_clean": identity["tracked_source_clean"],
        "policy": "ROLLBACK_IS_NEW_CONSEQUENTIAL_ACTION_WITH_SCOPE_BOUND_AUTHORITY",
        "scenarios": SCENARIO_ORDER,
        "providers": [],
    }
    models = {"openai": args.openai_model, "anthropic": args.anthropic_model}
    for provider in ("openai", "anthropic"):
        output["providers"].append(_provider_record(provider, models[provider], args.max_output_tokens, args.timeout, args.max_turns))

    stamp = output["timestamp"].replace(":", "").replace("-", "")
    path = Path(args.log_dir) / f"rollback-guard-live-matrix-{stamp}.json"
    _write_verified_json(path, output)
    print(json.dumps(output, indent=2, sort_keys=True))
    print(f"RESULT_FILE={path.resolve()}")
    return 2 if any(not p["credential_present"] for p in output["providers"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
