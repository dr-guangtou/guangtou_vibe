---
name: one-sentence
description: Summarize current development progress in 1-2 precise sentences using recent commits, working tree state, and recent session notes; optionally append the summary to today's Obsidian daily note.
---

# One-Sentence

Generate a precise, evidence-backed 1-2 sentence summary of recent development progress.

## Argument Handling

Accept optional arguments after `$one-sentence`:

- No argument or `session`: summarize recent session context.
- Git range (for example `HEAD~5..HEAD`): summarize commits in that range only.
- Time keyword (`today`, `week`, `month`): use `git log --since` for matching period.
- Free-text topic: focus summary on that topic while using the same evidence sources.
- `--record`: append the final summary to today's Obsidian daily note automatically.

Arguments can be combined, for example: `HEAD~10..HEAD --record`.

## Run This Workflow

1. Collect evidence.
   - Git commits:
     - Session/no args: `git log --oneline -20`
     - Range: `git log --oneline <range>`
     - Time: `git log --oneline --since="<period>"`
   - Working tree: `git diff --stat HEAD`
   - Recent repo journal notes (if present): `ls -t docs/journal/*.md 2>/dev/null | head -3`
   - Read most recent journal note when available.
   - Optional memory signal (Claude-compatible projects): check `~/.claude/projects/*/memory/MEMORY.md` and extract current-state section when relevant.
   - Optional task signal: if `docs/todo.md` exists, collect completed items.

2. Write the summary.
   - Produce exactly 1-2 sentences.
   - Use specific components/files rather than vague outcomes.
   - Use past tense.
   - Prefer one sentence; use two only when a key accomplishment and key remaining blocker both matter.
   - Omit meta-work unless meta-work was the primary activity.

3. Print output in exact format.
   - `[YYYY-MM-DD] <repo-name>: <summary>`
   - Date source: `date +%Y-%m-%d`
   - Repo name: `basename $(git rev-parse --show-toplevel)`
   - If not in a git repo, use current directory basename.

4. Record conditionally.
   - If `--record` is present, run:
     - `obsidian vault=wensai daily:append content="## Dev Snapshot\n\n> [YYYY-MM-DD] <repo>: <summary>"`
   - Confirm with: `Recorded to today's Obsidian journal.`
   - If `--record` is absent, ask whether to append instead of auto-writing.

## Output Quality Rules

- Do not invent facts.
- Keep scope faithful to the provided range/time/topic.
- Keep summary high-signal and compact.
