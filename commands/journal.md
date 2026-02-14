---
description: Write a development journal entry summarizing the current session
argument-hint: [optional: focus, tone, or scope instructions in natural language]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git:*), Bash(date:*), Bash(ls:*), Task
---

# Development Journal

Write a concise development journal entry summarizing work done in the current session on this project.

## User's requirements for the summary

$ARGUMENTS

If the user provided requirements above, adapt the summary accordingly (e.g., focus area, tone, audience, level of detail, format). If blank, use the defaults below.

## Step 1: Gather context

Collect the following by inspecting the conversation history, codebase, and git state:

1. **What was done**: Features built, bugs fixed, refactoring, benchmarks run, decisions made.
2. **Key findings**: Surprising results, performance numbers, important tradeoffs discovered.
3. **Current state**: What works, what's left, any open questions.

Also run:
- `git log --oneline --since="$(date -v-16H +%Y-%m-%dT%H:%M:%S)" --until="$(date +%Y-%m-%dT%H:%M:%S)"` to see today's commits (adjust if the user mentions a different timeframe)
- `git diff --stat` for uncommitted changes
- Check `docs/todo.md` for overall progress context

## Step 2: Write the journal entry

**Default style** (override if the user requested something different):
- A few sentences in past tense, narrative prose (not bullet points)
- Technical but readable — suitable for the developer's own reference
- Mention specific numbers (test counts, benchmark results, line counts) where relevant
- Note key decisions and their rationale
- Note any surprises or lessons learned
- Keep it to one short paragraph unless the session was unusually productive

**File location**: `docs/journal/YYYY-MM-DD.md` (today's date). If the file already exists, append the new entry under a new `## Session N` heading (increment N based on existing entries). If creating a new file, use the format:

```markdown
# Journal — YYYY-MM-DD

## Session 1

[Entry here]
```

## Step 3: Confirm

Print the journal entry text directly so the user can review it. Mention the file path where it was saved. Ask if they want any changes.
