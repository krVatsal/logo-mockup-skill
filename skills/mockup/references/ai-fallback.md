# AI fallback

Use the installed image-generation skill only when:

- the user requests a surface absent from the catalog;
- a custom lifestyle context materially improves the requested set; or
- the user explicitly asks for a generative treatment.

Do not use it when `--no-ai` is present.

Generate the **blank canvas first**, then place the supplied logo with the deterministic renderer. Classify scene generation as `product-mockup`; classify any model-assisted insertion as `compositing`.

## Production-grade blank canvas brief

The fallback is not a shortcut for pasting artwork into a generic photograph. Generate a reusable scene with convincing material, lighting, and mounting logic. Every blank-scene prompt must specify:

- the precise substrate: woven textile, ribbed metal, concrete, stone, glass, packaging board, and so on;
- a single unobstructed branding surface with its position, scale, camera angle, and approximate aspect ratio;
- controlled commercial or architectural lighting that will support realistic contact shadows;
- enough resolution and edge detail for a 2048 px final render;
- no existing logo, letters, signage, text, symbols, watermark, or decorative mark on the branding surface;
- no feature that crosses the intended placement area unless it is meant to modulate the final artwork as texture.

Use the following prompt scaffold and adapt only the relevant fields:

```text
Use case: product-mockup
Asset type: reusable premium brand mockup canvas
Primary request: a photorealistic blank <product/environment> prepared for later logo compositing
Scene/backdrop: <specific commercial context>
Branding surface: <material>, fully blank, unobstructed, position and approximate aspect ratio
Composition/framing: <camera and crop>; preserve a clean placement area
Lighting/mood: controlled commercial lighting with realistic directional shadows and reflections
Materials/textures: physically plausible microtexture and edge construction
Constraints: no logo, letters, text, symbols, watermark, or existing signage; no blank white studio void unless the product category requires it
```

Prefer physical brand applications over generic media rectangles for identity-led technology brands: raised wall signs, fabricated facade marks, woven badges, etched or frosted glass, reception signage, device hardware, and environmental wayfinding. A billboard or screen is appropriate only when the brief specifically needs advertising or interface presentation.

After generation, inspect the blank at full size. Reject scenes with invented marks, distorted product geometry, unusable surfaces, muddy material detail, or lighting that cannot support a believable composite.

## Deterministic insertion

Use the template transform and select a material effect that matches the substrate:

- `raised-sign` for fabricated letters or symbols; include depth, cast shadow, and optional restrained halo;
- `fabric-ink` for woven labels and textile printing; retain weave and lighting variation;
- `glass-vinyl` for translucent or frosted applications; retain reflections and background visibility.

Preserve logo geometry and colors. Do not ask the image model to redraw authoritative artwork. State these invariants in any model-assisted compositing prompt:

```text
Preserve the supplied logo exactly: identical spelling, geometry, proportions, colors, and orientation. Do not redraw, restyle, embellish, or invent text. Change only the requested product or scene context. No watermark.
```

Inspect the output at full size. If the mark or wording changes, do not ship it as an authoritative mockup. Retain the deterministic result, label the generated file as exploratory, and record the exact prompt in `manifest.json`.

## Promote a successful canvas to the library

When a generated blank is broadly reusable and the user asks to keep it, add it to `assets/templates/<template-id>/` rather than leaving it in a run-specific output folder. Use `scripts/add_generated_template.py`; record the exact generation prompt and generator in `template.json`. Then run `prepare_templates.py` and `validate_templates.py`.

Do not promote a canvas containing the current client's logo or a scene whose styling is too brand-specific to work for other identities. The reusable asset must be the clean pre-composite image.
