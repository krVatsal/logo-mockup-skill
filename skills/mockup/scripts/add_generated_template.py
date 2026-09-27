#!/usr/bin/env python3
"""Promote a reviewed blank generated canvas into the bundled template catalog."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

from PIL import Image

from prepare_templates import main as rebuild_catalog


TEMPLATES = Path(__file__).resolve().parents[1] / "assets" / "templates"
EFFECTS = ("raised-sign", "fabric-ink", "glass-vinyl", "none")


def parse_quad(value: str) -> list[list[float]]:
    try:
        points = [[float(number) for number in pair.split(",")] for pair in value.split(";")]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("quad must be x,y;x,y;x,y;x,y") from exc
    if len(points) != 4 or any(len(point) != 2 for point in points):
        raise argparse.ArgumentTypeError("quad must contain four x,y points")
    if any(not 0 <= number <= 1 for point in points for number in point):
        raise argparse.ArgumentTypeError("quad values must be normalized from 0 to 1")
    return points


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, type=Path)
    parser.add_argument("--id", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--tags", required=True, help="Comma-separated selection tags")
    parser.add_argument("--quad", required=True, type=parse_quad)
    parser.add_argument("--material-effect", choices=EFFECTS, default="none")
    parser.add_argument("--material-depth", type=int, default=9)
    parser.add_argument("--material-glow", action="store_true")
    parser.add_argument("--padding", type=float, default=0.1)
    parser.add_argument("--texture-strength", type=float, default=0.12)
    parser.add_argument("--priority", type=int, default=10)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--generator", default="built-in image generation")
    return parser.parse_args()


def main() -> int:
    options = args()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", options.id):
        raise ValueError("id must use lowercase kebab-case")
    if not options.base.is_file():
        raise ValueError(f"base image not found: {options.base}")
    with Image.open(options.base) as image:
        image.verify()
    destination = TEMPLATES / options.id
    if destination.exists():
        raise ValueError(f"template already exists: {destination}")
    destination.mkdir(parents=True)
    shutil.copy2(options.base, destination / "base.png")
    with Image.open(destination / "base.png") as image:
        width, height = image.size
    metadata = {
        "id": options.id,
        "name": options.name,
        "role": options.role,
        "priority": options.priority,
        "tags": [tag.strip().lower() for tag in options.tags.split(",") if tag.strip()],
        "quad": options.quad,
        "padding": options.padding,
        "texture_strength": options.texture_strength,
        "width": width,
        "height": height,
        "source": {"kind": "ai-generated-blank", "generator": options.generator, "prompt": options.prompt},
    }
    if options.material_effect != "none":
        metadata["material_effect"] = options.material_effect
    if options.material_effect == "raised-sign":
        metadata["material_depth"] = max(2, options.material_depth)
        metadata["material_glow"] = options.material_glow
    (destination / "template.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    rebuild_catalog()
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
