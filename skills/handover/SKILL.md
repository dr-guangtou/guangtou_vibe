---
name: handover
description: Create a clean context handover package for software projects. Use when the user asks for session handoff, context preservation, or types "$handover" (or asks for "/handover") near context limits. Produce a detailed summary file, a next-session starter prompt, and an optional Obsidian-ready development snapshot.
---

# Handover

Create a structured handover that preserves technical context with minimal information loss.

## Run This Workflow

1. Gather current state.
   - Capture current goal, recent request, completed work, in-flight work, blockers, and key decisions.
   - Run `git status --short --branch` and `git log --oneline -5`.
   - If there are uncommitted changes, run `git diff --stat`.
   - If `docs/todo.md` exists, extract current TODO and completed items.
   - Best-effort session ID lookup for Claude compatibility: `ls -t ~/.claude/session-env/ | head -1`.

2. Write the handover summary file.
   - Path pattern: `docs/journal/YYYY-MM-DD_handover.md`.
   - If the file exists, append numeric suffixes: `_2`, `_3`, and so on.
   - Use `references/handover-template.md` as the canonical structure.
   - Include concrete file paths, commands, and verification status.

3. Update project memory (if available).
   - If a project memory file exists (for example under `~/.claude/projects/*/memory/MEMORY.md`), update only the concise current-state section.
   - Keep the memory file short and high-signal; avoid duplicating full handover notes.

4. Generate a one-sentence development snapshot.
   - Follow the same rules as the `one-sentence` skill.
   - Output format: `[YYYY-MM-DD] <repo-name>: <summary>`.
   - Keep to 1 sentence by default; use 2 only when a key remaining blocker must be included.

5. Optionally record the snapshot in Obsidian.
   - Only auto-append when the user requested recording or provided an equivalent flag.
   - Command:
     - `obsidian vault=wensai daily:append content="## Dev Snapshot\n\n> [YYYY-MM-DD] <repo>: <summary>"`
   - If recording was not requested, provide the command and ask the user whether to run it.

6. Prepare a next-session starter prompt.
   - At the end of the response, provide a ready-to-paste prompt in a fenced code block.
   - It must include:
     - `Read docs/journal/YYYY-MM-DD_handover.md for full context.`
     - Immediate next step in 1-2 sentences.
     - Any warnings, constraints, or verification gaps.

7. Confirm completion.
   - List created or updated files.
   - Include the handover summary file path and the generated starter prompt.

## Output Quality Rules

- Use explicit paths and commands.
- Distinguish facts from assumptions.
- Do not invent results; mark unknowns as `not yet verified`.
- Keep wording concise and operational.

## Minimal Adaptation Guidance

- If the repository has an existing handover convention, follow it.
- Cross-reference `docs/todo.md` and `docs/SPEC.md` when they exist.
- If no implementation changed, still capture decisions and pending actions.
