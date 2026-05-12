# US Map Learner

A phone-optimized web app for learning all 50 US states. Single self-contained `index.html`, no build step, no runtime dependencies (Google Fonts come from CDN).

## Features

- Accurate state shapes from the US Census Bureau (via the `us-atlas` package, Albers projection).
- Tap a state to see its name, region, capital, population, three memorable facts, and tappable neighbor chips.
- Mark states as learned. Pre-marked: CA, NY, TX, FL.
- Quiz mode: hides labels, prompts you to find a named state. Right tap = green flash. Wrong tap = red flash. "Show me" reveals the answer.
- Pinch-to-zoom and pan on touch, mouse-wheel zoom + drag pan on desktop. Double-tap to reset view.
- Dark theme with gold accent, Playfair Display + DM Sans typography, iOS safe-area handling.

## Run locally

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

Or just open `index.html` directly in a browser.

## Deploy

This is a single static HTML file — any static host works. To deploy to Vercel:

```sh
vercel --prod
```

When asked for framework, pick "Other".

## Data

State shapes come from `us-atlas` (TopoJSON of US Census boundaries, Albers projection). The TopoJSON is decoded to inline SVG `<path>` strings keyed by USPS postal code in a small Python pipeline (`build.py`). State metadata (region, capital, population, facts, neighbors) is hand-compiled inside `build.py`. Populations are 2023 Census estimates.

## Files

- `index.html` — the entire app, self-contained.
- `build.py` — regenerates `index.html` from `index.template.html` + `paths.json` + the inline `STATE_DATA` dict.
- `convert.py` — decodes the TopoJSON arcs into SVG path strings and computes label centroids.
- `index.template.html` — markup, styles, and behavior with `__GEO_DATA__` / `__STATE_DATA__` placeholders.

## Rebuilding from scratch

```sh
npm pack us-atlas
tar -xzf us-atlas-*.tgz
python3 convert.py     # produces paths.json
python3 build.py       # produces index.html
```
