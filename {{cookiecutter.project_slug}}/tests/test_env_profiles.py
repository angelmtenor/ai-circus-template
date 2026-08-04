"""
test_env_profiles.py
--------------------

Tests for the environment-aware configuration loading.

Author: {{cookiecutter.author_name}}
"""

from __future__ import annotations

import pytest

from {{cookiecutter.package_name}}.data_model import get_env_config


@pytest.fixture(autouse=True)
def _prepare_env() -> None:
    """Clear the lru_cache before each test."""
    get_env_config.cache_clear()


def test_get_env_config_default_local(monkeypatch: pytest.MonkeyPatch) -> None:
    """With no APP_ENVIRONMENT set, the 'local' profile (base defaults) is used."""
    monkeypatch.delenv("APP_ENVIRONMENT", raising=False)

    config = get_env_config()

    assert config.LOG_LEVEL == "INFO"
    assert config.EXAMPLE_SERVICE_BASE_URL == "https://httpbin.org"


@pytest.mark.parametrize("profile", ["local", "staging", "production"])
def test_get_env_config_reads_app_environment(monkeypatch: pytest.MonkeyPatch, profile: str) -> None:
    """APP_ENVIRONMENT selects the active profile (all profiles currently fall back to base defaults)."""
    monkeypatch.setenv("APP_ENVIRONMENT", profile)

    config = get_env_config()

    assert config.LOG_LEVEL == "INFO"


def test_get_env_config_explicit_env_overrides_app_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """An explicit `env=` argument takes priority over the APP_ENVIRONMENT variable."""
    monkeypatch.setenv("APP_ENVIRONMENT", "production")

    config = get_env_config(env="staging")

    assert config.LOG_LEVEL == "INFO"
