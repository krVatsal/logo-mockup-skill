---
name: mockup
description: Create curated brand mockups from a supplied logo and company brief. Use for logo mockups, merchandise previews, packaging applications, billboards, storefronts, and brand presentation imagery. Do not use for UI wireframes or redesigning the logo itself.
---

# /mockup

Turn one logo and a concise company brief into a relevant, presentation-ready mockup set.

## Invocation

Accept natural language or these options:

```text
/mockup --logo ./logo.svg --brand "Acme" --brief "Premium sustainable running company"
/mockup --logo ./logo.png --surfaces tshirt,sneaker,billboard --count 3
/mockup this logo for an irreverent neighborhood coffee brand
```

Options: `--logo`, `--brand`, `--brief`, `--surfaces`, `--count` (default 6), `--style`, `--format` (`square`, `landscape`, `portrait`), `--no-ai`, and `--output`.

Require one SVG or transparent PNG logo, the company name, and a useful description of the business. Infer the industry, audience, tone, and likely applications. Ask only when the logo path, brand identity, or company purpose cannot be determined.

## Workflow

1. Read [references/analyze-and-select.md](references/analyze-and-select.md). Validate the input and choose a varied, relevant set from `assets/templates/catalog.json`.
2. Create the output directory. Use `mockup-output/` unless it exists; then use `mockup-output-YYYY-MM-DD-HHmmss/`. Never overwrite a prior run.
3. Run the deterministic renderer described in [references/render.md](references/render.md). This is the authoritative default and preserves the supplied artwork.
4. If no bundled surface can satisfy an important request and AI is allowed, read [references/ai-fallback.md](references/ai-fallback.md). Keep generated work additive and label it clearly.
5. Read [references/quality-and-delivery.md](references/quality-and-delivery.md). Inspect every result and deliver individual images, `contact-sheet.jpg`, `brand-analysis.md`, and `manifest.json`.

## Non-negotiables

- Never redraw, retype, stretch, or silently recolor the logo.
- Do not paste a flat rectangle onto a product. Use the template transform, mask, and surface shading.
- Prefer six varied, brand-relevant applications over a generic fixed pack.
- Never replace deterministic outputs with generative alternatives.
- Record every generative prompt and label those images `generative` in the manifest.
- Reject an opaque or unusably small PNG with a precise correction instead of guessing at background removal.
- Keep all final, project-bound files in the user's workspace.
