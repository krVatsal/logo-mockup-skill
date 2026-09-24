#!/usr/bin/env python3
"""Validate the bundled template contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1] / "assets" / "templates"
REQUIRED = ("base.png", "preview.jpg", "mask.png", "shading.png", "template.json")


def main() -> int:
    errors: list[str] = []
    folders = [p for p in ROOT.iterdir() if p.is_dir()]
    ids: set[str] = set()
    for folder in sorted(folders):
        missing = [name for name in REQUIRED if not (folder / name).exists()]
        if missing:
            errors.append(f"{folder.name}: missing {', '.join(missing)}")
            continue
        try:
            meta = json.loads((folder / "template.json").read_text(encoding="utf-8"))
            if meta.get("id") != folder.name:
                errors.append(f"{folder.name}: id must match folder")
            if meta.get("id") in ids:
                errors.append(f"{folder.name}: duplicate id")
            ids.add(meta.get("id"))
            quad = meta.get("quad", [])
            if len(quad) != 4 or any(len(point) != 2 for point in quad):
                errors.append(f"{folder.name}: quad must contain four [x,y] points")
            if any(not 0 <= value <= 1 for point in quad for value in point):
                errors.append(f"{folder.name}: quad coordinates must be normalized")
            base_size = Image.open(folder / "base.png").size
            for resource in ("mask.png", "shading.png"):
                if Image.open(folder / resource).size != base_size:
                    errors.append(f"{folder.name}: {resource} size differs from base")
        except Exception as exc:
            errors.append(f"{folder.name}: {exc}")
    if len(folders) < 8:
        errors.append("catalog must contain at least eight templates")
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors))
        return 1
    print(f"Validated {len(folders)} templates.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
