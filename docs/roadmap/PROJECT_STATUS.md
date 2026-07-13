# Project Status

- Project: AI Data Understanding Core (working name)
- Current phase: Phase 0 — Full-Core definition and public foundation
- Current release: unreleased
- Target release: `0.1.0-alpha.0`
- Overall status: full-Core mission, architecture, epistemic lifecycle, and adoption-value gates are defined; the official full-Core schema is not yet implemented

## Official direction

ADUC is an open, model-independent contract intended to let data describe:

```text
structure
semantics
identity
context
provenance
uncertainty
relations
policy
```

to AI systems, agents, and applications.

The complete candidate contract contains ten blocks:

```text
aduc
resource
structure
semantics
identity
context
provenance
uncertainty
relations
policy
```

`spec/ADUC_CORE_SPEC_0_1.md` is the authoritative full-Core working draft.

ADR-0004 preserves the existing semantic-mapping implementation as the first experimental subset of the `semantics` block. It is not the complete Core.

## Completed project foundation

- repository governance and contribution structure;
- project charter and non-goals;
- execution method and decision records;
- prior-art matrix covering thirteen standards and approaches;
- official project structure and master plan;
- complete full-Core working draft;
- ADR-0004 positioning the existing semantic profile inside the full Core;
- first informative ten-block full-Core example;
- English static public website source and GitHub Pages workflow;
- deterministic website and example validation;
- ADR-0005 complete epistemic lifecycle decision;
- `spec/EPISTEMIC_STATUS_MODEL_0_1.md`;
- nine reference lifecycle cases covering all seven effective states;
- eight rejected counterexamples;
- deterministic lifecycle evaluator and unit tests;
- official `docs/roadmap/ADOPTION_AND_VALUE_VALIDATION.md` plan;
- roadmap tests requiring the adoption plan to remain visible while source binding remains the next technical task.

## Accepted epistemic model

The seven effective states are not stored in one overloaded property.

| Concern | Full-Core representation |
|---|---|
| unresolved field | coverage record with `resolutionStatus: unknown` |
| assertion authority | `inferred`, `reviewed`, `verified`, or `canonical` |
| unresolved dispute | separate immutable challenge record producing `contested` |
| retired assertion | separate immutable deprecation record producing `deprecated` |

Key consequences:

- `reviewed` means accountable examination;
- `verified` requires a declared verification method and evidence;
- `canonical` requires recognized source authority and forbids confidence;
- open challenges block automatic use without erasing original authority;
- deprecated assertions remain historical and immutable;
- old `contested` mapping-profile assertions require explicit migration because their underlying authority state was not preserved.

## Accepted adoption and value-validation constraints

ADUC tools must be evaluated as tools, not assumed valuable because the specification is coherent.

Required future evidence includes:

- four declared inference modes: `structure-only`, `sample-assisted`, `documentation-assisted`, and `publisher-assisted`;
- method identifiers, versions, evidence references, and exact source bindings for every inferred proposal;
- no presentation of uncalibrated model self-confidence as probability;
- a manual mapping versus `infer + review` benchmark;
- a review-tax report measuring accepted, edited, rejected, unresolved, and false proposals;
- a controlled with-ADUC versus without-ADUC multi-model comparison;
- an initial alpha target of at least 30% lower median assisted human time without lower final correctness;
- no silently accepted critical false mapping in the reference benchmark;
- MCP treated as a future optional adapter, not a Core dependency.

These are cross-cutting gates. They do not replace source binding, Core conformance, or external interoperability proof.

## Completed experimental semantic-mapping implementation

- minimal semantic-mapping assertion model;
- immutable assertion lifecycle;
- implemented legacy statuses: `inferred`, `reviewed`, `canonical`, and `contested`;
- Draft 2020-12 semantic-mapping profile schema;
- four valid and ten invalid mapping fixtures;
- text and JSON CLI validator with stable error codes;
- duplicate-ID, lifecycle-cycle, canonical-conflict, and authority-warning checks;
- manual authoring and review workflow;
- deterministic semantic comparison protocol and CLI;
- French and US comparison examples;
- explicit `notEvaluated` behavior for absent unit, time, and identity dimensions;
- protected local JSON-LD context and RDF round-trip;
- provider-neutral multi-model conformance protocol, frozen package, result schema, and evaluator.

## Evidence-based findings

- Existing standards cover most individual capabilities and must be reused rather than duplicated.
- Croissant is a strong dataset-description foundation but does not alone provide the complete ADUC consumer contract.
- Comparable semantic targets alone do not establish units, time alignment, or entity identity.
- Unknown, inferred, contested, and deprecated information must not be silently upgraded or hidden.
- Authority, verification, probability, conflict, and lifecycle are separate claims.
- JSON Schema cannot prove publisher authority, factual truth, global identity, or legal permission.
- A frozen multi-model harness can test agreement, but illustrative results are not external interoperability proof.
- Compiler usefulness must be measured against equivalent manual work rather than assumed.
- Agreement between models must be compared with and without ADUC to support a causal value claim.

## Full-Core version 0.1 scoreboard

| Deliverable | Status |
|---|---|
| Core specification | Working draft created |
| Complete epistemic lifecycle | Defined and reference-tested |
| Adoption and value-validation plan | Defined; benchmarks not yet run |
| Source-description binding model | Next action |
| Official full-Core JSON Schema | Not implemented |
| Ten valid full-Core examples | 1 informative example created |
| Ten invalid full-Core examples | Not implemented |
| CLI validator | Partial: semantic-mapping profile and lifecycle reference evaluator |
| JSON/CSV compiler | Not implemented |
| Inference calibration | Protocol and report not implemented |
| Manual vs assisted benchmark | Not implemented |
| Minimal review interface | Not implemented |
| Review-tax report | Not implemented |
| Core vocabulary | Partial: semantic-mapping JSON-LD context only |
| Two-source comparison | Partial: semantic targets; units/time/identity absent |
| Two-model demonstration | Harness exists; external proof and baseline comparison absent |
| Conformance suite | Partial implementation |
| MCP adapter | Deferred until Core stability |
| Try in 5 minutes | English website guide created for current tools |

## Not yet validated

- source-description and immutable source-binding profile;
- normative cardinalities and rules for all ten Core blocks;
- unit identifier and conversion strategy;
- temporal semantics and alignment;
- entity identity and equivalence;
- complete policy profile;
- full-Core JSON Schema;
- migration tooling from the mapping-profile document to the full Core envelope;
- JSON and CSV compiler;
- inference evidence protocol and calibrated benchmark set;
- manual mapping versus `infer + review` performance;
- review interface and review-tax outcome;
- with-ADUC versus without-ADUC model performance;
- qualifying external runs from two independent AI consumers;
- public HTTPS namespace and final project name;
- optional MCP adapter;
- commercial adoption model.

## Active blockers

- the source-description and source-binding ADR is not accepted;
- full-Core schema boundaries and schema family do not exist;
- the first complete example is informative rather than schema-validatable;
- unit, time, and identity comparison cannot be demonstrated from the current semantic-only profile;
- no qualifying external model runs have been committed;
- no manual-versus-assisted or with-versus-without-ADUC benchmark has been run;
- the public name remains provisional.

## Next gate

Define how ADUC references or embeds Croissant, JSON Schema, OpenAPI, DCAT, and versioned custom source descriptions; bind contracts to exact source versions; and resolve local JSON and CSV references deterministically without duplicating established structural standards.

The adoption and value-validation plan applies later, but reliable benchmarking is impossible until source and evidence binding are deterministic.

## Rule

This file reports evidence, not optimism. Do not mark an item complete without a linked artifact or passing check.