from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path
import textwrap
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"
LOG_PATH = LOG_DIR / "model_runs.log"
ASSETS = ROOT / "assets" / "screenshots"
ASSETS.mkdir(parents=True, exist_ok=True)


def cleanup_logs():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    for p in LOG_DIR.glob("*"):
        try:
            if p.is_file():
                p.unlink()
        except Exception:
            pass


def run_generate_model():
    gen = ROOT / "scripts" / "generate_model.py"
    subprocess.check_call([sys.executable, str(gen)])


def run_app_and_capture(timeout: float = 8.0) -> str:
    cmd = [sys.executable, str(ROOT / "main.py"), "--interval-seconds", "3", "--log-path", str(LOG_PATH)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    out_lines = []
    start = time.time()
    try:
        while time.time() - start < timeout:
            if proc.stdout is None:
                break
            line = proc.stdout.readline()
            if line:
                out_lines.append(line.rstrip("\n"))
            time.sleep(0.05)
    finally:
        try:
            proc.terminate()
        except Exception:
            pass
    return "\n".join(out_lines)


def render_text_image(text: str, outpath: Path, max_width: int = 1000, padding: int = 18, font_size: int = 14):
    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    probe = Image.new("RGB", (10, 10), color=(255, 255, 255))
    draw_probe = ImageDraw.Draw(probe)

    def _line_size(s: str) -> tuple[int, int]:
        bbox = draw_probe.textbbox((0, 0), s or " ", font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    lines = []
    for raw in text.splitlines():
        wrapped = textwrap.wrap(raw, width=120)
        if not wrapped:
            lines.append("")
        else:
            lines.extend(wrapped)

    max_line_w = max((_line_size(l)[0] for l in lines), default=0)
    img_w = min(max(max_line_w + padding * 2, 600), max_width)
    line_h = _line_size("Ay")[1] + 2
    img_h = padding * 2 + line_h * max(1, len(lines))

    img = Image.new("RGB", (img_w, img_h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    y = padding
    for line in lines:
        draw.text((padding, y), line, font=font, fill=(0, 0, 0))
        y += line_h

    img.save(outpath)


def main() -> None:
    # cleanup
    if (ROOT / "model.pkl").exists():
        (ROOT / "model.pkl").unlink()
    cleanup_logs()

    # regenerate model and run
    run_generate_model()
    out = run_app_and_capture(timeout=6.0)

    # save terminal text and image
    text_path = ASSETS / "terminal_run.txt"
    png_path = ASSETS / "terminal_run.png"
    text_path.write_text(out, encoding="utf-8")
    render_text_image(out, png_path)

    print("Wrote:", text_path)
    print("Wrote:", png_path)


if __name__ == "__main__":
    main()
