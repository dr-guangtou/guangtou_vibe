---
name: journal
description: Create faithful, concise Obsidian markdown journal notes for software work. Use when asked to summarize development progress, lessons learned, and key issues or next steps for a repository session, checkpoint, handoff, or retrospective.
---

# Journal

## Run This Workflow

1. Identify repository context from the workspace:
   - Repository name
   - Current branch name
   - Date in `YYYY-MM-DD`
2. Collect factual inputs from the active session (changes made, tests run, decisions, blockers).
3. Write one Obsidian note using this filename format:
   - `[REPOSITORY_NAME]_[BRANCH_NAME]_[YYYY-MM-DD].md`
4. Add Obsidian properties at the top with at least:
   - `date`
   - `repo`
   - `tags`
5. Write only concise bullet points in three sections:
   - `## Progress`
   - `## Lessons Learned`
   - `## Key Issues`

## Writing Rules

- Prefer facts over interpretation; do not invent missing details.
- Use short, unambiguous bullets.
- Keep wording concrete (what changed, what failed, what is blocked, what is next).
- Put open questions and immediate next actions under `## Key Issues`.

## Output Template

Use `skills/journal/references/note-template.md` as the canonical structure.
