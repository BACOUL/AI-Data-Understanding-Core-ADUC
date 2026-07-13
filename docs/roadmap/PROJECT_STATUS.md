# Project Status

- Project: AI Data Understanding Core (working name)
- Current phase: Phase 0 — Full-Core definition and public foundation
- Current release: unreleased
- Target release: `0.1.0-alpha.0`
- Overall status: mission, architecture, epistemic lifecycle, adoption gates, source binding, units, temporal semantics, and entity identity are defined; provenance is the next Core decision and the official full-Core schema is not yet implemented

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
- ADR-0008 temporal semantics and timezone-alignment profile and evaluator;
- ADR-0009 entity identity and safe-equivalence profile and evaluator;
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

ADUC separates resource content, structural description, and local field reference.

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
- UCUM codes remain compact aliases where available;
- local codes and symbols do not act as global identifiers;
- matching dimensions are necessary but not sufficient;
- absolute temperatures and temperature differences are distinct;
- v0.1 supports exact identity, multiplicative, and affine conversion;
- conversion evidence is pinned and uncertainty is preserved.

Reference evidence:

- five valid conversion cases;
- fifteen invalid counterexamples;
- nine unit tests;
- deterministic results including `89 °C = 192.2 °F`.

## Accepted temporal model

Key rules:

- RFC 3339 represents fixed instants with explicit offsets;
- RFC 9557 may attach named-zone evidence;
- IANA timezone identifiers and a pinned timezone-database release resolve local civil times;
- a numeric offset does not replace named timezone rules;
- temporal roles remain separate;
- locale-dependent strings require explicit format and locale;
- ambiguous and nonexistent civil times block automatic use;
- interval boundaries and uncertainty are explicit;
- exact durations and calendar periods are not interchangeable.

Reference evidence:

- nine valid temporal cases;
- fifteen invalid counterexamples;
- seven temporal tests;
- `13/07/2026 14:00` in `Europe/Paris` resolves to `2026-07-13T12:00:00Z`;
- ambiguous and nonexistent Paris civil times are detected.

## Accepted identity model

ADR-0009 separates:

```text
entity
identifier
human label
identity relation assertion
consumer merge decision
```

Key rules:

- local identity requires scheme, namespace, issuer, canonical value, and applicable time;
- local, global, pseudonymous, and linkage-token identifiers remain distinct;
- labels and matching observations do not prove identity;
- `possibleMatch` produces `candidateOnly`;
- `sameEntity` requires verified or canonical authority;
- confidence remains separate from authority;
- recycled identifiers require non-overlapping validity;
- contradictory, contested, expired, reassigned, type-incompatible, or privacy-incompatible identity blocks merge;
- `owl:sameAs` is available only after `mergeAllowed`.

Reference evidence:

- nine valid identity cases;
- seventeen invalid counterexamples;
- nine identity tests;
- canonical `M42` / `MAIN-B` crosswalk produces `mergeAllowed`;
- inferred similarity remains `candidateOnly`;
- identical lexical values in different namespaces remain unresolved;
- purpose-limited pseudonymous linkage is enforced.

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
| Entity identity | Defined and reference-tested |
| Provenance and transformation lineage | Next action |
| Uncertainty, relation, and policy profiles | Not implemented |
| Official full-Core JSON Schema | Not implemented |
| Ten valid full-Core examples | 1 informative complete example; profile-specific fixtures exist |
| Ten invalid full-Core examples | Not implemented |
| CLI validator | Partial reference tools exist |
| JSON/CSV compiler | Not implemented |
| Review interface | Not implemented |
| Core vocabulary | Partial |
| Two-source comparison | Semantic, unit, time, and identity reference behavior exist separately; unified comparison absent |
| Two-model demonstration | Harness exists; external proof and baseline comparison absent |
| MCP adapter | Deferred until Core stability |
| Try in 5 minutes | English guide exists for current tools |

## Not yet validated

- provenance and transformation lineage;
- complete uncertainty, relation, and policy rules;
- normative full-Core object model and JSON Schema family;
- migration tooling into the complete Core envelope;
- JSON/CSV compiler and review interface;
- inference calibration and manual-versus-assisted performance;
- with/without-ADUC external model performance;
- two qualifying independent AI runs;
- final HTTPS namespace and project name;
- optional MCP adapter and commercial adoption model.

## Active blockers

- ADR-0010 provenance and transformation lineage does not exist;
- uncertainty and policy boundaries remain undefined;
- full-Core schema boundaries do not exist;
- the complete example is not yet schema-validatable;
- end-to-end comparison has not unified all profile dimensions;
- no qualifying external model runs or value benchmarks exist;
- the public name remains provisional.

## Next gate

Define provenance and transformation lineage, including agents, activities, generation, use, derivation, software/model versions, parameters, hashes, completeness, redaction, and reproducibility.

Every provenance record must reuse ADR-0005, ADR-0006, ADR-0008, and the accepted domain profiles rather than duplicating them.

## Rule

This file reports evidence, not optimism. Do not mark an item complete without a linked artifact or passing check.
