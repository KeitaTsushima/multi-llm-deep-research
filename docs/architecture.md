# Architecture

> This document describes the internal architecture of `multi-llm-deep-research`.
> It defines module responsibilities, data flow, and public Python / CLI interfaces.

---

## 1. Core Concepts

### 1.1 Research Workspace

- A **workspace** is any directory on the local filesystem where a research project lives.
- Each research project has:
  - `research-request.md` (input specification)
- Example:
  - `~/Documents/mldr/workspace/20250105-washoku/research-request.md`

### 1.2 Output Directory

- For each research run, outputs are written to an **output directory** outside the repo.
- Example:
  - `~/Documents/mldr/output/20250105-washoku/`
- Output files:
  - Stage 1 (primary research):
    - `gpt.md`
    - `claude.md`
    - `gemini.md`
    - `perplexity.md`
    - `grok.md` (if enabled)
  - Stage 2 (meta-review):
    - `meta-review-gpt.md` (structural)
    - `meta-review-claude.md` (interpretive)
  - Stage 3 (final):
    - `final-report.md`

### 1.3 Templates

- `templates/research-request.md`
- `templates/meta-review.md`
- `templates/final-report.md`

These are **not** modified by the pipeline at runtime; they serve as prompt scaffolding.

---

## 2. Modules & Responsibilities

### 2.1 `mldr.core.config`

- Defines configuration objects and default values.
- Loads API keys **from environment variables**, never hard-codes them.

Key types:

```python
# mldr/core/config.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Optional

ModelId = Literal["gpt", "claude", "gemini", "perplexity", "grok"]

@dataclass
class ModelConfig:
    enabled: bool
    model_name: str          # provider-specific name
    timeout_sec: int = 120

@dataclass
class Config:
    primary_models: list[ModelId]           # models used in Stage 1
    chairman_model: ModelId = "gpt"         # model used for final synthesis

    default_workspace_dir: Optional[Path] = None
    default_output_root: Optional[Path] = None

    # Use field(default_factory=...) to avoid mutable default argument issues
    gpt: ModelConfig = field(default_factory=lambda: ModelConfig(enabled=True, model_name="gpt-4.1-mini"))
    claude: ModelConfig = field(default_factory=lambda: ModelConfig(enabled=True, model_name="claude-3-5-sonnet"))
    gemini: ModelConfig = field(default_factory=lambda: ModelConfig(enabled=True, model_name="gemini-1.5-pro"))
    perplexity: ModelConfig = field(default_factory=lambda: ModelConfig(enabled=True, model_name="sonar-pro"))
    grok: ModelConfig = field(default_factory=lambda: ModelConfig(enabled=False, model_name="grok-2"))

def load_api_keys() -> dict[ModelId, str]:
    ...
    # loads from env:
    # OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY,
    # PERPLEXITY_API_KEY, GROK_API_KEY

def default_config() -> Config:
    ...
```

**Important:**
`config.py` never stores API keys.
Always load from `os.environ[...]` / `.env`.

---

### 2.2 `mldr.core.llm_clients`

Purpose:
Provide a unified interface for all LLM providers.

```python
# mldr/core/llm_clients.py
from dataclasses import dataclass
from typing import Protocol
from .config import Config, ModelId, load_api_keys

@dataclass
class LLMResult:
    raw_text: str

class LLMClient(Protocol):
    def run(self, prompt: str) -> LLMResult:
        ...

def build_clients(config: Config) -> dict[ModelId, LLMClient]:
    """
    Instantiate one client per model, using env-based API keys.
    Only creates clients for models that are enabled in Config.
    """
    ...
```

- `build_clients` initializes each SDK (OpenAI, Anthropic, etc.) internally.
- The rest of the code (pipeline) only needs to know **ModelId → client.run(prompt)**.

---

### 2.3 `mldr.core.prompts`

Purpose:
Generate the **final prompt string** to send to an LLM,
by combining templates + research spec + model outputs.

```python
# mldr/core/prompts.py
from pathlib import Path
from typing import Mapping
from .config import ModelId, Config

def build_primary_prompt(
    request_path: Path,
    model_id: ModelId,
    config: Config,
) -> str:
    """
    Stage 1 prompt.
    - Read research-request.md
    - Apply generic rules + model-specific instructions
    - Return the final prompt string for that model
    """
    ...

def build_structural_meta_prompt(
    request_path: Path,
    primary_outputs: Mapping[ModelId, Path],
) -> str:
    """
    Stage 2 (structural meta-review) prompt.
    - Based on "2. Structural Meta-Review" block from templates/meta-review.md
    - Embed research-request.md content
    - Embed each model's primary output (gpt.md, claude.md, ...)
    - Return a single prompt string
    """
    ...

def build_interpretive_meta_prompt(
    request_path: Path,
    primary_outputs: Mapping[ModelId, Path],
    structural_meta_path: Path,
) -> str:
    """
    Stage 2 (interpretive meta-review) prompt.
    - Based on "3. Interpretive Meta-Review" block from templates/meta-review.md
    - Embed research-request.md
    - Embed all primary outputs
    - Embed structural meta-review text
    - Return a single prompt string
    """
    ...

def build_final_report_prompt(
    request_path: Path,
    primary_outputs: Mapping[ModelId, Path],
    structural_meta_path: Path,
    interpretive_meta_path: Path,
    config: Config,
) -> str:
    """
    Stage 3 prompt.
    - Based on templates/final-report.md
    - Embed all md files as context
    - Return the final prompt string for the chairman model
    """
    ...
```

---

### 2.4 `mldr.core.pipeline`

Purpose:
Orchestrate Stage 1–3 **end-to-end in a single function**.

```python
# mldr/core/pipeline.py
from pathlib import Path
from typing import Mapping
from .config import Config, ModelId
from .llm_clients import build_clients, LLMClient  # LLMClient is a Protocol
from .prompts import (
    build_primary_prompt,
    build_structural_meta_prompt,
    build_interpretive_meta_prompt,
    build_final_report_prompt,
)

def run_research(
    request_path: Path,
    output_dir: Path,
    config: Config,
) -> None:
    """
    End-to-end pipeline:
    - Stage 1: primary research by all configured models
    - Stage 2: structural + interpretive meta-review
    - Stage 3: final synthesis by chairman model

    Side-effects:
    - Writes markdown files into output_dir:
        gpt.md, claude.md, gemini.md, perplexity.md, grok.md (enabled only)
        meta-review-gpt.md
        meta-review-claude.md
        final-report.md
    """
    ...

def _run_primary_research(
    request_path: Path,
    output_dir: Path,
    config: Config,
    clients: Mapping[ModelId, "LLMClient"],
) -> Mapping[ModelId, Path]:
    """
    Stage 1:
    - For each model in config.primary_models:
      - build_primary_prompt(...)
      - call client.run(prompt)
      - save result to <model_id>.md in output_dir
    - Returns: {model_id: path_to_output_md}
    """
    ...

def _run_meta_review(
    request_path: Path,
    output_dir: Path,
    config: Config,
    primary_outputs: Mapping[ModelId, Path],
    clients: Mapping[ModelId, LLMClient],
) -> tuple[Path, Path]:
    """
    Stage 2:
    - Structural meta-review:
        - build_structural_meta_prompt(...)
        - send to GPT (hardcoded in v0)
        - write meta-review-gpt.md
    - Interpretive meta-review:
        - build_interpretive_meta_prompt(...)
        - send to Claude (hardcoded in v0)
        - write meta-review-claude.md

    v0 policy: Structural reviewer = GPT, Interpretive reviewer = Claude (hardcoded).
    Future versions may add config options (structural_reviewer_model, interpretive_reviewer_model).

    Returns:
        (path_to_structural_meta, path_to_interpretive_meta)
    """
    ...

def _run_final_synthesis(
    request_path: Path,
    output_dir: Path,
    config: Config,
    primary_outputs: Mapping[ModelId, Path],
    structural_meta_path: Path,
    interpretive_meta_path: Path,
    clients: Mapping[ModelId, "LLMClient"],
) -> Path:
    """
    Stage 3:
    - build_final_report_prompt(...)
    - send to chairman model (config.chairman_model)
    - write final-report.md

    Returns:
        Path to final-report.md
    """
    ...
```

**Note on Stage 0:**
Stage 0 ("Research brief refinement") is **not part of this pipeline**.
It can be done manually or implemented later as a separate helper command.
`run_research()` assumes `research-request.md` is already prepared.

---

## 3. CLI Interface

### 3.1 Entry Point

- `mldr` command (`python -m mldr.cli.main` or via `console_scripts`)

### 3.2 Commands (v0.5)

#### `mldr new research`

```bash
mldr new research \
  --workspace /path/to/workspace \
  --slug 20250105-topic
```

**Behavior:**

- Creates directory: `<workspace>/<slug>/`
- Copies `templates/research-request.md` into:
  - `<workspace>/<slug>/research-request.md`
- Does **not** run any LLM calls.
- If directory already exists:
  - Either fail with clear error, or require `--force` (implementation choice)

#### `mldr run`

```bash
mldr run \
  --request /path/to/research-request.md \
  --output  /path/to/output-dir \
  [--models gpt,claude]
```

**Behavior:**

- Loads `default_config()`
- If `--models` is provided, overrides `config.primary_models` with the specified list
- Calls `run_research(request_path, output_dir, config)`
- Creates output directory if it does not exist.
- Fails fast if:
  - `request` does not exist
  - Required API keys are missing for specified models

**Options:**

| Option | Required | Description |
|--------|----------|-------------|
| `--request` | Yes | Path to `research-request.md` |
| `--output` | Yes | Output directory for results |
| `--models` | No | Comma-separated list of models to use (e.g., `gpt,claude`). Overrides `config.primary_models`. Useful for development and cost control. |

---

## 4. Error Handling & Assumptions

- The pipeline assumes:
  - `research-request.md` follows the template structure,
    but does **not** attempt to strictly validate it in v0.
  - LLM calls may fail; minimal handling:
    - Log error
    - Skip that model
    - Continue with remaining models

- For v0:
  - Prefer **simplicity over robustness**.
  - Later versions can add:
    - Retries
    - Per-model error reports
    - Partial run recovery

---

## 5. Design Principles & Version Roadmap

This project intentionally separates **v0.5** (minimal viable pipeline) from **v1.0** (structured, scalable pipeline).
The goal is to ensure the first version is small, reliable, and easy to validate, while leaving clear extension points for more advanced research workflows.

---

### 5.1 v0.5 — Scope & Required Guarantees

v0.5 focuses solely on producing a complete research workflow:

**Core Pipeline**
- Primary Research → Meta-Review → Final Synthesis
- Implement Stage 1–3 as defined, with no additional feedback loops.

**Fault Tolerance (Mandatory)**
- A failure in one model **must not** stop the entire pipeline.
- `_run_primary_research()` wraps each model call in try/except.
- Failed models are skipped with warnings and explicitly noted in Meta-Review prompts.
- Example prompt addition: *"Note: The following models failed and are excluded: [model_list]"*

**Model Selection Flexibility**
- `config.primary_models` controls which models run.
- CLI supports `--models` to override this (see Section 3.2).
- Enables fast testing (e.g., `--models gpt,claude` for development).

**Markdown Output Only**
- All LLM outputs remain in Markdown following the template structure.
- No parsing or structured-data extraction is performed in v0.5.
- Templates should strongly discourage verbose intros or format deviations.

**Full-Context Meta Review**
- Stage 2 receives full primary outputs (no summarization layer yet).
- Prompt templates enforce concise, bullet-point style responses.

These are the **only guarantees** required for v0.5 to function reliably.

---

### 5.2 v1.0 — Planned Extensions (Do NOT Implement in v0.5)

The following enhancements are explicitly **out of scope** for v0.5, but the architecture must leave room for them:

**Structured Output (JSON or XML tagging)**
- Primary model outputs will eventually be parsed into an internal `ModelReport` structure (Pydantic).
- Markdown will be generated after structured interpretation.
- Enables programmatic extraction of "Key Facts", "Evidence", etc.

**Map-Reduce Compression Layer (Stage 1.5)**
- Before Meta-Review, an optional summarization step will extract:
  - Key claims
  - Evidence / sources
  - Contradictions
- This reduces context window load and improves reasoning stability.
- Design hook: `_summarize_primary_reports()` function placeholder in pipeline.

**Evidence & Source Extraction**
- Perplexity/Gemini URLs will be parsed and attached to fact objects.
- Distinction between "evidence-supported facts" and "model-internal knowledge" will be introduced.
- v0.5 relies on "Evidence & Sources" section in templates only.

**Critic Loop (Stage 3 → Stage 4)**
- After Meta-Review, a Critic model can request:
  - Clarifications
  - Targeted re-research
  - Contradictions to investigate
- Only then a final synthesis is produced.
- Pipeline stages become: `stage_primary → stage_meta → stage_critic → stage_final`

**Async Execution for Performance**
- All primary research calls may run with `asyncio` in the future.
- v0.5 uses synchronous calls for simplicity.

These future features influence design choices, but **must not be implemented now**.

---

### 5.3 Principle Summary

| Version | Focus |
|---------|-------|
| **v0.5** | Correctness + Stability + Clarity |
| **v1.0** | Structure + Scalability + Depth |

The architecture must remain small and robust for v0.5, while clearly marking the seams where v1 features will attach later.

> **Implementation Note (for all contributors and LLMs):**
> When producing implementation plans or writing code,
> **strictly follow the v0.5 scope** described in Section 5.1.
>
> Items listed under **v1.0 — Planned Extensions** (Section 5.2)
> are *design constraints only* and **must NOT be implemented** in v0.5.
>
> Any implementation plan that includes structured-output parsing,
> JSON/XML, map-reduce summarization, evidence extraction, critic loops,
> or async execution is considered **out of scope** and should be rejected.

---

### 5.4 Legacy Roadmap Hooks

This architecture also leaves room for:

- Configurable chairman model (GPT / Gemini / Claude) — already supported via `config.chairman_model`
- Web dashboard or API layer on top of `run_research()`
- Optional Stage 0 helper command (`mldr assist request` etc.)
