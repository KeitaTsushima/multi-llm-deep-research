# How to Write a PLAN

## When to Create a PLAN

Create a PLAN.md before implementing any non-trivial feature or change:
- New features
- Refactoring existing code
- Bug fixes that require design decisions
- Architecture changes

## PLAN Template Usage

Use `PLAN-template.md` as your starting point. The template is flexible for different scenarios:

### For New Feature Development

Focus on:
- **Goals**: What user problem does this solve?
- **Context**: Requirements, use cases, constraints
- **Proposed Solution**: Architecture, components, data flow
- **Implementation Steps**: Build order (often skeleton → core → integration)

Example: "PLAN: Add User Authentication"

### For Refactoring/Improvements

Focus on:
- **Goals**: What pain point are we addressing?
- **Context**: Current implementation with file:line references
- **Proposed Solution**: What will change and why
- **Implementation Steps**: Migration path (often backwards compatible)

Example: "PLAN: Refactor API Client for Testability"

### For Bug Fixes

Focus on:
- **Goals**: What is broken and why does it matter?
- **Context**: Current behavior, affected files, reproduction steps
- **Proposed Solution**: Root cause and fix approach
- **Testing Strategy**: How to verify the fix and prevent regression

Example: "PLAN: Fix Race Condition in Data Sync"

## Key Principles

1. **Be specific**: Use file:line references, not vague descriptions
2. **Think sequentially**: Implementation steps should be in build order
3. **Document uncertainties**: Open Questions section is important
4. **Plan for testing**: Write this BEFORE coding, not after
5. **Keep it concise**: 1-3 pages max, not a novel

## After Implementation

Update your PLAN with:
- **Issues Encountered and Resolved**: Real problems you hit
- **Decisions Changed**: Where you deviated from the plan and why
- **Learnings**: What you'd do differently next time

This makes the PLAN valuable for future reference and blog posts.

## Future Improvements → GitHub Issues

**Rule**: Don't write detailed future improvements in PLAN files. Use GitHub Issues instead.

**Why?**
- Issues are searchable and filterable
- Can track status (Open/Closed)
- Supports discussion and assignment
- Avoids stale documentation

**Workflow:**
1. Identify out-of-scope improvement during implementation
2. Create GitHub Issue with labels (`v1.x`, `enhancement`, `priority:*`)
3. Add link to PLAN's Future Improvements section

**Example command:**
```bash
gh issue create \
  --title "Add retry logic with exponential backoff" \
  --body "## Summary\n..." \
  --label "v1.x,enhancement"
```

**Labels to use:**
| Label | Purpose |
|-------|---------|
| `v1.x` | Planned for future version |
| `enhancement` | New feature |
| `code-quality` | Refactoring/improvement |
| `priority:medium` | Medium priority |
| `priority:low` | Low priority |
| `wontfix` | Won't implement (with reason) |
