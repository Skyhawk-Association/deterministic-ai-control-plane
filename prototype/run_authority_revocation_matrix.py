#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any

import dacp_action_provider as native_actions
import dacp_authority_revocation_guard as revocation
import dacp_broker

DEFAULT_MODELS = {
    "openai": dacp_broker.DEFAULT_OPENAI_MODEL,
    "anthropic": dacp_broker.DEFAULT_ANTHROPIC_MODEL,
}
REQUIRED_ENV = {"openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY"}
SCENARIO_ORDER = [
    revocation.VALID_CONTROL,
    revocation.REVOKED_AFTER_PREDECLARE,
    revocation.TRUST_ROOT_COMPROMISED,
]


def _repo_identity() -> dict[str, Any]:
    repo_root = Path(__file__).resolve().parents[1]
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo_root, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    dirty = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"], cwd=repo_root,
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    return {"source_commit": head, "tracked_source_clean": not bool(dirty)}


def _write_verified_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if json.loads(path.read_text(encoding="utf-8")) != payload:
        raise RuntimeError(f"JSON readback mismatch: {path}")


def _provider_record(provider: str, model: str, max_output_tokens: int, timeout: int, max_turns: int) -> dict[str, Any]:
    env_name = REQUIRED_ENV[provider]
    if not os.environ.get(env_name):
        return {
            "provider": provider,
            "model": model,
            "credential_present": False,
            "status": "NOT_RUN_MISSING_CREDENTIAL",
            "scenarios": [],
        }

    action_call = native_actions.make_provider_call(provider, model, max_output_tokens, timeout)
    scenarios = []
    for scenario_id in SCENARIO_ORDER:
        episode = revocation.run_episode(
            revocation.SCENARIOS[scenario_id], action_call, max_turns=max_turns,
        )
        scenarios.append({
            "scenario": scenario_id,
            "approval_id": episode.approval_id,
            "approval_trust_root": episode.approval_trust_root,
            "authority_initially_valid": episode.authority_initially_valid,
            "revocation_injected": episode.revocation_injected,
            "trust_root_compromise_injected": episode.trust_root_compromise_injected,
            "authority_event_hidden_until_commit": episode.authority_event_hidden_until_commit,
            "commit_authority_revalidation_count": episode.commit_authority_revalidation_count,
            "authority_block_count": episode.authority_block_count,
            "authority_failure_reason": episode.authority_failure_reason,
            "consequential_attempt_count": episode.consequential_attempt_count,
            "consequential_execute_count": episode.consequential_execute_count,
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

    return {
        "provider": provider,
        "model": model,
        "credential_present": True,
        "status": "RUN_COMPLETE",
        "scenarios": scenarios,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run DACP authority revocation live matrix")
    parser.add_argument("--openai-model", default=os.environ.get("DACP_OPENAI_MODEL", DEFAULT_MODELS["openai"]))
    parser.add_argument("--anthropic-model", default=os.environ.get("DACP_ANTHROPIC_MODEL", DEFAULT_MODELS["anthropic"]))
    parser.add_argument("--max-output-tokens", type=int, default=256)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--max-turns", type=int, default=5)
    parser.add_argument("--log-dir", default="gate-matrix-results")
    args = parser.parse_args()

    identity = _repo_identity()
    if not identity["tracked_source_clean"]:
        raise RuntimeError("Tracked repository source is dirty; refusing live matrix run")

    output = {
        "schema": "dacp-authority-revocation-live-matrix-0.17",
        "timestamp": dacp_broker.utc_now(),
        "source_commit": identity["source_commit"],
        "tracked_source_clean": identity["tracked_source_clean"],
        "policy": "COMMIT_TIME_AUTHORITY_REVALIDATION_AND_TRUST_ROOT_QUARANTINE",
        "scenarios": SCENARIO_ORDER,
        "providers": [],
    }

    models = {"openai": args.openai_model, "anthropic": args.anthropic_model}
    for provider in ("openai", "anthropic"):
        output["providers"].append(
            _provider_record(provider, models[provider], args.max_output_tokens, args.timeout, args.max_turns)
        )

    stamp = output["timestamp"].replace(":", "").replace("-", "")
    path = Path(args.log_dir) / f"authority-revocation-live-matrix-{stamp}.json"
    _write_verified_json(path, output)

    print(json.dumps(output, indent=2, sort_keys=True))
    print(f"RESULT_FILE={path.resolve()}")
    missing = [p["provider"] for p in output["providers"] if not p["credential_present"]]
    return 2 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
