# AI Data Understanding Core — ADUC

> Working name and experimental open specification. ADUC is not yet a recognized standard, and the public name must not be frozen before naming and trademark checks.

AI Data Understanding Core (ADUC) is a model-independent contract intended to let a data resource describe its structure, meaning, identity, context, provenance, uncertainty, relations, and conditions of use to AI systems, agents, and applications.

## Mission

> Create an open standard that allows any data resource to describe its structure, meaning, context, provenance, uncertainty, relations, and conditions of use to any AI system.

## Initial promise

> Two incompatible sources described with ADUC can be understood and compared consistently by multiple AI systems without rebuilding a different semantic integration for every model.

ADUC reuses established standards instead of replacing JSON-LD/RDF, Croissant, PROV-O, DQV, ODRL, JSON Schema, OpenAPI, CloudEvents, DCAT, QUDT, UCUM, RFC 3339, RFC 9557, IANA TZDB, OWL-Time, or MCP.

## Public website

- provisional URL: <https://bacoul.github.io/AI-Data-Understanding-Core-ADUC/>
- source: [`website/`](website/)
- deployment: [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml)

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

Reference verification:

```bash
python tools/aduc_source_binding.py \
  examples/source-description/reference-cases.json \
  examples/source-description/invalid-cases.json
```

### Units and deterministic conversions

ADR-0007 and [`UNIT_PROFILE_0_1.md`](spec/UNIT_PROFILE_0_1.md) define quantity kinds, unit identity, dimensional compatibility, quantity roles, exact conversion, uncertainty propagation, rounding, and provenance.

Reference rules:

- QUDT IRIs identify quantity kinds, units, and dimension vectors;
- case-sensitive UCUM codes are compact aliases where available;
- local codes such as `C`, `F`, or `%` never replace global identifiers;
- `known`, `unitless`, `unknown`, `arbitrary`, and `contextual` are distinct states;
- absolute temperature and temperature difference are distinct roles;
- v0.1 supports exact identity, multiplicative, and affine conversions;
- currency, calendar, nonlinear, and procedure-defined conversions remain blocked without dedicated context.

Reference evaluation:

```bash
python tools/aduc_units.py \
  examples/units/reference-cases.json \
  examples/units/invalid-cases.json
```

Validated examples include:

```text
89 °C = 192.2 °F
10 °C difference = 18.0 °F difference
1.5 m³/s = 1500.0 L/s
50 % = 0.500 unitless ratio
```

### Temporal semantics and timezone alignment

ADR-0008 and [`TEMPORAL_PROFILE_0_1.md`](spec/TEMPORAL_PROFILE_0_1.md) define temporal kinds, roles, lexical evidence, timezone resolution, DST ambiguity, intervals, durations, precision, uncertainty, and deterministic alignment.

Reference rules:

- RFC 3339 represents fixed instants with explicit offsets;
- RFC 9557 may attach a named timezone to a fixed timestamp;
- IANA TZDB identifiers and pinned releases resolve local civil times;
- a numeric offset is not a named timezone;
- observation, publication, processing, validity, sampling, and aggregation are distinct roles;
- ambiguous and nonexistent civil times block automatic use;
- exact durations and calendar-relative periods remain distinct;
- interval boundaries and uncertainty are explicit.

Reference evaluation:

```bash
python tools/aduc_time.py \
  examples/time/reference-cases.json \
  examples/time/invalid-cases.json
```

Validated conclusions include:

```text
13/07/2026 14:00 Europe/Paris = 2026-07-13T12:00:00Z
2026-10-25T02:30:00 Europe/Paris is ambiguous without an occurrence
2026-03-29T02:30:00 Europe/Paris does not exist
PT15M = 900 exact seconds
P1M remains a calendar period requiring context
```

The reference timezone subset is pinned to IANA TZDB `2026c` evidence and a repository SHA-256 digest.

## Adoption and value validation

The official cross-cutting plan is [`ADOPTION_AND_VALUE_VALIDATION.md`](docs/roadmap/ADOPTION_AND_VALUE_VALIDATION.md).

ADUC tooling is not successful merely because it produces valid files. Before the compiler and review interface can be called successful, the project must prove that:

- `infer + review` is materially faster than equivalent manual mapping;
- final semantic correctness is not lower than the manual baseline;
- unknown, low-support, and conflicting mappings remain visible;
- numeric confidence is calibrated before being described as probability;
- multi-model evaluation compares the same tasks with and without ADUC;
- MCP remains an optional adoption adapter rather than a Core dependency.

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
- Adoption/value validation: defined; benchmarks not yet run
- Next Core decision: entity identity and equivalence
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
6. [`ADOPTION_AND_VALUE_VALIDATION.md`](docs/roadmap/ADOPTION_AND_VALUE_VALIDATION.md)
7. [`MASTER_PLAN.md`](docs/roadmap/MASTER_PLAN.md)
8. [`METHOD.md`](docs/method/METHOD.md)
9. [`AGENTS.md`](AGENTS.md) for AI coding agents

## Implemented today

- project governance, roadmap, ADR method, and CI;
- full-Core working draft and first ten-block example;
- complete epistemic reference model and evaluator;
- source-binding profile and evaluator;
- unit profile, pinned registry subset, exact converter, and evaluator;
- temporal profile, pinned timezone subset, resolver, and alignment evaluator;
- semantic-mapping profile, validator, and comparator;
- JSON-LD context and offline RDF round-trip;
- provider-neutral multi-model conformance harness;
- English public website.

## Not yet implemented

- entity identity and equivalence;
- remaining provenance, uncertainty, relation, and policy decisions;
- official full-Core JSON Schema family;
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
python -m unittest discover -s tests/roadmap -p "test_*.py"
python tools/validate_website.py
```

## Existing reference commands

```bash
python tools/aduc_epistemic.py \
  examples/epistemic-status/reference-cases.json \
  examples/epistemic-status/invalid-cases.json
```

```bash
python tools/aduc_validate.py examples/authoring/river/reviewed.aduc.json
```

```bash
python tools/aduc_compare.py \
  examples/comparison/fr/profile.aduc.json \
  examples/comparison/us/profile.aduc.json \
  --trusted-authority-b https://example.org/id/us-data-authority
```

```bash
python tools/aduc_rdf.py examples/authoring/river/reviewed.aduc.json
```

## Website preview

```bash
python -m http.server 8000 --directory website
```

## Licensing

- Reference code: Apache License 2.0
- Specification and documentation: CC BY 4.0 target before public release

See [`LICENSES.md`](LICENSES.md).
