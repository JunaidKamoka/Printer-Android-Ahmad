#!/usr/bin/env python3
"""Render the 30-second Play Store promo video for HP Printer Tools.

Output:  playstore/promo_video.mp4   (1920x1080, 30 fps, ~30 s, H.264 mp4)

Run:  python3 scripts/generate_video.py
"""
from __future__ import annotations

import math
from pathlib import Path

import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFilter

# Reuse UI rendering from the screenshots script.
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_screenshots import (  # type: ignore
    HP_BLUE, HP_DARK, HP_LIGHT, WHITE,
    font, text_size,
    render_home, render_tool_detail,
    draw_icon_glyph,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "playstore" / "promo_video.mp4"

W, H = 1920, 1080
FPS = 30
DURATION = 30.0
TOTAL = int(DURATION * FPS)

# Cache UI screens once (slow to render).
print("Pre-rendering UI screens…")
UI_HOME = render_home(1080, 1920)
UI_PRINT_PHOTO = render_tool_detail(1080, 1920, "Print Photo", "image",
    "Pick a picture from your gallery and print it instantly.")
UI_SCAN = render_tool_detail(1080, 1920, "Scan Document", "scan",
    "Capture a page with your camera, then save or print the result.")
UI_ID = render_tool_detail(1080, 1920, "ID Card Copy", "id",
    "Capture both sides of an ID card and print them combined on a single page.")
UI_FAX = render_tool_detail(1080, 1920, "Mobile Fax", "fax",
    "Compose a fax-style email with an attachment to send from your phone.")
print("  done.")


# ---------- helpers --------------------------------------------------------

def ease_in_out(t: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, t)))


def ease_out(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def gradient_bg(w: int, h: int, t: float) -> Image.Image:
    """Animated gradient background — slow shimmer."""
    img = Image.new("RGB", (w, h), HP_DARK)
    px = img.load()
    shift = (math.sin(t * 0.6) * 0.5 + 0.5) * 0.2
    for y in range(h):
        for x in range(w):
            u = (x / w) * 0.7 + (1 - y / h) * 0.3 + shift
            u = max(0.0, min(1.0, u))
            px[x, y] = (
                int(HP_DARK[0] * (1 - u) + HP_BLUE[0] * u),
                int(HP_DARK[1] * (1 - u) + HP_BLUE[1] * u),
                int(HP_DARK[2] * (1 - u) + HP_BLUE[2] * u),
            )
    return img


def device_frame(ui: Image.Image, scale: float = 1.0) -> Image.Image:
    """Wrap a UI screenshot in a thin black bezel with rounded corners."""
    uw, uh = ui.size
    if scale != 1.0:
        ui = ui.resize((int(uw * scale), int(uh * scale)), Image.LANCZOS)
        uw, uh = ui.size
    bezel = max(8, int(uw * 0.035))
    fw, fh = uw + bezel * 2, uh + bezel * 2
    frame = Image.new("RGB", (fw, fh), (10, 14, 20))
    frame.paste(ui, (bezel, bezel))
    mask = Image.new("L", (fw, fh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, fw, fh), radius=int(fw * 0.07), fill=255)
    out = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
    out.paste(frame, (0, 0), mask)
    return out


def paste_with_shadow(canvas: Image.Image, layer: Image.Image, pos: tuple[int, int],
                      shadow_blur: int = 30, shadow_alpha: int = 140):
    lw, lh = layer.size
    pad = shadow_blur * 2
    sh = Image.new("RGBA", (lw + pad * 2, lh + pad * 2), (0, 0, 0, 0))
    sh.paste(layer, (pad, pad), layer if layer.mode == "RGBA" else None)
    a = sh.split()[3]
    shadow = Image.new("RGBA", sh.size, (0, 0, 0, 0))
    shadow.paste((0, 0, 0, shadow_alpha), mask=a)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=shadow_blur))
    shadow_pos = (pos[0] - pad, pos[1] - pad + 20)
    canvas.alpha_composite(shadow, shadow_pos)
    canvas.alpha_composite(layer if layer.mode == "RGBA" else layer.convert("RGBA"), pos)


def draw_text_centered(d: ImageDraw.ImageDraw, txt: str, f, y: int, color, max_w: int):
    """Wraps to two lines if needed, returns y after last line."""
    words = txt.split()
    lines: list[str] = []
    cur: list[str] = []
    for w in words:
        cur.append(w)
        tw, _ = text_size(d, " ".join(cur), f)
        if tw > max_w:
            cur.pop()
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    cy = y
    for line in lines[:2]:
        tw, th = text_size(d, line, f)
        d.text(((W - tw) // 2, cy), line, font=f, fill=color)
        cy += int(th * 1.15)
    return cy


def draw_app_icon(size: int) -> Image.Image:
    """Self-contained app icon at any size."""
    full = size * 2
    bg = Image.new("RGB", (full, full), HP_BLUE)
    px = bg.load()
    for y in range(full):
        for x in range(full):
            r = math.hypot(x - full / 2, y - full / 2) / (full / 2 * 1.2)
            r = min(1.0, r)
            px[x, y] = (
                int(HP_BLUE[0] * (1 - r) + HP_DARK[0] * r),
                int(HP_BLUE[1] * (1 - r) + HP_DARK[1] * r),
                int(HP_BLUE[2] * (1 - r) + HP_DARK[2] * r),
            )
    bg = bg.convert("RGBA")
    glyph = Image.new("RGBA", (full, full), (0, 0, 0, 0))
    # Reuse "printer" glyph, larger, with hp wordmark
    from generate_icons import draw_printer  # type: ignore
    draw_printer(glyph, scale=0.95, with_hp_mark=True)
    bg.alpha_composite(glyph)
    mask = Image.new("L", (full, full), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, full, full), radius=int(full * 0.22), fill=255)
    out = Image.new("RGBA", (full, full), (0, 0, 0, 0))
    out.paste(bg, (0, 0), mask)
    return out.resize((size, size), Image.LANCZOS)


# ---------- scene renderers ------------------------------------------------

# Pre-cache device frames for hot scenes
print("Pre-rendering device frames…")
DEV_HOME = device_frame(UI_HOME, scale=0.46)        # ~497x884
DEV_PHOTO = device_frame(UI_PRINT_PHOTO, scale=0.46)
DEV_SCAN = device_frame(UI_SCAN, scale=0.46)
DEV_ID = device_frame(UI_ID, scale=0.46)
DEV_FAX = device_frame(UI_FAX, scale=0.46)
APP_ICON_LARGE = draw_app_icon(380)
APP_ICON_SMALL = draw_app_icon(180)
print("  done.")


def scene_intro(t: float) -> Image.Image:
    """0–4s. Brand intro: animated icon + title."""
    canvas = gradient_bg(W, H, t).convert("RGBA")

    # Icon scales up with bounce
    p = ease_out(min(1.0, t / 1.2))
    overshoot = 1 + 0.08 * math.sin(p * math.pi) * (1 - p) if p < 0.99 else 1.0
    scale = p * overshoot
    icon_size = int(380 * scale) if scale > 0.05 else 1
    icon = APP_ICON_LARGE.resize((icon_size, icon_size), Image.LANCZOS) if icon_size > 1 else None

    title_alpha = int(255 * ease_out(max(0, (t - 1.2) / 0.7)))
    sub_alpha = int(255 * ease_out(max(0, (t - 1.7) / 0.7)))

    if icon is not None:
        ix = (W - icon_size) // 2
        iy = (H - icon_size) // 2 - 80
        paste_with_shadow(canvas, icon, (ix, iy), shadow_blur=40, shadow_alpha=160)

    d = ImageDraw.Draw(canvas)
    title_f = font(96, bold=True)
    sub_f = font(46)
    title = "HP Printer Tools"
    sub = "12 tools for your HP printer"
    tw, th = text_size(d, title, title_f)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text(((W - tw) // 2, H // 2 + 160), title, font=title_f, fill=(255, 255, 255, title_alpha))
    sw, sh = text_size(d, sub, sub_f)
    ld.text(((W - sw) // 2, H // 2 + 280), sub, font=sub_f,
            fill=(HP_LIGHT[0], HP_LIGHT[1], HP_LIGHT[2], sub_alpha))
    canvas.alpha_composite(layer)
    return canvas.convert("RGB")


def _scene_phone_with_text(t: float, dev: Image.Image, headline: str, sub: str,
                           local_t: float, scene_dur: float) -> Image.Image:
    """Phone slides in from right; big text on the left fades in."""
    canvas = gradient_bg(W, H, t).convert("RGBA")

    # Slide-in
    slide_p = ease_out(min(1.0, local_t / 0.7))
    fw, fh = dev.size
    target_x = int(W * 0.62)
    start_x = W + 40
    px = int(lerp(start_x, target_x, slide_p))
    py = (H - fh) // 2
    paste_with_shadow(canvas, dev, (px, py), shadow_blur=35, shadow_alpha=160)

    # Text fade in
    text_alpha = int(255 * ease_out(max(0, (local_t - 0.4) / 0.7)))
    sub_alpha = int(255 * ease_out(max(0, (local_t - 0.7) / 0.7)))

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    title_f = font(110, bold=True)
    sub_f = font(46)

    pad = int(W * 0.05)
    text_max_w = int(W * 0.46)

    # Wrap headline
    words = headline.split()
    lines: list[str] = []
    cur: list[str] = []
    for w in words:
        cur.append(w)
        tw, _ = text_size(ld, " ".join(cur), title_f)
        if tw > text_max_w:
            cur.pop()
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))

    # Vertically center stack
    line_h = int(110 * 1.18)
    block_h = line_h * len(lines) + 70
    y = (H - block_h) // 2
    for line in lines:
        ld.text((pad, y), line, font=title_f, fill=(255, 255, 255, text_alpha))
        y += line_h
    y += 14
    ld.text((pad, y), sub, font=sub_f,
            fill=(HP_LIGHT[0], HP_LIGHT[1], HP_LIGHT[2], sub_alpha))

    # End of scene: ease the phone back out (last 0.4s)
    if local_t > scene_dur - 0.4:
        out_p = ease_in_out((local_t - (scene_dur - 0.4)) / 0.4)
        # Recreate canvas with phone moving further right and fading
        out_x = int(lerp(target_x, W + 60, out_p))
        # Re-render: cheap approach — redraw phone over canvas at out_x with reduced alpha
        # We've already pasted the phone at target_x; instead we'll skip altering
        # and let the next scene's slide-in cover it.

    canvas.alpha_composite(layer)
    return canvas.convert("RGB")


def scene_home(t: float, local_t: float) -> Image.Image:
    return _scene_phone_with_text(t, DEV_HOME, "12 tools.\nOne tap each.",
                                  "Print, scan, copy and fax — all in one app.",
                                  local_t, 5.0)


def scene_print_photo(t: float, local_t: float) -> Image.Image:
    return _scene_phone_with_text(t, DEV_PHOTO, "Print photos\nin seconds.",
                                  "Pick from your gallery. Done.",
                                  local_t, 5.0)


def scene_scan(t: float, local_t: float) -> Image.Image:
    return _scene_phone_with_text(t, DEV_SCAN, "Scan with\nyour camera.",
                                  "Save as PDF or print straight away.",
                                  local_t, 5.0)


def scene_id(t: float, local_t: float) -> Image.Image:
    return _scene_phone_with_text(t, DEV_ID, "Copy IDs,\nboth sides.",
                                  "Front and back, on a single page.",
                                  local_t, 5.0)


def scene_outro(t: float, local_t: float, scene_dur: float) -> Image.Image:
    """Final brand card: large icon + CTA."""
    canvas = gradient_bg(W, H, t).convert("RGBA")

    p = ease_out(min(1.0, local_t / 0.6))
    icon_size = int(420 * p) if p > 0.02 else 1
    icon = APP_ICON_LARGE.resize((icon_size, icon_size), Image.LANCZOS) if icon_size > 1 else None
    if icon is not None:
        ix = (W - icon_size) // 2
        iy = (H - icon_size) // 2 - 140
        paste_with_shadow(canvas, icon, (ix, iy), shadow_blur=45, shadow_alpha=160)

    title_alpha = int(255 * ease_out(max(0, (local_t - 0.5) / 0.7)))
    sub_alpha = int(255 * ease_out(max(0, (local_t - 0.9) / 0.7)))
    cta_alpha = int(255 * ease_out(max(0, (local_t - 1.3) / 0.7)))

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    title_f = font(96, bold=True)
    sub_f = font(46)
    cta_f = font(40, bold=True)

    title = "HP Printer Tools"
    tw, th = text_size(ld, title, title_f)
    ld.text(((W - tw) // 2, H // 2 + 180), title, font=title_f, fill=(255, 255, 255, title_alpha))

    sub = "Free · No ads · No sign-up"
    sw, sh = text_size(ld, sub, sub_f)
    ld.text(((W - sw) // 2, H // 2 + 290), sub, font=sub_f,
            fill=(HP_LIGHT[0], HP_LIGHT[1], HP_LIGHT[2], sub_alpha))

    # CTA pill
    cta_text = "Get it on Google Play"
    cw, ch = text_size(ld, cta_text, cta_f)
    pill_w = cw + 80
    pill_h = ch + 36
    pill_x = (W - pill_w) // 2
    pill_y = H // 2 + 380
    ld.rounded_rectangle(
        (pill_x, pill_y, pill_x + pill_w, pill_y + pill_h),
        radius=pill_h // 2,
        fill=(255, 255, 255, cta_alpha),
    )
    ld.text((pill_x + 40, pill_y + 14),
            cta_text, font=cta_f,
            fill=(HP_DARK[0], HP_DARK[1], HP_DARK[2], cta_alpha))

    canvas.alpha_composite(layer)
    return canvas.convert("RGB")


# ---------- timeline -------------------------------------------------------

def render_frame(t: float) -> Image.Image:
    if t < 4.0:
        return scene_intro(t)
    elif t < 9.0:
        return scene_home(t, t - 4.0)
    elif t < 14.0:
        return scene_print_photo(t, t - 9.0)
    elif t < 19.0:
        return scene_scan(t, t - 14.0)
    elif t < 24.0:
        return scene_id(t, t - 19.0)
    else:
        return scene_outro(t, t - 24.0, 6.0)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    print(f"Rendering {TOTAL} frames at {W}x{H}@{FPS} → {OUT.relative_to(ROOT)}")
    writer = imageio.get_writer(
        str(OUT),
        fps=FPS,
        codec="libx264",
        quality=8,
        macro_block_size=1,
        ffmpeg_params=["-pix_fmt", "yuv420p", "-movflags", "+faststart"],
    )
    try:
        for i in range(TOTAL):
            t = i / FPS
            frame = render_frame(t)
            writer.append_data(_to_array(frame))
            if i % 30 == 0:
                print(f"  frame {i:4d}/{TOTAL}  t={t:5.2f}s")
    finally:
        writer.close()
    print(f"  → {OUT}")


def _to_array(img: Image.Image):
    import numpy as np
    if img.mode != "RGB":
        img = img.convert("RGB")
    return np.asarray(img)


if __name__ == "__main__":
    main()
