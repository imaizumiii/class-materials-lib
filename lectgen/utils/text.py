# path: lectgen/utils/text.py
from __future__ import annotations

_LATEX_SPECIALS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}

def latex_escape(s: str) -> str:
    """
    LaTeX用に最小限のエスケープ。
    数式は raw=True で渡すのが前提（KISS）
    """
    return "".join(_LATEX_SPECIALS.get(ch, ch) for ch in s)