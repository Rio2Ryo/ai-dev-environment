---
name: git-workflow
description: Best practices for Git version control, branching strategies, commit messages, and collaboration workflows. Use this skill when managing code repositories, creating branches, writing commits, or handling merge conflicts.
---

# Git Workflow Skill

Professional Git practices for effective version control and team collaboration.

## Commit Message Convention

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change, no feature/fix |
| `perf` | Performance improvement |
| `test` | Adding tests |
| `chore` | Maintenance tasks |

### Examples

```
feat(auth): add OAuth2 login support

Implement Google and GitHub OAuth providers.
- Add OAuth callback handlers
- Store tokens securely
- Add user linking for existing accounts

Closes #123
```

```
fix(api): handle null response from payment gateway

The payment gateway occasionally returns null instead of
an error object. This caused unhandled exceptions.

Fixes #456
```

### Rules

- Subject line: max 50 characters, imperative mood
- Body: wrap at 72 characters
- Explain what and why, not how

## Branching Strategy

### Branch Naming

```
<type>/<ticket-id>-<short-description>

Examples:
feature/AUTH-123-oauth-login
fix/BUG-456-null-payment-response
hotfix/URGENT-789-security-patch
```

### Branch Types

| Branch | Purpose | Base | Merge To |
|--------|---------|------|----------|
| `main` | Production code | - | - |
| `develop` | Integration branch | main | main |
| `feature/*` | New features | develop | develop |
| `fix/*` | Bug fixes | develop | develop |
| `hotfix/*` | Urgent production fixes | main | main, develop |
| `release/*` | Release preparation | develop | main, develop |

### Workflow

```
main ─────────────────────────────────────────────►
  │                                    ▲
  │                                    │ merge
  ▼                                    │
develop ──────────────────────────────────────────►
  │         ▲         ▲         ▲
  │         │         │         │ merge
  ▼         │         │         │
feature/a ──┘         │         │
                      │         │
feature/b ────────────┘         │
                                │
fix/c ──────────────────────────┘
```

## Common Git Commands

### Daily Workflow

```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/TICKET-123-new-feature

# Work on feature
git add .
git commit -m "feat(module): implement feature"

# Keep up to date
git fetch origin
git rebase origin/develop

# Push and create PR
git push -u origin feature/TICKET-123-new-feature
```

### Useful Commands

```bash
# Interactive rebase (clean up commits)
git rebase -i HEAD~3

# Amend last commit
git commit --amend

# Stash changes
git stash
git stash pop

# Cherry-pick specific commit
git cherry-pick <commit-hash>

# View commit history
git log --oneline --graph --all

# Find who changed a line
git blame <file>

# Search commit messages
git log --grep="keyword"
```

## Handling Merge Conflicts

### Prevention

1. Pull frequently from base branch
2. Keep branches short-lived
3. Communicate with team about overlapping work

### Resolution Process

```bash
# 1. Update your branch
git fetch origin
git rebase origin/develop

# 2. When conflicts occur, Git marks them:
<<<<<<< HEAD
your changes
=======
their changes
>>>>>>> develop

# 3. Edit files to resolve conflicts

# 4. Mark as resolved
git add <resolved-files>

# 5. Continue rebase
git rebase --continue

# 6. Force push (if already pushed)
git push --force-with-lease
```

### Conflict Resolution Tips

- Understand both changes before resolving
- Test after resolving
- Use `git mergetool` for complex conflicts
- When in doubt, discuss with the other author

## Pull Request Best Practices

### Before Creating PR

- [ ] Rebase on latest base branch
- [ ] All tests pass
- [ ] Linting passes
- [ ] Self-review completed
- [ ] Documentation updated

### PR Description Template

```markdown
## Summary
Brief description of changes

## Changes
- Change 1
- Change 2

## Testing
How to test these changes

## Screenshots (if UI changes)
Before/After screenshots

## Checklist
- [ ] Tests added
- [ ] Documentation updated
- [ ] No breaking changes
```

### Review Process

1. Request review from appropriate team members
2. Address feedback promptly
3. Re-request review after changes
4. Squash commits if needed before merge

## Git Configuration

### Recommended Settings

```bash
# Set identity
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Default branch name
git config --global init.defaultBranch main

# Auto-prune on fetch
git config --global fetch.prune true

# Rebase by default on pull
git config --global pull.rebase true

# Better diff algorithm
git config --global diff.algorithm histogram

# Useful aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all"
```

## Emergency Procedures

### Undo Last Commit (not pushed)

```bash
git reset --soft HEAD~1  # Keep changes staged
git reset --mixed HEAD~1 # Keep changes unstaged
git reset --hard HEAD~1  # Discard changes
```

### Recover Deleted Branch

```bash
git reflog
git checkout -b recovered-branch <commit-hash>
```

### Revert Pushed Commit

```bash
git revert <commit-hash>
git push
```
