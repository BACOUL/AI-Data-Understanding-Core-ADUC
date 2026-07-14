# ADUC Master Plan

- Status: Official execution plan
- Working name: AI Data Understanding Core — ADUC
- Date: 2026-07-14
- Rule: complete phases in order unless an accepted ADR changes the order

## North-star outcome

A source publisher can attach one portable ADUC contract to JSON or CSV data. Independent AI systems can then identify the same concepts, units, time semantics, identity, provenance, uncertainty, relations, and use conditions without provider-specific semantic mappings.

## Program rules

1. Define the Core before broad implementation.
2. Document every normative decision.
3. Reuse established standards whenever possible.
4. Never promote automatic inference silently.
5. Preserve unknown, unsupported, conflicting, redacted, and prohibited information.
6. Use frozen inputs and reproducible evidence.
7. Do not claim interoperability before two independent consumers pass.
8. Keep TimeProofs and the anticipation engine separate.
9. Keep the public website English-first.
10. Keep the working name provisional.
11. Require measurable user value before compiler success claims.

## Current baseline

Implemented reference foundations:

- semantic-mapping assertion model, schema, validator, and comparator;
- JSON-LD context and deterministic RDF round-trip;
- provider-neutral multi-model harness;
- epistemic lifecycle;
- immutable source binding;
- units and deterministic conversion;
- temporal semantics and timezone alignment;
- entity identity and safe equivalence;
- provenance and transformation lineage;
- uncertainty, missingness, censoring, propagation, and DQV-compatible quality;
- general relation semantics and deterministic graph safeguards;
- ODRL-aligned policy and permitted-use conditions;
- governance, CI, execution ledger, English website, GitHub Pages, and Vercel deployment.

These are reference implementations of selected Core behavior, not yet the complete ADUC Core envelope.

# Phase 0 — Full-Core definition

## Objective

Freeze the mission, boundaries, fundamental profiles, official roadmap, normative Core object model, and one complete example before implementing the full-Core JSON Schema.

## Completed

- [x] mission and non-goals;
- [x] prior-art matrix;
- [x] official project structure;
- [x] full-Core working draft;
- [x] first informative ten-block example;
- [x] epistemic lifecycle;
- [x] source-binding profile;
- [x] unit profile;
- [x] temporal profile;
- [x] identity profile;
- [x] provenance profile;
- [x] uncertainty and data-quality profile;
- [x] general relation profile;
- [x] policy and permitted-use profile;
- [x] adoption and value-validation plan;
- [x] English public website.

## Remaining

- [ ] normative Core object model and modular boundaries;
- [ ] complete example aligned with the frozen object model;
- [ ] name and trademark research before public name freeze.

## Exit gate

An independent developer can explain every Core block, its relationship to existing standards, its ownership and references, and the deterministic behavior for unknown, unsafe, prohibited, or incomplete information.

# Phase 1 — Standard v0.1

## Objective

Convert the accepted profiles and frozen object model into a coherent, reviewable specification and schema family.

## Deliverables

- [ ] normative Core object model;
- [ ] `schema/aduc-core.schema.json`;
- [ ] justified modular schemas for resource, semantics, identity, context, provenance, uncertainty, relations, and policy;
- [ ] Core JSON-LD vocabulary;
- [ ] versioning and migration rules;
- [ ] extension discovery rules;
- [ ] ten complete valid examples;
- [ ] ten intentionally invalid examples;
- [ ] migration design from the current mapping-profile format.

## Exit gate

Every official valid example passes and every official invalid example fails for the documented reason.

# Phase 2 — Reference implementation

## Objective

Provide deterministic local tooling for the complete Core.

## Deliverables

- [ ] full-Core CLI validator;
- [ ] stable unified error catalogue;
- [ ] contract formatter;
- [ ] unified comparator across concepts, units, time, identity, provenance, uncertainty, relations, and policy;
- [ ] TypeScript SDK;
- [ ] Python SDK;
- [ ] conformance runner;
- [ ] package publication plan;
- [ ] updated “Try in 5 minutes” guide.

## Exit gate

A developer can install the tools, validate a complete contract, and compare two example sources without maintainer assistance.

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

## Exit gate

The compiler generates valid provisional contracts for the reference JSON and CSV examples and reports every unresolved field and policy gap.

# Phase 4 — Review interface

## Objective

Let a reviewer inspect only uncertain, unsupported, conflicting, prohibited, or incomplete parts.

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
- [ ] raw-output hashes;
- [ ] normalized results;
- [ ] deterministic comparison report;
- [ ] public reproduction instructions.

## Exit gate

- at least 30% lower median assisted human time without lower final correctness;
- no critical false mapping silently accepted;
- two independent consumers qualify and agree without hidden mappings.

# Later phases

## Phase 6 — First extension

Build Dataset or Live Data only after the Core passes the value and interoperability gate.

## Phase 7 — Situation & Action extension

Represent situations, possible developments, actions, constraints, and evidence without turning the Core into a decision engine.

## Phase 8 — Anticipation engine

A separately governed application using:

```text
ADUC Core
+ Live Data Extension
+ Situation & Action Extension
```

## Phase 9 — Ecosystem

- public and private semantic registries;
- community extensions;
- connectors and optional MCP adapter;
- certification;
- professional support;
- independent governance transition.

# Public website rules

- no claim that ADUC is recognized or adopted;
- no claim that multi-model interoperability is already proven;
- no claim that policy evaluation is legal advice or access-control enforcement;
- working-name disclaimer remains visible;
- implementation status remains accurate;
- mobile-first and accessible;
- no dependency on a proprietary SaaS.

# Immediate execution sequence

1. Freeze the normative Core object model and modular boundaries.
2. Align the complete example with the frozen model.
3. Implement the schema family.
4. Create ten complete valid and ten invalid examples.
5. Build the unified validator and comparator.
6. Build compiler and review tooling.
7. Run value and multi-model proofs.

# Stop and pivot rules

Narrow, revise, or stop a feature when:

- it duplicates an established standard without measurable integration value;
- independent implementers cannot use it from the specification;
- independent consumers interpret conforming contracts incompatibly;
- uncertainty is lost or silently upgraded;
- relation semantics or permissions are invented;
- domain logic is forced into the Core instead of an extension;
- adoption requires a proprietary hosted service;
- assisted mapping is not measurably better than the manual baseline.

# Definition of progress

Progress means passing reproducible gates, not adding pages, fields, or claims.
