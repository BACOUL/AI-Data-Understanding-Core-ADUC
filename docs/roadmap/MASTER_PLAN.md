# ADUC Master Plan

- Status: Official execution plan
- Working name: AI Data Understanding Core (ADUC)
- Date: 2026-07-13
- Rule: complete phases in order unless an accepted ADR changes the order

## North-star outcome

A source publisher can attach one portable ADUC contract to JSON or CSV data. Independent AI systems can then identify the same concepts, units, time semantics, provenance, uncertainty, relations, and use conditions without provider-specific semantic mappings.

## Program rules

1. The Core is defined before broad implementation.
2. Every normative decision is documented.
3. Existing standards are reused whenever possible.
4. Automatic inference never becomes authoritative silently.
5. Unsupported dimensions remain explicit and unresolved.
6. Demonstrations use frozen inputs and reproducible evidence.
7. The project does not claim success before two independent consumers pass.
8. TimeProofs and the anticipation engine remain separate projects.
9. The public website is English-first.
10. The working name remains provisional.

## Current baseline

Already implemented in the repository:

- semantic-mapping assertion model;
- experimental mapping-profile JSON Schema;
- valid and invalid fixtures;
- CLI validator;
- semantic conflict checks;
- authoring lifecycle examples;
- deterministic semantic comparator;
- JSON-LD context and RDF round-trip;
- provider-neutral multi-model conformance harness.

Interpretation:

> The current code is valuable, but it implements mainly the semantic-mapping and consumer-conformance subset. It does not yet implement the complete ADUC Core envelope.

## Phase 0 — Definition

### Objective

Freeze the mission, boundaries, full Core blocks, official roadmap, and one complete example.

### Deliverables

- [x] project mission;
- [x] non-goals;
- [x] prior-art matrix;
- [x] official project structure;
- [x] `spec/ADUC_CORE_SPEC_0_1.md` working draft;
- [ ] normative ADR for the seven-state epistemic model;
- [ ] normative ADR for source description profiles;
- [ ] one complete full-Core example validated against the candidate model;
- [ ] name and trademark availability research before public name freeze.

### Exit gate

Phase 0 passes only when an independent developer can read the Core draft and explain every block, its purpose, and its relationship to existing standards.

## Phase 1 — Standard v0.1

### Objective

Convert the full-Core working draft into a coherent, reviewable specification and schema family.

### Deliverables

- [ ] normative Core object model;
- [ ] `schema/aduc-core.schema.json`;
- [ ] modular resource, semantics, identity, context, provenance, uncertainty, relation, and policy schemas where justified;
- [ ] Core JSON-LD vocabulary;
- [ ] unit strategy;
- [ ] time and timezone strategy;
- [ ] entity identity strategy;
- [ ] versioning rules;
- [ ] extension discovery rules;
- [ ] ten complete valid examples;
- [ ] ten intentionally invalid examples;
- [ ] migration design from the current mapping-profile format.

### Exit gate

All official examples pass the schema and every invalid example fails for the documented reason.

## Phase 2 — Reference implementation

### Objective

Provide deterministic local tooling for the complete Core.

### Deliverables

- [ ] full-Core CLI validator;
- [ ] stable error catalogue;
- [ ] Core contract formatter;
- [ ] comparator including concepts, units, time, and identity uncertainty;
- [ ] TypeScript SDK;
- [ ] Python SDK;
- [ ] conformance test runner;
- [ ] package publication plan;
- [ ] "Try in 5 minutes" documentation.

### Exit gate

A developer can install the tools, validate a contract, and compare two example sources without maintainer assistance.

## Phase 3 — JSON/CSV compiler

### Objective

Create provisional ADUC contracts from existing JSON and CSV sources.

### Compiler pipeline

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
Ambiguity and contradiction report
    ↓
Provisional inferred contract
```

### Deliverables

- [ ] JSON importer;
- [ ] CSV importer;
- [ ] primitive type inference;
- [ ] date/time detection;
- [ ] unit detection;
- [ ] identifier candidate detection;
- [ ] semantic concept proposal interface;
- [ ] method-bound confidence scores;
- [ ] evidence references;
- [ ] deterministic export;
- [ ] no silent promotion beyond `inferred`.

### Exit gate

The compiler generates a structurally valid provisional contract for the reference JSON and CSV examples and reports all unresolved fields.

## Phase 4 — Review interface

### Objective

Allow a human reviewer to inspect only the uncertain or conflicting parts of a contract.

### Deliverables

- [ ] unknown-field queue;
- [ ] low-confidence mapping queue;
- [ ] ambiguous-unit queue;
- [ ] time interpretation review;
- [ ] identity match review;
- [ ] contradiction review;
- [ ] immutable review decisions;
- [ ] source-authority publication flow;
- [ ] portable final export.

### Exit gate

A reviewer can turn a provisional contract into reviewed or canonical assertions without editing published history in place.

## Phase 5 — Interoperability demonstration

### Objective

Prove that the same contracts produce compatible understanding in two independent AI consumers.

### Reference scenario

- French machine source with Celsius and local date format;
- US machine source with Fahrenheit and UTC timestamp;
- different field names;
- possible but unproven equipment identity.

### Required conclusions

- equivalent temperature concept;
- explicit Celsius/Fahrenheit conversion;
- same instant after timezone interpretation;
- identity remains uncertain without evidence;
- uncertainty and epistemic status preserved.

### Deliverables

- [x] provider-neutral harness foundation;
- [x] frozen input package foundation;
- [ ] full-Core package including unit, time, and identity semantics;
- [ ] external run A;
- [ ] external run B from a distinct provider or implementation;
- [ ] raw-output hashes;
- [ ] normalized result files;
- [ ] deterministic comparison report;
- [ ] public reproducibility instructions.

### Exit gate

The evaluator reports two qualifying independent runs and semantic agreement without hidden mappings.

## Phase 6 — First extension

Build only after the Core passes the interoperability gate.

Candidate first extension:

- Dataset Extension; or
- Live Data Extension.

Selection criteria:

- strongest validated user need;
- lowest Core impact;
- reusable across domains;
- demonstrable with public examples.

## Phase 7 — Situation & Action extension

### Objective

Represent situations, possible developments, actions, constraints, and evidence without embedding a complete decision engine into the Core.

### Gate

This phase starts only after at least one earlier extension has passed conformance and external use.

## Phase 8 — Anticipation engine

The anticipation engine becomes the first major application demonstrating:

```text
ADUC Core
+ Live Data Extension
+ Situation & Action Extension
```

It remains separately versioned, separately governed, and optional.

## Phase 9 — Ecosystem

### Deliverables

- public semantic registry;
- private registry option;
- community extensions;
- connectors;
- certification program;
- professional support;
- independent governance transition plan.

## Public website plan

### Version 1 website

English-only static site containing:

- Home;
- Specification;
- Architecture;
- Roadmap;
- Complete Example;
- Try in 5 Minutes;
- GitHub and contribution links.

### Website constraints

- no claim that ADUC is a recognized standard;
- no claim that multi-model interoperability is already proven;
- working-name disclaimer visible;
- accurate implementation status;
- mobile-first and accessible;
- no dependency on a commercial SaaS.

### Later website additions

- interactive validator;
- compiler demo;
- review UI;
- registry browser;
- conformance dashboard;
- release and governance pages.

## Version 0.1 completion scoreboard

| Deliverable | Status |
|---|---|
| Core specification | Draft created |
| Official full-Core JSON Schema | Not implemented |
| 10 valid full-Core examples | Not implemented |
| 10 invalid full-Core examples | Not implemented |
| CLI validator | Partial: mapping profile only |
| JSON/CSV compiler | Not implemented |
| Minimal review UI | Not implemented |
| Core vocabulary | Partial: mapping context only |
| Two-source comparison | Partial: semantic target comparison only |
| Two-model demonstration | Harness exists; external proof absent |
| Conformance suite | Partial: mapping profile and harness |
| Try in 5 minutes | Website first version in progress |

## Immediate execution sequence

### Milestone A — Official foundation and website

1. Publish the full-Core draft.
2. Publish the official structure and master plan.
3. Add one complete example.
4. Add the English website.
5. Update README and status files.

### Milestone B — Full-Core schema design

1. Accept lifecycle ADR.
2. Accept units ADR.
3. Accept temporal ADR.
4. Accept identity ADR.
5. Define the modular schema boundaries.
6. Implement the first full-Core schema.

### Milestone C — Full-Core examples and validator migration

1. Create ten valid examples.
2. Create ten invalid examples.
3. Extend the validator.
4. Preserve compatibility or publish migration tooling for the mapping profile.

### Milestone D — Compiler and review

1. JSON importer.
2. CSV importer.
3. inference proposal model.
4. minimal review interface.
5. final export.

### Milestone E — Full interoperability proof

1. upgrade the frozen package;
2. run two independent consumers;
3. publish raw and normalized evidence;
4. accept or revise the Core based on results.

## Stop and pivot rules

The project must narrow, revise, or stop a proposed feature when:

- it merely duplicates an established standard without measurable integration value;
- independent implementers cannot use it from the specification;
- multiple AI consumers interpret the same conforming contract incompatibly;
- uncertainty is lost or silently upgraded;
- the Core grows to include domain logic better suited to extensions;
- adoption requires a proprietary hosted service.

## Definition of progress

Progress means passing reproducible gates, not adding pages, fields, or claims.
