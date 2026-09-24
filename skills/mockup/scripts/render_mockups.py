#!/usr/bin/env python3
"""Render a curated brand mockup set from one SVG or transparent PNG logo."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = SKILL_DIR / "assets" / "templates"
ROLES = ("wearable", "packaging", "carry", "environmental", "stationery", "customer-touchpoint")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--logo", required=True, type=Path)
    parser.add_argument("--brand", required=True)
    parser.add_argument("--brief", required=True)
    parser.add_argument("--surfaces", default="")
    parser.add_argument("--count", type=int, default=6)
    parser.add_argument("--style", default="")
    parser.add_argument("--format", choices=("square", "landscape", "portrait"), default="square")
    parser.add_argument("--output", type=Path, default=Path("mockup-output"))
    return parser.parse_args()


def output_path(requested: Path) -> Path:
    if not requested.exists():
        return requested
    stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    return requested.with_name(f"{requested.name}-{stamp}")


def load_logo(path: Path) -> Image.Image:
    if not path.exists():
        raise ValueError(f"Logo not found: {path}")
    suffix = path.suffix.lower()
    if suffix == ".svg":
        try:
            import resvg_py
        except ImportError as exc:
            raise ValueError("SVG input requires resvg; run with the declared uv project.") from exc
        png = resvg_py.svg_to_bytes(svg_path=str(path), width=2048)
        image = Image.open(__import__("io").BytesIO(png)).convert("RGBA")
    elif suffix == ".png":
        image = Image.open(path).convert("RGBA")
        alpha = np.asarray(image.getchannel("A"))
        if alpha.min() == 255:
            raise ValueError("PNG logo is opaque. Supply a transparent PNG or SVG.")
    else:
        raise ValueError("Logo must be an SVG or transparent PNG.")
    bbox = image.getchannel("A").getbbox()
    if not bbox:
        raise ValueError("Logo contains no visible artwork.")
    image = image.crop(bbox)
    if suffix == ".png" and max(image.size) < 512:
        raise ValueError("PNG logo is too small; supply at least 512 px on its longest visible edge.")
    return image


def templates() -> list[dict]:
    found = []
    for folder in sorted(TEMPLATES_DIR.iterdir()):
        meta_path = folder / "template.json"
        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            meta["_dir"] = folder
            found.append(meta)
    return found


def select(items: list[dict], brief: str, surfaces: str, count: int, style: str) -> list[dict]:
    count = max(1, min(count, len(items)))
    requested = [part.strip().lower() for part in surfaces.split(",") if part.strip()]
    if requested:
        by_id = {item["id"]: item for item in items}
        missing = [item for item in requested if item not in by_id]
        if missing:
            raise ValueError(f"Unknown surfaces: {', '.join(missing)}")
        return [by_id[item] for item in requested[:count]]
    words = set(re.findall(r"[a-z0-9-]+", f"{brief} {style}".lower()))
    chosen: list[dict] = []
    remaining = list(items)
    while remaining and len(chosen) < count:
        role_counts = {role: sum(x["role"] == role for x in chosen) for role in ROLES}
        def score(item: dict) -> float:
            tag_hits = len(words.intersection(item.get("tags", [])))
            diversity = 5 if role_counts.get(item["role"], 0) == 0 else -4 * role_counts[item["role"]]
            return tag_hits * 7 + item.get("priority", 0) + diversity
        winner = max(remaining, key=score)
        chosen.append(winner)
        remaining.remove(winner)
    return chosen


def logo_canvas(logo: Image.Image, quad: np.ndarray, padding: float) -> Image.Image:
    top = np.linalg.norm(quad[1] - quad[0])
    bottom = np.linalg.norm(quad[2] - quad[3])
    left = np.linalg.norm(quad[3] - quad[0])
    right = np.linalg.norm(quad[2] - quad[1])
    width = max(64, round((top + bottom) / 2))
    height = max(64, round((left + right) / 2))
    inset = max(4, round(min(width, height) * padding))
    canvas = Image.new("RGBA", (width, height))
    fitted = ImageOps.contain(logo, (width - 2 * inset, height - 2 * inset), Image.Resampling.LANCZOS)
    canvas.alpha_composite(fitted, ((width - fitted.width) // 2, (height - fitted.height) // 2))
    return canvas


def render(item: dict, logo: Image.Image, destination: Path) -> tuple[int, int]:
    folder = item["_dir"]
    base = Image.open(folder / "base.png").convert("RGBA")
    width, height = base.size
    quad = np.float32([[x * width, y * height] for x, y in item["quad"]])
    artwork = logo_canvas(logo, quad, item.get("padding", 0.1))
    src = np.float32([[0, 0], [artwork.width - 1, 0], [artwork.width - 1, artwork.height - 1], [0, artwork.height - 1]])
    transform = cv2.getPerspectiveTransform(src, quad)
    warped = cv2.warpPerspective(
        np.asarray(artwork), transform, (width, height), flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0)
    )
    mask = np.asarray(Image.open(folder / "mask.png").convert("L"), dtype=np.float32) / 255
    warped[:, :, 3] = (warped[:, :, 3].astype(np.float32) * mask).astype(np.uint8)
    shade = np.asarray(Image.open(folder / "shading.png").convert("L"), dtype=np.float32)
    strength = float(item.get("texture_strength", 0.15))
    factor = 1 + ((shade - 128) / 128) * strength
    warped[:, :, :3] = np.clip(warped[:, :, :3].astype(np.float32) * factor[:, :, None], 0, 255)
    result = Image.alpha_composite(base, Image.fromarray(warped.astype(np.uint8), "RGBA")).convert("RGB")
    if max(result.size) < 2048:
        scale = 2048 / max(result.size)
        result = result.resize(
            (round(result.width * scale), round(result.height * scale)),
            Image.Resampling.LANCZOS,
        )
    result.save(destination, quality=96)
    return result.size


def make_contact_sheet(records: list[dict], output: Path, layout: str) -> None:
    columns = {"portrait": 2, "square": 3, "landscape": 3}[layout]
    card_w, image_h, label_h = 560, 430, 64
    rows = math.ceil(len(records) / columns)
    sheet = Image.new("RGB", (columns * card_w, rows * (image_h + label_h)), "#EEEAE3")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=24)
    for index, record in enumerate(records):
        x = (index % columns) * card_w
        y = (index // columns) * (image_h + label_h)
        image = Image.open(record["absolute_path"]).convert("RGB")
        image = ImageOps.contain(image, (card_w - 28, image_h - 28), Image.Resampling.LANCZOS)
        sheet.paste(image, (x + (card_w - image.width) // 2, y + (image_h - image.height) // 2))
        draw.text((x + 20, y + image_h + 14), record["name"], fill="#191817", font=font)
    sheet.save(output, quality=92, optimize=True)


def reason(item: dict, words: set[str]) -> str:
    hits = [tag for tag in item.get("tags", []) if tag in words]
    if hits:
        return f"Matches the brand's {', '.join(hits[:2])} context and adds a {item['role']} application."
    return f"Adds a strong {item['role']} application to keep the set varied."


def main() -> int:
    args = parse_args()
    logo = load_logo(args.logo.resolve())
    all_templates = templates()
    selected = select(all_templates, args.brief, args.surfaces, args.count, args.style)
    target = output_path(args.output.resolve())
    images_dir = target / "images"
    images_dir.mkdir(parents=True)
    words = set(re.findall(r"[a-z0-9-]+", f"{args.brief} {args.style}".lower()))
    records = []
    for index, item in enumerate(selected, 1):
        name = f"{index:02d}-{item['id']}.png"
        path = images_dir / name
        dimensions = render(item, logo, path)
        records.append({
            "template": item["id"], "name": item["name"], "role": item["role"],
            "mode": "deterministic", "dimensions": list(dimensions),
            "path": str(path.relative_to(target)).replace("\\", "/"),
            "absolute_path": str(path), "reason": reason(item, words)
        })
    make_contact_sheet(records, target / "contact-sheet.jpg", args.format)
    analysis = [
        f"# Brand analysis: {args.brand}", "", f"**Company:** {args.brief}",
        f"**Style direction:** {args.style or 'Inferred from the supplied brief and logo.'}", "",
        "## Selected applications", ""
    ]
    analysis.extend(f"- **{r['name']}** - {r['reason']}" for r in records)
    (target / "brand-analysis.md").write_text("\n".join(analysis) + "\n", encoding="utf-8")
    digest = hashlib.sha256(args.logo.read_bytes()).hexdigest()
    manifest_records = [{k: v for k, v in record.items() if k != "absolute_path"} for record in records]
    manifest = {
        "version": 1, "brand": args.brand, "brief": args.brief, "style": args.style or None,
        "logo": {"source": str(args.logo.resolve()), "sha256": digest, "format": args.logo.suffix.lower()[1:]},
        "contact_sheet_format": args.format, "render_mode": "deterministic",
        "generated_at": datetime.now().astimezone().isoformat(), "outputs": manifest_records,
        "generative_outputs": []
    }
    (target / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
