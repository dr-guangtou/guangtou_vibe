# note-style Skill

This self-contained skill applies the owner's shared style to scientific notes,
research summaries, and engineering documentation. It uses Markdown, Sphinx,
MyST, and customized Furo.

## Included files

- [SKILL.md](SKILL.md) provides the agent workflow and skill trigger.
- [Rule book](references/note_style_guide.md) defines the requirements, examples,
  conversion process, and acceptance checks.
- [Furo starter](assets/starter/README.md) contains source examples, configuration,
  a uv lockfile, and locally hosted MathJax and math fonts with license notices.
- [Font integration](references/font_integration.md) explains the preferred Chinese
  font and how its separate license affects embedding.

## Installation

Copy this entire folder to `.agents/skills/note-style/` within another repository
for project-scoped discovery. For personal discovery across local repositories,
copy it to `~/.agents/skills/note-style/`. A symlink to the complete folder is also
supported for a local installation.

The copy should exclude `.venv/`, `_build/`, `__pycache__/`, and `.ruff_cache/`.
All remaining files, including the bundled vendor assets, are part of the package.
The build needs `uv` and the locked Python dependencies. A first environment setup
may download those dependencies. The generated sample's mathematical rendering
uses assets from its own static server.

## Example requests

```text
Use $note-style to convert this project's study notes into a Furo publication.
Preserve the original Markdown content and existing document identifiers.
```

```text
Use $note-style for a small HTML manual in this repository.
Start with one representative note and verify equations and navigation.
```

```text
Apply note-style to these engineering notes and check the rendered Chinese
and English text, references, equations, and dark/light behavior.
```

The user's proprietary Chinese font is supplied separately when its license
permits the intended use. The bundled profile works with its fallback fonts.

## Export a clean copy

From the skill folder, run the following command, choosing an archive location
outside the skill directory.

```sh
uv run --project assets/starter python scripts/package_skill.py /tmp/note-style.zip
```

The exporter includes the rule book, starter sources, lockfile, and local vendor
assets. It excludes environments, build outputs, and caches. Extract the archive
and copy its `note-style/` folder to the destination's skill directory.
