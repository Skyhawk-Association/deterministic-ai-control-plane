#!/usr/bin/env python3
"""DACP broker v0: blinded two-provider comparison with deterministic checks.

No retries. No provider sees the other's output. No consequential actions.
Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.request
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OPENAI_URL = "https://api.openai.com/v1/responses"
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
DEFAULT_OPENAI_MODEL = "gpt-5.6-luna"
DEFAULT_ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"
DEFAULT_MAX_OUTPUT_TOKENS = 300
DEFAULT_TIMEOUT_SECONDS = 60


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass
class ProviderResult:
    provider: str
    model: str
    status: str  # SUCCEEDED | FAILED | PENDING
    text: str | None
    error: str | None
    http_status: int | None
    request_id: str | None
    latency_ms: int
    usage: dict[str, Any] | None


def _post_json(
    *,
    url: str,
    headers: dict[str, str],
    payload: dict[str, Any],
    timeout: int,
) -> tuple[dict[str, Any], dict[str, str], int]:
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    request = urllib.request.Request(url, data=body, method="POST")
    for key, value in headers.items():
        request.add_header(key, value)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read().decode("utf-8")
        return json.loads(raw), dict(response.headers.items()), response.status


def _openai_text(data: dict[str, Any]) -> str:
    pieces: list[str] = []
    for item in data.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text" and isinstance(content.get("text"), str):
                pieces.append(content["text"])
    return "".join(pieces)


def _anthropic_text(data: dict[str, Any]) -> str:
    pieces: list[str] = []
    for item in data.get("content", []):
        if item.get("type") == "text" and isinstance(item.get("text"), str):
            pieces.append(item["text"])
    return "".join(pieces)


def call_openai(prompt: str, model: str, max_output_tokens: int, timeout: int) -> ProviderResult:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return ProviderResult("openai", model, "FAILED", None, "OPENAI_API_KEY is not set", None, None, 0, None)

    payload = {
        "model": model,
        "input": prompt,
        "max_output_tokens": max_output_tokens,
        "reasoning": {"effort": "none"},
        "store": False,
    }
    start = time.monotonic()
    try:
        data, headers, status = _post_json(
            url=OPENAI_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            payload=payload,
            timeout=timeout,
        )
        text = _openai_text(data)
        if not text:
            raise ValueError("OpenAI response contained no output_text")
        return ProviderResult(
            "openai",
            model,
            "SUCCEEDED",
            text,
            None,
            status,
            headers.get("x-request-id") or data.get("id"),
            int((time.monotonic() - start) * 1000),
            data.get("usage"),
        )
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:1000]
        return ProviderResult("openai", model, "FAILED", None, f"HTTP {exc.code}: {detail}", exc.code, None, int((time.monotonic() - start) * 1000), None)
    except (TimeoutError, socket.timeout, urllib.error.URLError) as exc:
        # The request may have reached the provider. Do not retry automatically.
        return ProviderResult("openai", model, "PENDING", None, f"Outcome uncertain: {exc}", None, None, int((time.monotonic() - start) * 1000), None)
    except Exception as exc:  # parse/contract failures are explicit failures
        return ProviderResult("openai", model, "FAILED", None, f"{type(exc).__name__}: {exc}", None, None, int((time.monotonic() - start) * 1000), None)


def call_anthropic(prompt: str, model: str, max_output_tokens: int, timeout: int) -> ProviderResult:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return ProviderResult("anthropic", model, "FAILED", None, "ANTHROPIC_API_KEY is not set", None, None, 0, None)

    payload = {
        "model": model,
        "max_tokens": max_output_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    start = time.monotonic()
    try:
        data, headers, status = _post_json(
            url=ANTHROPIC_URL,
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            payload=payload,
            timeout=timeout,
        )
        text = _anthropic_text(data)
        if not text:
            raise ValueError("Anthropic response contained no text block")
        return ProviderResult(
            "anthropic",
            model,
            "SUCCEEDED",
            text,
            None,
            status,
            headers.get("request-id") or data.get("id"),
            int((time.monotonic() - start) * 1000),
            data.get("usage"),
        )
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:1000]
        return ProviderResult("anthropic", model, "FAILED", None, f"HTTP {exc.code}: {detail}", exc.code, None, int((time.monotonic() - start) * 1000), None)
    except (TimeoutError, socket.timeout, urllib.error.URLError) as exc:
        return ProviderResult("anthropic", model, "PENDING", None, f"Outcome uncertain: {exc}", None, None, int((time.monotonic() - start) * 1000), None)
    except Exception as exc:
        return ProviderResult("anthropic", model, "FAILED", None, f"{type(exc).__name__}: {exc}", None, None, int((time.monotonic() - start) * 1000), None)


def classify(results: list[ProviderResult], expected_exact: str | None) -> tuple[str, dict[str, Any]]:
    by_provider = {result.provider: result for result in results}
    if any(result.status != "SUCCEEDED" for result in results):
        return "UNRESOLVED", {"reason": "one_or_more_provider_calls_not_succeeded"}

    openai_text = (by_provider["openai"].text or "").strip()
    anthropic_text = (by_provider["anthropic"].text or "").strip()

    if expected_exact is not None:
        expected = expected_exact.strip()
        checks = {
            "comparison_mode": "strip_exact",
            "openai_matches_expected": openai_text == expected,
            "anthropic_matches_expected": anthropic_text == expected,
        }
        if checks["openai_matches_expected"] and checks["anthropic_matches_expected"]:
            return "VERIFIED_MATCH", checks
        return "DISAGREEMENT", checks

    if openai_text == anthropic_text:
        return "SUPPORTED_AGREEMENT", {"comparison_mode": "strip_exact_between_models"}
    return "DISAGREEMENT", {"comparison_mode": "strip_exact_between_models"}


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def run(args: argparse.Namespace) -> int:
    if bool(args.prompt) == bool(args.prompt_file):
        raise SystemExit("Provide exactly one of --prompt or --prompt-file")

    prompt = args.prompt if args.prompt is not None else Path(args.prompt_file).read_text(encoding="utf-8")
    run_id = f"dacp-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    audit_path = Path(args.log_dir) / f"{run_id}.jsonl"

    start_record = {
        "event": "run_started",
        "run_id": run_id,
        "timestamp": utc_now(),
        "input_sha256": sha256_text(prompt),
        "input_chars": len(prompt),
        "openai_model": args.openai_model,
        "anthropic_model": args.anthropic_model,
        "max_output_tokens": args.max_output_tokens,
        "timeout_seconds": args.timeout,
        "independence": "both provider calls dispatched before either result is consumed",
        "automatic_retries": 0,
        "consequential_actions": False,
    }
    append_jsonl(audit_path, start_record)

    if args.dry_run:
        append_jsonl(audit_path, {"event": "dry_run_complete", "run_id": run_id, "timestamp": utc_now()})
        print(json.dumps({"run_id": run_id, "status": "DRY_RUN", "audit": str(audit_path)}, indent=2))
        return 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [
            pool.submit(call_openai, prompt, args.openai_model, args.max_output_tokens, args.timeout),
            pool.submit(call_anthropic, prompt, args.anthropic_model, args.max_output_tokens, args.timeout),
        ]
        results = [future.result() for future in futures]

    for result in results:
        append_jsonl(
            audit_path,
            {
                "event": "provider_result",
                "run_id": run_id,
                "timestamp": utc_now(),
                **asdict(result),
            },
        )

    terminal_state, verification = classify(results, args.expect_exact)
    terminal_record = {
        "event": "run_completed",
        "run_id": run_id,
        "timestamp": utc_now(),
        "terminal_state": terminal_state,
        "verification": verification,
    }
    append_jsonl(audit_path, terminal_record)

    summary = {
        "run_id": run_id,
        "terminal_state": terminal_state,
        "input_sha256": start_record["input_sha256"],
        "providers": {result.provider: result.status for result in results},
        "verification": verification,
        "audit": str(audit_path),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if terminal_state in {"VERIFIED_MATCH", "SUPPORTED_AGREEMENT"} else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Minimal blinded OpenAI/Anthropic DACP broker experiment")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--prompt", help="Task/evidence package sent identically to both providers")
    source.add_argument("--prompt-file", help="UTF-8 file containing the task/evidence package")
    parser.add_argument("--expect-exact", help="Optional deterministic expected answer; compared after strip()")
    parser.add_argument("--openai-model", default=os.environ.get("OPENAI_MODEL", DEFAULT_OPENAI_MODEL))
    parser.add_argument("--anthropic-model", default=os.environ.get("ANTHROPIC_MODEL", DEFAULT_ANTHROPIC_MODEL))
    parser.add_argument("--max-output-tokens", type=int, default=DEFAULT_MAX_OUTPUT_TOKENS)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--log-dir", default="runs")
    parser.add_argument("--dry-run", action="store_true", help="Write audit preconditions without making API calls")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.max_output_tokens < 1:
        raise SystemExit("--max-output-tokens must be >= 1")
    if args.timeout < 1:
        raise SystemExit("--timeout must be >= 1")
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
