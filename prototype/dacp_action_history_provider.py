#!/usr/bin/env python3
"""Provider-native action adapter for role-separated history replay.

Used only by delayed-distance scenarios. It preserves the same native action tools
as dacp_action_provider while supplying prior user/assistant exchanges through each
provider's native message-history field rather than flattening them into one string.
"""

from __future__ import annotations

import json
import os
import socket
import time
import urllib.error
from typing import Any, Callable

import dacp_action_provider as actions
import dacp_broker


def _canonical_text(action: dict[str, Any]) -> str:
    return json.dumps(action, sort_keys=True, separators=(",", ":"))


def call_openai_action_history(
    messages: list[dict[str, str]],
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
        "instructions": actions.ACTION_SYSTEM,
        "input": [{"role": m["role"], "content": m["content"]} for m in messages],
        "tools": actions._openai_tools(),
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
        action = actions.normalize_native_action(call.get("name"), native_input)
        return dacp_broker.ProviderResult(
            "openai", model, "SUCCEEDED", _canonical_text(action), None, http_status,
            headers.get("x-request-id") or data.get("id"),
            int((time.monotonic() - start) * 1000), data.get("usage"),
            completion_status, completion_reason, data.get("model"),
            {
                "interface_mode": "native_function_tool_role_history",
                "native_tool_name": call.get("name"),
                "native_tool_call_count": len(calls),
                "history_message_count": len(messages),
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
            provider_metadata={"interface_mode": "native_function_tool_role_history"},
        )


def call_anthropic_action_history(
    messages: list[dict[str, str]],
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
        "system": actions.ACTION_SYSTEM,
        "max_tokens": max_output_tokens,
        "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
        "tools": actions._anthropic_tools(),
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
        action = actions.normalize_native_action(call.get("name"), call.get("input"))
        usage = data.get("usage")
        return dacp_broker.ProviderResult(
            "anthropic", model, "SUCCEEDED", _canonical_text(action), None, http_status,
            headers.get("request-id") or data.get("id"),
            int((time.monotonic() - start) * 1000), usage,
            stop_reason, stop_reason, data.get("model"),
            {
                "interface_mode": "native_tool_use_role_history",
                "native_tool_name": call.get("name"),
                "native_tool_call_count": len(calls),
                "history_message_count": len(messages),
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
            provider_metadata={"interface_mode": "native_tool_use_role_history"},
        )


def make_history_provider_call(provider: str, model: str, max_output_tokens: int, timeout: int):
    if provider == "openai":
        return lambda messages: call_openai_action_history(messages, model, max_output_tokens, timeout)
    if provider == "anthropic":
        return lambda messages: call_anthropic_action_history(messages, model, max_output_tokens, timeout)
    raise ValueError(f"unknown provider {provider!r}")
