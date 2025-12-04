# Claude Code - [Project Name]

## Session Startup Checklist (MUST READ ALOUD)

**At the start of EVERY session, read and confirm the following:**

1. **Current branch check**
   - Run `git branch` to confirm current branch
   - If on `main`, create a feature branch before any code changes
   - Never commit directly to main

2. **Workflow reminder**
   - Code changes require CodeRabbit CLI review (`coderabbit review --prompt-only --type uncommitted`)
   - Commits go to feature branch, then PR to main
   - PR triggers CodeRabbit GitHub review
   - Q&A pause after each implementation step (CANNOT SKIP)

3. **Confirm with user**
   - "現在のブランチは [branch name] です。作業を開始してよいですか？"

---

## Important Rules

1. **Check current status before working**
   - Read `docs/project-overview.md` to understand project purpose and goals
   - Reference current PLAN in `docs/plans/` for implementation steps
   - Check progress in `docs/daily-logs/` (most recent file)

2. **Never work directly on main branch**
   - Create feature branches for all work

3. **Always confirm before deletion**

4. **Record session log regularly**
   - Create/update `docs/daily-logs/YYYY-MM-DD.md` throughout the session (see `docs/daily-logs/template.md` for format)
   - Good timing: after completing a feature, solving a problem, or making a key decision

## Code Implementation Procedure

**This workflow ensures effective collaboration, even for beginners.**

### Complete Development Workflow

#### Phase 1: Planning (Create PLAN.md)

Create `docs/plans/PLAN-{NN}-[feature-name].md` using `PLAN-template.md` as starting point (NN = sequential number: 01, 02...). See `docs/plans/PLAN-guide.md` for detailed guidance.

#### Phase 2: Skeleton Implementation

**Step 1: Structure Only** (20-30 lines max)
- Write ONLY empty functions/classes, type definitions, and interface declarations
- NO implementation yet
- **IMMEDIATELY STOP after writing structure**
- Present what you wrote to the user

**Step 2: Q&A Pause** (MANDATORY - CANNOT SKIP)
- Explain the structure and architecture decisions you made
- Wait for user questions and clarifications
- Make adjustments based on feedback
- **Wait for EXPLICIT user confirmation before proceeding to Step 3**

**Step 3: Review & Confirm**
```bash
git add .
coderabbit review --prompt-only --type uncommitted
```
- Fix any issues found by CodeRabbit
- **Wait for EXPLICIT user confirmation before proceeding to Phase 3**

#### Phase 3: Incremental Implementation

**For each function/component:**

1. **Implement ONE function** (20-30 lines max)
   - **IMPORTANT**: Follow `docs/development/quality-guide.md` for code quality standards
   - **IMMEDIATELY STOP after implementing the function**
   - Present the implementation to the user

2. **Mandatory Q&A pause** (CANNOT SKIP)
   - Explain what you implemented and why
   - Answer user questions
   - **Wait for EXPLICIT user confirmation before proceeding**

3. **Run CodeRabbit review**
   ```bash
   git add .
   coderabbit review --prompt-only --type uncommitted
   ```
   See `docs/development/coderabbit-workflow.md` for detailed CodeRabbit usage.

4. **Create task list from CodeRabbit findings** (CRITICAL - prevents forgetting issues)
   - Use TodoWrite tool to record ALL issues found by CodeRabbit
   - Mark each issue with type (potential_issue, nitpick, etc.)
   - Example task list:
     - [pending] Fix memory leak in event handler (potential_issue)
     - [pending] Add null check for response.data (potential_issue)
     - [pending] Handle retry on initialization failure (nitpick)
   - This ensures no issue is forgotten during long Q&A sessions

5. **Fix issues one by one**
   - For each issue in the task list:
     - Mark issue as in_progress using TodoWrite
     - Fix ONE issue only
     - **IMMEDIATELY STOP after the fix**
     - Explain what you fixed and why
     - Answer user questions
     - **Wait for EXPLICIT user confirmation**
     - Mark issue as completed using TodoWrite
   - Repeat until all issues are resolved

6. **Re-run CodeRabbit to verify** (if significant changes were made)
   - Ensure all issues are resolved
   - If new issues appear, create a new task list (step 4) and repeat the process

7. **Write unit test** (Skip only if trivial getter/setter)
   - **IMPORTANT**: Follow `docs/development/testing-guide.md` for test strategy and patterns
   - Create test file (e.g., `function_name.test.ts` or `test_function_name.py`)
   - Write test cases:
     - Happy path (normal input)
     - Edge cases (empty, null, invalid input)
     - Error handling (if applicable)
   - Use appropriate test doubles (Mock, Stub, Fake) per testing-guide.md
   - Run tests to ensure they pass
   - **STOP and present test results**

8. **Wait for EXPLICIT confirmation** before implementing next function

#### Phase 4: Integration & Testing

After all functions implemented:
- **Integration testing**
  - Run build: `npm run build` / `pytest` (verify no errors)
  - Run dev server: `npm run dev` (manual testing if applicable)
  - Test actual functionality works end-to-end
- **Final CodeRabbit review**
  - Run `git add .` and `coderabbit review --prompt-only --type uncommitted`
  - Fix any issues found by CodeRabbit
- **Documentation update (BEFORE commit)**
  - Update `docs/plans/PLAN-*.md` with "Issues Encountered and Resolved"
  - Update `docs/daily-logs/YYYY-MM-DD.md` with implementation details
  - Document learnings for future reference
- **Single commit with everything**
  - Stage all changes: implementation + PLAN + daily log
  - Commit with descriptive message that mentions documentation updates
  - Example:
    ```bash
    git add src/feature.ts docs/plans/PLAN-feature.md docs/daily-logs/2025-11-13.md
    git commit -m "feat: Add new feature implementation

    - Add core functionality with type definitions
    - Fix edge cases found during testing
    - Update daily log with implementation details
    - Update PLAN with Issues and resolutions

    🤖 Generated with [Claude Code](https://claude.com/claude-code)

    Co-Authored-By: Claude <noreply@anthropic.com>"
    ```

### Key Principles

- **Never rush**: Small iterations prevent misunderstandings
- **Document discoveries**: Real issues > theoretical assumptions
- **Always pause**: Frequent Q&A keeps understanding aligned
- **CodeRabbit as gatekeeper**: Review before every progression

### ❌ DON'T DO THIS
- Implementing multiple functions at once
- Skipping CodeRabbit reviews
- Moving forward without confirmation
- Writing implementation in planning phase

## Documentation Structure

This project follows a standardized documentation structure. See `docs/README.md` for complete details.

## Code Quality Standards

- **No trailing whitespace**: Files must not contain trailing spaces or tabs on empty lines
- **Clean empty lines**: Empty lines should contain no characters (not even spaces)
- **Consistent indentation**: Use spaces consistently, no mixed tabs/spaces
