# path: examples/make_sample.py
from lectgen.document import Document
from lectgen.renderers.latex import LatexRenderer
import subprocess

filename = "教師なし学習.tex"

doc = Document()

doc.add_title("教師なし学習")

doc.add_section("k-means法")

doc.add_terms(
    "データをk個のクラスタに分ける代表的手法",
    title="k-means法",
    boxed=True
)

doc.add_figure_space(
    height="200pt",         # 各ボックスの高さ
    count=1,               # 3つ横並び
    margin_top="0pt",     # 外側マージン（上）
    margin_bottom="10pt",  # 外側マージン（下）
    margin_left="0pt",     # 外側マージン（左）
    margin_right="0pt",    # 外側マージン（右）
    gap="6pt",             # ボックス間の横ギャップ
    arc="4pt",             # 角丸
    rule="0.4pt",          # 枠の太さ
)

doc.add_list(
    items=[
        "シンプルで理解しやすい",
        "計算が早くスケーラブル",
        "結果が分かりやすく、可視化しやすい",
    ],
    title="メリット",
    title_marker= "▶",
    style="itemize",  # または "enumerate"
    boxed=False,   
    margin_before="8pt",
    margin_after="4pt"
)


renderer = LatexRenderer(
    docclass="ltjsarticle",  # LuaLaTeX + Japanese の例
    preamble=r"""
\usepackage{luatexja}
\usepackage[haranoaji, match]{luatexja-preset} % TeX Live 標準の HaranoAji 系を使用

% --- ここがポイント ---
\renewcommand{\familydefault}{\sfdefault}      % 欧文デフォルトをサンセリフに
\renewcommand{\kanjifamilydefault}{\gtdefault} % 和文デフォルトをゴシックに
% ------------------------

\usepackage{amsmath, amssymb, amsthm}
\usepackage{bm}
\usepackage{physics}
\usepackage[margin=24mm]{geometry}
\usepackage[most]{tcolorbox}
\usepackage{xcolor}
\usepackage{anyfontsize}
\AtBeginDocument{\fontsize{11pt}{18pt}\selectfont}
""",
)

latex = renderer.render(doc)

with open(filename, "w", encoding="utf-8") as f:
    f.write(latex)

print(f"Wrote {filename}")

subprocess.run(["lualatex", filename])