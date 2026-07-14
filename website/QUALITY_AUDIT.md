# ADUC Public Website Quality Audit

- Date: 2026-07-14
- Branch target: `website/align-with-complete-aduc-core`
- Base checked: remote `main` at `3131ab30987f1f67579cc6db0d6d0f92c49b826f`
- Canonical URL used: `https://bacoul.github.io/AI-Data-Understanding-Core-ADUC/`
- Status: Working Draft, not a recognized standard

## Visual Review

| Area | Result |
|---|---|
| Grid coherence | Consistent shell width, two-column layouts, evidence ledgers, trace steps and responsive one-column collapse. |
| Typography | System fonts only; large editorial hero headings, smaller dense technical blocks, monospace only for commands and contract excerpts. |
| Contrast | Dark graphite background with mint and amber accents; text and focus states designed for WCAG 2.2 AA target. |
| Line length | Narrative sections constrained; code wraps on mobile to avoid page-level horizontal scroll. |
| Spacing | Generous section spacing on desktop, reduced but readable spacing on mobile. |
| Hero quality | Answers what ADUC is, the problem, what exists now and the next action. Includes a faithful contract-flow visual. |
| CTA hierarchy | Primary CTA to Try in 5 minutes, secondary CTA to validation, GitHub as supporting action. |
| Diagrams | Uses semantic HTML/CSS diagrams for contract flow, validation/comparison trace, status ledgers and assessment states. |
| Mobile quality | Browser-rendered at 360x800, 390x844, 768x1024, 1024x768, 1440x900 and 1920x1080. No real horizontal scroll; nav remains keyboard-accessible as normal links. |
| Repetition | Pages have distinct search intent and role: Why, Core, Validate, Compare, Trust, Evidence, Roadmap, Docs. |
| Generic components | Avoids stock images, fake testimonials, invented metrics and generic AI SaaS hero patterns. |

## Browser Render Checks

Rendered in the originating Codex environment from `http://127.0.0.1:8766/` against:

- `index.html`
- `why-aduc.html`
- `core.html`
- `validate.html`
- `compare.html`
- `architecture.html`
- `trust.html`
- `evidence.html`
- `docs.html`
- `example.html`
- `roadmap.html`
- `specification.html`

Viewport matrix:

- 360 x 800
- 390 x 844
- 768 x 1024
- 1024 x 768
- 1440 x 900
- 1920 x 1080

Result:

- 72 page/viewport combinations checked.
- H1 present on every rendered page.
- Primary navigation contained all 10 public links including GitHub.
- No visible offscreen elements detected.
- Horizontal scroll probe returned `scrollX = 0` after attempted horizontal scroll.
- Code blocks wrap on mobile rather than widening the document.

The originating browser audit reported only unrelated host telemetry warnings. The final status correction changes text only; a post-publication Vercel Preview review remains required.

## Scoring Matrix

| Dimension | Max | Score | Evidence | Limits / improvements |
|---|---:|---:|---|---|
| Positioning and comprehension | 15 | 14 | Home states canonical definition, problem, flow, available/in-progress/planned/not-proven states and non-goals. | Could improve with a future real-world case study after the formatter and adoption gates. |
| Technical accuracy | 15 | 15 | Site mirrors Core, 14 schemas, 11/15 fixtures, validator/comparator, 24 scenarios, profile evaluators, implemented semantic-profile migration and active formatter task. `tools/aduc_core.py`, schemas, specs, examples and evaluators were verified unchanged from current `main`. | Production deployment still needs post-push verification. |
| Design and visual identity | 15 | 13 | Contract-ledger visual system, dark technical palette, status colors for equivalent/unknown/contested/prohibited/review. | No professional visual-design review or brand/trademark decision yet. |
| UX and pathways | 10 | 9 | Non-technical path on home/Why; developer path reaches command, Core, validation, comparison, schema and GitHub within three clicks. | Future playground could reduce developer friction after safety gates. |
| Performance | 10 | 9 | Static HTML/CSS/JS, no remote fonts, no framework, minimal JS, no stock media. | Lighthouse was not available in this environment, so score is based on architecture and render behavior, not measured Lighthouse output. |
| Accessibility | 10 | 9 | Semantic landmarks, skip link, visible focus, keyboard-accessible nav, reduced-motion guard, responsive reflow and no color-only critical state. | No automated axe or screen-reader pass was available. |
| SEO | 8 | 8 | Unique titles/descriptions, canonical URLs, sitemap, robots, H1 discipline, Open Graph, Twitter cards, JSON-LD and descriptive internal links. | Search engine validation requires deployed URL verification. |
| AEO/GEO | 7 | 7 | Definition blocks, FAQ-like distinctions, capabilities, limits, commands, evidence and non-goals are explicit and crawlable without JS. | Future external evidence pages will strengthen answer-engine retrieval. |
| Trust and evidence | 5 | 5 | Evidence page separates implemented artifacts, future conformance classes, no external proof and no first-world claim. |
| Maintainability and tests | 5 | 5 | `website/assets/site-data.json`, `website/build_site.py`, strengthened `tools/validate_website.py`, 11 website tests and roadmap tests. |

Total: 94 / 100.

No critical dimension is below 8/10 equivalent. The site is acceptable as a durable Working Draft public reference, with the explicit caveat that Lighthouse, Vercel deployment status and external proof must be verified after publication.
