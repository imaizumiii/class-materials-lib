# path: lectgen/renderers/base.py
from __future__ import annotations
from typing import Protocol
from ..document import Document

class Renderer(Protocol):
    def render(self, doc: Document) -> str:
        """ドキュメント全体を文字列にレンダリング"""
        ...