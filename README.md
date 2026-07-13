# AI Data Understanding Core — ADUC

> Working name and experimental open specification. ADUC is not yet a recognized standard, and the public name must not be frozen before naming and trademark checks.

AI Data Understanding Core (ADUC) is a model-independent contract intended to let a data resource describe its structure, meaning, context, provenance, uncertainty, relations, and conditions of use to AI systems, agents, and applications.

## Mission

> Create an open standard that allows any data resource to describe its structure, meaning, context, provenance, uncertainty, relations, and conditions of use to any AI system.

## Initial promise

> Two incompatible sources described with ADUC can be understood and compared consistently by multiple AI systems without rebuilding a different semantic integration for every model.

ADUC reuses established standards instead of replacing JSON-LD/RDF, Croissant, PROV-O, DQV, ODRL, JSON Schema, OpenAPI, CloudEvents, DCAT, or MCP.

## Public website

The English-only public website source is maintained under `website/` for GitHub Pages:

- provisional URL: <https://bacoul.github.io/AI-Data-Understanding-Core-ADUC/>
- source: [`website/`](website/)
- deployment: [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml)

## Official Core direction

The complete candidate Core contains ten blocks:

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

The existing semantic-mapping tools are the first implemented experimental subset of the `semantics` block. They are not the complete ADUC Core.

## Complete epistemic lifecycle

ADR-0005 and [`EPISTEMIC_STATUS_MODEL_0_1.md`](spec/EPISTEMIC_STATUS_MODEL_0_1.md) define seven effective states without placing all of them in one ambiguous property:

```text
unknown      coverage record without a semantic target
inferred     assertion authority level
reviewed     assertion authority level
verified     assertion authority level
canonical    assertion authority level
contested    effective state from an unresolved challenge or conflict
deprecated   effective state from an immutable deprecation record
```

Assertions, challenges, resolutions, and deprecations are immutable records. Confidence is required for inferred assertions, conditional for reviewed or verified assertions, and forbidden for canonical assertions.

## Source description and immutable binding

ADR-0006 and [`SOURCE_DESCRIPTION_PROFILE_0_1.md`](spec/SOURCE_DESCRIPTION_PROFILE_0_1.md) define how an ADUC contract addresses the exact resource, structural description, and local field to which an assertion applies.

The model separates:

```text
resource content
structural description
local field reference
```

Supported binding modes are:

```text
content
description
content-and-description
```

Core rules:

- v0.1 reference bindings use SHA-256;
- a mutable URL or version label is not sufficient integrity evidence;
- linked descriptions bind exact raw bytes;
- embedded JSON descriptions use an RFC 8785 canonicalization scope;
- Croissant, JSON Schema, OpenAPI, and DCAT retain ownership of their structural models;
- JSON Pointer, Croissant field IDs, CSV headers, OpenAPI references, DCAT IRIs, and custom references use explicit schemes and bases;
- CSV header references require a fixed dialect and unique exact headers;
- stale, unavailable, ambiguous, or conflicting descriptions block automatic semantic use;
- legacy mappings are never migrated by guessing missing source evidence.

Reference verification:

```bash
python tools/aduc_source_binding.py \
  examples/source-description/reference-cases.json \
  examples/source-description/invalid-cases.json
```

## Adoption and value validation

The official cross-cutting plan is [`ADOPTION_AND_VALUE_VALIDATION.md`](docs/roadmap/ADOPTION_AND_VALUE_VALIDATION.md).

ADUC tooling is not successful merely because it generates a valid contract. Before the compiler and review interface can be called successful, the project must prove that:

- `infer + review` is materially faster than equivalent manual mapping;
- final semantic correctness is not lower than the manual baseline;
- low-support, unknown, and conflicting mappings remain visible;
- numeric confidence is method-bound and empirically calibrated before being described as probability;
- multi-model evaluation compares the same tasks with and without ADUC;
- MCP remains an optional adoption adapter rather than a Core dependency.

The future compiler must declare whether it used structure-only, sample-assisted, documentation-assisted, or publisher-assisted evidence. A high model score never creates review, verification, or canonical authority.

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
- Release: unreleased
- Target release: `0.1.0-alpha.0`
- Epistemic lifecycle: specified and reference-tested
- Source binding: specified and reference-tested
- Adoption/value validation: officially defined; benchmarks not yet run
- Next Core decision: units and conversions
- Full-Core conformance: not yet implemented
- Multi-model interoperability: harness available; qualifying external proof absent

See:

- [`PROJECT_STATUS.md`](docs/roadmap/PROJECT_STATUS.md)
- [`MASTER_PLAN.md`](docs/roadmap/MASTER_PLAN.md)
- [`ADOPTION_AND_VALUE_VALIDATION.md`](docs/roadmap/ADOPTION_AND_VALUE_VALIDATION.md)
- [`NEXT_ACTION.md`](docs/roadmap/NEXT_ACTION.md)

## Read first

1. [`ADUC_CORE_SPEC_0_1.md`](spec/ADUC_CORE_SPEC_0_1.md)
2. [`EPISTEMIC_STATUS_MODEL_0_1.md`](spec/EPISTEMIC_STATUS_MODEL_0_1.md)
3. [`ADR-0005`](docs/decisions/ADR-0005-complete-epistemic-lifecycle.md)
4. [`SOURCE_DESCRIPTION_PROFILE_0_1.md`](spec/SOURCE_DESCRIPTION_PROFILE_0_1.md)
5. [`ADR-0006`](docs/decisions/ADR-0006-source-description-and-binding.md)
6. [`ADOPTION_AND_VALUE_VALIDATION.md`](docs/roadmap/ADOPTION_AND_VALUE_VALIDATION.md)
7. [`OFFICIAL_PROJECT_STRUCTURE.md`](docs/project/OFFICIAL_PROJECT_STRUCTURE.md)
8. [`MASTER_PLAN.md`](docs/roadmap/MASTER_PLAN.md)
9. [`PROJECT_CHARTER.md`](docs/project/PROJECT_CHARTER.md)
10. [`NON_GOALS.md`](docs/project/NON_GOALS.md)
11. [`METHOD.md`](docs/method/METHOD.md)
12. [`AGENTS.md`](AGENTS.md) when using an AI coding agent

## First full-Core example

```text
examples/basic-json/river-r42.data.json
examples/basic-json/river-r42.aduc.json
```

The example is informative until the official full-Core JSON Schema exists.

## Implemented today

- full-Core mission, structure, working draft, and master plan;
- complete seven-state effective epistemic model;
- deterministic epistemic evaluator and counterexample suite;
- source-description and immutable source-binding profile;
- JSON, CSV, and embedded OpenAPI binding examples;
- deterministic source-binding evaluator and counterexamples;
- official adoption and value-validation plan;
- semantic-mapping assertion model;
- Draft 2020-12 mapping-profile schema;
- valid and invalid mapping fixtures;
- CLI validator with stable error codes;
- immutable authoring and review workflow;
- deterministic semantic comparator;
- JSON-LD context and offline RDF round-trip;
- provider-neutral multi-model conformance harness;
- English public website.

## Not yet implemented

- unit identifier and conversion strategy;
- final full-Core object model and schema family;
- temporal and entity-identity strategies;
- full-Core serialization of coverage, challenge, resolution, and deprecation records;
- JSON and CSV compiler;
- inference calibration report and labeled benchmark set;
- manual mapping versus `infer + review` benchmark;
- with and without ADUC multi-model comparison;
- minimal review web interface;
- complete unit conversion, temporal alignment, and entity-resolution comparison;
- public semantic registry;
- two qualifying external AI runs;
- optional MCP adapter;
- extensions and anticipation engine.

## Repository areas

- `spec/`: Core, epistemic, source-binding, and profile specifications
- `schema/`: machine-validatable JSON Schemas
- `context/`: pinned JSON-LD contexts
- `examples/`: raw sources, Core drafts, profiles, source bindings, epistemic cases, and conformance fixtures
- `tools/`: validation, source binding, lifecycle evaluation, comparison, RDF, conformance, and website checks
- `tests/`: validator, comparator, source binding, JSON-LD, conformance, epistemic, and roadmap tests
- `website/`: static English public website
- `docs/decisions/`: architecture decision records
- `docs/roadmap/`: master plan, adoption/value validation, project status, next action, and execution ledger

## Install development dependencies

```bash
python -m pip install -r requirements-dev.txt
```

## Run all local checks

```bash
python tools/validate_contracts.py
python -m unittest discover -s tests/validator -p "test_*.py"
python -m unittest discover -s tests/comparator -p "test_*.py"
python -m unittest discover -s tests/jsonld -p "test_*.py"
python -m unittest discover -s tests/conformance -p "test_*.py"
python -m unittest discover -s tests/epistemic -p "test_*.py"
python -m unittest discover -s tests/source_binding -p "test_*.py"
python -m unittest discover -s tests/roadmap -p "test_*.py"
python tools/validate_website.py
```

## Evaluate epistemic cases

```bash
python tools/aduc_epistemic.py \
  examples/epistemic-status/reference-cases.json

python tools/aduc_epistemic.py \
  examples/epistemic-status/invalid-cases.json
```

## Validate one semantic-mapping profile

```bash
python tools/aduc_validate.py examples/authoring/river/reviewed.aduc.json
```

## Compare two semantic-mapping profiles

```bash
python tools/aduc_compare.py \
  examples/comparison/fr/profile.aduc.json \
  examples/comparison/us/profile.aduc.json \
  --trusted-authority-b https://example.org/id/us-data-authority
```

The current comparator uses published semantic targets and mapping relations only. Unit conversion, time alignment, and entity identity remain `notEvaluated` when they are not declared.

## Expand and normalize a profile as RDF

```bash
python tools/aduc_rdf.py examples/authoring/river/reviewed.aduc.json
```

Official implemented mapping profiles use `urn:aduc:context:0.1`, resolved locally from `context/aduc-context-0.1.jsonld`.

## Preview the website locally

```bash
python -m http.server 8000 --directory website
```

Open `http://localhost:8000`.

## Licensing

- Reference code: Apache License 2.0
- Specification and documentation: CC BY 4.0 target before public release

See [`LICENSES.md`](LICENSES.md).
