# path: lectgen/document.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Sequence, Optional

from .nodes import (
    Node, Title, Paragraph, Terms, Section, TermItem,
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