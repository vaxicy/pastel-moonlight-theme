# Generate a DARK variant mock VS Code editor screenshot for README.
# 1280x800, faithful to pastel-moonlight-dark-color-theme.json colors.
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1280, 800
TITLE_H, TAB_H, STATUS_H = 40, 38, 26
ACT_W, SIDE_W = 50, 230

# dark theme palette (from pastel-moonlight-dark-color-theme.json)
BG = "#1A1520"; PANEL = "#221B27"; HILITE = "#6B4A60"; ACCENT = "#5A3D52"
FG = "#D8CED3"; SUB = "#A890A0"; LINENO = "#7E6E78"; LINENO_A = "#D98FB0"
KW = "#E2A4C4"; FN = "#D6B3CD"; STR = "#B8CFB8"; NUM = "#F5B87A"
CMT = "#B099A8"; PROP = "#D1C0C8"; TYPE = "#D98FB0"; PUNC = "#B89AA8"; PARAM = "#C8B8D2"
STATUS_BG = "#5A3D52"; STATUS_FG = "#DDCDD2"; SECTION = "#28131C"
ACTIVE_TAB_FG = "#DED5DB"; ACTIVE_FILE = "#DED5DB"; INACTIVE_FILE = "#C2B2BC"
ACTIVE_BORDER = "#E2A4C4"; INLINE_HILITE = "#221B27"

FONT_DIR = r"C:\Windows\Fonts"
code = ImageFont.truetype(os.path.join(FONT_DIR, "consola.ttf"), 16)
code_i = ImageFont.truetype(os.path.join(FONT_DIR, "consolai.ttf"), 16)
ui = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 14)
ui_sm = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 12)
ui_b = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 14)

LINE_H = 24

def base_frame(d, img, active_tab, tabs, files, active_file):
    d.rectangle([0, 0, W, TITLE_H], fill=PANEL)
    for i, c in enumerate(("#E8909C", "#EFC078", "#9CCB86")):
        x = 20 + i * 22
        d.ellipse([x, TITLE_H // 2 - 6, x + 12, TITLE_H // 2 + 6], fill=c)
    t = "pastel-moonlight-demo — Visual Studio Code"
    d.text((W // 2 - d.textlength(t, ui) / 2, TITLE_H // 2 - 9), t, font=ui, fill=SUB)
    # activity bar
    d.rectangle([0, TITLE_H, ACT_W, H - STATUS_H], fill=PANEL)
    icons_y = TITLE_H + 22
    for i in range(5):
        y = icons_y + i * 52
        col = "#D98FB0" if i == 0 else "#8A7086"
        if i == 0:
            d.rectangle([0, y - 4, 3, y + 24], fill=ACTIVE_BORDER)
        d.rounded_rectangle([14, y, 36, y + 22], radius=5, outline=col, width=2)
    # sidebar
    d.rectangle([ACT_W, TITLE_H, ACT_W + SIDE_W, H - STATUS_H], fill=PANEL)
    d.text((ACT_W + 16, TITLE_H + 10), "EXPLORER", font=ui_sm, fill=SUB)
    d.rectangle([ACT_W, TITLE_H + 34, ACT_W + SIDE_W, TITLE_H + 60], fill=SECTION)
    d.text((ACT_W + 16, TITLE_H + 39), "▾  PASTEL-MOONLIGHT-DEMO", font=ui_b, fill="#D7CAD0")
    fy = TITLE_H + 70
    for name in files:
        if name == active_file:
            d.rectangle([ACT_W, fy - 3, ACT_W + SIDE_W, fy + 20], fill=HILITE)
            d.text((ACT_W + 28, fy), name, font=ui, fill=ACTIVE_FILE)
        else:
            d.text((ACT_W + 28, fy), name, font=ui, fill=INACTIVE_FILE)
        fy += 26
    # tab bar
    x0 = ACT_W + SIDE_W
    d.rectangle([x0, TITLE_H, W, TITLE_H + TAB_H], fill=PANEL)
    tx = x0
    for name in tabs:
        tw = int(d.textlength(name, ui)) + 44
        if name == active_tab:
            d.rectangle([tx, TITLE_H, tx + tw, TITLE_H + TAB_H], fill=BG)
            d.rectangle([tx, TITLE_H, tx + tw, TITLE_H + 2], fill=ACTIVE_BORDER)
            d.text((tx + 18, TITLE_H + 10), name, font=ui, fill=ACTIVE_TAB_FG)
        else:
            d.text((tx + 18, TITLE_H + 10), name, font=ui, fill=SUB)
        tx += tw
    # editor bg
    d.rectangle([x0, TITLE_H + TAB_H, W, H - STATUS_H], fill=BG)
    # status bar
    d.rectangle([0, H - STATUS_H, W, H], fill=STATUS_BG)
    d.text((14, H - STATUS_H + 4), "⎇ main    ↻ 0 ↓ 0    ⚠ 0  ⌧ 0", font=ui_sm, fill=STATUS_FG)
    right = "Ln 12, Col 8    Spaces: 2    UTF-8    Pastel Moonlight Dark"
    d.text((W - d.textlength(right, ui_sm) - 16, H - STATUS_H + 4), right, font=ui_sm, fill=STATUS_FG)
    return x0

def render_code(d, x0, lines, active_line=None):
    gut_w = 56
    y = TITLE_H + TAB_H + 12
    for idx, segs in enumerate(lines, start=1):
        if active_line == idx:
            d.rectangle([x0, y - 3, W, y + LINE_H - 6], fill=INLINE_HILITE)
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

js = [
    [("// A cozy little React component", CMT, "i")],
    [("import", KW), (" React, { useState } ", FG), ("from", KW), (" ", FG), ("'react'", STR), (";", PUNC)],
    [("import", KW), (" { motion } ", FG), ("from", KW), (" ", FG), ("'framer-motion'", STR), (";", PUNC)],
    [],
    [("const", KW), (" PALETTE ", NUM), ("= [", PUNC), ("'#1A1520'", STR), (", ", PUNC), ("'#6B4A60'", STR), (", ", PUNC), ("'#5A3D52'", STR), ("];", PUNC)],
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

make("screenshot-dark.png", ["App.jsx", "utils.py", "styles.css"], "App.jsx", FILES, js, 12)
