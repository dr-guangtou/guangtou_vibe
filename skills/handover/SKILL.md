---
name: handover
description: Create a clean context handover package for software projects. Use when the user asks for session handoff, context preservation, or types "$handover" (or asks for "/handover") near context limits. Produce a journal snapshot of progress, key files, goals, and next steps, plus a concise first prompt for the next clean session.
---

# Handover

Create a structured handover when context is getting tight or when the user explicitly asks.

## Workflow

1. Confirm or infer the project journal location.
- Prefer `docs/journal/` when it exists.
- If missing, create `docs/journal/` in the current workspace.

2. Gather current session state.
- Collect completed work, in-progress work, and blockers.
- Collect key reference files that matter for continuation.
- Collect the current main goal and immediate next steps.
- Collect verification status: what was tested, what was not tested, and why.

3. Write a timestamped handover journal entry.
- Path pattern: `docs/journal/handover-YYYY-MM-DD-HHMM.md`.
- Use the structure from `references/handover-template.md`.
- Keep entries concise, factual, and action-oriented.
- Include exact file paths and runnable commands for resuming.

4. Write a concise first prompt for the next clean session.
- Path pattern: `docs/journal/next-session-prompt-YYYY-MM-DD-HHMM.md`.
- Keep it short (6-12 lines).
- Include: goal, current status, key files, first 1-3 actions, and verification command(s).

5. Report completion to the user.
- Return both file paths.
- Inline the first prompt text so it can be used immediately.

## Output quality rules

- Use explicit file paths; avoid vague references.
- Distinguish facts from assumptions.
- Do not invent results; mark unknowns as "not yet verified".
- Prefer numbered next steps with concrete commands.
- Keep wording concise to reduce context carryover noise.

## Minimal adaptation guidance

- If the repository already has a handover convention, follow it.
- If `docs/todo.md` or `docs/spec.md` exists, cross-reference relevant sections.
- If no implementation changed, still record analysis decisions and pending actions.
