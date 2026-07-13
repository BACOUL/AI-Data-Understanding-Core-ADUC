# Project Status

- Project: AI Data Understanding Core — working name
- Current phase: Phase 0 — Full-Core definition and public foundation
- Current release: unreleased
- Target release: `0.1.0-alpha.0`
- Overall status: eight foundational Core decisions are specified and reference-tested; policy and permitted-use conditions are the final domain profile required before the normative Core object model and schema family can be frozen

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

The candidate envelope contains:

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

`spec/ADUC_CORE_SPEC_0_1.md` remains the full-Core working draft.

## Completed foundation

- governance, contribution rules, ADR method, roadmap, execution ledger, and CI;
- prior-art matrix and official full-Core program;
- first informative ten-block example;
- English website with GitHub Pages and Vercel deployment;
- semantic-mapping profile, validator, comparator, JSON-LD/RDF tooling, and provider-neutral multi-model harness;
- adoption and value-validation gates;
- ADR-0005 epistemic lifecycle;
- ADR-0006 source description and immutable binding;
- ADR-0007 units and deterministic conversion;
- ADR-0008 temporal semantics and timezone alignment;
- ADR-0009 entity identity and safe equivalence;
- ADR-0010 provenance and transformation lineage;
- ADR-0011 uncertainty and DQV-compatible data quality;
- ADR-0012 general relation semantics.

## Accepted Core profile evidence

| Profile | Evidence |
|---|---|
| Epistemic lifecycle | 9 valid, 8 invalid, deterministic evaluator |
| Source binding | 3 valid, 10 invalid, 7 tests |
| Units | 5 valid, 15 invalid, 9 tests |
| Time | 9 valid, 15 invalid, 7 tests |
| Identity | 9 valid, 17 invalid, 9 tests |
| Provenance | 7 valid, 20 invalid, 8 tests |
| Uncertainty and quality | 14 valid, 24 invalid, 10 tests |
| General relations | 13 valid, 20 invalid, 10 tests |

## General relation decision

ADR-0012 and `spec/RELATION_PROFILE_0_1.md` establish that:

- vocabulary definitions, relation assertions, and consumer inferences are separate;
- predicates use absolute IRIs from authoritative vocabularies;
- endpoints are bound and typed;
- direction, inverse, symmetry, and transitivity are never guessed;
- `skos:closeMatch` is not equality;
- `owl:sameAs` requires a qualifying identity-profile decision;
- `skos:broader` closure yields `skos:broaderTransitive`;
- absence means unknown rather than false;
- negative claims require explicit assertions;
- correlation, dependency, or temporal order do not prove causation;
- contested, deprecated, out-of-scope, contradictory, or cyclic relations block automatic use;
- qualifying assertions export deterministically to JSON-LD/RDF.

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
| Core working draft | Created |
| Epistemic lifecycle | Complete |
| Source binding | Complete |
| Units and conversions | Complete |
| Temporal semantics | Complete |
| Entity identity | Complete |
| Provenance and lineage | Complete |
| Uncertainty and quality | Complete |
| General relations | Complete |
| Policy and permitted use | Next action |
| Normative Core object model | Not implemented |
| Official full-Core JSON Schema | Not implemented |
| Ten valid complete examples | Not implemented |
| Ten invalid complete examples | Not implemented |
| Unified Core validator/comparator | Not implemented |
| JSON/CSV compiler | Not implemented |
| Review interface | Not implemented |
| Value benchmark | Not run |
| External multi-model proof | Not established |

## Active blockers

- ADR-0013 policy and permitted-use conditions does not exist;
- normative Core envelope and modular boundaries are not frozen;
- the complete example is not schema-validatable;
- current reference tools are separate rather than unified;
- no qualifying value benchmark or external multi-model runs exist;
- the public name remains provisional.

## Next gate

Define the policy and permitted-use profile, including permissions, prohibitions, duties, parties, purposes, temporal and territorial scope, evidence, provenance, disclosure, conflicts, lifecycle, deterministic consumer outcomes, and the boundary between machine evaluation and human legal interpretation.

## Rule

This file reports evidence, not optimism. Do not mark an item complete without a linked artifact and passing checks.
