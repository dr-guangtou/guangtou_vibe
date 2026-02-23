---
name: merge-commit
description: Commit all changes, then merge the current branch into main. Use when the user wants to finalize a feature branch by committing all work and merging it back to the main branch with a merge commit.
---

# Merge and Commit to Main

Finalize the current branch by committing all changes and merging into main.

## Run This Workflow

1. Pre-flight checks.
   - Run `git branch --show-current` to confirm we're NOT already on main. If on main, STOP and tell the user.
   - Run `git status` to show uncommitted changes.
   - Run `git log --oneline main..HEAD` to show commits on this branch not yet in main.

2. Commit uncommitted changes.
   - If there are staged or unstaged changes (modified/untracked files):
     - Stage all changes: `git add -A`.
     - Commit with the user's message if provided as an argument, otherwise draft a concise commit message summarizing the changes.
     - Use standard commit formatting.
   - If there are NO uncommitted changes, skip this step.

3. Merge into main.
   - Save the current branch name.
   - `git checkout main`.
   - `git merge <branch-name> --no-ff` — use a merge commit to preserve branch history.
   - Report the merge result.

4. Cleanup.
   - `git branch -d <branch-name>` — delete the merged branch.
   - `git log --oneline -5` — show the final state.

5. Confirm.
   - Print a summary:
     - Branch merged: `<name>`
     - Commits merged: N
     - Current branch: main
     - Remind the user that changes are local only (not pushed).

## Output Quality Rules

- Do not proceed if the current branch is main.
- Ensure all changes are committed before merging.
- Use `--no-ff` to ensure a merge commit is created.
- Confirm successful merge and branch deletion.
