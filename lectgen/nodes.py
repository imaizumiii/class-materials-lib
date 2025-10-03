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