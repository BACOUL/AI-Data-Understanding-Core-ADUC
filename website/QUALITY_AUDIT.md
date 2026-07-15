# ADUC Public Website V2 — Quality Audit

Audit date: 2026-07-15  
Branch: `website/international-standard-redesign-v2`  
Base: `2f069b5c3f9c1b8e1159e02eb46f00a25ea7d094`  
Status: **draft-quality candidate, not authorized for merge**

## Score

| Dimension | Maximum | Score | Evidence and limits |
|---|---:|---:|---|
| Positioning and comprehension | 15 | 15 | Hero answers what ADUC is, the problem, current availability and the next action. The four-step promise and concrete comparison states appear on Home. |
| Technical accuracy | 15 | 14 | Uses the ten-block Core, current schema/fixture/scenario counts, real CLI commands and current formatter task. External interoperability remains explicitly unproven. Final repository CI is still required. |
| Design and visual identity | 15 | 13 | New contract-layer visual language, custom mark, protocol rails, evidence trails and state vocabulary. No stock imagery or generic gradient-card layout. Final maintainer taste approval remains open. |
| UX and user journeys | 10 | 9 | Non-technical story is visible within the first minute; developer commands are reachable in two clicks. Mobile menu and CTA hierarchy are corrected. Real-device review remains open. |
| Performance | 10 | 9 | Static HTML/CSS, no framework, no external font, minimal JavaScript and no image dependency above the fold. Production Lighthouse measurement remains open. |
| Accessibility | 10 | 9 | Semantic landmarks, skip link, visible focus, 46–50 px controls, reduced motion, keyboard menu behavior, text state labels and no document overflow in 72 checks. Independent screen-reader/axe review remains open. |
| SEO | 8 | 8 | Unique titles/descriptions, canonical URLs, sitemap, robots, one H1, internal links, Open Graph, Twitter metadata and factual JSON-LD. |
| AEO/GEO | 7 | 6 | Explicit definition, capabilities, limits, comparisons, commands, evidence and FAQ distinctions. No ranking or citation promise. External retrieval testing remains open. |
| Trust and evidence | 5 | 5 | Available/in-progress/planned/not-proven states are separated; schemas, fixtures, scenarios, CI and unsupported claims are linked or stated. |
| Maintainability and tests | 5 | 5 | Shared dependency-free generator, centralized site data, readable unminified CSS, focused navigation tests and machine-readable visual report. |
| **Total** | **100** | **93** | Provisional until Preview, CI and production Lighthouse checks are complete. |

No critical dimension is below 8/10. The site must still remain in draft because the final manual Preview gate has not been completed.

## Automated evidence

- Website alignment tests: 11 passed locally.
- Website validator: passed locally against the current generated pages and official Core shape expectations.
- Responsive matrix: 72 checks, 0 failures.
- Horizontal page overflow: 0 failures across all tested pages/viewports.
- Mobile navigation: closed initial state, focus transfer, Escape close and focus return verified.
- Generator: Python syntax compilation passed.

## Page-by-page review

### Home

- Short product promise and exact canonical definition.
- Informative source → contract → checks → consumers diagram.
- Implemented evidence, ten-block map, real Core syntax, comparison states and honest status lanes.

### Why ADUC

- Leads with the difference between readability and understanding.
- Explains syntax limits, prompt limits, proprietary lock-in and the shift to a portable contract.
- Includes hydrometry, unit conversion and policy examples plus standards composition.

### Core

- Shows required versus optional responsibilities.
- Gives each block a role, example and non-goal boundary.

### Validate

- Real command, explicit pipeline, stable report excerpt and validation limits.

### Compare

- Visually separates `changeType` from `assessment`.
- Includes every normative assessment and conservative evidence rules.

### Architecture

- Separates resource, Core, schema, deterministic tools, migration and future tooling.

### Trust

- Centers unknown-safe behavior, provider neutrality, human review, local operation and authority boundaries.

### Evidence

- Connects claims to schema, fixture, scenario and CI evidence.
- States that external two-consumer proof and first-world claims are not established.

### Roadmap

- Shows Core/schema/migration as complete, formatter as active and compiler/review UI as blocked or planned.

### Docs

- Provides clone, install, validation, comparison, test and website-validation commands.

### Example and specification

- Use real Core vocabulary and link to authoritative repository artifacts.

## Release blockers

- Final Vercel Preview manual approval.
- Measured Lighthouse mobile scores on the deployed Preview/production environment.
- Optional independent axe and screen-reader review.
- No merge until the maintainer explicitly approves the visual result.
