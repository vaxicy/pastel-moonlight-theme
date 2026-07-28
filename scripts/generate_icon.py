# Generate a 256x256 icon: pastel pink background + crescent moon — NO glow, NO dark ring
from PIL import Image, ImageDraw
import os

S = 256

# --- Solid rounded-square pink background ---
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# Soft pink gradient
top = (252, 235, 240)   # #FCEBF0
bot = (245, 210, 222)   # #F5D2DE
for y in range(S):
    t = y / (S - 1)
    c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    d.line([(0, y), (S, y)], fill=c + (255,))

# Clip to rounded rectangle
mask = Image.new("L", (S, S), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([8, 8, S - 8, S - 8], radius=56, fill=255)

final = Image.new("RGBA", (S, S), (0, 0, 0, 0))
final.paste(img, (0, 0), mask)

d = ImageDraw.Draw(final)

# --- Crescent moon (NO glow behind it) ---
cx, cy, R = 128, 122, 62

moon_mask = Image.new("L", (S, S), 0)
mm = ImageDraw.Draw(moon_mask)
mm.ellipse([cx - R, cy - R, cx + R, cy + R], fill=255)
mm.ellipse([cx - R + 44, cy - R - 26, cx + R + 44, cy + R - 26], fill=0)

moon_layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
ml = ImageDraw.Draw(moon_layer)
ml.bitmap((0, 0), moon_mask, fill=(255, 250, 242, 255))
final.alpha_composite(moon_layer)

# --- Sparkle stars ---
def star4(draw, x, y, r, color):
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
final.save(out)
print("saved", out)
