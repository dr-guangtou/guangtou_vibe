---
name: kimi-cli
description: Delegate coding tasks to Kimi CLI (Moonshot AI's coding agent). Use for building features, refactoring, PR reviews, and autonomous coding sessions. Requires the kimi CLI installed.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Coding-Agent, Kimi, Moonshot, Code-Review, Refactoring]
    related_skills: [claude-code, codex, opencode]
---

# Kimi CLI

Delegate coding tasks to [Kimi CLI](https://github.com/MoonshotAI/kimi-cli) via the Hermes terminal. Kimi CLI is Moonshot AI's autonomous coding agent that runs in the terminal.

## Prerequisites

- Kimi CLI installed via uv or pip
- Authenticated: run `kimi login` once to log in
- Use `pty=true` in terminal calls — Kimi CLI is an interactive terminal app

## One-Shot Tasks

```
terminal(command="kimi --print -p 'Add error handling to the API calls'", workdir="/path/to/project", pty=true)
```

For quick scratch work:
```
terminal(command="cd $(mktemp -d) && git init && kimi --print -p 'Build a REST API for todos'", pty=true)
```

## Background Mode (Long Tasks)

For tasks that take minutes, use background mode so you can monitor progress:

```
# Start in background with PTY
terminal(command="kimi --print -p 'Refactor the auth module to use JWT'", workdir="~/project", background=true, pty=true)
# Returns session_id

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Kill if needed
process(action="kill", session_id="<id>")
```

## Key Flags

| Flag | Effect |
|------|--------|
| `--print` | Non-interactive mode, exits when done (implicitly adds `--yolo`) |
| `--quiet` | Shortcut for `--print --output-format text --final-message-only` |
| `-p, --prompt "text"` | Pass prompt directly |
| `-y, --yolo` | Auto-approve all actions |
| `--thinking` / `--no-thinking` | Enable/disable thinking mode |
| `-m, --model <model>` | Specify LLM model |
| `-w, --work-dir <dir>` | Set working directory |
| `-C, --continue` | Continue previous session |
| `-S, --session <id>` | Resume specific session |

## Print Mode (Recommended for Automation)

Kimi's `--print` mode is designed for scripting:

```
# Basic print mode
kimi --print -p "List all Python files and their sizes"

# Quiet mode (only final output)
kimi --quiet -p "Generate a Git commit message for current changes"

# JSON output for programmatic use
kimi --print -p "Task" --output-format=stream-json
```

Exit codes:
- `0` - Success
- `1` - Failure (not retryable)
- `75` - Failure (retryable, e.g., rate limit)

## PR Reviews

Clone to a temp directory to avoid modifying the working tree:

```
REVIEW=$(mktemp -d) && git clone <repo> $REVIEW && cd $REVIEW && gh pr checkout 42 && kimi --print -p 'Review this PR against main. Check for bugs, security issues, and style.'
```

Or use git worktrees:
```
git worktree add /tmp/pr-42 pr-42-branch
kimi --print -p 'Review the changes in this branch vs main' --work-dir /tmp/pr-42
```

## Parallel Work

Spawn multiple Kimi instances for independent tasks:

```
terminal(command="kimi --print -p 'Fix the login bug'", workdir="/tmp/issue-1", background=true, pty=true)
terminal(command="kimi --print -p 'Add unit tests for auth'", workdir="/tmp/issue-2", background=true, pty=true)

# Monitor all
process(action="list")
```

## Sessions

Kimi maintains sessions automatically per working directory:

```
# Continue last session
kimi --continue

# Resume specific session
kimi --session <session-id>

# View session info
kimi info
```

## Additional Commands

| Command | Purpose |
|---------|---------|
| `kimi login` | Authenticate with Moonshot AI |
| `kimi logout` | Clear credentials |
| `kimi info` | Show version and protocol info |
| `kimi mcp` | Manage MCP server configurations |
| `kimi web` | Launch web interface |
| `kimi term` | Run Toad TUI |
| `kimi vis` | Launch Agent Tracing Visualizer |

## Configuration

Config file location: `~/.kimi/config.toml`

Environment variables:
- `KIMI_API_KEY` - API key for authentication
- `KIMI_BASE_URL` - Custom API endpoint

## Rules

1. **Always use `pty=true`** — Kimi CLI is an interactive terminal app and may hang without a PTY
2. **Use `--print` for one-shots** — Non-interactive mode exits cleanly
3. **Use `--quiet` for clean output** — Only returns the final result
4. **Background for long tasks** — use `background=true` and monitor with `process` tool
5. **Check exit codes** — `75` means retryable (rate limit), `1` means permanent failure
6. **Don't interfere** — monitor with `poll`/`log`, be patient with long-running tasks
