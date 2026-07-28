# Generate a dark variant of the Pastel Moonlight theme by HSL-flipping the light theme.
import json, colorsys, os, re

base = os.path.dirname(__file__)
src = os.path.join(base, "..", "themes", "pastel-moonlight-color-theme.json")
out = os.path.join(base, "..", "themes", "pastel-moonlight-dark-color-theme.json")

with open(src, encoding="utf-8") as f:
    theme = json.load(f)

HEX = re.compile(r"^#([0-9A-Fa-f]{6})([0-9A-Fa-f]{2})?$")

# Explicit overrides: original light hex -> fixed dark hex (for selection/comment/etc.)
OVERRIDE = {
    "#F9F5F6": "#1A1520",   # editor background (darkest)
    "#F8E8EE": "#221B27",   # panel / surface
    "#F0E2E8": "#2C2330",   # indent guides / rulers
    "#EBDDE3": "#332838",   # whitespace
    "#FDCEDF": "#6B4A60",   # selection / selection highlight (must be visible)
    "#F2BED1": "#5A3D52",   # word highlight / find match / widget border
    "#C5A3B1": "#B099A8",   # comment (light muted)
    "#9A8089": "#A890A0",   # description foreground
    "#D3B7C1": "#7E6E78",   # line number
    "#B4637A": "#D98FB0",   # active line number
    "#B99AA6": "#9C8494",   # codelens
    "#8A6B77": "#B89AA8",   # icon foreground
    "#D08543": "#F5B87A",   # numbers / constants (was too dim brown on dark)
    "#E3C7A7": "#F0C878",   # warning / git modified (brighter gold)
}


def transform(hexc):
    m = HEX.match(hexc)
    if not m:
        return hexc
    if hexc[:7].upper() in OVERRIDE:
        dark = OVERRIDE[hexc[:7].upper()]
        return dark + (hexc[7:] if len(hexc) == 9 else "")
    body = m.group(1)
    alpha = m.group(2) or "FF"
    r, g, b = int(body[0:2], 16), int(body[2:4], 16), int(body[4:6], 16)
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if l > 0.6:
        nl = 0.10 + (1 - l) * 0.20
        ns = s * 0.65
    elif l > 0.35:
        nl = 0.74 + (0.6 - l) * 0.45
        ns = min(1.0, s * 1.10)
    else:
        nl = 0.82 + (0.35 - l) * 0.40
        ns = min(1.0, s * 1.05)
    nl = max(0.06, min(0.96, nl))
    ns = max(0.0, min(1.0, ns))
    r2, g2, b2 = colorsys.hls_to_rgb(h, nl, ns)
    return "#%02X%02X%02X%s" % (int(r2 * 255), int(g2 * 255), int(b2 * 255), alpha)


def walk(obj):
    if isinstance(obj, dict):
        return {k: walk(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk(v) for v in obj]
    if isinstance(obj, str) and HEX.match(obj):
        return transform(obj)
    return obj


dark = walk(theme)
dark["name"] = "Pastel Moonlight Dark"
dark["type"] = "dark"

with open(out, "w", encoding="utf-8") as f:
    json.dump(dark, f, indent=2, ensure_ascii=False)
print("saved", out)
