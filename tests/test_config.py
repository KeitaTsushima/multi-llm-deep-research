"""Unit tests for config.py."""

import os
from unittest.mock import patch

import pytest

from mldr.core.config import (
    Config,
    ModelConfig,
    default_config,
    get_env_var_name,
    load_api_keys,
)


class TestLoadApiKeys:
    """Tests for load_api_keys()."""

    def test_returns_empty_dict_when_no_env_vars_set(self) -> None:
        """Returns empty dict when no API keys are set."""
        with patch.dict(os.environ, {}, clear=True):
            keys = load_api_keys()
            assert keys == {}

    def test_loads_single_api_key(self) -> None:
        """Loads a single API key from environment."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test123"}, clear=True):
            keys = load_api_keys()
            assert keys == {"gpt": "sk-test123"}

    def test_loads_multiple_api_keys(self) -> None:
        """Loads multiple API keys from environment."""
        env = {
            "OPENAI_API_KEY": "sk-openai",
            "ANTHROPIC_API_KEY": "sk-anthropic",
        }
        with patch.dict(os.environ, env, clear=True):
            keys = load_api_keys()
            assert keys == {"gpt": "sk-openai", "claude": "sk-anthropic"}

    def test_ignores_whitespace_only_values(self) -> None:
        """Ignores API keys that are whitespace-only."""
        env = {
            "OPENAI_API_KEY": "   ",
            "ANTHROPIC_API_KEY": "sk-valid",
        }
        with patch.dict(os.environ, env, clear=True):
            keys = load_api_keys()
            assert keys == {"claude": "sk-valid"}

    def test_ignores_empty_string_values(self) -> None:
        """Ignores API keys that are empty strings."""
        env = {
            "OPENAI_API_KEY": "",
            "ANTHROPIC_API_KEY": "sk-valid",
        }
        with patch.dict(os.environ, env, clear=True):
            keys = load_api_keys()
            assert keys == {"claude": "sk-valid"}

    def test_strips_whitespace_from_values(self) -> None:
        """Strips leading/trailing whitespace from API keys."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "  sk-test  "}, clear=True):
            keys = load_api_keys()
            assert keys == {"gpt": "sk-test"}


class TestGetEnvVarName:
    """Tests for get_env_var_name()."""

    def test_returns_correct_env_var_for_gpt(self) -> None:
        assert get_env_var_name("gpt") == "OPENAI_API_KEY"

    def test_returns_correct_env_var_for_claude(self) -> None:
        assert get_env_var_name("claude") == "ANTHROPIC_API_KEY"

    def test_returns_correct_env_var_for_gemini(self) -> None:
        assert get_env_var_name("gemini") == "GOOGLE_API_KEY"

    def test_returns_correct_env_var_for_perplexity(self) -> None:
        assert get_env_var_name("perplexity") == "PERPLEXITY_API_KEY"

    def test_returns_correct_env_var_for_grok(self) -> None:
        assert get_env_var_name("grok") == "GROK_API_KEY"


class TestDefaultConfig:
    """Tests for default_config()."""

    def test_returns_config_instance(self) -> None:
        """Returns a Config instance."""
        config = default_config()
        assert isinstance(config, Config)

    def test_primary_models_contains_gpt_and_claude(self) -> None:
        """Default primary_models contains GPT and Claude."""
        config = default_config()
        assert config.primary_models == ["gpt", "claude"]

    def test_chairman_model_is_gpt(self) -> None:
        """Default chairman_model is GPT."""
        config = default_config()
        assert config.chairman_model == "gpt"

    def test_gpt_and_claude_are_enabled(self) -> None:
        """GPT and Claude are enabled by default."""
        config = default_config()
        assert config.gpt.enabled is True
        assert config.claude.enabled is True

    def test_other_models_are_disabled(self) -> None:
        """Gemini, Perplexity, Grok are disabled by default."""
        config = default_config()
        assert config.gemini.enabled is False
        assert config.perplexity.enabled is False
        assert config.grok.enabled is False

    def test_returns_new_instance_each_call(self) -> None:
        """Returns a new Config instance on each call."""
        config1 = default_config()
        config2 = default_config()
        assert config1 is not config2


class TestConfigValidation:
    """Tests for Config validation in __post_init__."""

    def test_raises_error_when_primary_models_empty(self) -> None:
        """Raises ValueError when primary_models is empty."""
        with pytest.raises(ValueError, match="must contain at least one model"):
            Config(primary_models=[])

    def test_raises_error_when_chairman_not_in_primary_models(self) -> None:
        """Raises ValueError when chairman_model not in primary_models."""
        with pytest.raises(ValueError, match="must be included in primary_models"):
            Config(primary_models=["claude"], chairman_model="gpt")

    def test_valid_config_does_not_raise(self) -> None:
        """Valid configuration does not raise."""
        config = Config(primary_models=["gpt", "claude"], chairman_model="gpt")
        assert config.chairman_model == "gpt"


class TestConfigGetModelConfig:
    """Tests for Config.get_model_config()."""

    def test_returns_correct_model_config_for_gpt(self) -> None:
        """Returns the correct ModelConfig for GPT."""
        config = default_config()
        gpt_config = config.get_model_config("gpt")
        assert isinstance(gpt_config, ModelConfig)
        assert gpt_config.enabled is True
        assert gpt_config.model_name == "gpt-4o"

    def test_returns_correct_model_config_for_claude(self) -> None:
        """Returns the correct ModelConfig for Claude."""
        config = default_config()
        claude_config = config.get_model_config("claude")
        assert isinstance(claude_config, ModelConfig)
        assert claude_config.enabled is True
        assert claude_config.model_name == "claude-sonnet-4-20250514"

    def test_raises_key_error_for_unknown_model_id(self) -> None:
        """Raises KeyError for unknown model ID."""
        config = default_config()
        with pytest.raises(KeyError, match="Unknown model_id"):
            config.get_model_config("unknown")  # type: ignore[arg-type]


class TestModelConfig:
    """Tests for ModelConfig dataclass."""

    def test_default_timeout_is_600(self) -> None:
        """Default timeout_sec is 600 seconds."""
        config = ModelConfig(enabled=True, model_name="test-model")
        assert config.timeout_sec == 600

    def test_custom_timeout(self) -> None:
        """Can set custom timeout_sec."""
        config = ModelConfig(enabled=True, model_name="test-model", timeout_sec=300)
        assert config.timeout_sec == 300
