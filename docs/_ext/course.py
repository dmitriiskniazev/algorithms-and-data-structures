"""Source presentation for the HTML course."""

from html import escape
from pathlib import PurePosixPath

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.directives.code import LiteralInclude
from sphinx.writers.html5 import HTML5Translator


class SourceDetails(nodes.General, nodes.Element):
    pass


def visit_source(translator: HTML5Translator, node: SourceDetails) -> None:
    title = escape(str(node["title"]))
    translator.body.append(f'<details class="source-details"><summary>Полный код · {title}</summary>')


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


def setup(app: Sphinx) -> dict[str, bool]:
    app.add_node(SourceDetails, html=(visit_source, depart_source))
    app.add_directive("literalinclude", CourseInclude, override=True)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
