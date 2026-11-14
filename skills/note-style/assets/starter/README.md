# note-style Furo Starter

This is the first working implementation of the shared science and technical
documentation style. Sources are ordinary Markdown files rendered by Sphinx
through MyST and styled with Furo.

From this directory, run the following commands.

```sh
uv sync --locked
uv run sphinx-build -W --keep-going -b html docs _build/html
uv run python -m http.server 8765 --directory _build/html --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/signal_noise.html` for the sample scientific note.

Copy this directory's source files and `uv.lock` into a documentation project,
excluding `.venv/` and `_build/`. Change the project title, replace the sample
notes, and adopt the shared guide in the destination repository's agent manual.
When adding this starter to an existing Python project, merge its dependencies
and configuration with that project's tooling.

The customization uses Furo's palette and font variables, a small CSS file,
and an initial-theme template override. The existing Furo theme buttons are
retained, with a small handler that supports dark-first behavior, blocked
storage, and synchronization between tabs. Recheck this integration when
upgrading Furo.

The named body and code fonts are candidates with system fallbacks. Font
files are supplied by the reader's system in this starter. MathJax 4.1.3 and its
matching math fonts are bundled under `docs/_static/vendor/` and served from the
publication's own static files. Keep that directory and its license notices with
the publication. Final Chinese font assets, Chinese search, and an interactive
scientific figure remain part of the next profile refinement.

Run Ruff checks from this starter directory.

```sh
uv run ruff check docs/conf.py
uv run ruff format --check docs/conf.py
```

The included pre-commit configuration uses the same Ruff commands. In a new Git
repository, `uv run pre-commit install` installs those hooks. When adopting the
starter inside an existing project, merge the hooks with that project's tooling.

## Verification

The initial build passed with warnings treated as errors using Sphinx 9.1.1,
MyST parser 5.2.0, and Furo 2025.12.19. Ruff and JavaScript syntax checks passed.
The in-app browser verified dark-first loading, light-mode switching, preference
persistence after reload, rendered equations, and page reflow at a 360 CSS-pixel
viewport. Focused script checks covered blocked storage and cross-tab updates.
Firefox and Safari coverage remains to be checked with representative documents.
