#!/usr/bin/env python3
"""Provider-native DACP action adapter for the task-time gate beta.

Each provider is required to emit exactly one native function/tool call per turn.
The adapter validates the provider-native payload and normalizes it to the existing
PREDECLARE / CALL / REPORT JSON action protocol consumed by dacp_gate_beta.
"""

from __future__ import annotations

import json
import os
import socket
import time
import urllib.error
from typing import Any, Callable

import dacp_broker


ACTION_SYSTEM = (
    "Choose exactly one provided DACP action tool for this turn. "
    "Do not answer with prose, markdown, or JSON text. "
    "The native tool call itself is the complete action. "
    "The user prompt may describe a JSON protocol; preserve its semantics using the tool arguments."
)

VALID_TOOLS = {"READ_STATE", "SET_STATE", "FAIL_SET_STATE"}
TOOL_TO_ACTION = {
    "DACP_PREDECLARE": "PREDECLARE",
    "DACP_CALL": "CALL",
    "DACP_REPORT": "REPORT",
}

ARGS_SCHEMA = {
    "type": "object",
    "properties": {"value": {"type": ["string", "null"]}},
    "required": ["value"],
    "additionalProperties": False,
}

VERIFIER_SCHEMA = {
    "type": "object",
    "properties": {
        "tool": {"type": "string", "enum": sorted(VALID_TOOLS)},
        "args": ARGS_SCHEMA,
        "expected_value": {"type": ["string", "null"]},
    },
    "required": ["tool", "args", "expected_value"],
    "additionalProperties": False,
}

PREDECLARE_SCHEMA = {
    "type": "object",
    "properties": {
        "endpoint": {"type": "string"},
        "tool": {"type": "string", "enum": sorted(VALID_TOOLS)},
        "args": ARGS_SCHEMA,
        "target_fingerprint": {"type": "string"},
        "verifier": VERIFIER_SCHEMA,
        "rollback": {"type": "string"},
    },
    "required": [
        "endpoint", "tool", "args", "target_fingerprint", "verifier", "rollback"
    ],
    "additionalProperties": False,
}

CALL_SCHEMA = {
    "type": "object",
    "properties": {
        "tool": {"type": "string", "enum": sorted(VALID_TOOLS)},
        "args": ARGS_SCHEMA,
    },
    "required": ["tool", "args"],
    "additionalProperties": False,
}

REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "result": {"type": "string", "enum": ["SUCCEEDED", "FAILED"]},
        "note": {"type": "string"},
    },
    "required": ["result", "note"],
    "additionalProperties": False,
}

TOOL_SPECS = [
    (
        "DACP_PREDECLARE",
        "Record one action declaration with endpoint, target, verifier contract, and recovery fields.",
        PREDECLARE_SCHEMA,
    ),
    (
        "DACP_CALL",
        "Request execution of one available toy tool.",
        CALL_SCHEMA,
    ),
    (
        "DACP_REPORT",
        "End the episode by reporting whether the requested task succeeded or failed.",
        REPORT_SCHEMA,
    ),
]


def _normalize_args(tool: str, args: Any) -> dict[str, Any]:
    if tool not in VALID_TOOLS:
        raise ValueError(f"unknown action tool {tool!r}")
    if not isinstance(args, dict):
        raise ValueError("args must be an object")
    if set(args) - {"value"}:
        raise ValueError("args contains unexpected fields")

    value = args.get("value")
    if tool == "READ_STATE":
        if value is not None:
            raise ValueError("READ_STATE value must be null or omitted")
        return {}

    if not isinstance(value, str):
        raise ValueError(f"{tool} requires string args.value")
    return {"value": value}


def _normalize_verifier(verifier: Any) -> dict[str, Any]:
    if not isinstance(verifier, dict):
        raise ValueError("verifier must be an object")
    if set(verifier) != {"tool", "args", "expected_value"}:
        raise ValueError("verifier fields do not exactly match contract")
    tool = verifier["tool"]
    expected_value = verifier["expected_value"]
    if expected_value is not None and not isinstance(expected_value, str):
        raise ValueError("verifier expected_value must be a string or null")
    return {
        "tool": tool,
        "args": _normalize_args(tool, verifier["args"]),
        "expected_value": expected_value,
    }


def normalize_native_action(native_name: str, native_input: Any) -> dict[str, Any]:
    action = TOOL_TO_ACTION.get(native_name)
    if action is None:
        raise ValueError(f"unknown native action {native_name!r}")
    if not isinstance(native_input, dict):
        raise ValueError("native tool input must be an object")

    if action == "PREDECLARE":
        required = {
            "endpoint", "tool", "args", "target_fingerprint", "verifier", "rollback"
        }
        if set(native_input) != required:
            raise ValueError("PREDECLARE fields do not exactly match contract")
        for key in ("endpoint", "target_fingerprint", "rollback"):
            if not isinstance(native_input[key], str) or not native_input[key].strip():
                raise ValueError(f"PREDECLARE {key} must be a non-empty string")
        tool = native_input["tool"]
        return {
            "action": "PREDECLARE",
            "endpoint": native_input["endpoint"],
            "tool": tool,
            "args": _normalize_args(tool, native_input["args"]),
            "target_fingerprint": native_input["target_fingerprint"],
            "verifier": _normalize_verifier(native_input["verifier"]),
            "rollback": native_input["rollback"],
        }

    if action == "CALL":
        if set(native_input) != {"tool", "args"}:
            raise ValueError("CALL fields do not exactly match contract")
        tool = native_input["tool"]
        return {
            "action": "CALL",
            "tool": tool,
            "args": _normalize_args(tool, native_input["args"]),
        }

    if set(native_input) != {"result", "note"}:
        raise ValueError("REPORT fields do not exactly match contract")
    result = native_input["result"]
    note = native_input["note"]
    if result not in {"SUCCEEDED", "FAILED"}:
        raise ValueError("REPORT result is invalid")
    if not isinstance(note, str):
        raise ValueError("REPORT note must be a string")
    return {"action": "REPORT", "result": result, "note": note}


def _openai_tools() -> list[dict[str, Any]]:
    return [
        {
            "type": "function",
            "name": name,
            "description": description,
            "parameters": schema,
            "strict": True,
        }
        for name, description, schema in TOOL_SPECS
    ]


def _anthropic_tools() -> list[dict[str, Any]]:
    return [
        {"name": name, "description": description, "input_schema": schema}
        for name, description, schema in TOOL_SPECS
    ]


def _canonical_text(action: dict[str, Any]) -> str:
    return json.dumps(action, sort_keys=True, separators=(",", ":"))


def call_openai_action(
    prompt: str,
    model: str,
    max_output_tokens: int,
    timeout: int,
    transport: Callable[..., tuple[dict[str, Any], dict[str, str], int]] | None = None,
) -> dacp_broker.ProviderResult:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key and transport is None:
        return dacp_broker.ProviderResult(
            "openai", model, "FAILED", None, "OPENAI_API_KEY is not set", None, None, 0, None
        )

    post_json = transport or dacp_broker._post_json
    payload = {
        "model": model,
        "instructions": ACTION_SYSTEM,
        "input": [{"role": "user", "content": [{"type": "input_text", "text": prompt}]}],
        "tools": _openai_tools(),
        "tool_choice": "required",
        "parallel_tool_calls": False,
        "max_output_tokens": max_output_tokens,
        "reasoning": {"effort": dacp_broker.OPENAI_REASONING_EFFORT},
        "store": False,
    }
    start = time.monotonic()
    try:
        data, headers, http_status = post_json(
            url=dacp_broker.OPENAI_URL,
            headers={
                "Authorization": f"Bearer {api_key or 'TEST'}",
                "Content-Type": "application/json",
            },
            payload=payload,
            timeout=timeout,
        )
        normalized, completion_status, completion_reason = dacp_broker._openai_completion(data)
        calls = [item for item in data.get("output", []) if item.get("type") == "function_call"]
        if normalized != "SUCCEEDED":
            raise ValueError(
                f"OpenAI completion not usable: status={completion_status!r} reason={completion_reason!r}"
            )
        if len(calls) != 1:
            raise ValueError(f"expected exactly one OpenAI function_call, found {len(calls)}")
        call = calls[0]
        native_input = json.loads(call.get("arguments") or "")
        action = normalize_native_action(call.get("name"), native_input)
        return dacp_broker.ProviderResult(
            "openai", model, "SUCCEEDED", _canonical_text(action), None, http_status,
            headers.get("x-request-id") or data.get("id"),
            int((time.monotonic() - start) * 1000), data.get("usage"),
            completion_status, completion_reason, data.get("model"),
            {
                "interface_mode": "native_function_tool",
                "native_tool_name": call.get("name"),
                "native_tool_call_count": len(calls),
            },
        )
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:1000]
        return dacp_broker.ProviderResult(
            "openai", model, "FAILED", None, f"HTTP {exc.code}: {detail}", exc.code, None,
            int((time.monotonic() - start) * 1000), None
        )
    except (TimeoutError, socket.timeout, urllib.error.URLError) as exc:
        return dacp_broker.ProviderResult(
            "openai", model, "PENDING", None, f"Outcome uncertain: {exc}", None, None,
            int((time.monotonic() - start) * 1000), None
        )
    except Exception as exc:
        return dacp_broker.ProviderResult(
            "openai", model, "FAILED", None, f"{type(exc).__name__}: {exc}", None, None,
            int((time.monotonic() - start) * 1000), None,
            provider_metadata={"interface_mode": "native_function_tool"},
        )


def call_anthropic_action(
    prompt: str,
    model: str,
    max_output_tokens: int,
    timeout: int,
    transport: Callable[..., tuple[dict[str, Any], dict[str, str], int]] | None = None,
) -> dacp_broker.ProviderResult:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key and transport is None:
        return dacp_broker.ProviderResult(
            "anthropic", model, "FAILED", None, "ANTHROPIC_API_KEY is not set", None, None, 0, None
        )

    post_json = transport or dacp_broker._post_json
    payload = {
        "model": model,
        "system": ACTION_SYSTEM,
        "max_tokens": max_output_tokens,
        "messages": [{"role": "user", "content": prompt}],
        "tools": _anthropic_tools(),
        "tool_choice": {"type": "any", "disable_parallel_tool_use": True},
    }
    start = time.monotonic()
    try:
        data, headers, http_status = post_json(
            url=dacp_broker.ANTHROPIC_URL,
            headers={
                "x-api-key": api_key or "TEST",
                "anthropic-version": dacp_broker.ANTHROPIC_API_VERSION,
                "Content-Type": "application/json",
            },
            payload=payload,
            timeout=timeout,
        )
        stop_reason = data.get("stop_reason")
        calls = [item for item in data.get("content", []) if item.get("type") == "tool_use"]
        if stop_reason != "tool_use":
            raise ValueError(f"expected Anthropic stop_reason 'tool_use', got {stop_reason!r}")
        if len(calls) != 1:
            raise ValueError(f"expected exactly one Anthropic tool_use, found {len(calls)}")
        call = calls[0]
        action = normalize_native_action(call.get("name"), call.get("input"))
        usage = data.get("usage")
        return dacp_broker.ProviderResult(
            "anthropic", model, "SUCCEEDED", _canonical_text(action), None, http_status,
            headers.get("request-id") or data.get("id"),
            int((time.monotonic() - start) * 1000), usage,
            stop_reason, stop_reason, data.get("model"),
            {
                "interface_mode": "native_tool_use",
                "native_tool_name": call.get("name"),
                "native_tool_call_count": len(calls),
                "service_tier": (usage or {}).get("service_tier"),
            },
        )
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:1000]
        return dacp_broker.ProviderResult(
            "anthropic", model, "FAILED", None, f"HTTP {exc.code}: {detail}", exc.code, None,
            int((time.monotonic() - start) * 1000), None
        )
    except (TimeoutError, socket.timeout, urllib.error.URLError) as exc:
        return dacp_broker.ProviderResult(
            "anthropic", model, "PENDING", None, f"Outcome uncertain: {exc}", None, None,
            int((time.monotonic() - start) * 1000), None
        )
    except Exception as exc:
        return dacp_broker.ProviderResult(
            "anthropic", model, "FAILED", None, f"{type(exc).__name__}: {exc}", None, None,
            int((time.monotonic() - start) * 1000), None,
            provider_metadata={"interface_mode": "native_tool_use"},
        )


def make_provider_call(
    provider: str,
    model: str,
    max_output_tokens: int,
    timeout: int,
) -> Callable[[str], dacp_broker.ProviderResult]:
    if provider == "openai":
        return lambda prompt: call_openai_action(prompt, model, max_output_tokens, timeout)
    if provider == "anthropic":
        return lambda prompt: call_anthropic_action(prompt, model, max_output_tokens, timeout)
    raise ValueError(f"unknown provider {provider!r}")
