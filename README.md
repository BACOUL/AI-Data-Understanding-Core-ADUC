# AI Data Understanding Core - ADUC

> Working name and experimental open specification. ADUC is not yet a recognized standard, and the public name must not be frozen before naming and trademark checks.

ADUC is a machine-readable contract that makes a data resource's structure, meaning, context, identity, provenance, uncertainty, relations and use conditions explicit, validatable and portable across AI systems.

ADUC accompanies the original resource. It is not an AI model, database, universal ontology, agent protocol, legal system or production access-control layer. It composes existing standards instead of replacing them.

```text
Original data
      ->
ADUC understanding contract
      ->
Deterministic validation and comparison
      ->
Portable understanding across AI systems
```

## Public Website

- Canonical public URL: <https://bacoul.github.io/AI-Data-Understanding-Core-ADUC/>
- Static source: [`website/`](website/)
- Vercel deployment root: [`vercel.json`](vercel.json)
- Website source of truth: [`website/assets/site-data.json`](website/assets/site-data.json)

GitHub Pages is the canonical URL currently declared by the repository. Vercel publishes the same static directory and should be treated as deployment infrastructure unless a future decision changes the canonical base.

## Current Implementation

Available now:

- normative ten-block Core object model;
- minimum interoperable envelope: `aduc + resource + structure`;
- official modular JSON Schema Draft 2020-12 family with 14 local schema files;
- 11 complete valid Core contracts and 15 intentionally invalid Core contracts;
- local schema-plus-architecture validator;
- unified full-Core validator;
- deterministic full-Core comparator;
- 24 official comparison scenarios;
- profile evaluators for epistemic lifecycle, source binding, units, time, identity, provenance, uncertainty and quality, relations and policy;
- deterministic JSON and text reports;
- provider-neutral conformance infrastructure foundation;
- deterministic migration from the standalone semantic-mapping profile into complete ADUC Core contracts;
- deterministic formatting of complete validated Core contracts with exact-decimal preservation, stable reports and byte idempotence.
- provider-neutral full-Core conformance runner for validators, comparators and formatters.

Single active technical task:

- public SDK and package publication boundary for the accepted Core CLI tools.

Not yet available:

- TypeScript and Python SDKs;
- JSON/CSV compiler;
- graphical review interface;
- stabilized public PyPI/npm packages;
- production registry;
- MCP adapter;
- official extensions;
- external proof with two independent AI consumers;
- absolute "first in the world" claim.

## Adoption And Value Gates

[`ADOPTION_AND_VALUE_VALIDATION.md`](docs/roadmap/ADOPTION_AND_VALUE_VALIDATION.md) remains mandatory before compiler, review workflow or interoperability success claims.

Future adoption evidence must compare manual mapping with assisted ADUC workflows, measure review tax, and run controlled with and without ADUC evaluations. The JSON/CSV compiler remains blocked until those value and review gates are ready to run.

## Core Envelope

ADR-0014 and [`ADUC_CORE_MODEL_0_1.md`](spec/ADUC_CORE_MODEL_0_1.md) define the normative envelope and module boundaries.

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

Every addressable object has an absolute-IRI identifier, every Core reference resolves deterministically and every normative fact has one owning module.

## Validate A Core Contract

```bash
python tools/aduc_core.py validate examples/core/complete-model.example.json
python tools/aduc_core.py validate examples/core/complete-model.example.json --format json
```

Validation reports distinguish JSON loading, schema validation, architecture checks, profile evaluation and final outcome. Passing validation does not prove factual truth, authority, legal permission or operational safety.

## Compare Two Core Contracts

```bash
python tools/aduc_core.py compare examples/core/complete-model.example.json examples/core/complete-model.example.json
python tools/aduc_core.py compare contract-a.json contract-b.json --format json
```

Comparison separates mechanical `changeType` from normative `assessment`:

```text
equivalent
convertible
compatible
incompatible
unknown
contested
deprecated
prohibited
requiresHumanReview
```

Unsafe inputs with duplicate identifiers, unresolved references, ownership violations, resource-binding errors, namespace conflicts or unsupported required extensions are not indexed as trustworthy comparable contracts.

## Format A Complete Core Contract

```bash
python tools/aduc_core_format.py examples/core/complete-model.example.json --output complete-model.formatted.json
python tools/aduc_core_format.py examples/core/complete-model.example.json --output complete-model.formatted.json --report-format json
```

The formatter validates before and after serialization, preserves exact decimal values and every array order, rejects duplicate JSON members, writes atomically and produces identical bytes when run repeatedly. Exit code `2` means the valid contract still requires human review; formatting never removes that state.

## Run Full-Core Conformance

```bash
python tools/aduc_conformance.py run --suite conformance/full-core/0.1 --adapter python tools/aduc_conformance_reference_adapter.py
python tools/aduc_conformance.py run --suite conformance/full-core/0.1 --format json --adapter python tools/aduc_conformance_reference_adapter.py
```

The conformance runner executes a frozen local suite through a provider-neutral adapter contract. Passing the reference adapter is self-conformance only; independent conformance requires a genuinely separate implementation and explicit independence attestation.

## Run Checks

```bash
python -m pip install --disable-pip-version-check -r requirements-dev.txt
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
python -m unittest discover -s tests/core_schema -p "test_*.py"
python -m unittest discover -s tests/core_validator -p "test_*.py"
python -m unittest discover -s tests/core_comparator -p "test_*.py"
python -m unittest discover -s tests/core_formatter -p "test_*.py"
python -m unittest discover -s tests/core_conformance -p "test_*.py"
python tools/aduc_core_validate.py examples/core/complete-model.example.json
python tools/aduc_core.py validate examples/core/complete-model.example.json
python tools/aduc_core.py compare examples/core/complete-model.example.json examples/core/complete-model.example.json
python tools/aduc_conformance.py run --suite conformance/full-core/0.1 --format json --adapter python tools/aduc_conformance_reference_adapter.py
python -m unittest discover -s tests/roadmap -p "test_*.py"
python -m unittest discover -s tests/website -p "test_*.py"
python tools/validate_website.py
```

## Read First

1. [`ADUC_CORE_SPEC_0_1.md`](spec/ADUC_CORE_SPEC_0_1.md)
2. [`ADUC_CORE_MODEL_0_1.md`](spec/ADUC_CORE_MODEL_0_1.md)
3. [`ADUC_CORE_VALIDATION_0_1.md`](spec/ADUC_CORE_VALIDATION_0_1.md)
4. [`ADUC_CORE_COMPARISON_0_1.md`](spec/ADUC_CORE_COMPARISON_0_1.md)
5. [`ADUC_CONFORMANCE_RUNNER_0_1.md`](spec/ADUC_CONFORMANCE_RUNNER_0_1.md)
6. [`schema/aduc-core.schema.json`](schema/aduc-core.schema.json)
7. [`MASTER_PLAN.md`](docs/roadmap/MASTER_PLAN.md)
8. [`NEXT_ACTION.md`](docs/roadmap/NEXT_ACTION.md)

## Licensing

- Reference code: Apache License 2.0
- Specification and documentation: CC BY 4.0 target before public release

See [`LICENSES.md`](LICENSES.md).
