# Project Status

- Project: AI Data Understanding Core — working name
- Current phase: Phase 0 — Full-Core definition and public foundation
- Current release: unreleased
- Target release: `0.1.0-alpha.0`
- Overall status: nine foundational Core decisions are specified and reference-tested; the normative Core object model and modular boundaries are the final definition task before the official schema family

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

`spec/ADUC_CORE_SPEC_0_1.md` remains the full-Core working draft. Its object ownership and modular boundaries are not yet frozen.

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
- ADR-0012 general relation semantics;
- ADR-0013 policy and permitted-use conditions.

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
| Policy and permitted use | 20 valid, 32 invalid, 13 tests |

## Policy and permitted-use decision

ADR-0013 and `spec/POLICY_PROFILE_0_1.md` establish that:

- ADUC reuses ODRL rather than creating a competing rights language;
- exact target identity and SHA-256 version binding are mandatory;
- executable permissions, prohibitions, and duties remain distinct from classifications, recommendations, and legal notices;
- actions, purposes, parties, recipients, places, and environments use absolute controlled identifiers;
- a descriptive `public` classification is not universal permission;
- free-text purpose matching is blocked;
- a matching prohibition overrides a matching permission in the deterministic offline subset;
- pre-use duties require bound satisfaction evidence;
- post-use duties remain visible as outstanding obligations;
- open mode yields `indeterminate` when no rule applies, while closed mode denies by default;
- supported outcomes are `permit`, `deny`, `notApplicable`, `indeterminate`, and `requiresHumanReview`;
- inferred, partial, redacted, externally governed, contested, or deprecated policies block automatic reliance;
- consent, ownership, and legal-compliance claims require typed evidence and provenance;
- ADUC does not grant legal permission, replace legal interpretation, or enforce access control;
- qualifying policy records export deterministically to JSON-LD/RDF.

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
| Policy and permitted use | Complete |
| Normative Core object model | Next action |
| Official full-Core JSON Schema | Not implemented |
| Ten valid complete examples | Not implemented |
| Ten invalid complete examples | Not implemented |
| Unified Core validator/comparator | Not implemented |
| JSON/CSV compiler | Not implemented |
| Review interface | Not implemented |
| Value benchmark | Not run |
| External multi-model proof | Not established |

## Active blockers

- the normative Core envelope, object ownership, cardinalities, and modular boundaries are not frozen;
- the complete example is not schema-validatable;
- the official full-Core JSON Schema family does not exist;
- current reference tools are separate rather than unified;
- no qualifying value benchmark or external multi-model runs exist;
- the public name remains provisional.

## Next gate

Freeze the normative Core object model and modular boundaries, including top-level cardinality, object ownership, deterministic references, qualification patterns, external-standard boundaries, JSON/JSON-LD representation, extension behavior, versioning, migration from the current mapping profile, and deterministic behavior for absent, unsafe, prohibited, contested, deprecated, or unsupported information.

## Rule

This file reports evidence, not optimism. Do not mark an item complete without a linked artifact and passing checks.
