# ─────────────────────────────
# 📘 title_marker で使える記号一覧
# 例: doc.add_list(..., title="メリット", title_marker="◆")
# ─────────────────────────────
#
# ●  黒丸（定番で見やすい）
# ○  白抜き丸（軽い印象）
# ■  黒四角（主張強め）
# □  白四角
# ◆  菱形（タイトルに映える）
# ◇  白抜き菱形
# ▶  小さい黒矢印（スマート）
# ▷  白抜き矢印（控えめ）
# ★  星マーク（目立たせたいとき）
# ☆  白抜き星
# ◎  二重丸（ポイント）
# ※  注意や補足に
# →  矢印（流れを表す）
# ⇒  強い矢印（結論を強調）
#
# ── LaTeX 記号（数式モードで使用）
#   title_marker = r"$\\bullet$"         # •
#   title_marker = r"$\\triangle$"       # △
#   title_marker = r"$\\blacktriangle$"  # ▲
#   title_marker = r"$\\bigstar$"        # ★
#   title_marker = r"$\\circ$"           # ∘
#   title_marker = r"$\\rightarrow$"     # →
#   title_marker = r"$\\Rightarrow$"     # ⇒
#
# ── カラー付きマーカー（xcolor使用時）
#   title_marker = r"\\textcolor{blue}{◆}"
#   title_marker = r"\\textcolor{red}{★}"
#
# おすすめ：
#   理論・定義 → ◆ or ■
#   注意・例外 → ※ or →
#   感覚的教材 → ● or ★
#   プレゼン風 → ▶ or ◇
# ─────────────────────────────