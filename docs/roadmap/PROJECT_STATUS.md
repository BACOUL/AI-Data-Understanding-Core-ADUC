# Project Status

- Project: AI Data Understanding Core (working name)
- Current phase: Phase 0 — Full-Core definition and public foundation
- Current release: unreleased
- Target release: `0.1.0-alpha.0`
- Overall status: mission, architecture, epistemic lifecycle, adoption gates, source binding, units, temporal semantics, entity identity, provenance, uncertainty, and data quality are defined and reference-tested; general relations are the next Core decision, and the official full-Core schema is not yet implemented

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
- ADR-0011 uncertainty and data-quality profile and evaluator;
- official adoption and value-validation gates;
- semantic-mapping profile, validator, comparator, JSON-LD/RDF tooling, and multi-model harness.

## Accepted Core decisions

### Epistemic lifecycle

Authority, confidence, conflict, and lifecycle are separate claims. Unresolved fields remain explicitly unknown; inferred, reviewed, verified, canonical, contested, and deprecated states are represented without silent promotion.

### Source binding

ADUC separates resource content, structural description, and local field reference. SHA-256 binds immutable content; mutable URLs and version labels are insufficient. Croissant, JSON Schema, OpenAPI, and DCAT retain authority for their structural models.

### Units and conversions

ADUC separates quantity kind, dimension, role, global unit identifier, local code, authority, and conversion evidence. Reference evidence includes five valid conversions, fifteen invalid cases, nine tests, and `89 °C = 192.2 °F`.

### Temporal semantics

Fixed instants, named-zone civil times, roles, precision, uncertainty, interval boundaries, exact durations, and calendar periods remain distinct. Ambiguous and nonexistent civil times block automatic use. The reference profile resolves `13/07/2026 14:00` in `Europe/Paris` to `2026-07-13T12:00:00Z`.

### Entity identity

Entity, identifier, label, relation assertion, and merge decision are separate. Inferred similarity remains `candidateOnly`; qualifying verified or canonical exact identity may produce `mergeAllowed`; `owl:sameAs` is never emitted for a candidate relation.

### Provenance and transformation lineage

ADUC reuses W3C PROV-O and separates artifacts, activities, agents, execution evidence, derivations, invalidations, disclosure, and reproducibility. Material inputs and outputs are hash-bound. Observed, attested, inferred, partial, and redacted lineage remain distinct. Manual intervention cannot be hidden.

Reference evidence:

- seven valid provenance cases;
- twenty invalid mutation fixtures;
- eight tests;
- one chain from source bytes through parsing, conversion, temporal resolution, identity linking, and comparison.

### Uncertainty and data quality

ADR-0011 separates:

```text
measurement or value uncertainty
semantic confidence
model confidence or calibrated probability
data-quality measurement
epistemic authority
```

The profile supports standard, expanded, relative, asymmetric, interval, distributional, categorical, and unknown uncertainty; missingness and censoring; DQV-compatible quality measurements; explicit dependence; and a small deterministic propagation subset.

Key rules:

- canonical authority never implies zero uncertainty;
- decimal formatting never establishes precision;
- model scores require calibration evidence before being treated as probability;
- unknown dependence blocks generic propagation;
- affine offsets apply to measured values, not uncertainty magnitudes;
- missing and censored values remain explicit;
- quality metrics remain tied to their metric, target, method, provenance, and disclosure state;
- unsupported propagation fails safely.

Reference evidence:

- fourteen valid uncertainty and quality cases;
- twenty-four invalid counterexamples;
- ten evaluator and CLI tests;
- `0.5 °C` standard uncertainty converts to `0.9 °F`;
- independent uncertainties `3` and `4` propagate to `5`;
- independent relative uncertainties `0.03` and `0.04` propagate to `0.05`;
- rectangular resolution `0.1` contributes `0.028867513459481`.

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
| Uncertainty and data quality | Defined and reference-tested |
| General relations | Next action |
| Policy and permitted use | Not implemented |
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

- general relation semantics;
- policy and permitted-use rules;
- normative full-Core object model and JSON Schema family;
- migration tooling into the complete Core envelope;
- JSON/CSV compiler and review interface;
- inference calibration and manual-versus-assisted performance;
- with/without-ADUC external model performance;
- two qualifying independent AI runs;
- final HTTPS namespace and project name;
- optional MCP adapter and commercial adoption model.

## Active blockers

- ADR-0012 general relation semantics does not exist;
- policy boundaries remain undefined;
- full-Core schema boundaries do not exist;
- the complete example is not yet schema-validatable;
- end-to-end comparison has not unified all profile dimensions;
- no qualifying external model runs or value benchmarks exist;
- the public name remains provisional.

## Next gate

Define general relation semantics, including predicate identity, direction, inverse, temporal and contextual qualification, authority, evidence, provenance, uncertainty, symmetry, transitivity, conflict, deprecation, and deterministic consumer behavior.

## Rule

This file reports evidence, not optimism. Do not mark an item complete without a linked artifact or passing check.
