"""Stripping the chain of thought.

Observed in a real session: the tutor's visible reasoning began "The system
prompt defines my identity... Also instructed to answer the 'who are you'
question plainly". The answer that followed was correct, but the reasoning
announced that the answer was scripted, which is the one thing the system
prompt exists to avoid. Clients can hide thinking locally, but that is the
student's setting to switch off.
"""

import json

import pytest

from gateway.upstream import _is_empty_delta_chunk, mask_body


@pytest.fixture
def hiding(cfg):
    a = cfg.aliases["tutor"]
    return a.__class__(**{**a.__dict__, "hide_reasoning": True})


def response_with_reasoning():
    return {
        "model": "secret-primary:cloud",
        "choices": [
            {
                "index": 0,
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": "I'm the course tutor.",
                    "reasoning": "The system prompt defines my identity; I was instructed to...",
                    "reasoning_details": [{"type": "reasoning.text", "text": "...",
                                           "format": "anthropic-claude-v1"}],
                },
            }
        ],
    }


def test_reasoning_removed_when_hidden():
    masked = mask_body(response_with_reasoning(), "tutor", "id", hide_reasoning=True)
    message = masked["choices"][0]["message"]
    assert "reasoning" not in message
    assert "reasoning_details" not in message
    assert message["content"] == "I'm the course tutor.", "the answer survives"
    assert "system prompt" not in json.dumps(masked)


def test_reasoning_kept_but_normalised_when_not_hidden():
    masked = mask_body(response_with_reasoning(), "tutor", "id", hide_reasoning=False)
    message = masked["choices"][0]["message"]
    assert "reasoning" in message
    assert message["reasoning_details"][0]["format"] == "unknown"


def test_streamed_reasoning_delta_removed():
    chunk = {
        "model": "secret-primary:cloud",
        "choices": [{"index": 0, "delta": {"reasoning": "thinking out loud"}}],
    }
    masked = mask_body(chunk, "tutor", "id", hide_reasoning=True)
    assert masked["choices"][0]["delta"] == {}
    assert "thinking out loud" not in json.dumps(masked)


def test_streamed_content_delta_untouched():
    chunk = {
        "model": "secret-primary:cloud",
        "choices": [{"index": 0, "delta": {"content": "Hello"}}],
    }
    masked = mask_body(chunk, "tutor", "id", hide_reasoning=True)
    assert masked["choices"][0]["delta"] == {"content": "Hello"}


def test_does_not_mutate_upstream_object():
    original = response_with_reasoning()
    mask_body(original, "tutor", "id", hide_reasoning=True)
    assert "reasoning" in original["choices"][0]["message"]


# ---- which chunks become empty and get dropped -----------------------------


def test_reasoning_only_chunk_is_empty_after_stripping():
    chunk = mask_body(
        {"choices": [{"index": 0, "delta": {"reasoning": "hm"}}]},
        "tutor", "id", hide_reasoning=True,
    )
    assert _is_empty_delta_chunk(chunk)


def test_content_chunk_is_not_empty():
    assert not _is_empty_delta_chunk({"choices": [{"delta": {"content": "hi"}}]})


def test_finish_chunk_is_not_empty():
    assert not _is_empty_delta_chunk(
        {"choices": [{"delta": {}, "finish_reason": "stop"}]}
    )


def test_usage_chunk_is_not_empty():
    assert not _is_empty_delta_chunk({"choices": [], "usage": {"total_tokens": 5}})


def test_role_only_chunk_is_treated_as_empty():
    """The opening {"role": "assistant"} delta carries nothing on its own."""
    assert _is_empty_delta_chunk({"choices": [{"delta": {"role": "assistant"}}]})
