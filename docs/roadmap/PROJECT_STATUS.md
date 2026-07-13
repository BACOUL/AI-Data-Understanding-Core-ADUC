# Project Status

- Project: AI Data Understanding Core (working name)
- Current phase: Phase 0 — Full-Core definition and public foundation
- Current release: unreleased
- Target release: `0.1.0-alpha.0`
- Overall status: mission, architecture, epistemic lifecycle, adoption gates, source binding, units, and temporal semantics are defined; entity identity is next and the official full-Core schema is not yet implemented

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
- ADR-0008 temporal semantics, timezone evidence, and deterministic alignment profile and evaluator;
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
- absolute temperatures and temperature differences are distinct;
- conversion data are pinned and exact decimal/rational arithmetic is used;
- rounding, uncertainty, source binding, and provenance are preserved;
- contextual conversions remain blocked without their required context.

Reference evidence:

- five valid conversion cases;
- fifteen invalid counterexamples;
- nine unit tests;
- deterministic results including `89 °C = 192.2 °F` and `1.5 m³/s = 1500.0 L/s`.

## Accepted temporal model

ADR-0008 separates:

```text
fixed instant
local civil date-time
date
time-of-day
exact elapsed duration
calendar-relative period
interval
temporal role
precision
uncertainty
timezone evidence
```

Key rules:

- RFC 3339 represents fixed instants with explicit offsets;
- RFC 9557 may attach named-zone evidence to fixed timestamps;
- IANA timezone identifiers and a pinned timezone-database release resolve local civil times;
- a numeric offset does not replace named timezone rules;
- observation, event, publication, processing, validity, sampling, and aggregation are separate roles;
- locale-dependent strings require an explicit format and locale;
- ambiguous and nonexistent civil times block automatic use;
- interval boundaries are explicit;
- uncertainty overlap does not prove exact simultaneity;
- exact durations and calendar periods are not interchangeable.

Reference evidence:

- nine valid temporal cases;
- fifteen invalid counterexamples;
- seven temporal tests;
- `13/07/2026 14:00` in `Europe/Paris` resolves to `2026-07-13T12:00:00Z`;
- the Paris overlap on `2026-10-25T02:30:00` requires an explicit occurrence;
- `2026-03-29T02:30:00` is rejected as nonexistent;
- `PT15M` resolves to 900 exact seconds while `P1M` remains contextual.

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
| Temporal semantics | Defined and reference-tested |
| Entity identity | Next action |
| Official full-Core JSON Schema | Not implemented |
| Ten valid full-Core examples | 1 informative complete example; profile-specific fixtures exist |
| Ten invalid full-Core examples | Not implemented |
| CLI validator | Partial reference tools exist |
| JSON/CSV compiler | Not implemented |
| Review interface | Not implemented |
| Core vocabulary | Partial |
| Two-source comparison | Semantic, unit, and temporal reference behavior exist; identity absent |
| Two-model demonstration | Harness exists; external proof and baseline comparison absent |
| MCP adapter | Deferred until Core stability |
| Try in 5 minutes | English guide exists for current tools |

## Not yet validated

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

- ADR-0009 entity identity is not accepted;
- full-Core schema boundaries do not exist;
- the complete example is not yet schema-validatable;
- end-to-end comparison still lacks entity identity behavior;
- no qualifying external model runs or value benchmarks exist;
- the public name remains provisional.

## Next gate

Define entity identity and equivalence, including identifier namespaces, issuers, validity, aliases, possible matches, authoritative equivalence, conflicts, recycled identifiers, privacy-sensitive identifiers, and deterministic merge-blocking rules.

Every identity assertion must remain bound to exact source and temporal evidence through ADR-0006 and ADR-0008.

## Rule

This file reports evidence, not optimism. Do not mark an item complete without a linked artifact or passing check.
