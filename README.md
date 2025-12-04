# Project Template

This is a standardized project template optimized for development with Claude Code and CodeRabbit.

## How to Use This Template

### Starting a New Project

1. Copy this template to your new project directory:
   ```bash
   cp -r ~/dev/project-templates/* ~/dev/your-new-project/
   cd ~/dev/your-new-project
   ```

2. Initialize git repository:
   ```bash
   git init
   git branch -m main
   git commit --allow-empty -m "Project start"
   ```

3. Customize project-specific files:
   - Update `README.md` (replace this template guide with project description)
   - Update `CLAUDE.md` (project name, specific rules)
   - Update `docs/project-overview.md` (purpose, tech stack)

4. Set up GitHub repository (if using GitHub):
   ```bash
   gh repo create your-repo-name --public --source=. --remote=origin
   git push -u origin main
   ```

5. Install CodeRabbit GitHub App (if using GitHub):
   - Visit https://github.com/apps/coderabbitai
   - Install for your repository

## What's Included

### Core Files
- `CLAUDE.md` - Claude Code project context and workflow
- `.coderabbit.yaml` - CodeRabbit configuration
- `.gitignore` - Standard ignore patterns

### Documentation Structure
- `docs/` - Complete documentation (see `docs/README.md` for full structure)
  - Project overview, daily logs, plans
  - Development guides (CodeRabbit, quality, testing)

## Development Workflow

This template uses an incremental development approach optimized for Claude Code:

- Plan before implementation (`docs/plans/`)
- Small iterations with frequent reviews (20-30 lines at a time)
- CodeRabbit review at each step
- Document progress in daily logs (`docs/daily-logs/`)

See `CLAUDE.md` for complete workflow details.

## Requirements

- Git installed
- CodeRabbit CLI installed (`curl -fsSL https://cli.coderabbit.ai/install.sh | sh`)
- Claude Code access
- GitHub account (optional, for PR reviews)

## Support

See individual documentation files for detailed guides:
- Development workflow: `CLAUDE.md`
- CodeRabbit usage: `docs/development/coderabbit-workflow.md`
- Quality standards: `docs/development/quality-guide.md`
- Testing guide: `docs/development/testing-guide.md`
- Documentation structure: `docs/README.md`
