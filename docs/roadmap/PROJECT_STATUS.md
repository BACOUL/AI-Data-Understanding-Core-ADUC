# Project Status

- Project: AI Data Understanding Core (working name)
- Current phase: Phase 0 — Full-Core definition and public foundation
- Current release: unreleased
- Target release: `0.1.0-alpha.0`
- Overall status: mission, architecture, epistemic lifecycle, adoption gates, source binding, and units are defined; temporal semantics are next and the official full-Core schema is not yet implemented

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

## Completed foundation

- repository governance, contribution rules, ADR method, roadmap, execution ledger, and CI;
- prior-art matrix and official full-Core program;
- first informative ten-block example;
- English public website and GitHub Pages workflow;
- ADR-0005 complete epistemic lifecycle and reference evaluator;
- ADR-0006 source-description and immutable source-binding profile and evaluator;
- ADR-0007 unit identifiers, dimensional compatibility, and conversion profile and evaluator;
- official adoption and value-validation gates;
- existing semantic-mapping profile, validator, comparator, JSON-LD/RDF tooling, and multi-model harness.

## Accepted epistemic model

| Concern | Representation |
|---|---|
| unresolved field | coverage record with `resolutionStatus: unknown` |
| assertion authority | `inferred`, `reviewed`, `verified`, or `canonical` |
| unresolved dispute | immutable challenge producing `contested` |
| retired assertion | immutable deprecation producing `deprecated` |

Authority, confidence, conflict, and lifecycle remain separate claims.

## Accepted source-binding model

ADUC separates:

```text
resource content
structural description
local field reference
```

The accepted binding modes are `content`, `description`, and `content-and-description`.

Key rules:

- v0.1 reference bindings use SHA-256;
- mutable URLs and version labels are not sufficient integrity evidence;
- linked descriptions bind raw bytes;
- embedded JSON descriptions use an RFC 8785 canonicalization scope;
- Croissant, JSON Schema, OpenAPI, and DCAT remain authoritative for their structures;
- local-reference schemes and bases are explicit;
- stale, unavailable, ambiguous, or conflicting descriptions block automatic use.

## Accepted unit and conversion model

ADR-0007 separates:

```text
source-bound field
quantity kind
dimension vector
quantity role
unit state
global unit identifier
local code or display symbol
epistemic authority
```

Key rules:

- QUDT IRIs are preferred semantic identifiers;
- UCUM codes are retained as compact aliases where available;
- local codes and symbols do not act as global identifiers;
- `known`, `unitless`, `unknown`, `arbitrary`, and `contextual` remain distinct;
- matching dimensions are necessary but not sufficient;
- quantity kind and quantity role must also match;
- absolute temperatures and temperature differences are distinct;
- v0.1 supports exact identity, multiplicative, and affine conversion;
- conversion data are pinned by registry identifier, version, and SHA-256;
- decimal/rational arithmetic, rounding, uncertainty, source binding, and provenance are preserved;
- contextual conversions remain blocked without their required context.

Reference evidence:

- five valid conversion cases;
- fifteen invalid counterexamples;
- nine unit tests;
- deterministic results including `89 °C = 192.2 °F`, `10 °C difference = 18.0 °F difference`, `1.5 m³/s = 1500.0 L/s`, and `50 % = 0.500` unitless ratio.

## Adoption and value-validation constraints

Before compiler or interoperability success claims, the project must provide:

- declared inference modes and exact evidence;
- method/version-bound confidence;
- manual mapping versus `infer + review` benchmark;
- review-tax report;
- controlled with-ADUC versus without-ADUC evaluation;
- at least 30% lower median assisted human time in the initial alpha target without lower final correctness;
- no silently accepted critical false mapping;
- MCP only as an optional future adapter.

## Full-Core version 0.1 scoreboard

| Deliverable | Status |
|---|---|
| Core specification | Working draft created |
| Epistemic lifecycle | Defined and reference-tested |
| Adoption/value plan | Defined; benchmarks not yet run |
| Source binding | Defined and reference-tested |
| Units and conversions | Defined and reference-tested |
| Temporal semantics | Next action |
| Entity identity | Not implemented |
| Official full-Core JSON Schema | Not implemented |
| Ten valid full-Core examples | 1 informative complete example; profile-specific fixtures exist |
| Ten invalid full-Core examples | Not implemented |
| CLI validator | Partial reference tools exist |
| JSON/CSV compiler | Not implemented |
| Review interface | Not implemented |
| Core vocabulary | Partial |
| Two-source comparison | Semantic and unit reference behavior exist; time and identity absent |
| Two-model demonstration | Harness exists; external proof and baseline comparison absent |
| MCP adapter | Deferred until Core stability |
| Try in 5 minutes | English guide exists for current tools |

## Not yet validated

- temporal semantics, timezone evidence, intervals, and alignment;
- entity identity and equivalence;
- remaining provenance, uncertainty, relation, and policy rules;
- full-Core schema boundaries and JSON Schema family;
- migration tooling into the complete Core envelope;
- JSON/CSV compiler and review interface;
- inference calibration and manual-versus-assisted performance;
- with/without-ADUC external model performance;
- two qualifying independent AI runs;
- final HTTPS namespace and project name;
- optional MCP adapter and commercial adoption model.

## Active blockers

- ADR-0008 temporal semantics is not accepted;
- entity identity remains undefined;
- full-Core schema boundaries do not exist;
- the complete example is not yet schema-validatable;
- end-to-end comparison still lacks temporal and identity behavior;
- no qualifying external model runs or value benchmarks exist;
- the public name remains provisional.

## Next gate

Define temporal semantics and timezone alignment, including instants, local civil time, intervals, precision, resolution, ambiguity, timezone-database provenance, and deterministic alignment.

Every temporal assertion must remain bound to the exact source and local field through ADR-0006.

## Rule

This file reports evidence, not optimism. Do not mark an item complete without a linked artifact or passing check.
