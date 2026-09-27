# /mockup

Turn a logo and a short company brief into a curated set of presentation-ready brand mockups.

`/mockup` is a cross-agent skill for Codex, Claude Code, and opencode. It selects relevant surfaces, renders the supplied artwork into bundled original photography, and delivers individual images, a contact sheet, a brand analysis, and a manifest.

## Use

    /mockup --logo ./logo.png --brand "Fabs" --brief "European merchandise and lifestyle brand"

Natural language works too:

    /mockup this logo for a playful coffee brand aimed at college students

The deterministic renderer can also run directly:

    uv run --project skills/mockup/scripts python skills/mockup/scripts/render_mockups.py --logo ./logo.png --brand "Fabs" --brief "European merchandise and lifestyle brand" --count 6

Transparent PNG and SVG logos are supported. SVG rendering uses a self-contained resvg wheel and does not require system graphics libraries.

## Examples

Three complete, production-oriented examples are included:

- AI Application - dimensional technology identity across fabric, offices, facades, reception, and glass
- Razor Eater - Indo-Chinese fast-moving food packaging, storefront, campaign, and staff apparel
- Fabs - European clothing and merchandise across apparel, accessories, retail bags, and campaign media

Each example contains the supplied source mark, company brief, six mockups, contact sheet, analysis, and manifest.

## Install

Install into Codex, Claude Code, Cursor, or opencode with:

    npx skills add . --skill mockup

The Claude plugin metadata is available under `.claude-plugin/`.

## Repository layout

- `skills/mockup/` - canonical skill, references, renderer, and template library
- `examples/` - runnable brand briefs and checked-in output galleries
- `tests/` - selection, validation, and example completeness tests
- `.claude-plugin/` - Claude plugin and marketplace metadata

All bundled base photographs were generated specifically for this repository. Example artwork provenance is documented in `examples/SOURCES.md`.
