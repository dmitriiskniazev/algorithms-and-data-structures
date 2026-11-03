import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "_ext"))

project = "Курс алгоритмов и структур данных"
copyright = "2026"
author = ""

language = "ru"
root_doc = "index"
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}

extensions = ["myst_parser", "sphinx.ext.mathjax", "sphinx_design", "course"]
myst_heading_anchors = 3
myst_enable_extensions = ["dollarmath", "colon_fence"]

exclude_patterns = ["_build"]
html_theme = "alabaster"
html_static_path = ["_static"]
html_css_files = [
    "course.css",
    "reader/themes/palettes.css",
    "fonts/fonts.css",
    "reader/settings/panel.css",
    "reader/code_viewer/view.css",
    "reader/view.css",
    "reader/source.css",
]
html_js_files = ["course-print.js", ("course-code.mjs", {"type": "module"}), ("reader/start.js", {"type": "module"})]
templates_path = ["_templates"]
html_sidebars = {"**": ["course-navigation.html"]}
html_theme_options = {"show_powered_by": False, "show_related": True}
html_title = "Алгоритмы и структуры данных"
pygments_style = "github-dark"
html_show_sourcelink = False
