#!/usr/bin/env python3
"""Build masks, shading maps, previews, and the aggregate catalog."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageOps

SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = SKILL_DIR / "assets" / "templates"


def pixel_quad(meta: dict, width: int, height: int) -> list[tuple[int, int]]:
    return [(round(x * width), round(y * height)) for x, y in meta["quad"]]


def prepare(template_dir: Path) -> dict:
    meta_path = template_dir / "template.json"
    base_path = template_dir / "base.png"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    base = Image.open(base_path).convert("RGB")
    width, height = base.size
    quad = pixel_quad(meta, width, height)

    mask = Image.new("L", base.size, 0)
    ImageDraw.Draw(mask).polygon(quad, fill=255)
    mask.save(template_dir / "mask.png")

    gray = cv2.cvtColor(np.asarray(base), cv2.COLOR_RGB2GRAY).astype(np.float32)
    low = cv2.GaussianBlur(gray, (0, 0), sigmaX=max(width, height) / 80)
    detail = np.clip((gray - low) * 1.8 + 128, 72, 184).astype(np.uint8)
    mask_np = np.asarray(mask)
    detail[mask_np == 0] = 128
    Image.fromarray(detail, mode="L").save(template_dir / "shading.png")

    preview = ImageOps.contain(base, (640, 640), Image.Resampling.LANCZOS)
    preview.save(template_dir / "preview.jpg", quality=88, optimize=True)
    meta["width"], meta["height"] = width, height
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return meta


def main() -> None:
    catalog = []
    for folder in sorted(TEMPLATES_DIR.iterdir()):
        if folder.is_dir() and (folder / "template.json").exists():
            catalog.append(prepare(folder))
    payload = {"version": 1, "templates": catalog}
    (TEMPLATES_DIR / "catalog.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Prepared {len(catalog)} templates.")


if __name__ == "__main__":
    main()
