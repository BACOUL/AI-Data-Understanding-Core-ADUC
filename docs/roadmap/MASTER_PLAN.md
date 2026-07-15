# ADUC Master Plan

- Status: Official execution plan
- Working name: AI Data Understanding Core — ADUC
- Date: 2026-07-15
- Rule: complete technical phases in order unless an accepted ADR changes the order
- Program rule: every phase is also subject to the cross-cutting coverage matrix and evidence gates

## North-star outcome

A source publisher can attach one portable ADUC contract to JSON or CSV data. Independent AI systems can then identify the same concepts, units, time semantics, identity, provenance, uncertainty, relations and use conditions without provider-specific semantic mappings.

The long-term product must remain usable by machines and humans, testable by independent implementations, secure and private by default, internationally usable, publicly discoverable and governed in a way that supports adoption without weakening the Core.

## Program rules

1. Define the Core before broad implementation.
2. Document every normative decision.
3. Reuse established standards whenever possible.
4. Never promote automatic inference silently.
5. Preserve unknown, unsupported, conflicting, redacted and prohibited information.
6. Use frozen inputs and reproducible evidence.
7. Do not claim interoperability before two independent consumers pass.
8. Keep TimeProofs and the anticipation engine separate.
9. Keep the public website English-first while designing for internationalization.
10. Keep the working name provisional until naming and trademark research is complete.
11. Require measurable user value before compiler success claims.
12. Treat AI-first as machine-actionable and provider-neutral, never as AI-only.
13. Preserve human review, contestability and understandable diagnostics for consequential decisions.
14. Apply privacy by design and by default to tools, examples, telemetry and hosted services.
15. Apply security by design to contracts, extensions, dependencies, builds and AI-facing projections.
16. Do not close a phase until every applicable cross-cutting requirement has evidence or an explicit deferred decision.
17. Do not make a “first in the world” claim without a dated claim boundary, prior-art record, independent review and reproducible implementation evidence.

## Program structure

The technical phases remain sequential. Five program tracks run across them.

```text
Track A — Standard and reference engine
Track B — AI-first and human-first product
Track C — Trust, safety and conformance
Track D — Visibility, distribution and adoption
Track E — First-world proof, identity and governance
```

The tracks do not authorize out-of-order implementation. They ensure that product, trust and adoption requirements are designed early and delivered at the correct phase.

## Track A — Standard and reference engine

Purpose:

- define the normative Core and extensions;
- provide schemas, validators, comparators, formatters and SDKs;
- compile existing sources into provisional contracts only after value gates permit it;
- maintain deterministic behavior, stable diagnostics and compatibility rules.

Mandatory evidence:

- accepted ADRs;
- positive and negative fixtures;
- offline reproducibility;
- stable machine-readable reports;
- version and migration tests;
- independent conformance results before stable 1.0.

## Track B — AI-first and human-first product

Purpose:

- make every normative artifact machine-readable and directly consumable by AI systems;
- keep every critical result inspectable and reviewable by humans;
- provide CLI, SDKs, documentation, playground, compiler and review interface in the correct phases.

AI-first requirements:

- provider-neutral inputs and outputs;
- deterministic JSON reports and stable codes;
- explicit capability and profile declarations;
- no hidden prompt-only semantics;
- projections that preserve provenance, uncertainty, policy and unknown states;
- conformance tests for AI consumers;
- no mandatory remote model dependency for Core validation.

Human-first requirements:

- readable diagnostics and remediation guidance;
- review queues limited to uncertain, unsupported, conflicting, prohibited or incomplete facts;
- immutable review decisions and visible history;
- accessible interfaces and documentation;
- explicit responsibility boundaries and no fabricated certainty.

## Track C — Trust, safety and conformance

Purpose:

- make privacy, security, accessibility, internationalization, reliability and independent conformance part of the product definition rather than late audits.

Required programs:

1. Privacy by design and by default
   - local processing by default;
   - data minimization;
   - no silent upload, retention, telemetry or model training;
   - explicit retention, deletion and export behavior for hosted services;
   - separation of source content, contract metadata, logs and analytics;
   - redaction and personal-data handling tests;
   - privacy impact review before any hosted upload workflow.

2. Security by design
   - threat model for contracts, descriptions, extensions and AI projections;
   - prompt-injection and malicious-description handling;
   - limits for size, depth, graph cycles and resource consumption;
   - no unapproved remote schema or vocabulary loading;
   - dependency review, SBOM and vulnerability disclosure process;
   - signed or attestable releases and build provenance when packages are published;
   - fuzzing and adversarial fixtures before stable release.

3. Unknown-safe and failure-safe behavior
   - absence is never silently converted to false, exact, permitted or safe;
   - unknown, indeterminate, contested, deprecated, prohibited and review-required states remain distinct;
   - partial failures degrade explicitly instead of producing trusted output;
   - unsafe indexing, merging, conversion or policy evaluation is blocked.

4. Accessibility and internationalization
   - target WCAG 2.2 AA for public and review interfaces;
   - keyboard, contrast, focus, error and screen-reader testing;
   - Unicode, locale, number, date, timezone, unit and directionality support;
   - identifiers remain language-independent;
   - translations are versioned and never redefine normative meaning.

5. Reliability, observability and sustainability
   - deterministic offline Core operations;
   - performance and memory budgets;
   - privacy-preserving logs and metrics for hosted services;
   - service objectives, incident handling and recovery plans when hosting begins;
   - cost measurement for model calls, storage and execution;
   - graceful degradation when optional external services fail.

6. Independent conformance
   - separate conformance classes for contracts, producers, validators, comparators, compilers, consumers and extensions;
   - normative requirement-to-test traceability;
   - at least one independent implementation before stable 1.0;
   - implementation report with passes, failures, optional features and known divergences;
   - no implementation may define the specification solely through its own behavior.

## Track D — Visibility, distribution and adoption

Purpose:

- make ADUC understandable, discoverable, installable and testable without weakening technical gates.

Required programs:

1. Website and documentation
   - clear home page and problem statement;
   - specification, architecture, standards reused, security, privacy, governance and roadmap pages;
   - versioned documentation and release notes;
   - “Try in 5 minutes” guide;
   - downloadable examples, reports and conformance fixtures;
   - playground only after safe local validation paths exist;
   - case studies and reproducible evidence after qualification.

2. SEO, AEO and GEO
   - target real problem queries, not only the unknown ADUC name;
   - stable crawlable URLs, sitemap, canonical metadata and structured data;
   - explicit definitions, question-answer pages, comparison pages and cited technical evidence;
   - machine-readable specification and downloadable raw artifacts;
   - test visibility across search engines, answer engines and generative systems;
   - record query sets, dates, languages and observed citations instead of claiming guaranteed ranking;
   - prevent marketing language from outrunning evidence.

3. Developer experience and distribution
   - Python and TypeScript SDKs with aligned behavior;
   - package publication plan, signed releases and compatibility policy;
   - GitHub Releases, PyPI and npm when release gates pass;
   - complete examples and copy-paste commands;
   - actionable errors and migration guides;
   - support and issue-triage expectations.

4. Adoption and validation
   - external developer usability tests;
   - pilots with explicit success and stop criteria;
   - manual versus assisted authoring benchmark;
   - review-tax measurement;
   - with-ADUC versus without-ADUC comparison;
   - public case studies only with permission and reproducible evidence.

## Track E — First-world proof, identity and governance

Purpose:

- define what is genuinely new, protect defensible identity and establish trustworthy governance.

Required programs:

1. Prior-art and claim boundary
   - maintain a dated matrix of standards, products, papers, repositories and patents;
   - define each proposed novelty claim precisely;
   - state what ADUC does not claim to have invented;
   - review the matrix before major public announcements and stable releases;
   - obtain independent legal or specialist review before using an absolute “first in the world” claim.

2. Reproducible first-world evidence
   - complete open specification and reference implementation;
   - frozen test package;
   - independent validator or consumer implementation;
   - two independent AI consumers using the same complete Core contract;
   - raw outputs, hashes, normalized results and public reproduction instructions;
   - evidence that the consumers preserve meaning, unknowns, uncertainty, provenance and policy without hidden mappings.

3. Naming and intellectual property
   - naming and trademark research before name freeze;
   - clear licenses for code, specification, examples and conformance tests;
   - patent policy for contributors and implementers;
   - provenance and license review for reused vocabularies and datasets;
   - no claim that a schema alone prevents copying.

4. Governance
   - documented contribution and decision process;
   - change control, errata, objections and appeals;
   - extension registration and namespace policy;
   - conflict-of-interest handling;
   - transition path toward broader or independent governance only when adoption justifies it.

## Cross-cutting gate

Every milestone PR must complete the review defined in:

```text
docs/roadmap/CROSS_CUTTING_COVERAGE_MATRIX.md
```

Each applicable requirement must identify:

- phase and track;
- deliverable;
- tests;
- evidence;
- status;
- owner or responsible role;
- reassessment trigger.

Allowed statuses:

```text
notStarted
planned
inProgress
implemented
verified
deferredWithReason
notApplicableWithReason
```

A missing entry is not equivalent to `notApplicable`.

## Standard maturity path

```text
Working Draft
    ↓
Alpha Specification
    ↓
Candidate Specification
    ↓
Implementation Report
    ↓
Stable 1.0
```

### Working Draft

- normative decisions may change;
- no compatibility promise;
- examples and counterexamples are required.

### Alpha Specification

- Core shape and reports are implemented;
- breaking changes remain possible and documented;
- package publication may be experimental.

### Candidate Specification

- conformance classes and complete test suite are frozen for review;
- at least two implementations or consumers are available;
- unresolved interoperability defects block advancement.

### Implementation Report

- independent results are published;
- optional and required behavior is separated;
- known divergences and errata are explicit.

### Stable 1.0

- compatibility, deprecation, errata and governance policies are active;
- independent implementation evidence exists;
- security, privacy, accessibility and licensing gates have passed;
- claims are limited to demonstrated evidence.

## Current baseline

Implemented reference foundations:

- semantic-mapping assertion model, schema, validator and comparator;
- JSON-LD context and deterministic RDF round-trip;
- provider-neutral multi-model harness;
- epistemic lifecycle;
- immutable source binding;
- units and deterministic conversion;
- temporal semantics and timezone alignment;
- entity identity and safe equivalence;
- provenance and transformation lineage;
- uncertainty, missingness, censoring, propagation and DQV-compatible quality;
- general relation semantics and deterministic graph safeguards;
- ODRL-aligned policy and permitted-use conditions;
- normative ten-block Core object model and module manifest;
- complete object-model example and architectural checker;
- official modular Core JSON Schema family;
- unified full-Core validator and deterministic comparator;
- deterministic semantic-profile migration into complete Core contracts;
- deterministic complete-contract formatter;
- governance, CI, execution ledger, English website, GitHub Pages and Vercel deployment.

# Phase 0 — Full-Core definition

## Objective

Freeze the mission, boundaries, fundamental profiles, normative Core object model, module dependencies, extension rules and one complete example before implementing the full-Core JSON Schema family.

## Completed

- [x] mission and non-goals;
- [x] prior-art matrix;
- [x] official project structure;
- [x] full-Core working draft;
- [x] epistemic lifecycle;
- [x] source-binding profile;
- [x] unit profile;
- [x] temporal profile;
- [x] identity profile;
- [x] provenance profile;
- [x] uncertainty and data-quality profile;
- [x] general relation profile;
- [x] policy and permitted-use profile;
- [x] normative Core object model and modular boundaries;
- [x] machine-readable module manifest;
- [x] complete example aligned with the frozen object model;
- [x] architectural counterexamples and deterministic checker;
- [x] adoption and value-validation plan;
- [x] English public website.

## Remaining external prerequisite

- [ ] name and trademark research before public name freeze.

## Cross-cutting requirements

- define the initial novelty claim boundary;
- record licenses and provenance for reused standards;
- establish privacy/security assumptions and non-goals;
- keep public claims at Working Draft level.

## Exit gate

An independent developer can identify every Core block, required cardinality, owning module, reference direction, external-standard boundary, extension behavior and deterministic response to missing or unsafe information.

# Phase 1 — Standard v0.1 schema family

## Objective

Translate the accepted profiles and frozen object model into a coherent Draft 2020-12 schema family and complete fixtures.

## Deliverables

- [x] `schema/aduc-core.schema.json`;
- [x] root envelope and metadata schemas;
- [x] modular schemas for resource, structure, semantics, identity, context, provenance, uncertainty, relations and policy;
- [x] reusable qualification and extension schemas;
- [x] at least ten complete valid examples;
- [x] at least ten intentionally invalid examples;
- [x] local schema validator and stable error paths;
- [x] documented graph checks beyond JSON Schema;
- [x] migration fixtures from the standalone semantic-mapping profile.

## Cross-cutting requirements

- all operational references resolve locally;
- malicious and excessive JSON inputs fail safely;
- normative requirements map to positive and negative tests;
- schema and fixture licenses are explicit before package release;
- public documentation remains crawlable and versioned.

## Exit gate

Every official valid example passes and every official invalid example fails for the documented reason. An independent implementer can trace every schema property to ADR-0014 and the module manifest.

# Phase 2 — Reference implementation

## Objective

Provide deterministic local tooling for the complete Core.

## Deliverables

- [x] unified full-Core CLI validator;
- [x] stable unified error catalogue;
- [x] contract formatter;
- [x] unified comparator across concepts, units, time, identity, provenance, uncertainty, relations and policy;
- [ ] conformance runner;
- [ ] TypeScript SDK;
- [ ] Python SDK;
- [ ] package publication plan;
- [ ] updated “Try in 5 minutes” guide.

## Cross-cutting requirements

- CLI and SDK behavior must be provider-neutral and offline-capable;
- text and JSON diagnostics must remain human- and machine-readable;
- package threat model, SBOM and signing plan must precede public package claims;
- installation tests must cover supported Windows, Linux and macOS environments;
- independent-developer usability testing is required for the exit gate;
- documentation, SEO/AEO/GEO foundations and stable URLs must be maintained alongside releases.

## Exit gate

A developer can install the tools, validate a complete contract and compare two example sources without maintainer assistance.

# Phase 3 — JSON/CSV compiler

## Objective

Create provisional ADUC contracts from existing JSON and CSV sources.

```text
Source import
    ↓
Structural inspection
    ↓
Field profiling
    ↓
Concept, unit, time, identity, provenance, uncertainty and relation proposals
    ↓
Policy evidence capture without invented permission
    ↓
Ambiguity and contradiction report
    ↓
Provisional inferred contract
```

## Deliverables

- [ ] JSON importer;
- [ ] CSV importer;
- [ ] primitive type inference;
- [ ] date/time and unit detection;
- [ ] identifier candidate detection;
- [ ] semantic concept proposal interface;
- [ ] provenance and uncertainty evidence capture;
- [ ] relation candidates without unsafe closure;
- [ ] policy evidence capture without invented permission;
- [ ] method-bound confidence;
- [ ] deterministic export;
- [ ] no silent promotion beyond `inferred`.

## Cross-cutting requirements

- local processing is the default and upload is never required;
- source content is not retained or used for training without explicit consent;
- prompt injection and malicious cell values are treated as untrusted data;
- sensitive-data detection and redaction pathways are documented;
- inference confidence is method-bound and calibrated;
- compiler cost, latency and memory are measured;
- compiler success claims require the adoption and review-tax benchmark.

## Exit gate

The compiler generates valid provisional contracts for reference JSON and CSV examples and reports every unresolved field and policy gap.

# Phase 4 — Review interface

## Objective

Let a reviewer inspect only uncertain, unsupported, conflicting, prohibited or incomplete parts.

## Deliverables

- [ ] unknown-field queue;
- [ ] low-confidence mapping queue;
- [ ] ambiguous-unit queue;
- [ ] time interpretation review;
- [ ] identity match review;
- [ ] provenance-gap review;
- [ ] uncertainty and quality review;
- [ ] relation and policy conflict review;
- [ ] immutable review decisions;
- [ ] source-authority publication flow;
- [ ] portable final export.

## Cross-cutting requirements

- WCAG 2.2 AA target and assistive-technology testing;
- keyboard-complete workflows and understandable errors;
- privacy-preserving sessions, retention and deletion controls;
- role and responsibility boundaries without pretending ADUC grants legal authority;
- internationalized dates, units, languages and directionality;
- immutable, contestable and auditable review history.

## Exit gate

A reviewer can turn a provisional contract into reviewed or canonical assertions without rewriting history or inventing permissions.

# Phase 5 — Value and interoperability proof

## Reference scenario

- French machine source with Celsius and local date format;
- US machine source with Fahrenheit and UTC timestamp;
- different field names;
- possible but unproven equipment identity;
- explicit provenance and uncertainty;
- policies permitting the tested use.

## Required conclusions

- equivalent temperature concept;
- explicit Celsius/Fahrenheit conversion;
- same instant after timezone interpretation;
- identity remains uncertain without evidence;
- provenance and uncertainty remain visible;
- prohibited or unsupported use remains blocked.

## Deliverables

- [x] provider-neutral harness foundation;
- [x] frozen input-package foundation;
- [ ] manual mapping versus `infer + review` benchmark;
- [ ] review-tax report;
- [ ] with-ADUC versus without-ADUC comparison;
- [ ] full-Core frozen package;
- [ ] external run A;
- [ ] external run B from a distinct provider or implementation;
- [ ] deterministic non-LLM consumer baseline;
- [ ] repeated-run stability analysis;
- [ ] adversarial and unknown-state scenarios;
- [ ] raw-output hashes;
- [ ] normalized results;
- [ ] deterministic comparison report;
- [ ] independent evaluation review;
- [ ] public reproduction instructions;
- [ ] dated first-world claim dossier.

## Cross-cutting requirements

- publish failures and limitations, not only successful outputs;
- preserve privacy and usage rights of all source data;
- record model, version, configuration, date, prompts/projections and raw hashes;
- separate provider variation from ADUC conformance;
- test multiple languages and query reformulations where relevant;
- prohibit absolute novelty claims until the prior-art and independent-review gate passes.

## Exit gate

- at least 30% lower median assisted human time without lower final correctness;
- no critical false mapping silently accepted;
- two independent consumers qualify and agree without hidden mappings;
- at least one independent implementation or conformance review exists;
- the public novelty claim is limited to reproducibly demonstrated capabilities.

# Later phases

## Phase 6 — First extension

Build Dataset or Live Data only after the Core passes the value and interoperability gate.

Cross-cutting gate: extension namespace, threat model, privacy impact, compatibility, conformance tests and governance approval are mandatory.

## Phase 7 — Situation & Action extension

Represent situations, possible developments, actions, constraints and evidence without turning the Core into a decision engine.

Cross-cutting gate: preserve uncertainty, human responsibility and policy boundaries; no autonomous consequential action is authorized by the data model alone.

## Phase 8 — Anticipation engine

A separately governed application using:

```text
ADUC Core
+ Live Data Extension
+ Situation & Action Extension
```

It requires its own safety case, evaluation plan, privacy/security review and product governance. It is not part of the Core standard.

## Phase 9 — Ecosystem

- public and private semantic registries;
- community extensions;
- connectors and optional MCP adapter;
- certification;
- professional support;
- independent governance transition.

Cross-cutting gate: registry trust, package provenance, certification independence, ecosystem security, sustainable funding and conflict-of-interest controls.

## Current single active task

The only active technical task is the provider-neutral full-Core conformance runner for validator, comparator and formatter implementations, as defined in `docs/roadmap/NEXT_ACTION.md`.

The conformance runner must not be presented as independent proof merely because it passes the reference implementation. This Master Plan does not authorize the compiler, review UI, SaaS, MCP adapter, extensions, anticipation engine or external multi-model proof ahead of their gates.
