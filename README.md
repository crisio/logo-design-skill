# Logo Design Skill for Claude

![Five example runs of the logo-design skill](docs/images/hero.png)

A comprehensive **logo-design skill** that turns Claude into a disciplined identity designer — from the first
brief to production-ready SVG files and brand guidelines.

- **Principles & process** — discovery and briefs, word mapping, choosing the right mark type, concepting,
  geometric construction, optical corrections (overshoot, bone effect, irradiation…), colour, typography, lockups,
  testing, presentation, delivery, redesigns and identity systems.
- **A reference library of 1,432 real-world SVG logos**, each visually classified by mark type, technique,
  geometry, subject, typography, mood and industry — searchable from the command line and browsable in a local
  gallery. Used to study construction, map category conventions and avoid look-alikes (never to copy).
- **Dependency-free Python tools** — audit an SVG against logo principles, build concept overview sheets and test
  sheets (16 px pixel test, one-colour, reversed, squint, mirror, contexts, competitor shelf test), create client
  presentation boards with industry-specific mockups, render PNGs, and export a complete favicon / app-icon /
  web-manifest set.

**Contents:** [How it works](#how-it-works) · [Examples](#examples) · [Tests](#what-the-tests-catch) ·
[Install](#install) · [Use](#use) · [What's inside](#whats-inside) · [Library](#library-at-a-glance)

---

## How it works

```mermaid
flowchart LR
    A[Brief<br/>questions or stated assumptions] --> B[Research<br/>category conventions in the library]
    B --> C[Concepts<br/>8–12 one-liners → build 3 in SVG]
    C --> D[Test & refine<br/>audit · 16 px · one-colour · shelf test]
    D --> E{{Checkpoint<br/>show concepts, recommend, stop}}
    E -- "you pick a direction<br/>and ask for the kit" --> F[Kit<br/>colour · lockups · board · icons · guidelines]
    E -- "you want changes" --> C
```

The skill always **stops at the checkpoint**: it shows the concepts as one overview image with a recommendation and
offers the full kit. Nothing else is produced until you choose a direction — the kit is most of the work and only
makes sense for an approved idea.

---

## Examples

Five fictional briefs, five sectors, five deliberately different styles — each run end to end with the skill.
For every brand you see exactly what the skill shows at the checkpoint (greyscale concepts with true 64/32/16 px
sizes), followed by a colour preview of the recommended direction on mockups chosen for that industry.

| Brand | Sector | Style | Recommended mark |
|---|---|---|---|
| [Kiln](#kiln--specialty-coffee-roaster) | Specialty coffee | Warm, crafted, modern | Letterform + custom wordmark |
| [Maison Orvelle](#maison-orvelle--luxury-fashion-atelier) | Luxury fashion | High-contrast Didone, monogram | Monogram |
| [Tinkertrail](#tinkertrail--kids-stem-workshops) | Kids' STEM education | Playful, rounded, multi-colour | Mascot |
| [Alderpeak](#alderpeak--outdoor-gear) | Outdoor gear | Rugged, slab, earthy | Pictorial symbol |
| [Calmera](#calmera--physiotherapy-clinic) | Physiotherapy clinic | Soft, organic, calm | Pictorial symbol |

### Kiln — specialty coffee roaster
*Small-batch roaster in Istanbul: warm, crafted and modern — not rustic cliché. Must work on bags, cups and an
Instagram avatar.*

![Kiln concepts](docs/images/kiln-concepts.png)

**Recommended: Kiln K** — a K whose leg is the kiln's arched firing mouth; the arch returns as the *n* of the
wordmark. The audit caught a 60.8° diagonal in an early *N* and an off-centre symbol before anything was shown.

![Kiln in use](docs/images/kiln-board.png)

### Maison Orvelle — luxury fashion atelier
*Paris womenswear, made-to-measure and small leather goods: elegant, refined, timeless — no crowns, laurels or gold
gradients.*

![Maison Orvelle concepts](docs/images/maison-orvelle-concepts.png)

**Recommended: Pendant** — a Didone M whose vertex holds an O like a pendant at a V-neckline; it still reads at 16 px
and is solid enough to emboss on leather. The craft pass dropped a shared-foot "LL" (it read as *ORVEILE*) and avoided
an M-in-a-circle (too close to a famous transit sign).

![Maison Orvelle in use](docs/images/maison-orvelle-board.png)

### Tinkertrail — kids' STEM workshops
*Hands-on robotics and circuits workshops that tour schools: playful, curious, trustworthy — no lightbulbs, atoms,
gears or rockets.*

![Tinkertrail concepts](docs/images/tinkertrail-concepts.png)

**Recommended: Workshop Snail** — a curious snail that carries its workshop on its back, just as Tinkertrail brings
it to every school. The skill flags the honest risks too: snails can suggest "slow", and the spiral fills in at 16 px,
so a simplified favicon cut is part of the kit.

![Tinkertrail in use](docs/images/tinkertrail-board.png)

### Alderpeak — outdoor gear
*Packs, shells and base layers from the Pacific Northwest: rugged, dependable, honest — no generic mountain-and-sun.*

![Alderpeak concepts](docs/images/alderpeak-concepts.png)

**Recommended: Cairn** — three stacked stones build a summit, a peak and a trail marker in one; the tilted gaps zigzag
like a switchback. Rejected along the way: a carabiner *a* (read as "cl") and tree-ring contours (read as a target).

![Alderpeak in use](docs/images/alderpeak-board.png)

### Calmera — physiotherapy clinic
*Rehab, sports physio and pilates: calm, caring, professional — no crosses, heartbeats, spines or hands-with-hearts.*

![Calmera concepts](docs/images/calmera-concepts.png)

**Recommended: Still Heron** — a heron balancing on one leg in still water; single-leg balance is a standard rehab and
pilates exercise, and nothing else in the category looks like it. An early abstract idea was dropped after the peer
test found it too close to an existing mark, and the sage was darkened to reach 3 : 1 contrast.

![Calmera in use](docs/images/calmera-board.png)

---

## What the tests catch

Every concept goes through `svg_audit.py` and `preview_sheet.py` before the checkpoint. The test sheet puts the
options side by side at 96 and 32 px, in one colour and reversed, then walks each one down a size ladder to 16 px —
here it shows why Maison Orvelle's wordmark (B) needs a companion mark while the monogram (A) holds up:

![Test sheet](docs/images/test-sheet.png)

The audit turns craft rules into checks. The same run, two files — the recommended lockup and the emblem that was not
recommended:

```text
$ python3 scripts/svg_audit.py a-lockup.svg b-emblem.svg

=== a-lockup.svg
viewBox 0 0 905 256 · aspect 3.535 (horizontal) · colours 1 · anchors 205
· INFO [complexity] 205 anchor points (library median 75, p75 155). Check every point earns its place.
production-readiness score: 99/100

=== b-emblem.svg
viewBox 0 0 256 256 · aspect 1.0 (square) · colours 1 · anchors 374
▲ WARN [complex] 374 anchor points — more than 95% of comparable reference logos (median 53).
▲ WARN [near-miss-angle] 8 straight edge(s) are 0.3–3° off a clean angle … (expected for type set on a curve)
▲ WARN [tiny-detail] 6 sub-shape(s) smaller than 1/48 of the canvas: 4.3×3.1 at (40,77) …
production-readiness score: 76/100
```

---

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
`python3 tools/package_skill.py`) and upload it under **Settings → Capabilities → Skills**. If your upload has a size
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

Tools can also be run directly:
```bash
cd skills/logo-design
python3 scripts/search_library.py --technique negative-space --exemplary
python3 scripts/search_library.py --industry payments-fintech --summary
python3 scripts/svg_audit.py my-logo.svg
python3 scripts/concept_sheet.py a.svg b.svg c.svg --names "A" "B" "C" --recommend 1 -o concepts.png
python3 scripts/preview_sheet.py my-logo.svg --refs-industry developer-tools -o preview.html
python3 scripts/render_png.py my-logo.svg --size 512 -o my-logo.png
python3 scripts/export_variants.py my-logo.svg --mono "#0F7C80" --icon-bg "#0F7C80" --web-icons
open assets/library/gallery.html      # browse the library visually
```
Requires Python 3.8+ (standard library only). PNG/ICO export uses whatever renderer is available: `cairosvg`,
`rsvg-convert`, Inkscape, a Chromium-based browser (Chrome, Edge, Brave) or macOS Quick Look.

## What's inside

```
skills/logo-design/
├── SKILL.md                     # workflow, checkpoint, principles, red flags, tool guide
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
│   ├── concept_sheet.py         # one-image concept overview shown at the checkpoint
│   ├── search_library.py        # query the 1,432-logo library (filters, --summary, --format paths)
│   ├── svg_audit.py             # structure, colours, complexity, near-miss angles, tiny details, centring
│   ├── preview_sheet.py         # HTML test sheet (sizes, backgrounds, treatments, contexts, shelf test)
│   ├── presentation_board.py    # client presentation with six industry-specific mockups per concept
│   ├── render_png.py            # SVG → transparent PNG at exact sizes, favicon.ico
│   ├── export_variants.py       # black / white / mono / square / favicon / app-icon, PNGs, full web-icon set
│   └── build_catalog.py         # maintainers: rebuild catalog, stats and gallery
├── templates/                   # brand-guidelines template, presentation spec example
└── assets/library/              # svg/ (1,432 files), catalog.json, classifications.json, stats.json, gallery.html
```

## Library at a glance

1,432 files · ≈1,200 brands · 233 brands with both a lockup and a standalone icon · mark types: abstract 24 %,
combination 21 %, pictorial 20 %, letterform 15 %, wordmark 10 %, emblem 4 %, mascot 4 %, lettermark 3 % · median
2 colours, 75 % use ≤ 3 · gradients in 19 % · 141 flagged as exemplary teaching examples. More in
[`references/library-guide.md`](skills/logo-design/references/library-guide.md).

## License & trademarks

Skill text, scripts, templates and catalog data: [MIT](LICENSE). The logo files in `assets/library/svg/` are
trademarks of their respective owners, included for reference and education only and **not** covered by the MIT
license — see [TRADEMARKS.md](TRADEMARKS.md). The brands in the examples are fictional briefs created to demonstrate the
skill.

Contributions welcome: new classified logos (with redistribution rights), better scripts, translations, evals.
