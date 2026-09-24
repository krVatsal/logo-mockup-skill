# /mockup

Turn a logo and a short company brief into a curated set of presentation-ready brand mockups.

`/mockup` is a cross-agent skill for Codex, Claude Code, and opencode. It selects relevant surfaces, renders the supplied artwork into bundled original photography, and delivers individual images, a contact sheet, a brand analysis, and a manifest.

## Use

    /mockup --logo ./logo.svg --brand "Northstar" --brief "Sustainable trail-running equipment"

Natural language works too:

    /mockup this logo for a playful coffee brand aimed at college students

The deterministic renderer can also run directly:

    uv run --project skills/mockup/scripts python skills/mockup/scripts/render_mockups.py --logo ./logo.png --brand "Northstar" --brief "Sustainable trail-running equipment" --count 6

Transparent PNG and SVG logos are supported. SVG rendering uses a self-contained resvg wheel and does not require system graphics libraries.

## Examples

Three fictional brand examples are included with complete rendered outputs:

- Northstar Trail - outdoor and trail-running equipment
- Verdant Pantry - sustainable food and consumer packaging
- After Hours Coffee - hospitality and neighborhood retail

Each example contains its CC0 source mark, company brief, six mockups, contact sheet, analysis, and manifest.

## Install

Install into Codex, Claude Code, Cursor, or opencode with:

    npx skills add . --skill mockup

The Claude plugin metadata is available under `.claude-plugin/`.

## Repository layout

- `skills/mockup/` - canonical skill, references, renderer, and template library
- `examples/` - runnable brand briefs and checked-in output galleries
- `tests/` - selection, validation, and example completeness tests
- `.claude-plugin/` - Claude plugin and marketplace metadata

All bundled base photographs were generated specifically for this repository. The downloaded example marks are CC0 and documented in `examples/SOURCES.md`.
