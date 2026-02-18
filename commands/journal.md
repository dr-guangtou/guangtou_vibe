---
description: Write a development journal entry summarizing the current session into the wensai Obsidian vault
argument-hint: [optional: focus, tone, or scope instructions in natural language]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git:*), Bash(date:*), Bash(ls:*), Bash(mkdir:*), Bash(python3:*), Bash(obsidian:*), Task
---

# Development Journal

Write a development journal entry summarizing work done in the current session and save it into the `wensai` Obsidian vault under `development/[REPO_NAME]/`.

## User's requirements for the summary

$ARGUMENTS

If the user provided requirements above, adapt the summary accordingly (e.g., focus area, tone, audience, level of detail). If blank, use the defaults below.

---

## Step 1: Gather repo context

Run all of the following to collect identifiers:

```bash
REPO_NAME=$(basename $(git rev-parse --show-toplevel))
BRANCH=$(git rev-parse --abbrev-ref HEAD)
TODAY=$(date +%Y-%m-%d)
```

Also collect:
- `git log --oneline --since="$(date -v-16H +%Y-%m-%dT%H:%M:%S)"` for recent commits (macOS syntax; on Linux omit `-v-16H` and use `--since="16 hours ago"`)
- `git diff --stat` for uncommitted changes
- Check `docs/todo.md` for overall progress context if it exists

---

## Step 2: Locate the vault

Try to get the vault root path via the Obsidian CLI:

```bash
obsidian vault=wensai vault info=path 2>/dev/null
```

If that fails (empty output or error), use python3 to search for the vault by looking for known candidate paths from `~/.claude/projects/` or common locations like `~/work/wensai`, `~/Documents/wensai`, `~/wensai`. A valid vault root contains an `.obsidian/` subdirectory.

```python
import os, subprocess

candidates = [
    os.path.expanduser("~/work/wensai"),
    os.path.expanduser("~/Documents/wensai"),
    os.path.expanduser("~/wensai"),
]
vault_path = None
for c in candidates:
    if os.path.isdir(os.path.join(c, ".obsidian")):
        vault_path = c
        break
if vault_path:
    print(vault_path)
else:
    print("")
```

If no valid vault is found, fall back to writing `docs/journal/YYYY-MM-DD.md` inside the current repo. Warn the user clearly that the vault was not found and the entry was saved locally instead.

---

## Step 3: Resolve the output path

```
DEST_DIR  = $VAULT_PATH/development/$REPO_NAME/
BASE_NAME = ${REPO_NAME}_${BRANCH}_${TODAY}
```

- If `DEST_DIR` does not exist: create it with `mkdir -p "$DEST_DIR"` and warn the user to add an entry for `$REPO_NAME` to `development/repo.yaml` in the vault.
- Filename collision check: if `$DEST_DIR/$BASE_NAME.md` already exists, try `$BASE_NAME_2.md`, `$BASE_NAME_3.md`, and so on until a free name is found. **Never overwrite an existing file.**

---

## Step 4: Write the journal entry

**Default style** (override if the user requested something different):
- Bullet-point style, past tense, technical but readable
- Mention specific numbers (counts, benchmark results) where relevant
- Note key decisions and their rationale
- Note any surprises or lessons learned

**File format:**

```markdown
---
date: YYYY-MM-DD
tags:
  - development
  - development/REPO_NAME
---

# REPO_NAME — BRANCH — YYYY-MM-DD

## Progress
- [What was built, fixed, or decided this session]

## Current State

### Key Issues
- [Open problems or blockers]

### Next Steps
- [Concrete, actionable items]

## Lessons Learned
- [Insights, gotchas, decisions and rationale]

---
*Agent: Claude Code (claude-sonnet-4-6) · Session: SESSION_ID*
```

**Session ID**: Use `$CLAUDE_CODE_SESSION_ID` if set. If the env var is unavailable, insert the placeholder `[paste session ID here]` and tell the user to fill it in (or pass it as `$ARGUMENTS`).

---

## Step 5: Confirm

Print the full file path where the entry was saved and show a preview of the content. Ask the user if they want any changes.
