---
name: wrap-up
description: Finish a feature branch in one go - write the dev journal plus one-sentence Obsidian snapshot, commit remaining work, merge into main/master with --no-ff, delete the branch, and push. Use only when the user types "/wrap-up" or "$wrap-up".
argument-hint: "[no-push] [commit message]"
disable-model-invocation: true
allowed-tools: Write, Skill, Bash(bash:*), Bash(mkdir:*), Bash(obsidian:*), Bash(git:*)
---

# Wrap Up

Arguments: $ARGUMENTS
- `no-push`: do everything except pulling/pushing the remote.
- Any other text: the commit message for uncommitted work.

## 1. Journal + snapshot (first, while still on the feature branch)

Run the `journal` skill (Claude: invoke it with the Skill tool; other agents: follow `../journal/SKILL.md`). It writes the vault entry and appends the one-sentence snapshot to Obsidian. Its repo-state evidence (`branch`, `default_branch`, `remote`, uncommitted files) is reused below; do not re-collect it.

## 2. Pre-flight

- If `branch` equals `default_branch` (or is `none`), STOP the git steps and tell the user: nothing to merge.
- If untracked files appear that were not created in this session, do not stage them; list them in the final report.

## 3. Commit

If there are uncommitted changes: `git add -u` plus untracked files created this session, then commit with the user's message or a concise drafted one (follow the repo's commit conventions and any required attribution lines). Skip if clean.

## 4. Merge

```bash
git checkout <default_branch>
git pull --ff-only          # skip if no-push or no remote
git merge --no-ff <branch>
git branch -d <branch>
```

On a pull or merge failure or conflict: stop, leave the repo as is, and report. Never force, reset, or delete with `-D`.

## 5. Push

Unless `no-push` was given or there is no remote: `git push <remote> <default_branch>`.

## 6. Report

One short block: journal path, snapshot line (recorded or not), branch merged and commit count, push status (or "local only"), untracked files left behind, and `git log --oneline -3`.
