# Agentic Coding Concept: Hooks (Claude Code as the reference)

- From OpenAI's ChatGPT

## 1) What a “hook” is (purpose and applications)

A **hook** is a **user-defined command** that runs automatically at specific points in an agentic coding tool’s workflow (for example: *before a tool runs*, *after a tool runs*, *when a session starts/ends*). The primary purpose is **reliable workflow control**: tasks you want to happen *every time* (formatting, checks, logging, notifications, guardrails) become automatic rather than “best effort.”

**Professional team analogy:** Hooks behave like always-on automated teammates:
- A **quality gate** (e.g., “run checks before changes land”),
- A **build/CI bot** (e.g., “run formatting/tests after edits”),
- A **compliance/safety officer** (e.g., “block risky operations unless approved”).

## 2) How to use hooks in Claude Code (very brief)

**Interactive setup**
1. In Claude Code, run: ` /hooks `
2. Choose a **hook event** (e.g., **PreToolUse**).
3. Add a **matcher** to constrain when it runs (e.g., only for the shell tool; `*` can match all tools).
4. Add the command to run.
5. Save as either:
   - **User settings** (applies across all projects), or
   - **Project settings** (shared within the repository if committed).

**File-based setup**
Claude Code also supports editing JSON settings files directly, adding a `hooks` section.

## 3) Key hook events (practical view)

Common event categories:
- **Before actions**: gatekeeping and validation (e.g., PreToolUse).
- **After actions**: formatting, tests, indexing, logging (e.g., PostToolUse).
- **Session boundaries**: initialization and wrap-up (e.g., SessionStart, SessionEnd).
- **User interactions / notifications**: prompt submit, attention-required alerts, stop signals.

In Claude Code, some hooks can **allow/deny/ask** before a tool runs, and can sometimes **modify inputs** before execution. Treat this as high-leverage control.

## 4) Best practices (research-focused)

1. **Start with observability**  
   Prefer low-risk hooks first:
   - logging tool usage (reproducibility),
   - notifications,
   - post-edit formatting.

2. **Use matchers aggressively**  
   Constrain hooks to specific tools, file types, or directories to avoid noise and slowdown.

3. **Scope correctly**  
   - **User hooks**: personal productivity (notifications, general formatting).
   - **Project hooks**: collaboration standards (formatting rules, tests, guardrails).

4. **Treat hooks as production automation**  
   Hooks run with your account’s privileges. Use safe defaults:
   - validate inputs, quote variables, avoid destructive operations,
   - exclude sensitive paths (keys, credentials, environment files),
   - test in a scratch area before enabling broadly.

## 5) How “hooks” are adopted across tools (similarities and differences)

All hook systems share the same core idea: **automatic scripts at defined workflow points**. The main differences are:
- **Event richness** (how many lifecycle points are supported),
- **Control power** (notify-only vs gate/modify),
- **Config style** (interactive vs config files; JSON input, etc.).

### Comparison table (Markdown compatible)

| Tool / ecosystem | What “hooks” are used for | Implementation style | Strengths | Limitations / risks |
|---|---|---|---|---|
| **Claude Code (Anthropic)** | Workflow automation across lifecycle events; can gate actions and sometimes modify tool inputs | `/hooks` interactive + JSON settings | Strong control layer for enforcing project policy (formatting, checks, guardrails) | High power implies higher operational/security responsibility |
| **Gemini CLI (Google)** | Similar: run scripts on defined hook points; can receive structured input (JSON) | Config + scripts (stdin JSON) | Good for logging and consistent automation; portable scripting approach | Also inherits security/operational responsibility; event/control model differs by tool |
| **Codex CLI (OpenAI)** | Event-based notifications via external program (notify) | Config-driven | Low-friction alerts for long-running work | More notification-oriented; less of a full “gate/modify” lifecycle system |
| **Git hooks (baseline concept)** | Enforce repository invariants at Git lifecycle points (e.g., pre-commit) | Local scripts in `.git/hooks/` | Tool-agnostic enforcement; blocks bad commits reliably | Not shared by default; varies across developer machines unless standardized |
| **pre-commit framework** | Standardized, shareable pre-commit checks across languages/tools | `.pre-commit-config.yaml` | Best practice for team consistency and tool-agnostic enforcement | Adds setup overhead; primarily Git-lifecycle scoped |

## 6) References (Markdown-ready)

- Anthropic — Claude Code “Hooks guide” — https://code.claude.com/docs/en/hooks-guide  
- Anthropic — Claude Code “Hooks reference” — https://code.claude.com/docs/en/hooks  
- Anthropic — Claude Code “Settings” (locations; `hooks` key) — https://code.claude.com/docs/en/settings  
- OpenAI — Codex “Advanced configuration” (notify) — https://developers.openai.com/codex/config-advanced/  
- Google — Gemini CLI “Writing hooks” — https://geminicli.com/docs/hooks/writing-hooks/  
- Git Book — “Customizing Git: Git Hooks” — https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks  
- pre-commit — “Introduction” — https://pre-commit.com/  

----

# From Gemini 3 Pro 

## 1. General Introduction of Concepts 

**Primary Purpose**: To enforce consistency, automate repetitive "housekeeping" tasks, and provide the AI agent with immediate feedback on whether its changes have broken the project. Applications: Automatically running a suite of astronomical data validation tests after the agent modifies a reduction script, or auto-formatting Python code to meet `PEP 8` (Python Enhancement Proposal 8) standards before a commit.

**Professional Team Role**: Think of a Hook as a Quality Assurance (QA) Specialist or a Gatekeeper. Before a developer (the AI) is allowed to say "I'm finished," the Gatekeeper steps in and says, "Hold on, let me run the standard tests and check the formatting first." If the tests fail, the developer is immediately notified to fix it before the work is considered "done."

## 2. Implementation and Tool Adoption

In Claude Code specifically, hooks are often defined in a configuration file (like `CLAUDE.md`). They tell the agent: "Every time you think you are finished with a task, you must run this specific command first."

- Comparison of Hook-like Features across Tools

| Tool | Feature Name | Implementation Method | Best For | Pros / Cons |
| :--- | :--- | :--- | :--- | :--- |
| **Claude Code** | **CLAUDE.md Hooks** | Defined in a markdown file as shell commands. | Project-specific rules and testing. | **+** Very simple to set up; **-** Specific to Claude's CLI. |
| **Cursor** | **Rules for AI** | Rules defined in `.cursorrules` file. | Formatting and linting. | **+** Global "vibes" for coding; **-** Less "event-driven" than Claude. |
| **OpenCode** | **Workflow Hooks** | Scripted YAML files. | Highly customized pipelines. | **+** Extremely powerful; **-** High configuration overhead. |
| **Google Antigravity** | **Pre-flight Checks** | Integrated UI settings. | Ensuring code compiles. | **+** User-friendly; **-** Less flexible for custom scripts. |
| **Standard Git** | **Git Hooks** | Scripts in the `.git/hooks` folder. | Universal enforcement. | **+** Works with/without AI; **-** Manual setup. |

**Very Brief Introduction to Use**

To use a hook in Claude Code, you simply create a section in your `CLAUDE.md` file:
- **Define the Build/Test Command**: Tell Claude how to verify the code (e.g., `pytest`).
- **Automation**: When you ask Claude to "Fix the bug in the light curve analysis," Claude will automatically run that test command after its edit to ensure the fix works.

## 3. References 

### References for Hooks and Automation in Agentic Coding

1.  **Anthropic Documentation.** *Configuring Claude Code with CLAUDE.md*. [https://docs.anthropic.com/claude/docs/claude-code-config](https://docs.anthropic.com/claude/docs/claude-code-config)
2.  **Git-SCM.** *Customizing Git - Git Hooks*. [https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
3.  **Cursor Guide.** *Defining Project Rules (.cursorrules)*. [https://docs.cursor.com/context/rules-for-ai](https://docs.cursor.com/context/rules-for-ai)
4.  **Python Software Foundation.** *PEP 8 – Style Guide for Python Code*. [https://peps.python.org/pep-0008/](https://peps.python.org/pep-0008/)
