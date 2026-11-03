"""Source presentation for the HTML course."""

from html import escape
from pathlib import Path, PurePosixPath

from docutils import nodes
from reader_sources import sources_json
from reader_themes import build_themes
from sphinx.application import Sphinx
from sphinx.directives.code import LiteralInclude
from sphinx.writers.html5 import HTML5Translator


class SourceDetails(nodes.General, nodes.Element):
    pass


def visit_source(translator: HTML5Translator, node: SourceDetails) -> None:
    title = escape(str(node["title"]))
    translator.body.append(
        f'<details class="source-details"><summary class="source-header"><span class="source-label">Полный код · {title}</span></summary>'
    )


def depart_source(translator: HTML5Translator, node: SourceDetails) -> None:
    translator.body.append("</details>")


class CourseInclude(LiteralInclude):
    def run(self) -> list[nodes.Node]:
        title = str(PurePosixPath(self.arguments[0]))
        while title.startswith("../"):
            title = title[3:]
        self.options["caption"] = title
        result = super().run()
        blocks = [block for node in result for block in node.findall(nodes.literal_block)]
        if not blocks:
            return result
        for block in blocks:
            block["course_path"] = title
        lines = sum(bool(line.strip()) for block in blocks for line in block.astext().splitlines())
        if lines <= 24:
            return result
        wrapper = SourceDetails("", title=title)
        for node in result:
            # The summary already contains the real path.
            for caption in list(node.findall(nodes.caption)):
                if caption.parent is not None:
                    caption.parent.remove(caption)
            wrapper += node
        return [wrapper]


def reader_assets(app: Sphinx) -> None:
    target = Path(app.outdir) / "_static/reader/themes"
    target.mkdir(parents=True, exist_ok=True)
    build_themes(Path(app.srcdir) / "_static/reader/themes/catalog.json", target)


def reader_context(
    app: Sphinx, pagename: str, templatename: str, context: dict[str, object], doctree: nodes.document | None
) -> None:
    context["reader_sources"] = sources_json(Path(app.srcdir).parent, doctree)


def setup(app: Sphinx) -> dict[str, object]:
    app.add_node(SourceDetails, html=(visit_source, depart_source))
    app.add_directive("literalinclude", CourseInclude, override=True)
    app.connect("builder-inited", reader_assets)
    app.connect("html-page-context", reader_context)
    return {"env_version": 1, "parallel_read_safe": True, "parallel_write_safe": True}
