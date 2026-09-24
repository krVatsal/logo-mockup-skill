# AI fallback

Use the installed image-generation skill only when:

- the user requests a surface absent from the catalog;
- a custom lifestyle context materially improves the requested set; or
- the user explicitly asks for a generative treatment.

Do not use it when `--no-ai` is present.

Start from the supplied logo plus, when useful, a deterministic composite. Classify the task as `product-mockup` or `compositing`. State these invariants in every prompt:

```text
Preserve the supplied logo exactly: identical spelling, geometry, proportions, colors, and orientation. Do not redraw, restyle, embellish, or invent text. Change only the requested product or scene context. No watermark.
```

Inspect the output at full size. If the mark or wording changes, do not ship it as an authoritative mockup. Retain the deterministic result, label the generated file as exploratory, and record the exact prompt in `manifest.json`.
