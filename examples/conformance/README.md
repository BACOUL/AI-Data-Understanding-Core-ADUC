# ADUC multi-model conformance package

This directory contains the provider-neutral Gate 6 test package and illustrative evaluator fixtures.

## Important status

The committed results are **illustrative only**. No external model provider was called to create them. They prove that the local harness works; they do not prove multi-model interoperability.

## Package contents

```text
package/
├── instructions.md
├── cases.json
├── result-template.json
└── manifest.json
```

The model receives the complete `package/` directory. It must not receive `expected.json`.

Verify the package before use:

```bash
python tools/aduc_conformance.py verify-package \
  examples/conformance/package
```

The verified package digest is recorded in every normalized result.

## Manual external run procedure

1. Verify the package.
2. Start a fresh model conversation or process.
3. Disable browsing, tools, retrieval and project memory.
4. Supply `instructions.md`, `cases.json` and `result-template.json` unchanged.
5. Preserve the raw model response in `results/raw/`.
6. Compute its SHA-256 digest.
7. Normalize the response to `schema/model-conformance-result.schema.json`.
8. Set `run.kind` to `external` only for a real independent run.
9. Record provider, implementation, model, version, parameters, execution time and repeat number.
10. Validate the normalized result locally.

Validate one result:

```bash
python tools/aduc_conformance.py validate-result \
  path/to/result.normalized.json \
  --package examples/conformance/package
```

Evaluate two or more results:

```bash
python tools/aduc_conformance.py evaluate \
  path/to/provider-a.normalized.json \
  path/to/provider-b.normalized.json \
  --package examples/conformance/package \
  --expected examples/conformance/expected.json
```

## Qualification rule

The report may set `interoperabilityProven` to `true` only when at least two qualifying external runs:

- come from distinct providers or independent implementations;
- use the same verified package digest;
- have verifiable raw-output files;
- pass the result schema;
- match the official expected semantics;
- agree with each other;
- declare that no external context was used.

The two committed `illustrative-*.normalized.json` fixtures must always produce:

```json
{
  "qualifyingExternalRuns": 0,
  "interoperabilityProven": false
}
```
