# Deterministic rendering

Use the bundled renderer from the project containing this skill:

```bash
uv run --project <skill-dir>/scripts python <skill-dir>/scripts/render_mockups.py \
  --logo <logo-path> --brand <brand-name> --brief <company-brief> \
  --count 6 --output <output-dir>
```

Pass `--surfaces` when the user names surfaces. `--format` controls the contact-sheet presentation; individual mockups preserve the source photography's native framing.

The renderer:

- rasterizes SVG at high resolution;
- trims transparent padding while preserving aspect ratio;
- fits the logo inside each template's safe area;
- uses a perspective transform, mask, and extracted surface lighting;
- measures logo-to-surface contrast and, when a template opts in, recolors the photographed product with a feathered subject mask while preserving its material texture;
- applies dense fold displacement on apparel before transferring highlights and weave texture;
- builds a padded, brand-color-derived artboard for environmental media instead of leaving signs as blank white panels;
- can print a coordinated editorial illustration system into selected merchandise surfaces; these treatments use layered color fields, large shapes, linework, and grain rather than swapping a light blank for a flat dark fill;
- exports numbered PNGs without changing the source logo file;
- writes the analysis, manifest, and contact sheet.

SVG input uses the self-contained `resvg` wheel. Run through the skill script's declared uv environment so no system graphics libraries are required. Do not convert the SVG through a screenshot.

## Template contract

Each folder under `assets/templates/` contains `base.png`, `preview.jpg`, `mask.png`, `shading.png`, and `template.json`.

Template coordinates are normalized `[x, y]` points in clockwise order: top-left, top-right, bottom-right, bottom-left. Masks are grayscale and match the base dimensions. Shading is a neutral grayscale texture layer; it modulates the placed artwork but does not replace its color.

Run `prepare_templates.py` after adding or changing template metadata. Run `validate_templates.py` before publishing.
