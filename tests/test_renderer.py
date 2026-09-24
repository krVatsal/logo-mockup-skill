from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "mockup" / "scripts" / "render_mockups.py"
SPEC = importlib.util.spec_from_file_location("mockup_renderer", SCRIPT)
renderer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = renderer
SPEC.loader.exec_module(renderer)


class RendererTests(unittest.TestCase):
    def test_catalog_and_diverse_selection(self):
        items = renderer.templates()
        self.assertEqual(len(items), 12)
        selected = renderer.select(items, "sustainable trail running outdoor fashion equipment", "", 6, "")
        self.assertEqual(len(selected), 6)
        self.assertGreaterEqual(len({item["role"] for item in selected}), 4)

    def test_explicit_surface_order(self):
        selected = renderer.select(renderer.templates(), "", "coffee-cup,billboard,tshirt", 3, "")
        self.assertEqual([item["id"] for item in selected], ["coffee-cup", "billboard", "tshirt"])

    def test_opaque_png_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "opaque.png"
            Image.new("RGB", (700, 700), "white").save(path)
            with self.assertRaisesRegex(ValueError, "opaque"):
                renderer.load_logo(path)

    def test_checked_in_examples_are_complete(self):
        for name in ("northstar-trail", "verdant-pantry", "after-hours-coffee"):
            output = ROOT / "examples" / name / "mockup-output"
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(len(manifest["outputs"]), 6)
            self.assertTrue((output / "contact-sheet.jpg").exists())
            for record in manifest["outputs"]:
                self.assertTrue((output / record["path"]).exists())


if __name__ == "__main__":
    unittest.main()
