# Project Status

- Project: AI Data Understanding Core (working name)
- Current phase: Phase 0 — Full-Core definition and public foundation
- Current release: unreleased
- Target release: `0.1.0-alpha.0`
- Overall status: mission, architecture, epistemic lifecycle, adoption gates, source binding, units, temporal semantics, entity identity, and provenance are defined and reference-tested; uncertainty and data quality are the next Core decision, and the official full-Core schema is not yet implemented

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
- English public website with GitHub Pages and Vercel deployment;
- ADR-0005 epistemic lifecycle and evaluator;
- ADR-0006 immutable source-binding profile and evaluator;
- ADR-0007 unit and conversion profile and evaluator;
- ADR-0008 temporal profile and evaluator;
- ADR-0009 identity and safe-equivalence profile and evaluator;
- ADR-0010 provenance and transformation-lineage profile and evaluator;
- official adoption and value-validation gates;
- semantic-mapping profile, validator, comparator, JSON-LD/RDF tooling, and multi-model harness.

## Accepted Core decisions

### Epistemic lifecycle

| Concern | Representation |
|---|---|
| unresolved field | coverage record with `resolutionStatus: unknown` |
| assertion authority | `inferred`, `reviewed`, `verified`, or `canonical` |
| unresolved dispute | immutable challenge producing `contested` |
| retired assertion | immutable deprecation producing `deprecated` |

Authority, confidence, conflict, and lifecycle remain separate claims.

### Source binding

ADUC separates resource content, structural description, and local field reference.

Key rules:

- v0.1 uses SHA-256 for reference bindings;
- mutable URLs and version labels are insufficient integrity evidence;
- Croissant, JSON Schema, OpenAPI, and DCAT remain authoritative for their structural models;
- stale, unavailable, ambiguous, or conflicting descriptions block automatic use.

### Units and conversions

ADUC separates quantity kind, dimension, quantity role, global unit identifier, local code, authority, and conversion evidence.

Reference evidence:

- five valid conversion cases;
- fifteen invalid counterexamples;
- nine unit tests;
- deterministic results including `89 °C = 192.2 °F`.

### Temporal semantics

Key rules:

- fixed instants use explicit offsets;
- named zones use pinned IANA timezone evidence;
- ambiguous and nonexistent civil times block automatic use;
- temporal roles, precision, uncertainty, interval boundaries, exact durations, and calendar periods remain distinct.

Reference evidence:

- nine valid temporal cases;
- fifteen invalid counterexamples;
- seven temporal tests;
- `13/07/2026 14:00` in `Europe/Paris` resolves to `2026-07-13T12:00:00Z`.

### Entity identity

ADR-0009 separates:

```text
entity
identifier
human label
identity relation assertion
consumer merge decision
```

Reference evidence:

- nine valid identity cases;
- seventeen invalid counterexamples;
- nine identity tests;
- canonical `M42` / `MAIN-B` crosswalk produces `mergeAllowed`;
- inferred similarity remains `candidateOnly`.

### Provenance and transformation lineage

ADR-0010 reuses W3C PROV-O and separates:

```text
entity or artifact
activity or transformation
responsible agent
software/model execution evidence
derivation
invalidation
disclosure state
reproducibility claim
```

Key rules:

- material inputs and outputs require exact source bindings and SHA-256 hashes;
- observed, attested, inferred, partial, and redacted lineage remain distinct;
- deterministic, nondeterministic, manual, external-attestation, and reconstructed execution remain distinct;
- deterministic claims require pinned software, build, environment, parameters, inputs, outputs, and complete disclosure;
- replayable AI execution requires pinned model, prompt, parameters, environment, tools, and seed where applicable;
- manual intervention cannot be hidden;
- cycles, impossible ordering, duplicate generation, broken derivations, invalidation errors, and unsupported reproduction claims block conformance.

Reference evidence:

- seven valid provenance cases;
- twenty invalid mutation fixtures;
- eight provenance evaluator and CLI tests;
- one end-to-end chain from raw source bytes through parsing, conversion, temporal resolution, identity linking, and comparison.

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
| Provenance and transformation lineage | Defined and reference-tested |
| Uncertainty and data quality | Next action |
| General relations and policy | Not implemented |
| Official full-Core JSON Schema | Not implemented |
| Ten valid full-Core examples | One informative complete example; profile-specific fixtures exist |
| Ten invalid full-Core examples | Not implemented |
| CLI validator | Partial reference tools exist |
| JSON/CSV compiler | Not implemented |
| Review interface | Not implemented |
| Core vocabulary | Partial |
| Unified two-source comparison | Separate profile behavior exists; unified comparison absent |
| Two-model demonstration | Harness exists; external proof and baseline comparison absent |
| MCP adapter | Deferred until Core stability |
| Try in 5 minutes | English guide exists for current tools |

## Not yet validated

- complete uncertainty and quality rules;
- general relation and policy rules;
- normative full-Core object model and JSON Schema family;
- migration tooling into the complete Core envelope;
- JSON/CSV compiler and review interface;
- inference calibration and manual-versus-assisted performance;
- with/without-ADUC external model performance;
- two qualifying independent AI runs;
- final HTTPS namespace and project name;
- optional MCP adapter and commercial adoption model.

## Active blockers

- ADR-0011 uncertainty and data quality does not exist;
- general relation and policy boundaries remain undefined;
- full-Core schema boundaries do not exist;
- the complete example is not yet schema-validatable;
- end-to-end comparison has not unified all profile dimensions;
- no qualifying external model runs or value benchmarks exist;
- the public name remains provisional.

## Next gate

Define uncertainty and data quality, including measurement error, statistical intervals, distributions, propagation, correlation assumptions, resolution, censoring, missingness, qualitative quality, and separation from epistemic authority.

Every uncertainty record must reuse the accepted source, unit, temporal, epistemic, and provenance profiles rather than duplicating them.

## Rule

This file reports evidence, not optimism. Do not mark an item complete without a linked artifact or passing check.
