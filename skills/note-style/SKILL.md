---
name: note-style
description: Create, convert, or refine science and technical HTML documentation using the owner's note-style standard, with ordinary Markdown, Sphinx, MyST, and customized Furo. Use when the user mentions note-style or asks to apply this standard to research notes, engineering manuals, or project documentation.
---

# note-style

Use the bundled [rule book](references/note_style_guide.md) for the shared requirements and [starter](assets/starter/README.md) for implementation. All required source assets are inside this skill folder.

## Apply the standard

- Read the rule book before establishing or changing a documentation profile. Respect the target repository's instructions, source ownership, language, and publication scope.
- Use Sphinx, ordinary `.md` source through MyST, and customized Furo as the selected first implementation. Start from `assets/starter/` for a new publication. For an existing project, adapt the relevant configuration and assets while preserving its dependencies, identifiers, links, and content.
- Keep a restrained reading layout, desktop project navigation on the left, Chinese-capable and English typography, dark-first appearance with a saved reader preference, labelled mathematics, and support for small scientific interactive figures.
- Manage Python dependencies with `uv`. The starter's lockfile records the tested environment. Keep generated builds and virtual environments out of copied source packages.
- Serve the bundled MathJax runtime and its font packages from the generated static site. Preserve `docs/_static/vendor/` and its license notices when transferring the starter. Ordinary rendering uses Python tooling and the bundled browser assets.
- Read [font integration](references/font_integration.md) when using the owner's preferred Chinese font. Its binary is supplied separately under the applicable license.
- Build and verify one representative note before expanding a conversion. Check math, links, theme switching, responsive layout, keyboard access, and the publication's actual language and search requirements. Record the browser coverage and remaining limitations.
- Convert within the source project, then integrate the verified publication into the website. The destination's page scope remains governed by the owner and its specification.

## Transfer and use

Copy this complete `note-style/` folder into an agent skill directory. Read [README](README.md) for the included files, local installation, and example prompts. Paths inside the package are relative to this folder.

The workflow is self-contained. If Modern Web Guidance is available, consult it for new browser-facing functionality in accordance with the target environment's instructions.
