# path: lectgen/renderers/latex.py
from __future__ import annotations
from dataclasses import dataclass

from .base import Renderer
from ..document import Document
from ..nodes import Title, Section, Paragraph, Terms, TermItem
from ..utils.text import latex_escape

@dataclass
class LatexRenderer(Renderer):
    docclass: str = "article"
    preamble: str = r"\usepackage{amsmath, amssymb}\n"
    begin_document: str = r""
    end_document: str = r""

    # 既存の terms_box/terms_box_options があっても無視してOK（後方互換のため残してもよい）

    def render(self, doc: Document) -> str:
        body_parts: list[str] = []
        for n in doc.nodes:
            body_parts.append(self._render_node(n))
        body = "\n\n".join(bp for bp in body_parts if bp)
        return self._wrap_document(body)

    def _render_node(self, n) -> str:
        if isinstance(n, Title):
            return self._render_title(n)
        if isinstance(n, Section):
            return self._render_section(n)
        if isinstance(n, Paragraph):
            return self._render_paragraph(n)
        if isinstance(n, Terms):
            return self._render_terms(n)
        raise TypeError(f"Unsupported node: {type(n).__name__}")

    def _render_title(self, t: Title) -> str:
        title = t.title if t.raw else latex_escape(t.title)
        subtitle = ""
        if t.subtitle:
            subtitle_text = t.subtitle if t.raw else latex_escape(t.subtitle)
            subtitle = f"\\\\\\large {subtitle_text}"
        # \maketitle は使わない
        return f"\\begin{{center}}\n\\LARGE {title}{subtitle}\n\\end{{center}}"

    def _render_section(self, s: Section) -> str:
        title = s.title if s.raw else latex_escape(s.title)
        return f"\\section*{{{title}}}"

    def _render_paragraph(self, p: Paragraph) -> str:
        text = p.text if p.raw else latex_escape(p.text)
        return text

# path: lectgen/renderers/latex.py
    def _render_terms(self, ts: Terms) -> str:
        """
        すべての Terms を角丸の tcolorbox で描画する。
        ts.title があれば太字の見出しとして先頭に出す（サイズは見出し内だけ適用）。
        """
        heading = ""
        if ts.title:
            # ★ ここを { ... } で囲ってスコープ化。本文へサイズ指定が漏れない。
            heading = f"{{\\large\\textbf{{{latex_escape(ts.title)}}}}}\\par\n"

        content = heading + ts.content
        return (
            "\\begin{tcolorbox}[enhanced, colback=white, colframe=black, boxrule=0.4pt, arc=5pt]\n"
            f"{content}\n"
            "\\end{tcolorbox}\n"
        )

    def _render_term_item(self, item: TermItem) -> str:
        key = item.term if item.raw_key else latex_escape(item.term)
        val = item.definition if item.raw_value else latex_escape(item.definition)
        return f"  \\item[{key}] {val}"

    def _wrap_document(self, body: str) -> str:
        return (
            f"\\documentclass{{{self.docclass}}}\n"
            f"{self.preamble}\n"
            "\\begin{document}\n"
            f"{self.begin_document}\n"
            f"{body}\n"
            f"{self.end_document}\n"
            "\\end{document}\n"
        )