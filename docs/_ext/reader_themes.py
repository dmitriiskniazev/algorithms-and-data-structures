"""Build the course's theme palettes and Pygments rules from one catalog."""

import json
from pathlib import Path

from pygments.formatters import HtmlFormatter
from pygments.style import Style
from pygments.styles import get_style_by_name
from pygments.token import Comment, Keyword, Name, Number, Operator, String, Text, Token


def mix(first: str, second: str, amount: float) -> str:
    a, b = first.lstrip("#"), second.lstrip("#")
    return "#" + "".join(
        f"{round(int(a[i : i + 2], 16) * (1 - amount) + int(b[i : i + 2], 16) * amount):02x}" for i in (0, 2, 4)
    )


def build_themes(catalog_path: Path, target: Path) -> None:
    catalog = json.loads(catalog_path.read_text())
    output = ["/* Theme adaptations: Pygments 2.21 palettes; Verdandi MIT notice in base.css. */"]
    for theme in catalog:
        if "colors" in theme:
            colors = theme["colors"]
            bg, fg = colors["background"], colors["text"]
            comment, keyword, string = (colors["comment"], colors["keyword"], colors["string"])
            emphasis = theme.get("emphasis", {})
            style = type(
                "CourseStyle",
                (Style,),
                {
                    "background_color": bg,
                    "styles": {
                        Token: colors.get("code_text", fg),
                        Keyword: f"{emphasis.get('keyword', '')} {keyword}".strip(),
                        String: f"{emphasis.get('string', '')} {string}".strip(),
                        Comment: comment,
                        Operator: f"{emphasis.get('operator', '')} {colors.get('operator', fg)}".strip(),
                        Number: colors.get("number", "#986801" if theme["kind"] == "light" else "#d19a66"),
                        Name.Function: colors.get("name", fg),
                        Name.Class: colors.get("name", fg),
                        Name.Decorator: colors.get("name", fg),
                        Name.Builtin: colors.get("name", fg),
                    },
                },
            )
        else:
            style = get_style_by_name(theme["style"])
            bg = style.background_color
            fg = (
                style.style_for_token(Text)["color"]
                or style.style_for_token(Token)["color"]
                or ("d8dce0" if theme["kind"] == "dark" else "212529")
            )
            fg = "#" + fg.lstrip("#")
        dark = theme["kind"] == "dark"
        muted = mix(bg, fg, 0.76)
        border = mix(bg, fg, 0.28)
        surface = mix(bg, fg, 0.055)
        tokens = {
            "page": bg,
            "surface": bg,
            "surface-muted": surface,
            "ink": fg,
            "muted": muted,
            "border": border,
            "accent": fg,
            "wash": surface,
            "sidebar": surface,
            "code": bg,
            "focus": "#8ac9ff" if dark else "#0757a8",
            "diff-added": mix(bg, "#1b813e", 0.3 if dark else 0.12),
            "diff-removed": mix(bg, "#b22222", 0.3 if dark else 0.08),
            "diff-added-marker": "#9ce8a8" if dark else "#176c2d",
            "diff-removed-marker": "#ffb0b0" if dark else "#a51d28",
            "syntax-text": "#" + (style.style_for_token(Token)["color"] or fg).lstrip("#"),
        }
        for token, name in [
            (Keyword, "keyword"),
            (String, "string"),
            (Number, "number"),
            (Comment, "comment"),
            (Name.Function, "name"),
        ]:
            tokens["syntax-" + name] = "#" + (style.style_for_token(token)["color"] or fg).lstrip("#")
        selector = f':root[data-theme="{theme["id"]}"], .theme-card[data-theme="{theme["id"]}"]'
        output.append(
            selector
            + "{"
            + ";".join(f"--{key}:{value}" for key, value in tokens.items())
            + f";color-scheme:{theme['kind']}"
            + "}"
        )
        scope = f':root[data-theme="{theme["id"]}"] .source-code'
        formatter = HtmlFormatter(style=style)
        output.append(scope + "{font-weight:inherit;font-style:normal}")
        output.append(
            scope
            + " :where(span:not([class^='diff-']):not(.code-space):not(.sr-only):not(.code-row):not(.code-line-content):not(.code-line-number)){font-weight:inherit;font-style:normal;background:transparent}"
        )
        for rules in (formatter.get_background_style_defs(scope), formatter.get_token_style_defs(scope)):
            output.extend(rules if isinstance(rules, list) else [rules])
    (target / "palettes.css").write_text("\n".join(output) + "\n")
