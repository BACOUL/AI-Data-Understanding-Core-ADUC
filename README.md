# AI Data Understanding Core

> Working title and experimental specification. Not yet a recognized standard.

AI Data Understanding Core (ADUC) is an open, model-independent contract intended to let a data source describe its structure, semantics, context, provenance, uncertainty, relations, and usage policy to AI systems.

## Initial promise

Two otherwise incompatible JSON or CSV sources, each accompanied by an ADUC contract, should be interpretable and comparable by multiple AI systems without rebuilding a separate semantic integration for every model.

## Project status

- Stage: Phase 0 — definition
- Release line: `0.1.0-alpha.x`
- Current task: see [`docs/roadmap/NEXT_ACTION.md`](docs/roadmap/NEXT_ACTION.md)
- Status: see [`docs/roadmap/PROJECT_STATUS.md`](docs/roadmap/PROJECT_STATUS.md)

## Read first

1. [`PROJECT_CHARTER.md`](docs/project/PROJECT_CHARTER.md)
2. [`NON_GOALS.md`](docs/project/NON_GOALS.md)
3. [`METHOD.md`](docs/method/METHOD.md)
4. [`NEXT_ACTION.md`](docs/roadmap/NEXT_ACTION.md)
5. [`AGENTS.md`](AGENTS.md) when using an AI coding agent

## Repository areas

- `spec/`: normative specification drafts
- `schema/`: machine-validatable JSON Schemas
- `examples/`: valid and invalid examples
- `tools/`: reference validation tools
- `tests/`: conformance tests
- `docs/decisions/`: architecture decision records
- `docs/roadmap/`: status, next action, and execution ledger

## Local validation

```bash
python -m pip install jsonschema
python tools/validate_contracts.py
```

## Licensing

- Code: Apache License 2.0
- Specification and documentation: intended to be CC BY 4.0 before public release

See [`LICENSES.md`](LICENSES.md).
