"""Configuration definitions for multi-llm-deep-research."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Literal

# Model identifiers supported by the pipeline
# NOTE: v1.x will migrate to Enum or registry pattern for extensibility
ModelId = Literal["gpt", "claude", "gemini", "perplexity", "grok"]

# Environment variable names for each model's API key
_API_KEY_ENV_VARS: dict[ModelId, str] = {
    "gpt": "OPENAI_API_KEY",
    "claude": "ANTHROPIC_API_KEY",
    "gemini": "GOOGLE_API_KEY",
    "perplexity": "PERPLEXITY_API_KEY",
    "grok": "GROK_API_KEY",
}


@dataclass
class ModelConfig:
    """User-facing model configuration.

    NOTE: Runtime parameters (max_tokens, temperature, retry policy)
    will NOT be added here to avoid config bloat. Those belong in
    a separate defaults module (planned for v1.x).
    """

    enabled: bool
    model_name: str
    timeout_sec: int = 600


@dataclass
class Config:
    """Application configuration with all model configs."""

    primary_models: list[ModelId]
    chairman_model: ModelId = "gpt"

    # Named fields for each model (type-safe access)
    gpt: ModelConfig = field(
        default_factory=lambda: ModelConfig(enabled=True, model_name="gpt-4o")
    )
    claude: ModelConfig = field(
        default_factory=lambda: ModelConfig(
            enabled=True, model_name="claude-sonnet-4-20250514"
        )
    )
    gemini: ModelConfig = field(
        default_factory=lambda: ModelConfig(enabled=False, model_name="gemini-1.5-pro")
    )
    perplexity: ModelConfig = field(
        default_factory=lambda: ModelConfig(enabled=False, model_name="sonar-pro")
    )
    grok: ModelConfig = field(
        default_factory=lambda: ModelConfig(enabled=False, model_name="grok-2")
    )

    def __post_init__(self) -> None:
        """Validate configuration consistency."""
        if not self.primary_models:
            raise ValueError("primary_models must contain at least one model")
        if self.chairman_model not in self.primary_models:
            raise ValueError(
                f"chairman_model='{self.chairman_model}' must be included in "
                f"primary_models={self.primary_models}"
            )

    def get_model_config(self, model_id: ModelId) -> ModelConfig:
        """Get model config by model ID (type-safe access).

        Raises:
            KeyError: If model_id is not a valid model identifier.
        """
        if not hasattr(self, model_id):
            raise KeyError(f"Unknown model_id: '{model_id}'")
        return getattr(self, model_id)


def load_api_keys() -> dict[ModelId, str]:
    """Load API keys from environment variables.

    Returns:
        Dict mapping model ID to API key. Only includes keys that are set
        and non-empty after stripping whitespace.
    """
    keys: dict[ModelId, str] = {}
    for model_id, env_var in _API_KEY_ENV_VARS.items():
        value = os.environ.get(env_var)
        if value:
            value = value.strip()
            if value:
                keys[model_id] = value
    return keys


def get_env_var_name(model_id: ModelId) -> str:
    """Get the environment variable name for a model's API key."""
    return _API_KEY_ENV_VARS[model_id]


def default_config() -> Config:
    """Return default configuration for v0.5.

    Default enables only GPT and Claude as primary models.
    """
    return Config(primary_models=["gpt", "claude"])
