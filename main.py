#!/usr/bin/env python3
"""
Make the cutest picture — make.fun bounty "cutest-picture-01"
https://make.fun/bounty/cutest-picture-01

A deterministic program that paints one picture and writes it to
/output/entry.png (override with the ENTRY_PATH environment variable).

Scene: "Mochi the kitten" — a big-eyed cream kitten sitting in a flower
meadow under a soft pastel sky, with a pink bow, a butterfly, a ball of
yarn, floating hearts and paw prints.

Deterministic: fixed seed, no network, no wall clock, no timestamps in the
PNG. Running the program twice produces byte-identical output.

Stdlib only (a hand-written zlib PNG encoder), so it runs on any Python 3.13
with no third-party packages.

License: MIT
"""

import math
import os
import random
import struct
import zlib

W, H = 1024, 1024
SEED = 20261114


# ---------------------------------------------------------------- canvas ----
class Canvas:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)

    def _i(self, x, y):
        return (y * self.w + x) * 3

    def set(self, x, y, r, g, b):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = self._i(x, y)
            self.px[i] = r
            self.px[i + 1] = g
            self.px[i + 2] = b

    def blend(self, x, y, r, g, b, a):
        """Alpha-blend colour (r,g,b) with alpha a (0..255) over the pixel."""
        if 0 <= x < self.w and 0 <= y < self.h and a > 0:
            i = self._i(x, y)
            if a >= 255:
                self.px[i] = r
                self.px[i + 1] = g
                self.px[i + 2] = b
            else:
                ia = 255 - a
                self.px[i] = (r * a + self.px[i] * ia) // 255
                self.px[i + 1] = (g * a + self.px[i + 1] * ia) // 255
                self.px[i + 2] = (b * a + self.px[i + 2] * ia) // 255

    def fill_row(self, y, color):
        if 0 <= y < self.h:
            i = y * self.w * 3
            self.px[i:i + self.w * 3] = bytes(color) * self.w

    def vgrad(self, y0, y1, c0, c1):
        """Vertical linear gradient between two RGB colours."""
        for y in range(max(0, y0), min(self.h, y1)):
            t = (y - y0) / max(1, y1 - y0 - 1)
            self.fill_row(y, tuple(
                int(c0[k] + (c1[k] - c0[k]) * t) for k in range(3)))

    def disc(self, cx, cy, r, color, alpha=255):
        """Filled disc with 1px antialiased edge."""
        x0 = max(0, int(cx - r - 1))
        x1 = min(self.w - 1, int(cx + r + 1))
        y0 = max(0, int(cy - r - 1))
        y1 = min(self.h - 1, int(cy + r + 1))
        for y in range(y0, y1 + 1):
            dy = y - cy
            for x in range(x0, x1 + 1):
                dx = x - cx
                d = math.sqrt(dx * dx + dy * dy)
                cov = r + 0.5 - d
                if cov <= 0:
                    continue
                a = alpha if cov >= 1 else int(alpha * cov)
                self.blend(x, y, color[0], color[1], color[2], a)

    def ellipse(self, cx, cy, rx, ry, color, alpha=255):
        """Filled ellipse with 1px antialiased edge."""
        x0 = max(0, int(cx - rx - 1))
        x1 = min(self.w - 1, int(cx + rx + 1))
        y0 = max(0, int(cy - ry - 1))
        y1 = min(self.h - 1, int(cy + ry + 1))
        for y in range(y0, y1 + 1):
            ny = (y - cy) / ry
            for x in range(x0, x1 + 1):
                nx = (x - cx) / rx
                d = math.sqrt(nx * nx + ny * ny)
                cov = 1.0 + 0.5 / max(rx, ry) - d
                if cov <= 0:
                    continue
                a = alpha if cov >= 1 else int(alpha * cov)
                self.blend(x, y, color[0], color[1], color[2], a)

    def line(self, x0, y0, x1, y1, color, alpha=255, width=1):
        """Line drawn as a chain of small discs (round caps)."""
        steps = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for i in range(steps + 1):
            t = i / steps
            self.disc(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t,
                      width / 2.0, color, alpha)


def poly_fill(c, pts, color, alpha=255):
    """Scanline fill of a simple polygon given as [(x, y), ...]."""
    ys = [p[1] for p in pts]
    y0, y1 = int(min(ys)), int(max(ys))
    n = len(pts)
    for y in range(max(0, y0), min(c.h, y1 + 1)):
        xs = []
        for i in range(n):
            x1, yy1 = pts[i]
            x2, yy2 = pts[(i + 1) % n]
            if (yy1 <= y < yy2) or (yy2 <= y < yy1):
                t = (y - yy1) / (yy2 - yy1)
                xs.append(x1 + t * (x2 - x1))
        xs.sort()
        for k in range(0, len(xs) - 1, 2):
            for x in range(int(xs[k]), int(xs[k + 1]) + 1):
                c.blend(x, y, color[0], color[1], color[2], alpha)


def heart(c, cx, cy, s, color, alpha=255):
    """A heart of overall size ~s, centred near (cx, cy)."""
    c.disc(cx - s * 0.42, cy - s * 0.18, s * 0.52, color, alpha)
    c.disc(cx + s * 0.42, cy - s * 0.18, s * 0.52, color, alpha)
    poly_fill(c, [(cx - s * 0.92, cy - s * 0.05),
                  (cx + s * 0.92, cy - s * 0.05),
                  (cx, cy + s * 1.05)], color, alpha)


def paw(c, cx, cy, s, color, alpha=255):
    """A little paw print (one pad + four toes)."""
    c.ellipse(cx, cy + s * 0.28, s * 0.52, s * 0.42, color, alpha)
    for dx, dy in ((-0.62, -0.42), (-0.21, -0.62), (0.21, -0.62),
                   (0.62, -0.42)):
        c.disc(cx + dx * s, cy + dy * s, s * 0.22, color, alpha)


def sparkle(c, cx, cy, s, color, alpha=230):
    """A four-point sparkle star."""
    poly_fill(c, [(cx, cy - s), (cx + s * 0.28, cy - s * 0.28),
                  (cx + s, cy), (cx + s * 0.28, cy + s * 0.28),
                  (cx, cy + s), (cx - s * 0.28, cy + s * 0.28),
                  (cx - s, cy), (cx - s * 0.28, cy - s * 0.28)],
             color, alpha)


def flower(c, cx, cy, petal, center, s=1.0):
    """A simple five-petal flower on a short stem."""
    c.line(cx, cy + 8, cx, cy + 34, (96, 170, 110), 255, 4)
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        px = cx + 15 * s * math.cos(a)
        py = cy + 15 * s * math.sin(a)
        c.disc(px, py, 11 * s, petal, 255)
    c.disc(cx, cy, 10 * s, center, 255)


# ------------------------------------------------------------------- png ----
def write_png(path, w, h, px):
    """Minimal deterministic PNG encoder (RGB, 8-bit, Up filter, zlib-9)."""
    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data +
                struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))

    raw = bytearray()
    stride = w * 3
    prev = bytes(stride)
    for y in range(h):
        row = bytes(px[y * stride:(y + 1) * stride])
        raw.append(2)  # Up filter
        raw += bytes((a - b) & 0xff for a, b in zip(row, prev))
        prev = row
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    data = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) +
            chunk(b"IDAT", zlib.compress(bytes(raw), 9)) +
            chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(data)


# ----------------------------------------------------------------- scene ----
CREAM = (255, 248, 238)
OUTLINE = (238, 195, 154)
ORANGE = (255, 179, 122)
PINK = (255, 143, 171)
PINK_SOFT = (255, 179, 198)
DARK = (58, 42, 34)


def main():
    rng = random.Random(SEED)
    c = Canvas(W, H)

    # --- pastel sky ---
    c.vgrad(0, 420, (255, 233, 243), (255, 246, 230))
    c.vgrad(420, H, (255, 246, 230), (255, 227, 238))

    # --- soft sun (top left) ---
    c.disc(150, 130, 78, (255, 217, 61), 60)
    c.disc(150, 130, 62, (255, 217, 61), 90)
    c.disc(150, 130, 50, (255, 224, 110), 255)
    c.disc(150, 130, 34, (255, 236, 150), 255)

    # --- clouds ---
    for (cx, cy, s) in ((830, 120, 1.0), (880, 150, 0.8), (120, 320, 0.9),
                        (905, 330, 0.75), (300, 90, 0.6)):
        for (dx, dy, r) in ((-52, 6, 34), (0, -6, 44), (52, 6, 34),
                            (-24, 14, 30), (24, 14, 30)):
            c.disc(cx + dx * s, cy + dy * s, r * s, (255, 255, 255), 215)

    # --- floating hearts and paw prints ---
    for (x, y, s, a) in ((90, 480, 26, 200), (930, 480, 22, 200),
                         (180, 640, 18, 170), (860, 640, 20, 170),
                         (250, 210, 16, 160), (760, 200, 15, 160)):
        heart(c, x, y, s, PINK_SOFT, a)
    for (x, y, s, a) in ((120, 760, 26, 150), (920, 780, 24, 150),
                         (330, 130, 20, 130)):
        paw(c, x, y, s, (255, 179, 198), a)

    # --- sparkles ---
    for (x, y, s) in ((330, 330, 14), (700, 300, 12), (880, 200, 13),
                      (140, 200, 11), (620, 150, 10), (400, 640, 12),
                      (940, 560, 11), (90, 560, 10)):
        sparkle(c, x, y, s, (255, 255, 255), 230)

    # --- green hill (deeper green so the scene is grounded) ---
    c.ellipse(512, 1130, 720, 270, (140, 208, 152), 255)
    c.ellipse(512, 1135, 720, 270, (104, 184, 128), 255)

    # --- flowers and grass on the hill ---
    for (x, y, petal, s) in ((150, 965, (255, 255, 255), 1.0),
                             (300, 992, (255, 179, 198), 0.9),
                             (880, 968, (255, 255, 255), 1.0),
                             (740, 998, (255, 205, 122), 0.85),
                             (950, 992, (255, 179, 198), 0.9),
                             (60, 1000, (255, 205, 122), 0.8)):
        flower(c, x, y, petal, (255, 209, 61), s)
    for (x, y, hgt) in ((230, 985, 22), (660, 985, 20), (830, 1005, 24),
                        (420, 1010, 18), (560, 1012, 20)):
        poly_fill(c, [(x, y - hgt), (x - 8, y), (x + 8, y)],
                  (110, 185, 130), 255)

    # --- soft shadow under the kitten ---
    c.ellipse(512, 968, 235, 26, (120, 90, 110), 40)

    # --- tail (a clear curl on the right side, drawn before the body) ---
    tail_pts = [(690, 905), (745, 922), (795, 905), (820, 862),
                (815, 812), (785, 775), (745, 768)]
    # smooth the control points into a curve
    smooth = []
    for i in range(len(tail_pts) - 1):
        x0, y0 = tail_pts[i]
        x1, y1 = tail_pts[i + 1]
        for k in range(8):
            t = k / 8.0
            smooth.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    smooth.append(tail_pts[-1])
    n = len(smooth)
    # outline pass, then the fill pass, so the curl reads on the pale sky
    for i, (x, y) in enumerate(smooth):
        r = 26 - 12 * (i / max(1, n - 1))
        c.disc(x, y, r + 5, (196, 138, 92), 255)
    for i, (x, y) in enumerate(smooth):
        r = 26 - 12 * (i / max(1, n - 1))
        col = ORANGE if i >= n - 6 else (255, 242, 224)
        c.disc(x, y, r, col, 255)

    # --- body (warm fill + strong outline + soft halo so it reads on the sky) ---
    c.ellipse(522, 812, 218, 198, (210, 160, 150), 70)
    c.ellipse(512, 800, 215, 195, (196, 138, 92), 255)
    c.ellipse(512, 800, 205, 185, (255, 236, 210), 255)
    # belly patch
    c.ellipse(512, 845, 128, 108, (255, 248, 238), 255)
    # orange patches on the body
    c.ellipse(380, 700, 46, 34, ORANGE, 255)
    c.ellipse(640, 730, 38, 28, ORANGE, 255)

    # --- back feet ---
    c.ellipse(398, 952, 68, 32, (196, 138, 92), 255)
    c.ellipse(398, 952, 60, 25, (255, 232, 208), 255)
    c.ellipse(626, 952, 68, 32, (196, 138, 92), 255)
    c.ellipse(626, 952, 60, 25, (255, 232, 208), 255)
    for x in (382, 398, 414):
        c.line(x, 938, x, 958, (190, 140, 105), 220, 2)
    for x in (610, 626, 642):
        c.line(x, 938, x, 958, (190, 140, 105), 220, 2)

    # --- front paws ---
    c.ellipse(438, 905, 55, 69, (196, 138, 92), 255)
    c.ellipse(438, 905, 46, 60, (255, 232, 208), 255)
    c.ellipse(586, 905, 55, 69, (196, 138, 92), 255)
    c.ellipse(586, 905, 46, 60, (255, 232, 208), 255)

    # --- ears (shorter and wider, so they read as cat ears, not hats) ---
    for sgn in (-1, 1):
        # outer ear triangle
        tip = (512 + sgn * 150, 210)
        base_l = (512 + sgn * 95, 335)
        base_r = (512 + sgn * 225, 335)
        poly_fill(c, [tip, base_l, base_r], OUTLINE, 255)
        poly_fill(c, [(tip[0], tip[1] + 8),
                      (base_l[0] + sgn * 8, base_l[1] - 6),
                      (base_r[0] - sgn * 8, base_r[1] - 6)], CREAM, 255)
        # inner ear (pink)
        cx = 512 + sgn * 155
        poly_fill(c, [(cx, 245), (cx - sgn * 30, 305), (cx + sgn * 30, 305)],
                  PINK_SOFT, 255)
        c.disc(tip[0], tip[1] + 4, 14, CREAM, 255)

    # --- head ---
    c.disc(512, 430, 207, OUTLINE, 255)
    c.disc(512, 430, 200, CREAM, 255)
    # orange patch on the upper-left of the head (kept inside the head disc)
    c.ellipse(380, 350, 40, 30, ORANGE, 255)

    # --- eyes (big, glossy) ---
    for ex in (428, 596):
        c.ellipse(ex, 420, 44, 58, (42, 28, 21), 255)
        c.ellipse(ex, 420, 40, 54, DARK, 255)
        c.disc(ex - 14, 398, 14, (255, 255, 255), 255)
        c.disc(ex + 16, 442, 6, (255, 255, 255), 255)
        sparkle(c, ex - 14, 398, 7, (255, 255, 255), 255)

    # --- nose, mouth, blush ---
    poly_fill(c, [(492, 492), (532, 492), (512, 518)], PINK, 255)
    c.disc(512, 500, 5, (255, 255, 255), 180)
    c.line(512, 518, 492, 540, (138, 106, 90), 220, 3)
    c.line(512, 518, 532, 540, (138, 106, 90), 220, 3)
    c.ellipse(378, 516, 44, 25, PINK_SOFT, 130)
    c.ellipse(646, 516, 44, 25, PINK_SOFT, 130)

    # --- whiskers ---
    for sgn in (-1, 1):
        c.line(512 + sgn * 140, 482, 512 + sgn * 238, 462,
               (185, 155, 138), 200, 2)
        c.line(512 + sgn * 142, 506, 512 + sgn * 242, 506,
               (185, 155, 138), 200, 2)
        c.line(512 + sgn * 140, 530, 512 + sgn * 236, 552,
               (185, 155, 138), 200, 2)

    # --- pink bow on the right ear ---
    bx, by = 665, 250
    poly_fill(c, [(bx, by), (bx - 42, by - 22), (bx - 42, by + 22)],
              PINK, 255)
    poly_fill(c, [(bx, by), (bx + 42, by - 22), (bx + 42, by + 22)],
              PINK, 255)
    c.disc(bx, by, 12, (255, 107, 157), 255)

    # --- butterfly (top right; separated wings, saturated colours) ---
    bfx, bfy = 830, 250
    c.ellipse(bfx - 22, bfy - 14, 16, 22, (255, 190, 60), 255)
    c.ellipse(bfx + 22, bfy - 14, 16, 22, (255, 110, 155), 255)
    c.ellipse(bfx - 16, bfy + 15, 12, 16, (255, 110, 155), 255)
    c.ellipse(bfx + 16, bfy + 15, 12, 16, (255, 190, 60), 255)
    c.ellipse(bfx, bfy, 5, 14, DARK, 255)
    c.line(bfx - 3, bfy - 12, bfx - 12, bfy - 32, DARK, 230, 2)
    c.line(bfx + 3, bfy - 12, bfx + 12, bfy - 32, DARK, 230, 2)

    # --- ball of yarn (bottom left) ---
    c.disc(185, 930, 46, (255, 143, 171), 255)
    c.disc(185, 930, 40, (255, 168, 190), 255)
    for k in range(-2, 3):
        y0 = 930 + k * 14
        for xx in range(150, 221, 4):
            yy = y0 + 5 * math.sin((xx - 150) / 70.0 * math.pi + k)
            c.blend(xx, int(yy), 230, 90, 140, 200)
    # loose thread to the kitten's paw
    for i in range(60):
        t = i / 59.0
        x = 225 + 190 * t
        y = 945 - 40 * math.sin(t * math.pi)
        c.blend(int(x), int(y), 230, 90, 140, 220)

    out = os.environ.get("ENTRY_PATH", "/output/entry.png")
    d = os.path.dirname(out)
    if d:
        os.makedirs(d, exist_ok=True)
    write_png(out, W, H, c.px)
    print("wrote", out)


if __name__ == "__main__":
    main()
