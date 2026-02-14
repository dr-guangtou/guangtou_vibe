---
description: Save session context to files and prepare handover prompt for next session
argument-hint: [optional notes about current work]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git:*), Bash(date:*), Bash(ls:*), Task
---

# Session Handover

The user is ending this session to preserve context quality. Your job is to capture everything needed for the next session to continue seamlessly, with zero information loss.

## User's additional notes

$ARGUMENTS

## Step 1: Gather current state

Collect the following information by inspecting the codebase and recalling the conversation:

1. **Current goal**: What is the user working toward right now? What was the most recent request?
2. **Progress**: What has been completed in this session? List specific files changed, commits made, tests passed/failed.
3. **In-flight work**: What was in progress but not yet finished? Be specific about what remains.
4. **Problems and blockers**: Any errors, failed tests, design questions, or unresolved decisions.
5. **Key decisions made**: Architectural choices, tradeoffs, things that were tried and rejected (and why).
6. **Branch state**: Current branch, uncommitted changes, relationship to main.

Also run these commands to capture concrete state:
- `git status` and `git log --oneline -5` for repo state
- `git diff --stat` if there are uncommitted changes
- Check for any TODO items in docs/todo.md

## Step 2: Write journal entry

Create a file at `docs/journal/YYYY-MM-DD_handover.md` (use today's date). If a handover file already exists for today, append a suffix like `_2`, `_3`, etc.

Format:

```markdown
# Session Handover — YYYY-MM-DD

## Goal
[What the user is working toward]

## Completed This Session
- [Specific accomplishments with file paths and commit hashes]

## In Progress (Not Finished)
- [What remains, with specific next steps]

## Problems / Blockers
- [Any unresolved issues]

## Key Decisions
- [Choices made and rationale]

## Branch State
- Branch: [name]
- Uncommitted changes: [yes/no, summary]
- Relationship to main: [ahead by N commits, etc.]

## Files Modified This Session
- [List of files touched]
```

## Step 3: Update MEMORY.md

Read the current auto-memory file at the project's memory directory. Update the "Current State" section to reflect the actual state after this session. Be concise — MEMORY.md is loaded into every session's system prompt and must stay under 200 lines.

Do NOT duplicate the journal entry. MEMORY.md should contain only the key facts needed to orient the next session (current branch, what's done, what's next, any critical warnings).

## Step 4: Prepare the handover prompt

Compose a ready-to-paste prompt that the user can use to start the next session. This prompt should:

1. Point to the journal entry: "Read docs/journal/YYYY-MM-DD_handover.md for full context."
2. State the immediate next step in 1-2 sentences.
3. Mention any warnings or things to watch out for.

Print this prompt clearly at the end, wrapped in a code block so the user can copy it directly.

## Step 5: Confirm

Summarize what you wrote and where. List the files created/updated.
