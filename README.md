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

## Candidate Core

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

# Accepted foundations

## Epistemic lifecycle

ADR-0005 and [`EPISTEMIC_STATUS_MODEL_0_1.md`](spec/EPISTEMIC_STATUS_MODEL_0_1.md) keep authority, confidence, conflict, and lifecycle separate.

```text
unknown
inferred
reviewed
verified
canonical
contested
deprecated
```

An inferred claim never becomes canonical merely because a model reports high confidence.

## Source description and immutable binding

ADR-0006 and [`SOURCE_DESCRIPTION_PROFILE_0_1.md`](spec/SOURCE_DESCRIPTION_PROFILE_0_1.md) bind assertions to exact resource bytes, structural descriptions, versions, SHA-256 evidence, and local field references.

Croissant, JSON Schema, OpenAPI, and DCAT retain authority for their structural models. Mutable URLs, stale descriptions, ambiguous CSV headers, and unresolved pointers block automatic use.

```bash
python tools/aduc_source_binding.py \
  examples/source-description/reference-cases.json \
  examples/source-description/invalid-cases.json
```

## Units and deterministic conversions

ADR-0007 and [`UNIT_PROFILE_0_1.md`](spec/UNIT_PROFILE_0_1.md) define quantity kinds, dimensions, quantity roles, global unit identity, exact conversions, rounding, uncertainty propagation, and provenance.

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

## Temporal semantics and timezone alignment

ADR-0008 and [`TEMPORAL_PROFILE_0_1.md`](spec/TEMPORAL_PROFILE_0_1.md) distinguish fixed instants, local civil time, intervals, exact durations, calendar periods, temporal roles, precision, uncertainty, and timezone evidence.

The reference profile resolves `13/07/2026 14:00` in `Europe/Paris` to `2026-07-13T12:00:00Z`. Ambiguous or nonexistent civil times block automatic use.

```bash
python tools/aduc_time.py \
  examples/time/reference-cases.json \
  examples/time/invalid-cases.json
```

## Entity identity and safe equivalence

ADR-0009 and [`IDENTITY_PROFILE_0_1.md`](spec/IDENTITY_PROFILE_0_1.md) separate entities, identifiers, labels, relation assertions, and merge decisions.

```text
canonical M42 / MAIN-B crosswalk -> mergeAllowed
inferred similarity -> candidateOnly
same text in different namespaces -> unresolved
reviewed negative identity -> differentEntity
```

`owl:sameAs` is emitted only after a qualifying verified or canonical identity decision.

```bash
python tools/aduc_identity.py \
  examples/identity/reference-cases.json \
  examples/identity/invalid-cases.json
```

## Provenance and transformation lineage

ADR-0010 and [`PROVENANCE_PROFILE_0_1.md`](spec/PROVENANCE_PROFILE_0_1.md) reuse PROV-O and define deterministic rules for exact artifact binding, transformations, agents, software or model execution, disclosure, invalidation, and reproducibility.

Observed, attested, inferred, partial, and redacted lineage remain distinct. A process described as `replayable` is not presented as deterministic reproduction, and material human intervention cannot be hidden.

```bash
python tools/aduc_provenance.py \
  examples/provenance/reference-cases.json \
  examples/provenance/invalid-cases.json
```

## Uncertainty and data quality

ADR-0011 and [`UNCERTAINTY_PROFILE_0_1.md`](spec/UNCERTAINTY_PROFILE_0_1.md) separate measurement uncertainty, semantic confidence, calibrated model probability, DQV-compatible quality, and epistemic authority.

The profile covers standard, expanded, relative, asymmetric, interval, distributional, categorical, and unknown uncertainty; missingness and censoring; dependence; deterministic propagation; and quality disclosure.

```text
0.5 °C standard uncertainty -> 0.9 °F
3 and 4 independent standard uncertainties -> 5
0.03 and 0.04 independent relative uncertainties -> 0.05
resolution 0.1 rectangular contribution -> 0.028867513459481
```

```bash
python tools/aduc_uncertainty.py \
  examples/uncertainty/reference-cases.json \
  examples/uncertainty/invalid-cases.json
```

## General relation semantics

ADR-0012 and [`RELATION_PROFILE_0_1.md`](spec/RELATION_PROFILE_0_1.md) separate vocabulary definitions, relation assertions, and consumer inferences.

The profile reuses RDF, OWL, SKOS, PROV-O, Dublin Core Terms, and explicit domain predicates. It preserves endpoint bindings, direction, authority, evidence, provenance, temporal and contextual scope, uncertainty, conflict, and lifecycle.

Core safeguards include:

```text
skos:closeMatch is not equality
owl:sameAs requires a qualifying identity decision
inverse relations require an authoritative inverse
transitivity is never assumed
skos:broader closure produces skos:broaderTransitive
correlation and temporal order do not establish causation
absence means unknown, not false
contested or deprecated relations block automatic use
```

The reference suite includes 13 valid cases, 20 invalid counterexamples, 10 tests, graph-conflict checks, and deterministic qualified JSON-LD/RDF export.

```bash
python tools/aduc_relations.py \
  examples/relations/reference-cases.json \
  examples/relations/invalid-cases.json
```

# Adoption and value validation

The mandatory cross-cutting plan is [`ADOPTION_AND_VALUE_VALIDATION.md`](docs/roadmap/ADOPTION_AND_VALUE_VALIDATION.md).

ADUC tooling is not successful merely because it produces valid files. Before compiler and review tooling can be called successful, the project must prove:

- `infer + review` is materially faster than equivalent manual mapping;
- final correctness is not lower than the manual mapping baseline;
- unknown, low-support, and conflicting mappings remain visible;
- confidence is calibrated before being described as probability;
- multi-model evaluation compares the same tasks with and without ADUC;
- MCP remains an optional adapter rather than a Core dependency.

The provisional alpha target is at least 30% lower median assisted human time, without lower final correctness or silently accepted critical false mappings.

# Mandatory construction order

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

# Current status

- Phase: Phase 0 — complete Core definition and public foundation
- Target release: `0.1.0-alpha.0`
- Epistemic lifecycle: specified and reference-tested
- Source binding: specified and reference-tested
- Units and conversions: specified and reference-tested
- Temporal semantics: specified and reference-tested
- Entity identity: specified and reference-tested
- Provenance and lineage: specified and reference-tested
- Uncertainty and data quality: specified and reference-tested
- General relations: specified and reference-tested
- Adoption/value validation: defined; benchmarks not yet run
- Next Core decision: policy and permitted-use conditions
- Full-Core JSON Schema: not yet implemented
- External multi-model proof: absent

See:

- [`PROJECT_STATUS.md`](docs/roadmap/PROJECT_STATUS.md)
- [`MASTER_PLAN.md`](docs/roadmap/MASTER_PLAN.md)
- [`NEXT_ACTION.md`](docs/roadmap/NEXT_ACTION.md)

# Read first

1. [`ADUC_CORE_SPEC_0_1.md`](spec/ADUC_CORE_SPEC_0_1.md)
2. [`EPISTEMIC_STATUS_MODEL_0_1.md`](spec/EPISTEMIC_STATUS_MODEL_0_1.md)
3. [`SOURCE_DESCRIPTION_PROFILE_0_1.md`](spec/SOURCE_DESCRIPTION_PROFILE_0_1.md)
4. [`UNIT_PROFILE_0_1.md`](spec/UNIT_PROFILE_0_1.md)
5. [`TEMPORAL_PROFILE_0_1.md`](spec/TEMPORAL_PROFILE_0_1.md)
6. [`IDENTITY_PROFILE_0_1.md`](spec/IDENTITY_PROFILE_0_1.md)
7. [`PROVENANCE_PROFILE_0_1.md`](spec/PROVENANCE_PROFILE_0_1.md)
8. [`UNCERTAINTY_PROFILE_0_1.md`](spec/UNCERTAINTY_PROFILE_0_1.md)
9. [`RELATION_PROFILE_0_1.md`](spec/RELATION_PROFILE_0_1.md)
10. [`ADOPTION_AND_VALUE_VALIDATION.md`](docs/roadmap/ADOPTION_AND_VALUE_VALIDATION.md)
11. [`MASTER_PLAN.md`](docs/roadmap/MASTER_PLAN.md)
12. [`AGENTS.md`](AGENTS.md)

# Not yet implemented

- policy and permitted-use profile;
- normative full-Core object model and JSON Schema family;
- ten valid and ten invalid complete Core examples;
- unified full-Core validator and comparator;
- JSON/CSV compiler and review UI;
- manual mapping versus assisted benchmark;
- controlled with and without ADUC external-model proof;
- optional MCP adapter, extensions, and anticipation engine.

# Run all checks

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
python -m unittest discover -s tests/relations -p "test_*.py"
python -m unittest discover -s tests/roadmap -p "test_*.py"
python -m unittest discover -s tests/website -p "test_*.py"
python tools/validate_website.py
```

# Licensing

- Reference code: Apache License 2.0
- Specification and documentation: CC BY 4.0 target before public release

See [`LICENSES.md`](LICENSES.md).
