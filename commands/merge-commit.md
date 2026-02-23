---
description: Commit all changes, then merge current branch into main
argument-hint: [optional commit message]
allowed-tools: Bash(git:*)
---

# Merge and Commit to Main

The user wants to finalize the current branch by committing all changes and merging into main.

## Step 1: Pre-flight checks

Run these commands and report the results:

1. `git branch --show-current` — confirm we're NOT already on main. If on main, STOP and tell the user.
2. `git status` — show uncommitted changes.
3. `git log --oneline main..HEAD` — show commits on this branch not yet in main.

## Step 2: Commit uncommitted changes

If there are staged or unstaged changes (modified/untracked files):

1. Stage all changes: `git add -A`
2. Commit with the user's message if provided via $ARGUMENTS, otherwise draft a concise commit message summarizing the changes.
3. Use the standard commit format with Co-Authored-By trailer.

If there are NO uncommitted changes, skip this step and say so.

## Step 3: Merge into main

1. Save the current branch name.
2. `git checkout main`
3. `git merge <branch-name> --no-ff` — use a merge commit to preserve branch history.
4. Report the merge result.

## Step 4: Cleanup

1. `git branch -d <branch-name>` — delete the merged branch.
2. `git log --oneline -5` — show the final state.

## Step 5: Confirm

Print a summary:
- Branch merged: `<name>`
- Commits merged: N
- Current branch: main
- Remind the user that changes are local only (not pushed).
