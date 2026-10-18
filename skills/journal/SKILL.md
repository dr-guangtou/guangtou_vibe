---
name: journal
description: Write a concise development journal entry for the current session into the wensai Obsidian vault (Progress, Current State, Lessons Learned) and append a one-sentence snapshot to today's Obsidian daily note. Use when the user types "/journal" or "$journal", or asks for a dev journal, checkpoint, or retrospective note.
argument-hint: "[optional focus, tone, or scope instructions] [--no-record]"
allowed-tools: Write, Bash(bash:*), Bash(mkdir:*)
---

# Journal

Summarize this session's work from the conversation plus the repo state below. Do not re-run git commands or search for the vault; everything needed is collected here.

User requirements (override the default style if given): $ARGUMENTS

## Repo state

!`bash "${CLAUDE_SKILL_DIR}/../one-sentence/scripts/evidence.sh"`

If the line above was not expanded (non-Claude agents), run once:
`bash <skills dir>/one-sentence/scripts/evidence.sh`

Session ID: ${CLAUDE_SESSION_ID}

## Write the entry

- Destination: the `journal_target` path from the evidence (already collision-free; never overwrite). Run `mkdir -p` on its directory first; if the directory is new, remind the user to add the repo to `development/repo.yaml` in the vault.
- If `journal_target` is missing (vault not found), write `docs/journal/<date>.md` in the repo and warn the user.
- Default style: short past-tense bullets, concrete (what changed, numbers, decisions and rationale, surprises). Facts only; do not invent missing details.

```markdown
---
date: YYYY-MM-DD
repo: REPO_NAME
branch: BRANCH_NAME
tags:
  - development
  - development/REPO_NAME
---

# REPO_NAME - BRANCH - YYYY-MM-DD

## Progress
-

## Current State

### Key Issues
-

### Next Steps
-

## Lessons Learned
-

---
*Agent: <agent and model> · Session: <SESSION_ID>*
```

## One-sentence snapshot

Write `[<date>] <repo>: <summary>`: 1 sentence (2 only if a key blocker must be included), past tense, concrete components, no meta-work, no invented facts. Unless `--no-record` was given, run once:

```bash
bash "${CLAUDE_SKILL_DIR}/../one-sentence/scripts/append_snapshot.sh" "[<date>] <repo>: <summary>"
```

It appends the line under the existing `## Dev Snapshot` heading of today's daily note (adding the heading once if missing) by writing the note file directly; it does not use the Obsidian CLI, which can hang. Non-Claude agents: run `<skills dir>/one-sentence/scripts/append_snapshot.sh`.

## Finish

Print only the saved journal path, the snapshot line, and whether it was recorded (no full preview).
