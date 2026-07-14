# Project Status

- Project: AI Data Understanding Core — working name
- Current phase: Phase 0 — Full-Core definition and public foundation
- Current release: unreleased
- Target release: `0.1.0-alpha.0`
- Overall status: nine domain profiles and the normative Core object model are specified and reference-tested; the official modular JSON Schema family is the single next implementation task

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

to AI systems, agents and applications.

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
- semantic-mapping profile, validator, comparator, JSON-LD/RDF tooling and provider-neutral multi-model harness;
- adoption and value-validation gates;
- ADR-0005 epistemic lifecycle;
- ADR-0006 source description and immutable binding;
- ADR-0007 units and deterministic conversion;
- ADR-0008 temporal semantics and timezone alignment;
- ADR-0009 entity identity and safe equivalence;
- ADR-0010 provenance and transformation lineage;
- ADR-0011 uncertainty and DQV-compatible data quality;
- ADR-0012 general relation semantics;
- ADR-0013 policy and permitted-use conditions;
- ADR-0014 normative Core object model and modular boundaries.

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
| Normative Core object model | complete ten-block example, 25 invalid architecture mutations, 11 tests, machine-readable module manifest |

## Normative Core model decision

ADR-0014, `spec/ADUC_CORE_MODEL_0_1.md` and `spec/core-module-manifest.json` establish that:

- the ten top-level block names and cardinalities are frozen;
- `aduc`, `resource` and `structure` are mandatory;
- `relations` is the only repeated top-level module;
- every addressable object uses an absolute-IRI identifier;
- `Ref` and `Refs` identify deterministic internal references;
- every normative fact has one owning module;
- semantic assertions require prior exact resource and structural binding;
- shared qualification preserves status, authority, evidence, provenance, confidence, uncertainty, conflict and lifecycle without conflation;
- external standards remain external and are referenced rather than copied;
- JSON is the canonical authoring representation and JSON-LD is a deterministic projection;
- extensions are declared, namespaced, collision-safe and never silently understood;
- hard module dependencies are acyclic;
- published history is immutable and replacement creates new identifiers;
- migration from the current semantic-mapping profile preserves authority, evidence, confidence and lifecycle;
- absent optional information is `notDescribed`, not false, exact, permitted or trusted.

The architecture checker validates these invariants but is not the future full-Core schema validator.

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
| Complete ten-block model example | Created; not yet schema-validated |
| Architectural counterexamples | 25 implemented |
| Official modular JSON Schema family | Next action |
| Ten complete valid schema fixtures | Not implemented |
| Ten complete invalid schema fixtures | Not implemented |
| Unified Core validator/comparator | Not implemented |
| JSON/CSV compiler | Not implemented |
| Review interface | Not implemented |
| Value benchmark | Not run |
| External multi-model proof | Not established |

## Active blockers

- the official modular full-Core JSON Schema family does not exist;
- the complete example is not yet schema-validatable;
- current reference tools are separate rather than unified;
- no qualifying value benchmark or external multi-model runs exist;
- the public name remains provisional.

## Next gate

Implement the Draft 2020-12 modular JSON Schema family from the frozen model, create complete valid and invalid fixtures, and document the graph-level checks that require the complementary reference validator.

## Rule

This file reports evidence, not optimism. Do not mark an item complete without a linked artifact and passing checks.