#!/usr/bin/env python3
"""Render a completely local, text-free LATCHES hero animation."""

import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import imageio_ffmpeg


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "LATCHES Image 1.png"
OUT = ROOT / "output" / "latches-ceiling-hero" / "LATCHES-ceiling-hero-local.mp4"
W, H, FPS, SECONDS = 1280, 720, 30, 15


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def mix(a, b, t):
    return a + (b - a) * t


def rgba(c, alpha):
    return tuple(c) + (round(alpha),)


def paste_fit(dst, src, box, alpha=255):
    x, y, w, h = map(round, box)
    if w < 2 or h < 2:
        return
    item = src.resize((w, h), Image.Resampling.LANCZOS)
    if alpha != 255:
        item = item.copy()
        item.putalpha(item.getchannel("A").point(lambda p: p * alpha // 255))
    dst.alpha_composite(item, (x, y))


def ceiling_tiles(layer, panel, amount, thermal):
    draw = ImageDraw.Draw(layer, "RGBA")
    horizon = 300
    rows, cols = 5, 9
    for r in range(rows):
        depth = r / (rows - 1)
        cy = mix(76, horizon, depth ** 1.55)
        scale = mix(0.20, 0.54, depth)
        gap = mix(82, 178, depth)
        row_alpha = 255 * smooth(amount * 1.55 - r * 0.10)
        for c in range(cols):
            distance = abs(c - (cols - 1) / 2)
            reveal = smooth(amount * 1.8 - (r * .07 + distance * .055))
            if reveal <= 0:
                continue
            tw, th = 170 * scale, 108 * scale
            x = W / 2 + (c - 4) * gap - tw / 2
            y = cy - th / 2
            paste_fit(layer, panel, (x, y, tw, th), round(row_alpha * reveal))
            draw.rounded_rectangle((x+2, y+2, x+tw-2, y+th-2), radius=max(2, 5*scale),
                                   outline=(185, 202, 207, round(100*reveal)), width=1)
            if thermal > 0:
                draw.rounded_rectangle((x+4, y+4, x+tw-4, y+th-4), radius=max(2, 5*scale),
                                       fill=(244, 92, 76, round(95*thermal*reveal)))


def room(draw, build, thermal):
    # Architecture resolves from cyan construction lines into material surfaces.
    floor_top = 315
    fill_alpha = round(235 * smooth((build - .22) / .55))
    line_alpha = round(220 * smooth(build / .42) * (1 - .55 * thermal))
    draw.polygon([(0, floor_top), (W, floor_top), (W, H), (0, H)],
                 fill=(round(mix(229, 24, thermal)), round(mix(235, 35, thermal)), round(mix(237, 65, thermal)), fill_alpha))
    draw.polygon([(0, 280), (210, 315), (210, H), (0, H)], fill=(25, 45, 56, fill_alpha))
    draw.polygon([(W, 280), (1070, 315), (1070, H), (W, H)], fill=(25, 45, 56, fill_alpha))
    # Windows and mullions.
    for x in range(230, 1060, 138):
        draw.rectangle((x, 330, x+112, 510), fill=(21, 52, 68, fill_alpha),
                       outline=(78, 151, 167, line_alpha), width=2)
        draw.line((x+56, 330, x+56, 510), fill=(100, 191, 203, line_alpha), width=1)
    # Floor perspective.
    for x in range(0, W+1, 128):
        draw.line((W/2, floor_top, x, H), fill=(69, 137, 150, round(line_alpha*.45)), width=1)
    for y in (390, 480, 590, 680):
        draw.line((0, y, W, y), fill=(69, 137, 150, round(line_alpha*.38)), width=1)


def workstation(draw, x, y, s, alpha, thermal):
    edge = (104, 178, 189, alpha)
    desk = tuple(round(mix(a, b, thermal)) for a, b in zip((72, 88, 94), (35, 34, 60))) + (alpha,)
    draw.rounded_rectangle((x-74*s, y, x+74*s, y+12*s), radius=3*s, fill=desk, outline=edge, width=max(1, round(2*s)))
    draw.line((x-55*s, y+12*s, x-62*s, y+85*s), fill=edge, width=max(1, round(3*s)))
    draw.line((x+55*s, y+12*s, x+62*s, y+85*s), fill=edge, width=max(1, round(3*s)))
    # Computer: no UI or text.
    draw.rounded_rectangle((x-31*s, y-44*s, x+31*s, y-4*s), radius=3*s,
                           fill=(round(mix(26, 243, thermal)), round(mix(45, 94, thermal)), round(mix(57, 45, thermal)), alpha),
                           outline=edge, width=max(1, round(2*s)))
    draw.line((x, y-4*s, x, y+3*s), fill=edge, width=max(1, round(2*s)))


def person(draw, x, y, s, alpha, thermal, phase):
    warm = (round(mix(62, 255, thermal)), round(mix(78, 91, thermal)), round(mix(87, 40, thermal)), alpha)
    skin = (round(mix(157, 255, thermal)), round(mix(117, 113, thermal)), round(mix(91, 47, thermal)), alpha)
    bob = math.sin(phase) * 2 * s
    draw.ellipse((x-13*s, y-86*s+bob, x+13*s, y-60*s+bob), fill=skin)
    draw.rounded_rectangle((x-22*s, y-61*s+bob, x+22*s, y-8*s+bob), radius=10*s, fill=warm)
    draw.line((x-14*s, y-7*s+bob, x-22*s, y+35*s), fill=warm, width=max(2, round(8*s)))
    draw.line((x+14*s, y-7*s+bob, x+22*s, y+35*s), fill=warm, width=max(2, round(8*s)))
    draw.line((x-18*s, y-48*s+bob, x-40*s, y-20*s), fill=skin, width=max(2, round(7*s)))
    draw.line((x+18*s, y-48*s+bob, x+38*s, y-24*s), fill=skin, width=max(2, round(7*s)))


def heat_particles(layer, progress, seed_offset):
    draw = ImageDraw.Draw(layer, "RGBA")
    sources = [(310, 520), (510, 590), (720, 505), (925, 590)]
    for si, (sx, sy) in enumerate(sources):
        for i in range(12):
            p = (progress * .75 + i / 12 + si * .11) % 1
            y = mix(sy, 245, p)
            x = sx + math.sin(p*8 + i*1.7 + seed_offset) * (18 + 16*p)
            a = 180 * math.sin(math.pi*p) * smooth(progress)
            radius = 3 + 9*p
            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(255, 86, 54, round(a)))


def frame_at(t, panel):
    # phases: product 0-3, ceiling 2-6, room 4-9, thermal 9-15
    expand = smooth((t - 2.0) / 3.6)
    build = smooth((t - 4.2) / 3.5)
    thermal = smooth((t - 9.0) / 3.0)
    bg = tuple(round(mix(a, b, thermal)) for a, b in zip((236, 241, 242), (8, 18, 42)))
    img = Image.new("RGBA", (W, H), bg + (255,))

    # Initial real product photograph, slowly moving into the ceiling plane.
    intro = 1 - smooth((t - 2.1) / 2.4)
    if intro > 0:
        scale = mix(1.0, .62, smooth(t / 4.2))
        pw, ph = 770*scale, 505*scale
        y = mix(95, 4, smooth(t / 4.2))
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow, "RGBA")
        sd.ellipse((W/2-pw*.42, y+ph*.68, W/2+pw*.42, y+ph*.90), fill=(7, 27, 35, round(90*intro)))
        shadow = shadow.filter(ImageFilter.GaussianBlur(24))
        img.alpha_composite(shadow)
        paste_fit(img, panel, (W/2-pw/2, y, pw, ph), round(255*intro))

    room_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(room_layer, "RGBA")
    if build > 0:
        room(rd, build, thermal)
        alpha = round(255*smooth((build-.15)/.55))
        for j, (x, y, s) in enumerate([(315, 535, .82), (500, 620, 1.0), (735, 525, .80), (940, 620, 1.0)]):
            workstation(rd, x, y, s, alpha, thermal)
            person(rd, x+20*s, y, s, alpha, thermal, t*1.2+j)
    img.alpha_composite(room_layer)

    ceiling = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if expand > 0:
        ceiling_tiles(ceiling, panel, expand, thermal)
    img.alpha_composite(ceiling)

    if thermal > 0:
        haze = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        heat_particles(haze, thermal, t)
        haze = haze.filter(ImageFilter.GaussianBlur(5))
        img.alpha_composite(haze)
        # Subtle thermal scan sweep.
        scan = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sy = int((t*95) % (H+180)) - 90
        ImageDraw.Draw(scan, "RGBA").rectangle((0, sy-2, W, sy+2), fill=(76, 209, 220, round(70*thermal)))
        img.alpha_composite(scan.filter(ImageFilter.GaussianBlur(7)))

    # Edge vignette keeps overlaid hero copy legible.
    vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette, "RGBA")
    for i in range(90):
        a = round((1-i/90)**2 * 85)
        vd.rectangle((i, i, W-i-1, H-i-1), outline=(5, 20, 30, a), width=2)
    img.alpha_composite(vignette)
    return img.convert("RGB")


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    panel = Image.open(SOURCE).convert("RGBA")
    # Remove only the source image's black transparent-looking backdrop.
    px = panel.load()
    for y in range(panel.height):
        for x in range(panel.width):
            r, g, b, a = px[x, y]
            if r < 18 and g < 18 and b < 18:
                px[x, y] = (r, g, b, 0)
    panel = ImageEnhance.Contrast(panel).enhance(1.03)
    panel.thumbnail((1000, 700), Image.Resampling.LANCZOS)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ffmpeg, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "medium",
           "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(OUT)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    try:
        for n in range(FPS * SECONDS):
            proc.stdin.write(frame_at(n / FPS, panel).tobytes())
            if n % FPS == 0:
                print(f"rendering {n//FPS + 1}/{SECONDS}", flush=True)
    finally:
        proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg encoding failed")
    print(OUT, flush=True)


if __name__ == "__main__":
    main()
