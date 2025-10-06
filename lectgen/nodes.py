# path: lectgen/nodes.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, List

# 表示はレンダラに委譲（DIP）。Nodeはデータのみを持つ。
class Node(Protocol):
    pass

@dataclass(frozen=True)
class Title:
    title: str
    subtitle: str | None = None
    raw: bool = False  # TrueならそのままLaTeXに流す

@dataclass(frozen=True)
class Section:
    title: str
    raw: bool = False

@dataclass(frozen=True)
class Paragraph:
    text: str
    raw: bool = False

@dataclass(frozen=True)
class TermItem:
    term: str
    definition: str
    raw_key: bool = False
    raw_value: bool = True

@dataclass(frozen=True)
class Terms:
    content: str
    title: str | None = None
    boxed: bool = False
    
@dataclass(frozen=True)
class FigureSpace:
    """
    PDF化後に図を貼るための“空き箱”を並べるためのノード。
    高さ・本数・外側マージン・角丸・枠線・箱間ギャップを指定。
    すべて TeX の長さ（pt, mm, cm 等）で指定可能。
    """
    height: str = "50pt"      # 各ボックスの高さ（既定: 50pt）
    count: int = 1            # ボックスの個数（横に並べる）
    margin_top: str = "0pt"   # 上外側マージン
    margin_bottom: str = "0pt"# 下外側マージン
    margin_left: str = "0pt"  # 左外側マージン
    margin_right: str = "0pt" # 右外側マージン
    gap: str = "6pt"          # ボックス間ギャップ（横）
    arc: str = "4pt"          # 角丸
    rule: str = "0.4pt"       # 枠線の太さ
    
@dataclass(frozen=True)
class ListBlock:
    """
    箇条書きリスト。
    - items: 箇条書き項目（文字列のリスト）
    - title: 見出し（任意）
    - style: 'itemize' または 'enumerate'
    - boxed: 枠で囲むかどうか
    """
    items: List[str]
    title: str | None = None
    title_marker: str = "●"
    style: str = "itemize"
    boxed: bool = False
    margin_before: str = "6pt"  # タイトルの上余白
    margin_after: str = "6pt"   # 箇条書き全体の下余白