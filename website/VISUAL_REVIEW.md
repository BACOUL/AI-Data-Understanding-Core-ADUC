# ADUC Website V2 — Visual Review Evidence

Status: **provisional review evidence; maintainer approval of the Vercel Preview is still required before merge.**

## Matrix executed

Twelve public pages were rendered at six target viewports:

- 360 × 800
- 390 × 844
- 768 × 1024
- 1024 × 768
- 1440 × 900
- 1920 × 1080

This produced **72 viewport checks**. Automated layout assertions reported **0 failures**.

The checks measured:

- document width against viewport width;
- initial mobile navigation state;
- mobile and desktop header height;
- mobile menu button visibility;
- one H1 per page;
- mobile H1 size ceiling;
- target breakpoint behavior.

Machine-readable results: [`visual-review/visual-review-report.json`](visual-review/visual-review-report.json).

## Contact sheets

Each contact sheet contains the initial viewport of all twelve principal pages:

- [`360 × 800`](visual-review/contact-360.jpg)
- [`390 × 844`](visual-review/contact-390.jpg)
- [`768 × 1024`](visual-review/contact-768.jpg)
- [`1024 × 768`](visual-review/contact-1024.jpg)
- [`1440 × 900`](visual-review/contact-1440.jpg)
- [`1920 × 1080`](visual-review/contact-1920.jpg)

The accessible mobile menu open state is captured separately:

- [`390 × 844 menu open`](visual-review/menu-390-open.png)

## Manual review observations

### Grid and hierarchy

- Home uses a two-part editorial hero on desktop and a single-column sequence on mobile.
- Page heroes share a consistent grid but use page-specific explanatory instruments.
- Long technical pages use rails, timelines and responsibility boundaries rather than repeated generic cards.

### Mobile navigation

- Initial header height is 69 px at 360/390 px.
- Navigation is closed by default when JavaScript is available.
- The toggle updates `aria-expanded`, moves focus into the menu, closes on Escape or outside pointer input, and returns focus to the toggle.
- Essential links remain present in the HTML if JavaScript fails.

### Typography and line length

- Mobile H1 sizing is capped below 59 px and does not use the previous `14vw` rule.
- Body copy remains within readable line lengths.
- Technical labels use monospace only where their function benefits from it.

### Diagrams

- The home diagram explicitly separates original data, the ADUC contract, deterministic checks and multiple consumers.
- State treatments include text labels and border/pattern differences; meaning is not carried by color alone.
- The Core, comparison, architecture, trust and evidence pages each use a distinct informational diagram.

### Responsive behavior

- No tested page produced document-level horizontal overflow.
- Code blocks retain local horizontal scrolling rather than forcing the page wider.
- Tables were replaced by responsive narrative rows where a table would reduce mobile comprehension.

## Remaining human gates

Before merge:

1. inspect the final Vercel Preview on a real Android phone and desktop browser;
2. verify 200% zoom and screen-reader navigation independently;
3. record measured Lighthouse production scores;
4. confirm that the visual direction represents the intended public identity of ADUC.
