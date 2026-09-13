#!/usr/bin/env python3
import argparse
from pathlib import Path

GLYPH_BASE = 0xA0
XSUB = 4
YSUB = 6
GLYPH_COUNT = XSUB * YSUB
GLYPH_BYTES = 64
WIDTH = 12
HEIGHT = 18

# MAX7456 two-bit pixel values used by Betaflight MCM fonts.
BLACK = 0b00
TRANSPARENT = 0b01
WHITE = 0b10

X_CENTERS = [1, 4, 7, 10]
Y_CENTERS = [1, 4, 7, 10, 13, 16]


def encode_glyph(pixels):
    # 64 bytes per glyph. First 54 bytes are 12x18 pixels, 2 bits/pixel.
    data = [0x55] * GLYPH_BYTES  # transparent (01 01 01 01)
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            row.append(pixels[y][x])
        for group in range(3):
            value = 0
            for i in range(4):
                value = (value << 2) | row[group * 4 + i]
            data[y * 3 + group] = value
    return data


def make_cursor(cx, cy):
    px = [[TRANSPARENT for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # Compact 5-pixel '+' cursor. It stays completely inside the 12x18 cell
    # for all 4x6 subpositions, avoiding clipping at cell boundaries.
    for dx, dy in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
        x, y = cx + dx, cy + dy
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            px[y][x] = WHITE
    return encode_glyph(px)


def read_mcm(path: Path):
    raw = path.read_text(encoding="ascii").splitlines()
    if not raw or raw[0].strip() != "MAX7456":
        raise SystemExit("Input is not a MAX7456 .mcm font (missing MAX7456 header).")
    lines = [ln.strip() for ln in raw[1:] if ln.strip()]
    if len(lines) < 256 * GLYPH_BYTES:
        raise SystemExit(f"Font is too short: {len(lines)} data lines; expected at least {256 * GLYPH_BYTES}.")
    for i, ln in enumerate(lines[:256 * GLYPH_BYTES]):
        if len(ln) != 8 or any(c not in "01" for c in ln):
            raise SystemExit(f"Invalid binary line at data line {i + 1}: {ln!r}")
    return lines


def main():
    ap = argparse.ArgumentParser(description="Create a MAX7456 font with 24 KISS-style stick cursor sub-cell glyphs")
    ap.add_argument("input_mcm", type=Path, help="Existing Betaflight/MAX7456 .mcm font")
    ap.add_argument("output_mcm", type=Path, help="Output .mcm font")
    args = ap.parse_args()

    lines = read_mcm(args.input_mcm)

    glyph = 0
    for sy, cy in enumerate(Y_CENTERS):
        for sx, cx in enumerate(X_CENTERS):
            data = make_cursor(cx, cy)
            slot = GLYPH_BASE + glyph
            start = slot * GLYPH_BYTES
            lines[start:start + GLYPH_BYTES] = [f"{b:08b}" for b in data]
            glyph += 1

    out = "MAX7456\n" + "\n".join(lines) + "\n"
    args.output_mcm.write_text(out, encoding="ascii")
    print(f"Wrote {args.output_mcm}")
    print(f"Replaced glyphs 0x{GLYPH_BASE:02X}-0x{GLYPH_BASE + GLYPH_COUNT - 1:02X} ({GLYPH_COUNT} glyphs).")
    print("These slots normally belong to the Betaflight logo area, so the boot/logo glyphs in that range are intentionally sacrificed.")

if __name__ == "__main__":
    main()
