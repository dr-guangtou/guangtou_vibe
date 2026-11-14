project = "note-style"
copyright = "2026, note-style contributors"
extensions = ["myst_parser", "sphinx.ext.mathjax"]
source_suffix = {".md": "markdown"}
root_doc = "index"
language = "en"
exclude_patterns = []
nitpicky = True
myst_enable_extensions = ["dollarmath", "colon_fence"]
numfig = True
math_numfig = True
mathjax_path = "vendor/mathjax/tex-mml-chtml.js"
mathjax_config_path = "mathjax_config.js"

html_theme = "furo"
html_title = "note-style"
html_static_path = ["_static"]
templates_path = ["_templates"]
html_css_files = ["note_style.css"]
html_js_files = ["note_style_theme.js"]
html_theme_options = {
    "top_of_page_buttons": [],
    "light_css_variables": {
        "font-stack": (
            '"Source Sans 3", "Source Han Sans SC", "Noto Sans CJK SC", '
            '"PingFang SC", "Microsoft YaHei", sans-serif'
        ),
        "font-stack--monospace": (
            '"IBM Plex Mono", "SFMono-Regular", Consolas, "PingFang SC", monospace'
        ),
        "color-brand-primary": "#236b69",
        "color-brand-content": "#236b69",
        "color-background-primary": "#fafaf8",
        "color-background-secondary": "#f0f1ee",
        "color-foreground-primary": "#262d31",
    },
    "dark_css_variables": {
        "color-brand-primary": "#83b5b2",
        "color-brand-content": "#83b5b2",
        "color-background-primary": "#171b20",
        "color-background-secondary": "#1d2329",
        "color-foreground-primary": "#dce1e5",
        "color-foreground-secondary": "#b0bac2",
    },
}
