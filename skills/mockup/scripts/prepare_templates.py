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

    if "surface_rect" in meta:
        x, y, w, h = meta["surface_rect"]
        grab_mask = np.full((height, width), cv2.GC_BGD, dtype=np.uint8)
        rectangle = (round(x * width), round(y * height), round(w * width), round(h * height))
        grab_mask[rectangle[1]:rectangle[1] + rectangle[3], rectangle[0]:rectangle[0] + rectangle[2]] = cv2.GC_PR_FGD
        if "surface_core" in meta:
            cx, cy, cw, ch = meta["surface_core"]
            grab_mask[round(cy * height):round((cy + ch) * height), round(cx * width):round((cx + cw) * width)] = cv2.GC_FGD
        bg_model = np.zeros((1, 65), np.float64)
        fg_model = np.zeros((1, 65), np.float64)
        cv2.grabCut(np.asarray(base), grab_mask, None, bg_model, fg_model, 8, cv2.GC_INIT_WITH_MASK)
        subject = np.where((grab_mask == cv2.GC_FGD) | (grab_mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
        subject = cv2.morphologyEx(subject, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
        if meta.get("surface_fill_hull"):
            contours, _ = cv2.findContours(subject, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                hull = cv2.convexHull(max(contours, key=cv2.contourArea))
                subject[:] = 0
                cv2.fillConvexPoly(subject, hull, 255)
        if "surface_clip_polygon" in meta:
            clip = np.zeros_like(subject)
            points = np.array([[round(px * width), round(py * height)] for px, py in meta["surface_clip_polygon"]], np.int32)
            cv2.fillPoly(clip, [points], 255)
            subject = clip if meta.get("surface_use_clip") else cv2.bitwise_and(subject, clip)
        subject = cv2.GaussianBlur(subject, (0, 0), 1.2)
        Image.fromarray(subject, mode="L").save(template_dir / "surface-mask.png")

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
