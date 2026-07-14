#!/usr/bin/env python3
"""Generate the static ADUC public website pages."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = "https://bacoul.github.io/AI-Data-Understanding-Core-ADUC/"
UPDATED = "2026-07-14"

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
        "review interface",
        "public packages",
        "production registry",
        "MCP adapter",
        "official extensions",
        "external two-consumer proof",
    ],
}


def page_url(path: str) -> str:
    return BASE if path == "index.html" else f"{BASE}{path}"


def json_ld(title: str, path: str, kind: str) -> str:
    data = [
        {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "AI Data Understanding Core",
            "alternateName": "ADUC",
            "url": BASE,
            "sameAs": ["https://github.com/BACOUL/AI-Data-Understanding-Core-ADUC"],
        },
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "ADUC",
            "url": BASE,
            "description": "Working Draft documentation for AI-readable data understanding contracts.",
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": title,
                    "item": page_url(path),
                },
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": kind,
            "headline": title,
            "url": page_url(path),
            "dateModified": UPDATED,
            "isAccessibleForFree": True,
            "about": [
                "AI data interoperability",
                "AI-readable data contract",
                "portable data understanding",
                "semantic interoperability for AI",
                "deterministic AI data validation",
                "AI data provenance",
                "multi-model data consistency",
            ],
        },
    ]
    return json.dumps(data, indent=2)


def head(title: str, description: str, path: str, kind: str) -> str:
    url = page_url(path)
    return f"""<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#0b0e12">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="ADUC">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <link rel="stylesheet" href="assets/styles.css">
  <script defer src="assets/app.js"></script>
  <script type="application/ld+json">{json_ld(title, path, kind)}</script>
</head>"""


def header(current: str) -> str:
    links = []
    for href, label in NAV:
        current_attr = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{href}"{current_attr}>{label}</a>')
    links.append(
        '<a class="nav-github" href="https://github.com/BACOUL/'
        'AI-Data-Understanding-Core-ADUC">GitHub</a>'
    )
    nav = "\n        ".join(links)
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="shell nav-shell">
    <a class="brand" href="index.html" aria-label="ADUC home">
      <span class="brand-mark" aria-hidden="true">AD</span>
      <span class="brand-copy">ADUC<span>Working Draft 0.1</span></span>
    </a>
    <nav class="site-nav" aria-label="Primary navigation">
        {nav}
    </nav>
  </div>
</header>"""


def footer() -> str:
    return """<footer class="site-footer">
  <div class="shell footer-grid">
    <section>
      <a class="brand footer-brand" href="index.html">
        <span class="brand-mark" aria-hidden="true">AD</span>
        <span class="brand-copy">ADUC<span>AI Data Understanding Core</span></span>
      </a>
      <p>ADUC is a Working Draft. It is not yet a recognized standard, does not grant legal permission, and does not prove universal interoperability.</p>
    </section>
    <section>
      <h2>Reference</h2>
      <a href="core.html">Core model</a>
      <a href="validate.html">Validation</a>
      <a href="compare.html">Comparison</a>
      <a href="architecture.html">Architecture</a>
    </section>
    <section>
      <h2>Evidence</h2>
      <a href="evidence.html">Conformance evidence</a>
      <a href="roadmap.html">Roadmap</a>
      <a href="example.html">Core example</a>
      <a href="docs.html">Try in 5 minutes</a>
    </section>
    <section>
      <h2>Governance</h2>
      <a href="https://github.com/BACOUL/AI-Data-Understanding-Core-ADUC/blob/main/GOVERNANCE.md">Governance</a>
      <a href="https://github.com/BACOUL/AI-Data-Understanding-Core-ADUC/blob/main/SECURITY.md">Security</a>
      <a href="https://github.com/BACOUL/AI-Data-Understanding-Core-ADUC/blob/main/LICENSES.md">Licensing</a>
    </section>
  </div>
  <div class="shell footer-bottom">
    <span>Updated 2026-07-14. Canonical public URL: GitHub Pages.</span>
    <span>Provider-neutral, local-first, unknown-safe.</span>
  </div>
</footer>"""


PAGES = {
    "index.html": {
        "title": "ADUC - Portable data understanding for AI systems",
        "description": "ADUC is a Working Draft machine-readable contract for portable data understanding, deterministic validation and deterministic comparison across AI systems.",
        "kind": "WebSite",
        "body": r"""
<section class="hero split-hero">
  <div class="shell hero-grid">
    <div class="hero-copy">
      <p class="kicker">Working Draft 0.1 - AI-readable data contract</p>
      <h1>Data that carries its understanding with it.</h1>
      <p class="lead definition">ADUC is a machine-readable contract that makes a data resource's structure, meaning, context, identity, provenance, uncertainty, relations and use conditions explicit, validatable and portable across AI systems.</p>
      <div class="hero-actions" aria-label="Primary actions">
        <a class="button primary" href="docs.html">Try in 5 minutes</a>
        <a class="button secondary" href="validate.html">See validation</a>
        <a class="button ghost" href="https://github.com/BACOUL/AI-Data-Understanding-Core-ADUC">GitHub</a>
      </div>
      <div class="status-ledger" aria-label="Current implementation status">
        <span><strong>Available:</strong> 10 Core blocks, 14 schemas, full-Core validator, deterministic comparator, semantic-profile migration</span>
        <span><strong>Active task:</strong> deterministic Core contract formatter</span>
        <span><strong>Not proven:</strong> external two-consumer interoperability claim</span>
      </div>
      <pre class="home-command"><code>python tools/aduc_core.py validate examples/core/complete-model.example.json</code></pre>
    </div>
    <div class="hero-instrument" aria-label="ADUC portable understanding flow">
      <div class="contract-flow">
        <div><span>Original data</span><code>{"flow": 1.5}</code></div>
        <div><span>ADUC understanding contract</span><code>conceptIri + unitIri + provenance + policy</code></div>
        <div><span>Deterministic validation and comparison</span><code>valid / unknown / prohibited / review</code></div>
        <div><span>Portable understanding across AI systems</span><code>same explicit contract, same rules</code></div>
      </div>
    </div>
  </div>
</section>
<section class="section-band" aria-labelledby="problem">
  <div class="shell two-column">
    <div><p class="kicker">The problem</p><h2 id="problem">AI can read bytes without sharing meaning.</h2></div>
    <div class="answer-block">
      <p>JSON and CSV expose syntax. Prompts, ETL jobs, connectors, spreadsheets and private mappings often carry the real interpretation: which field is a flow rate, what unit it uses, which timestamp role applies, who asserted it, whether identity is exact, and whether the data may be used for the requested purpose.</p>
      <p>ADUC moves that understanding out of hidden glue and into a versioned contract that can be validated, compared and reviewed.</p>
    </div>
  </div>
</section>
<section aria-labelledby="four-steps">
  <div class="shell">
    <div class="section-head">
      <p class="kicker">The promise</p>
      <h2 id="four-steps">Original data -> ADUC contract -> deterministic checks -> portable understanding.</h2>
      <p>ADUC accompanies the original resource. It does not replace the source data, become an AI model, or grant legal permission.</p>
    </div>
    <ol class="trace-steps">
      <li><strong>Original data</strong><span>The source stays authoritative and unchanged.</span></li>
      <li><strong>ADUC understanding contract</strong><span>Structure, semantics, identity, context, provenance, uncertainty, relations and policy travel together.</span></li>
      <li><strong>Deterministic validation and comparison</strong><span>Local schemas, architecture checks, profile evaluators and stable reports expose what is valid, unknown or unsafe.</span></li>
      <li><strong>Portable understanding across AI systems</strong><span>Multiple consumers can receive the same description and be evaluated by the same rules.</span></li>
    </ol>
  </div>
</section>
<section class="section-band" aria-labelledby="core-dimensions">
  <div class="shell">
    <div class="section-head compact"><p class="kicker">Core model</p><h2 id="core-dimensions">Ten dimensions, one explicit contract.</h2></div>
    <div class="core-map" role="list" aria-label="ADUC Core blocks">
      <a href="core.html#aduc" role="listitem">aduc<span>contract metadata</span></a>
      <a href="core.html#resource" role="listitem">resource<span>the described data</span></a>
      <a href="core.html#structure" role="listitem">structure<span>records and fields</span></a>
      <a href="core.html#semantics" role="listitem">semantics<span>meaning and mappings</span></a>
      <a href="core.html#identity" role="listitem">identity<span>entities and identifiers</span></a>
      <a href="core.html#context" role="listitem">context<span>time, space, operation</span></a>
      <a href="core.html#provenance" role="listitem">provenance<span>agents and evidence</span></a>
      <a href="core.html#uncertainty" role="listitem">uncertainty<span>quality and unknowns</span></a>
      <a href="core.html#relations" role="listitem">relations<span>graph assertions</span></a>
      <a href="core.html#policy" role="listitem">policy<span>use conditions</span></a>
    </div>
  </div>
</section>
<section aria-labelledby="today">
  <div class="shell two-column">
    <div><p class="kicker">What exists today</p><h2 id="today">The repository now contains complete Core foundations.</h2></div>
    <div class="status-columns">
      <div class="state-panel available"><h3>Available now</h3><ul><li>Normative ten-block Core model</li><li>Minimum envelope: <code>aduc + resource + structure</code></li><li>14 local Draft 2020-12 schemas</li><li>11 valid and 15 invalid Core fixtures</li><li>Unified full-Core validator</li><li>Deterministic full-Core comparator</li><li>Deterministic semantic-profile migration</li><li>24 comparison scenarios</li><li>Local processing without unapproved remote resolution</li></ul></div>
      <div class="state-panel progress"><h3>In progress</h3><ul><li>Deterministic formatting for complete Core contracts, with byte stability and no semantic repair.</li></ul></div>
      <div class="state-panel planned"><h3>Planned, not available</h3><ul><li>JSON/CSV compiler</li><li>Review interface</li><li>Stabilized public PyPI/npm packages</li><li>Production registry and MCP adapter</li><li>Official extensions</li><li>External two-consumer proof</li></ul></div>
    </div>
  </div>
</section>
<section class="section-band" aria-labelledby="core-example">
  <div class="shell example-layout">
    <div>
      <p class="kicker">Conformant Core excerpt</p>
      <h2 id="core-example">A real contract names the field, the concept, the unit and the evidence boundary.</h2>
      <p>This excerpt is adapted from <code>examples/core/complete-model.example.json</code>. It uses the official Core shape, including <code>conceptIri</code> and <code>unitIri</code>.</p>
      <a class="button secondary" href="example.html">Open the annotated example</a>
    </div>
    <pre class="code-block"><code>{
  "aduc": {"contractId": "urn:aduc:contract:river-r42:2026-07-14", "coreVersion": "0.1.0-alpha.0"},
  "resource": {"id": "urn:example:resource:river-r42-observations:2026-07-14T08:00Z", "mediaType": "application/json"},
  "structure": {"records": [{"fields": [{"id": "urn:example:field:flow", "sourcePath": "$.flow", "primitiveType": "number"}]}]},
  "semantics": {"assertions": [{"subjectRef": "urn:example:field:flow", "conceptIri": "https://example.org/vocab/env/WaterDischarge", "unitIri": "https://qudt.org/vocab/unit/M3-PER-SEC"}]}
}</code></pre>
  </div>
</section>
<section aria-labelledby="demo">
  <div class="shell">
    <div class="section-head"><p class="kicker">Concrete demonstration</p><h2 id="demo">ADUC makes comparison results explicit instead of implied.</h2></div>
    <div class="comparison-demo" aria-label="Validation and comparison demonstration">
      <div class="source-box"><strong>Source A + Contract A</strong><span>Flow in cubic meters per second, reviewed authority, local provenance.</span></div>
      <div class="source-box"><strong>Source B + Contract B</strong><span>Flow may use another unit, different evidence, policy or identity state.</span></div>
      <div class="pipeline-box">Validation -> Comparison</div>
      <div class="assessment-strip" aria-label="Possible comparison assessments"><span class="ok">equivalent</span><span class="convert">convertible</span><span class="unknown">unknown</span><span class="contest">contested</span><span class="stop">prohibited</span><span class="review">requiresHumanReview</span></div>
    </div>
    <p class="note">These states are not decorative labels. A unit is marked convertible only when the accepted evaluator has the required registry, quantity-kind, dimension, rounding and uncertainty evidence.</p>
  </div>
</section>
<section class="section-band" aria-labelledby="principles">
  <div class="shell">
    <div class="section-head compact"><p class="kicker">Operating principles</p><h2 id="principles">AI-first, human-review-first, privacy/security by design, unknown-safe.</h2></div>
    <div class="principle-grid">
      <article><h3>AI-first, not AI-only</h3><p>Reports are deterministic JSON and text so machines and humans can inspect the same outcome.</p></article>
      <article><h3>Human review stays visible</h3><p>Unknown, contested, prohibited and review-required facts are not flattened into false certainty.</p></article>
      <article><h3>Privacy and security by default</h3><p>Core validation is local-first and does not require silent upload or unapproved remote schema loading.</p></article>
      <article><h3>Authority is not invented</h3><p>ADUC records who asserted a fact and with what status; it does not manufacture truth or legal permission.</p></article>
    </div>
  </div>
</section>
<section aria-labelledby="limits">
  <div class="shell two-column">
    <div><p class="kicker">Limits</p><h2 id="limits">Working Draft means honest boundaries.</h2></div>
    <div class="answer-block"><ul class="plain-list"><li>The JSON/CSV compiler is not implemented.</li><li>The review UI is not implemented.</li><li>Public packages, registry, MCP adapter and official extensions are not stabilized.</li><li>The external two-consumer proof has not been completed.</li><li>ADUC is not a legal permission system, access-control layer, database, AI model or universal ontology.</li></ul></div>
  </div>
</section>
""",
    },
    "why-aduc.html": {
        "title": "Why ADUC - Portable understanding beyond JSON, CSV and prompts",
        "description": "Why AI-readable data contracts are needed when syntax, prompts and proprietary mappings do not preserve portable data understanding.",
        "kind": "FAQPage",
        "body": r"""
<section class="page-hero"><div class="shell"><p class="kicker">Why ADUC</p><h1>Portable understanding should not live in prompts and private glue.</h1><p class="lead">Data pipelines usually preserve values. They rarely preserve the exact interpretation that makes those values safe to compare, transform or use.</p></div></section>
<section><div class="shell comparison-table"><div><h2>JSON and CSV are necessary, not sufficient.</h2><p>They tell a consumer that a value is present and maybe that it is a string or number. They do not reliably say what the value means, what unit or time role applies, what identity decision was made, what uncertainty applies, or which policy condition blocks a use.</p></div><table><thead><tr><th>Carrier</th><th>What travels</th><th>What is usually missing</th></tr></thead><tbody><tr><td>JSON/CSV</td><td>Fields and values</td><td>Meaning, evidence, authority, policy</td></tr><tr><td>Prompt</td><td>Instruction for one model or workflow</td><td>Stable contract, testable diagnostics, portability</td></tr><tr><td>ETL mapping</td><td>Operational transformation</td><td>Open semantic evidence and consumer-neutral rules</td></tr><tr><td>ADUC</td><td>Explicit understanding contract</td><td>Source bytes remain external and authoritative</td></tr></tbody></table></div></section>
<section class="section-band"><div class="shell"><div class="section-head"><p class="kicker">Lock-in problem</p><h2>Hidden mappings make every consumer re-learn the same source.</h2><p>A proprietary connector may know that <code>flow</code> means water discharge in cubic meters per second. A prompt may explain it differently. A second AI system may never see either explanation. ADUC creates a shared, versioned object that can be carried with the resource and checked independently.</p></div><div class="principle-grid"><article><h3>Meaning becomes inspectable</h3><p>Concepts, units, mappings and qualifications are explicit fields, not prose hidden in a prompt.</p></article><article><h3>Provenance travels</h3><p>Agents, evidence, activities and derivation chains remain attached to the understanding, not only to the raw source.</p></article><article><h3>Uncertainty survives</h3><p>Unknown, contested, deprecated and review-required states stay visible to downstream consumers.</p></article><article><h3>Policy is bounded</h3><p>Usage conditions can be evaluated when the required request and evidence exist; otherwise the result remains indeterminate or human-review-required.</p></article></div></div></section>
<section><div class="shell two-column"><div><p class="kicker">What changes</p><h2>ADUC lets multiple consumers receive the same explanation and the same tests.</h2></div><div class="answer-block"><p>The practical shift is small and powerful: the understanding no longer has to be reconstructed for every model, vendor, connector or prompt. Consumers can validate the same contract, compare versions deterministically and expose the exact places where evidence is missing.</p><p>ADUC is therefore an AI-readable data contract, not an AI model, database, ontology, access-control system or agent protocol.</p></div></div></section>
<section class="section-band"><div class="shell faq"><h2>Quick distinctions</h2><details open><summary>Is ADUC the same as MCP?</summary><p>No. MCP is a communication adapter pattern for tools and agents. ADUC is a portable understanding contract attached to data. A future MCP adapter may transport ADUC, but MCP is not part of the Core.</p></details><details><summary>Is ADUC a data contract?</summary><p>It overlaps with data contracts, but it also carries semantics, identity, provenance, uncertainty, relations and usage policy so AI consumers can preserve more than schema shape.</p></details><details><summary>Is ADUC an ontology?</summary><p>No. It references external vocabularies and ontologies where useful, but it does not try to become a universal ontology.</p></details></div></section>
""",
    },
}


EXTRA_PAGES = {
    "core.html": (
        "ADUC Core - Ten blocks for portable data understanding",
        "The ADUC Core model defines ten blocks for structure, semantics, identity, context, provenance, uncertainty, relations and policy.",
        "TechArticle",
        r"""
<section class="page-hero"><div class="shell"><p class="kicker">Core</p><h1>The ten-block ADUC Core model.</h1><p class="lead">The Core separates contract metadata, source resource, structure, semantics, identity, context, provenance, uncertainty, relations and policy so each normative fact has one owner.</p></div></section>
<section><div class="shell"><div class="core-detail-list">
<article id="aduc"><h2>aduc <span>required object</span></h2><p>Owns contract identity, Core version, status, publisher, profile declarations and extension declarations.</p><pre class="code-block"><code>"aduc": {"contractId": "urn:aduc:contract:river-r42:2026-07-14", "coreVersion": "0.1.0-alpha.0"}</code></pre></article>
<article id="resource"><h2>resource <span>required object</span></h2><p>Describes the original resource being accompanied: kind, media type, digest, locator and version. ADUC accompanies the resource; it does not replace it.</p><pre class="code-block"><code>"resource": {"id": "urn:example:resource:river-r42-observations:2026-07-14T08:00Z", "mediaType": "application/json"}</code></pre></article>
<article id="structure"><h2>structure <span>required object</span></h2><p>Owns records, fields, primitive types, source paths and links from structure to the described resource. <code>structure.records</code> is the normative form.</p><pre class="code-block"><code>"structure": {"resourceRef": "urn:example:resource:river-r42-observations:2026-07-14T08:00Z", "records": [...]}</code></pre></article>
<article id="semantics"><h2>semantics <span>optional object</span></h2><p>Owns assertions that bind fields or objects to concepts, mapping relations, units, value maps, authority, evidence and lifecycle state.</p><pre class="code-block"><code>"semantics": {"assertions": [{"subjectRef": "urn:example:field:flow", "conceptIri": "https://example.org/vocab/env/WaterDischarge"}]}</code></pre></article>
<article id="identity"><h2>identity <span>optional object</span></h2><p>Owns entities, identifiers and identity assertions. Exact identity requires qualifying evidence; similar labels or inferred matches do not silently merge entities.</p><pre class="code-block"><code>"identity": {"entities": [{"id": "urn:example:entity:station-r42"}], "identityAssertions": [...]}</code></pre></article>
<article id="context"><h2>context <span>optional object</span></h2><p>Owns temporal, spatial and operational context such as timestamp roles, timezone evidence, precision and operating environment.</p><pre class="code-block"><code>"context": {"temporal": [{"fieldRef": "urn:example:field:timestamp", "timezoneIri": "urn:iana:tz:UTC"}]}</code></pre></article>
<article id="provenance"><h2>provenance <span>optional object</span></h2><p>Owns agents, entities, activities, evidence and derivation assertions. It preserves lineage without claiming that replayable means perfectly reproducible.</p><pre class="code-block"><code>"provenance": {"agents": [...], "activities": [...], "evidence": [...]}</code></pre></article>
<article id="uncertainty"><h2>uncertainty <span>optional object</span></h2><p>Owns measurement uncertainty, missingness and quality measurements. Missing data is not silently converted into false, safe or exact.</p><pre class="code-block"><code>"uncertainty": {"statements": [{"subjectRef": "urn:example:field:flow", "kind": "relativeStandardUncertainty"}]}</code></pre></article>
<article id="relations"><h2>relations <span>optional array</span></h2><p>Owns graph assertions with explicit subject, predicate, object endpoint, polarity, authority and evidence. Relations are an array; other top-level modules are single objects.</p><pre class="code-block"><code>"relations": [{"subjectRef": "urn:example:resource:...", "predicateIri": "http://www.w3.org/ns/prov#wasDerivedFrom", "objectRef": "urn:example:prov-entity:raw-sensor-feed"}]</code></pre></article>
<article id="policy"><h2>policy <span>optional object</span></h2><p>Owns use-condition descriptions and machine-evaluable rules when evidence allows. Policy requires provenance and does not grant automatic legal permission.</p><pre class="code-block"><code>"policy": {"policies": [{"targetRef": "urn:example:resource:...", "rules": [{"effect": "prohibition"}]}]}</code></pre></article>
</div></div></section>
<section class="section-band"><div class="shell"><h2>Responsibility boundary</h2><div class="boundary-grid"><div><h3>JSON Schema validates structure</h3><p>Types, required properties, cardinality, enums, formats, absolute IRIs, SHA-256 digests, closed objects and exclusive object forms.</p></div><div><h3>Architecture and profiles validate cross-cutting rules</h3><p>Identifier uniqueness, reference resolution, binding consistency, extension use, graph safety, profile-specific uncertainty, identity, relation and policy constraints.</p></div></div></div></section>
""",
    ),
    "validate.html": (
        "Validate ADUC Core contracts deterministically",
        "Run the unified ADUC full-Core validator and understand schema, architecture and profile diagnostics.",
        "SoftwareSourceCode",
        r"""
<section class="page-hero"><div class="shell"><p class="kicker">Validate</p><h1>One command validates a complete ADUC Core contract.</h1><p class="lead">The unified validator separates schema errors, architectural errors and profile-level diagnostics while producing stable JSON and text reports.</p></div></section>
<section><div class="shell command-layout"><div><h2>Command</h2><pre class="code-block"><code>python tools/aduc_core.py validate examples/core/complete-model.example.json
python tools/aduc_core.py validate examples/core/complete-model.example.json --format json
python tools/aduc_core.py validate contract.json --schema-only
python tools/aduc_core.py validate contract.json --no-profile-evaluation</code></pre><p><code>--schema-only</code> runs only the Draft 2020-12 schema family. <code>--no-profile-evaluation</code> keeps schema and architecture checks but skips profile adapter evaluation.</p></div><div class="state-panel available"><h2>Exit outcomes</h2><ul><li><code>valid</code></li><li><code>validWithWarnings</code></li><li><code>requiresHumanReview</code></li><li><code>blocked</code></li></ul><p>These are full-Core validation outcomes, not policy decisions.</p></div></div></section>
<section class="section-band"><div class="shell"><div class="section-head"><p class="kicker">Pipeline</p><h2>Validation order is explicit.</h2></div><ol class="trace-steps compact"><li><strong>Load JSON</strong><span>Reject unreadable, invalid or excessive input with stable input diagnostics.</span></li><li><strong>Validate schema</strong><span>Use the 14 local Draft 2020-12 schemas without remote retrieval.</span></li><li><strong>Check architecture</strong><span>Resolve identifiers, references, bindings, ownership and extension boundaries.</span></li><li><strong>Evaluate profiles</strong><span>Call applicable ADR-0005 through ADR-0013 evaluators and report non-applicable rules explicitly.</span></li></ol></div></section>
<section><div class="shell example-layout"><div><h2>Report excerpt</h2><p>This structure is taken from the implemented validation report specification. It keeps profile adapter evidence separate from ordinary diagnostics.</p></div><pre class="code-block"><code>{
  "reportVersion": "0.1.0",
  "valid": false,
  "outcome": "blocked",
  "contractId": "urn:example:contract:1",
  "coreVersion": "0.1.0-alpha.0",
  "summary": {"errors": 1, "warnings": 0, "humanReview": 0},
  "pipeline": {"jsonLoaded": true, "schemaValid": true, "architectureValid": false, "profileEvaluation": true},
  "modules": {"aduc": {"status": "valid"}, "resource": {"status": "valid"}, "structure": {"status": "valid"}},
  "profileEvaluations": [],
  "diagnostics": []
}</code></pre></div></section>
<section class="section-band"><div class="shell"><h2>What validation does not prove</h2><div class="principle-grid"><article><h3>No factual truth proof</h3><p>A schema-valid assertion may still be wrong in the world.</p></article><article><h3>No automatic authority</h3><p>Authority must be asserted and evidenced; it is not inferred from format correctness.</p></article><article><h3>No universal permission</h3><p>Policy evaluation is bounded by the request, evidence and applicable rules.</p></article><article><h3>No silent remote trust</h3><p>Core operation remains local unless a future integration explicitly approves remote resolution.</p></article></div></div></section>
""",
    ),
    "compare.html": (
        "Compare ADUC Core contracts deterministically",
        "Use the ADUC full-Core comparator to separate changeType from normative assessment across structure, semantics, policy and evidence.",
        "SoftwareSourceCode",
        r"""
<section class="page-hero"><div class="shell"><p class="kicker">Compare</p><h1>Deterministic comparison separates mechanical change from semantic assessment.</h1><p class="lead">The comparator validates both contracts, indexes addressable objects by identifier, and reports what changed without trusting unsafe inputs.</p></div></section>
<section><div class="shell command-layout"><div><h2>Command</h2><pre class="code-block"><code>python tools/aduc_core.py compare contract-a.json contract-b.json
python tools/aduc_core.py compare contract-a.json contract-b.json --format json</code></pre><p>Addressable arrays are compared by stable Core identifiers, not by accidental JSON array order.</p></div><div class="state-panel planned"><h2>Unsafe inputs</h2><p>Contracts with duplicate identifiers, unresolved references, ownership violations, broken resource binding, namespace conflicts or unsupported required extensions are <code>notComparable</code>.</p></div></div></section>
<section class="section-band"><div class="shell"><h2>Two dimensions in every meaningful change</h2><div class="boundary-grid"><div><h3><code>changeType</code></h3><p>The mechanical diff shape: <code>unchanged</code>, <code>added</code>, <code>removed</code> or <code>modified</code>.</p></div><div><h3><code>assessment</code></h3><p>The normative semantic result: <code>equivalent</code>, <code>convertible</code>, <code>compatible</code>, <code>incompatible</code>, <code>unknown</code>, <code>contested</code>, <code>deprecated</code>, <code>prohibited</code> or <code>requiresHumanReview</code>.</p></div></div></div></section>
<section><div class="shell"><div class="section-head"><p class="kicker">Normative assessment states</p><h2>The comparator avoids false certainty.</h2></div><div class="assessment-grid"><div class="ok"><strong>equivalent</strong><span>No material semantic difference under the checked dimension.</span></div><div class="convert"><strong>convertible</strong><span>Conversion is proven by the accepted evaluator and required registry evidence.</span></div><div class="ok"><strong>compatible</strong><span>The change can be consumed without known breakage under documented assumptions.</span></div><div class="stop"><strong>incompatible</strong><span>The change breaks or contradicts the compared dimension.</span></div><div class="unknown"><strong>unknown</strong><span>Information is insufficient; ADUC does not guess.</span></div><div class="contest"><strong>contested</strong><span>Evidence or assertions conflict and must remain visible.</span></div><div class="muted"><strong>deprecated</strong><span>The object or assertion remains present but is no longer current.</span></div><div class="stop"><strong>prohibited</strong><span>A policy or rule blocks the compared use.</span></div><div class="review"><strong>requiresHumanReview</strong><span>Automatic use is not safe without human decision.</span></div></div></div></section>
<section class="section-band"><div class="shell example-layout"><div><h2>Report excerpt</h2><p>A unit change is <code>convertible</code> only when ADR-0007 confirms matching dimension, quantity kind, role compatibility, supported conversion, verified registry, rounding policy and preserved uncertainty.</p></div><pre class="code-block"><code>{
  "reportVersion": "0.1.0",
  "comparable": true,
  "overall": "potentiallyIncompatible",
  "overallAssessment": "unknown",
  "changes": [{"changeType": "modified", "assessment": "unknown", "module": "semantics", "dimension": "unit"}]
}</code></pre></div></section>
""",
    ),
}

EXTRA_PAGES.update(
    {
        "architecture.html": (
            "ADUC architecture - Core, schemas, validator and comparator",
            "The ADUC architecture separates the normative Core, local schemas, full-Core validator, deterministic comparator and future product layers.",
            "TechArticle",
            r"""
<section class="page-hero"><div class="shell"><p class="kicker">Architecture</p><h1>Core, schemas, validator and comparator are separate layers.</h1><p class="lead">ADUC keeps normative model decisions, structural schemas, architecture checks, profile evaluators and future product tooling in distinct responsibility zones.</p></div></section>
<section><div class="shell layer-stack"><article><h2>1. Normative Core</h2><p>ADR-0014 defines the ten-block object model, module ownership, extension boundaries and minimum envelope.</p></article><article><h2>2. Modular schemas</h2><p>ADR-0015 implements 14 local Draft 2020-12 schemas. They validate structure without replacing external vocabularies or proving truth.</p></article><article><h2>3. Full-Core validator</h2><p>ADR-0016 orchestrates schema validation, architecture checks and applicable profile evaluators into one deterministic report.</p></article><article><h2>4. Deterministic comparator</h2><p>The comparator validates both inputs, blocks dangerous indexes and reports mechanical changes plus normative assessments.</p></article><article><h2>5. Legacy semantic profile migration</h2><p>The old standalone semantic-mapping profile remains supported as a migration source. It is not the current Core architecture.</p></article><article><h2>6. Future product layers</h2><p>Compiler, review UI, SDKs, registry, MCP adapter and extensions remain future gates, not current site claims.</p></article></div></section>
<section class="section-band"><div class="shell"><h2>Offline and provider-neutral by design</h2><div class="principle-grid"><article><h3>Local schemas</h3><p>Operational references resolve locally; no remote schema retrieval is required for Core validation.</p></article><article><h3>Stable reports</h3><p>JSON and text outputs use stable codes, paths and deterministic ordering.</p></article><article><h3>Profile adapters</h3><p>Accepted evaluators are called where the contract contains the required shape and evidence.</p></article><article><h3>Future adapters stay optional</h3><p>MCP, registries and hosted services may carry ADUC later but do not define the Core.</p></article></div></div></section>
""",
        ),
        "trust.html": (
            "ADUC trust model - AI-first, local-first and unknown-safe",
            "ADUC preserves uncertainty, provenance, policy boundaries, human review and privacy/security constraints for AI-readable data contracts.",
            "FAQPage",
            r"""
<section class="page-hero"><div class="shell"><p class="kicker">Trust</p><h1>ADUC is designed to preserve uncertainty instead of hiding it.</h1><p class="lead">The project is AI-first, but not AI-only; local-first, but not anti-integration; explicit, but not a source of legal or factual authority by itself.</p></div></section>
<section><div class="shell trust-matrix"><article><h2>Provider neutrality</h2><p>Core validation and comparison do not depend on a model vendor or remote AI service. Reports are deterministic artifacts.</p></article><article><h2>Human review</h2><p>Consequential unknowns, contested assertions, prohibited uses and unsupported conversions remain visible as review states.</p></article><article><h2>Privacy by design</h2><p>Core tooling is local by default. Hosted uploads, telemetry, retention and training are future product choices that require explicit review.</p></article><article><h2>Security by design</h2><p>Contracts, descriptions and extensions are untrusted input. Size, depth and graph limits prevent unsafe processing and cycles.</p></article><article><h2>No unapproved remote resolution</h2><p>The schema family works offline. External vocabularies are referenced, not copied as ADUC replacements or silently fetched.</p></article><article><h2>Authority remains bounded</h2><p>ADUC can record authority and evidence. It does not make a statement true, legal, permitted or safe merely by encoding it.</p></article></div></section>
<section class="section-band"><div class="shell"><h2>Failure-safe states</h2><div class="assessment-grid"><div class="unknown"><strong>unknown</strong><span>Insufficient information remains explicit.</span></div><div class="contest"><strong>contested</strong><span>Conflicting assertions are not merged away.</span></div><div class="muted"><strong>deprecated</strong><span>Outdated information remains visible with lifecycle state.</span></div><div class="stop"><strong>prohibited</strong><span>Blocked policy outcomes are not softened.</span></div><div class="review"><strong>requiresHumanReview</strong><span>Automation stops where evidence or responsibility requires a person.</span></div></div></div></section>
<section><div class="shell faq"><h2>Trust FAQ</h2><details open><summary>Does ADUC prove a data value is true?</summary><p>No. ADUC validates the contract and records evidence, provenance and authority. Truth remains a domain claim.</p></details><details><summary>Does ADUC grant legal permission?</summary><p>No. Policy rules can be represented and evaluated under bounded conditions, but ADUC is not legal advice or production access control.</p></details><details><summary>Does ADUC require uploading data?</summary><p>No. The Core reference path is local and offline-capable.</p></details></div></section>
""",
        ),
        "evidence.html": (
            "ADUC evidence - schemas, fixtures, tests and limits",
            "Current ADUC evidence includes schemas, fixtures, profile evaluators, deterministic reports and comparison scenarios, with explicit limits.",
            "TechArticle",
            r"""
<section class="page-hero"><div class="shell"><p class="kicker">Conformance and evidence</p><h1>Evidence is tied to artifacts, not marketing claims.</h1><p class="lead">ADUC is a Working Draft with implemented Core foundations, deterministic fixtures and tests. It is not yet a recognized standard or a proven first-world claim.</p></div></section>
<section><div class="shell evidence-ledger"><div><strong>10</strong><span>normative Core blocks</span></div><div><strong>14</strong><span>Draft 2020-12 schema files</span></div><div><strong>11</strong><span>valid complete Core contracts</span></div><div><strong>15</strong><span>invalid complete Core contracts</span></div><div><strong>24</strong><span>comparison scenarios</span></div><div><strong>9</strong><span>domain profile evaluators</span></div></div></section>
<section class="section-band"><div class="shell"><h2>What is evidenced now</h2><div class="principle-grid"><article><h3>Schemas</h3><p>The Core schema family validates structure locally using the Draft 2020-12 entry point <code>schema/aduc-core.schema.json</code>.</p></article><article><h3>Fixtures</h3><p>Official valid and invalid Core fixtures exercise the envelope, modules, references, extensions and architecture checker.</p></article><article><h3>Reports</h3><p>Validator and comparator reports are stable JSON/text outputs with deterministic diagnostic ordering.</p></article><article><h3>CI path</h3><p>The validation workflow runs profile suites, Core model checks, schema checks, website checks and full-Core commands.</p></article></div></div></section>
<section><div class="shell two-column"><div><h2>What is not yet proven</h2></div><div class="answer-block"><ul class="plain-list"><li>No independent full conformance implementation has been published.</li><li>No external two-consumer AI proof has completed.</li><li>No absolute first-world claim is made.</li><li>Conformance classes for producers, validators, comparators, compilers, consumers and extensions remain future work.</li></ul></div></div></section>
<section class="section-band"><div class="shell"><h2>Before stronger public claims</h2><ol class="trace-steps compact"><li><strong>Freeze a reproducible package</strong><span>Inputs, contracts, reports and hashes.</span></li><li><strong>Run independent consumers</strong><span>At least two consumers or implementations must preserve meaning without hidden mappings.</span></li><li><strong>Publish failures too</strong><span>Unknowns, disagreements and limitations remain part of the evidence.</span></li><li><strong>Review prior art</strong><span>Novelty boundaries require dated prior-art and independent review.</span></li></ol></div></section>
""",
        ),
        "roadmap.html": (
            "ADUC roadmap - Completed Core, migration available and formatter next",
            "ADUC roadmap status synchronized with the current repository: Core foundations and semantic migration complete, deterministic formatter active, compiler and review UI not started.",
            "TechArticle",
            r"""
<section class="page-hero"><div class="shell"><p class="kicker">Roadmap</p><h1>The roadmap separates completed Core foundations from future product gates.</h1><p class="lead">Semantic-profile migration is available. The active technical task is a deterministic formatter for complete ADUC Core contracts.</p></div></section>
<section><div class="shell roadmap-list"><article class="done"><h2>Phase 0 - Core foundations</h2><p>Complete: mission, non-goals, profiles ADR-0005 through ADR-0013, normative ten-block Core object model, module manifest, complete example and architecture checker.</p></article><article class="done"><h2>Phase 1 - Schema family and migration</h2><p>Complete: 14 local Draft 2020-12 schemas, valid and invalid Core fixtures, local schema-plus-architecture validator, and deterministic migration from the old semantic profile.</p></article><article class="mixed"><h2>Phase 2 - Reference implementation</h2><p>Validator, comparator and semantic-profile migration are complete. Remaining tools include the formatter, SDKs, conformance runner, package publication plan and updated developer distribution work.</p></article><article class="active"><h2>Active task - Deterministic Core formatter</h2><p>Define and implement stable UTF-8 formatting for complete validated Core contracts without inferring, repairing or changing semantic content.</p></article><article class="blocked"><h2>Blocked until gates pass</h2><p>JSON/CSV compiler, review UI, external multi-model proof, registry, MCP adapter, extensions and anticipation engine are not current implementation tasks.</p></article></div></section>
<section class="section-band"><div class="shell"><h2>Cross-cutting tracks</h2><div class="principle-grid"><article><h3>AI-first and human-first</h3><p>Provider-neutral machine reports and understandable human diagnostics.</p></article><article><h3>Privacy and security</h3><p>Local defaults, no silent upload, safe graph and input limits.</p></article><article><h3>Visibility</h3><p>Stable URLs, crawlable docs, honest SEO/AEO/GEO content and no ranking promises.</p></article><article><h3>Novelty proof</h3><p>No first-world claim without prior-art boundary, independent review and reproducible evidence.</p></article></div></div></section>
""",
        ),
        "docs.html": (
            "ADUC docs - Try validation and comparison in 5 minutes",
            "Install ADUC development dependencies, validate a Core contract, compare contracts and run the website checks locally.",
            "SoftwareSourceCode",
            r"""
<section class="page-hero"><div class="shell"><p class="kicker">Try in 5 minutes</p><h1>Run the local ADUC checks from the repository.</h1><p class="lead">The developer path is intentionally boring: install test dependencies, validate a Core contract, compare two contracts and run the website checks.</p></div></section>
<section><div class="shell command-layout"><div><h2>Install</h2><pre class="code-block"><code>python -m pip install --disable-pip-version-check -r requirements-dev.txt</code></pre><h2>Validate a complete Core contract</h2><pre class="code-block"><code>python tools/aduc_core.py validate examples/core/complete-model.example.json
python tools/aduc_core.py validate examples/core/complete-model.example.json --format json</code></pre><h2>Compare two contracts</h2><pre class="code-block"><code>python tools/aduc_core.py compare examples/core/complete-model.example.json examples/core/complete-model.example.json
python tools/aduc_core.py compare contract-a.json contract-b.json --format json</code></pre></div><aside class="state-panel available"><h2>Developer shortcuts</h2><p><a href="core.html">Read the ten-block Core</a></p><p><a href="validate.html">Understand validation reports</a></p><p><a href="compare.html">Understand comparison reports</a></p><p><a href="https://github.com/BACOUL/AI-Data-Understanding-Core-ADUC/tree/main/schema">Open schemas</a></p></aside></div></section>
<section class="section-band"><div class="shell"><h2>Run principal tests</h2><pre class="code-block"><code>python tools/validate_contracts.py
python -m unittest discover -s tests/core_schema -p "test_*.py"
python -m unittest discover -s tests/core_validator -p "test_*.py"
python -m unittest discover -s tests/core_comparator -p "test_*.py"
python -m unittest discover -s tests/website -p "test_*.py"
python tools/validate_website.py</code></pre></div></section>
<section><div class="shell"><h2>Domain reference evaluators</h2><p>The older specialized tools remain useful for profile-level reference behavior and migration work. They are not replacements for the full-Core validator.</p><div class="tool-list"><code>tools/aduc_epistemic.py</code><code>tools/aduc_source_binding.py</code><code>tools/aduc_units.py</code><code>tools/aduc_time.py</code><code>tools/aduc_identity.py</code><code>tools/aduc_provenance.py</code><code>tools/aduc_uncertainty.py</code><code>tools/aduc_relations.py</code><code>tools/aduc_policy.py</code></div></div></section>
<section class="section-band"><div class="shell"><h2>Canonical and deployment note</h2><p>The repository currently declares GitHub Pages as the canonical public URL: <code>https://bacoul.github.io/AI-Data-Understanding-Core-ADUC/</code>. Vercel is configured to publish the same static <code>website/</code> directory and should be treated as deployment infrastructure unless a future decision changes the canonical URL.</p></div></section>
""",
        ),
        "example.html": (
            "ADUC example - A conformant Core contract excerpt",
            "A conformant ADUC Core example showing aduc, resource, structure and semantics from the complete model fixture.",
            "TechArticle",
            r"""
<section class="page-hero"><div class="shell"><p class="kicker">Example</p><h1>A complete Core contract explains more than field names.</h1><p class="lead">The official example describes a river observation resource with structure, semantics, identity, context, provenance, uncertainty, relations and policy.</p></div></section>
<section><div class="shell example-layout"><div><h2>What the source alone says</h2><pre class="code-block"><code>{"station":"R42","flow":1.5,"quality":1,"timestamp":"2026-07-14T08:00:00Z"}</code></pre><p>The values are readable. Their shared meaning is not guaranteed without extra context.</p></div><div><h2>What ADUC adds</h2><ul class="plain-list"><li><code>flow</code> is water discharge.</li><li>The unit is <code>https://qudt.org/vocab/unit/M3-PER-SEC</code>.</li><li>The timestamp role is SOSA result time.</li><li>The station identity has an issuer and authority state.</li><li>Provenance, uncertainty and policy remain visible.</li></ul></div></div></section>
<section class="section-band"><div class="shell"><h2>Core excerpt</h2><pre class="code-block"><code>{
  "aduc": {"contractId": "urn:aduc:contract:river-r42:2026-07-14", "coreVersion": "0.1.0-alpha.0"},
  "resource": {"id": "urn:example:resource:river-r42-observations:2026-07-14T08:00Z", "mediaType": "application/json"},
  "structure": {"records": [{"fields": [{"id": "urn:example:field:flow", "sourcePath": "$.flow", "primitiveType": "number"}]}]},
  "semantics": {"assertions": [{"subjectRef": "urn:example:field:flow", "conceptIri": "https://example.org/vocab/env/WaterDischarge", "unitIri": "https://qudt.org/vocab/unit/M3-PER-SEC"}]}
}</code></pre><p><a class="button secondary" href="https://github.com/BACOUL/AI-Data-Understanding-Core-ADUC/blob/main/examples/core/complete-model.example.json">Open the full example on GitHub</a></p></div></section>
""",
        ),
        "specification.html": (
            "ADUC specification - Working Draft technical reference",
            "Technical reference links for the ADUC Working Draft Core model, schema family, validation report and comparison report.",
            "TechArticle",
            r"""
<section class="page-hero"><div class="shell"><p class="kicker">Specification</p><h1>Technical reference for the current Working Draft.</h1><p class="lead">This page points to the normative model, schemas, validation report, comparison report and accepted ADRs without replacing the repository specifications.</p></div></section>
<section><div class="shell spec-index"><a href="core.html"><strong>Core model</strong><span>Ten blocks and module ownership</span></a><a href="https://github.com/BACOUL/AI-Data-Understanding-Core-ADUC/blob/main/schema/aduc-core.schema.json"><strong>Schema entry point</strong><span>Draft 2020-12 local validation</span></a><a href="validate.html"><strong>Validation report</strong><span>Schema, architecture and profile diagnostics</span></a><a href="compare.html"><strong>Comparison report</strong><span>changeType and assessment</span></a><a href="architecture.html"><strong>Architecture</strong><span>Layer boundaries and future tools</span></a><a href="evidence.html"><strong>Evidence</strong><span>Fixtures, scenarios, tests and limits</span></a></div></section>
<section class="section-band"><div class="shell"><h2>Standards composed, not replaced</h2><p>ADUC references established standards and vocabularies such as JSON Schema, JSON-LD/RDF, PROV-O, DQV, ODRL, QUDT, UCUM, RFC 3339, IANA TZDB, OWL-Time and identity vocabularies where appropriate. External schemas and vocabularies are referenced; they are not copied as ADUC replacements.</p></div></section>
""",
        ),
        "404.html": (
            "ADUC - Page not found",
            "The requested ADUC page was not found. Return to the Working Draft documentation.",
            "WebPage",
            r"""
<section class="page-hero"><div class="shell"><p class="kicker">404</p><h1>That ADUC page is not described here.</h1><p class="lead">The site keeps stable static URLs. Use the navigation to reach the current Working Draft pages.</p><p><a class="button primary" href="index.html">Return home</a></p></div></section>
""",
        ),
    }
)


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


CSS = r"""
:root { --bg:#0b0e12; --surface:#141c24; --surface-2:#1b2731; --line:#31414d; --text:#f4f7f8; --muted:#b6c2c8; --accent:#00d1a7; --accent-2:#d6b56d; --danger:#ff7d73; --review:#c7a4ff; --unknown:#9fb0bc; --ok:#8ce6a7; --shadow:0 22px 60px rgba(0,0,0,.28); --radius:8px; --shell:1180px; --mono:"SFMono-Regular",Consolas,"Liberation Mono",monospace; --sans:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
*{box-sizing:border-box} html{overflow-x:clip;scroll-behavior:smooth;scroll-padding-top:92px} body{max-width:100%;overflow-x:clip;margin:0;color:var(--text);background:linear-gradient(180deg,#0b0e12 0%,#0f151b 42%,#0b0e12 100%);font-family:var(--sans);line-height:1.6;-webkit-font-smoothing:antialiased} body:before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px);background-size:42px 42px;mask-image:linear-gradient(to bottom,black,transparent 75%)} a{color:var(--accent);text-underline-offset:.2em} a:hover{color:#7ff7de} code,pre{font-family:var(--mono)} img,svg{max-width:100%} button,input,textarea,select{font:inherit}:focus-visible{outline:3px solid var(--accent-2);outline-offset:4px}.shell{width:min(calc(100% - 32px),var(--shell));margin-inline:auto}.shell>*{min-width:0}.skip-link{position:fixed;top:12px;left:12px;z-index:1000;padding:10px 14px;color:#06110f;background:var(--accent);transform:translateY(-160%);border-radius:var(--radius);font-weight:800}.skip-link:focus{transform:translateY(0)}.site-header{position:sticky;top:0;z-index:20;background:rgba(11,14,18,.92);border-bottom:1px solid var(--line);backdrop-filter:blur(14px)}.nav-shell{min-height:74px;display:flex;gap:20px;align-items:center;justify-content:space-between}.brand{display:inline-flex;gap:12px;align-items:center;color:var(--text);text-decoration:none;font-weight:900}.brand-mark{width:42px;height:42px;display:grid;place-items:center;color:#06110f;background:linear-gradient(135deg,var(--accent),var(--accent-2));border-radius:10px;font-size:13px;letter-spacing:-.03em}.brand-copy span{display:block;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.08em;font-weight:750}.site-nav{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:4px}.site-nav a{min-height:38px;display:inline-flex;align-items:center;padding:7px 10px;color:var(--muted);border-radius:7px;text-decoration:none;font-size:14px;font-weight:700}.site-nav a:hover,.site-nav a[aria-current=page]{color:var(--text);background:rgba(255,255,255,.07)}.nav-github{color:#06110f!important;background:var(--accent)!important}
.hero,.page-hero{padding:clamp(56px,8vw,112px) 0 clamp(36px,6vw,78px)}.split-hero{border-bottom:1px solid rgba(255,255,255,.06)}.hero-grid{display:grid;grid-template-columns:minmax(0,1.02fr) minmax(340px,.98fr);gap:clamp(30px,6vw,84px);align-items:center}.hero-copy,.hero-instrument{min-width:0}.kicker{margin:0 0 14px;color:var(--accent-2);text-transform:uppercase;letter-spacing:.11em;font-size:12px;font-weight:900}h1,h2,h3{margin-top:0;line-height:1.1;letter-spacing:-.02em;max-width:100%}h1{max-width:min(12ch,100%);margin-bottom:20px;font-size:clamp(44px,8vw,92px)}.page-hero h1{max-width:min(16ch,100%);font-size:clamp(38px,6vw,72px)}h2{font-size:clamp(28px,4vw,50px)}h3{font-size:20px}.lead{max-width:68ch;color:#d3dde2;font-size:clamp(18px,2vw,23px)}.definition{border-left:3px solid var(--accent);padding-left:18px}.hero-actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}.button{min-height:46px;display:inline-flex;align-items:center;justify-content:center;padding:10px 15px;border:1px solid var(--line);border-radius:var(--radius);text-decoration:none;font-weight:850}.button.primary{color:#06110f;background:var(--accent);border-color:var(--accent)}.button.secondary{color:var(--text);background:var(--surface-2)}.button.ghost{color:var(--text);background:transparent}.status-ledger{display:grid;gap:8px;margin-top:26px;color:var(--muted);font-size:14px}.status-ledger span{padding-left:12px;border-left:2px solid var(--line)}
.home-command{width:100%;max-width:100%;overflow-x:auto;contain:inline-size;margin:18px 0 0;padding:12px;color:#dbe8ec;background:#070b0f;border:1px solid #2b3b45;border-radius:var(--radius);font-size:12px}.home-command code{white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word}.contract-flow{display:grid;gap:12px;padding:18px;background:linear-gradient(180deg,#141c24,#10161d);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow);min-width:0}.contract-flow div{position:relative;min-width:0;padding:16px;background:#0b1117;border:1px solid #2a3945;border-radius:var(--radius)}.contract-flow div:not(:last-child):after{content:"";position:absolute;left:28px;bottom:-13px;width:2px;height:13px;background:var(--accent)}.contract-flow span{display:block;color:var(--accent-2);font-weight:850}.contract-flow code{display:block;margin-top:6px;color:#d8e4e8;white-space:normal;overflow-wrap:anywhere}section{padding:clamp(48px,7vw,88px) 0}.section-band{background:rgba(255,255,255,.025);border-top:1px solid rgba(255,255,255,.055);border-bottom:1px solid rgba(255,255,255,.055)}.two-column,.example-layout,.command-layout{display:grid;grid-template-columns:minmax(0,.78fr) minmax(0,1.22fr);gap:clamp(24px,5vw,64px);align-items:start}.two-column>*,.example-layout>*,.command-layout>*{min-width:0}.section-head{max-width:880px;margin-bottom:32px}.section-head.compact{max-width:720px}.answer-block{color:#d3dde2;font-size:18px}
.trace-steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;padding:0;margin:0;list-style:none;counter-reset:step}.trace-steps li{min-height:150px;padding:18px;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);counter-increment:step}.trace-steps li:before{content:counter(step,decimal-leading-zero);display:block;color:var(--accent);font-family:var(--mono);margin-bottom:18px}.trace-steps strong,.trace-steps span{display:block}.trace-steps span{color:var(--muted);margin-top:6px}.trace-steps.compact li{min-height:120px}.core-map{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}.core-map a{min-height:104px;display:flex;flex-direction:column;justify-content:space-between;padding:14px;color:var(--text);background:#101820;border:1px solid var(--line);border-radius:var(--radius);text-decoration:none;font-family:var(--mono)}.core-map a:hover{border-color:var(--accent)}.core-map span{color:var(--muted);font:13px var(--sans)}
.status-columns,.principle-grid,.trust-matrix,.assessment-grid,.boundary-grid{display:grid;gap:14px}.status-columns{grid-template-columns:1fr}.principle-grid{grid-template-columns:repeat(4,minmax(0,1fr))}.trust-matrix{grid-template-columns:repeat(3,minmax(0,1fr))}.boundary-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.state-panel,.principle-grid article,.trust-matrix article,.boundary-grid div,.source-box,.layer-stack article,.roadmap-list article,.spec-index a{padding:18px;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius)}.state-panel h3,.state-panel h2{margin-bottom:8px}.state-panel.available{border-left:4px solid var(--ok)}.state-panel.progress,.roadmap-list .active{border-left:4px solid var(--accent-2)}.state-panel.planned,.roadmap-list .blocked{border-left:4px solid var(--unknown)}.plain-list{padding-left:20px;color:#d3dde2}
pre.code-block{display:block;width:100%;max-width:100%;overflow-x:auto;contain:inline-size;margin:0;padding:18px;color:#dbe8ec;background:#070b0f;border:1px solid #2b3b45;border-radius:var(--radius);font-size:13px;line-height:1.62;tab-size:2}pre.code-block code{white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word}p code,li code,td code{padding:2px 5px;color:#dffbf5;background:rgba(0,209,167,.09);border:1px solid rgba(0,209,167,.18);border-radius:5px;overflow-wrap:anywhere}.comparison-demo{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.source-box strong,.source-box span{display:block}.source-box span{color:var(--muted)}.pipeline-box{grid-column:1/-1;padding:18px;text-align:center;color:#06110f;background:linear-gradient(90deg,var(--accent),var(--accent-2));border-radius:var(--radius);font-weight:900}.assessment-strip,.assessment-grid{grid-column:1/-1;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px}.assessment-strip span,.assessment-grid div{min-height:58px;padding:10px;display:flex;flex-direction:column;justify-content:center;border:1px solid var(--line);border-radius:var(--radius);color:var(--text)}.assessment-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.assessment-grid span{color:var(--muted)}.ok{background:rgba(140,230,167,.08);border-color:rgba(140,230,167,.35)!important}.convert{background:rgba(0,209,167,.08);border-color:rgba(0,209,167,.35)!important}.unknown,.muted{background:rgba(159,176,188,.08);border-color:rgba(159,176,188,.3)!important}.contest{background:rgba(214,181,109,.09);border-color:rgba(214,181,109,.35)!important}.stop{background:rgba(255,125,115,.09);border-color:rgba(255,125,115,.38)!important}.review{background:rgba(199,164,255,.09);border-color:rgba(199,164,255,.38)!important}.note{color:var(--muted)}
.comparison-table{display:grid;grid-template-columns:minmax(0,.7fr) minmax(0,1.3fr);gap:32px;align-items:start}.comparison-table>*{min-width:0}table{width:100%;border-collapse:collapse;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden}th,td{padding:12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{color:var(--text);background:#1a252e}td{color:var(--muted)}.faq details{padding:18px 0;border-top:1px solid var(--line)}.faq summary{cursor:pointer;font-weight:850}.faq p{color:var(--muted);max-width:76ch}.core-detail-list{display:grid;gap:28px}.core-detail-list article{min-width:0;padding-bottom:28px;border-bottom:1px solid var(--line)}.core-detail-list h2 span{color:var(--accent-2);font:14px var(--sans);text-transform:uppercase;letter-spacing:.08em}.layer-stack,.roadmap-list{display:grid;gap:14px}.layer-stack{grid-template-columns:repeat(2,minmax(0,1fr))}.layer-stack>*,.roadmap-list>*{min-width:0}.roadmap-list .done{border-left:4px solid var(--ok)}.roadmap-list .mixed{border-left:4px solid var(--accent)}.evidence-ledger{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}.evidence-ledger div{padding:18px;background:#101820;border:1px solid var(--line);border-radius:var(--radius)}.evidence-ledger strong{display:block;color:var(--accent);font-size:40px;line-height:1}.evidence-ledger span{color:var(--muted)}.tool-list,.spec-index{display:grid;gap:10px}.tool-list{grid-template-columns:repeat(3,minmax(0,1fr))}.tool-list code{padding:12px;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);overflow-wrap:anywhere}.spec-index{grid-template-columns:repeat(3,minmax(0,1fr))}.spec-index a{min-width:0;color:var(--text);text-decoration:none}.spec-index span{display:block;color:var(--muted);margin-top:6px}
.site-footer{padding:42px 0 28px;border-top:1px solid var(--line);color:var(--muted)}.footer-grid{display:grid;grid-template-columns:1.4fr repeat(3,.7fr);gap:28px}.footer-grid h2{font-size:14px;text-transform:uppercase;letter-spacing:.08em;color:var(--text)}.footer-grid a{display:block;width:fit-content;margin:7px 0;color:var(--muted);text-decoration:none}.footer-grid a:hover{color:var(--accent)}.footer-brand{margin-bottom:12px}.footer-bottom{display:flex;justify-content:space-between;gap:16px;padding-top:20px;margin-top:24px;border-top:1px solid var(--line);font-size:13px}@media(max-width:980px){.hero-grid,.two-column,.example-layout,.command-layout,.comparison-table{grid-template-columns:1fr}.core-map{grid-template-columns:repeat(2,minmax(0,1fr))}.principle-grid,.trust-matrix,.assessment-grid,.layer-stack,.spec-index,.tool-list,.evidence-ledger{grid-template-columns:repeat(2,minmax(0,1fr))}.trace-steps{grid-template-columns:repeat(2,minmax(0,1fr))}.footer-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:700px){.nav-shell{align-items:flex-start;flex-direction:column;padding:14px 0}.site-nav{justify-content:flex-start}.site-nav a{min-height:42px}h1{font-size:clamp(38px,14vw,56px)}.core-map,.principle-grid,.trust-matrix,.assessment-grid,.assessment-strip,.trace-steps,.footer-grid,.spec-index,.tool-list,.evidence-ledger{grid-template-columns:1fr}.comparison-demo{grid-template-columns:1fr}.footer-bottom{flex-direction:column}pre.code-block{font-size:12px}}@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;transition:none!important;animation:none!important}}
"""

JS = r"""
(() => {
  document.querySelectorAll('[data-copy-target]').forEach((button) => {
    button.addEventListener('click', async () => {
      const selector = button.getAttribute('data-copy-target');
      const target = selector ? document.querySelector(selector) : null;
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


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.strip() + "\n", encoding="utf-8")


def main() -> None:
    all_pages = dict(PAGES)
    for path, (title, description, kind, body) in EXTRA_PAGES.items():
        all_pages[path] = {
            "title": title,
            "description": description,
            "kind": kind,
            "body": body,
        }

    for path, meta in all_pages.items():
        write(
            path,
            render_page(
                path,
                meta["title"],
                meta["description"],
                meta["kind"],
                meta["body"],
            ),
        )
    write("assets/styles.css", CSS)
    write("assets/app.js", JS)
    write("assets/site-data.json", json.dumps(SITE_DATA, indent=2))
    write(
        "robots.txt",
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {BASE}sitemap.xml\n",
    )
    sitemap_pages = [
        "index.html",
        "why-aduc.html",
        "core.html",
        "validate.html",
        "compare.html",
        "trust.html",
        "evidence.html",
        "roadmap.html",
        "docs.html",
        "architecture.html",
        "example.html",
        "specification.html",
    ]
    urls = []
    for path in sitemap_pages:
        urls.append(f"  <url><loc>{page_url(path)}</loc><lastmod>{UPDATED}</lastmod></url>")
    write(
        "sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n",
    )
    write(
        "README.md",
        """# ADUC public website

Static source for the ADUC Working Draft public site.

Canonical public URL: https://bacoul.github.io/AI-Data-Understanding-Core-ADUC/

The site intentionally separates:

- available Core artifacts;
- active deterministic complete-Core formatting work;
- planned compiler, review UI, registry, MCP adapter, packages and extensions;
- not-yet-proven external multi-consumer evidence.

Run:

```bash
python -m unittest discover -s tests/website -p "test_*.py"
python tools/validate_website.py
```
""",
    )


if __name__ == "__main__":
    main()
