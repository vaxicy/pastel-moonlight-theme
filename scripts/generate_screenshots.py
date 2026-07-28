# Generate mock VS Code editor screenshots for README (JS/React, Python, CSS)
# 1280x800, faithful to pastel-pink-color-theme.json colors
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1280, 800
TITLE_H, TAB_H, STATUS_H = 40, 38, 26
ACT_W, SIDE_W = 50, 230

# theme palette
BG = "#F9F5F6"; PANEL = "#F8E8EE"; HILITE = "#FDCEDF"; ACCENT = "#F2BED1"
FG = "#5C4A52"; SUB = "#9A8089"; LINENO = "#D3B7C1"; LINENO_A = "#B4637A"
KW = "#C2528B"; FN = "#A86798"; STR = "#739E73"; NUM = "#D08543"
CMT = "#C5A3B1"; PROP = "#8F6B7C"; TYPE = "#B4637A"; PUNC = "#8A6B77"; PARAM = "#8A6B9E"
STATUS_BG = "#F2BED1"; STATUS_FG = "#5C4048"; SECTION = "#F5DEE8"

FONT_DIR = r"C:\Windows\Fonts"
code = ImageFont.truetype(os.path.join(FONT_DIR, "consola.ttf"), 16)
code_i = ImageFont.truetype(os.path.join(FONT_DIR, "consolai.ttf"), 16)
ui = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 14)
ui_sm = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 12)
ui_b = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 14)

LINE_H = 24
CHAR_W = code.getlength("x")

def base_frame(d, img, active_tab, tabs, files, active_file):
    # title bar
    d.rectangle([0, 0, W, TITLE_H], fill=PANEL)
    for i, c in enumerate(("#E8909C", "#EFC078", "#9CCB86")):
        x = 20 + i * 22
        d.ellipse([x, TITLE_H // 2 - 6, x + 12, TITLE_H // 2 + 6], fill=c)
    t = "pastel-pink-demo — Visual Studio Code"
    d.text((W // 2 - d.textlength(t, ui) / 2, TITLE_H // 2 - 9), t, font=ui, fill=SUB)
    # activity bar
    d.rectangle([0, TITLE_H, ACT_W, H - STATUS_H], fill=PANEL)
    icons_y = TITLE_H + 22
    for i in range(5):
        y = icons_y + i * 52
        col = "#B4637A" if i == 0 else "#C9A9B4"
        if i == 0:
            d.rectangle([0, y - 4, 3, y + 24], fill=KW)
        d.rounded_rectangle([14, y, 36, y + 22], radius=5, outline=col, width=2)
    # sidebar
    d.rectangle([ACT_W, TITLE_H, ACT_W + SIDE_W, H - STATUS_H], fill=PANEL)
    d.text((ACT_W + 16, TITLE_H + 10), "EXPLORER", font=ui_sm, fill=SUB)
    d.rectangle([ACT_W, TITLE_H + 34, ACT_W + SIDE_W, TITLE_H + 60], fill=SECTION)
    d.text((ACT_W + 16, TITLE_H + 39), "▾  PASTEL-PINK-DEMO", font=ui_b, fill="#7A5E6B")
    fy = TITLE_H + 70
    for name in files:
        if name == active_file:
            d.rectangle([ACT_W, fy - 3, ACT_W + SIDE_W, fy + 20], fill=HILITE)
            d.text((ACT_W + 28, fy), name, font=ui, fill="#4A3B44")
        else:
            d.text((ACT_W + 28, fy), name, font=ui, fill="#6B5560")
        fy += 26
    # tab bar
    x0 = ACT_W + SIDE_W
    d.rectangle([x0, TITLE_H, W, TITLE_H + TAB_H], fill=PANEL)
    tx = x0
    for name in tabs:
        tw = int(d.textlength(name, ui)) + 44
        if name == active_tab:
            d.rectangle([tx, TITLE_H, tx + tw, TITLE_H + TAB_H], fill=BG)
            d.rectangle([tx, TITLE_H, tx + tw, TITLE_H + 2], fill=KW)
            d.text((tx + 18, TITLE_H + 10), name, font=ui, fill="#4A3B44")
        else:
            d.text((tx + 18, TITLE_H + 10), name, font=ui, fill=SUB)
        tx += tw
    # editor bg
    d.rectangle([x0, TITLE_H + TAB_H, W, H - STATUS_H], fill=BG)
    # status bar
    d.rectangle([0, H - STATUS_H, W, H], fill=STATUS_BG)
    d.text((14, H - STATUS_H + 4), "\u2325 main    \u21bb 0 \u2193 0    \u26a0 0  \u24e7 0", font=ui_sm, fill=STATUS_FG)
    right = "Ln 12, Col 8    Spaces: 2    UTF-8    Pastel Pink"
    d.text((W - d.textlength(right, ui_sm) - 16, H - STATUS_H + 4), right, font=ui_sm, fill=STATUS_FG)
    return x0

def render_code(d, x0, lines, active_line=None):
    gut_w = 56
    y = TITLE_H + TAB_H + 12
    for idx, segs in enumerate(lines, start=1):
        if active_line == idx:
            d.rectangle([x0, y - 3, W, y + LINE_H - 6], fill="#F8E8EE")
        ln = str(idx)
        d.text((x0 + gut_w - 14 - d.textlength(ln, code), y), ln, font=code,
               fill=LINENO_A if active_line == idx else LINENO)
        x = x0 + gut_w + 8
        for text, color, *style in segs:
            f = code_i if style and style[0] == "i" else code
            d.text((x, y), text, font=f, fill=color)
            x += f.getlength(text)
        y += LINE_H

def make(fname, tabs, active_tab, files, lines, active_line):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    x0 = base_frame(d, img, active_tab, tabs, files, active_tab)
    render_code(d, x0, lines, active_line)
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
    os.makedirs(out_dir, exist_ok=True)
    p = os.path.join(out_dir, fname)
    img.save(p)
    print("saved", p)

FILES = ["App.jsx", "styles.css", "utils.py", "package.json", "README.md"]

# ---------- JS / React ----------
js = [
    [("// A cozy little React component", CMT, "i")],
    [("import", KW), (" React, { useState } ", FG), ("from", KW), (" ", FG), ("'react'", STR), (";", PUNC)],
    [("import", KW), (" { motion } ", FG), ("from", KW), (" ", FG), ("'framer-motion'", STR), (";", PUNC)],
    [],
    [("const", KW), (" PALETTE ", NUM), ("= [", PUNC), ("'#F9F5F6'", STR), (", ", PUNC), ("'#FDCEDF'", STR), (", ", PUNC), ("'#F2BED1'", STR), ("];", PUNC)],
    [],
    [("export default function", KW), (" ", FG), ("MoodBoard", FN), ("(", PUNC), ("{ title }", PARAM), (") {", PUNC)],
    [("  ", FG), ("const", KW), (" [likes, setLikes] ", FG), ("=", PUNC), (" ", FG), ("useState", FN), ("(", PUNC), ("0", NUM), (");", PUNC)],
    [],
    [("  ", FG), ("const", KW), (" ", FG), ("handleLike", FN), (" ", FG), ("=", PUNC), (" () ", PUNC), ("=>", KW), (" {", PUNC)],
    [("    ", FG), ("setLikes", FN), ("(", PUNC), ("prev", PARAM), (" ", FG), ("=>", KW), (" prev ", FG), ("+", PUNC), (" ", FG), ("1", NUM), (");", PUNC)],
    [("  };", PUNC)],
    [],
    [("  ", FG), ("return", KW), (" (", PUNC)],
    [("    <", PUNC), ("motion.section", TYPE), (" ", FG), ("className", FN, "i"), ("=", PUNC), ("\"board\"", STR), (">", PUNC)],
    [("      <", PUNC), ("h1", KW), (">{", PUNC), ("title", FG), ("}</", PUNC), ("h1", KW), (">", PUNC)],
    [("      <", PUNC), ("button", KW), (" ", FG), ("onClick", FN, "i"), ("=", PUNC), ("{", PUNC), ("handleLike", FN), ("}>", PUNC)],
    [("        \u2764 {", PUNC), ("likes", FG), ("} likes", FG)],
    [("      </", PUNC), ("button", KW), (">", PUNC)],
    [("    </", PUNC), ("motion.section", TYPE), (">", PUNC)],
    [("  );", PUNC)],
    [("}", PUNC)],
]

# ---------- Python ----------
py = [
    [("# Dreamy palette utilities", CMT, "i")],
    [("from", KW), (" dataclasses ", FG), ("import", KW), (" dataclass", FG)],
    [("from", KW), (" typing ", FG), ("import", KW), (" List", TYPE)],
    [],
    [("PASTELS", NUM), (" = [", PUNC), ("\"#F9F5F6\"", STR), (", ", PUNC), ("\"#F8E8EE\"", STR), (", ", PUNC), ("\"#FDCEDF\"", STR), ("]", PUNC)],
    [],
    [("@dataclass", FN, "i")],
    [("class", KW), (" ", FG), ("Swatch", TYPE), (":", PUNC)],
    [("    name", PROP), (": ", PUNC), ("str", TYPE)],
    [("    hex_code", PROP), (": ", PUNC), ("str", TYPE)],
    [("    opacity", PROP), (": ", PUNC), ("float", TYPE), (" = ", PUNC), ("1.0", NUM)],
    [],
    [("    ", FG), ("def", KW), (" ", FG), ("blend", FN), ("(", PUNC), ("self", KW, "i"), (", ", PUNC), ("other", PARAM), (": ", PUNC), ("\"Swatch\"", STR), (") -> ", PUNC), ("str", TYPE), (":", PUNC)],
    [("        ", FG), ("\"\"\"Blend two pastel swatches softly.\"\"\"", STR)],
    [("        ", FG), ("mixed", FG), (" = ", PUNC), ("mix_hex", FN), ("(", PUNC), ("self", KW, "i"), (".hex_code, other.hex_code, ", PUNC), ("0.5", NUM), (")", PUNC)],
    [("        ", FG), ("return", KW), (" ", FG), ("f\"blended: ", STR), ("{", KW), ("mixed", FG), ("}", KW), ("\"", STR)],
    [],
    [("def", KW), (" ", FG), ("build_palette", FN), ("(", PUNC), ("codes", PARAM), (": ", PUNC), ("List", TYPE), ("[", PUNC), ("str", TYPE), ("]) -> ", PUNC), ("list", TYPE), (":", PUNC)],
    [("    ", FG), ("# keep it soft, keep it minimal", CMT, "i")],
    [("    ", FG), ("return", KW), (" [", PUNC), ("Swatch", TYPE), ("(", PUNC), ("f\"tone-", STR), ("{", KW), ("i", FG), ("}", KW), ("\"", STR), (", c) ", PUNC), ("for", KW), (" i, c ", FG), ("in", KW), (" ", FG), ("enumerate", FN), ("(codes)]", PUNC)],
]

# ---------- CSS ----------
css = [
    [("/* Pastel Pink design tokens */", CMT, "i")],
    [(":root", KW), (" {", PUNC)],
    [("  --bg", PROP), (": ", PUNC), ("#F9F5F6", NUM), (";", PUNC)],
    [("  --panel", PROP), (": ", PUNC), ("#F8E8EE", NUM), (";", PUNC)],
    [("  --highlight", PROP), (": ", PUNC), ("#FDCEDF", NUM), (";", PUNC)],
    [("  --accent", PROP), (": ", PUNC), ("#F2BED1", NUM), (";", PUNC)],
    [("}", PUNC)],
    [],
    [(".card", KW), (" {", PUNC)],
    [("  background", PROP), (": ", PUNC), ("var", FN), ("(", PUNC), ("--panel", PROP), (");", PUNC)],
    [("  border-radius", PROP), (": ", PUNC), ("16", NUM), ("px", KW), (";", PUNC)],
    [("  padding", PROP), (": ", PUNC), ("24", NUM), ("px", KW), (" ", FG), ("28", NUM), ("px", KW), (";", PUNC)],
    [("  box-shadow", PROP), (": ", PUNC), ("0 8", NUM), ("px", KW), (" ", FG), ("24", NUM), ("px", KW), (" ", FG), ("rgba", FN), ("(", PUNC), ("242", NUM), (", ", PUNC), ("190", NUM), (", ", PUNC), ("209", NUM), (", ", PUNC), (".35", NUM), (");", PUNC)],
    [("  transition", PROP), (": ", PUNC), ("transform ", FG), (".25", NUM), ("s", KW), (" ease", FG), (";", PUNC)],
    [("}", PUNC)],
    [],
    [(".card", KW), (":hover", FN, "i"), (" {", PUNC)],
    [("  transform", PROP), (": ", PUNC), ("translateY", FN), ("(", PUNC), ("-4", NUM), ("px", KW), (");", PUNC)],
    [("  background", PROP), (": ", PUNC), ("var", FN), ("(", PUNC), ("--highlight", PROP), (");", PUNC)],
    [("}", PUNC)],
]

make("screenshot-js.png", ["App.jsx", "utils.py", "styles.css"], "App.jsx", FILES, js, 12)
make("screenshot-python.png", ["utils.py", "App.jsx", "styles.css"], "utils.py", FILES, py, 13)
make("screenshot-css.png", ["styles.css", "App.jsx", "utils.py"], "styles.css", FILES, css, 10)
