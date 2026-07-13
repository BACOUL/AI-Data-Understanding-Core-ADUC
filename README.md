# AI Data Understanding Core — ADUC

> Working name and experimental open specification. ADUC is not yet a recognized standard, and the public name must not be frozen before naming and trademark checks.

AI Data Understanding Core (ADUC) is a model-independent contract intended to let a data resource describe its structure, meaning, identity, context, provenance, uncertainty, relations, and conditions of use to AI systems, agents, and applications.

## Mission

> Create an open standard that allows any data resource to describe its structure, meaning, context, provenance, uncertainty, relations, and conditions of use to any AI system.

## Initial promise

> Two incompatible sources described with ADUC can be understood and compared consistently by multiple AI systems without rebuilding a different semantic integration for every model.

ADUC composes established standards rather than replacing JSON-LD/RDF, Croissant, PROV-O, DQV, ODRL, JSON Schema, OpenAPI, CloudEvents, DCAT, QUDT, UCUM, RFC 3339, RFC 9557, IANA TZDB, OWL-Time, OWL identity, DID, GS1, LEI, or MCP.

## Public website

- provisional GitHub Pages URL: <https://bacoul.github.io/AI-Data-Understanding-Core-ADUC/>
- static source: [`website/`](website/)
- Vercel deployment root: [`vercel.json`](vercel.json)

## Core direction

The candidate Core contains ten blocks:

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

The existing tools are reference implementations of selected Core behavior. They are not yet the complete ADUC Core.

## Accepted foundations

### Epistemic lifecycle

ADR-0005 and [`EPISTEMIC_STATUS_MODEL_0_1.md`](spec/EPISTEMIC_STATUS_MODEL_0_1.md) separate:

```text
unknown      unresolved coverage without a fabricated target
inferred     automated or non-authoritative assertion
reviewed     accountable examination
verified     evidence-based verification procedure
canonical    source-authority publication
contested    unresolved immutable challenge
deprecated   immutable retirement record
```

Authority, confidence, conflict, and lifecycle remain separate claims.

### Source description and immutable binding

ADR-0006 and [`SOURCE_DESCRIPTION_PROFILE_0_1.md`](spec/SOURCE_DESCRIPTION_PROFILE_0_1.md) bind assertions to exact resource bytes, structural descriptions, and local fields.

```text
resource content
+ structural description
+ explicit local-reference scheme
+ version and SHA-256 evidence
```

Croissant, JSON Schema, OpenAPI, and DCAT retain ownership of their structural models. Mutable URLs, stale descriptions, ambiguous CSV headers, unresolved pointers, and conflicting copied structure block automatic use.

```bash
python tools/aduc_source_binding.py \
  examples/source-description/reference-cases.json \
  examples/source-description/invalid-cases.json
```

### Units and deterministic conversions

ADR-0007 and [`UNIT_PROFILE_0_1.md`](spec/UNIT_PROFILE_0_1.md) define quantity kinds, unit identity, dimensional compatibility, exact conversion, uncertainty propagation, rounding, and provenance.

Validated examples include:

```text
89 °C = 192.2 °F
10 °C difference = 18.0 °F difference
1.5 m³/s = 1500.0 L/s
50 % = 0.500 unitless ratio
```

```bash
python tools/aduc_units.py \
  examples/units/reference-cases.json \
  examples/units/invalid-cases.json
```

### Temporal semantics and timezone alignment

ADR-0008 and [`TEMPORAL_PROFILE_0_1.md`](spec/TEMPORAL_PROFILE_0_1.md) distinguish fixed instants, local civil time, intervals, exact durations, calendar periods, temporal roles, precision, uncertainty, and timezone provenance.

The reference case proves that `13/07/2026 14:00` in `Europe/Paris` resolves to `2026-07-13T12:00:00Z` under pinned timezone evidence. Ambiguous and nonexistent civil times block automatic use.

```bash
python tools/aduc_time.py \
  examples/time/reference-cases.json \
  examples/time/invalid-cases.json
```

### Entity identity and safe equivalence

ADR-0009 and [`IDENTITY_PROFILE_0_1.md`](spec/IDENTITY_PROFILE_0_1.md) distinguish entities, identifiers, labels, relation assertions, and consumer merge decisions.

```text
canonical M42 / MAIN-B crosswalk -> mergeAllowed
inferred similarity -> candidateOnly
same lexical value in different namespaces -> unresolved
reviewed negative relation -> differentEntity
broader/narrower relation -> relationOnly
```

`owl:sameAs` is exported only after a qualifying verified or canonical `mergeAllowed` decision.

```bash
python tools/aduc_identity.py \
  examples/identity/reference-cases.json \
  examples/identity/invalid-cases.json
```

### Provenance and transformation lineage

ADR-0010 and [`PROVENANCE_PROFILE_0_1.md`](spec/PROVENANCE_PROFILE_0_1.md) reuse W3C PROV-O and add deterministic ADUC rules for exact artifact binding, execution evidence, disclosure, and reproducibility.

The profile separates:

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

Material inputs and outputs are bound by SHA-256. Observed, attested, inferred, partial, and redacted lineage remain distinct. `replayable` is not presented as deterministic reproduction, and material human intervention cannot be hidden.

```bash
python tools/aduc_provenance.py \
  examples/provenance/reference-cases.json \
  examples/provenance/invalid-cases.json
```

### Uncertainty and data quality

ADR-0011 and [`UNCERTAINTY_PROFILE_0_1.md`](spec/UNCERTAINTY_PROFILE_0_1.md) separate:

```text
measurement uncertainty
semantic-mapping confidence
model confidence or calibrated probability
data-quality measurement
epistemic authority
```

The profile supports standard, expanded, relative, asymmetric, interval, distributional, categorical, and unknown uncertainty; missingness and censoring; DQV-compatible quality measurements; and a deliberately small deterministic propagation subset.

Validated reference results include:

```text
0.5 °C standard uncertainty -> 0.9 °F
3 and 4 independent standard uncertainties -> 5
0.03 and 0.04 independent relative uncertainties -> 0.05
resolution 0.1 rectangular contribution -> 0.028867513459481
```

Uncalibrated model scores are not probabilities. Canonical authority does not imply zero uncertainty. Unknown dependence blocks propagation, and unknown uncertainty is never replaced by zero.

```bash
python tools/aduc_uncertainty.py \
  examples/uncertainty/reference-cases.json \
  examples/uncertainty/invalid-cases.json
```

## Adoption and value validation

The official cross-cutting plan is [`ADOPTION_AND_VALUE_VALIDATION.md`](docs/roadmap/ADOPTION_AND_VALUE_VALIDATION.md).

ADUC tooling is not successful merely because it produces valid files. Before the compiler and review interface can be called successful, the project must prove that:

- `infer + review` is materially faster than equivalent manual mapping;
- final correctness is not lower than the manual mapping baseline;
- unknown, low-support, and conflicting mappings remain visible;
- numeric confidence is calibrated before being described as probability;
- multi-model evaluation compares the same tasks with and without ADUC;
- MCP remains an optional adoption adapter rather than a Core dependency.

The provisional alpha target is at least 30% lower median assisted human time with no lower final correctness and no silently accepted critical false mapping.

## Mandatory construction order

```text
1. Core
2. Schema
3. Validator
4. Examples
5. JSON/CSV compiler
6. Multi-model demonstration
7. Extensions
8. Anticipation engine
```

TimeProofs and the anticipation engine remain separate projects.

## Current status

- Phase: Phase 0 — complete Core definition and public foundation
- Target release: `0.1.0-alpha.0`
- Epistemic lifecycle: specified and reference-tested
- Source binding: specified and reference-tested
- Units and conversions: specified and reference-tested
- Temporal semantics: specified and reference-tested
- Entity identity: specified and reference-tested
- Provenance and lineage: specified and reference-tested
- Uncertainty and data quality: specified and reference-tested
- Adoption/value validation: defined; benchmarks not yet run
- Next Core decision: general relation semantics
- Full-Core JSON Schema: not yet implemented
- External multi-model proof: absent

See:

- [`PROJECT_STATUS.md`](docs/roadmap/PROJECT_STATUS.md)
- [`MASTER_PLAN.md`](docs/roadmap/MASTER_PLAN.md)
- [`ADOPTION_AND_VALUE_VALIDATION.md`](docs/roadmap/ADOPTION_AND_VALUE_VALIDATION.md)
- [`NEXT_ACTION.md`](docs/roadmap/NEXT_ACTION.md)

## Read first

1. [`ADUC_CORE_SPEC_0_1.md`](spec/ADUC_CORE_SPEC_0_1.md)
2. [`EPISTEMIC_STATUS_MODEL_0_1.md`](spec/EPISTEMIC_STATUS_MODEL_0_1.md)
3. [`SOURCE_DESCRIPTION_PROFILE_0_1.md`](spec/SOURCE_DESCRIPTION_PROFILE_0_1.md)
4. [`UNIT_PROFILE_0_1.md`](spec/UNIT_PROFILE_0_1.md)
5. [`TEMPORAL_PROFILE_0_1.md`](spec/TEMPORAL_PROFILE_0_1.md)
6. [`IDENTITY_PROFILE_0_1.md`](spec/IDENTITY_PROFILE_0_1.md)
7. [`PROVENANCE_PROFILE_0_1.md`](spec/PROVENANCE_PROFILE_0_1.md)
8. [`UNCERTAINTY_PROFILE_0_1.md`](spec/UNCERTAINTY_PROFILE_0_1.md)
9. [`ADOPTION_AND_VALUE_VALIDATION.md`](docs/roadmap/ADOPTION_AND_VALUE_VALIDATION.md)
10. [`MASTER_PLAN.md`](docs/roadmap/MASTER_PLAN.md)
11. [`METHOD.md`](docs/method/METHOD.md)
12. [`AGENTS.md`](AGENTS.md) for AI coding agents

## Implemented today

- governance, roadmap, ADR method, CI, and public website;
- full-Core working draft and first ten-block example;
- epistemic, source-binding, unit, temporal, identity, provenance, and uncertainty profiles with deterministic evaluators;
- semantic-mapping profile, validator, and comparator;
- JSON-LD context and offline RDF round-trip;
- provider-neutral multi-model conformance harness.

## Not yet implemented

- general-relation and policy profiles;
- normative full-Core object model and JSON Schema family;
- ten valid and ten invalid complete Core examples;
- complete Core validator and SDKs;
- JSON/CSV compiler and review UI;
- inference calibration and manual-versus-assisted benchmark;
- controlled with/without-ADUC external model proof;
- optional MCP adapter, extensions, and anticipation engine.

## Run all checks

```bash
python -m pip install -r requirements-dev.txt
python tools/validate_contracts.py
python -m unittest discover -s tests/validator -p "test_*.py"
python -m unittest discover -s tests/comparator -p "test_*.py"
python -m unittest discover -s tests/jsonld -p "test_*.py"
python -m unittest discover -s tests/conformance -p "test_*.py"
python -m unittest discover -s tests/epistemic -p "test_*.py"
python -m unittest discover -s tests/source_binding -p "test_*.py"
python -m unittest discover -s tests/units -p "test_*.py"
python -m unittest discover -s tests/time -p "test_*.py"
python -m unittest discover -s tests/identity -p "test_*.py"
python -m unittest discover -s tests/provenance -p "test_*.py"
python -m unittest discover -s tests/uncertainty -p "test_*.py"
python -m unittest discover -s tests/roadmap -p "test_*.py"
python -m unittest discover -s tests/website -p "test_*.py"
python tools/validate_website.py
```

## Website preview

```bash
python -m http.server 8000 --directory website
```

## Licensing

- Reference code: Apache License 2.0
- Specification and documentation: CC BY 4.0 target before public release

See [`LICENSES.md`](LICENSES.md).
