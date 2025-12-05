# Meta-Review Template

> This file defines how meta-review models (e.g., GPT and Claude) should analyze
> the primary research outputs from multiple LLMs.

The meta-review operates on:
- One shared `research-request.md` (specification)
- Multiple primary research outputs (e.g., `gpt.md`, `claude.md`, `gemini.md`, `grok.md`, `perplexity.md`)

There are two distinct meta-review roles:
- **Structural meta-review** (GPT or equivalent)
- **Interpretive meta-review** (Claude or equivalent)

---

## 1. Inputs to Meta-Review

The meta-review model receives:

1. The original **research-request.md**
2. All primary research outputs from each model, each following the same structure:
   - 5.1 Key Facts
   - 5.2 Key Concepts / Entities
   - 5.3 Context & Drivers
   - 5.4 Distinguishing Features / Patterns
   - 5.5 Hypotheses
   - 5.6 Conflicting Perspectives / Open Questions
   - 5.7 Evidence & Sources
   - 5.8 Limitations

---

## 2. Structural Meta-Review (e.g., GPT)

**Goal:**
Provide a **structured aggregation** of all model outputs, without over-interpreting them.
Focus on mapping the landscape: common ground, conflicts, claim strength, and coverage gaps.

The structural meta-review must follow this format:

### 2.1 Overview

- Briefly summarize:
  - How many models were reviewed
  - At a high level, how consistent or divergent their outputs are

### 2.2 Common Ground (Shared Facts & Themes)

- List facts, themes, or patterns that **multiple models agree on**.
- For each item, indicate:
  - Which models support it
  - Whether it appears in "Key Facts", "Context & Drivers", or "Distinguishing Features"

### 2.3 Conflicting Claims

- List points where models **disagree** or provide divergent explanations.
- For each conflict:
  - Describe the conflicting views
  - Indicate which models support each side

### 2.4 Claim Strength Assessment

- Group important claims into:
  - **Strongly supported** (multiple models + evidence)
  - **Moderately supported** (single model + some evidence)
  - **Weakly supported / speculative** (single model, little or no evidence)
- This is about **evidential strength**, not about final judgment.

### 2.5 Model Focus Map

- Describe what each model tends to emphasize:
  - e.g., "Model A focuses on historical context; Model B on stakeholders; Model C on practical use cases."
- Note any **blind spots** where one model provides coverage that others lack.

### 2.6 Clarification Points

- List items that clearly require:
  - More evidence
  - Clearer definitions
  - Additional research
- These will later feed into "Next Actions" in the final report.

---

## 3. Interpretive Meta-Review (e.g., Claude)

**Goal:**
Provide **interpretation and critique** based on the structural view.
Focus on assumptions, missing perspectives, risks, and alternative narratives.

The interpretive meta-review must follow this format:

### 3.1 Interpretive Overview

- Briefly restate:
  - What the structural meta-review concluded
  - Where the most interesting or risky areas of disagreement lie

### 3.2 Assumption Analysis

- Identify **implicit assumptions** behind:
  - Shared conclusions
  - Major conflicts
- For each assumption, describe:
  - Why it matters
  - What could change if the assumption is wrong

### 3.3 Missing Perspectives & Blind Spots

- Highlight:
  - Stakeholders, contexts, or time horizons that are **underrepresented or missing**
  - Domains of expertise that seem absent (e.g., legal, operational, user behavior, ethics)

### 3.4 Risks & "Do-Not-Do" Directions

- Identify **risks** if the synthesized insights were used directly for:
  - Business or product strategy
  - Policy or operational decisions
- Point out any **directions we probably should not take**, and why:
  - e.g., high regulatory risk, ethical issues, low robustness of evidence

### 3.5 Alternative Explanations / Narratives

- Propose **alternative causal stories or interpretations** that could also explain the observed facts.
- Make explicit:
  - Where different narratives are plausible
  - What evidence would help discriminate between them

### 3.6 Recommendations for Further Research

- Based on all of the above, suggest:
  - Which uncertainties to prioritize
  - What types of data, experiments, or expert interviews would be most valuable
  - How to refine future research requests

---

## 4. Constraints for Meta-Review Models

- Do **not** re-run primary web research; operate on the provided model outputs and research-request.
- Be explicit about where you are interpreting vs. restating.
- Do not hide uncertainties; call them out clearly.
- Keep the structure above; do not change section names or order.
