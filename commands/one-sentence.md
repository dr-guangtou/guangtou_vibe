---
description: Summarize current development progress in 1-2 precise sentences
argument-hint: [git range like HEAD~5..HEAD | "today" | "week" | topic description | --record]
allowed-tools: Read, Glob, Grep, Bash(git:*), Bash(date:*), Bash(ls:*), Bash(obsidian:*)
---

# One-Sentence Development Summary

Generate a precise, accurate 1-2 sentence summary of recent development progress.

## Arguments

$ARGUMENTS

Parse the argument(s):
- **No argument / "session"**: summarize this context window — recent git commits plus in-session work recalled from conversation.
- **Git range** (e.g., `HEAD~5..HEAD`, `v1.2..HEAD`): summarize commits in that range only.
- **Time keyword** (`today`, `week`, `month`): use `git log --since` with the matching period (`1 day ago`, `1 week ago`, `1 month ago`).
- **Free text topic** (e.g., "the auth refactor"): focus summary on that topic while still reading the same git + journal sources.
- **`--record`**: after generating the summary, append it to the wensai Obsidian daily note automatically without asking.

Multiple flags can appear together, e.g. `HEAD~10..HEAD --record`.

---

## Step 1: Collect evidence

### Git commits

Run the appropriate git command (skip gracefully if not in a git repo):

- Session/no-args: `git log --oneline -20`
- Git range: `git log --oneline <range>`
- Time-based: `git log --oneline --since="<period>"`

Also run `git diff --stat HEAD` to surface any uncommitted changes.

### Journal files

Check for recent session journal or handover notes in the current repo:

```bash
ls -t docs/journal/*.md 2>/dev/null | head -3
```

Read the most recent file found (skip if the directory does not exist).

### Memory

Read the project MEMORY.md from the auto-memory directory. The path is derived from the current working directory, encoded as `~/.claude/projects/<encoded-path>/memory/MEMORY.md`. Try:

```bash
ls ~/.claude/projects/*/memory/MEMORY.md 2>/dev/null
```

Read the file that corresponds to the current project (match by path encoding or recency). Extract only the "Current State" or equivalent section.

### Task list

If `docs/todo.md` exists, extract completed items (`- [x]`) from it.

---

## Step 2: Write the summary

Synthesize all evidence into **exactly 1-2 sentences**. Hard rules:
- Be specific: name features, files, or components, not vague outcomes ("made progress on X" is banned).
- Past tense.
- One sentence is preferred; use two only when one captures a key accomplishment and the second captures a meaningful remaining item or blocker.
- Omit meta-work (updating MEMORY.md, writing handover notes, adjusting prompts) unless that was the primary session work.
- If the scope is narrow (e.g., a 3-commit range), reflect that accurately — do not inflate scope.

---

## Step 3: Output

Print the summary in this exact format:

```
[YYYY-MM-DD] <repo-name>: <summary>
```

Use `date +%Y-%m-%d` for the date and `basename $(git rev-parse --show-toplevel)` for the repo name. If not in a git repo, use the current directory basename.

---

## Step 4: Record (conditional)

**If `--record` was in the arguments**, append to the wensai Obsidian daily note automatically:

```bash
obsidian vault=wensai daily:append content="## Dev Snapshot\n\n> [YYYY-MM-DD] <repo>: <summary>"
```

Confirm with: `Recorded to today's Obsidian journal.`

**If `--record` was NOT in the arguments**, print the summary, then ask:

> Append this to today's Obsidian journal? (y/n)

If the user replies yes, run the same `obsidian daily:append` command above.
