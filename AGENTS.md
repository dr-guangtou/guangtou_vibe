# Agent Core Mandates (v2026.02.23)

## Principles & Logic

- **English Only**: All code, docs, commits, and logs must be in English.
- **Branch Strategy**: Never work on `main`. Always create feature branches. Do not merge without explicit permission.
- **Spec-Driven**: Maintain `docs/SPEC.md` as the source of truth for architecture. Interview the user for new/complex features to update the spec before coding.
- **Scaling & Epistemology**: Validate at small scale (sub-minute) before full execution. Never estimate numerical values; always benchmark and measure.
- **Constraint Persistence**: Persist new rules ("never X", "always Y") to `AGENTS.md` immediately.

## Code Style

- **Python/General**: Use `snake_case` (underscores) for everything. **Never use camelCase.**
- **Naming**: Use specific, complete words. Names must be clear to those unfamiliar with the codebase.
- **Comments**: No redundant comments that restate function/variable names.

## Workflow Orchestration

- **Lessons Loop**: Record mistakes and rationale in `docs/lessons.md`. Review this file at session start.
- **Task Tracking**: Use `docs/todo.md` for planning and tracking progress. Add a review section upon completion.
- **Pre-Implementation**: Review 3-5 similar files in the codebase to align with existing style/patterns before writing new code.
- **Elegance Check**: For non-trivial changes, pause to evaluate if a more elegant or simpler approach exists.

## Python Specifics

- **Package Management**: Use `uv` exclusively for dependencies (sync, lock, install). Never use pip, poetry, or conda.
- **Linting/Formatting**: Implement `pre-commit` using `Ruff` as the single source of truth. Keep hooks fast and actionable.
