# Project Status

- Project: AI Data Understanding Core — working name
- Current phase: Phase 2 - Reference implementation
- Current release: unreleased
- Target release: `0.1.0-alpha.0`
- Overall status: nine domain profiles, the normative Core object model, the official modular Draft 2020-12 schema family, the unified full-Core validator/comparator, deterministic semantic-profile migration and deterministic complete-contract formatter are implemented and reference-tested; the provider-neutral full-Core conformance runner is the single next engine task

## Official direction

ADUC is an open, model-independent contract intended to let data describe structure, semantics, identity, context, provenance, uncertainty, relations and policy to AI systems, agents and applications.

The normative envelope is frozen as:

```text
aduc        required object
resource    required object
structure   required object
semantics   optional object
identity    optional object
context     optional object
provenance  optional object
uncertainty optional object
relations   optional array
policy      optional object
```

The minimum interoperable envelope is `aduc + resource + structure`.

## Completed foundation

- governance, contribution rules, ADR method, roadmap, execution ledger and CI;
- prior-art matrix and official full-Core program;
- English website with GitHub Pages and Vercel deployment;
- standalone semantic-mapping schema, validator, comparator and JSON-LD/RDF tooling;
- provider-neutral multi-model harness foundation;
- adoption and value-validation gates;
- ADR-0005 through ADR-0013 domain profiles;
- ADR-0014 normative Core object model and modular boundaries;
- ADR-0015 official modular Core JSON Schema family and local reference validator;
- ADR-0016 unified Core validator and deterministic comparator;
- ADR-0017 deterministic semantic-profile migration into complete Core contracts;
- ADR-0018 deterministic complete-contract formatting with exact-decimal and array-order preservation.

## Accepted evidence

| Profile or model | Evidence |
|---|---|
| Epistemic lifecycle | 9 valid, 8 invalid, deterministic evaluator |
| Source binding | 3 valid, 10 invalid, 7 tests |
| Units | 5 valid, 15 invalid, 9 tests |
| Time | 9 valid, 15 invalid, 7 tests |
| Identity | 9 valid, 17 invalid, 9 tests |
| Provenance | 7 valid, 20 invalid, 8 tests |
| Uncertainty and quality | 14 valid, 24 invalid, 10 tests |
| General relations | 13 valid, 20 invalid, 10 tests |
| Policy and permitted use | 20 valid, 32 invalid, 13 tests |
| Normative Core object model | complete ten-block example, 25 invalid architecture mutations, 11 tests, module manifest |
| Modular Core schema family | 14 Draft 2020-12 schemas, 11 valid contracts, 15 invalid contracts, 13 schema tests, local validator |
| Unified Core validation and comparison | `tools/aduc_core.py`, 24 comparison scenarios, 15 validator tests, 13 comparator tests, evaluator-adapter orchestration, separated change type and semantic assessments, stable report specs |
| Deterministic semantic-profile migration | explicit migration manifest, conservative status mapping, complete Core revalidation, three frozen end-to-end scenarios and 19 focused tests |
| Deterministic complete-contract formatter | strict UTF-8 JSON parser, duplicate-key rejection, exact-decimal preservation, frozen Core ordering, unchanged arrays, atomic writes, stable reports, frozen fixtures and 13 focused tests |
| Public website alignment | canonical GitHub Pages URL, dedicated Core/Validate/Compare/Trust/Evidence pages, site-data metrics, sitemap/canonical checks and obsolete-claim regression tests |

## Schema-family decision

ADR-0015 establishes that:

- `schema/aduc-core.schema.json` is the full-Core validation entry point;
- all operational `$ref` values resolve locally without remote retrieval;
- the ten reserved top-level blocks and minimum envelope are enforced;
- Core objects are closed and extensions use declared external namespaces;
- identifiers, timestamps, digests, controlled enums and assertion qualification are structurally checked;
- `structure.records` is mandatory according to ADR-0014;
- relations use exactly one object endpoint form;
- descriptive policy rules cannot be made machine executable;
- policy requires provenance;
- JSON Schema remains structural and does not claim factual, legal or operational validity;
- `tools/aduc_core_validate.py` combines schema validation with the ADR-0014 architecture checker.

## Adoption and value constraints

Before compiler or interoperability success claims, the project must demonstrate:

- declared inference modes and evidence;
- method-bound calibrated confidence;
- manual mapping versus `infer + review` timing;
- review-tax measurement;
- controlled evaluation with and without ADUC;
- at least 30% lower median assisted human time in the provisional alpha target;
- no lower final correctness and no silently accepted critical false mapping;
- MCP only as an optional future adapter.

## Full-Core v0.1 scoreboard

| Deliverable | Status |
|---|---|
| Core working draft | Updated |
| Nine domain profiles | Complete |
| Normative Core object model | Complete |
| Core module manifest | Complete |
| Complete ten-block model example | Schema- and architecture-valid |
| Architectural counterexamples | 25 implemented |
| Official modular JSON Schema family | Complete |
| Complete valid schema fixtures | 11 implemented |
| Complete invalid schema fixtures | 15 implemented |
| Local Core schema validator | Complete |
| Unified Core validator/comparator | Complete |
| Semantic-profile migration tool | Complete |
| Deterministic complete-contract formatter | Complete |
| Provider-neutral full-Core conformance runner | Next action |
| JSON/CSV compiler | Not implemented |
| Review interface | Not implemented |
| Value benchmark | Not run |
| External multi-model proof | Not established |

## Active blockers

- a provider-neutral full-Core conformance runner is not yet implemented;
- public TypeScript/Python SDKs and package-release controls are not yet implemented;
- no qualifying value benchmark or external multi-model runs exist;
- the public name remains provisional.

## Next gate

Define and implement the provider-neutral full-Core conformance runner for validator, comparator and formatter implementations. The runner must produce reproducible implementation reports without treating the reference engine as the specification. The JSON/CSV compiler remains blocked until the adoption and review-tax gates are ready to run.

## Rule

This file reports evidence, not optimism. Do not mark an item complete without a linked artifact and passing checks.
