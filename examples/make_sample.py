# path: examples/make_sample.py
from lectgen.document import Document
from lectgen.renderers.latex import LatexRenderer
import subprocess

doc = Document()

doc.add_section("add_sectionで出力")

doc.add_terms(
    "add-termsで出力",
    title="タイトル",
    boxed=True
)

doc.add_paragraph("区間 $[a,b]$ を縮めていくと、極限として瞬間変化率が得られます。", raw=True)

renderer = LatexRenderer(
    docclass="ltjsarticle",  # LuaLaTeX + Japanese の例
    preamble=r"""
\usepackage{luatexja}
\usepackage{amsmath, amssymb, amsthm}
\usepackage{bm}
\usepackage{physics}
\usepackage[margin=12mm]{geometry}
\usepackage[most]{tcolorbox}
\usepackage{anyfontsize}
\AtBeginDocument{\fontsize{11pt}{18pt}\selectfont}
""",
)
latex = renderer.render(doc)

with open("lecture.tex", "w", encoding="utf-8") as f:
    f.write(latex)

print("Wrote lecture.tex")

subprocess.run(["lualatex", "lecture.tex"])