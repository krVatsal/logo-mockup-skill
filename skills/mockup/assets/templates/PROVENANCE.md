# Template asset provenance

All base photographs in this directory were generated specifically for `/mockup` with OpenAI's built-in image-generation tool on 2026-09-24. They were prompted as unbranded, logo-free product or environmental photography and are bundled as editable mockup source material.

Each `template.json` records its asset role, surface geometry, and selection tags. Derived masks, shading maps, and previews are produced locally by `scripts/prepare_templates.py`.

AI-generated blank canvases additionally record `source.kind`, the generator, and the exact prompt in their template metadata. Only reviewed pre-composite blanks are stored; client logos and branded final renders are not library assets.
