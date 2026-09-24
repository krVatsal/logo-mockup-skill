# Analyze and select

## Input gate

Before rendering, confirm:

1. A logo file exists and is SVG or PNG.
2. PNG artwork has useful alpha transparency and at least 512 px on its longest visible edge.
3. Brand name and company purpose are known.

Do not treat a white rectangular background as transparency. Tell the user to supply a transparent export or SVG.

## Brand profile

Write `brand-analysis.md` with:

- Company and one-sentence purpose
- Inferred industry
- Audience
- Personality and visual register
- Colors observed in the logo
- Selected surfaces and one concise reason for each

Avoid inventing brand strategy. Use the provided brief and visible logo evidence.

## Selection

Read `assets/templates/catalog.json`. Score entries using their industry, audience, style, and role tags. Explicit `--surfaces` always wins. Otherwise select six by default.

The set should cover different roles where relevant:

- wearable or merchandise
- packaging or carry
- environmental or promotional
- stationery or customer touchpoint

Avoid choosing more than three items from one role unless the user asks for a focused collection. Use these broad patterns as guidance, not rigid mappings:

- Fashion/lifestyle: apparel, sneaker, tote, shopping bag, billboard.
- Food/beverage: cup, pouch, shopping bag, storefront, shipping box.
- Technology/services: stationery, apparel, tote, storefront, billboard.
- Consumer products: pouch, shipping box, shopping bag, billboard, apparel.

If several entries tie, prefer higher `priority` and then a more varied role mix.
