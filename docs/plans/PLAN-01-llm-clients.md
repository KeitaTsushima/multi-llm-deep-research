# PLAN-01: Config & LLM Clients

## Goals

### What are we trying to achieve?

Implement the configuration layer (`config.py`) and LLM client abstraction (`llm_clients.py`) as defined in `docs/architecture.md`.

This enables the pipeline to:
1. Load configuration with model settings (model_name, timeout, enabled)
2. Load API keys securely from environment variables
3. Call LLMs via unified interface: `client.run(prompt, system) -> LLMResult`

### Success Criteria (v0.5 Scope)

- [x] `config.py`: `ModelId`, `ModelConfig`, `Config`, `load_api_keys()`, `default_config()` implemented
- [ ] `llm_clients.py`: `LLMResult`, `LLMClient` Protocol, `build_clients()` implemented
- [ ] **Required clients**: OpenAIClient (GPT) and AnthropicClient (Claude) fully working
- [ ] **Optional clients**: Gemini/Perplexity/Grok as stubs (`NotImplementedError`) or `enabled=False`
- [ ] `build_clients(config)` returns `dict[ModelId, LLMClient]` respecting `enabled` flag
- [x] Unit tests passing for config.py (25 tests)
- [ ] Unit tests passing for llm_clients.py
- [x] `ruff` / `mypy` pass without errors

## Context

### Architecture Alignment

Per `docs/architecture.md`:

**`config.py` is responsible for:**
- `ModelId` type (Literal)
- `ModelConfig` dataclass (enabled, model_name, timeout_sec)
- `Config` dataclass (primary_models, chairman_model, model configs)
- `load_api_keys()` function
- `default_config()` function

**`llm_clients.py` is responsible for:**
- `LLMResult` dataclass (`raw_text: str` only for v0.5)
- `LLMClient` Protocol (`run(prompt: str, system: str | None = None) -> LLMResult`)
- `build_clients(config: Config) -> dict[ModelId, LLMClient]`

### v0.5 Scope Constraints

- **Required**: GPT (OpenAI) and Claude (Anthropic) must work
- **Optional**: Gemini, Perplexity, Grok can be stubs
- **No streaming**: Batch processing only
- **No rate limiting**: Handled in v1
- **No usage tracking**: `LLMResult` contains only `raw_text`
- **Synchronous only**: `LLMClient.run()` must remain synchronous in v0.5

> **Design Note (Async)**: v1.x will introduce async support via a *separate* interface
> (e.g., `AsyncLLMClient`). The v0.5 `run()` signature must not be modified.
> This avoids breaking the v0.5 pipeline while preserving a forward-compatible upgrade path.

### Dependencies

**External SDKs (to be added to requirements.txt):**
- `openai` - OpenAI Python SDK
- `anthropic` - Anthropic Python SDK

**Optional (for stubs or v1):**
- `google-generativeai` - Google Generative AI SDK

## Proposed Solution

### High-Level Approach

```
┌─────────────────────────────────────────────────────────────┐
│                        config.py                            │
│  ModelId, ModelConfig, Config, load_api_keys()              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      llm_clients.py                         │
│  LLMResult, LLMClient (Protocol), build_clients(config)     │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        OpenAIClient   AnthropicClient   (Stubs...)
```

### Why This Approach?

1. **Separation of concerns**: Config in `config.py`, clients in `llm_clients.py`
2. **Protocol pattern**: Flexible, testable with mocks
3. **`build_clients()` over `get_client()`**: Returns all enabled clients at once, aligned with pipeline's batch execution model
4. **Config-driven**: `ModelConfig.model_name` and `timeout_sec` passed to SDK calls

### Key Components

**config.py:**
1. `ModelId` - Literal type for model identifiers
2. `ModelConfig` - Per-model settings (enabled, model_name, timeout_sec)
3. `Config` - Application configuration with all model configs
4. `load_api_keys()` - Reads API keys from environment variables
5. `default_config()` - Returns default Config instance

**llm_clients.py:**
1. `LLMResult` - Response dataclass (`raw_text: str`)
2. `LLMClient` - Protocol defining `run(prompt: str, system: str | None = None) -> LLMResult`
3. `OpenAIClient` - GPT implementation
4. `AnthropicClient` - Claude implementation
5. `build_clients()` - Factory that creates enabled clients

### Error Handling Strategy

- `load_api_keys()`: Returns dict of available keys, missing keys = empty string or KeyError
- `build_clients()`: Raises exception if required API key is missing for enabled model
- Client `run()`: Lets SDK exceptions propagate (pipeline handles via try/except)
- Logging: Use `print()` for v0.5 simplicity

## Implementation Steps

### Step 1: config.py - Type definitions

- Modify: `src/mldr/core/config.py`
- Add:
  - `ModelId = Literal["gpt", "claude", "gemini", "perplexity", "grok"]`
  - `ModelConfig` dataclass
  - `Config` dataclass with **named fields** for each model:
    ```python
    @dataclass
    class Config:
        primary_models: list[ModelId]
        chairman_model: ModelId = "gpt"
        gpt: ModelConfig = ...
        claude: ModelConfig = ...
        gemini: ModelConfig = ...
        perplexity: ModelConfig = ...
        grok: ModelConfig = ...

        def get_model_config(self, model_id: ModelId) -> ModelConfig:
            return getattr(self, model_id)
    ```
  - Access pattern: `config.get_model_config(model_id)` for type-safe access
- Why: Foundation for all configuration; named fields ensure type safety and IDE support

### Step 2: config.py - API key loading

- Add: `load_api_keys() -> dict[ModelId, str]`
- Read from environment:
  - `OPENAI_API_KEY` → "gpt"
  - `ANTHROPIC_API_KEY` → "claude"
  - `GOOGLE_API_KEY` → "gemini"
  - `PERPLEXITY_API_KEY` → "perplexity"
  - `GROK_API_KEY` → "grok"
- Why: Secure key management

### Step 3: config.py - default_config()

- Add: `default_config() -> Config`
- Returns Config with:
  - `primary_models = ["gpt", "claude"]`
  - `gpt.enabled = True`
  - `claude.enabled = True`
  - `gemini.enabled = False`
  - `perplexity.enabled = False`
  - `grok.enabled = False`
- Why: v0.5 focuses on GPT + Claude only; other models available for future expansion

### Step 4: llm_clients.py - LLMResult & Protocol

- Modify: `src/mldr/core/llm_clients.py`
- Add:
  - `LLMResult` dataclass (`raw_text: str`)
  - `LLMClient` Protocol:
    ```python
    def run(self, prompt: str, system: str | None = None) -> LLMResult: ...
    ```
- Why: Define interface before implementations; `system` param allows SDK-native system prompt handling

### Step 5: llm_clients.py - OpenAIClient

- Add: `OpenAIClient` class
- Constructor: Takes `api_key`, `model_name`, `timeout_sec`
- Method: `run(prompt, system=None) -> LLMResult` using `openai` SDK
  - If `system` provided: use as system message
  - `prompt` becomes user message
- Why: Required for v0.5

### Step 6: llm_clients.py - AnthropicClient

- Add: `AnthropicClient` class
- Constructor: Takes `api_key`, `model_name`, `timeout_sec`
- Method: `run(prompt, system=None) -> LLMResult` using `anthropic` SDK
  - Uses SDK's native `system` parameter
  - `prompt` becomes user message
- Why: Required for v0.5

### Step 7: llm_clients.py - Stub clients

- Add: `GeminiClient`, `PerplexityClient`, `GrokClient` as stubs
- Each raises `NotImplementedError` in `run()`
- Why: Placeholder for v1 expansion

### Step 8: llm_clients.py - build_clients()

- Add: `build_clients(config: Config) -> dict[ModelId, LLMClient]`
- Logic:
  - Call `load_api_keys()`
  - For each `model_id` in `config.primary_models`:
    - Get model config: `model_cfg = config.get_model_config(model_id)`
    - If `model_cfg.enabled is False`: skip
    - If `enabled is True` but API key is missing: **raise exception immediately**
      ```
      Missing API key for model 'gpt'. Expected env var OPENAI_API_KEY.
      ```
    - Instantiate appropriate client with `model_cfg.model_name`, `model_cfg.timeout_sec`
  - Return dict of `{model_id: client}`
- **No partial creation**: If any enabled model fails, the whole function fails
- Why: Single entry point for pipeline; fail-fast prevents silent failures

### Step 9: Update requirements.txt

- Add with version pins:
  ```
  openai>=1.0.0,<2.0.0
  anthropic>=0.3.0,<1.0.0
  ```
- Why: SDK dependencies; pin major versions to avoid SDK breaking changes

### Step 10: Testing

- Create: `tests/test_config.py`
  - Test `load_api_keys()` with mocked env vars
  - Test `default_config()` returns valid Config
- Create: `tests/test_llm_clients.py`
  - Test Protocol conformance (type checking)
  - Test `build_clients()` with mocked config
  - Test OpenAI/Anthropic clients with mocked SDK responses
- Why: Quality assurance

## Testing Strategy

### Unit Tests

- Test A: `load_api_keys()` reads from environment correctly
- Test B: `default_config()` returns expected defaults
- Test C: `OpenAIClient` and `AnthropicClient` conform to `LLMClient` Protocol
- Test D: `build_clients()` returns correct clients based on config
- Test E: `build_clients()` raises error when API key missing for enabled model

### Integration Tests (Manual)

- Scenario 1: Run with real API keys, verify "Hello" prompt returns response
- Scenario 2: Verify timeout is respected

### Manual Testing

- [ ] `build_clients()` with `Config.primary_models = ["gpt", "claude"]` returns 2 clients
- [ ] Missing API key shows clear error message

## Open Questions

*Resolved based on architecture.md:*

1. ~~Model ID format~~ → Use `ModelId = Literal["gpt", "claude", ...]`
2. ~~get_client vs build_clients~~ → Use `build_clients(config)`
3. ~~LLMResponse vs LLMResult~~ → Use `LLMResult`

*Remaining:*

1. **Gemini/Perplexity/Grok stubs**: Raise `NotImplementedError` or return mock response?
   → Recommendation: `NotImplementedError` (explicit failure is clearer)

## Issues Encountered and Resolved

### config.py Implementation (2025-12-06)

1. **timeout_sec default too short**: Initial value of 120s inadequate for deep research
   - Resolution: Changed to 600s (10 min) based on SDK defaults research

2. **chairman_model validation missing**: No check that chairman is in primary_models
   - Resolution: Added `__post_init__()` validation

3. **ModelConfig responsibility unclear**: Risk of config bloat with runtime params
   - Resolution: Added docstring clarifying user-facing vs runtime params separation

4. **ModelId extensibility concern**: Literal type limits future model additions
   - Resolution: Documented v1.x migration path to Enum/registry pattern

5. **LLMClient.run() missing system param**: SDK-native system prompt handling needed
   - Resolution: Updated PLAN to include `system: str | None = None` parameter

6. **pyproject.toml missing**: Package not installable for pytest
   - Resolution: Created pyproject.toml with package config and dev dependencies

## Future Improvements

*(Out of scope for v0.5 — tracked in GitHub Issues)*

All future improvements are tracked in GitHub Issues with label `v1.x`:
- [View all v1.x issues](https://github.com/KeitaTsushima/multi-llm-deep-research/issues?q=is%3Aissue+is%3Aopen+label%3Av1.x)

### Features

| Issue | Title | Labels |
|-------|-------|--------|
| [#9](https://github.com/KeitaTsushima/multi-llm-deep-research/issues/9) | Implement Deep Research API integration | enhancement |
| [#10](https://github.com/KeitaTsushima/multi-llm-deep-research/issues/10) | Implement additional LLM clients (Gemini, Perplexity, Grok) | enhancement |
| [#11](https://github.com/KeitaTsushima/multi-llm-deep-research/issues/11) | Add resilience features (rate limiting, retry, async) | enhancement |

### Code Quality

| Issue | Title | Priority |
|-------|-------|----------|
| [#2](https://github.com/KeitaTsushima/multi-llm-deep-research/issues/2) | Add py.typed marker for PEP 561 compliance | 🟡 Medium |
| [#3](https://github.com/KeitaTsushima/multi-llm-deep-research/issues/3) | Refactor get_model_config() to use explicit mapping | 🟡 Medium |
| [#4](https://github.com/KeitaTsushima/multi-llm-deep-research/issues/4) | Add logging to load_api_keys() for missing keys | 🟡 Medium |
| [#5](https://github.com/KeitaTsushima/multi-llm-deep-research/issues/5) | Add SecureApiKey wrapper to mask keys in logs | 🟢 Low |
| [#6](https://github.com/KeitaTsushima/multi-llm-deep-research/issues/6) | Add frozen=True to dataclasses for immutability | 🟢 Low |
| [#7](https://github.com/KeitaTsushima/multi-llm-deep-research/issues/7) | Add pre-commit hooks for automated linting | 🟢 Low |
| [#8](https://github.com/KeitaTsushima/multi-llm-deep-research/issues/8) | Add bandit security scanning to CI | 🟢 Low |

### Design Decisions

| Issue | Title |
|-------|-------|
| [#12](https://github.com/KeitaTsushima/multi-llm-deep-research/issues/12) | Consider relaxing chairman_model validation |
| [#13](https://github.com/KeitaTsushima/multi-llm-deep-research/issues/13) | Migrate ModelId from Literal to Enum/registry pattern |
