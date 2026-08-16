import textwrap

import pytest

from gateway.config import load_config

# A config with two hops on the primary alias, so fallback is exercisable, and
# real-looking model names so a leak in a test failure is obvious.
CONFIG_YAML = """
server:
  first_token_timeout_s: 2
  request_timeout_s: 10
  max_concurrent_per_student: 2
  max_tokens_per_request: 4096

quota:
  period: term
  term_start: "2020-01-01"
  timezone: "UTC"
  default: { requests: 3, total_tokens: 1000 }
  overrides:
    rich-student: { requests: 100, total_tokens: 100000 }

providers:
  ollama:
    base_url: "https://ollama.test/v1"
    api_key_env: TEST_OLLAMA_KEY
  openrouter:
    base_url: "https://openrouter.test/api/v1"
    api_key_env: TEST_OPENROUTER_KEY
    extra_headers: { X-Title: "test" }

aliases:
  tutor:
    name: "Course Tutor"
    max_tokens: 2048
    route:
      - { provider: ollama, model: "secret-primary:cloud" }
      - { provider: openrouter, model: "secret-vendor/secret-fallback" }
  solo:
    route:
      - { provider: openrouter, model: "secret-vendor/secret-only" }

pricing:
  "openrouter:secret-vendor/secret-fallback": { input: 1.0, output: 2.0 }
"""

ENV = {"TEST_OLLAMA_KEY": "k-ollama", "TEST_OPENROUTER_KEY": "k-openrouter"}

# Every real model string in the config. Responses are asserted against this.
SECRETS = [
    "secret-primary:cloud",
    "secret-vendor/secret-fallback",
    "secret-vendor/secret-only",
    "ollama",
    "openrouter",
]


@pytest.fixture
def config_path(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text(textwrap.dedent(CONFIG_YAML))
    return path


@pytest.fixture
def cfg(config_path):
    return load_config(config_path, env=ENV)


def assert_no_leak(blob: str) -> None:
    """No real model or provider name may appear in anything client-facing."""
    for secret in SECRETS:
        assert secret not in blob, f"leaked {secret!r} in: {blob[:400]}"
