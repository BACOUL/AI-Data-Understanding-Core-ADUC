#!/usr/bin/env python3
"""Generate the static ADUC public website.

The generator is intentionally dependency-free. Every public page is rendered from
shared navigation, metadata, status, and design primitives so repeated product
facts cannot silently diverge.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = "https://bacoul.github.io/AI-Data-Understanding-Core-ADUC/"
UPDATED = "2026-07-15"
REPO = "https://github.com/BACOUL/AI-Data-Understanding-Core-ADUC"

NAV = [
    ("index.html", "Home"),
    ("why-aduc.html", "Why ADUC"),
    ("core.html", "Core"),
    ("validate.html", "Validate"),
    ("compare.html", "Compare"),
    ("trust.html", "Trust"),
    ("evidence.html", "Evidence"),
    ("roadmap.html", "Roadmap"),
    ("docs.html", "Docs"),
]

SITE_DATA = {
    "project": "AI Data Understanding Core",
    "shortName": "ADUC",
    "status": "Working Draft",
    "coreVersion": "0.1.0-alpha.0",
    "lastUpdated": UPDATED,
    "canonicalBase": BASE,
    "activeTask": "deterministic complete-Core contract formatter",
    "availableNow": {
        "coreBlocks": 10,
        "schemaFiles": 14,
        "validCoreFixtures": 11,
        "invalidCoreFixtures": 15,
        "comparisonScenarios": 24,
        "validator": True,
        "comparator": True,
        "profileEvaluators": 9,
        "semanticProfileMigration": True,
    },
    "inProgress": ["deterministic complete-Core contract formatter"],
    "planned": [
        "JSON/CSV compiler",
        "graphical review interface",
        "stabilized public packages",
        "production registry",
        "MCP adapter",
        "official extensions",
        "external two-consumer proof",
    ],
}

CANONICAL_DEFINITION = (
    "ADUC is a machine-readable contract that makes a data resource's structure, "
    "meaning, context, identity, provenance, uncertainty, relations and use "
    "conditions explicit, validatable and portable across AI systems."
)

CORE_BLOCKS = [
    ("aduc", "Contract identity", "required", "Version, publisher, status and declared profiles."),
    ("resource", "Original resource", "required", "Kind, media type, digest, version and locator."),
    ("structure", "Addressable shape", "required", "Records, fields, types and source paths."),
    ("semantics", "Declared meaning", "optional", "Concept IRIs, units, mappings and qualifications."),
    ("identity", "Entity decisions", "optional", "Identifiers, entities and evidence-backed equivalence."),
    ("context", "Interpretation frame", "optional", "Temporal, spatial and operational conditions."),
    ("provenance", "Evidence trail", "optional", "Agents, activities, entities and derivation."),
    ("uncertainty", "Limits and quality", "optional", "Measurement uncertainty, confidence and quality."),
    ("relations", "Typed connections", "optional", "Dependencies, mappings, derivations and correlations."),
    ("policy", "Use conditions", "optional", "Permit, deny, indeterminate and human-review outcomes."),
]


def page_url(path: str) -> str:
    return BASE if path == "index.html" else f"{BASE}{path}"


def json_ld(title: str, description: str, path: str, kind: str) -> str:
    graph = [
        {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "AI Data Understanding Core",
            "alternateName": "ADUC",
            "url": BASE,
            "sameAs": [REPO],
        },
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "ADUC",
            "url": BASE,
            "description": "Working Draft documentation for portable AI data understanding contracts.",
        },
    ]
    if path != "index.html":
        graph.append(
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
                    {"@type": "ListItem", "position": 2, "name": title, "item": page_url(path)},
                ],
            }
        )
    graph.append(
        {
            "@context": "https://schema.org",
            "@type": kind,
            "headline": title,
            "description": description,
            "url": page_url(path),
            "dateModified": UPDATED,
            "isAccessibleForFree": True,
            "about": [
                "AI data interoperability",
                "AI-readable data contract",
                "portable data understanding",
                "deterministic AI data validation",
                "AI data provenance",
                "multi-model data consistency",
            ],
        }
    )
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":"))


def head(title: str, description: str, path: str, kind: str) -> str:
    url = page_url(path)
    return f"""<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark light">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="theme-color" content="#071018">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="ADUC">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <script>document.documentElement.classList.add('js');</script>
  <link rel="stylesheet" href="assets/styles.css">
  <script defer src="assets/app.js"></script>
  <script type="application/ld+json">{json_ld(title, description, path, kind)}</script>
</head>"""


def brand_symbol() -> str:
    return """<svg class="brand-symbol" viewBox="0 0 48 48" aria-hidden="true" focusable="false">
  <rect x="4" y="4" width="40" height="40" rx="12" fill="currentColor" opacity=".12"/>
  <path d="M13 14h22M13 20h16M13 26h22M13 32h12" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>
  <circle cx="35" cy="20" r="2.8" fill="currentColor"/>
  <circle cx="29" cy="32" r="2.8" fill="currentColor"/>
</svg>"""


def header(current: str) -> str:
    links = []
    for href, label in NAV:
        active = ' aria-current="page"' if current == href else ""
        links.append(f'<a href="{href}"{active}>{label}</a>')
    links.append(f'<a class="nav-github" href="{REPO}">GitHub <span aria-hidden="true">↗</span></a>')
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header" data-site-header>
  <div class="shell header-row">
    <a class="brand" href="index.html" aria-label="ADUC home">
      {brand_symbol()}
      <span class="brand-wordmark"><strong>ADUC</strong><small>AI Data Understanding Core</small></span>
    </a>
    <div class="header-status" aria-label="Project status">
      <span class="status-pulse" aria-hidden="true"></span>
      Working Draft 0.1
    </div>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-navigation" data-nav-toggle>
      <span class="sr-only">Open navigation</span>
      <span class="nav-toggle-lines" aria-hidden="true"><i></i><i></i></span>
    </button>
    <nav class="site-nav" id="primary-navigation" aria-label="Primary navigation" data-site-nav>
      {''.join(links)}
    </nav>
  </div>
</header>"""


def footer() -> str:
    return f"""<footer class="site-footer">
  <div class="shell footer-callout">
    <div>
      <p class="eyebrow">Open Working Draft</p>
      <h2>Make understanding portable, not proprietary.</h2>
    </div>
    <div class="footer-actions">
      <a class="button primary" href="docs.html">Run the validator</a>
      <a class="button quiet" href="{REPO}">Open GitHub <span aria-hidden="true">↗</span></a>
    </div>
  </div>
  <div class="shell footer-grid">
    <div class="footer-intro">
      <a class="brand" href="index.html">{brand_symbol()}<span class="brand-wordmark"><strong>ADUC</strong><small>AI Data Understanding Core</small></span></a>
      <p>ADUC is not yet a recognized standard. It does not grant legal permission and does not claim universal interoperability.</p>
    </div>
    <div><h2>Understand</h2><a href="why-aduc.html">Why ADUC</a><a href="core.html">Core model</a><a href="architecture.html">Architecture</a></div>
    <div><h2>Use</h2><a href="validate.html">Validate</a><a href="compare.html">Compare</a><a href="docs.html">Try in 5 minutes</a></div>
    <div><h2>Verify</h2><a href="evidence.html">Evidence</a><a href="trust.html">Trust model</a><a href="roadmap.html">Roadmap</a></div>
  </div>
  <div class="shell footer-bottom"><span>Updated {UPDATED}. Canonical public URL: GitHub Pages.</span><span>Provider-neutral · local-first · unknown-safe</span></div>
</footer>"""


def status_chip(label: str, kind: str = "neutral") -> str:
    return f'<span class="state-chip state-{kind}">{label}</span>'


def code_block(code: str, ident: str | None = None, copy: bool = False) -> str:
    id_attr = f' id="{ident}"' if ident else ""
    button = f'<button class="copy-button" type="button" data-copy-target="#{ident}">Copy</button>' if copy and ident else ""
    return f'<div class="code-frame">{button}<pre class="code-block"{id_attr}><code>{html.escape(code)}</code></pre></div>'


def core_spine() -> str:
    items = []
    for idx, (name, role, required, _) in enumerate(CORE_BLOCKS, 1):
        items.append(
            f'<a href="core.html#{name}" class="core-node" data-required="{required}"><span>{idx:02d}</span><strong>{name}</strong><small>{role}</small></a>'
        )
    return '<div class="core-spine" aria-label="The ten ADUC Core blocks">' + "".join(items) + "</div>"


def render_page(path: str, title: str, description: str, kind: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
{head(title, description, path, kind)}
<body data-page="{path}">
{header(path)}
<main id="main">
{body.strip()}
</main>
{footer()}
</body>
</html>
"""


HOME = f"""
<section class="home-hero">
  <div class="shell home-hero-grid">
    <div class="hero-copy">
      <div class="hero-meta"><span class="draft-badge">Working Draft 0.1</span><span>Core, schemas, validator and comparator available now</span></div>
      <h1>Give every AI system the same understanding of your data.</h1>
      <p class="hero-definition">{CANONICAL_DEFINITION}</p>
      <p class="hero-support">Today, meaning is scattered across prompts, code, mappings, connectors and human documentation. ADUC turns that hidden interpretation into an explicit contract that travels with the resource.</p>
      <div class="hero-actions">
        <a class="button primary" href="docs.html">Try it in 5 minutes</a>
        <a class="button secondary" href="core.html">Explore the Core</a>
      </div>
      <div class="hero-quickproof" aria-label="Current implementation">
        <span><strong>10</strong> Core blocks</span><span><strong>14</strong> local schemas</span><span><strong>24</strong> comparison scenarios</span>
      </div>
    </div>
    <div class="understanding-stage" aria-label="Original data becomes portable understanding through an ADUC contract">
      <div class="stage-label">The ADUC layer</div>
      <div class="stage-source">
        <span class="stage-index">01</span>
        <div><small>Original data</small><code>{{"station":"R42","flow":1.5}}</code></div>
      </div>
      <div class="stage-connector" aria-hidden="true"><span></span></div>
      <div class="stage-contract">
        <div class="contract-header"><span class="stage-index">02</span><strong>ADUC understanding contract</strong>{status_chip('validated', 'valid')}</div>
        <div class="contract-lines"><span>resource</span><span>structure</span><span>semantics</span><span>identity</span><span>context</span><span>provenance</span><span>uncertainty</span><span>relations</span><span>policy</span></div>
        <div class="contract-fact"><code>conceptIri</code><span>WaterDischarge</span></div>
        <div class="contract-fact"><code>unitIri</code><span>M3-PER-SEC</span></div>
        <div class="contract-fact"><code>authority</code><span>reviewed</span></div>
      </div>
      <div class="stage-checks"><span>03</span><strong>Deterministic checks</strong><em>schema · architecture · profiles · comparison</em></div>
      <div class="stage-consumers">
        <div><span>AI system A</span><strong>same explicit facts</strong></div>
        <div><span>AI system B</span><strong>same visible limits</strong></div>
      </div>
    </div>
  </div>
</section>

<section class="proof-ribbon" aria-label="Implemented evidence">
  <div class="shell proof-ribbon-grid"><span><strong>11</strong> valid Core fixtures</span><span><strong>15</strong> invalid Core fixtures</span><span><strong>9</strong> domain evaluators</span><span><strong>Local</strong> deterministic reports</span><a href="evidence.html">Inspect the evidence <b aria-hidden="true">→</b></a></div>
</section>

<section class="section problem-section">
  <div class="shell section-split">
    <div class="section-heading sticky-heading"><p class="eyebrow">The missing layer</p><h2>Machine-readable is not the same as machine-understood.</h2></div>
    <div class="problem-ledger">
      <article><span>01</span><div><h3>Syntax exposes values</h3><p>JSON, CSV and APIs can show that <code>flow</code> is a number. They do not establish what it means, which unit applies or who is authoritative.</p></div></article>
      <article><span>02</span><div><h3>Interpretation hides in glue</h3><p>Prompts, ETL jobs, private mappings and connector code rebuild the same understanding for every consumer.</p></div></article>
      <article><span>03</span><div><h3>Unknowns disappear</h3><p>Identity gaps, uncertainty, conflicts and use restrictions are often flattened into confident but unsafe assumptions.</p></div></article>
      <article class="problem-answer"><span>AD</span><div><h3>ADUC makes the interpretation inspectable</h3><p>One versioned contract carries the meaning, evidence, limits and conditions to every consumer.</p></div></article>
    </div>
  </div>
</section>

<section class="section section-paper" id="how-it-works">
  <div class="shell">
    <div class="section-heading wide"><p class="eyebrow">Four explicit steps</p><h2>From a resource to portable understanding.</h2><p>ADUC accompanies the source. It does not transform or replace the original bytes.</p></div>
    <ol class="protocol-rail">
      <li><span>01</span><strong>Bind the source</strong><p>Identify the exact resource, format, version and digest.</p></li>
      <li><span>02</span><strong>Declare understanding</strong><p>Describe structure, semantics, identity, context, evidence and limits.</p></li>
      <li><span>03</span><strong>Validate and compare</strong><p>Run deterministic schema, architecture and profile checks.</p></li>
      <li><span>04</span><strong>Deliver the same contract</strong><p>Multiple consumers receive the same explicit facts and unknowns.</p></li>
    </ol>
  </div>
</section>

<section class="section core-section">
  <div class="shell">
    <div class="section-heading wide"><p class="eyebrow">The complete Core</p><h2>Ten blocks. One contract. Clear responsibility boundaries.</h2><p>The minimum interoperable envelope is <code>aduc + resource + structure</code>. Every additional block adds explicit understanding without changing the source.</p></div>
    {core_spine()}
    <div class="core-legend"><span><i class="legend-required"></i> Required envelope</span><span><i class="legend-optional"></i> Optional understanding modules</span></div>
  </div>
</section>

<section class="section section-ink demo-section">
  <div class="shell">
    <div class="section-heading wide"><p class="eyebrow">A concrete difference</p><h2>The output is not always “yes”. That is the point.</h2><p>ADUC preserves the reason a comparison succeeds, fails or must remain unresolved.</p></div>
    <div class="comparison-workbench">
      <div class="workbench-source source-a"><small>Source A + contract A</small><strong>Body temperature</strong><code>37 °C</code><span>unit evidence present</span></div>
      <div class="workbench-source source-b"><small>Source B + contract B</small><strong>Body temperature</strong><code>98.6 °F</code><span>conversion evidence present</span></div>
      <div class="workbench-engine"><span>validate A</span><span>validate B</span><strong>deterministic compare</strong></div>
      <div class="workbench-outcomes">
        <div class="outcome outcome-valid"><b>Convertible</b><span>when the unit relation is evidenced</span></div>
        <div class="outcome outcome-unknown"><b>Unknown</b><span>when identity proof is missing</span></div>
        <div class="outcome outcome-contested"><b>Contested</b><span>when qualifying assertions conflict</span></div>
        <div class="outcome outcome-prohibited"><b>Prohibited</b><span>when policy denies the requested use</span></div>
        <div class="outcome outcome-review"><b>Human review</b><span>when automation cannot decide safely</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section example-section">
  <div class="shell example-grid">
    <div class="section-heading"><p class="eyebrow">Real Core syntax</p><h2>A contract is explicit enough to inspect and strict enough to test.</h2><p>This excerpt follows the official complete Core example. It uses <code>conceptIri</code>, <code>unitIri</code>, qualified status, authority and evidence references.</p><a class="text-link" href="example.html">Open the complete example <span aria-hidden="true">→</span></a></div>
    {code_block('''{{
  "aduc": {{
    "contractId": "urn:aduc:contract:river-r42:2026-07-14",
    "coreVersion": "0.1.0-alpha.0",
    "status": "reviewed"
  }},
  "resource": {{
    "id": "urn:example:resource:river-r42-observations",
    "mediaType": "application/json",
    "digest": "aaaaaaaa…"
  }},
  "structure": {{
    "representation": "record",
    "records": [{{"fields": [{{"name": "flow", "primitiveType": "number"}}]}}]
  }},
  "semantics": {{
    "assertions": [{{
      "subjectRef": "urn:example:field:flow",
      "conceptIri": "https://example.org/vocab/env/WaterDischarge",
      "unitIri": "https://qudt.org/vocab/unit/M3-PER-SEC",
      "status": "reviewed",
      "authority": "reviewed"
    }}]
  }}
}}''', 'home-contract', True)}
  </div>
</section>

<section class="section section-paper status-section">
  <div class="shell">
    <div class="section-heading wide"><p class="eyebrow">Status without marketing blur</p><h2>Implemented, active, planned and unproven are different states.</h2></div>
    <div class="status-board">
      <article class="status-lane lane-now"><header><span></span><h3>Available now</h3></header><p>10-block Core, 14 schemas, 11 valid and 15 invalid fixtures, unified validator, deterministic comparator, 24 scenarios, nine evaluators and semantic-profile migration.</p></article>
      <article class="status-lane lane-progress"><header><span></span><h3>In progress</h3></header><p>Deterministic formatting of complete validated Core contracts without inference or silent repair.</p></article>
      <article class="status-lane lane-planned"><header><span></span><h3>Planned, not available</h3></header><p>JSON/CSV compiler, graphical review, stabilized packages, registry, MCP adapter and official extensions.</p></article>
      <article class="status-lane lane-proof"><header><span></span><h3>Not proven</h3></header><p>External interoperability with two independent AI consumers and any absolute “first in the world” claim.</p></article>
    </div>
  </div>
</section>

<section class="section principles-section">
  <div class="shell principles-layout">
    <div class="section-heading"><p class="eyebrow">Design principles</p><h2>Useful to AI. Safe for people to inspect.</h2></div>
    <div class="principle-list">
      <article><span>AI-first</span><p>Machine-readable contracts and deterministic reports, without dependence on one provider.</p></article>
      <article><span>Human-review-first</span><p>Conflicts, unknowns and authority gaps remain visible instead of being silently repaired.</p></article>
      <article><span>Privacy and security by design</span><p>Local schemas, bounded processing and no unapproved remote resolution.</p></article>
      <article><span>Unknown-safe</span><p>Absence of evidence is not converted into equivalence, permission or certainty.</p></article>
    </div>
  </div>
</section>

<section class="section final-cta"><div class="shell final-cta-box"><div><p class="eyebrow">Start with evidence</p><h2>Validate the complete Core example locally.</h2><p>No account, hosted upload or remote schema resolution is required.</p></div>{code_block('python tools/aduc_core.py validate examples/core/complete-model.example.json', 'home-command', True)}<div class="hero-actions"><a class="button primary" href="validate.html">Understand validation</a><a class="button secondary" href="{REPO}">View source on GitHub</a></div></div></section>
"""


WHY = """
<section class="page-hero page-hero-why"><div class="shell page-hero-grid"><div><p class="eyebrow">Why ADUC</p><h1>The missing layer between data and AI.</h1><p class="page-lead">Data can be machine-readable and still machine-ambiguous. ADUC turns the interpretation hidden in prompts, code and private mappings into a portable contract.</p></div><div class="hero-thesis"><span>Readable</span><b>≠</b><span>Understood</span><i>ADUC makes the difference explicit.</i></div></div></section>

<section class="section"><div class="shell narrative-grid"><aside class="narrative-index" aria-label="Page sections"><a href="#syntax">01 Syntax</a><a href="#prompts">02 Prompts</a><a href="#lock-in">03 Lock-in</a><a href="#changes">04 What changes</a></aside><div class="narrative-flow">
  <article id="syntax"><p class="eyebrow">01 · Syntax</p><h2>JSON and CSV carry values, not a shared interpretation.</h2><p>A field named <code>flow</code> may be a discharge rate, a business process or a boolean state. A number does not identify its quantity kind, unit, timestamp role, authority or uncertainty.</p><div class="contrast-line"><span>Data alone</span><code>{"flow": 1.5}</code><strong>multiple plausible meanings</strong></div></article>
  <article id="prompts"><p class="eyebrow">02 · Prompts</p><h2>A prompt explains one interaction. It is not a portable contract.</h2><p>Prompt text is difficult to version, validate, compare and audit across models. It may be omitted from the next integration or interpreted differently by another provider.</p><div class="contrast-line"><span>Prompt</span><code>“flow means water discharge”</code><strong>workflow-specific and hard to test</strong></div></article>
  <article id="lock-in"><p class="eyebrow">03 · Lock-in</p><h2>Private mappings make every consumer relearn the same source.</h2><p>ETL jobs and connectors often know the real meaning, but that knowledge stays trapped in proprietary code. The next AI system must rebuild it, trust undocumented assumptions or guess.</p></article>
  <article id="changes"><p class="eyebrow">04 · What changes</p><h2>ADUC makes understanding a versioned object.</h2><p>Structure, semantics, identity, context, provenance, uncertainty, relations and use conditions can travel together and be checked by the same deterministic rules.</p><div class="before-after"><div><small>Before</small><strong>Prompts · code · mappings · docs</strong><span>fragmented, implicit, provider-specific</span></div><div><small>With ADUC</small><strong>One explicit understanding contract</strong><span>portable, comparable, reviewable</span></div></div></article>
</div></div></section>

<section class="section section-ink"><div class="shell"><div class="section-heading wide"><p class="eyebrow">Concrete consequences</p><h2>Small ambiguities become large operational errors.</h2></div><div class="case-studies">
  <article><span class="case-number">01</span><div><h3>Two station identifiers</h3><p><strong>Without ADUC:</strong> systems may merge <code>R42</code> and <code>897</code> because labels look similar.</p><p><strong>With ADUC:</strong> identity remains unknown until qualifying evidence supports equivalence. Correlation does not become identity.</p></div></article>
  <article><span class="case-number">02</span><div><h3>Celsius and Fahrenheit</h3><p><strong>Without ADUC:</strong> values can be combined as if their units were identical.</p><p><strong>With ADUC:</strong> quantity kind, unit identity and conversion evidence make a deterministic conversion possible.</p></div></article>
  <article><span class="case-number">03</span><div><h3>Conditions of use</h3><p><strong>Without ADUC:</strong> permission may be assumed from access to the bytes.</p><p><strong>With ADUC:</strong> policy evaluation can return permit, deny, indeterminate or requiresHumanReview. It still does not grant legal permission by itself.</p></div></article>
</div></div></section>

<section class="section standards-section"><div class="shell"><div class="section-heading wide"><p class="eyebrow">Composition, not replacement</p><h2>ADUC connects responsibilities that existing standards already handle well.</h2><p>It can reference JSON Schema, RDF/OWL, PROV-O, DQV, ODRL, QUDT, UCUM and other established vocabularies. The Core provides one contract boundary for AI consumers.</p></div><div class="standards-matrix"><div><strong>JSON Schema</strong><span>structure</span></div><div><strong>RDF / OWL</strong><span>semantic vocabularies</span></div><div><strong>PROV-O</strong><span>provenance</span></div><div><strong>DQV</strong><span>quality</span></div><div><strong>ODRL</strong><span>use policies</span></div><div class="matrix-aduc"><strong>ADUC</strong><span>portable understanding contract</span></div></div></div></section>

<section class="section section-paper"><div class="shell faq-layout"><div class="section-heading"><p class="eyebrow">Quick distinctions</p><h2>What ADUC is — and is not.</h2></div><div class="faq">
<details open><summary>Is ADUC an AI model?</summary><p>No. It is a machine-readable contract consumed by AI systems, tools and applications.</p></details>
<details><summary>Is ADUC the same as MCP?</summary><p>No. MCP transports tool and agent interactions. A future adapter could transport an ADUC contract, but MCP is not the Core.</p></details>
<details><summary>Is ADUC a universal ontology?</summary><p>No. It references external vocabularies and ontologies instead of replacing them.</p></details>
<details><summary>Does ADUC reveal private model reasoning?</summary><p>No. It makes declared consumer behavior and contract handling auditable; it does not expose private chain-of-thought.</p></details>
</div></div></section>
"""


def core_details() -> str:
    examples = {
        "aduc": '"coreVersion": "0.1.0-alpha.0"',
        "resource": '"digest": "aaaaaaaa…"',
        "structure": '"sourcePath": "$.flow"',
        "semantics": '"conceptIri": "…/WaterDischarge"',
        "identity": '"decision": "exactEntity"',
        "context": '"timezoneIri": "urn:iana:tz:UTC"',
        "provenance": '"typeIri": "http://www.w3.org/ns/prov#Activity"',
        "uncertainty": '"uncertaintyType": "relative"',
        "relations": '"relationIri": "http://www.w3.org/2004/02/skos/core#closeMatch"',
        "policy": '"effect": "deny"',
    }
    boundaries = {
        "aduc": "Identifies the contract; it does not certify the truth of every assertion.",
        "resource": "Binds the source; it does not embed or replace the source bytes.",
        "structure": "Describes addressable shape; it does not define domain meaning.",
        "semantics": "Declares meaning; it does not create a universal vocabulary.",
        "identity": "Records evidence-backed identity decisions; matching labels are insufficient.",
        "context": "Defines interpretation conditions; it does not infer missing operational facts.",
        "provenance": "Records agents and activities; it does not prove trustworthiness automatically.",
        "uncertainty": "Preserves limits and quality; it does not convert confidence into authority.",
        "relations": "Declares typed connections; transitivity and causality are never assumed.",
        "policy": "Describes use conditions; it is not legal advice or an access-control engine.",
    }
    parts = []
    for idx, (name, role, required, description) in enumerate(CORE_BLOCKS, 1):
        parts.append(f'''<article class="core-detail" id="{name}"><div class="core-detail-key"><span>{idx:02d}</span><code>{name}</code><small>{required}</small></div><div><h2>{role}</h2><p>{description}</p><div class="core-mini-example"><code>{html.escape(examples[name])}</code></div><p class="boundary-note"><strong>Boundary:</strong> {boundaries[name]}</p></div></article>''')
    return "".join(parts)


CORE = f"""
<section class="page-hero"><div class="shell page-hero-grid"><div><p class="eyebrow">The Core model</p><h1>Ten responsibilities, separated on purpose.</h1><p class="page-lead">The Core is a normative envelope for complete data understanding. Required source binding stays distinct from optional meaning, identity, evidence, uncertainty, relations and policy.</p></div><div class="core-orbit" aria-label="ADUC Core overview"><div class="orbit-center">ADUC<br><small>contract</small></div><span>source</span><span>meaning</span><span>identity</span><span>context</span><span>evidence</span><span>limits</span><span>relations</span><span>policy</span></div></div></section>
<section class="section core-detail-section"><div class="shell"><div class="minimum-envelope"><span>Minimum interoperable envelope</span><strong><code>aduc</code> + <code>resource</code> + <code>structure</code></strong><p>Optional modules are included when their facts are available and relevant. Missing evidence remains visible rather than being guessed.</p></div><div class="core-detail-list">{core_details()}</div></div></section>
<section class="section section-ink"><div class="shell boundary-layout"><div class="section-heading"><p class="eyebrow">Responsibility boundaries</p><h2>One fact should have one owner.</h2></div><div class="boundary-rules"><p><span>01</span> A field path belongs to <code>structure</code>; its domain meaning belongs to <code>semantics</code>.</p><p><span>02</span> An entity identifier belongs to <code>identity</code>; the activity that asserted it belongs to <code>provenance</code>.</p><p><span>03</span> Measurement uncertainty belongs to <code>uncertainty</code>; semantic authority remains a separate qualification.</p><p><span>04</span> Use conditions belong to <code>policy</code>; access to the bytes does not imply permission.</p></div></div></section>
"""


VALIDATE = f"""
<section class="page-hero page-hero-tool"><div class="shell page-hero-grid"><div><p class="eyebrow">Validate</p><h1>One command. A complete Core validation pipeline.</h1><p class="page-lead">The unified validator loads JSON, applies 14 local Draft 2020-12 schemas, checks Core architecture and runs applicable profile evaluators.</p><div class="hero-actions"><a class="button primary" href="#command">Copy the command</a><a class="button secondary" href="evidence.html">Inspect test evidence</a></div></div><div class="tool-terminal">{code_block('python tools/aduc_core.py validate examples/core/complete-model.example.json', 'validate-hero-command', True)}<div class="terminal-result"><span class="result-dot"></span><strong>Deterministic local report</strong><small>JSON or human-readable text</small></div></div></div></section>
<section class="section" id="command"><div class="shell command-grid"><div class="section-heading"><p class="eyebrow">Official CLI</p><h2>Validate a complete contract.</h2><p>No hosted upload or remote schema resolution is required.</p></div>{code_block('''python tools/aduc_core.py validate examples/core/complete-model.example.json
python tools/aduc_core.py validate examples/core/complete-model.example.json --format json
python tools/aduc_core.py validate contract.json --schema-only
python tools/aduc_core.py validate contract.json --no-profile-evaluation''', 'validate-commands', True)}</div></section>
<section class="section section-paper"><div class="shell"><div class="section-heading wide"><p class="eyebrow">Validation order</p><h2>Every layer answers a different question.</h2></div><ol class="validation-pipeline"><li><span>01</span><div><strong>Load JSON</strong><p>Is the input readable, bounded and free of duplicate members?</p></div></li><li><span>02</span><div><strong>Apply schemas</strong><p>Do the Core and module shapes conform to the 14 local Draft 2020-12 schemas?</p></div></li><li><span>03</span><div><strong>Check architecture</strong><p>Do identifiers, references, bindings, ownership rules and graph limits hold?</p></div></li><li><span>04</span><div><strong>Evaluate profiles</strong><p>Do applicable unit, time, identity, provenance, uncertainty, relation and policy rules pass?</p></div></li><li><span>05</span><div><strong>Return final status</strong><p>Valid, valid with warnings, requires human review or blocked.</p></div></li></ol></div></section>
<section class="section"><div class="shell report-grid"><div class="section-heading"><p class="eyebrow">Stable report shape</p><h2>Diagnostics stay attributable.</h2><p>Schema, architecture and profile outcomes remain separate so a consumer can see what failed and why.</p></div>{code_block('''{{
  "reportVersion": "0.1.0",
  "valid": false,
  "outcome": "blocked",
  "contractId": "urn:example:contract:1",
  "summary": {{"errors": 1, "warnings": 0, "humanReview": 0}},
  "pipeline": {{
    "jsonLoaded": true,
    "schemaValid": true,
    "architectureValid": false,
    "profileEvaluation": true
  }},
  "diagnostics": []
}}''')}</div></section>
<section class="section section-ink"><div class="shell"><div class="section-heading wide"><p class="eyebrow">Validation boundaries</p><h2>A valid contract is structured and internally consistent — not automatically true or legally permitted.</h2></div><div class="boundary-strip"><span>No factual truth proof</span><span>No automatic authority</span><span>No universal permission</span><span>No unapproved remote trust</span></div></div></section>
"""


COMPARE = f"""
<section class="page-hero page-hero-tool"><div class="shell page-hero-grid"><div><p class="eyebrow">Compare</p><h1>See what changed — and what the change means.</h1><p class="page-lead">The deterministic comparator separates mechanical <code>changeType</code> from normative <code>assessment</code>. A modified field is not automatically incompatible.</p></div><div class="compare-signal"><div><small>Mechanical</small><strong>changeType</strong><span>added · removed · modified · unchanged</span></div><i aria-hidden="true">≠</i><div><small>Normative</small><strong>assessment</strong><span>equivalent · convertible · unknown · prohibited…</span></div></div></div></section>
<section class="section"><div class="shell command-grid"><div class="section-heading"><p class="eyebrow">Official CLI</p><h2>Compare two complete contracts.</h2></div>{code_block('''python tools/aduc_core.py compare contract-a.json contract-b.json
python tools/aduc_core.py compare examples/core/complete-model.example.json examples/core/complete-model.example.json
python tools/aduc_core.py compare contract-a.json contract-b.json --format json''', 'compare-commands', True)}</div></section>
<section class="section section-paper"><div class="shell"><div class="section-heading wide"><p class="eyebrow">Normative assessment vocabulary</p><h2>Results preserve uncertainty and policy.</h2></div><div class="assessment-spectrum"><span class="outcome-valid">equivalent</span><span class="outcome-valid">convertible</span><span class="outcome-compatible">compatible</span><span class="outcome-prohibited">incompatible</span><span class="outcome-unknown">unknown</span><span class="outcome-contested">contested</span><span class="outcome-deprecated">deprecated</span><span class="outcome-prohibited">prohibited</span><span class="outcome-review">requiresHumanReview</span></div></div></section>
<section class="section"><div class="shell compare-explanation"><div class="section-heading"><p class="eyebrow">Safe comparison</p><h2>No evidence, no invented equivalence.</h2></div><div class="compare-rules"><article><span>Units</span><p>Convertible only when quantity kind and an allowed conversion are established.</p></article><article><span>Identity</span><p>Matching labels do not merge entities. A qualifying identity decision is required.</p></article><article><span>Relations</span><p>Close match is not equality. Direction, authority and evidence remain explicit.</p></article><article><span>Policy</span><p>Permission is never inferred from data access or schema compatibility.</p></article></div></div></section>
<section class="section section-ink"><div class="shell"><div class="section-heading wide"><p class="eyebrow">Example interpretation</p><h2>The same structural change can lead to different assessments.</h2></div><div class="change-cases"><div><code>unitIri</code><strong>modified</strong><span class="state-chip state-valid">convertible</span><p>Known deterministic conversion with matching quantity kind.</p></div><div><code>identity assertion</code><strong>added</strong><span class="state-chip state-review">requiresHumanReview</span><p>Evidence exists but the authority level is insufficient for an automatic merge.</p></div><div><code>policy prohibition</code><strong>added</strong><span class="state-chip state-prohibited">prohibited</span><p>The requested use is explicitly denied.</p></div></div></div></section>
"""


ARCHITECTURE = """
<section class="page-hero"><div class="shell page-hero-grid"><div><p class="eyebrow">Architecture</p><h1>A small Core with explicit layers around it.</h1><p class="page-lead">ADUC separates the normative contract, schema enforcement, deterministic evaluation and future adoption tooling. Vision does not masquerade as implementation.</p></div><div class="architecture-stack"><span>Future tooling</span><strong>Compiler · Review UI · Registry · MCP adapter</strong><span>Deterministic tools</span><strong>Formatter · Validator · Comparator</strong><span>Normative contract</span><strong>10-block Core + 14 schemas</strong><span>Original resource</span><strong>JSON · CSV · API · document · database</strong></div></div></section>
<section class="section"><div class="shell architecture-lanes"><article><span>01</span><div><h2>Original resource</h2><p>The source remains authoritative. ADUC binds it through identifiers, versions and digests without replacing its bytes.</p></div></article><article><span>02</span><div><h2>Normative Core</h2><p>Ten blocks define responsibility boundaries. The minimum envelope is <code>aduc + resource + structure</code>.</p></div></article><article><span>03</span><div><h2>Schema family</h2><p>Fourteen local Draft 2020-12 schemas enforce module shapes and closed Core objects.</p></div></article><article><span>04</span><div><h2>Unified validator and comparator</h2><p>One local interface orchestrates schema, architecture and applicable domain rules with deterministic reports.</p></div></article><article><span>05</span><div><h2>Legacy semantic profile migration</h2><p>The accepted migration tool converts the earlier standalone profile only when an explicit manifest supplies missing Core facts.</p></div></article><article class="future"><span>06</span><div><h2>Future adoption layer</h2><p>Compiler, review UI, packages, registry and MCP adapter remain separate roadmap work.</p></div></article></div></section>
<section class="section section-paper"><div class="shell"><div class="section-heading wide"><p class="eyebrow">Provider neutrality</p><h2>The Core does not depend on a model vendor.</h2><p>Contracts are local JSON documents. Validation and comparison are deterministic Python tools. A consumer can be an AI system, an agent, an application or a human review workflow.</p></div></div></section>
"""


TRUST = """
<section class="page-hero page-hero-trust"><div class="shell page-hero-grid"><div><p class="eyebrow">Trust model</p><h1>Explicit evidence beats confident guessing.</h1><p class="page-lead">ADUC is AI-first, not AI-only. It makes unknowns, conflicts, authority and use conditions visible to machines and people.</p></div><div class="trust-seal"><strong>UNKNOWN</strong><span>is a valid result</span><i>no silent promotion</i></div></div></section>
<section class="section"><div class="shell trust-principles"><article><span>01</span><h2>Provider-neutral</h2><p>No model-specific reasoning format is required. Consumers receive the same contract and the same deterministic checks.</p></article><article><span>02</span><h2>Human review</h2><p>Requires-human-review is an explicit outcome, not a failure to hide.</p></article><article><span>03</span><h2>Privacy by default</h2><p>Validation operates locally and does not upload source data or resolve remote schemas without approval.</p></article><article><span>04</span><h2>Security by design</h2><p>Input size, depth, node count and graph behavior are bounded. Duplicate JSON members and dangerous references are rejected.</p></article><article><span>05</span><h2>Authority stays separate</h2><p>Confidence, evidence and authority are distinct. High confidence does not create canonical status.</p></article><article><span>06</span><h2>No automatic legal permission</h2><p>Policy conditions can be evaluated, but ADUC is not legal advice or a production access-control system.</p></article></div></section>
<section class="section section-ink"><div class="shell"><div class="section-heading wide"><p class="eyebrow">Failure-safe states</p><h2>What the contract cannot establish remains visible.</h2></div><div class="state-vocabulary"><span class="outcome-unknown">unknown</span><span class="outcome-inferred">inferred</span><span class="outcome-contested">contested</span><span class="outcome-deprecated">deprecated</span><span class="outcome-valid">canonical</span><span class="outcome-review">requires human review</span></div></div></section>
<section class="section section-paper"><div class="shell boundary-layout"><div class="section-heading"><p class="eyebrow">Operational limits</p><h2>Trust requires boundaries.</h2></div><div class="boundary-rules"><p><span>01</span> No unapproved remote schema or vocabulary resolution.</p><p><span>02</span> No inferred publisher authority, identity equivalence or legal permission.</p><p><span>03</span> No silent repair of invalid complete-Core contracts.</p><p><span>04</span> No claim that a valid contract proves truth in the world.</p></div></div></section>
"""


EVIDENCE = f"""
<section class="page-hero"><div class="shell page-hero-grid"><div><p class="eyebrow">Conformance and evidence</p><h1>Claims should point to executable evidence.</h1><p class="page-lead">ADUC separates implemented artifacts, automated conformance evidence and future external proof. Green tests do not prove universal adoption.</p></div><div class="evidence-counter"><div><strong>14</strong><span>local schemas</span></div><div><strong>11</strong><span>valid fixtures</span></div><div><strong>15</strong><span>invalid fixtures</span></div><div><strong>24</strong><span>comparison scenarios</span></div></div></div></section>
<section class="section"><div class="shell evidence-timeline"><article><span>01</span><div><h2>Normative artifacts</h2><p>Ten-block Core model, modular Draft 2020-12 schema family and documented validation/comparison contracts.</p></div><a href="core.html">Inspect Core</a></article><article><span>02</span><div><h2>Reference fixtures</h2><p>11 complete valid contracts, 15 intentionally invalid contracts and 24 comparison scenarios.</p></div><a href="{REPO}/tree/main/examples/core">Open fixtures</a></article><article><span>03</span><div><h2>Deterministic reports</h2><p>JSON and text reports expose schema, architecture, profile and comparison outcomes.</p></div><a href="validate.html">See validation</a></article><article><span>04</span><div><h2>Continuous integration</h2><p>Repository workflows execute contract, evaluator, roadmap and public-site checks.</p></div><a href="{REPO}/actions">Open CI</a></article></div></section>
<section class="section section-paper"><div class="shell proof-boundary"><div><p class="eyebrow">What evidence does not exist yet</p><h2>No external two-consumer AI proof has completed.</h2><p>No absolute first-world claim is made. A credible external claim requires two independent consumers, frozen inputs, controlled with/without-ADUC tests, published reports and reproducible failure analysis.</p></div><div class="proof-checklist"><span>Independent consumers</span><span>Frozen contracts</span><span>Controlled baseline</span><span>Published diagnostics</span><span>Repeatable results</span></div></div></section>
<section class="section section-ink"><div class="shell"><div class="section-heading wide"><p class="eyebrow">Future conformance</p><h2>Conformance classes remain roadmap work.</h2><p>Schema conformance, complete-Core validation, comparison behavior and consumer-behavior audits may become distinct classes. They are not yet presented as a mature certification program.</p></div></div></section>
"""


ROADMAP = """
<section class="page-hero"><div class="shell page-hero-grid"><div><p class="eyebrow">Roadmap</p><h1>Build the contract first. Prove adoption before scaling the tooling.</h1><p class="page-lead">The roadmap follows the repository Master Plan and keeps one active technical task at a time.</p></div><div class="roadmap-now"><small>Active task - Deterministic Core formatter</small><strong>Stable bytes without changing meaning.</strong><span>Issue #60 · open</span></div></div></section>
<section class="section"><div class="shell roadmap-track"><article class="complete"><span>Phase 0</span><div><h2>Core foundations</h2><p>Normative ten-block model, responsibility boundaries and complete example.</p></div><strong>Complete</strong></article><article class="complete"><span>Phase 1</span><div><h2>Schema and migration</h2><p>14 local schemas, valid/invalid fixtures and deterministic semantic-profile migration.</p></div><strong>Complete</strong></article><article class="active"><span>Phase 2</span><div><h2>Deterministic Core tools</h2><p>Unified validator and comparator complete. Contract formatter is the single active task.</p></div><strong>Active</strong></article><article class="blocked"><span>Phase 3</span><div><h2>Compiler and review workflow</h2><p>JSON/CSV compiler remains blocked until adoption, value and review-tax gates are ready.</p></div><strong>Blocked</strong></article><article><span>Phase 4</span><div><h2>Packages, registry and adapters</h2><p>Public packages, registry, MCP adapter and official extensions.</p></div><strong>Planned</strong></article><article><span>Phase 5</span><div><h2>Independent interoperability proof</h2><p>Two external consumers, controlled evaluation and published evidence.</p></div><strong>Foundations only</strong></article></div></section>
<section class="section section-paper"><div class="shell boundary-layout"><div class="section-heading"><p class="eyebrow">Release discipline</p><h2>Roadmap language follows evidence.</h2></div><div class="boundary-rules"><p><span>01</span> A future compiler is not described as available.</p><p><span>02</span> A preview deployment is not treated as adoption proof.</p><p><span>03</span> A passing schema does not establish factual truth.</p><p><span>04</span> A global novelty claim waits for independent prior-art and interoperability evidence.</p></div></div></section>
"""


DOCS = f"""
<section class="page-hero page-hero-tool"><div class="shell page-hero-grid"><div><p class="eyebrow">Try in 5 minutes</p><h1>Clone. Validate. Compare.</h1><p class="page-lead">The current reference tools run locally with Python. Start with the official complete Core contract, then inspect deterministic reports.</p></div><div class="quickstart-steps"><span>01 Clone</span><span>02 Install</span><span>03 Validate</span><span>04 Compare</span></div></div></section>
<section class="section"><div class="shell docs-flow"><article><span>01</span><div><h2>Clone and install</h2>{code_block('''git clone https://github.com/BACOUL/AI-Data-Understanding-Core-ADUC.git
cd AI-Data-Understanding-Core-ADUC
python -m pip install -r requirements-dev.txt''', 'docs-install', True)}</div></article><article><span>02</span><div><h2>Validate the complete Core example</h2>{code_block('python tools/aduc_core.py validate examples/core/complete-model.example.json', 'docs-validate', True)}</div></article><article><span>03</span><div><h2>Compare two contracts</h2>{code_block('python tools/aduc_core.py compare examples/core/complete-model.example.json examples/core/complete-model.example.json', 'docs-compare', True)}</div></article><article><span>04</span><div><h2>Run the principal checks</h2>{code_block('''python tools/validate_contracts.py
python -m unittest discover -s tests -p "test_*.py"
python tools/validate_website.py''', 'docs-tests', True)}</div></article></div></section>
<section class="section section-paper"><div class="shell"><div class="section-heading wide"><p class="eyebrow">Reference evaluators</p><h2>Domain tools remain available for focused testing.</h2><p>The unified Core interface is the main path. Specialized tools remain useful as domain reference evaluators.</p></div><div class="tool-index"><code>aduc_epistemic.py</code><code>aduc_source_binding.py</code><code>aduc_units.py</code><code>aduc_time.py</code><code>aduc_identity.py</code><code>aduc_provenance.py</code><code>aduc_uncertainty.py</code><code>aduc_relations.py</code><code>aduc_policy.py</code></div></div></section>
<section class="section section-ink"><div class="shell final-cta-box"><div><p class="eyebrow">Next reference</p><h2>Read the Core before building an integration.</h2><p>The specification defines what each module owns and what it must never infer.</p></div><div class="hero-actions"><a class="button primary" href="core.html">Read the Core</a><a class="button secondary" href="specification.html">Specification index</a></div></div></section>
"""


EXAMPLE = f"""
<section class="page-hero"><div class="shell page-hero-grid"><div><p class="eyebrow">Complete example</p><h1>A ten-block contract bound to one exact resource.</h1><p class="page-lead">The official river-observation example demonstrates source binding, field structure, semantics, identity, temporal context, provenance, uncertainty, relations and policy.</p></div><div class="example-summary"><span>contract</span><strong>river-r42 · 2026-07-14</strong><span>coreVersion</span><strong>0.1.0-alpha.0</strong><span>status</span><strong>reviewed</strong></div></div></section>
<section class="section"><div class="shell example-grid"><div class="section-heading"><p class="eyebrow">Source binding</p><h2>The contract identifies the source before describing it.</h2><p>The resource block carries media type, version, locator and SHA-256 digest. The structure block then exposes addressable records and fields.</p></div>{code_block('''{{
  "aduc": {{
    "contractId": "urn:aduc:contract:river-r42:2026-07-14",
    "coreVersion": "0.1.0-alpha.0",
    "status": "reviewed"
  }},
  "resource": {{
    "id": "urn:example:resource:river-r42-observations:2026-07-14T08:00Z",
    "kind": "dataset",
    "mediaType": "application/json",
    "digest": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
  }},
  "structure": {{
    "representation": "record",
    "records": [{{
      "fields": [
        {{"name": "station", "sourcePath": "$.station", "primitiveType": "string"}},
        {{"name": "flow", "sourcePath": "$.flow", "primitiveType": "number"}}
      ]
    }}]
  }}
}}''')}</div></section>
<section class="section section-paper"><div class="shell example-grid"><div class="section-heading"><p class="eyebrow">Qualified meaning</p><h2>Meaning includes evidence and limits.</h2><p>The assertion points to a concept and unit while preserving status, authority, evidence, provenance, conflict and lifecycle.</p></div>{code_block('''{{
  "id": "urn:example:semantic:flow",
  "subjectRef": "urn:example:field:flow",
  "conceptIri": "https://example.org/vocab/env/WaterDischarge",
  "mappingRelationIri": "http://www.w3.org/2004/02/skos/core#exactMatch",
  "unitIri": "https://qudt.org/vocab/unit/M3-PER-SEC",
  "status": "reviewed",
  "authority": "reviewed",
  "evidenceRefs": ["urn:example:evidence:river-dictionary"],
  "provenanceRef": "urn:example:activity:semantic-review",
  "uncertaintyRef": "urn:example:uncertainty:flow-relative",
  "conflict": "clear",
  "lifecycle": "active"
}}''')}</div></section>
<section class="section"><div class="shell"><div class="section-heading wide"><p class="eyebrow">Open the source</p><h2>The website excerpt is informative. The repository file is authoritative.</h2></div><a class="button primary" href="{REPO}/blob/main/examples/core/complete-model.example.json">View complete-model.example.json <span aria-hidden="true">↗</span></a></div></section>
"""


SPECIFICATION = f"""
<section class="page-hero"><div class="shell page-hero-grid"><div><p class="eyebrow">Specification index</p><h1>Normative Core, schemas and deterministic behavior.</h1><p class="page-lead">The public site summarizes the project. The repository specifications and ADRs remain the authoritative technical references.</p></div><div class="spec-mark"><strong>0.1</strong><span>Working Draft</span><small>not a recognized standard</small></div></div></section>
<section class="section"><div class="shell spec-directory"><a href="{REPO}/blob/main/spec/ADUC_CORE_SPEC_0_1.md"><span>Core</span><strong>ADUC Core specification</strong><small>Normative ten-block model</small></a><a href="{REPO}/blob/main/spec/ADUC_CORE_MODEL_0_1.md"><span>Model</span><strong>Core object model</strong><small>Envelope and module boundaries</small></a><a href="{REPO}/blob/main/schema/aduc-core.schema.json"><span>Schema</span><strong>Draft 2020-12 entry point</strong><small>Official modular schema family</small></a><a href="{REPO}/blob/main/spec/ADUC_CORE_VALIDATION_0_1.md"><span>Validate</span><strong>Validation report contract</strong><small>Pipeline and outcomes</small></a><a href="{REPO}/blob/main/spec/ADUC_CORE_COMPARISON_0_1.md"><span>Compare</span><strong>Comparison report contract</strong><small>Change types and assessments</small></a><a href="{REPO}/tree/main/docs/decisions"><span>ADRs</span><strong>Architecture decisions</strong><small>Accepted rules and boundaries</small></a></div></section>
<section class="section section-paper"><div class="shell"><div class="section-heading wide"><p class="eyebrow">Conformance warning</p><h2>Schema conformance is necessary, not sufficient.</h2><p>Architecture and profile checks enforce rules that JSON Schema alone cannot decide, including graph references, one-owner boundaries, identity evidence and policy context.</p></div></div></section>
"""


NOT_FOUND = """
<section class="page-hero not-found"><div class="shell"><p class="eyebrow">404 · Unknown reference</p><h1>This path is not part of the current contract.</h1><p class="page-lead">The resource may have moved or the link may be incomplete. Unknown stays unknown until a valid target is available.</p><div class="hero-actions"><a class="button primary" href="index.html">Return home</a><a class="button secondary" href="docs.html">Open documentation</a></div></div></section>
<section class="section"><div class="shell"><h2>Useful destinations</h2><div class="link-rail"><a href="core.html">Core model</a><a href="validate.html">Validation</a><a href="compare.html">Comparison</a><a href="evidence.html">Evidence</a></div></div></section>
"""

PAGES = {
    "index.html": ("ADUC — Portable data understanding for AI systems", "ADUC makes data structure, meaning, context, identity, provenance, uncertainty, relations and use conditions explicit and portable across AI systems.", "WebSite", HOME),
    "why-aduc.html": ("Why ADUC — The missing data-understanding layer for AI", "Why JSON, CSV, prompts and proprietary mappings do not preserve portable understanding across AI systems.", "TechArticle", WHY),
    "core.html": ("ADUC Core — The ten-block AI-readable data contract", "Explore the ten normative ADUC Core blocks, their responsibilities, required status and safety boundaries.", "TechArticle", CORE),
    "validate.html": ("Validate ADUC Core contracts deterministically", "Run the unified ADUC full-Core validator and understand schema, architecture and profile diagnostics.", "SoftwareSourceCode", VALIDATE),
    "compare.html": ("Compare ADUC Core contracts deterministically", "Compare complete ADUC Core contracts while separating mechanical changes from normative assessments.", "SoftwareSourceCode", COMPARE),
    "architecture.html": ("ADUC architecture — Core, schemas, tools and future layers", "Understand the boundary between the ADUC normative Core, schemas, validator, comparator, migration and future tooling.", "TechArticle", ARCHITECTURE),
    "trust.html": ("ADUC trust model — Unknown-safe, local-first and reviewable", "How ADUC preserves unknowns, authority, evidence, privacy, security and human-review requirements.", "TechArticle", TRUST),
    "evidence.html": ("ADUC conformance evidence — Schemas, fixtures, tests and limits", "Inspect implemented ADUC schemas, fixtures, comparison scenarios, deterministic reports, CI evidence and unproven claims.", "TechArticle", EVIDENCE),
    "roadmap.html": ("ADUC roadmap — From Core foundations to independent proof", "The evidence-gated ADUC roadmap for deterministic tooling, adoption, review workflows and external interoperability proof.", "TechArticle", ROADMAP),
    "docs.html": ("ADUC documentation — Validate and compare in five minutes", "Clone ADUC, install local dependencies, validate a complete Core contract, compare contracts and run the test suite.", "SoftwareSourceCode", DOCS),
    "example.html": ("ADUC complete Core example — River observation contract", "Read an official ten-block ADUC Core contract excerpt with source binding, semantics, identity, provenance, uncertainty and policy.", "TechArticle", EXAMPLE),
    "specification.html": ("ADUC specification index — Core, schemas and reports", "Authoritative ADUC Core, schema, validation, comparison and architecture-decision references.", "TechArticle", SPECIFICATION),
}

CSS = r"""
:root {
  --ink-950: #050a0e;
  --ink-900: #071018;
  --ink-850: #0a1620;
  --ink-800: #0f1d28;
  --ink-700: #182b38;
  --paper: #f1efe7;
  --paper-soft: #e7e3d8;
  --text: #f7f8f5;
  --muted: #a9b6bd;
  --line: rgba(170, 199, 211, .18);
  --line-strong: rgba(170, 199, 211, .34);
  --signal: #55e6c1;
  --signal-dark: #0b9f87;
  --amber: #f2c66d;
  --red: #ff7b72;
  --violet: #c5a7ff;
  --blue: #84b9ff;
  --slate: #96a9b4;
  --shadow: 0 24px 80px rgba(0, 0, 0, .28);
  --radius-sm: 8px;
  --radius: 16px;
  --radius-lg: 28px;
  --shell: 1180px;
  --sans: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --mono: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
  --serif: Georgia, "Times New Roman", serif;
}

* { box-sizing: border-box; }
html { overflow-x: clip; scroll-behavior: smooth; scroll-padding-top: 96px; }
body {
  margin: 0;
  max-width: 100%;
  overflow-x: clip;
  color: var(--text);
  background: var(--ink-900);
  font-family: var(--sans);
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
}
body::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: -2;
  pointer-events: none;
  background:
    radial-gradient(circle at 15% 10%, rgba(85, 230, 193, .08), transparent 26rem),
    radial-gradient(circle at 86% 26%, rgba(132, 185, 255, .07), transparent 30rem),
    linear-gradient(180deg, var(--ink-900), var(--ink-950));
}
body::after {
  content: "";
  position: fixed;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  opacity: .18;
  background-image:
    linear-gradient(rgba(255,255,255,.055) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: linear-gradient(to bottom, black, transparent 80%);
}

img, svg { display: block; max-width: 100%; }
a { color: inherit; text-underline-offset: .18em; }
button, input, textarea, select { font: inherit; }
code, pre { font-family: var(--mono); }
:focus-visible { outline: 3px solid var(--amber); outline-offset: 4px; }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: clip; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
.shell { width: min(calc(100% - 40px), var(--shell)); margin-inline: auto; }
.shell > * { min-width: 0; }
.skip-link { position: fixed; top: 12px; left: 12px; z-index: 999; transform: translateY(-180%); padding: 10px 14px; border-radius: 8px; color: var(--ink-950); background: var(--signal); font-weight: 800; }
.skip-link:focus { transform: translateY(0); }

.site-header { position: sticky; top: 0; z-index: 50; border-bottom: 1px solid var(--line); background: rgba(5, 10, 14, .86); backdrop-filter: blur(18px); }
.header-row { min-height: 76px; display: grid; grid-template-columns: auto auto 1fr; align-items: center; gap: 24px; }
.brand { display: inline-flex; align-items: center; gap: 11px; width: fit-content; text-decoration: none; }
.brand-symbol { width: 42px; height: 42px; color: var(--signal); flex: 0 0 auto; }
.brand-wordmark { display: grid; line-height: 1.05; }
.brand-wordmark strong { font-size: 18px; letter-spacing: .06em; }
.brand-wordmark small { margin-top: 5px; color: var(--muted); font-size: 9px; letter-spacing: .12em; text-transform: uppercase; }
.header-status { display: inline-flex; align-items: center; gap: 8px; padding-left: 22px; border-left: 1px solid var(--line); color: var(--muted); font: 700 11px var(--mono); text-transform: uppercase; letter-spacing: .08em; }
.status-pulse { width: 8px; height: 8px; border-radius: 50%; background: var(--amber); box-shadow: 0 0 0 5px rgba(242, 198, 109, .1); }
.site-nav { display: flex; align-items: center; justify-content: flex-end; gap: 2px; }
.site-nav a { min-height: 42px; display: inline-flex; align-items: center; padding: 8px 9px; border-radius: 8px; color: var(--muted); text-decoration: none; font-size: 13px; font-weight: 720; }
.site-nav a:hover, .site-nav a[aria-current="page"] { color: var(--text); background: rgba(255,255,255,.06); }
.site-nav .nav-github { margin-left: 8px; padding-inline: 13px; color: var(--ink-950); background: var(--signal); }
.site-nav .nav-github:hover { color: var(--ink-950); background: #82f4d7; }
.nav-toggle { display: none; width: 46px; height: 46px; place-items: center; padding: 0; border: 1px solid var(--line-strong); border-radius: 12px; color: var(--text); background: var(--ink-800); cursor: pointer; }
.nav-toggle-lines { width: 20px; display: grid; gap: 6px; }
.nav-toggle-lines i { display: block; height: 2px; border-radius: 2px; background: currentColor; transition: transform .18s ease; }
.nav-toggle[aria-expanded="true"] .nav-toggle-lines i:first-child { transform: translateY(4px) rotate(45deg); }
.nav-toggle[aria-expanded="true"] .nav-toggle-lines i:last-child { transform: translateY(-4px) rotate(-45deg); }

.eyebrow { margin: 0 0 14px; color: var(--signal); font: 800 12px var(--mono); letter-spacing: .14em; text-transform: uppercase; }
h1, h2, h3 { margin-top: 0; line-height: 1.08; letter-spacing: -.035em; text-wrap: balance; }
h1 { font-size: clamp(46px, 6.3vw, 88px); }
h2 { font-size: clamp(32px, 4.2vw, 58px); }
h3 { font-size: clamp(19px, 2vw, 24px); }
p { margin-top: 0; }
p code, li code, td code { padding: .12em .34em; border: 1px solid rgba(85,230,193,.2); border-radius: 5px; color: #dffbf3; background: rgba(85,230,193,.08); overflow-wrap: anywhere; }
.section { padding: clamp(72px, 9vw, 132px) 0; }
.section-paper { color: #152028; background: var(--paper); }
.section-paper .eyebrow { color: #087e6b; }
.section-paper code { color: #145548; background: rgba(11,159,135,.08); border-color: rgba(11,159,135,.2); }
.section-ink { background: #03080c; border-block: 1px solid var(--line); }
.section-heading { max-width: 620px; }
.section-heading.wide { max-width: 880px; margin-bottom: 46px; }
.section-heading p:not(.eyebrow) { color: var(--muted); font-size: 18px; }
.section-paper .section-heading p:not(.eyebrow) { color: #52616a; }
.section-split { display: grid; grid-template-columns: .82fr 1.18fr; gap: clamp(38px, 8vw, 110px); align-items: start; }
.sticky-heading { position: sticky; top: 118px; }

.button { min-height: 50px; display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 11px 17px; border: 1px solid var(--line-strong); border-radius: 10px; text-decoration: none; font-weight: 800; }
.button.primary { color: var(--ink-950); border-color: var(--signal); background: var(--signal); }
.button.primary:hover { background: #80f5d7; }
.button.secondary { color: var(--text); background: rgba(255,255,255,.045); }
.button.quiet { color: var(--muted); background: transparent; }
.text-link { display: inline-flex; gap: 7px; align-items: center; color: var(--signal-dark); font-weight: 800; }
.hero-actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 30px; }

.home-hero { padding: clamp(62px, 8vw, 116px) 0 clamp(70px, 8vw, 110px); border-bottom: 1px solid var(--line); }
.home-hero-grid { display: grid; grid-template-columns: minmax(0, .95fr) minmax(420px, 1.05fr); gap: clamp(42px, 7vw, 92px); align-items: center; }
.hero-meta { display: flex; flex-wrap: wrap; gap: 10px 16px; align-items: center; margin-bottom: 24px; color: var(--muted); font: 700 12px var(--mono); }
.draft-badge { display: inline-flex; padding: 7px 10px; border: 1px solid rgba(242,198,109,.35); border-radius: 999px; color: var(--amber); background: rgba(242,198,109,.08); text-transform: uppercase; letter-spacing: .08em; }
.home-hero h1 { max-width: 11ch; margin-bottom: 24px; }
.hero-definition { max-width: 66ch; margin-bottom: 16px; padding-left: 18px; border-left: 3px solid var(--signal); color: #e9efed; font-size: clamp(18px, 2vw, 22px); }
.hero-support { max-width: 64ch; color: var(--muted); font-size: 16px; }
.hero-quickproof { display: flex; flex-wrap: wrap; gap: 10px 22px; margin-top: 34px; color: var(--muted); font-size: 13px; }
.hero-quickproof span { display: inline-flex; gap: 7px; align-items: baseline; }
.hero-quickproof strong { color: var(--signal); font: 800 18px var(--mono); }

.understanding-stage { position: relative; min-height: 610px; padding: 28px; border: 1px solid var(--line-strong); border-radius: var(--radius-lg); background: linear-gradient(145deg, rgba(16,31,42,.94), rgba(5,12,17,.98)); box-shadow: var(--shadow); overflow: clip; }
.understanding-stage::before { content: ""; position: absolute; inset: 0; pointer-events: none; background-image: linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px); background-size: 32px 32px; mask-image: linear-gradient(black, transparent); }
.stage-label { position: relative; margin-bottom: 22px; color: var(--amber); font: 800 11px var(--mono); letter-spacing: .14em; text-transform: uppercase; }
.stage-source, .stage-contract, .stage-checks, .stage-consumers { position: relative; }
.stage-source { display: flex; gap: 14px; align-items: center; padding: 14px 16px; border: 1px solid var(--line); border-radius: 12px; background: rgba(2,8,12,.68); }
.stage-index { display: grid; place-items: center; width: 32px; height: 32px; flex: 0 0 auto; border-radius: 50%; color: var(--ink-950); background: var(--signal); font: 800 11px var(--mono); }
.stage-source small, .stage-source code { display: block; }
.stage-source small { color: var(--muted); }
.stage-source code { margin-top: 3px; color: var(--text); overflow-wrap: anywhere; }
.stage-connector { height: 26px; position: relative; }
.stage-connector::before { content: ""; position: absolute; left: 31px; top: 0; bottom: 0; width: 1px; background: var(--signal); }
.stage-connector span { position: absolute; left: 27px; bottom: 1px; width: 9px; height: 9px; border-right: 2px solid var(--signal); border-bottom: 2px solid var(--signal); transform: rotate(45deg); }
.stage-contract { padding: 17px; border: 1px solid rgba(85,230,193,.42); border-radius: 16px; background: rgba(9,25,32,.95); box-shadow: inset 0 0 0 1px rgba(85,230,193,.06); }
.contract-header { display: flex; align-items: center; gap: 11px; margin-bottom: 15px; }
.contract-header strong { margin-right: auto; font-size: 14px; }
.contract-lines { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin-bottom: 15px; }
.contract-lines span { padding: 7px 8px; border-left: 2px solid var(--signal); color: #c4d1d6; background: rgba(255,255,255,.035); font: 700 10px var(--mono); }
.contract-fact { display: grid; grid-template-columns: 105px 1fr; gap: 8px; padding: 8px 0; border-top: 1px solid var(--line); font-size: 12px; }
.contract-fact code { color: var(--amber); }
.contract-fact span { color: #d8e2e5; overflow-wrap: anywhere; }
.stage-checks { display: grid; grid-template-columns: auto 1fr; gap: 2px 12px; margin: 22px 0; padding: 12px 15px; border: 1px dashed var(--line-strong); border-radius: 10px; color: var(--muted); }
.stage-checks > span { grid-row: 1 / 3; color: var(--signal); font: 800 12px var(--mono); }
.stage-checks strong { color: var(--text); font-size: 13px; }
.stage-checks em { font: normal 10px var(--mono); }
.stage-consumers { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.stage-consumers div { padding: 13px; border: 1px solid var(--line); border-radius: 12px; background: rgba(255,255,255,.03); }
.stage-consumers span, .stage-consumers strong { display: block; }
.stage-consumers span { color: var(--muted); font-size: 11px; }
.stage-consumers strong { margin-top: 3px; font-size: 13px; }

.proof-ribbon { border-bottom: 1px solid var(--line); background: rgba(255,255,255,.025); }
.proof-ribbon-grid { min-height: 78px; display: grid; grid-template-columns: repeat(4, 1fr) auto; align-items: center; gap: 16px; }
.proof-ribbon span { color: var(--muted); font-size: 13px; }
.proof-ribbon strong { margin-right: 5px; color: var(--text); font: 800 16px var(--mono); }
.proof-ribbon a { color: var(--signal); font-weight: 800; text-decoration: none; }

.problem-ledger { border-top: 1px solid var(--line); }
.problem-ledger article { display: grid; grid-template-columns: 58px 1fr; gap: 20px; padding: 28px 0; border-bottom: 1px solid var(--line); }
.problem-ledger article > span { color: var(--slate); font: 800 13px var(--mono); }
.problem-ledger h3 { margin-bottom: 8px; }
.problem-ledger p { margin: 0; color: var(--muted); }
.problem-ledger .problem-answer { margin-top: 18px; padding: 28px; border: 1px solid rgba(85,230,193,.3); border-radius: 14px; background: rgba(85,230,193,.055); }
.problem-ledger .problem-answer > span { color: var(--signal); }
.problem-ledger .problem-answer p { color: #d8e5e3; }

.protocol-rail { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; padding: 0; margin: 0; list-style: none; border: 1px solid rgba(21,32,40,.2); border-radius: 18px; overflow: clip; }
.protocol-rail li { position: relative; min-height: 250px; padding: 25px; border-right: 1px solid rgba(21,32,40,.16); }
.protocol-rail li:last-child { border-right: 0; }
.protocol-rail li::after { content: "→"; position: absolute; right: -10px; top: 30px; z-index: 2; display: grid; place-items: center; width: 20px; height: 20px; border-radius: 50%; color: var(--paper); background: #16232b; font-size: 11px; }
.protocol-rail li:last-child::after { display: none; }
.protocol-rail span { color: #087e6b; font: 800 13px var(--mono); }
.protocol-rail strong { display: block; margin: 34px 0 12px; font-size: 22px; line-height: 1.15; }
.protocol-rail p { color: #52616a; }

.core-spine { display: grid; grid-template-columns: repeat(5, 1fr); border: 1px solid var(--line); border-radius: 18px; overflow: clip; }
.core-node { min-height: 170px; display: grid; align-content: space-between; gap: 10px; padding: 18px; border-right: 1px solid var(--line); border-bottom: 1px solid var(--line); text-decoration: none; background: rgba(255,255,255,.025); }
.core-node:nth-child(5n) { border-right: 0; }
.core-node:nth-child(n+6) { border-bottom: 0; }
.core-node:hover { background: rgba(85,230,193,.055); }
.core-node[data-required="required"] { box-shadow: inset 0 3px 0 var(--signal); }
.core-node[data-required="optional"] { box-shadow: inset 0 3px 0 var(--line-strong); }
.core-node > span { color: var(--muted); font: 800 11px var(--mono); }
.core-node strong { font: 800 17px var(--mono); }
.core-node small { color: var(--muted); line-height: 1.35; }
.core-legend { display: flex; flex-wrap: wrap; gap: 22px; margin-top: 18px; color: var(--muted); font-size: 12px; }
.core-legend span { display: inline-flex; align-items: center; gap: 8px; }
.core-legend i { width: 18px; height: 3px; }
.legend-required { background: var(--signal); }
.legend-optional { background: var(--line-strong); }

.comparison-workbench { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.workbench-source { padding: 22px; border: 1px solid var(--line); border-radius: 16px; background: var(--ink-850); }
.workbench-source small, .workbench-source strong, .workbench-source code, .workbench-source span { display: block; }
.workbench-source small { color: var(--muted); font: 700 11px var(--mono); }
.workbench-source strong { margin: 18px 0 6px; font-size: 20px; }
.workbench-source code { color: var(--amber); font-size: 28px; }
.workbench-source span { margin-top: 14px; color: var(--muted); font-size: 13px; }
.workbench-engine { grid-column: 1 / -1; display: grid; grid-template-columns: 1fr 1fr 2fr; border: 1px solid rgba(85,230,193,.35); border-radius: 12px; overflow: clip; }
.workbench-engine span, .workbench-engine strong { padding: 13px; text-align: center; font: 700 12px var(--mono); }
.workbench-engine span { color: var(--muted); border-right: 1px solid var(--line); }
.workbench-engine strong { color: var(--ink-950); background: var(--signal); }
.workbench-outcomes { grid-column: 1 / -1; display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; }
.outcome { min-height: 105px; padding: 13px; border: 1px solid var(--line); border-radius: 10px; }
.outcome b, .outcome span { display: block; }
.outcome b { margin-bottom: 8px; font: 800 12px var(--mono); }
.outcome span { color: var(--muted); font-size: 11px; line-height: 1.4; }
.outcome-valid { border-color: rgba(85,230,193,.42)!important; background: rgba(85,230,193,.08)!important; }
.outcome-compatible { border-color: rgba(132,185,255,.42)!important; background: rgba(132,185,255,.08)!important; }
.outcome-unknown { border-color: rgba(150,169,180,.42)!important; background: rgba(150,169,180,.08)!important; }
.outcome-contested { border-color: rgba(242,198,109,.44)!important; background: rgba(242,198,109,.08)!important; }
.outcome-prohibited { border-color: rgba(255,123,114,.45)!important; background: rgba(255,123,114,.08)!important; }
.outcome-review { border-color: rgba(197,167,255,.45)!important; background: rgba(197,167,255,.08)!important; }
.outcome-deprecated { border-color: rgba(150,169,180,.35)!important; background: repeating-linear-gradient(135deg, rgba(150,169,180,.08), rgba(150,169,180,.08) 8px, transparent 8px, transparent 16px)!important; }
.outcome-inferred { border-color: rgba(132,185,255,.42)!important; background: rgba(132,185,255,.08)!important; }

.example-grid { display: grid; grid-template-columns: .75fr 1.25fr; gap: clamp(38px, 8vw, 100px); align-items: start; }
.code-frame { position: relative; min-width: 0; }
.code-block { width: 100%; max-width: 100%; margin: 0; padding: 24px; overflow-x: auto; border: 1px solid var(--line-strong); border-radius: 15px; color: #dce8e8; background: #03080c; font-size: 13px; line-height: 1.7; tab-size: 2; }
.code-block code { white-space: pre; }
.copy-button { position: absolute; top: 10px; right: 10px; z-index: 2; min-height: 34px; padding: 5px 10px; border: 1px solid var(--line-strong); border-radius: 7px; color: var(--text); background: rgba(15,29,40,.94); cursor: pointer; font-size: 12px; font-weight: 800; }
.section-paper .code-block { color: #dce8e8; }

.status-board { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
.status-lane { padding: 23px; border: 1px solid rgba(21,32,40,.18); border-radius: 14px; background: rgba(255,255,255,.42); }
.status-lane header { display: flex; gap: 10px; align-items: center; }
.status-lane header span { width: 9px; height: 9px; border-radius: 50%; }
.status-lane h3 { margin: 0; font-size: 19px; }
.status-lane p { margin: 18px 0 0; color: #52616a; }
.lane-now header span { background: var(--signal-dark); }
.lane-progress header span { background: #b27b13; }
.lane-planned header span { background: #6f8490; }
.lane-proof header span { background: #a34d47; }

.principles-layout { display: grid; grid-template-columns: .72fr 1.28fr; gap: clamp(38px, 8vw, 110px); }
.principle-list { border-top: 1px solid var(--line); }
.principle-list article { display: grid; grid-template-columns: 190px 1fr; gap: 30px; padding: 25px 0; border-bottom: 1px solid var(--line); }
.principle-list span { color: var(--signal); font: 800 12px var(--mono); text-transform: uppercase; letter-spacing: .08em; }
.principle-list p { margin: 0; color: var(--muted); }

.final-cta-box { display: grid; grid-template-columns: .78fr 1.22fr; gap: 22px 50px; padding: clamp(28px,5vw,54px); border: 1px solid var(--line-strong); border-radius: 22px; background: linear-gradient(135deg, rgba(85,230,193,.08), rgba(132,185,255,.04)); }
.final-cta-box .hero-actions { grid-column: 2; margin-top: 0; }

.page-hero { padding: clamp(76px, 9vw, 128px) 0 clamp(62px, 8vw, 104px); border-bottom: 1px solid var(--line); }
.page-hero-grid { display: grid; grid-template-columns: minmax(0, .95fr) minmax(360px, 1.05fr); gap: clamp(42px, 8vw, 108px); align-items: center; }
.page-hero h1 { max-width: 12ch; margin-bottom: 24px; }
.page-lead { max-width: 66ch; color: #c5d0d4; font-size: clamp(18px, 2vw, 22px); }
.hero-thesis { display: grid; grid-template-columns: 1fr auto 1fr; gap: 16px; align-items: center; padding: 30px; border: 1px solid var(--line-strong); border-radius: 22px; background: var(--ink-850); }
.hero-thesis span { padding: 16px; border: 1px solid var(--line); border-radius: 12px; text-align: center; font-weight: 850; }
.hero-thesis b { color: var(--red); font-size: 32px; }
.hero-thesis i { grid-column: 1 / -1; color: var(--signal); text-align: center; font: normal 12px var(--mono); }

.narrative-grid { display: grid; grid-template-columns: 190px 1fr; gap: 70px; }
.narrative-index { position: sticky; top: 112px; align-self: start; display: grid; gap: 9px; }
.narrative-index a { color: var(--muted); text-decoration: none; font: 700 11px var(--mono); text-transform: uppercase; }
.narrative-index a:hover { color: var(--signal); }
.narrative-flow { display: grid; gap: 0; }
.narrative-flow article { padding: 0 0 76px; margin-bottom: 76px; border-bottom: 1px solid var(--line); }
.narrative-flow article:last-child { margin-bottom: 0; border-bottom: 0; }
.narrative-flow h2 { max-width: 17ch; }
.narrative-flow p:not(.eyebrow) { max-width: 74ch; color: var(--muted); font-size: 18px; }
.contrast-line { display: grid; grid-template-columns: 120px 1fr 1fr; gap: 12px; align-items: center; margin-top: 28px; padding: 14px; border: 1px solid var(--line); border-radius: 12px; }
.contrast-line span { color: var(--signal); font: 800 11px var(--mono); text-transform: uppercase; }
.contrast-line strong { color: var(--muted); font-size: 13px; }
.before-after { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 30px; }
.before-after div { padding: 22px; border: 1px solid var(--line); border-radius: 14px; }
.before-after div:last-child { border-color: rgba(85,230,193,.38); background: rgba(85,230,193,.055); }
.before-after small, .before-after strong, .before-after span { display: block; }
.before-after small { color: var(--signal); font: 800 11px var(--mono); text-transform: uppercase; }
.before-after strong { margin: 16px 0 7px; }
.before-after span { color: var(--muted); font-size: 13px; }

.case-studies { display: grid; gap: 0; border-top: 1px solid var(--line); }
.case-studies article { display: grid; grid-template-columns: 80px 1fr; gap: 28px; padding: 34px 0; border-bottom: 1px solid var(--line); }
.case-number { color: var(--signal); font: 800 14px var(--mono); }
.case-studies h3 { margin-bottom: 14px; }
.case-studies p { color: var(--muted); }
.standards-matrix { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.standards-matrix div { min-height: 130px; display: grid; align-content: space-between; padding: 18px; border: 1px solid var(--line); border-radius: 12px; }
.standards-matrix span { color: var(--muted); }
.standards-matrix .matrix-aduc { color: var(--ink-950); border-color: var(--signal); background: var(--signal); }
.standards-matrix .matrix-aduc span { color: #14433a; }
.faq-layout { display: grid; grid-template-columns: .7fr 1.3fr; gap: 80px; }
.faq details { padding: 22px 0; border-top: 1px solid rgba(21,32,40,.2); }
.faq details:last-child { border-bottom: 1px solid rgba(21,32,40,.2); }
.faq summary { cursor: pointer; font-weight: 850; }
.faq p { margin: 14px 0 0; color: #52616a; }

.core-orbit { position: relative; min-height: 410px; display: grid; place-items: center; border: 1px solid var(--line-strong); border-radius: 50%; background: radial-gradient(circle, rgba(85,230,193,.1), transparent 58%); }
.orbit-center { display: grid; place-items: center; width: 140px; height: 140px; border-radius: 50%; color: var(--ink-950); background: var(--signal); text-align: center; font: 900 24px var(--mono); }
.orbit-center small { font: 700 10px var(--sans); text-transform: uppercase; }
.core-orbit > span { position: absolute; padding: 7px 10px; border: 1px solid var(--line); border-radius: 999px; color: var(--muted); background: var(--ink-850); font: 700 10px var(--mono); }
.core-orbit > span:nth-of-type(1) { top: 12%; left: 38%; }
.core-orbit > span:nth-of-type(2) { top: 25%; right: 9%; }
.core-orbit > span:nth-of-type(3) { top: 50%; right: 4%; }
.core-orbit > span:nth-of-type(4) { bottom: 18%; right: 13%; }
.core-orbit > span:nth-of-type(5) { bottom: 8%; left: 40%; }
.core-orbit > span:nth-of-type(6) { bottom: 19%; left: 9%; }
.core-orbit > span:nth-of-type(7) { top: 49%; left: 3%; }
.core-orbit > span:nth-of-type(8) { top: 24%; left: 10%; }
.minimum-envelope { display: grid; grid-template-columns: .7fr 1fr 1.2fr; gap: 20px; align-items: center; margin-bottom: 80px; padding: 22px; border: 1px solid var(--line-strong); border-radius: 14px; }
.minimum-envelope > span { color: var(--signal); font: 800 11px var(--mono); text-transform: uppercase; }
.minimum-envelope > strong { font-size: 19px; }
.minimum-envelope p { margin: 0; color: var(--muted); }
.core-detail-list { display: grid; }
.core-detail { display: grid; grid-template-columns: 230px 1fr; gap: 70px; padding: 50px 0; border-top: 1px solid var(--line); }
.core-detail-key { display: grid; align-content: start; gap: 9px; }
.core-detail-key span { color: var(--muted); font: 800 11px var(--mono); }
.core-detail-key code { color: var(--signal); font-size: 20px; }
.core-detail-key small { width: fit-content; padding: 4px 7px; border: 1px solid var(--line); border-radius: 999px; color: var(--muted); text-transform: uppercase; }
.core-detail h2 { margin-bottom: 12px; font-size: 36px; }
.core-detail p { color: var(--muted); }
.core-mini-example { width: fit-content; margin: 20px 0; padding: 10px 12px; border: 1px solid var(--line); border-radius: 8px; background: rgba(255,255,255,.03); }
.boundary-note { padding-left: 16px; border-left: 2px solid var(--amber); }
.boundary-layout { display: grid; grid-template-columns: .72fr 1.28fr; gap: 80px; }
.boundary-rules { border-top: 1px solid var(--line); }
.boundary-rules p { display: grid; grid-template-columns: 45px 1fr; gap: 16px; padding: 20px 0; margin: 0; border-bottom: 1px solid var(--line); color: var(--muted); }
.boundary-rules span { color: var(--signal); font: 800 11px var(--mono); }

.tool-terminal { padding: 18px; border: 1px solid var(--line-strong); border-radius: 18px; background: #02070a; box-shadow: var(--shadow); }
.tool-terminal .code-block { border: 0; padding: 42px 16px 20px; background: transparent; white-space: pre-wrap; }
.terminal-result { display: grid; grid-template-columns: auto 1fr; gap: 2px 9px; padding: 14px; border-top: 1px solid var(--line); }
.result-dot { grid-row: 1/3; width: 10px; height: 10px; margin-top: 5px; border-radius: 50%; background: var(--signal); }
.terminal-result small { color: var(--muted); }
.command-grid, .report-grid { display: grid; grid-template-columns: .7fr 1.3fr; gap: 80px; align-items: start; }
.validation-pipeline { padding: 0; margin: 0; list-style: none; border-top: 1px solid rgba(21,32,40,.2); }
.validation-pipeline li { display: grid; grid-template-columns: 72px 1fr; gap: 24px; padding: 24px 0; border-bottom: 1px solid rgba(21,32,40,.2); }
.validation-pipeline span { color: #087e6b; font: 800 12px var(--mono); }
.validation-pipeline strong { display: block; margin-bottom: 5px; font-size: 20px; }
.validation-pipeline p { margin: 0; color: #52616a; }
.boundary-strip { display: grid; grid-template-columns: repeat(4, 1fr); border: 1px solid var(--line); border-radius: 14px; overflow: clip; }
.boundary-strip span { min-height: 100px; display: grid; place-items: center; padding: 15px; border-right: 1px solid var(--line); color: var(--muted); text-align: center; font-weight: 800; }
.boundary-strip span:last-child { border-right: 0; }

.compare-signal { display: grid; grid-template-columns: 1fr auto 1fr; gap: 18px; align-items: center; }
.compare-signal div { min-height: 190px; display: grid; align-content: center; padding: 22px; border: 1px solid var(--line); border-radius: 16px; background: var(--ink-850); }
.compare-signal small, .compare-signal strong, .compare-signal span { display: block; }
.compare-signal small { color: var(--signal); font: 800 11px var(--mono); text-transform: uppercase; }
.compare-signal strong { margin: 13px 0; font-size: 23px; }
.compare-signal span { color: var(--muted); font-size: 12px; }
.compare-signal i { color: var(--red); font: normal 36px var(--serif); }
.assessment-spectrum { display: flex; flex-wrap: wrap; gap: 9px; }
.assessment-spectrum span, .state-vocabulary span { padding: 10px 13px; border: 1px solid rgba(21,32,40,.2); border-radius: 999px; font: 800 12px var(--mono); }
.compare-explanation { display: grid; grid-template-columns: .7fr 1.3fr; gap: 80px; }
.compare-rules { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.compare-rules article { padding: 22px; border: 1px solid var(--line); border-radius: 12px; }
.compare-rules span { color: var(--signal); font: 800 11px var(--mono); text-transform: uppercase; }
.compare-rules p { margin: 16px 0 0; color: var(--muted); }
.change-cases { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.change-cases > div { padding: 20px; border: 1px solid var(--line); border-radius: 12px; }
.change-cases code, .change-cases strong, .change-cases span { display: block; width: fit-content; }
.change-cases strong { margin: 14px 0; }
.change-cases p { margin: 15px 0 0; color: var(--muted); }
.state-chip { display: inline-flex; padding: 4px 8px; border: 1px solid var(--line); border-radius: 999px; font: 800 10px var(--mono); white-space: nowrap; }
.state-valid { color: var(--signal); border-color: rgba(85,230,193,.4); background: rgba(85,230,193,.08); }
.state-review { color: var(--violet); border-color: rgba(197,167,255,.4); background: rgba(197,167,255,.08); }
.state-prohibited { color: var(--red); border-color: rgba(255,123,114,.4); background: rgba(255,123,114,.08); }

.architecture-stack { display: grid; padding: 20px; border: 1px solid var(--line-strong); border-radius: 18px; background: var(--ink-850); }
.architecture-stack span { margin-top: 12px; color: var(--signal); font: 800 10px var(--mono); text-transform: uppercase; }
.architecture-stack strong { padding: 12px 14px; border-left: 3px solid var(--signal); background: rgba(255,255,255,.035); }
.architecture-lanes { display: grid; }
.architecture-lanes article { display: grid; grid-template-columns: 80px 1fr auto; gap: 28px; align-items: start; padding: 32px 0; border-top: 1px solid var(--line); }
.architecture-lanes > article > span { color: var(--signal); font: 800 12px var(--mono); }
.architecture-lanes h2 { margin-bottom: 8px; font-size: 32px; }
.architecture-lanes p { margin: 0; color: var(--muted); }
.architecture-lanes a { color: var(--signal); }
.architecture-lanes .future { opacity: .78; }

.trust-seal { width: min(100%, 390px); aspect-ratio: 1; display: grid; place-items: center; align-content: center; margin-inline: auto; border: 1px solid var(--line-strong); border-radius: 50%; background: radial-gradient(circle, rgba(150,169,180,.12), transparent 62%); }
.trust-seal::before, .trust-seal::after { content: ""; position: absolute; border-radius: 50%; }
.trust-seal strong { font: 900 clamp(34px,5vw,58px) var(--mono); letter-spacing: -.06em; }
.trust-seal span { color: var(--slate); }
.trust-seal i { margin-top: 18px; padding: 6px 9px; border: 1px solid var(--line); border-radius: 999px; color: var(--amber); font: normal 10px var(--mono); }
.trust-principles { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.trust-principles article { min-height: 260px; padding: 24px; border: 1px solid var(--line); border-radius: 14px; background: rgba(255,255,255,.025); }
.trust-principles > article > span { color: var(--signal); font: 800 11px var(--mono); }
.trust-principles h2 { margin: 50px 0 12px; font-size: 26px; }
.trust-principles p { color: var(--muted); }
.state-vocabulary { display: flex; flex-wrap: wrap; gap: 10px; }

.evidence-counter { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.evidence-counter div { min-height: 135px; display: grid; align-content: center; padding: 18px; border: 1px solid var(--line); border-radius: 12px; }
.evidence-counter strong { color: var(--signal); font: 900 42px var(--mono); }
.evidence-counter span { color: var(--muted); }
.evidence-timeline { display: grid; }
.evidence-timeline article { display: grid; grid-template-columns: 70px 1fr auto; gap: 24px; align-items: center; padding: 30px 0; border-top: 1px solid var(--line); }
.evidence-timeline > article > span { color: var(--signal); font: 800 12px var(--mono); }
.evidence-timeline h2 { margin-bottom: 7px; font-size: 30px; }
.evidence-timeline p { margin: 0; color: var(--muted); }
.evidence-timeline a { color: var(--signal); font-weight: 800; }
.proof-boundary { display: grid; grid-template-columns: 1fr .8fr; gap: 80px; align-items: start; }
.proof-boundary p { color: #52616a; }
.proof-checklist { display: grid; gap: 8px; }
.proof-checklist span { padding: 14px; border-left: 3px solid #a34d47; background: rgba(163,77,71,.07); font-weight: 750; }

.roadmap-now { padding: 24px; border: 1px solid rgba(242,198,109,.4); border-radius: 16px; background: rgba(242,198,109,.07); }
.roadmap-now small, .roadmap-now strong, .roadmap-now span { display: block; }
.roadmap-now small { color: var(--amber); font: 800 11px var(--mono); text-transform: uppercase; }
.roadmap-now strong { margin: 18px 0 8px; font-size: 24px; }
.roadmap-now span { color: var(--muted); }
.roadmap-track { display: grid; }
.roadmap-track article { display: grid; grid-template-columns: 100px 1fr 150px; gap: 26px; align-items: center; padding: 30px 0; border-top: 1px solid var(--line); }
.roadmap-track > article > span { color: var(--muted); font: 800 12px var(--mono); }
.roadmap-track h2 { margin-bottom: 7px; font-size: 30px; }
.roadmap-track p { margin: 0; color: var(--muted); }
.roadmap-track > article > strong { text-align: right; font: 800 12px var(--mono); text-transform: uppercase; }
.roadmap-track .complete > strong { color: var(--signal); }
.roadmap-track .active > strong { color: var(--amber); }
.roadmap-track .blocked > strong { color: var(--red); }

.quickstart-steps { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.quickstart-steps span { padding: 15px; border: 1px solid var(--line); border-radius: 10px; color: var(--muted); font: 800 12px var(--mono); }
.docs-flow { display: grid; }
.docs-flow article { display: grid; grid-template-columns: 80px 1fr; gap: 28px; padding: 38px 0; border-top: 1px solid var(--line); }
.docs-flow > article > span { color: var(--signal); font: 800 12px var(--mono); }
.docs-flow h2 { font-size: 30px; }
.tool-index { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.tool-index code { padding: 14px; border: 1px solid rgba(21,32,40,.18); border-radius: 8px; color: #145548; background: rgba(11,159,135,.06); overflow-wrap: anywhere; }

.example-summary { display: grid; grid-template-columns: auto 1fr; gap: 8px 20px; padding: 22px; border: 1px solid var(--line); border-radius: 16px; }
.example-summary span { color: var(--muted); font: 700 11px var(--mono); }
.example-summary strong { overflow-wrap: anywhere; }
.spec-mark { min-height: 320px; display: grid; place-items: center; align-content: center; border: 1px solid var(--line-strong); border-radius: 50%; background: radial-gradient(circle, rgba(85,230,193,.11), transparent 62%); }
.spec-mark strong { color: var(--signal); font: 900 70px var(--mono); }
.spec-mark span, .spec-mark small { display: block; }
.spec-mark span { font-weight: 800; }
.spec-mark small { margin-top: 8px; color: var(--muted); }
.spec-directory { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.spec-directory a { min-height: 190px; display: grid; align-content: space-between; padding: 22px; border: 1px solid var(--line); border-radius: 14px; text-decoration: none; }
.spec-directory a:hover { border-color: var(--signal); background: rgba(85,230,193,.045); }
.spec-directory span { color: var(--signal); font: 800 11px var(--mono); text-transform: uppercase; }
.spec-directory strong { margin: 24px 0 8px; font-size: 21px; }
.spec-directory small { color: var(--muted); }
.not-found h1 { max-width: 14ch; }
.link-rail { display: flex; flex-wrap: wrap; gap: 10px; }
.link-rail a { padding: 12px 15px; border: 1px solid var(--line); border-radius: 9px; text-decoration: none; }

.site-footer { padding: 78px 0 28px; border-top: 1px solid var(--line); background: #03080c; }
.footer-callout { display: flex; justify-content: space-between; gap: 40px; align-items: end; padding-bottom: 58px; margin-bottom: 44px; border-bottom: 1px solid var(--line); }
.footer-callout h2 { max-width: 16ch; margin-bottom: 0; }
.footer-actions { display: flex; flex-wrap: wrap; gap: 10px; }
.footer-grid { display: grid; grid-template-columns: 1.45fr repeat(3, .65fr); gap: 42px; }
.footer-intro p { max-width: 42ch; margin-top: 20px; color: var(--muted); }
.footer-grid h2 { margin-bottom: 14px; color: var(--text); font: 800 11px var(--mono); text-transform: uppercase; letter-spacing: .12em; }
.footer-grid > div:not(.footer-intro) a { display: block; width: fit-content; margin: 9px 0; color: var(--muted); text-decoration: none; }
.footer-grid a:hover { color: var(--signal); }
.footer-bottom { display: flex; justify-content: space-between; gap: 20px; padding-top: 24px; margin-top: 44px; border-top: 1px solid var(--line); color: var(--muted); font-size: 12px; }

@media(max-width:1080px) {
  .header-status { display: none; }
  .header-row { grid-template-columns: auto 1fr; }
  .home-hero-grid, .page-hero-grid { grid-template-columns: 1fr; }
  .understanding-stage { min-height: auto; }
  .proof-ribbon-grid { grid-template-columns: repeat(2, 1fr); padding-block: 18px; }
  .proof-ribbon a { grid-column: 1 / -1; }
  .core-spine { grid-template-columns: repeat(2, 1fr); }
  .core-node:nth-child(n) { border-right: 1px solid var(--line); border-bottom: 1px solid var(--line); }
  .core-node:nth-child(2n) { border-right: 0; }
  .core-node:nth-last-child(-n+2) { border-bottom: 0; }
  .workbench-outcomes { grid-template-columns: repeat(3, 1fr); }
  .trust-principles { grid-template-columns: 1fr 1fr; }
}

@media(max-width:900px) {
  .js .nav-toggle { display: grid; justify-self: end; }
  .header-row { grid-template-columns: 1fr auto; min-height: 68px; gap: 14px; }
  .brand-symbol { width: 38px; height: 38px; }
  .brand-wordmark small { display: none; }
  .site-nav { grid-column: 1 / -1; display: grid; grid-template-columns: 1fr 1fr; gap: 4px; padding: 8px 0 18px; }
  .js .site-nav { position: fixed; top: 68px; left: 0; right: 0; max-height: calc(100dvh - 68px); overflow-y: auto; padding: 18px 20px 28px; border-bottom: 1px solid var(--line-strong); background: rgba(5,10,14,.98); box-shadow: 0 20px 60px rgba(0,0,0,.42); transform: translateY(-120%); visibility: hidden; transition: transform .2s ease, visibility .2s ease; }
  .js .site-nav[data-open="true"] { transform: translateY(0); visibility: visible; }
  .site-nav a { min-height: 48px; padding: 11px 13px; border: 1px solid transparent; font-size: 15px; }
  .site-nav a:hover, .site-nav a[aria-current="page"] { border-color: var(--line); }
  .site-nav .nav-github { grid-column: 1 / -1; justify-content: center; margin: 8px 0 0; }
  body.nav-open { overflow: clip; }
  .section-split, .principles-layout, .command-grid, .report-grid, .compare-explanation, .boundary-layout, .faq-layout, .proof-boundary, .example-grid, .final-cta-box { grid-template-columns: 1fr; }
  .sticky-heading, .narrative-index { position: static; }
  .narrative-grid { grid-template-columns: 1fr; gap: 32px; }
  .narrative-index { display: flex; flex-wrap: wrap; }
  .protocol-rail { grid-template-columns: 1fr 1fr; }
  .protocol-rail li:nth-child(2) { border-right: 0; }
  .protocol-rail li:nth-child(-n+2) { border-bottom: 1px solid rgba(21,32,40,.16); }
  .protocol-rail li:nth-child(2)::after { display: none; }
  .minimum-envelope { grid-template-columns: 1fr; }
  .core-detail { grid-template-columns: 150px 1fr; gap: 40px; }
  .final-cta-box .hero-actions { grid-column: 1; }
  .footer-grid { grid-template-columns: 1fr 1fr; }
}

@media(max-width:700px) {
  .shell { width: min(calc(100% - 28px), var(--shell)); }
  .site-nav { grid-template-columns: 1fr; }
  .site-nav .nav-github { grid-column: auto; }
  h1 { font-size: clamp(40px, 12vw, 58px); line-height: 1.02; }
  h2 { font-size: clamp(30px, 9vw, 44px); }
  .section { padding: 72px 0; }
  .home-hero { padding: 50px 0 72px; }
  .hero-meta { margin-bottom: 18px; }
  .home-hero h1 { max-width: 12ch; }
  .hero-definition { font-size: 17px; }
  .hero-actions { display: grid; grid-template-columns: 1fr; }
  .button { width: 100%; }
  .hero-quickproof { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .understanding-stage { padding: 18px; border-radius: 18px; }
  .contract-lines { grid-template-columns: 1fr 1fr; }
  .contract-fact { grid-template-columns: 1fr; }
  .stage-consumers { grid-template-columns: 1fr; }
  .proof-ribbon-grid { grid-template-columns: 1fr 1fr; gap: 10px; }
  .proof-ribbon span { padding: 6px 0; }
  .problem-ledger article { grid-template-columns: 38px 1fr; gap: 12px; }
  .problem-ledger .problem-answer { padding: 20px; }
  .protocol-rail { grid-template-columns: 1fr; border-radius: 14px; }
  .protocol-rail li { min-height: auto; border-right: 0; border-bottom: 1px solid rgba(21,32,40,.16); }
  .protocol-rail li::after { display: none; }
  .protocol-rail li:last-child { border-bottom: 0; }
  .protocol-rail strong { margin-top: 22px; }
  .core-spine { grid-template-columns: 1fr 1fr; }
  .core-node { min-height: 145px; padding: 14px; }
  .comparison-workbench { grid-template-columns: 1fr; }
  .workbench-engine, .workbench-outcomes { grid-column: auto; }
  .workbench-engine { grid-template-columns: 1fr; }
  .workbench-engine span { border-right: 0; border-bottom: 1px solid var(--line); }
  .workbench-outcomes { grid-template-columns: 1fr 1fr; }
  .outcome { min-height: 92px; }
  .code-block { padding: 20px 16px; font-size: 11px; }
  .code-block code { white-space: pre; }
  .status-board { grid-template-columns: 1fr; }
  .principle-list article { grid-template-columns: 1fr; gap: 8px; }
  .footer-callout { display: grid; align-items: start; }
  .footer-actions { display: grid; }
  .footer-grid { grid-template-columns: 1fr 1fr; gap: 32px 20px; }
  .footer-intro { grid-column: 1 / -1; }
  .footer-bottom { flex-direction: column; }
  .hero-thesis, .compare-signal { grid-template-columns: 1fr; }
  .hero-thesis b, .compare-signal i { transform: rotate(90deg); text-align: center; }
  .contrast-line { grid-template-columns: 1fr; }
  .before-after, .standards-matrix { grid-template-columns: 1fr; }
  .case-studies article { grid-template-columns: 42px 1fr; gap: 14px; }
  .core-orbit { min-height: 330px; }
  .orbit-center { width: 110px; height: 110px; }
  .core-orbit > span { font-size: 8px; padding: 5px 7px; }
  .core-detail { grid-template-columns: 1fr; gap: 18px; padding: 38px 0; }
  .core-detail-key { display: flex; flex-wrap: wrap; align-items: center; }
  .boundary-strip { grid-template-columns: 1fr 1fr; }
  .boundary-strip span { min-height: 80px; border-bottom: 1px solid var(--line); }
  .boundary-strip span:nth-child(2n) { border-right: 0; }
  .assessment-spectrum { display: grid; grid-template-columns: 1fr 1fr; }
  .compare-rules, .change-cases, .trust-principles, .evidence-counter, .quickstart-steps, .tool-index, .spec-directory { grid-template-columns: 1fr; }
  .architecture-lanes article, .evidence-timeline article, .roadmap-track article { grid-template-columns: 50px 1fr; gap: 14px; }
  .architecture-lanes article > a, .evidence-timeline article > a, .roadmap-track article > strong { grid-column: 2; text-align: left; }
  .docs-flow article { grid-template-columns: 40px 1fr; gap: 12px; }
}

@media(max-width:390px) {
  .shell { width: min(calc(100% - 24px), var(--shell)); }
  h1 { font-size: clamp(38px, 11.4vw, 48px); }
  .brand-wordmark strong { font-size: 16px; }
  .hero-quickproof { grid-template-columns: 1fr; }
  .core-spine { grid-template-columns: 1fr; }
  .core-node:nth-child(n) { border-right: 0; border-bottom: 1px solid var(--line); }
  .core-node:last-child { border-bottom: 0; }
  .workbench-outcomes { grid-template-columns: 1fr; }
  .footer-grid { grid-template-columns: 1fr; }
  .footer-intro { grid-column: auto; }
  .assessment-spectrum { grid-template-columns: 1fr; }
}

@media(prefers-reduced-motion:reduce) {
  *, *::before, *::after { scroll-behavior: auto!important; animation-duration: .01ms!important; animation-iteration-count: 1!important; transition-duration: .01ms!important; }
}
"""

JS = r"""
(() => {
  const toggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-site-nav]');
  const header = document.querySelector('[data-site-header]');
  let lastFocused = null;

  const navLinks = nav ? Array.from(nav.querySelectorAll('a')) : [];

  function setNavigation(open, { returnFocus = false } = {}) {
    if (!toggle || !nav) return;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.querySelector('.sr-only').textContent = open ? 'Close navigation' : 'Open navigation';
    nav.dataset.open = String(open);
    document.body.classList.toggle('nav-open', open);

    if (open) {
      lastFocused = document.activeElement;
      window.requestAnimationFrame(() => navLinks[0]?.focus());
    } else if (returnFocus && lastFocused instanceof HTMLElement) {
      lastFocused.focus();
    }
  }

  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    setNavigation(open, { returnFocus: !open });
  });

  navLinks.forEach((link) => link.addEventListener('click', () => setNavigation(false)));

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && toggle?.getAttribute('aria-expanded') === 'true') {
      setNavigation(false, { returnFocus: true });
    }
  });

  document.addEventListener('pointerdown', (event) => {
    if (!header || toggle?.getAttribute('aria-expanded') !== 'true') return;
    if (!header.contains(event.target)) setNavigation(false, { returnFocus: true });
  });

  const desktop = window.matchMedia('(min-width: 901px)');
  desktop.addEventListener?.('change', (event) => {
    if (event.matches) setNavigation(false);
  });

  document.querySelectorAll('[data-copy-target]').forEach((button) => {
    button.addEventListener('click', async () => {
      const target = document.querySelector(button.getAttribute('data-copy-target'));
      if (!target) return;
      const original = button.textContent;
      try {
        await navigator.clipboard.writeText(target.textContent || '');
        button.textContent = 'Copied';
      } catch {
        button.textContent = 'Copy unavailable';
      }
      window.setTimeout(() => { button.textContent = original; }, 1400);
    });
  });
})();
"""


def write(relative: str, content: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def main() -> None:
    for path, (title, description, kind, body) in PAGES.items():
        write(path, render_page(path, title, description, kind, body))
    write("404.html", render_page("404.html", "Page not found — ADUC", "The requested ADUC page could not be found.", "WebPage", NOT_FOUND))
    write("assets/styles.css", CSS)
    write("assets/app.js", JS)
    write("assets/site-data.json", json.dumps(SITE_DATA, indent=2, ensure_ascii=False))
    write(".nojekyll", "")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
    sitemap_paths = list(PAGES)
    urls = "\n".join(f"  <url><loc>{page_url(path)}</loc><lastmod>{UPDATED}</lastmod></url>" for path in sitemap_paths)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>')
    write("README.md", f"""# ADUC public website

Static, dependency-free public website for the ADUC Working Draft.

Canonical public URL: {BASE}

The generator centralizes navigation, metadata and repeated project facts:

```bash
python website/build_site.py
python tools/validate_website.py
python -m unittest discover -s tests/website -p "test_*.py"
```

Visual release evidence must cover 360×800, 390×844, 768×1024, 1024×768, 1440×900 and 1920×1080 before a redesign PR may be merged.
""")


if __name__ == "__main__":
    main()
