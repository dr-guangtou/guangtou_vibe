# Context Management (Context Window Management)

## 1) Concept and purpose

**Context management** is the disciplined practice of controlling **what the agent sees now**, **what must persist**, and **what should be excluded** so work remains correct, consistent, and reproducible across long sessions, large codebases, and large documents. It is the operational counterpart to **context window** limits (the working-memory capacity for input plus output).

### Core objective
Maintain a **high-signal working set** that contains:
- the current goal and success criteria,
- hard constraints and non-goals,
- the minimum necessary “source of truth” material (files, snippets, results),

while pushing everything else into **external artifacts** (notes, decision logs, tests, small reference files) that can be reloaded when needed.

## 2) General approaches and best practices

### 2.1 Build a layered “context stack”
Use layers so you can add/remove context without losing control.

1. **Persistent project guidance (always-on)**
   - Coding style, repo etiquette, how to run tests, key commands, forbidden actions/paths.
   - Keep it short and maintained.

   *Claude Code pattern:* `CLAUDE.md` is automatically pulled into context at session start and is intended to hold commands, core files, style, testing instructions, and repo etiquette.

2. **Task brief (per task)**
   - “What we’re doing, why, definition of done, constraints, acceptance checks.”
   - Put this near the top of your current prompt so it remains salient.

3. **Working set (per step)**
   - Only the few files/sections needed for *this* change or analysis.
   - Rotate aggressively: as soon as a file is no longer needed, stop including it and rely on external notes instead.

4. **External memory artifacts (durable, versioned)**
   - Decision log, assumptions, interfaces, data provenance, “how to reproduce,” links to notebooks/scripts.
   - Reload these after a reset/compaction.

### 2.2 Prefer “retrieve and summarize” over “keep everything”
As context grows, performance can degrade and noise accumulates. Best practice is:
- keep raw logs, long tool outputs, and bulky results **out of the main context** once decisions are made,
- store them in files,
- keep only the **conclusion** plus a pointer to the source.

### 2.3 Use explicit structure for long documents
When feeding large documents:
- Place long-form source material first and your query last.
- Ask for “grounding” (quote relevant excerpts before conclusions).
- When multiple documents are involved, wrap each with clear metadata tags.

### 2.4 Make “state” explicit to prevent drift
Use a small, consistent “state block” that you keep updated:

- **Current objective**
- **Constraints / non-goals**
- **Decisions made (with rationale)**
- **Open questions**
- **Next 3 actions**
- **Verification plan** (tests, plots, checks)

This reduces the chance the agent re-litigates earlier decisions after they drop out of context.

### 2.5 Token budgeting as an operational discipline
Many platforms enforce a combined limit: **prompt + generated output** must fit within the model’s maximum context. Practical rule:
- If you want a thorough answer, **do not fill the window** with inputs; leave headroom for output.

## 3) Tool- and platform-specific tactics

### 3.1 Claude Code (Anthropic): “memory files” as first-class context management
Claude Code provides a hierarchy of memory files loaded automatically into context (project, rules, user, and local project memory).

Key practices:
- Maintain a concise **project** `CLAUDE.md` (team-shared) and modular **rules** under `./.claude/rules/*.md` for topic-specific guidance.
- Use imports (`@path/to/file`) to pull only what’s needed, rather than bloating one file.
- Keep these files short and iterate on them like any frequently used prompt.

### 3.2 Claude (API / long context): optimize placement and grounding
- Put long documents first; put the query at the end; structure multi-document inputs; request quote-first grounding.

### 3.3 OpenAI API: prefix stability and caching economics
For repeated calls with the same base instructions:
- Put static content (instructions, examples, policies) at the **start**, and variable content at the end to improve prompt caching effectiveness.
- Prompt caching can reduce latency and input cost and works automatically for sufficiently long prompts.

### 3.4 Gemini (Google): long-context with caching, but watch “multiple needles”
Common guidance includes:
- query at end for long contexts,
- use context caching for repeated long materials,
- be mindful that performance can drop when you need to locate many separate facts in huge contexts.

### 3.5 IDE tools (e.g., Cursor): auto-context is helpful but can add noise
IDE tools may automatically attach relevant parts of your codebase. This reduces manual copying but increases the importance of constraining what is included to avoid irrelevant context.

## 4) A practical playbook you can adopt immediately

1. **Create a persistent project brief**
   - One page: commands, tests, style, data locations, “do not touch,” key references.
   - In Claude Code: `CLAUDE.md` (shared) + optional `CLAUDE.local.md` (private).

2. **Use a “task packet” per analysis/modeling effort**
   - `docs/task-<name>.md` containing:
     - objective, inputs, outputs, acceptance checks,
     - file list (“working set”),
     - decision log,
     - next steps.

3. **Compact aggressively**
   - When the thread gets long: summarize into the task packet and restart from:
     - the persistent project brief + the task packet + the current working set.

4. **Keep evidence close to claims**
   - For any conclusion from long docs/logs, store:
     - the conclusion,
     - the minimal excerpt (or a pointer),
     - and how to reproduce (command/script/notebook cell).

5. **Treat tests/plots as context**
   - Verification artifacts (unit tests, regression plots, summary tables) are high-signal anchors for correctness.

## 5) References (Markdown-ready)

- Anthropic — Effective context engineering for AI agents (compaction; structured note-taking) — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic — Claude Docs: Context windows (working-memory framing; token behavior) — https://platform.claude.com/docs/en/build-with-claude/context-windows
- Anthropic — Claude Docs: Long context prompting tips (document placement; structure; grounding) — https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/long-context-tips
- Anthropic — Claude Code Docs: Manage Claude’s memory (CLAUDE.md hierarchy; imports) — https://code.claude.com/docs/en/memory
- Anthropic — Claude Code best practices (CLAUDE.md guidance; context gathering costs) — https://www.anthropic.com/engineering/claude-code-best-practices
- OpenAI — API concepts (tokens; prompt + output within max context) — https://platform.openai.com/docs/concepts
- OpenAI — Prompt caching guide (prefix matching; structure prompts for caching) — https://platform.openai.com/docs/guides/prompt-caching
- OpenAI — Prompt engineering best practices (instructions first; clear structure) — https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api
- Google — Gemini API: Long context (query placement; context caching; limitations) — https://ai.google.dev/gemini-api/docs/long-context
- Cursor — Context overview / rules / mentions (IDE context attachment patterns) — https://cursor.com/learn/context
