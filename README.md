# Logo Design Skill for Claude

A comprehensive **logo-design skill** that turns Claude into a disciplined identity designer — from the first
brief to production-ready SVG files and brand guidelines.

- **Principles & process** — discovery and briefs, word mapping, choosing the right mark type, concepting,
  geometric construction, optical corrections (overshoot, bone effect, irradiation…), colour, typography, lockups,
  testing, presentation, delivery, redesigns and identity systems.
- **A reference library of 1,432 real-world SVG logos**, each visually classified by mark type, technique,
  geometry, subject, typography, mood and industry — searchable from the command line and browsable in a local
  gallery. Used to study construction, map category conventions and avoid look-alikes (never to copy).
- **Dependency-free Python tools** — audit an SVG against logo principles, generate test sheets (16 px pixel test,
  one-colour, reversed, squint, mirror, favicon/app-icon/header/business-card contexts, competitor shelf test),
  build client presentation boards with industry-specific mockups, render PNGs, and export delivery variants
  including a complete favicon / app-icon / web-manifest set.


---

## What's inside

```
skills/logo-design/
├── SKILL.md                     # workflow, principles, red flags, tool guide (loaded when the skill triggers)
├── references/                  # loaded on demand
│   ├── principles.md            # the twelve principles, mnemonic model, simplicity, relevance, longevity
│   ├── discovery-brief.md       # question bank, brief template, word mapping
│   ├── mark-types.md            # wordmark → combination: pros, cons, decision guide
│   ├── visual-techniques.md     # geometry, grids, balance, optical corrections, negative space, gradients…
│   ├── color.md · typography.md · process.md · svg-construction.md
│   ├── testing-checklist.md · presentation-delivery.md · identity-system.md
│   ├── redesign.md · critique.md
│   └── library-guide.md         # library contents, data insights, curated examples by technique
├── scripts/
│   ├── concept_sheet.py         # one-image concept overview shown before any kit is built
│   ├── search_library.py        # query the 1,432-logo library (filters, --summary, --format paths)
│   ├── svg_audit.py             # structure, colours, complexity, near-miss angles, tiny details, centring
│   ├── preview_sheet.py         # HTML test sheet (sizes, backgrounds, treatments, contexts, shelf test)
│   ├── presentation_board.py    # client presentation with rationale and six industry-specific mockups per concept
│   ├── render_png.py            # SVG → transparent PNG at exact sizes, favicon.ico (cairosvg/rsvg/Inkscape/Chrome/Quick Look)
│   ├── export_variants.py       # black / white / mono / square / favicon / app-icon, PNGs, full web-icon set
│   └── build_catalog.py         # maintainers: rebuild catalog, stats and gallery
├── templates/                   # brand-guidelines template, presentation spec example
└── assets/library/              # svg/ (1,432 files), catalog.json, classifications.json, stats.json, gallery.html
```

## Install

### Claude Code — plugin marketplace (recommended)
```
/plugin marketplace add kaankiziltug/logo-design-skill
/plugin install logo-design@logo-design-skill
```

### Claude Code — manual
Copy the skill folder into your personal (all projects) or project skills directory:
```bash
git clone https://github.com/kaankiziltug/logo-design-skill.git
cp -r logo-design-skill/skills/logo-design ~/.claude/skills/logo-design          # personal
# or: cp -r logo-design-skill/skills/logo-design .claude/skills/logo-design     # per project
```

### Claude.ai / Claude Desktop
Download `logo-design.zip` from the [Releases](https://github.com/kaankiziltug/logo-design-skill/releases) page (or run
`python tools/package_skill.py`) and upload it under **Settings → Capabilities → Skills**. If your upload has a size
limit, use `logo-design-lite.zip` (everything except the SVG files themselves).

### Other agents
The skill follows the open Agent Skills format (a folder with `SKILL.md`), so any agent that supports skills can load
`skills/logo-design/`.

## Use

Just ask — the skill triggers on logo, wordmark, monogram, brand mark, app icon, favicon, rebrand and critique requests:

> *"Design a logo for **Harbor**, a savings app for first-time savers. It should feel calm and safe."*
> *"Here's our current logo (logo.svg) — critique it and suggest a refresh."*
> *"Give me three wordmark directions for a specialty coffee roaster called Kiln."*
> *"Turn this symbol into favicon, app icon and one-colour versions, plus a one-page usage guide."*

Typical flow: brief → category research in the library → 8–12 one-sentence concepts → three built as SVG (black
first) → audit + visual test sheet → refinement → **the skill shows you the concepts as one overview image and stops**
→ you pick a direction → on request, it builds the full kit: colour, lockups, presentation board, favicon/app-icon
set, variants and a usage guide.

Tools can also be run directly:
```bash
cd skills/logo-design
python3 scripts/search_library.py --technique negative-space --exemplary
python3 scripts/search_library.py --industry payments-fintech --summary
python3 scripts/svg_audit.py my-logo.svg
python3 scripts/preview_sheet.py my-logo.svg --refs-industry developer-tools -o preview.html
python3 scripts/render_png.py my-logo.svg --size 512 -o my-logo.png
python3 scripts/export_variants.py my-logo.svg --mono "#0F7C80" --icon-bg "#0F7C80" --web-icons
open assets/library/gallery.html      # browse the library visually
```
Requires Python 3.8+ (standard library only). PNG/ICO export uses whatever renderer is available: `cairosvg`, `rsvg-convert`, Inkscape, a Chromium-based browser (Chrome, Edge, Brave) or macOS Quick Look.

## Library at a glance

1,432 files · ≈1,200 brands · 233 brands with both a lockup and a standalone icon · mark types: abstract 24 %,
combination 21 %, pictorial 20 %, letterform 15 %, wordmark 10 %, emblem 4 %, mascot 4 %, lettermark 3 % · median
2 colours, 75 % use ≤ 3 · gradients in 19 % · 141 flagged as exemplary teaching examples. More in
[`references/library-guide.md`](skills/logo-design/references/library-guide.md).

## License & trademarks

Skill text, scripts, templates and catalog data: [MIT](LICENSE). The logo files in `assets/library/svg/` are
trademarks of their respective owners, included for reference and education only and **not** covered by the MIT
license — see [TRADEMARKS.md](TRADEMARKS.md).

Contributions welcome: new classified logos (with redistribution rights), better scripts, translations, evals.
