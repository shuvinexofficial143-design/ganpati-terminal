import base64, io, os, sys, time, shutil

IMAGE_B64 = """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"""
MASK_B64 = """iVBORw0KGgoAAAANSUhEUgAAASwAAAGQAQAAAAA8DmDWAAADz0lEQVR42u1au3LTQBS9u9qJtvBgFSlSZIg+gZKCmXiomOEn4A9IR+et+Yr8Bp0YChr+AUEoUopOAVlLYcfWYx/H9jpOZvY2ia2js/e9uisTRYkSJUqUKFGiRIkSJUqUKCFF9j9yC+wUg+UYjDDYa+z2FmJj2KKcQpogMJhkECwLqhsIy1G2MqhuAdlOCujmRGtQN4WxVeFMEBis2ZHNLBd64BGrCV8AWD5MJStbBuimta79bAnm3jZoyXAiqoPWggzKJjAYf/hWA8Emo4BZ2RoM9kDBOsfYuKMOOrD31gbd2/T0ulfNdYCO9A65IdVlp0wddZpZtuYBTGK6CQT2kZICi+nSrVctEdGJz2+ffGxnRERMGMzdOgqFy1Ru/XCjjFfKAcG5maDCtJxq3S7zbiUVZukEgyWVBcaUJHru1W0gpYmtPkZ/k0duqgeFfcCiUGNsAoKlnk66j6WltfVziC3DKitn3UI/beyJfbVhWzDHstw+Dd1/XfRbPDMHK9FaA5YK2L0Im8TYMiLWhWk7VHHsod6/aP4oCrDYh202dMhewSKi9oCWzvZhU0cKVoPBbv0whi3KiejaDxNEWqGWDoawcXNItW6O4V4ejq0JqtsCZmux7G2QCf76zWcgWJQOe8YceUZyzuzc18P9MGHeqLS5DvqTPrt5ZtjVgKfBjqnOKJyNl58aNnHNR2wvTKWsRmzGHetOQvmWllhaZhhM7lanzD1oe9iqoM0BdEjxhB62ObI7ECWN8zK3nn6F1+1uCBP7LFoPYfLxBEtiMIHB+I66mQeeda8J45AZBsuDLrpj46rcYQijGz9ovmVPb/y/T7infoKxPSx/xLrNMJgKuSiDJhrblrW+vt2iIqjfZFC2bE+2EoNd9GC5h477EuSsGwz7ycry2Zf7Is/ASXwW9BAm28Bc4AnGtrE0LaCxfVr5IBzJDyjfFAabYbCctjverLw7NGCpwBblB+iWBQRLcuTtCBcZxCax0NfkOIZeP9VzMr0CN1g6oVd+GEtrWXuOOpaH83WYKGwT0+YY+6kIxcbC6qaIWOoPguaQ35givmCgbizzNxtORH9Y4vbe15WlrXs8fbtpFGx8otNc3v/TuWU+ht1/1/Rfsw6kIegcqaap1t/nvTWNMGLFLO2/k09GsNVlrSDYy37k+ph2Dp3m/bXkG0fT8tY4qw8k0d96+ltOGttBZ1LWtrem+qd1lerCYqmymmq2b0FEWtq2gst1NJ0/rvjR2UMdsF9rD946f/+W2zKyX1K/l39+lp7qXVqgfIV70V6u3u5HiRIlSjj5Dxvb7rDfRcsSAAAAAElFTkSuQmCC"""

try:
    from PIL import Image
except ImportError:
    print("Pillow missing. Run: pip install pillow")
    raise SystemExit(1)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if os.name == "nt":
    os.system("chcp 65001 > nul")

DOT = "⣿"  # dense 8-dot Braille cell: much clearer than a single round dot
RESET = "\x1b[0m"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def load_image():
    img = Image.open(io.BytesIO(base64.b64decode(IMAGE_B64))).convert("RGB")
    mask = Image.open(io.BytesIO(base64.b64decode(MASK_B64))).convert("L")
    return img, mask

def fit_for_terminal(img):
    cols = shutil.get_terminal_size((110, 40)).columns
    width = max(50, min(100, cols - 2))
    # terminal cells are taller than wide, so compensate vertically
    ratio = img.height / img.width
    height = max(1, int(width * ratio * 0.48))
    return img.resize((width, height), Image.Resampling.LANCZOS)

def pixel_dot(r, g, b):
    return f"\x1b[38;2;{r};{g};{b}m{DOT}{RESET}"

def render_slow(img, mask, delay=0.022):
    px = img.load()
    mx = mask.load()
    w, h = img.size
    clear()
    print("\n")
    for y in range(h):
        row = []
        for x in range(w):
            if mx[x, y] < 128:
                row.append(" ")
                continue
            r, g, b = px[x, y]
            row.append(pixel_dot(r, g, b))
        print("".join(row) + RESET, flush=True)
        time.sleep(delay)
    time.sleep(0.35)
    print("\n\x1b[38;2;255;190;40mॐ गं गणपतये नमः\x1b[0m")
    print("\x1b[38;2;255;110;40mगणपति बप्पा मोरया 🙏\x1b[0m")

def main():
    delay = 0.022
    if len(sys.argv) > 1:
        try:
            delay = max(0.0, float(sys.argv[1]))
        except ValueError:
            pass
    img, mask = load_image()
    img, mask = fit_for_terminal(img, mask)
    render_slow(img, mask, delay)

if __name__ == "__main__":
    main()
