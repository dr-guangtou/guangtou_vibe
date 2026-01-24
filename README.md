# Guangtou's Vibe Coding Experience 

- I want to use this repo to keep a record of the useful resources, configurations, and files for my own "vibe coding", or agentic development experiment. 

## Agentic Developing Tools 

### Command Line Tools 

- [`claude-code` - An agentic coding tool that lives in your terminal](https://github.com/anthropics/claude-code)
  - [Claude code's official website](https://claude.com/product/claude-code) 
- [`gemini-cli` - An open-source AI agent that brings the power of Gemini directly into your terminal](https://github.com/google-gemini/gemini-cli)
  - [Gemini CLI's official document](https://docs.cloud.google.com/gemini/docs/codeassist/gemini-cli)
- [`opencode` - The open source coding agent](https://github.com/anomalyco/opencode)
  - [OpenCode's official website](https://opencode.ai/)
- [OpenAI's `codex` - Lightweight coding agent that runs in your terminal](https://github.com/openai/codex)
  - [`Codex`'s official website](https://openai.com/codex/)

### IDE-Based Tools

- [`Cursor` - The AI Code Editor](https://github.com/cursor/cursor)
  - [`Cursor`'s official website](https://cursor.com/home?from=agents)
  - [`Cursor` command line interface](https://cursor.com/cli)
- [Google `Antigravity`](https://antigravity.google/)
- [`TRAE` - Chinese version](https://www.trae.cn/)
  - [`TRAE` - International version](https://www.trae.ai)
- [`Qoder` - An Agentic Coding Platform](https://qoder.com/)
  - [`Qoder` command line interface](https://qoder.com/cli)

### Utilities

#### General Purpose

- [`AGENTS.md` — a simple, open format for guiding coding agent](https://github.com/agentsmd/agents.md)
  - [`AGENTS.md` website](https://agents.md/)
  - "README.md for agent": AGENTS.md complements this by containing the extra, sometimes detailed context coding agents need: build steps, tests, and conventions that might clutter a README or aren’t relevant to human contributors.

- [`SKILLS.sh` - The open agent skills ecosystem](https://skills.sh/)
  - Skills are reusable capabilities for AI agents. Install them with a single command to enhance your agents with access to procedural knowledge.

- [`Superpowers` - Claude Code superpowers: core skills library](https://github.com/obra/superpowers)
  - `Superpowers` is a complete software development workflow for your coding agents, built on top of a set of composable "skills" and some initial instructions that make sure your agent uses them.

- [`agentskills` - Specification and documentation for Agent Skills, a simple, open format for giving agents new capabilities and expertise](https://github.com/agentskills/agentskills)
  - The [website for Agent Skills](https://agentskills.io/home)
  - [The public repository for Agent Skills maintained by Antropics](https://github.com/anthropics/skills)

- [`claude_code_bridge` - Real-time multi-AI collaboration: Claude, Codex & Gemini with persistent context, minimal token overhead](https://github.com/bfly123/claude_code_bridge)
  - New Multi-Model Collaboration Tool via Split-Pane Terminal Claude & Codex & Gemini & OpenCode Ultra-low token real-time communication, unleashing full CLI power

#### MCP

- [`Context7` - Up-to-date Docs for LLMs and AI code editors](https://context7.com/)
  - [The `GitHub` repository for `Context7`](https://github.com/upstash/context7)
 
- [`PlayWright` MCP Server](https://github.com/microsoft/playwright-mcp)
  - A Model Context Protocol (MCP) server that provides browser automation capabilities using [Playwright](https://playwright.dev/).

- [`exa-mcp-server` - Exa MCP for web search and web crawling](https://github.com/exa-labs/exa-mcp-server)
  - [`exa` MCP documents](https://exa.ai/docs/reference/exa-mcp)

#### For Claude Code 

- [`gastown` - multi-agent workspace manager](https://github.com/steveyegge/gastown)
- [`planning-with-files` - Claude Code skill implementing Manus-style persistent markdown planning](https://github.com/OthmanAdi/planning-with-files)
- [`obsidian-skills` - Claude Skills for Obsidian](https://github.com/kepano/obsidian-skills/)
- [`autocoder` - A long-running autonomous coding agent powered by the Claude Agent SDK](https://github.com/leonvanzyl/autocoder?tab=readme-ov-file)
- [`Continuous-Claude-v3` - Context management for Claude Code](https://github.com/parcadei/Continuous-Claude-v3)
  - A persistent, learning, multi-agent development environment built on Claude Code.
- [`claude-scientific-skills` - A set of ready-to-use scientific skills for Claude](https://github.com/K-Dense-AI/claude-scientific-skills)

- [`cc-wf-studio` - CC (Claude code / GitHub Copilot) Workflow Studio](https://github.com/breaking-brake/cc-wf-studio)
  - Design complex AI agent workflows intuitively with drag-and-drop. Build Sub-Agent orchestrations and conditional branching without writing code, then export directly to `.claude` format for immediate execution.
 
- [`Claude` for Excel](https://claude.com/claude-in-excel)

#### For OpenCode 

- [`oh-my-opencode` - OpenCode plugin with async subagents](https://github.com/code-yeongyu/oh-my-opencode)

#### For TRAE 

- [`trae-agent` - an LLM-based agent for general-purpose software engineering tasks](https://github.com/bytedance/trae-agent)

--- 

## Glossary

- [Hook - Claude Code](https://github.com/dr-guangtou/guangtou_vibe/blob/main/glossary/hook.md)
- [Context Window](https://github.com/dr-guangtou/guangtou_vibe/blob/main/glossary/context_window.md)
- [Context Management](https://github.com/dr-guangtou/guangtou_vibe/blob/main/glossary/context_management.md)
- [Subagent - Claude Code]()
- [Skill - Claude Code]()
- [Plan Mode - Claude Code]()
- [MCP]()

## Useful Resources 

### Curated Lists

- [Awesome Claude Code Subagents](https://github.com/VoltAgent/awesome-claude-code-subagents?tab=readme-ov-file)
  - A collection of Claude Code subagents - specialized AI agents designed for specific development tasks.
- [`everything-claude-code` - Complete Claude Code configuration collection](https://github.com/affaan-m/everything-claude-code)
  - This repo contains production-ready agents, skills, hooks, commands, rules, and MCP configurations 

### Tutorials

- [Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/)


#### The "Ralph Wiggum" Technique

- [`ralph-playbook` - A comprehensive guide to running autonomous AI coding loops using Geoff Huntley's Ralph methodology](https://github.com/ClaytonFarr/ralph-playbook)
  - [The formatted view of the playbook](https://claytonfarr.github.io/ralph-playbook/)

- [`how-to-ralph-wiggum` - The Ralph Wiggum Technique—the AI development methodology that reduces software costs to less than a fast food worker's wage](https://github.com/ghuntley/how-to-ralph-wiggum)

- [`awesome-ralph` - A curated list of resources about Ralph, the AI coding technique that runs AI coding agents in automated loops until specifications are fulfilled](https://github.com/snwfdhmp/awesome-ralph)

#### Claude Code 

- [Claude Cookbook - Practical guides and examples for using Claude effectively](https://platform.claude.com/cookbook)
  - Not all of these cookbooks are from the official source.
 
- [Claude Code: Best practices for agentic coding by Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices)
  - This is from Apr 2025; some of these suggestions might be outdated.

- [Claude Code Project Configuration Showcase](https://github.com/ChrisWiles/claude-code-showcase)
  - Comprehensive Claude Code project configuration example with hooks, skills, agents, commands, and GitHub Actions workflows.

#### Misc 

- [`doom-coding` - A guide for how to use your smartphone to code anywhere at anytime](https://github.com/rberg27/doom-coding)

### Others 

- [System Prompts and Models of AI Tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)
- [Demystifying evals for AI agents by Anthropic](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
