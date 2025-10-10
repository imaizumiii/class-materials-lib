from __future__ import annotations
from dataclasses import dataclass

from .base import Renderer
from ..document import Document
from ..nodes import Title, Section, Paragraph, Terms, TermItem, FigureSpace, ListBlock, PageBreak
from ..utils.text import latex_escape

@dataclass
class LatexRenderer(Renderer):
    docclass: str = "article"
    docclass_options: str = ""
    preamble: str = r"\usepackage{amsmath, amssymb}\n"
    begin_document: str = r""
    end_document: str = r""

    # ▼ 追加：add_terms タイトルの見た目（お好みでデフォルト変更OK）
    terms_title_marker: str = "●"      # 目印（例: "■" "◆" "●" "▶"）
    terms_title_bg: str = "blue!6"     # タイトル帯の背景色
    terms_title_fg: str = "black"      # タイトル文字色
    terms_box_arc: str = "5pt"         # 枠角の丸み
    terms_box_rule: str = "0.4pt"      # 枠線の太さ
    terms_box_sep: str = "6pt"         # 内側余白（padding）
    terms_box_before_skip: str = "20pt"  # 外側余白（margin）
    terms_box_after_skip: str = "6pt"   

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
        if isinstance(n, FigureSpace):
            return self._render_figure_space(n)
        if isinstance(n, ListBlock):
            return self._render_listblock(n)
        if isinstance(n, PageBreak):                  # ★ 追加
            return self._render_pagebreak(n)
        raise TypeError(f"Unsupported node: {type(n).__name__}")

    # path: lectgen/renderers/latex.py
    def _render_title(self, t: Title) -> str:
        title = t.title if t.raw else latex_escape(t.title)
        subtitle = ""
        if t.subtitle:
            subtitle_text = t.subtitle if t.raw else latex_escape(t.subtitle)
            # サブタイトルは小さめ・灰色
            subtitle = f"\\\\{{\\normalsize\\color{{gray!60}} {subtitle_text}}}"
        # tcolorbox で左帯＋角丸＋余白多め
        return (
            "\\begin{tcolorbox}[enhanced, sharp corners=southwest, arc=4pt, "
            "colback=white, colframe=gray!30, boxrule=0.4pt, boxsep=6pt, "
            "borderline west={3pt}{0pt}{blue!60}]\n"
            f"{{\\LARGE\\bfseries {title}}}{subtitle}\n"
            "\\end{tcolorbox}\n"
        )
    
    def _render_pagebreak(self, _: PageBreak) -> str:
    # \newpage でも良いが、未処理の浮動体を流したい時は \clearpage が堅い
        return "\\clearpage\n"
 # path: lectgen/renderers/latex.py
    def _render_section(self, s: Section) -> str:
        title = s.title if s.raw else latex_escape(s.title)
        margin_before = getattr(s, "margin_before", "-4pt")
        margin_after = getattr(s, "margin_after", "-4pt")
        return (
            f"\\vspace*{{{margin_before}}}\n"
            # tcbox はインライン箱。内容幅=タイトル幅になる
            "\\noindent\\tcbox[enhanced, colback=white, colframe=white, "
            "boxrule=0pt, left=0pt, right=0pt, top=10pt, bottom=2pt, "
            "borderline south={0.9pt}{0pt}{blue!60}]{"
            f"\\Large\\bfseries {title}"
            "}%\n"
            "\\par\n"
            f"\\vspace*{{{margin_after}}}\n"
        )

    def _render_paragraph(self, p: Paragraph) -> str:
        text = p.text if p.raw else latex_escape(p.text)
        return text

# path: lectgen/renderers/latex.py
    def _render_terms(self, ts: Terms) -> str:
        """
        add_terms を角丸ボックスで描画。title があれば
        tcolorbox の title 機能で「目印つき見出し」を付ける。
        - ts.title: 見出しテキスト
        - ts.content: 本文（string）。もし items 方式なら description を生成。
        """
        # --- 本文の組み立て（content 方式 / items 方式どちらでも動く） ---
        if hasattr(ts, "content") and isinstance(getattr(ts, "content"), str):
            body = ts.content
        else:
            # 旧: Terms(items=...) にも対応（保険）
            try:
                items = "\n".join(self._render_term_item(it) for it in ts.items)  # type: ignore[attr-defined]
                body = "\\begin{description}\n" + items + "\n\\end{description}"
            except Exception:
                body = ""

        # --- タイトル（目印付き）の作成 ---
        title_opt = ""
        if getattr(ts, "title", None):
            title_text = ts.title if getattr(ts, "raw", False) else latex_escape(ts.title)  # type: ignore[arg-type]
            # 見出しだけ大きくするが、サイズは見出しの中だけに閉じ込める
            title_latex = (
                "{\\large\\bfseries "
                f"{latex_escape(self.terms_title_marker)}\\;{title_text}"
                "}"
            )
            title_opt = f"title={{{title_latex}}}, fonttitle=\\bfseries, coltitle={self.terms_title_fg}, colbacktitle={self.terms_title_bg}"

        # --- tcolorbox で全体を出力 ---
        # タイトルがあるときは title オプション付き、ないときは通常ボックス
        options_common = (
            f"enhanced, boxrule={self.terms_box_rule}, arc={self.terms_box_arc}, "
            f"boxsep={self.terms_box_sep}, colback=white, colframe=black, "
            f"before skip={self.terms_box_before_skip}, after skip={self.terms_box_after_skip}"
        )
        if title_opt:
            options = options_common + (", " + title_opt if title_opt else "")
        else:
            options = options_common

        return (
            f"\\begin{{tcolorbox}}[{options}]\n"
            f"{body}\n"
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
        
    def _render_figure_space(self, fs: FigureSpace) -> str:
        """
        tcolorbox の tcbraster を用いて、flex風に横並びの空ボックス群を描画。
        横方向マージンは minipage の幅を縮めて確保。
        縦方向マージンは前後の \vspace* で確保。
        """
        # 安全側：個数が1未満なら1に
        cols = max(1, int(fs.count))

        # tcbraster の列間隔
        colskip = fs.gap

        # ラッパー（minipage）の幅 = 全幅 - 左右マージン
        wrap_begin = (
            f"\\par\\vspace*{{{fs.margin_top}}}%\n"
            f"\\noindent\\hspace*{{{fs.margin_left}}}%\n"
            f"\\begin{{minipage}}{{\\dimexpr\\linewidth - {fs.margin_left} - {fs.margin_right}\\relax}}\n"
        )
        wrap_end = (
            "\\end{minipage}%\n"
            f"\\hspace*{{{fs.margin_right}}}\\par\\vspace*{{{fs.margin_bottom}}}\n"
        )

        # 中の空ボックス（枠あり・角丸・指定の高さ）
        # boxsep=0pt, left/right/top/bottom=0pt で“純粋な空き領域”に近づける
        box_opts = (
            f"enhanced, colback=white, colframe=black, "
            f"boxrule={fs.rule}, arc={fs.arc}, "
            "boxsep=0pt, left=0pt, right=0pt, top=0pt, bottom=0pt, "
            f"height={fs.height}"
        )

        # tcbraster（columns=cols, raster column skip = gap）
        raster_begin = (
            "\\begin{tcbraster}["
            f"raster columns={cols}, "
            f"raster column skip={colskip}, "
            "raster left skip=0pt, raster right skip=0pt, "
            "raster before skip=0pt, raster after skip=0pt"
            "]\n"
        )
        raster_end = "\\end{tcbraster}\n"

        # 空ボックスを columns 個生成（中身は空）
        boxes = "".join(f"\\begin{{tcolorbox}}[{box_opts}]\\end{{tcolorbox}}\n" for _ in range(cols))

        return wrap_begin + raster_begin + boxes + raster_end + wrap_end
    
    def _render_listblock(self, lb: ListBlock) -> str:
        marker = latex_escape(getattr(lb, "title_marker", "●"))
        heading = (
            f"\\vspace*{{{lb.margin_before}}}\\noindent"
            f"\\textbf{{{marker}\\;{latex_escape(lb.title)}}}\\\\[-24pt]\n"
        )
        
        body = [f"  \\item {latex_escape(it)}" for it in lb.items]
        env = lb.style if lb.style in ("itemize", "enumerate") else "itemize"

        # ★ 角括弧を使わず、内部で余白を設定
        list_env = (
            f"\\begin{{{env}}}\n"
            "\\setlength{\\topsep}{2pt}%\n"
            "\\setlength{\\itemsep}{2pt}%\n"
            "\\setlength{\\parsep}{0pt}%\n"
            "\\setlength{\\partopsep}{0pt}%\n"
            + "\n".join(body)
            + f"\n\\end{{{env}}}"
        )

        content = heading + list_env + f"\\vspace*{{{lb.margin_after}}}\n"

        if lb.boxed:
            return (
                "\\begin{tcolorbox}[enhanced, colback=white, colframe=black, "
                "boxrule=0.4pt, arc=4pt, boxsep=6pt]\n"
                f"{content}\n"
                "\\end{tcolorbox}\n"
            )
        return content