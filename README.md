# AI Data Understanding Core — ADUC

> Working name and experimental open specification. ADUC is not yet a recognized standard, and the public name must not be frozen before naming and trademark checks.

AI Data Understanding Core (ADUC) is a model-independent contract intended to let a data resource describe its structure, meaning, context, provenance, uncertainty, relations, and conditions of use to AI systems, agents, and applications.

## Mission

> Create an open standard that allows any data resource to describe its structure, meaning, context, provenance, uncertainty, relations, and conditions of use to any AI system.

## Initial promise

> Two incompatible sources described with ADUC can be understood and compared consistently by multiple AI systems without rebuilding a different semantic integration for every model.

ADUC reuses established standards instead of replacing JSON-LD/RDF, Croissant, PROV-O, DQV, ODRL, JSON Schema, OpenAPI, CloudEvents, or MCP.

## Public website

The first English-only public website is maintained under `website/` and is designed for GitHub Pages:

- provisional URL: <https://bacoul.github.io/AI-Data-Understanding-Core-ADUC/>
- website source: [`website/`](website/)
- deployment: [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml)

The Pages source may need to be set to **GitHub Actions** once in repository settings after the deployment workflow is merged.

## Official project direction

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

The existing semantic-mapping schema, validator, comparator, JSON-LD/RDF tooling, and conformance harness are preserved as the first implemented experimental subset of the `semantics` block and its consumer behavior.

They are not the complete ADUC Core.

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

TimeProofs and the anticipation engine remain separate projects. TimeProofs may later prove release dates, but it is not required to create, understand, or validate an ADUC contract.

## Current project status

- Phase: Phase 0 — complete Core definition and public foundation
- Release: unreleased
- Target release: `0.1.0-alpha.0`
- Full-Core conformance: not yet implemented
- Multi-model interoperability: harness available; qualifying external proof absent

See:

- [`PROJECT_STATUS.md`](docs/roadmap/PROJECT_STATUS.md)
- [`MASTER_PLAN.md`](docs/roadmap/MASTER_PLAN.md)
- [`NEXT_ACTION.md`](docs/roadmap/NEXT_ACTION.md)

## Read first

1. [`ADUC_CORE_SPEC_0_1.md`](spec/ADUC_CORE_SPEC_0_1.md)
2. [`OFFICIAL_PROJECT_STRUCTURE.md`](docs/project/OFFICIAL_PROJECT_STRUCTURE.md)
3. [`MASTER_PLAN.md`](docs/roadmap/MASTER_PLAN.md)
4. [`PROJECT_CHARTER.md`](docs/project/PROJECT_CHARTER.md)
5. [`NON_GOALS.md`](docs/project/NON_GOALS.md)
6. [`ADR-0004`](docs/decisions/ADR-0004-full-core-program-and-semantic-profile-position.md)
7. [`METHOD.md`](docs/method/METHOD.md)
8. [`AGENTS.md`](AGENTS.md) when using an AI coding agent

## First complete full-Core example

```text
examples/basic-json/river-r42.data.json
examples/basic-json/river-r42.aduc.json
```

The example shows how a raw river observation gains field meaning, units, code-list interpretation, identity, time context, provenance, uncertainty, relations, and usage conditions.

It is an informative draft example until the final full-Core JSON Schema exists.

## What is implemented today

- semantic-mapping assertion model;
- Draft 2020-12 mapping-profile schema;
- valid and invalid mapping fixtures;
- CLI validator with stable error codes;
- immutable authoring and review workflow;
- deterministic semantic comparator;
- JSON-LD context and offline RDF round-trip;
- provider-neutral multi-model conformance harness;
- English public website.

## What is not yet implemented

- final full-Core object model and schema family;
- complete seven-state epistemic lifecycle in the schema;
- JSON and CSV compiler;
- minimal review web interface;
- complete unit conversion, temporal alignment, and entity-resolution comparison;
- public semantic registry;
- two qualifying external AI runs;
- extensions and anticipation engine.

## Repository areas

- `spec/`: Core and profile specification drafts
- `schema/`: machine-validatable JSON Schemas
- `context/`: pinned JSON-LD contexts
- `examples/`: raw sources, Core drafts, profiles, and conformance fixtures
- `tools/`: validation, comparison, RDF, conformance, and website checks
- `tests/`: schema, validator, comparator, JSON-LD, and conformance tests
- `website/`: static English public website
- `docs/decisions/`: architecture decision records
- `docs/roadmap/`: master plan, project status, next action, and execution ledger

## Install development dependencies

```bash
python -m pip install -r requirements-dev.txt
```

## Run the complete local checks

```bash
python tools/validate_contracts.py
python -m unittest discover -s tests/validator -p "test_*.py"
python -m unittest discover -s tests/comparator -p "test_*.py"
python -m unittest discover -s tests/jsonld -p "test_*.py"
python -m unittest discover -s tests/conformance -p "test_*.py"
python tools/validate_website.py
```

## Validate one semantic-mapping profile

```bash
python tools/aduc_validate.py examples/authoring/river/reviewed.aduc.json
```

JSON report:

```bash
python tools/aduc_validate.py \
  examples/authoring/river/reviewed.aduc.json \
  --format json
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

Official implemented mapping profiles use `urn:aduc:context:0.1`, resolved locally from `context/aduc-context-0.1.jsonld`. Conformance processing performs no remote context fetch.

## Preview the website locally

```bash
python -m http.server 8000 --directory website
```

Open `http://localhost:8000`.

## Licensing

- Reference code: Apache License 2.0
- Specification and documentation: CC BY 4.0 target before public release

See [`LICENSES.md`](LICENSES.md).
