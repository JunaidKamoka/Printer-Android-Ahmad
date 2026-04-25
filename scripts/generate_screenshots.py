#!/usr/bin/env python3
"""Generate Play Store screenshots for HP Printer Tools.

Renders the app's UI as a marketing screenshot with a tagline at the top
and the simulated phone/tablet UI below. Output goes to:

  playstore/screenshots/phone/    1080x1920  (5 frames)
  playstore/screenshots/tablet7/  1200x1920  (3 frames)
  playstore/screenshots/tablet10/ 1600x2560  (3 frames)

Run:  python3 scripts/generate_screenshots.py
"""
from __future__ import annotations

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT_PHONE = ROOT / "playstore" / "screenshots" / "phone"
OUT_T7 = ROOT / "playstore" / "screenshots" / "tablet7"
OUT_T10 = ROOT / "playstore" / "screenshots" / "tablet10"

HP_BLUE = (0, 150, 214)
HP_DARK = (0, 63, 107)
HP_LIGHT = (230, 244, 251)
WHITE = (255, 255, 255)
BG_GRAY = (247, 250, 252)
TEXT_DARK = (20, 30, 40)
TEXT_MUTED = (110, 125, 140)
CARD_BORDER = (235, 240, 245)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates_bold = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    candidates_reg = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for p in (candidates_bold if bold else candidates_reg):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def text_size(d: ImageDraw.ImageDraw, txt: str, f: ImageFont.FreeTypeFont) -> tuple[int, int]:
    bbox = d.textbbox((0, 0), txt, font=f)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def round_rect(d: ImageDraw.ImageDraw, xy, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


# ---------- icon glyphs (simple, recognizable) -----------------------------

def draw_icon_glyph(canvas: Image.Image, kind: str, color: tuple[int, int, int]):
    """Draw a small monochrome glyph centered on a square canvas."""
    W, H = canvas.size
    d = ImageDraw.Draw(canvas)
    pad = int(W * 0.18)
    cx = cy = W // 2

    if kind == "image":
        round_rect(d, (pad, pad, W - pad, H - pad), W * 0.10, outline=color, width=max(2, W // 22))
        d.ellipse((pad + W * 0.12, pad + W * 0.12, pad + W * 0.32, pad + W * 0.32), fill=color)
        # mountain
        pts = [(pad + W * 0.10, H - pad - W * 0.05),
               (W * 0.45, pad + W * 0.30),
               (W * 0.65, H - pad - W * 0.20),
               (W - pad - W * 0.05, H - pad - W * 0.05)]
        d.polygon(pts, fill=color)
    elif kind == "pdf":
        round_rect(d, (pad, pad, W - pad, H - pad), W * 0.08, outline=color, width=max(2, W // 22))
        # folded corner
        d.polygon([(W - pad - W * 0.20, pad), (W - pad, pad + W * 0.20), (W - pad - W * 0.20, pad + W * 0.20)], fill=color)
        # lines
        for i, y in enumerate([0.45, 0.58, 0.71]):
            yy = int(H * y)
            d.line([(pad + W * 0.10, yy), (W - pad - W * 0.18 - i * W * 0.05, yy)], fill=color, width=max(2, W // 30))
    elif kind == "scan":
        # frame with corners + center bar
        c = max(2, W // 18)
        L = int(W * 0.10)
        d.line([(pad, pad + L), (pad, pad), (pad + L, pad)], fill=color, width=c)
        d.line([(W - pad - L, pad), (W - pad, pad), (W - pad, pad + L)], fill=color, width=c)
        d.line([(pad, H - pad - L), (pad, H - pad), (pad + L, H - pad)], fill=color, width=c)
        d.line([(W - pad - L, H - pad), (W - pad, H - pad), (W - pad, H - pad - L)], fill=color, width=c)
        d.line([(pad + W * 0.05, H // 2), (W - pad - W * 0.05, H // 2)], fill=color, width=c)
    elif kind == "copy":
        # two stacked rectangles
        round_rect(d, (pad + W * 0.15, pad + W * 0.05, W - pad, H - pad - W * 0.15), W * 0.06, outline=color, width=max(2, W // 22))
        round_rect(d, (pad, pad + W * 0.15, W - pad - W * 0.15, H - pad - W * 0.05), W * 0.06, fill=WHITE, outline=color, width=max(2, W // 22))
    elif kind == "id":
        round_rect(d, (pad, pad + W * 0.12, W - pad, H - pad - W * 0.12), W * 0.06, outline=color, width=max(2, W // 22))
        # avatar circle
        d.ellipse((pad + W * 0.10, pad + W * 0.22, pad + W * 0.36, pad + W * 0.48), fill=color)
        # lines
        for y in [0.30, 0.42, 0.54]:
            yy = int(H * y)
            d.line([(W * 0.45, yy), (W - pad - W * 0.10, yy)], fill=color, width=max(2, W // 30))
    elif kind == "fax" or kind == "email":
        # envelope
        round_rect(d, (pad, pad + W * 0.10, W - pad, H - pad - W * 0.10), W * 0.06, outline=color, width=max(2, W // 22))
        d.line([(pad, pad + W * 0.10), (cx, cy), (W - pad, pad + W * 0.10)], fill=color, width=max(2, W // 26))
    elif kind == "wifi":
        for i, r in enumerate([0.18, 0.30, 0.42]):
            R = int(W * r)
            bbox = (cx - R, cy - R + W * 0.10, cx + R, cy + R + W * 0.10)
            start, end = 220, 320
            d.arc(bbox, start, end, fill=color, width=max(2, W // 20))
        d.ellipse((cx - W * 0.05, cy + W * 0.10 - W * 0.05, cx + W * 0.05, cy + W * 0.10 + W * 0.05), fill=color)
    elif kind == "printer":
        round_rect(d, (pad, pad + W * 0.05, W - pad, pad + W * 0.30), W * 0.04, fill=color)
        round_rect(d, (pad - W * 0.02, pad + W * 0.25, W - pad + W * 0.02, H - pad - W * 0.10), W * 0.06, outline=color, width=max(2, W // 22))
        round_rect(d, (pad + W * 0.05, H - pad - W * 0.20, W - pad - W * 0.05, H - pad), W * 0.04, outline=color, width=max(2, W // 26))
    elif kind == "drop":
        # stylized water drop
        d.polygon([(cx, pad), (W - pad, cy + W * 0.10), (cx, H - pad), (pad, cy + W * 0.10)], outline=color, width=max(2, W // 22))
    elif kind == "globe":
        d.ellipse((pad, pad, W - pad, H - pad), outline=color, width=max(2, W // 22))
        d.line([(pad, cy), (W - pad, cy)], fill=color, width=max(2, W // 30))
        d.arc((cx - W * 0.18, pad, cx + W * 0.18, H - pad), 0, 360, fill=color, width=max(2, W // 30))
    elif kind == "puzzle":
        round_rect(d, (pad, pad, W - pad, H - pad), W * 0.10, outline=color, width=max(2, W // 22))
        d.ellipse((cx - W * 0.10, pad - W * 0.05, cx + W * 0.10, pad + W * 0.15), fill=color)
        d.ellipse((W - pad - W * 0.10, cy - W * 0.10, W - pad + W * 0.10, cy + W * 0.10), fill=color)
    elif kind == "settings":
        for k in range(8):
            ang = math.radians(k * 45)
            x = cx + math.cos(ang) * W * 0.32
            y = cy + math.sin(ang) * W * 0.32
            d.ellipse((x - W * 0.06, y - W * 0.06, x + W * 0.06, y + W * 0.06), fill=color)
        d.ellipse((cx - W * 0.18, cy - W * 0.18, cx + W * 0.18, cy + W * 0.18), fill=WHITE, outline=color, width=max(2, W // 22))
    elif kind == "camera":
        round_rect(d, (pad, pad + W * 0.10, W - pad, H - pad), W * 0.06, outline=color, width=max(2, W // 22))
        round_rect(d, (cx - W * 0.18, pad, cx + W * 0.18, pad + W * 0.15), W * 0.04, fill=color)
        d.ellipse((cx - W * 0.18, cy - W * 0.10, cx + W * 0.18, cy + W * 0.28), outline=color, width=max(2, W // 22))


# ---------- UI primitives --------------------------------------------------

TOOLS = [
    ("Print Photo",     "From gallery",   "image",    HP_BLUE),
    ("Print Document",  "PDF & DOCX",     "pdf",      HP_BLUE),
    ("Scan Document",   "Use camera",     "scan",     HP_BLUE),
    ("Photocopy",       "Capture & print","copy",     HP_BLUE),
    ("ID Card Copy",    "Front & back",   "id",       HP_BLUE),
    ("Mobile Fax",      "Send by email",  "fax",      HP_BLUE),
    ("Find Printer",    "Wi-Fi setup",    "wifi",     HP_BLUE),
    ("Printer Status",  "Print services", "printer",  HP_BLUE),
    ("Ink Levels",      "Check supplies", "drop",     HP_BLUE),
    ("Setup Printer",   "123.hp.com",     "camera",   HP_BLUE),
    ("Print Web Page",  "From browser",   "globe",    HP_BLUE),
    ("HP Print Plugin", "Play Store",     "puzzle",   HP_BLUE),
]


def status_bar(canvas: Image.Image, height: int):
    d = ImageDraw.Draw(canvas)
    W, _ = canvas.size
    d.rectangle((0, 0, W, height), fill=HP_DARK)
    f = font(int(height * 0.45), bold=True)
    d.text((int(W * 0.04), int(height * 0.22)), "9:41", font=f, fill=WHITE)
    # right side icons (simple bars + battery)
    rx = W - int(W * 0.04)
    # battery
    bw, bh = int(height * 0.7), int(height * 0.35)
    bx, by = rx - bw, int(height * 0.30)
    d.rounded_rectangle((bx, by, bx + bw, by + bh), radius=4, outline=WHITE, width=2)
    d.rectangle((bx + bw, by + bh // 4, bx + bw + 3, by + bh - bh // 4), fill=WHITE)
    d.rounded_rectangle((bx + 3, by + 3, bx + bw - 3, by + bh - 3), radius=2, fill=WHITE)
    # wifi triangle
    wx = bx - int(W * 0.02)
    d.polygon([(wx, by + bh), (wx - bh, by + bh), (wx - bh // 2, by)], fill=WHITE)
    # signal bars
    sx = wx - bh - int(W * 0.025)
    for i in range(4):
        bw2 = 4
        h = (i + 1) * (bh // 4)
        d.rectangle((sx - i * (bw2 + 3), by + bh - h, sx + bw2 - i * (bw2 + 3), by + bh), fill=WHITE)


def app_header(canvas: Image.Image, top: int, title: str, subtitle: str | None = None, back: bool = False) -> int:
    """Draw the gradient app header. Returns y-offset where content starts."""
    W, _ = canvas.size
    height = int(W * 0.36)
    grad = Image.new("RGB", (W, height), HP_BLUE)
    px = grad.load()
    for y in range(height):
        for x in range(W):
            t = (x / W) * 0.6 + (y / height) * 0.2
            t = max(0.0, min(1.0, t))
            px[x, y] = (
                int(HP_BLUE[0] * (1 - t) + HP_DARK[0] * t),
                int(HP_BLUE[1] * (1 - t) + HP_DARK[1] * t),
                int(HP_BLUE[2] * (1 - t) + HP_DARK[2] * t),
            )
    canvas.paste(grad, (0, top))
    d = ImageDraw.Draw(canvas)
    if back:
        # back arrow
        cx0 = int(W * 0.07)
        cy0 = top + int(height * 0.42)
        d.line([(cx0 + 22, cy0 - 22), (cx0, cy0), (cx0 + 22, cy0 + 22)], fill=WHITE, width=6)
    pad_x = int(W * 0.18 if back else W * 0.06)
    title_f = font(int(W * 0.085), bold=True)
    d.text((pad_x, top + int(height * 0.30)), title, font=title_f, fill=WHITE)
    if subtitle:
        sub_f = font(int(W * 0.038))
        d.text((pad_x, top + int(height * 0.65)), subtitle, font=sub_f, fill=HP_LIGHT)
    return top + height


def grid_card(canvas: Image.Image, x: int, y: int, w: int, h: int, name: str, sub: str, kind: str):
    d = ImageDraw.Draw(canvas)
    round_rect(d, (x, y, x + w, y + h), 30, fill=WHITE, outline=CARD_BORDER, width=2)
    icon_size = int(w * 0.30)
    icon = Image.new("RGBA", (icon_size, icon_size), (230, 244, 251, 255))
    glyph_canvas = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
    draw_icon_glyph(glyph_canvas, kind, HP_BLUE)
    icon = Image.alpha_composite(icon, glyph_canvas)
    # rounded mask
    mask = Image.new("L", (icon_size, icon_size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, icon_size, icon_size), radius=int(icon_size * 0.22), fill=255)
    canvas.paste(icon, (x + 30, y + 30), mask)

    name_f = font(int(w * 0.085), bold=True)
    sub_f = font(int(w * 0.060))
    d.text((x + 30, y + h - int(w * 0.32)), name, font=name_f, fill=TEXT_DARK)
    d.text((x + 30, y + h - int(w * 0.18)), sub, font=sub_f, fill=TEXT_MUTED)


# ---------- screen renderers ----------------------------------------------

def render_home(W: int, H: int) -> Image.Image:
    img = Image.new("RGB", (W, H), BG_GRAY)
    sb = int(W * 0.06)
    status_bar(img, sb)
    content_top = app_header(img, sb, "HP Smart Tools", "Pick a tool to get started")
    pad = int(W * 0.04)
    cols = 3
    gap = int(W * 0.025)
    card_w = (W - pad * 2 - gap * (cols - 1)) // cols
    card_h = card_w
    for i, (name, sub, kind, _) in enumerate(TOOLS):
        col = i % cols
        row = i // cols
        x = pad + col * (card_w + gap)
        y = content_top + pad + row * (card_h + gap)
        if y + card_h > H - pad:
            break
        grid_card_compact(img, x, y, card_w, card_h, name, kind)
    return img


def grid_card_compact(canvas: Image.Image, x: int, y: int, w: int, h: int, name: str, kind: str):
    """Compact 3-col card — icon on top, name below, no subtitle."""
    d = ImageDraw.Draw(canvas)
    round_rect(d, (x, y, x + w, y + h), 24, fill=WHITE, outline=CARD_BORDER, width=2)
    icon_size = int(w * 0.45)
    icon = Image.new("RGBA", (icon_size, icon_size), (230, 244, 251, 255))
    glyph_canvas = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
    draw_icon_glyph(glyph_canvas, kind, HP_BLUE)
    icon = Image.alpha_composite(icon, glyph_canvas)
    mask = Image.new("L", (icon_size, icon_size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, icon_size, icon_size), radius=int(icon_size * 0.22), fill=255)
    icon_x = x + (w - icon_size) // 2
    icon_y = y + int(w * 0.15)
    canvas.paste(icon, (icon_x, icon_y), mask)

    name_f = font(int(w * 0.105), bold=True)
    tw, _ = text_size(d, name, name_f)
    if tw > w - 20:
        name_f = font(int(w * 0.085), bold=True)
        tw, _ = text_size(d, name, name_f)
    d.text((x + (w - tw) // 2, y + h - int(w * 0.30)), name, font=name_f, fill=TEXT_DARK)


def render_tool_detail(W: int, H: int, name: str, kind: str, description: str, button: str = "Use this tool") -> Image.Image:
    img = Image.new("RGB", (W, H), BG_GRAY)
    sb = int(W * 0.06)
    status_bar(img, sb)
    content_top = app_header(img, sb, name, back=True)

    d = ImageDraw.Draw(img)
    # Big rounded icon square
    icon_size = int(W * 0.45)
    icon_x = (W - icon_size) // 2
    icon_y = content_top + int(W * 0.10)
    bg = Image.new("RGBA", (icon_size, icon_size), (230, 244, 251, 255))
    glyph = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
    draw_icon_glyph(glyph, kind, HP_BLUE)
    bg = Image.alpha_composite(bg, glyph)
    mask = Image.new("L", (icon_size, icon_size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, icon_size, icon_size), radius=int(icon_size * 0.20), fill=255)
    img.paste(bg, (icon_x, icon_y), mask)

    # Title
    title_f = font(int(W * 0.085), bold=True)
    title_w, _ = text_size(d, name, title_f)
    d.text(((W - title_w) // 2, icon_y + icon_size + int(W * 0.06)), name, font=title_f, fill=TEXT_DARK)

    # Description (wrap)
    desc_f = font(int(W * 0.045))
    pad = int(W * 0.08)
    words = description.split()
    lines = []
    cur = []
    for w in words:
        cur.append(w)
        tw, _ = text_size(d, " ".join(cur), desc_f)
        if tw > W - pad * 2:
            cur.pop()
            lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    y = icon_y + icon_size + int(W * 0.20)
    line_h = int(W * 0.065)
    for line in lines:
        tw, _ = text_size(d, line, desc_f)
        d.text(((W - tw) // 2, y), line, font=desc_f, fill=TEXT_MUTED)
        y += line_h

    # Button
    btn_h = int(W * 0.16)
    btn_w = W - pad * 2
    btn_y = H - btn_h - int(W * 0.12)
    round_rect(d, (pad, btn_y, pad + btn_w, btn_y + btn_h), 32, fill=HP_BLUE)
    btn_f = font(int(W * 0.055), bold=True)
    bw, bh = text_size(d, button, btn_f)
    d.text(((W - bw) // 2, btn_y + (btn_h - bh) // 2 - 4), button, font=btn_f, fill=WHITE)
    return img


# ---------- compose with marketing tagline --------------------------------

def compose_marketing(ui: Image.Image, target_w: int, target_h: int, headline: str, sub: str) -> Image.Image:
    canvas = Image.new("RGB", (target_w, target_h), HP_DARK)
    # Gradient background
    px = canvas.load()
    for y in range(target_h):
        for x in range(target_w):
            t = (y / target_h)
            px[x, y] = (
                int(HP_DARK[0] * (1 - t) + HP_BLUE[0] * t * 0.65 + HP_DARK[0] * t * 0.35),
                int(HP_DARK[1] * (1 - t) + HP_BLUE[1] * t * 0.65 + HP_DARK[1] * t * 0.35),
                int(HP_DARK[2] * (1 - t) + HP_BLUE[2] * t * 0.65 + HP_DARK[2] * t * 0.35),
            )

    d = ImageDraw.Draw(canvas)
    # Headline area at top (~22% of height)
    title_f = font(int(target_w * 0.075), bold=True)
    sub_f = font(int(target_w * 0.038))
    # Wrap headline (manual, two lines max)
    pad = int(target_w * 0.06)
    line_y = int(target_h * 0.04)

    # Headline
    words = headline.split()
    lines: list[str] = []
    cur: list[str] = []
    for w in words:
        cur.append(w)
        tw, _ = text_size(d, " ".join(cur), title_f)
        if tw > target_w - pad * 2:
            cur.pop()
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    for line in lines[:2]:
        tw, th = text_size(d, line, title_f)
        d.text(((target_w - tw) // 2, line_y), line, font=title_f, fill=WHITE)
        line_y += int(th * 1.15)

    # Sub
    line_y += int(target_w * 0.015)
    tw, th = text_size(d, sub, sub_f)
    d.text(((target_w - tw) // 2, line_y), sub, font=sub_f, fill=HP_LIGHT)
    headline_bottom = line_y + th + int(target_w * 0.04)

    # Phone frame: scale UI to fit remaining area
    avail_h = target_h - headline_bottom - int(target_w * 0.04)
    avail_w = int(target_w * 0.86)
    ui_w, ui_h = ui.size
    scale = min(avail_w / ui_w, avail_h / ui_h)
    new_w, new_h = int(ui_w * scale), int(ui_h * scale)
    ui_resized = ui.resize((new_w, new_h), Image.LANCZOS)

    # Round the corners of the UI to look like a device screen
    bezel = int(new_w * 0.04)
    frame_w, frame_h = new_w + bezel * 2, new_h + bezel * 2
    frame = Image.new("RGB", (frame_w, frame_h), (10, 14, 20))
    frame.paste(ui_resized, (bezel, bezel))
    # Mask the whole frame with rounded corners
    mask = Image.new("L", (frame_w, frame_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, frame_w, frame_h), radius=int(frame_w * 0.07), fill=255)

    # Drop shadow
    shadow = Image.new("RGBA", (frame_w + 80, frame_h + 80), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((40, 40, frame_w + 40, frame_h + 40), radius=int(frame_w * 0.07), fill=(0, 0, 0, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=20))

    fx = (target_w - frame_w) // 2
    fy = headline_bottom
    canvas.paste(shadow.convert("RGB"), (fx - 40, fy - 40 + 12), shadow.split()[3])
    canvas.paste(frame, (fx, fy), mask)
    return canvas


# ---------- main pipeline -------------------------------------------------

def make_phone_screenshots():
    OUT_PHONE.mkdir(parents=True, exist_ok=True)
    UI_W, UI_H = 1080, 1920  # internal UI render size (also final size)
    target_w, target_h = 1080, 1920

    plans = [
        ("01_home.png",
         render_home(UI_W, UI_H),
         "12 powerful tools, one tap away",
         "Print, scan, copy and fax with any HP printer"),
        ("02_print_photo.png",
         render_tool_detail(UI_W, UI_H, "Print Photo", "image",
                            "Pick a picture from your gallery and print it instantly."),
         "Print photos in seconds",
         "Straight from your gallery — no extra steps"),
        ("03_scan.png",
         render_tool_detail(UI_W, UI_H, "Scan Document", "scan",
                            "Capture a page with your camera, then save or print the result."),
         "Turn your phone into a scanner",
         "Capture, save or print — all from one screen"),
        ("04_id_copy.png",
         render_tool_detail(UI_W, UI_H, "ID Card Copy", "id",
                            "Capture both sides of an ID card and print them combined on a single page."),
         "Copy IDs both sides on one page",
         "Front and back, perfectly aligned"),
        ("05_setup.png",
         render_tool_detail(UI_W, UI_H, "Setup Printer", "camera",
                            "Walk through the official HP setup flow at 123.hp.com."),
         "Set up any HP printer in seconds",
         "Wi-Fi, Wi-Fi Direct, USB — all supported"),
    ]

    for name, ui_img, headline, sub in plans:
        out = compose_marketing(ui_img, target_w, target_h, headline, sub)
        out.save(OUT_PHONE / name, optimize=True)
        print(f"  phone/{name}")


def make_tablet7_screenshots():
    OUT_T7.mkdir(parents=True, exist_ok=True)
    target_w, target_h = 1200, 1920
    UI_W, UI_H = 1080, 1920
    plans = [
        ("01_home.png",
         render_home(UI_W, UI_H),
         "12 tools for your HP printer",
         "Print · Scan · Copy · Fax"),
        ("02_print_photo.png",
         render_tool_detail(UI_W, UI_H, "Print Photo", "image",
                            "Pick a picture from your gallery and print it instantly."),
         "Print from gallery in two taps",
         "No accounts, no sign-in, no fuss"),
        ("03_setup.png",
         render_tool_detail(UI_W, UI_H, "Setup Printer", "camera",
                            "Walk through the official HP setup flow at 123.hp.com."),
         "Set up your printer fast",
         "Wi-Fi or Wi-Fi Direct, in seconds"),
    ]
    for name, ui_img, headline, sub in plans:
        out = compose_marketing(ui_img, target_w, target_h, headline, sub)
        out.save(OUT_T7 / name, optimize=True)
        print(f"  tablet7/{name}")


def make_tablet10_screenshots():
    OUT_T10.mkdir(parents=True, exist_ok=True)
    target_w, target_h = 1600, 2560
    UI_W, UI_H = 1080, 1920
    plans = [
        ("01_home.png",
         render_home(UI_W, UI_H),
         "12 powerful HP printer tools",
         "Print, scan, copy and fax — all in one app"),
        ("02_scan.png",
         render_tool_detail(UI_W, UI_H, "Scan Document", "scan",
                            "Capture a page with your camera, then save or print the result."),
         "Scan to PDF on the go",
         "Camera scanning that prints in one tap"),
        ("03_id.png",
         render_tool_detail(UI_W, UI_H, "ID Card Copy", "id",
                            "Capture both sides of an ID card and print them combined on a single page."),
         "ID cards copied perfectly",
         "Front and back combined automatically"),
    ]
    for name, ui_img, headline, sub in plans:
        out = compose_marketing(ui_img, target_w, target_h, headline, sub)
        out.save(OUT_T10 / name, optimize=True)
        print(f"  tablet10/{name}")


def main():
    make_phone_screenshots()
    make_tablet7_screenshots()
    make_tablet10_screenshots()


if __name__ == "__main__":
    main()
