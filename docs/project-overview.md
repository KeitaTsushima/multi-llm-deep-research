# Project Overview

## Project Name

multi-llm-deep-research

## Purpose

This project provides a **reproducible, general-purpose research pipeline** that:

- Runs **multiple LLMs in parallel** on the same research spec
- Collects their outputs in a consistent structure
- Performs **meta-review** (structural + interpretive)
- Produces a **final synthesized research report**

It exists to turn ad-hoc, manual "deep research with multiple LLMs" into a **structured, automatable workflow**.

## Goals

- Provide a **standard file/structure protocol** for multi-LLM research (inputs, outputs, meta-review, final report)
- Offer a **CLI and Python API** to run the entire pipeline end-to-end
- Make it easy to swap or add models (GPT, Claude, Gemini, Perplexity, Grok, etc.) behind a unified interface

## Key Features

- **Research spec template** (`research-request.md`) shared across all models
- **Parallel primary research** across multiple LLMs with a unified output schema
- **Two-layer meta-review**:
  - Structural aggregation (common ground, conflicts, claim strength)
  - Interpretive critique (assumptions, missing perspectives, risks, alternative narratives)
- **Final synthesis** by a "chair" model into a decision-ready report
- **Source-code-only repo**: inputs/outputs live outside the repository to keep it clean and safe

## Technology Stack

### Core

- **Language**: Python
- **Usage**: CLI tool + library (no frontend, no backend service in v0)
- **Config**: `config.py` / optional `.env` / `config.yaml`
- **Package name**: `mldr` (multi-llm-deep-research)

### External Services

- LLM providers via HTTP APIs:
  - OpenAI (GPT)
  - Anthropic (Claude)
  - Google (Gemini)
  - Perplexity
  - X/Grok
- SDKs abstracted behind `llm_clients.py`

### Infrastructure

- Local execution by default (no mandatory cloud infrastructure)
- Optional: can be wired into CI/CD or job runners

## Workspace & Output Directories

multi-llm-deep-research does not store any research data inside this repository.
Two external directories are required:

- **Workspace** = Where each research project's input (`research-request.md`) lives.
  Contains contextual or confidential information.
  Example: `/Users/<name>/Documents/mldr/workspace/20250105-topic/`

- **Output directory** = Where all model outputs, meta-reviews, and final reports are written.
  Example: `/Users/<name>/Documents/mldr/output/20250105-topic/`

The pipeline always reads inputs from the workspace and writes results to the output directory.
Keeping these two locations separate and outside the repository preserves reproducibility and prevents accidental leakage of confidential data.

## Architecture Overview

### Directory Structure

```
multi-llm-deep-research/
├── src/
│   └── mldr/
│       ├── core/
│       │   ├── pipeline.py      # Stage 0–3 orchestration
│       │   ├── llm_clients.py   # LLM provider abstraction
│       │   ├── prompts.py       # Prompt builders
│       │   └── config.py        # Configuration management
│       ├── cli/
│       │   └── main.py          # CLI entrypoint
│       └── __init__.py
├── templates/
│   ├── research-request.md      # Research spec template
│   ├── meta-review.md           # Meta-review instructions
│   └── final-report.md          # Final report structure
├── docs/
├── pyproject.toml
└── README.md
```

### Core Modules

| Module | Responsibility |
|--------|----------------|
| `pipeline.py` | Orchestrates Stage 0–3: primary research → meta-review → final synthesis |
| `llm_clients.py` | Unified interface for different LLM providers (`ModelId → client.run(prompt)`) |
| `prompts.py` | Builds prompts by combining templates with research specs |
| `config.py` | Model selection, timeouts, output paths. **Never stores API keys** — all credentials are loaded from environment variables via `load_api_keys()` |

### Pipeline Stages

```
Stage 0 (optional): Research brief refinement
    ↓
Stage 1: Primary research (parallel across all models)
    ↓
Stage 2: Meta-review (structural by GPT + interpretive by Claude)
    ↓
Stage 3: Final synthesis by chairman model
```

> **Note**: Stage 0 is not automatically executed by the pipeline. It is performed manually by the user or via a separate CLI helper (future). `run_research()` starts from Stage 1.

### CLI Commands

```bash
# Create new research project
mldr new research --workspace ~/Documents/mldr/workspace --slug 20250105-topic

# Run full pipeline
mldr run --request <path-to-request.md> --output <output-dir>
```

## Project Status

- **Current**: v0 — templates and pipeline design finalized
- **Implemented**:
  - Conceptual pipeline and file templates
  - README and research templates
- **Next**:
  - Implement Python core (`pipeline.py`, `llm_clients.py`, `prompts.py`)
  - Implement CLI (`main.py`) with `new` and `run` commands

## Getting Started

1. Clone the repository
2. Set up Python environment:
   ```bash
   pip install -r requirements.txt
   ```
3. Set API keys in environment:
   ```bash
   export OPENAI_API_KEY="..."
   export ANTHROPIC_API_KEY="..."
   export GOOGLE_API_KEY="..."
   export PERPLEXITY_API_KEY="..."
   ```
4. Copy `templates/research-request.md` to your workspace and customize
5. Run the pipeline:
   ```bash
   mldr run --request <path> --output <dir>
   ```

> **Note**: By design, research inputs/outputs live **outside** this repo (e.g., `~/Documents/mldr/workspace`, `~/Documents/mldr/output`).

## Contact

- Repository: https://github.com/KeitaTsushima/multi-llm-deep-research
