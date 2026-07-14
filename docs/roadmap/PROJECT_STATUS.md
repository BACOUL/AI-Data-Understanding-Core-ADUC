# Project Status

- Project: AI Data Understanding Core — working name
- Current phase: Phase 1 — Standard v0.1 implementation
- Current release: unreleased
- Target release: `0.1.0-alpha.0`
- Overall status: nine domain profiles, the normative Core object model and the official modular Draft 2020-12 schema family are implemented and reference-tested; unified full-Core validation and comparison are the single next task

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
- ADR-0015 official modular Core JSON Schema family and local reference validator.

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
| Modular Core schema family | 14 Draft 2020-12 schemas, 11 valid contracts, 15 invalid contracts, 10 schema tests, local validator |

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
| Unified Core validator/comparator | Next action |
| Semantic-profile migration tool | Not implemented |
| JSON/CSV compiler | Not implemented |
| Review interface | Not implemented |
| Value benchmark | Not run |
| External multi-model proof | Not established |

## Active blockers

- current domain evaluators are separate rather than orchestrated by one Core validator;
- complete deterministic cross-contract comparison does not yet exist;
- migration from the standalone semantic-mapping profile is not automated;
- no qualifying value benchmark or external multi-model runs exist;
- the public name remains provisional.

## Next gate

Build the unified full-Core validator and comparator, preserving every schema, architectural, epistemic and domain-specific diagnostic without weakening accepted safeguards.

## Rule

This file reports evidence, not optimism. Do not mark an item complete without a linked artifact and passing checks.
