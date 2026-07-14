# AI Data Understanding Core — ADUC

> Working name and experimental open specification. ADUC is not yet a recognized standard, and the public name must not be frozen before naming and trademark checks.

ADUC is a model-independent contract intended to let a data resource describe its structure, meaning, identity, context, provenance, uncertainty, relations and conditions of use to AI systems, agents and applications.

## Mission

> Create an open standard that allows any data resource to describe its structure, meaning, context, provenance, uncertainty, relations and conditions of use to any AI system.

## Initial promise

> Two incompatible sources described with ADUC can be understood and compared consistently by multiple AI systems without rebuilding a different semantic integration for every model.

ADUC composes established standards rather than replacing JSON-LD/RDF, Croissant, PROV-O, DQV, ODRL, JSON Schema, OpenAPI, CloudEvents, DCAT, QUDT, UCUM, RFC 3339, RFC 9557, IANA TZDB, OWL-Time, OWL identity, DID, GS1, LEI or MCP.

## Public website

- provisional GitHub Pages URL: <https://bacoul.github.io/AI-Data-Understanding-Core-ADUC/>
- static source: [`website/`](website/)
- Vercel deployment root: [`vercel.json`](vercel.json)

# Frozen Core object model

ADR-0014 and [`ADUC_CORE_MODEL_0_1.md`](spec/ADUC_CORE_MODEL_0_1.md) freeze the normative envelope and module boundaries.

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

The minimum interoperable contract is `aduc + resource + structure`. Every addressable object has an absolute-IRI identifier, every Core reference resolves deterministically and every normative fact has one owning module.

The machine-readable architecture is in [`core-module-manifest.json`](spec/core-module-manifest.json). The complete ten-block example is [`complete-model.example.json`](examples/core/complete-model.example.json).

```bash
python tools/aduc_core_model.py
python -m unittest discover -s tests/core_model -p "test_*.py"
```

The architecture checker enforces the frozen object model. It is not the future official JSON Schema validator.

# Accepted foundations

## Epistemic lifecycle

ADR-0005 and [`EPISTEMIC_STATUS_MODEL_0_1.md`](spec/EPISTEMIC_STATUS_MODEL_0_1.md) keep authority, confidence, conflict and lifecycle separate.

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

ADR-0006 and [`SOURCE_DESCRIPTION_PROFILE_0_1.md`](spec/SOURCE_DESCRIPTION_PROFILE_0_1.md) bind assertions to exact resource bytes, structural descriptions, versions, SHA-256 evidence and field references.

```bash
python tools/aduc_source_binding.py examples/source-description/reference-cases.json examples/source-description/invalid-cases.json
```

## Units and deterministic conversions

ADR-0007 and [`UNIT_PROFILE_0_1.md`](spec/UNIT_PROFILE_0_1.md) define quantity kinds, dimensions, quantity roles, global unit identity, exact conversions, rounding, uncertainty propagation and provenance.

```text
89 °C = 192.2 °F
10 °C difference = 18.0 °F difference
1.5 m³/s = 1500.0 L/s
50 % = 0.500 unitless ratio
```

```bash
python tools/aduc_units.py examples/units/reference-cases.json examples/units/invalid-cases.json
```

## Temporal semantics and timezone alignment

ADR-0008 and [`TEMPORAL_PROFILE_0_1.md`](spec/TEMPORAL_PROFILE_0_1.md) distinguish fixed instants, local civil time, intervals, exact durations, calendar periods, temporal roles, precision, uncertainty and timezone evidence.

The reference profile resolves `13/07/2026 14:00` in `Europe/Paris` to `2026-07-13T12:00:00Z`.

```bash
python tools/aduc_time.py examples/time/reference-cases.json examples/time/invalid-cases.json
```

## Entity identity and safe equivalence

ADR-0009 and [`IDENTITY_PROFILE_0_1.md`](spec/IDENTITY_PROFILE_0_1.md) separate entities, identifiers, labels, relation assertions and merge decisions.

```text
canonical M42 / MAIN-B crosswalk -> mergeAllowed
inferred similarity -> candidateOnly
same text in different namespaces -> unresolved
reviewed negative identity -> differentEntity
```

`owl:sameAs` is emitted only after a qualifying verified or canonical identity decision.

```bash
python tools/aduc_identity.py examples/identity/reference-cases.json examples/identity/invalid-cases.json
```

## Provenance and transformation lineage

ADR-0010 and [`PROVENANCE_PROFILE_0_1.md`](spec/PROVENANCE_PROFILE_0_1.md) reuse PROV-O and define exact artifact binding, transformations, agents, software or model execution, disclosure, invalidation and reproducibility.

A process described as `replayable` is not presented as deterministic reproduction.

```bash
python tools/aduc_provenance.py examples/provenance/reference-cases.json examples/provenance/invalid-cases.json
```

## Uncertainty and data quality

ADR-0011 and [`UNCERTAINTY_PROFILE_0_1.md`](spec/UNCERTAINTY_PROFILE_0_1.md) separate measurement uncertainty, semantic confidence, calibrated model probability, DQV-compatible quality and epistemic authority.

```text
0.5 °C standard uncertainty -> 0.9 °F
3 and 4 independent standard uncertainties -> 5
0.03 and 0.04 independent relative uncertainties -> 0.05
resolution 0.1 rectangular contribution -> 0.028867513459481
```

```bash
python tools/aduc_uncertainty.py examples/uncertainty/reference-cases.json examples/uncertainty/invalid-cases.json
```

## General relation semantics

ADR-0012 and [`RELATION_PROFILE_0_1.md`](spec/RELATION_PROFILE_0_1.md) preserve endpoint binding, direction, authority, evidence, provenance, temporal and contextual scope, uncertainty, conflict and lifecycle.

```text
skos:closeMatch is not equality
owl:sameAs requires a qualifying identity decision
inverse relations require an authoritative inverse
transitivity is never assumed
correlation and temporal order do not establish causation
absence means unknown, not false
```

```bash
python tools/aduc_relations.py examples/relations/reference-cases.json examples/relations/invalid-cases.json
```

## Policy and permitted-use conditions

ADR-0013 and [`POLICY_PROFILE_0_1.md`](spec/POLICY_PROFILE_0_1.md) reuse ODRL while preserving exact target binding, controlled purposes, parties, evidence, provenance, validity and lifecycle.

```text
permit
deny
notApplicable
indeterminate
requiresHumanReview
```

A public classification is not universal permission, and ADUC policy evaluation is not legal advice or access-control enforcement.

```bash
python tools/aduc_policy.py examples/policy/reference-cases.json examples/policy/invalid-cases.json
```

# Adoption and value validation

The mandatory cross-cutting plan is [`ADOPTION_AND_VALUE_VALIDATION.md`](docs/roadmap/ADOPTION_AND_VALUE_VALIDATION.md).

Before compiler and review tooling can be called successful, the project must prove:

- `infer + review` is materially faster than equivalent manual mapping;
- final correctness is not lower than the manual mapping baseline;
- unknown, low-support and conflicting mappings remain visible;
- confidence is calibrated before being described as probability;
- multi-model evaluation compares the same tasks with and without ADUC;
- MCP remains an optional adapter rather than a Core dependency.

The provisional alpha target is at least 30% lower median assisted human time without lower final correctness or silently accepted critical false mappings.

# Mandatory construction order

```text
1. Core model
2. Schema family
3. Unified validator
4. Complete examples
5. JSON/CSV compiler
6. Multi-model demonstration
7. Extensions
8. Anticipation engine
```

TimeProofs and the anticipation engine remain separate projects.

# Current status

- Phase: Phase 0 — complete Core definition and public foundation
- Target release: `0.1.0-alpha.0`
- Nine domain profiles: specified and reference-tested
- Normative Core object model: frozen and architecture-tested
- Complete ten-block model example: created, not yet schema-validated
- Next action: implement the official modular full-Core JSON Schema family
- Full-Core schema validator: not yet implemented
- External multi-model proof: absent

See [`PROJECT_STATUS.md`](docs/roadmap/PROJECT_STATUS.md), [`MASTER_PLAN.md`](docs/roadmap/MASTER_PLAN.md) and [`NEXT_ACTION.md`](docs/roadmap/NEXT_ACTION.md).

# Read first

1. [`ADUC_CORE_SPEC_0_1.md`](spec/ADUC_CORE_SPEC_0_1.md)
2. [`ADUC_CORE_MODEL_0_1.md`](spec/ADUC_CORE_MODEL_0_1.md)
3. [`CORE_MODULE_BOUNDARIES_0_1.md`](docs/architecture/CORE_MODULE_BOUNDARIES_0_1.md)
4. [`EPISTEMIC_STATUS_MODEL_0_1.md`](spec/EPISTEMIC_STATUS_MODEL_0_1.md)
5. [`SOURCE_DESCRIPTION_PROFILE_0_1.md`](spec/SOURCE_DESCRIPTION_PROFILE_0_1.md)
6. [`UNIT_PROFILE_0_1.md`](spec/UNIT_PROFILE_0_1.md)
7. [`TEMPORAL_PROFILE_0_1.md`](spec/TEMPORAL_PROFILE_0_1.md)
8. [`IDENTITY_PROFILE_0_1.md`](spec/IDENTITY_PROFILE_0_1.md)
9. [`PROVENANCE_PROFILE_0_1.md`](spec/PROVENANCE_PROFILE_0_1.md)
10. [`UNCERTAINTY_PROFILE_0_1.md`](spec/UNCERTAINTY_PROFILE_0_1.md)
11. [`RELATION_PROFILE_0_1.md`](spec/RELATION_PROFILE_0_1.md)
12. [`POLICY_PROFILE_0_1.md`](spec/POLICY_PROFILE_0_1.md)
13. [`ADOPTION_AND_VALUE_VALIDATION.md`](docs/roadmap/ADOPTION_AND_VALUE_VALIDATION.md)
14. [`AGENTS.md`](AGENTS.md)

# Not yet implemented

- official modular full-Core JSON Schema family;
- ten complete valid and ten complete invalid schema fixtures;
- unified full-Core validator and comparator;
- JSON/CSV compiler and review UI;
- manual mapping versus assisted benchmark;
- controlled with and without ADUC external-model proof;
- optional MCP adapter, extensions and anticipation engine.

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
python -m unittest discover -s tests/policy -p "test_*.py"
python -m unittest discover -s tests/core_model -p "test_*.py"
python -m unittest discover -s tests/roadmap -p "test_*.py"
python -m unittest discover -s tests/website -p "test_*.py"
python tools/validate_website.py
```

# Licensing

- Reference code: Apache License 2.0
- Specification and documentation: CC BY 4.0 target before public release

See [`LICENSES.md`](LICENSES.md).