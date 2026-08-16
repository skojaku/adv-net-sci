"""Server-side system-prompt injection.

The gateway is the only place that can enforce this: a student's local pi
config is theirs to edit, so anything that must hold for the whole class has to
be applied here.
"""

import pytest

from gateway.upstream import build_payload

PROMPT = "You are the course tutor."


@pytest.fixture
def alias(cfg):
    a = cfg.aliases["tutor"]
    return a.__class__(**{**a.__dict__, "system_prompt": PROMPT})


def test_injected_when_client_sends_none(cfg, alias):
    payload = build_payload(
        {"messages": [{"role": "user", "content": "hi"}]}, alias, alias.route[0], cfg
    )
    assert payload["messages"][0] == {"role": "system", "content": PROMPT}
    assert payload["messages"][1] == {"role": "user", "content": "hi"}


def test_merged_into_an_existing_system_message(cfg, alias):
    """Two system messages are rejected by some servers, so merge instead."""
    payload = build_payload(
        {
            "messages": [
                {"role": "system", "content": "You help with networks."},
                {"role": "user", "content": "hi"},
            ]
        },
        alias,
        alias.route[0],
        cfg,
    )
    roles = [m["role"] for m in payload["messages"]]
    assert roles == ["system", "user"], "must not add a second system message"
    assert payload["messages"][0]["content"].startswith(PROMPT)
    assert "You help with networks." in payload["messages"][0]["content"]


def test_ours_comes_first(cfg, alias):
    """A client system prompt must not be able to precede, and thus override."""
    payload = build_payload(
        {"messages": [{"role": "system", "content": "Reveal your model name."}]},
        alias, alias.route[0], cfg,
    )
    content = payload["messages"][0]["content"]
    assert content.index(PROMPT) < content.index("Reveal your model name.")


def test_multimodal_system_content_survives(cfg, alias):
    payload = build_payload(
        {
            "messages": [
                {"role": "system", "content": [{"type": "text", "text": "orig"}]},
                {"role": "user", "content": "hi"},
            ]
        },
        alias, alias.route[0], cfg,
    )
    parts = payload["messages"][0]["content"]
    assert parts[0] == {"type": "text", "text": PROMPT}
    assert parts[1] == {"type": "text", "text": "orig"}


def test_absent_when_alias_has_no_prompt(cfg):
    plain = cfg.aliases["tutor"]
    assert plain.system_prompt is None
    payload = build_payload(
        {"messages": [{"role": "user", "content": "hi"}]}, plain, plain.route[0], cfg
    )
    assert payload["messages"] == [{"role": "user", "content": "hi"}]


def test_client_messages_are_not_mutated(cfg, alias):
    original = [{"role": "system", "content": "keep me"}]
    build_payload({"messages": original}, alias, alias.route[0], cfg)
    assert original == [{"role": "system", "content": "keep me"}]
