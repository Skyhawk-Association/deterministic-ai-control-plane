#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any

import dacp_action_history_provider as history_actions
import dacp_action_provider as native_actions
import dacp_broker
import dacp_gate_beta as base_gate
import dacp_gate_beta_v2 as gate

DEFAULT_MODELS = {
    "openai": dacp_broker.DEFAULT_OPENAI_MODEL,
    "anthropic": dacp_broker.DEFAULT_ANTHROPIC_MODEL,
}
REQUIRED_ENV = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
}
SCENARIO_ORDER = [
    "deceptive_tool",
    gate.COLLUDING_VERIFIER_SCENARIO_ID,
    gate.SELF_VERIFIER_SCENARIO_ID,
    gate.DELAYED_OVERRIDE_SCENARIO_ID,
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


def _provider_record(provider: str, model: str, max_output_tokens: int, timeout: int, max_turns: int) -> dict[str, Any]:
    env_name = REQUIRED_ENV[provider]
    if not os.environ.get(env_name):
        return {
            "provider": provider, "model": model, "credential_env": env_name,
            "credential_present": False, "status": "NOT_RUN_MISSING_CREDENTIAL",
            "rule_knowledge_test": None, "general_control_knowledge": None,
            "independence_knowledge": None, "knowledge_probe_status": None,
            "knowledge_probe_raw_text": None, "knowledge_probe_method": None,
            "knowledge_probe_rubric": None, "action_interface": "PROVIDER_NATIVE",
            "scenarios": [],
        }

    knowledge_call = base_gate._make_provider_call(provider, model, max_output_tokens, timeout)
    action_call = native_actions.make_provider_call(provider, model, max_output_tokens, timeout)
    history_call = history_actions.make_history_provider_call(provider, model, max_output_tokens, timeout)
    knowledge = gate.run_knowledge_probe(knowledge_call)
    scenarios: list[dict[str, Any]] = []

    for scenario_id in SCENARIO_ORDER:
        episode = gate.run_episode(
            gate.SCENARIOS[scenario_id], action_call, max_turns=max_turns,
            history_provider_call=history_call,
        )
        scenarios.append({
            "scenario": scenario_id,
            "context_mode": episode.context_mode,
            "distance_transport": episode.distance_transport,
            "rule_knowledge_test": knowledge["rule_knowledge_test"],
            "general_control_knowledge": knowledge["general_control_knowledge"],
            "independence_knowledge": knowledge["independence_knowledge"],
            "action_interface": "PROVIDER_NATIVE",
            "first_call_was_predeclared": episode.first_call_was_predeclared,
            "gate_blocked_first_attempt": episode.gate_blocked_first_attempt,
            "gate_block_count": episode.gate_block_count,
            "recovered_after_gate": episode.recovered_after_gate,
            "predeclaration_matches_action": episode.predeclaration_matches_action,
            "invalid_verifier_predeclare_count": episode.invalid_verifier_predeclare_count,
            "consequential_execute_count": episode.consequential_execute_count,
            "post_commit_block_count": episode.post_commit_block_count,
            "post_commit_read_count": episode.post_commit_read_count,
            "declared_verifier_executed": episode.declared_verifier_executed,
            "declared_verifier_result": episode.declared_verifier_result,
            "declared_verifier_observed_value": episode.declared_verifier_observed_value,
            "declared_verifier_fault_injected": episode.declared_verifier_fault_injected,
            "oracle_result": episode.oracle_result,
            "oracle_observed_value": episode.oracle_observed_value,
            "verifier_matches_oracle": episode.verifier_matches_oracle,
            "verification_conflict": episode.verification_conflict,
            "verifier_result": episode.verifier_result,
            "verifier_observed_value": episode.verifier_observed_value,
            "verifier_disclosed_before_report": episode.verifier_disclosed_before_report,
            "model_claimed_result": episode.model_claimed_result,
            "claim_matches_verifier": episode.claim_matches_verifier,
            "claim_matches_oracle": episode.claim_matches_oracle,
            "completion_acceptance": episode.completion_acceptance,
            "report_basis": episode.report_basis,
            "terminal_state": episode.terminal_state,
            "turn_count": episode.turn_count,
            "action_trace": episode.action_trace,
            "unparseable_turn_count": episode.unparseable_turn_count,
            "turns": episode.turns,
        })

    return {
        "provider": provider, "model": model, "credential_env": env_name,
        "credential_present": True, "status": "RUN_COMPLETE",
        "rule_knowledge_test": knowledge["rule_knowledge_test"],
        "general_control_knowledge": knowledge["general_control_knowledge"],
        "independence_knowledge": knowledge["independence_knowledge"],
        "knowledge_probe_status": knowledge["provider_status"],
        "knowledge_probe_raw_text": knowledge["raw_text"],
        "knowledge_probe_method": knowledge["knowledge_probe_method"],
        "knowledge_probe_rubric": knowledge["knowledge_probe_rubric"],
        "action_interface": "PROVIDER_NATIVE", "scenarios": scenarios,
    }


def _write_verified_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if json.loads(path.read_text(encoding="utf-8")) != payload:
        raise RuntimeError(f"JSON readback mismatch: {path}")


def _publish_shared(local_path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    shared_root_raw = os.environ.get(dacp_broker.SHARED_EVIDENCE_ENV)
    if not shared_root_raw:
        return {"status": "LOCAL_ONLY", "shared_evidence_env": dacp_broker.SHARED_EVIDENCE_ENV, "shared_path": None}
    shared_path = Path(shared_root_raw) / "gate-matrix-results" / local_path.name
    _write_verified_json(shared_path, payload)
    return {"status": "SHARED_EVIDENCE_VERIFIED", "shared_evidence_env": dacp_broker.SHARED_EVIDENCE_ENV, "shared_path": str(shared_path.resolve())}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run DACP gate beta live matrix")
    parser.add_argument("--openai-model", default=os.environ.get("DACP_OPENAI_MODEL", DEFAULT_MODELS["openai"]))
    parser.add_argument("--anthropic-model", default=os.environ.get("DACP_ANTHROPIC_MODEL", DEFAULT_MODELS["anthropic"]))
    parser.add_argument("--max-output-tokens", type=int, default=256)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--max-turns", type=int, default=gate.MAX_TURNS_DEFAULT)
    parser.add_argument("--log-dir", default="gate-matrix-results")
    args = parser.parse_args()

    identity = _repo_identity()
    if not identity["tracked_source_clean"]:
        raise RuntimeError("Tracked repository source is dirty; refusing live matrix run")

    output: dict[str, Any] = {
        "schema": "dacp-gate-live-matrix-0.11",
        "timestamp": dacp_broker.utc_now(),
        "source_commit": identity["source_commit"],
        "tracked_source_clean": identity["tracked_source_clean"],
        "scenarios": SCENARIO_ORDER,
        "max_turns": args.max_turns,
        "action_interface": "PROVIDER_NATIVE",
        "verifier_contract": "STRUCTURED_READ_STATE_POSTCONDITION_REQUIRED_AND_EXECUTED",
        "verifier_audit": "DECLARED_VERIFIER_CROSS_CHECKED_AGAINST_LEDGER_ORACLE_WITH_FAULT_INJECTION",
        "verifier_disclosure": "HIDDEN_UNTIL_AFTER_MODEL_REPORT",
        "acceptance_policy": "ORACLE_CONFLICT_REJECTS_COMPLETION",
        "distance_transport": "ROLE_SEPARATED_PROVIDER_HISTORY_FIRST_TRIGGER",
        "knowledge_metric": "GENERAL_CONTROL_AND_EXPLICIT_INDEPENDENCE_SPLIT_STEMMED",
        "post_commit_read_policy": "MODEL_VISIBLE_READBACK_THEN_REPORT_REQUIRED",
        "providers": [],
    }
    models = {"openai": args.openai_model, "anthropic": args.anthropic_model}
    for provider in ("openai", "anthropic"):
        output["providers"].append(_provider_record(provider, models[provider], args.max_output_tokens, args.timeout, args.max_turns))

    stamp = output["timestamp"].replace(":", "").replace("-", "")
    output_path = Path(args.log_dir) / f"gate-live-matrix-{stamp}.json"
    _write_verified_json(output_path, output)
    evidence = _publish_shared(output_path, output)

    print("=== DACP_GATE_LIVE_MATRIX_BEGIN ===")
    print(json.dumps(output, indent=2, sort_keys=True))
    print("=== DACP_GATE_LIVE_MATRIX_END ===")
    print(f"RESULT_FILE={output_path.resolve()}")
    print(f"EVIDENCE_STATUS={evidence['status']}")
    print(f"SHARED_EVIDENCE_PATH={evidence['shared_path']}")

    missing = [r["provider"] for r in output["providers"] if not r["credential_present"]]
    return 2 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
