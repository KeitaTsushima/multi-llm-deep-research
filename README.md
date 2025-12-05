# multi-llm-deep-research

A reproducible research pipeline.
— Source code only. Inputs & outputs live outside this repository.

## What is this?

**multi-llm-deep-research** is an OSS project that codifies a **reproducible, general-purpose research pipeline** leveraging multiple LLMs in parallel:

> Primary Research → Cross-Model Diff → Meta-Review → Final Insight Synthesis

This repository contains **only executable code and templates**. Specific research requests (inputs) and LLM outputs (results) are stored **locally on your machine**.

The goal is to **structure traditional manual deep research** into a form that anyone can reproduce.

## Why Multi-LLM Research?

A single model alone cannot avoid certain limitations:

- **Perspective bias**
- **Hallucinations**
- **Incorrect assumptions**
- **Lack of up-to-date information**
- **Weak evidence**

To address these, this project **uses LLMs with different strengths in parallel** and treats **cross-model differences and contradictions as sources of insight**.

### Models Used

| Model | Strength |
|-------|----------|
| GPT | Logic, structure, final synthesis (chair role) |
| Claude | Critical thinking, assumption testing, depth of insight |
| Gemini | Latest web news, tech blogs, search-based research |
| Perplexity | Academic papers, cited research, evidence collection |
| Grok/X | Social narratives, public opinion, cultural context analysis |

## Repository Structure

This repository contains **only executable code and templates**.
All research inputs and outputs are stored **outside the repository**.

```
multi-llm-deep-research/
├── src/
│   └── mldr/
│       ├── core/
│       │   ├── pipeline.py      # Stage 1–3 pipeline orchestration
│       │   ├── llm_clients.py   # LLM provider abstraction
│       │   ├── prompts.py       # Prompt builders for each stage
│       │   └── config.py        # Configuration (model selection, timeouts)
│       ├── cli/
│       │   └── main.py          # CLI entry point
│       └── __init__.py
├── templates/
│   ├── research-request.md      # Research specification template
│   ├── meta-review.md           # Structural + interpretive meta-review template
│   └── final-report.md          # Final report template
├── docs/
│   ├── project-overview.md      # Project purpose, goals, tech stack
│   └── architecture.md          # Module responsibilities, data flow, interfaces
├── pyproject.toml
└── README.md
```

## Where Inputs & Outputs Live

**No research data (inputs or outputs) is stored in this repository.**

Instead, create an arbitrary "workspace" on your local machine.

### Input (research-request.md)

Example:
```
~/Documents/mldr/workspace/
 └── 20250105-mci-care/
      └── research-request.md
```

### Output (LLM outputs / meta-review / final-report)

Example:
```
~/Documents/mldr/output/
 └── 20250105-mci-care/
      ├── gpt.md
      ├── claude.md
      ├── gemini.md
      ├── grok.md
      ├── perplexity.md
      ├── meta-review-gpt.md
      ├── meta-review-claude.md
      └── final-report.md
```

## Research Pipeline

### Stage 0 — Research Briefing

Use GPT to structure the research theme and generate an optimal research-request (optional).

### Stage 1 — Parallel Deep Research

Submit the same `research-request.md` to 5 LLMs for primary research.

Each model responds following the structure defined in `templates/research-request.md` (Section 5: Expected Output Structure):

- Key Facts
- Key Concepts / Entities
- Context & Drivers
- Distinguishing Features / Patterns
- Hypotheses
- Conflicting Perspectives / Open Questions
- Evidence & Sources
- Limitations

### Stage 2 — Meta Review (Diff & Critique)

#### GPT meta-review (structural)

GPT looks across all model reports and focuses on **structural aggregation**:

- Extracts common facts and shared conclusions
- Identifies conflicting claims between models
- Scores claims by apparent evidential strength (multi-model support, citations, etc.)
- Maps which model emphasizes which aspects of the topic
- Surfaces points that clearly require further clarification or investigation

#### Claude meta-review (interpretive)

Claude takes the structural view (including GPT's meta-review) and focuses on **interpretation and critique**:

- Examines hidden assumptions behind the shared conclusions and conflicts
- Highlights missing perspectives, stakeholders, and time horizons
- Identifies business/strategic risks and "directions we probably should not take"
- Proposes alternative explanations or causal stories that could also fit the observed facts

### Stage 3 — Final Synthesis (GPT as Chair)

GPT integrates all information and outputs:

- **High-confidence facts summary**
- **Points of contention across models**
- **Strategic implications**
- **Priority hypotheses**
- **Next actions** (research, PoC, interviews, etc.)
- **Additional sources to review**

## Roadmap

- [x] **v0**: Templates & pipeline specification ← *current*
- [ ] **v0.5**: CLI tools (`new research` / `run pipeline` / `save output`)
- [ ] **v1**: Automated meta-review generation and formatting
- [ ] **v1.5**: Automated final-report generation
- [ ] **v2**: Research Dashboard (Web UI / history / diff)
- [ ] **v3**: Multi-agent orchestration layer (LLM-to-LLM chat / role optimization)

## License

MIT License

## Contributing

Pull requests, issues, and feature suggestions are welcome.
