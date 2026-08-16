"""The alias must be the only model name a client can observe."""

import json

from conftest import assert_no_leak

from gateway.upstream import ALLOWED_FIELDS, build_payload, mask_body


def test_mask_rewrites_model_and_id(cfg):
    upstream = {
        "id": "gen-1234-openrouter",
        "model": "secret-vendor/secret-fallback",
        "provider": "SecretVendor",
        "system_fingerprint": "fp_secret",
        "choices": [{"index": 0, "message": {"role": "assistant", "content": "hi"}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15,
                  "cost": 0.0004},
    }
    masked = mask_body(upstream, "tutor", "chatcmpl-abc")

    assert masked["model"] == "tutor"
    assert masked["id"] == "chatcmpl-abc"
    assert "provider" not in masked
    assert "system_fingerprint" not in masked
    # The dollar cost is a price list away from naming the model.
    assert "cost" not in masked["usage"]
    assert masked["usage"]["total_tokens"] == 15
    assert_no_leak(json.dumps(masked))


def test_mask_normalises_reasoning_format(cfg):
    """`reasoning_details[].format` names the provider's reasoning dialect."""
    upstream = {
        "model": "secret-vendor/secret-fallback",
        "choices": [
            {
                "index": 0,
                "message": {
                    "content": None,
                    "reasoning": "thinking...",
                    "reasoning_details": [
                        {"type": "reasoning.text", "text": "hm", "format": "anthropic-claude-v1"}
                    ],
                },
            }
        ],
    }
    masked = mask_body(upstream, "tutor", "chatcmpl-abc")
    details = masked["choices"][0]["message"]["reasoning_details"][0]
    assert details["format"] == "unknown"
    assert details["text"] == "hm", "the reasoning itself is left alone"
    assert "anthropic" not in json.dumps(masked)
    # The upstream object must not be edited in place.
    assert upstream["choices"][0]["message"]["reasoning_details"][0]["format"] == (
        "anthropic-claude-v1"
    )


def test_mask_normalises_reasoning_format_in_stream_delta(cfg):
    upstream = {
        "model": "secret-primary:cloud",
        "choices": [
            {"index": 0, "delta": {"reasoning_details": [{"format": "openai-responses-v1"}]}}
        ],
    }
    masked = mask_body(upstream, "tutor", "chatcmpl-abc")
    assert masked["choices"][0]["delta"]["reasoning_details"][0]["format"] == "unknown"


def test_mask_leaves_plain_choices_alone(cfg):
    upstream = {
        "model": "secret-primary:cloud",
        "choices": [{"index": 0, "message": {"role": "assistant", "content": "hi"}}],
    }
    masked = mask_body(upstream, "tutor", "chatcmpl-abc")
    assert masked["choices"][0]["message"] == {"role": "assistant", "content": "hi"}


def test_mask_does_not_mutate_input(cfg):
    upstream = {"model": "secret-primary:cloud", "provider": "x"}
    mask_body(upstream, "tutor", "chatcmpl-abc")
    assert upstream["model"] == "secret-primary:cloud"


def test_payload_uses_real_model_upstream(cfg):
    alias = cfg.aliases["tutor"]
    payload = build_payload({"messages": [{"role": "user", "content": "hi"}]},
                            alias, alias.route[0], cfg)
    assert payload["model"] == "secret-primary:cloud"


def test_payload_drops_openrouter_escape_hatches(cfg):
    """A student must not be able to name their own model through us.

    OpenRouter honours `models` and `provider` in the request body, so a
    passthrough proxy would let anyone route around the alias entirely.
    """
    alias = cfg.aliases["tutor"]
    payload = build_payload(
        {
            "messages": [{"role": "user", "content": "hi"}],
            "models": ["openai/gpt-5", "anthropic/claude-opus-5"],
            "provider": {"order": ["OpenAI"]},
            "route": "fallback",
            "transforms": [],
        },
        alias,
        alias.route[1],
        cfg,
    )
    assert "models" not in payload
    assert "provider" not in payload
    assert "route" not in payload
    assert "transforms" not in payload
    assert payload["model"] == "secret-vendor/secret-fallback"


def test_payload_clamps_max_tokens(cfg):
    alias = cfg.aliases["tutor"]  # alias max_tokens 2048, server cap 4096
    payload = build_payload(
        {"messages": [], "max_tokens": 999999}, alias, alias.route[0], cfg
    )
    assert payload["max_tokens"] == 2048

    payload = build_payload({"messages": []}, alias, alias.route[0], cfg)
    assert payload["max_tokens"] == 2048, "absent max_tokens still gets a ceiling"

    payload = build_payload(
        {"messages": [], "max_tokens": 100}, alias, alias.route[0], cfg
    )
    assert payload["max_tokens"] == 100, "a modest request is left alone"


def test_payload_requests_stream_usage(cfg):
    alias = cfg.aliases["tutor"]
    payload = build_payload(
        {"messages": [], "stream": True}, alias, alias.route[0], cfg
    )
    assert payload["stream_options"] == {"include_usage": True}

    payload = build_payload({"messages": []}, alias, alias.route[0], cfg)
    assert "stream_options" not in payload


def test_allowlist_covers_what_pi_sends():
    # Guard against someone trimming the allowlist and quietly breaking tools.
    for field in ("messages", "temperature", "tools", "tool_choice", "stream",
                  "response_format", "reasoning_effort", "stop", "seed"):
        assert field in ALLOWED_FIELDS
