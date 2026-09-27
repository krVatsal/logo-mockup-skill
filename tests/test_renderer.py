from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "mockup" / "scripts" / "render_mockups.py"
SPEC = importlib.util.spec_from_file_location("mockup_renderer", SCRIPT)
renderer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = renderer
SPEC.loader.exec_module(renderer)


class RendererTests(unittest.TestCase):
    def test_catalog_and_diverse_selection(self):
        items = renderer.templates()
        self.assertEqual(len(items), 18)
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

    def test_contrasting_surface_meets_accessible_ratio(self):
        for color in (np.array([237, 230, 214]), np.array([22, 24, 28]), np.array([210, 40, 80])):
            surface = renderer.contrasting_surface(color)
            self.assertGreaterEqual(renderer.contrast_ratio(color, surface), 3.0)

    def test_billboard_uses_padded_brand_artboard(self):
        billboard = next(item for item in renderer.templates() if item["id"] == "billboard")
        self.assertTrue(billboard["artboard"])
        self.assertGreaterEqual(billboard["padding"], 0.2)

    def test_brand_field_is_an_illustration_not_a_flat_fill(self):
        field = np.asarray(renderer.brand_field((800, 500), np.array([237, 230, 214])))[:, :, :3]
        self.assertGreater(float(field.std(axis=(0, 1)).max()), 20)
        tote = next(item for item in renderer.templates() if item["id"] == "tote")
        self.assertTrue(tote["surface_design"])

    def test_apparel_uses_dense_displacement(self):
        tshirt = next(item for item in renderer.templates() if item["id"] == "tshirt")
        self.assertGreater(tshirt["displacement_strength"], 0)
        self.assertLessEqual(tshirt["displacement_strength"], 6)
        self.assertTrue(tshirt["adaptive_surface"])

    def test_cap_uses_patch_instead_of_partial_surface_recolor(self):
        cap = next(item for item in renderer.templates() if item["id"] == "cap")
        self.assertFalse(cap["adaptive_surface"])
        self.assertEqual(cap["logo_backing"], "woven-patch")

    def test_checked_in_examples_are_complete(self):
        for name in ("ai-application", "razor-eater", "fabs-clothing"):
            output = ROOT / "examples" / name / "mockup-output"
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(len(manifest["outputs"]), 6)
            self.assertTrue((output / "contact-sheet.jpg").exists())
            for record in manifest["outputs"]:
                self.assertTrue((output / record["path"]).exists())


if __name__ == "__main__":
    unittest.main()
