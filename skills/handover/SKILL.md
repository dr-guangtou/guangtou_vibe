---
name: handover
description: Save session context to a handover note, record a one-sentence snapshot to Obsidian, and print a starter prompt for the next session. Use when the user types "/handover" or "$handover", or asks for a session handoff near context limits.
argument-hint: "[optional notes about current work] [--no-record]"
allowed-tools: Read, Write, Edit, Bash(bash:*), Bash(obsidian:*)
---

# Handover

Capture everything the next session needs, with zero information loss. The conversation is the main source; the repo state below is already collected, so do not re-run git commands.

User notes: $ARGUMENTS

## Repo state

!`bash "${CLAUDE_SKILL_DIR}/../one-sentence/scripts/evidence.sh"`

If the line above was not expanded (non-Claude agents), run once:
`bash <skills dir>/one-sentence/scripts/evidence.sh`

Session ID: ${CLAUDE_SESSION_ID}

## 1. Write the handover note

Path: `docs/journal/<date>_handover.md`; if it exists, use `_2`, `_3`, ... Use explicit paths and commands, distinguish facts from assumptions, and mark anything unchecked as `not yet verified`.

```markdown
# Session Handover - YYYY-MM-DD

## Goal
- Current objective / most recent request

## Completed This Session
- Specific accomplishments with file paths and commit IDs

## In Progress (Not Finished)
- Remaining work and immediate next actions

## Problems / Blockers
- Unresolved issues

## Key Decisions
- Decision, rationale, and approaches tried and rejected

## Branch State
- Branch / uncommitted changes / relationship to main

## Files Modified This Session
- `path/to/file`

## Verification
- Ran / result / not run yet and why

## Snapshot
- `[YYYY-MM-DD] <repo>: <one-sentence summary>`

---
*Session: <SESSION_ID> - resume with `claude --resume <SESSION_ID>`*
```

## 2. Update project memory (only if it exists)

If the evidence shows a "Project memory" section, update only its Current State section: branch, what is done, what is next, critical warnings. Do not duplicate the handover note.

## 3. Snapshot

Write the `## Snapshot` line yourself (do not invoke `/one-sentence`): 1 sentence (2 only if a key blocker must be included), past tense, concrete components, no meta-work. Unless `--no-record` was given, run once:

```bash
obsidian vault=wensai daily:append content="## Dev Snapshot\n\n> [<date>] <repo>: <summary>"
```

## 4. Finish

Reply briefly with: files created/updated, the snapshot line and whether it was recorded, and a ready-to-paste starter prompt in a fenced code block containing:
- `Read docs/journal/<file>.md for full context.`
- The immediate next step in 1-2 sentences.
- Warnings, constraints, or verification gaps.
