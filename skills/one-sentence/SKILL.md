---
name: one-sentence
description: Summarize current development progress in 1-2 precise sentences and append it to today's Obsidian daily note. Use when the user types "/one-sentence" or "$one-sentence".
argument-hint: "[HEAD~5..HEAD | today | week | month | topic] [--no-record]"
model: haiku
context: fork
allowed-tools: Bash(bash:*), Bash(obsidian:*)
---

# One-Sentence

Cheap, single-pass task. Do not explore the repo or read extra files; the evidence below is enough.

Arguments: $ARGUMENTS

## Evidence

!`bash "${CLAUDE_SKILL_DIR}/scripts/evidence.sh" $ARGUMENTS`

If the line above was not expanded into evidence (non-Claude agents), run once:
`bash <this skill dir>/scripts/evidence.sh [git-range | today | week | month]`

## Write the summary

- Exactly 1-2 sentences, past tense. Prefer one; use two only for a key accomplishment plus a key remaining blocker.
- Name concrete features, files, or components. "Made progress on X" is banned.
- Stay within the requested range/time/topic; do not inflate scope or invent facts. If a git range or time keyword was given, summarize only those commits and ignore the Uncommitted section.
- Omit meta-work (handover notes, memory updates, prompt tweaks) unless it was the main work.
- Format: `[<date>] <repo>: <summary>` using `date` and `repo` from the evidence.

## Record

Unless arguments contain `--no-record`, run exactly one command:

```bash
obsidian vault=wensai daily:append content="## Dev Snapshot\n\n> [<date>] <repo>: <summary>"
```

Reply with only the summary line, then `Recorded to today's Obsidian journal.` (or `Not recorded: <error>` if the command failed).
