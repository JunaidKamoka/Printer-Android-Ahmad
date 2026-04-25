#!/usr/bin/env python3
"""Generate launcher icons + Play Store assets for HP Printer Tools.

Outputs:
  app/src/main/res/mipmap-{mdpi,hdpi,xhdpi,xxhdpi,xxxhdpi}/ic_launcher.png
  app/src/main/res/mipmap-{...}/ic_launcher_round.png
  playstore/play_store_icon.png      (512x512)
  playstore/feature_graphic.png      (1024x500)

Run:  python3 scripts/generate_icons.py
"""
from __future__ import annotations

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "app" / "src" / "main" / "res"
PLAYSTORE = ROOT / "playstore"

HP_BLUE = (0, 150, 214)        # #0096D6
HP_DARK = (0, 63, 107)         # #003F6B
HP_LIGHT = (230, 244, 251)     # #E6F4FB
WHITE = (255, 255, 255)
SHADOW = (0, 0, 0, 70)

DENSITIES = {
    "mdpi": 48,
    "hdpi": 72,
    "xhdpi": 96,
    "xxhdpi": 144,
    "xxxhdpi": 192,
}


def find_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def radial_gradient(size: int, inner: tuple[int, int, int], outer: tuple[int, int, int]) -> Image.Image:
    img = Image.new("RGB", (size, size), outer)
    px = img.load()
    cx = cy = size / 2
    max_r = math.hypot(cx, cy)
    for y in range(size):
        for x in range(size):
            r = math.hypot(x - cx, y - cy) / max_r
            r = min(1.0, r)
            px[x, y] = (
                int(inner[0] * (1 - r) + outer[0] * r),
                int(inner[1] * (1 - r) + outer[1] * r),
                int(inner[2] * (1 - r) + outer[2] * r),
            )
    return img


def rounded_mask(size: int, radius_ratio: float = 0.22) -> Image.Image:
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    r = int(size * radius_ratio)
    d.rounded_rectangle((0, 0, size - 1, size - 1), radius=r, fill=255)
    return mask


def circle_mask(size: int) -> Image.Image:
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((0, 0, size - 1, size - 1), fill=255)
    return mask


def draw_printer(canvas: Image.Image, scale: float = 1.0, with_hp_mark: bool = True) -> None:
    """Draw a clean printer glyph centered on canvas."""
    W, H = canvas.size
    cx, cy = W / 2, H / 2

    # Geometry, scaled
    body_w = int(W * 0.62 * scale)
    body_h = int(H * 0.30 * scale)
    body_x = int(cx - body_w / 2)
    body_y = int(cy - body_h / 2 + H * 0.03)

    tray_w = int(body_w * 0.78)
    tray_h = int(body_h * 0.55)
    tray_x = int(cx - tray_w / 2)
    tray_y = int(body_y - tray_h * 0.85)

    paper_w = int(body_w * 0.62)
    paper_h = int(body_h * 0.85)
    paper_x = int(cx - paper_w / 2)
    paper_y = int(body_y + body_h - paper_h * 0.20)

    # Soft drop shadow under the printer
    shadow_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_layer)
    pad = int(W * 0.03)
    sd.rounded_rectangle(
        (body_x - pad, body_y + body_h - pad // 2, body_x + body_w + pad, body_y + body_h + pad * 2),
        radius=int(body_h * 0.2),
        fill=(0, 0, 0, 80),
    )
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=W * 0.02))
    canvas.alpha_composite(shadow_layer)

    d = ImageDraw.Draw(canvas)

    # Top paper feed slot (small dark slit on top)
    slot_w = int(body_w * 0.55)
    slot_h = max(2, int(H * 0.012 * scale))
    slot_x = int(cx - slot_w / 2)
    slot_y = tray_y - slot_h - int(H * 0.005)
    d.rounded_rectangle(
        (slot_x, slot_y, slot_x + slot_w, slot_y + slot_h),
        radius=slot_h // 2,
        fill=(255, 255, 255, 200),
    )

    # Top tray (lighter)
    d.rounded_rectangle(
        (tray_x, tray_y, tray_x + tray_w, tray_y + tray_h),
        radius=int(tray_h * 0.18),
        fill=HP_LIGHT,
    )

    # Output paper, sticking out from front (drawn first, below the body front lip)
    d.rounded_rectangle(
        (paper_x, paper_y, paper_x + paper_w, paper_y + paper_h),
        radius=int(paper_h * 0.05),
        fill=WHITE,
        outline=(220, 230, 240),
        width=max(1, int(W * 0.004)),
    )
    # Lines on the paper
    line_color = (180, 200, 215)
    line_pad_x = int(paper_w * 0.12)
    line_y0 = paper_y + int(paper_h * 0.30)
    line_gap = int(paper_h * 0.18)
    for i in range(3):
        ly = line_y0 + i * line_gap
        d.rounded_rectangle(
            (paper_x + line_pad_x, ly, paper_x + paper_w - line_pad_x, ly + max(2, int(H * 0.012))),
            radius=2,
            fill=line_color,
        )

    # Main printer body (white, on top, covers paper top edge)
    d.rounded_rectangle(
        (body_x, body_y, body_x + body_w, body_y + body_h),
        radius=int(body_h * 0.22),
        fill=WHITE,
    )

    # Front LED / status circle
    led_r = int(body_h * 0.16)
    led_cx = body_x + int(body_w * 0.16)
    led_cy = body_y + int(body_h * 0.55)
    d.ellipse(
        (led_cx - led_r, led_cy - led_r, led_cx + led_r, led_cy + led_r),
        fill=HP_BLUE,
    )

    if with_hp_mark:
        # "hp" wordmark on the front of the body
        font_size = max(8, int(body_h * 0.55))
        font = find_font(font_size)
        text = "hp"
        bbox = d.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        tx = body_x + int(body_w * 0.62) - tw // 2
        ty = body_y + (body_h - th) // 2 - bbox[1]
        d.text((tx, ty), text, font=font, fill=HP_DARK)


def make_adaptive_foreground(size: int) -> Image.Image:
    """432x432-style foreground at given size. Content sits in inner ~66% safe zone."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    # Adaptive icons clip to a 108dp rect; the visible content area is the inner 72dp.
    # We render the printer at ~62% of full to land safely inside the safe zone for any mask.
    draw_printer(img, scale=0.95)
    return img


def make_legacy_icon(size: int, round_icon: bool) -> Image.Image:
    """Composited legacy launcher icon: gradient bg + printer + rounded/circle mask."""
    full = size * 2  # supersample
    bg = radial_gradient(full, HP_BLUE, HP_DARK).convert("RGBA")
    draw_printer(bg, scale=0.95)

    if round_icon:
        mask = circle_mask(full)
    else:
        mask = rounded_mask(full, radius_ratio=0.22)

    out = Image.new("RGBA", (full, full), (0, 0, 0, 0))
    out.paste(bg, (0, 0), mask)
    return out.resize((size, size), Image.LANCZOS)


def make_play_store_icon(size: int = 512) -> Image.Image:
    """Square 512x512 Play Store icon (no transparency, no rounded corners)."""
    full = size * 2
    bg = radial_gradient(full, HP_BLUE, HP_DARK).convert("RGBA")
    draw_printer(bg, scale=0.95)
    return bg.convert("RGB").resize((size, size), Image.LANCZOS)


def make_feature_graphic(w: int = 1024, h: int = 500) -> Image.Image:
    """1024x500 Play Store feature graphic with title + printer glyph."""
    full_w, full_h = w * 2, h * 2

    # Diagonal-ish gradient background
    bg = Image.new("RGB", (full_w, full_h), HP_DARK)
    px = bg.load()
    for y in range(full_h):
        for x in range(full_w):
            t = (x / full_w) * 0.7 + (1 - y / full_h) * 0.3
            t = max(0.0, min(1.0, t))
            px[x, y] = (
                int(HP_DARK[0] * (1 - t) + HP_BLUE[0] * t),
                int(HP_DARK[1] * (1 - t) + HP_BLUE[1] * t),
                int(HP_DARK[2] * (1 - t) + HP_BLUE[2] * t),
            )
    bg = bg.convert("RGBA")

    # Right-side printer (sized to leave room for title on the left)
    glyph_size = int(full_h * 0.78)
    glyph = Image.new("RGBA", (glyph_size, glyph_size), (0, 0, 0, 0))
    draw_printer(glyph, scale=1.0, with_hp_mark=True)
    gx = full_w - glyph_size - int(full_w * 0.06)
    gy = (full_h - glyph_size) // 2
    bg.alpha_composite(glyph, (gx, gy))

    d = ImageDraw.Draw(bg)
    title_font = find_font(int(full_h * 0.16))
    sub_font = find_font(int(full_h * 0.065))

    title = "HP Printer Tools"
    sub = "12 easy tools — print, scan, copy, fax"

    pad = int(full_w * 0.05)
    title_y = int(full_h * 0.34)
    d.text((pad, title_y), title, font=title_font, fill=WHITE)
    sub_y = title_y + int(full_h * 0.20)
    d.text((pad, sub_y), sub, font=sub_font, fill=HP_LIGHT)

    return bg.convert("RGB").resize((w, h), Image.LANCZOS)


def main() -> None:
    PLAYSTORE.mkdir(parents=True, exist_ok=True)

    # Legacy mipmap PNGs
    for density, size in DENSITIES.items():
        out_dir = RES / f"mipmap-{density}"
        out_dir.mkdir(parents=True, exist_ok=True)
        make_legacy_icon(size, round_icon=False).save(out_dir / "ic_launcher.png", optimize=True)
        make_legacy_icon(size, round_icon=True).save(out_dir / "ic_launcher_round.png", optimize=True)
        # Adaptive foreground PNG (used as fallback if vector path is missing)
        # Standard adaptive icon foreground is 108dp — at xxxhdpi that's 432px.
        # For each density we also output a square foreground sized to its full canvas.
        fg_size = int(size * 108 / 48)
        make_adaptive_foreground(fg_size).save(out_dir / "ic_launcher_foreground.png", optimize=True)
        print(f"  wrote mipmap-{density}/ ({size}px legacy, {fg_size}px foreground)")

    # Play Store assets
    make_play_store_icon(512).save(PLAYSTORE / "play_store_icon.png", optimize=True)
    print(f"  wrote playstore/play_store_icon.png (512x512)")
    make_feature_graphic(1024, 500).save(PLAYSTORE / "feature_graphic.png", optimize=True)
    print(f"  wrote playstore/feature_graphic.png (1024x500)")


if __name__ == "__main__":
    main()
