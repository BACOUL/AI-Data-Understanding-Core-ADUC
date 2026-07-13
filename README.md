# AI Data Understanding Core

> Working title and experimental profile. Not yet a recognized standard.

AI Data Understanding Core (ADUC) is an open, model-independent semantic mapping and conformance profile. It preserves how a local field is mapped to an existing semantic identifier, who asserted that mapping, whether it is inferred or authoritative, what evidence supports it, and how compatible consumers must handle uncertainty or conflict.

ADUC reuses established standards instead of replacing JSON-LD/RDF, Croissant, PROV-O, DQV, ODRL, JSON Schema, OpenAPI, CloudEvents or MCP.

## Initial promise

Two otherwise incompatible JSON or CSV datasets, accompanied by the same source descriptions and ADUC mapping assertions, should be interpreted compatibly by independent AI systems without rebuilding provider-specific semantic mappings.

## Project status

- Stage: Gate 3 — reference validator
- Release line: `0.1.0-alpha.x`
- Current task: see [`docs/roadmap/NEXT_ACTION.md`](docs/roadmap/NEXT_ACTION.md)
- Status: see [`docs/roadmap/PROJECT_STATUS.md`](docs/roadmap/PROJECT_STATUS.md)

## Read first

1. [`PROJECT_CHARTER.md`](docs/project/PROJECT_CHARTER.md)
2. [`NON_GOALS.md`](docs/project/NON_GOALS.md)
3. [`METHOD.md`](docs/method/METHOD.md)
4. [`ADR-0002`](docs/decisions/ADR-0002-aduc-as-an-ai-semantic-mapping-profile.md)
5. [`Semantic Mapping Assertion Model`](spec/SEMANTIC_MAPPING_ASSERTION_MODEL_0_1.md)
6. [`NEXT_ACTION.md`](docs/roadmap/NEXT_ACTION.md)
7. [`AGENTS.md`](AGENTS.md) when using an AI coding agent

## Repository areas

- `spec/`: information model and conformance drafts
- `schema/`: machine-validatable JSON Schemas
- `examples/`: source and profile examples
- `tools/`: reference validation tools
- `tests/`: schema and semantic-validator tests
- `docs/decisions/`: architecture decision records
- `docs/roadmap/`: status, next action, and execution ledger

## Install development dependencies

```bash
python -m pip install -r requirements-dev.txt
```

## Validate the official fixtures

```bash
python tools/validate_contracts.py
python -m unittest discover -s tests/validator -p "test_*.py"
```

## Validate one profile

Text report:

```bash
python tools/aduc_validate.py path/to/profile.json
```

JSON report:

```bash
python tools/aduc_validate.py path/to/profile.json --format json
```

Declare a locally trusted canonical authority:

```bash
python tools/aduc_validate.py path/to/profile.json \
  --trusted-authority https://publisher.example/id/data-authority
```

A locally trusted authority option does not provide cryptographic or global proof. Unverified canonical authority is reported as a warning.

## Licensing

- Code: Apache License 2.0
- Specification and documentation: intended to be CC BY 4.0 before public release

See [`LICENSES.md`](LICENSES.md).
