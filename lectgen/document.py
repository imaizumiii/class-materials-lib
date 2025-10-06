# path: lectgen/document.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Sequence, Optional

from .nodes import (
    Node, Title, Paragraph, Terms, Section, TermItem, FigureSpace
)

@dataclass
class Document:
    """授業資料（ノードのコンテナ）"""
    nodes: List[Node] = field(default_factory=list)

    # 直感的なAPI（KISS）
    def add_title(self, title: str, subtitle: Optional[str] = None, *, raw: bool = False) -> None:
        self.nodes.append(Title(title=title, subtitle=subtitle, raw=raw))

    def add_paragraph(self, text: str, *, raw: bool = False) -> None:
        self.nodes.append(Paragraph(text=text, raw=raw))

    def add_section(self, title: str, *, raw: bool = False) -> None:
        self.nodes.append(Section(title=title, raw=raw))

    def add_terms(
        self,
        content: str,
        *,
        title: str | None = None,
        boxed: bool = False
    ) -> None:
        """
        用語集を文字列として追加。
        title: 見出し
        boxed: True の場合はレンダラ側で枠付きで表示
        """
        self.nodes.append(Terms(content=content, title=title, boxed=boxed))
        
    def add_figure_space(
        self,
        *,
        height: str = "50pt",
        count: int = 1,
        margin_top: str = "0pt",
        margin_bottom: str = "0pt",
        margin_left: str = "0pt",
        margin_right: str = "0pt",
        gap: str = "6pt",
        arc: str = "4pt",
        rule: str = "0.4pt",
    ) -> None:
        """
        図をあとから貼るための“空きボックス”を横並びで作る。
        - height: 各ボックスの高さ（例 "50pt"）
        - count: ボックスの個数（例 3）
        - margin_*: 外側マージン（上下左右）
        - gap: ボックス同士の横間隔
        - arc: 角丸
        - rule: 枠線の太さ
        """
        self.nodes.append(
            FigureSpace(
                height=height,
                count=count,
                margin_top=margin_top,
                margin_bottom=margin_bottom,
                margin_left=margin_left,
                margin_right=margin_right,
                gap=gap,
                arc=arc,
                rule=rule,
            )
        )