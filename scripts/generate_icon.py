# Generate a 256x256 icon: pastel pink background + crescent moon
from PIL import Image, ImageDraw, ImageFilter
import os

S = 256
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))

# --- Rounded-square pink gradient background (#F8E8EE -> #F2BED1) ---
bg = Image.new("RGBA", (S, S), (0, 0, 0, 0))
bd = ImageDraw.Draw(bg)
top = (248, 232, 238)
bot = (242, 190, 209)
for y in range(S):
    t = y / (S - 1)
    c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    bd.line([(0, y), (S, y)], fill=c + (255,))
mask = Image.new("L", (S, S), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([8, 8, S - 8, S - 8], radius=56, fill=255)
img.paste(bg, (0, 0), mask)

d = ImageDraw.Draw(img)
# Subtle border
d.rounded_rectangle([8, 8, S - 8, S - 8], radius=56, outline=(235, 179, 201, 255), width=4)

# --- Soft glow behind moon ---
glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
cx, cy, R = 128, 122, 62
gd.ellipse([cx - R - 22, cy - R - 22, cx + R + 22, cy + R + 22], fill=(255, 250, 240, 110))
glow = glow.filter(ImageFilter.GaussianBlur(14))
img.alpha_composite(glow)

# --- Crescent moon (full circle minus offset circle) ---
moon_mask = Image.new("L", (S, S), 0)
mm = ImageDraw.Draw(moon_mask)
mm.ellipse([cx - R, cy - R, cx + R, cy + R], fill=255)          # full moon
# cut-out circle shifted to upper-right -> crescent opens to the right
mm.ellipse([cx - R + 44, cy - R - 26, cx + R + 44, cy + R - 26], fill=0)

moon_layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
ml = ImageDraw.Draw(moon_layer)
# cream-white moon with a hint of warmth
ml.bitmap((0, 0), moon_mask, fill=(255, 250, 242, 255))
img.alpha_composite(moon_layer)

# --- Tiny sparkle stars (rose + white), kept minimal & elegant ---
def star4(draw, x, y, r, color):
    """4-point sparkle."""
    draw.polygon([(x, y - r), (x + r * 0.3, y - r * 0.3), (x + r, y),
                  (x + r * 0.3, y + r * 0.3), (x, y + r),
                  (x - r * 0.3, y + r * 0.3), (x - r, y),
                  (x - r * 0.3, y - r * 0.3)], fill=color)

star4(d, 186, 74, 11, (255, 252, 246, 235))
star4(d, 206, 118, 6, (194, 82, 139, 200))
star4(d, 78, 66, 7, (194, 82, 139, 170))
d.ellipse([64, 176, 70, 182], fill=(255, 252, 246, 220))
d.ellipse([190, 168, 195, 173], fill=(194, 82, 139, 160))

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icon.png"))
img.save(out)
print("saved", out)
