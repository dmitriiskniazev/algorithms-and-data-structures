project = "Курс алгоритмов и структур данных"
copyright = "2026"
author = ""

language = "ru"
root_doc = "index"
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

extensions = ["myst_parser", "sphinx.ext.mathjax"]
myst_heading_anchors = 3
myst_enable_extensions = ["dollarmath"]

exclude_patterns = ["_build"]
html_theme = "alabaster"
