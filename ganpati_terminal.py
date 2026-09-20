import base64
import os
import shutil
import sys
import time
import zlib
from pathlib import Path

SOURCE_WIDTH = 120
SOURCE_HEIGHT = 160
DOT = "●"
RESET = "\x1b[0m"
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def enable_ansi():
    if os.name != "nt":
        return
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_uint32()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
    except Exception:
        os.system("")


def load_image():
    parts = []
    for path in sorted(DATA_DIR.glob("part*.txt")):
        parts.append(path.read_text(encoding="ascii").strip())
    if not parts:
        raise RuntimeError("Ganpati image data files are missing.")

    blob = zlib.decompress(base64.b64decode("".join(parts)))
    palette = blob[:768]
    pixels = blob[768:]
    if len(pixels) != SOURCE_WIDTH * SOURCE_HEIGHT:
        raise RuntimeError("Ganpati image data is damaged.")
    return palette, pixels


def terminal_dimensions():
    size = shutil.get_terminal_size((90, 45))
    return max(30, size.columns), max(18, size.lines)


def fit_size(cols, rows):
    max_w = min(SOURCE_WIDTH, max(28, cols - 4))
    max_h = max(12, rows - 6)
    # Terminal cells are roughly twice as tall as they are wide.
    visual_ratio = (SOURCE_HEIGHT / SOURCE_WIDTH) * 0.50
    out_w = max_w
    out_h = max(1, int(out_w * visual_ratio))
    if out_h > max_h:
        out_h = max_h
        out_w = max(1, int(out_h / visual_ratio))
    return max(24, min(out_w, max_w)), max(12, min(out_h, max_h))


def colour_for(palette, index):
    i = index * 3
    return palette[i], palette[i + 1], palette[i + 2]


def make_row(palette, pixels, y_out, out_w, out_h):
    src_y = min(SOURCE_HEIGHT - 1, int(y_out * SOURCE_HEIGHT / out_h))
    parts = []
    last = None
    for x_out in range(out_w):
        src_x = min(SOURCE_WIDTH - 1, int(x_out * SOURCE_WIDTH / out_w))
        index = pixels[src_y * SOURCE_WIDTH + src_x]
        rgb = colour_for(palette, index)
        if rgb != last:
            parts.append(f"\x1b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m")
            last = rgb
        parts.append(DOT)
    parts.append(RESET)
    return "".join(parts)


def centered_col(cols, width):
    return max(1, (cols - width) // 2 + 1)


def render(row_delay=0.07):
    enable_ansi()
    palette, pixels = load_image()
    cols, rows = terminal_dimensions()
    out_w, out_h = fit_size(cols, rows)
    left = centered_col(cols, out_w)
    top = 2

    sys.stdout.write("\x1b[2J\x1b[H\x1b[?25l")
    sys.stdout.flush()

    try:
        for y in range(out_h):
            row = make_row(palette, pixels, y, out_w, out_h)
            sys.stdout.write(f"\x1b[{top + y};{left}H{row}")
            sys.stdout.flush()
            time.sleep(row_delay)

        message1 = "ॐ गं गणपतये नमः"
        message2 = "गणपति बप्पा मोरया"
        line = top + out_h + 1
        col1 = centered_col(cols, len(message1))
        col2 = centered_col(cols, len(message2))
        sys.stdout.write(f"\x1b[{line};{col1}H\x1b[1;33m{message1}{RESET}")
        sys.stdout.flush()
        time.sleep(0.7)
        sys.stdout.write(f"\x1b[{line + 1};{col2}H\x1b[1;35m{message2}{RESET}")
        sys.stdout.write(f"\x1b[{line + 3};1H")
    finally:
        sys.stdout.write(RESET + "\x1b[?25h")
        sys.stdout.flush()


def main():
    delay = 0.07
    if "--faster" in sys.argv:
        delay = 0.025
    elif "--slow" in sys.argv:
        delay = 0.12
    render(delay)


if __name__ == "__main__":
    main()
