# ADUC Master Plan

- Status: Official execution plan
- Working name: AI Data Understanding Core (ADUC)
- Date: 2026-07-13
- Rule: complete phases in order unless an accepted ADR changes the order

## North-star outcome

A source publisher can attach one portable ADUC contract to JSON or CSV data. Independent AI systems can then identify the same concepts, units, time semantics, identity, provenance, uncertainty, relations, and use conditions without provider-specific semantic mappings.

## Program rules

1. Define the Core before broad implementation.
2. Document every normative decision.
3. Reuse established standards whenever possible.
4. Never promote automatic inference to authority silently.
5. Keep unsupported dimensions explicit and unresolved.
6. Use frozen inputs and reproducible evidence for demonstrations.
7. Do not claim success before two independent consumers pass.
8. Keep TimeProofs and the anticipation engine separate.
9. Keep the public website English-first.
10. Keep the working name provisional until naming checks are complete.
11. Require measurable user value before calling `infer` or `review` successful.

## Current reference-tested foundations

- semantic-mapping assertion model and validator;
- complete epistemic lifecycle;
- immutable source binding;
- unit identity and deterministic conversion;
- temporal semantics and timezone alignment;
- entity identity and safe equivalence;
- provenance and transformation lineage;
- JSON-LD/RDF round-trip;
- provider-neutral multi-model conformance harness;
- English static website deployed through GitHub Pages and Vercel.

Interpretation:

> The repository contains real, tested Core components, but it does not yet contain the normative full-Core object model or schema family.

## Phase 0 — Core definition

### Objective

Freeze the mission, boundaries, fundamental profiles, official roadmap, and one complete example before implementing the full-Core JSON Schema.

### Completed

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
- [x] adoption and value-validation plan;
- [x] English public website.

### Remaining

- [ ] uncertainty and data-quality profile;
- [ ] general relation profile boundary;
- [ ] policy and permitted-use profile boundary;
- [ ] normative Core object model and modular schema boundaries;
- [ ] one complete example validated against the candidate Core schema;
- [ ] name and trademark research before public name freeze.

### Exit gate

Phase 0 passes only when an independent developer can explain every Core block, its relationship to existing standards, and the deterministic consumer behavior for unknown or unsafe information.

## Phase 1 — Standard v0.1

### Objective

Convert the full-Core working draft into a coherent, reviewable specification and schema family.

### Deliverables

- [ ] normative Core object model;
- [ ] `schema/aduc-core.schema.json`;
- [ ] justified modular schemas for resource, semantics, identity, context, provenance, uncertainty, relations, and policy;
- [ ] Core JSON-LD vocabulary;
- [ ] versioning and migration rules;
- [ ] extension discovery rules;
- [ ] ten complete valid examples;
- [ ] ten intentionally invalid examples;
- [ ] migration design from the current mapping-profile format.

### Exit gate

Every official valid example passes and every official invalid example fails for the documented reason.

## Phase 2 — Reference implementation

### Objective

Provide deterministic local tooling for the complete Core.

### Deliverables

- [ ] full-Core CLI validator;
- [ ] stable error catalogue;
- [ ] Core formatter;
- [ ] unified comparator across concepts, units, time, identity, provenance, uncertainty, relations, and policy;
- [ ] TypeScript SDK;
- [ ] Python SDK;
- [ ] complete conformance runner;
- [ ] package publication plan;
- [ ] updated “Try in 5 minutes” documentation.

### Exit gate

A developer can install the tools, validate a complete contract, and compare the reference sources without maintainer assistance.

## Phase 3 — JSON/CSV compiler

### Objective

Generate provisional ADUC contracts from existing JSON and CSV sources.

```text
Source import
    ↓
Structural inspection
    ↓
Field profiling
    ↓
Concept and unit proposals
    ↓
Time and identity proposals
    ↓
Available provenance and uncertainty extraction
    ↓
Ambiguity and contradiction report
    ↓
Provisional inferred contract
```

### Deliverables

- JSON and CSV importers;
- primitive type and date/time detection;
- unit and identifier candidates;
- semantic proposals;
- declared inference evidence modes;
- method-bound, calibrated confidence;
- provenance references;
- deterministic export;
- no silent promotion beyond `inferred`.

### Exit gate

The compiler creates a structurally valid provisional contract for reference JSON and CSV sources and reports every unresolved field or unsupported assumption.

## Phase 4 — Review interface

### Objective

Show only the uncertain, unknown, conflicting, or unsafe parts of a contract.

### Deliverables

- unknown-field queue;
- low-confidence mapping queue;
- ambiguous-unit queue;
- temporal interpretation review;
- identity-match review;
- provenance-gap review;
- uncertainty and quality review;
- contradiction review;
- immutable review decisions;
- publisher-authority flow;
- portable final export.

### Exit gate

A reviewer can turn a provisional contract into reviewed or canonical assertions without rewriting published history.

## Phase 5 — Value and interoperability proof

### Controlled comparisons

1. manual mapping versus `infer + review`;
2. sources without ADUC versus the same sources with ADUC;
3. at least two independent AI consumers using one frozen full-Core package.

### Initial value gate

- median assisted human time at least 30% lower than manual mapping;
- final correctness not lower than the manual baseline;
- no critical false mapping silently accepted;
- uncertainty and unsupported conclusions remain visible.

### Reference scenario

- French source with Celsius and local date format;
- US source with Fahrenheit and UTC timestamp;
- different field names;
- possible but unproven equipment identity;
- complete transformation provenance;
- explicit uncertainty and permitted-use behavior.

### Deliverables

- [x] provider-neutral harness foundation;
- [x] frozen package foundation;
- [ ] upgraded full-Core package;
- [ ] manual and assisted benchmark evidence;
- [ ] with-ADUC and without-ADUC evidence;
- [ ] external run A;
- [ ] external run B from an independent provider or implementation;
- [ ] raw-output hashes;
- [ ] normalized results;
- [ ] deterministic comparison report;
- [ ] public reproduction instructions.

### Exit gate

The evaluator reports two qualifying independent runs with semantic agreement and the value benchmark passes without hidden mappings.

## Phase 6 — First extension

Build only after the Core passes the interoperability gate.

Candidate:

- Dataset Extension; or
- Live Data Extension.

Choose using validated user need, minimal Core impact, domain reuse, and demonstrability.

## Phase 7 — Situation & Action extension

Represent situations, possible developments, actions, constraints, and evidence without embedding a complete decision engine into the Core.

## Phase 8 — Anticipation engine

The separately versioned application demonstrates:

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
- independent-governance transition.

## Version 0.1 scoreboard

| Deliverable | Status |
|---|---|
| Core specification | Working draft |
| Fundamental profiles through provenance | Reference-tested |
| Uncertainty profile | Next action |
| General relations and policy | Not implemented |
| Full-Core JSON Schema | Not implemented |
| Ten valid full-Core examples | Not implemented |
| Ten invalid full-Core examples | Not implemented |
| Full-Core validator | Partial profile tools only |
| JSON/CSV compiler | Not implemented |
| Review UI | Not implemented |
| Unified comparator | Not implemented |
| Two-model proof | Harness exists; external proof absent |
| Value benchmark | Defined; not run |
| Try in 5 minutes | Available for current tools |

## Immediate execution sequence

### Milestone B — Complete Core decisions

1. [x] accept lifecycle ADR;
2. [x] accept source-binding ADR;
3. [x] accept unit ADR;
4. [x] accept temporal ADR;
5. [x] accept identity ADR;
6. [x] accept provenance ADR;
7. [ ] accept uncertainty and data-quality ADR;
8. [ ] define general relations and policy boundaries;
9. [ ] freeze modular schema boundaries;
10. [ ] implement the first full-Core schema.

### Milestone C — Examples and validator migration

1. create ten valid examples;
2. create ten invalid examples;
3. extend the validator;
4. publish compatibility or migration tooling.

### Milestone D — Compiler and review

1. JSON importer;
2. CSV importer;
3. inference proposal model;
4. minimal review interface;
5. benchmark review tax and value;
6. final export.

### Milestone E — Full proof

1. upgrade the frozen package;
2. compare without ADUC and with ADUC;
3. run two independent consumers;
4. publish raw and normalized evidence;
5. accept, revise, narrow, or stop based on results.

## Stop and pivot rules

Narrow, revise, or stop a feature when:

- it duplicates an established standard without measurable integration value;
- independent implementers cannot use it from the specification;
- AI consumers interpret the same conforming contract incompatibly;
- uncertainty is lost or silently upgraded;
- the Core absorbs domain logic better suited to extensions;
- adoption requires a proprietary hosted service;
- assisted mapping does not beat the manual baseline.

## Definition of progress

Progress means passing reproducible gates, not adding pages, fields, or claims.
