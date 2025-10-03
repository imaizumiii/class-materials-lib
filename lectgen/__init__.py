# path: lectgen/__init__.py
from __future__ import annotations
from .document import Document
from .renderers.latex import LatexRenderer

__all__ = ["Document", "LatexRenderer"]