# CodeRabbit Workflow Guide

**Detailed reference for CodeRabbit CLI commands, configuration, and troubleshooting.**

**For the complete development workflow, see `CLAUDE.md` "Code Implementation Procedure" section.**

---

## Common Commands

### CLI Review Commands

```bash
# Review uncommitted changes (most common)
coderabbit review --prompt-only --type uncommitted

# Review all changes in repository
coderabbit review --prompt-only --type all

# Review with detailed output (not optimized for AI)
coderabbit review --plain

# Review against specific base branch
coderabbit review --prompt-only --base develop
```

### PR Reviews (Automatic)

CodeRabbit automatically reviews all pull requests when:
1. CodeRabbit GitHub App is installed on the repository (one-time setup)
2. `.coderabbit.yaml` is configured with `auto_review: enabled: true`

If auto-review doesn't trigger, manually trigger with:

```text
@coderabbitai review
```

### Check Authentication

```bash
coderabbit auth status
```

---

## GitHub Branch Protection (Solo Projects)

CodeRabbit PR reviews require branch protection to enforce PR workflow.

### Recommended Settings for Solo Projects

| Setting | Value | Reason |
|---------|-------|--------|
| Direct push to main | ❌ Blocked | Force PR workflow for CodeRabbit |
| Approval required | ✅ 1 person | For external PRs |
| CodeRabbit pass required | ✅ | Ensure code quality |
| enforce_admins | ❌ false | Owner can bypass approval (but still sees CodeRabbit) |

### Why This Configuration?

**Problem:** Solo projects face a conflict:

- Want main push blocked → PR required
- Want approval required → Can't approve own PRs

**Solution:**

- Approval required for external contributors
- Owner bypasses approval (enforce_admins: false)
- CodeRabbit pass still provides quality gate

**Trade-off:**

- Owner can push directly to main (must self-enforce PR workflow)
- External PRs require both approval + CodeRabbit pass

### Setup Commands

```bash
# Set branch protection
gh api repos/OWNER/REPO/branches/main/protection -X PUT \
  --input - <<EOF
{
  "required_status_checks": {
    "strict": false,
    "contexts": ["CodeRabbit"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1
  },
  "restrictions": null
}
EOF
```

---

## Integration with Claude Code

### Typical Prompts

**During implementation:**

```text
[After implementing a function]
Run CodeRabbit review and fix any issues
```

**Verify fixes:**

```text
Run CodeRabbit again to verify all issues are resolved
```

---

## Review Modes

### --prompt-only (Recommended for Claude Code)

- Token-efficient output
- Optimized for AI consumption
- Specific file locations and suggestions
- Use with Claude Code

### --plain

- Detailed human-readable output
- Full feedback with explanations
- Use for manual review

### Interactive (default)

- Full UI with browsable findings
- Not suitable for automation

---

## Understanding CodeRabbit Output

### CLI Output Structure

```text
File: data_processor.py
Line: 47 to 51
Type: potential_issue

Prompt for AI Agent:
In data_processor.py around lines 54 to 59, the current sanitize_input
function strips a fixed set of characters which is insecure...
```

### PR Output Structure

**Summary by CodeRabbit:**

- High-level overview
- Walkthrough of changes
- Changes table

**Review comments:**

- Actionable comments (must fix)
- Nitpick comments (suggestions)
- Additional context

**Pre-merge checks:**

- Failed checks (warnings/errors)
- Passed checks

---

## Best Practices

### Handling CodeRabbit Suggestions

**Prioritize:**
1. Security issues
2. Bugs and logic errors
3. Performance problems
4. Code quality improvements
5. Style suggestions (optional)

**Ignore when:**
- False positives
- Project-specific patterns
- Over-optimization for prototypes

---

## Troubleshooting

### CodeRabbit Not Commenting on PR

**Cause:** Auto-review disabled or misconfigured

**Solution:**
1. Check `.coderabbit.yaml` exists in main branch
2. Verify `base_branches: [".*"]`
3. Manually trigger: `@coderabbitai review`

### Different Results: CLI vs PR

**Cause:** CodeRabbit is incremental

**Solution:**
- CLI reviews uncommitted changes
- PR reviews committed changes
- Ensure you're comparing same code state

---

## Related Files

- **Complete Development Workflow**: `../../CLAUDE.md` "Code Implementation Procedure"
- **Quality Standards**: [Quality Guide](./quality-guide.md)
- **Testing Strategy**: [Testing Guide](./testing-guide.md)
- **Configuration**: `../../.coderabbit.yaml`
