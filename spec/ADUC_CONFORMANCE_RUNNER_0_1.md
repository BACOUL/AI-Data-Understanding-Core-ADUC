# ADUC Conformance Runner 0.1

## Scope

This specification defines the local provider-neutral full-Core conformance runner for ADUC Core validator, comparator and formatter implementations.

The runner tests observable behavior through a public adapter protocol. It does not make the Python implementation normative and it does not prove independent interoperability by itself.

## Suite Location

The v0.1 frozen suite is:

```text
conformance/full-core/0.1/
```

It contains:

- `manifest.json`
- `manifest.schema.json`
- validation fixtures
- comparison fixtures
- formatting fixtures
- adversarial adapter expectations

## CLI

```bash
python tools/aduc_conformance.py run \
  --suite conformance/full-core/0.1 \
  --format json \
  --adapter python tools/aduc_conformance_reference_adapter.py
```

`--adapter` is an argv list and should be the last option. The runner never uses shell interpolation.

Output formats:

- `json`: stable machine-readable report
- `text`: deterministic human-readable summary

Exit codes:

- `0`: all required cases pass and no required capability is unsupported
- `1`: at least one case fails, is unsupported, times out, exceeds resource limits or returns an invalid response
- `2`: legacy multi-model conformance input error for older commands

## Adapter Protocol

Protocol identifier:

```text
urn:aduc:full-core-conformance-adapter:0.1
```

Required operations:

```text
declareCapabilities
validate <contract.json>
compare <left.json> <right.json>
format <contract.json>
```

Declaration response:

```json
{
  "adapterProtocol": "urn:aduc:full-core-conformance-adapter:0.1",
  "operation": "declareCapabilities",
  "implementation": {
    "id": "urn:example:implementation",
    "name": "Example implementation",
    "version": "0.1.0",
    "kind": "external"
  },
  "capabilities": {
    "validate": true,
    "compare": true,
    "format": true,
    "classes": ["fullCoreValidator", "fullCoreComparator", "fullCoreFormatter"]
  },
  "independenceAttestation": {
    "genuineSeparateImplementation": true,
    "scope": "Independent implementation of the public specification."
  }
}
```

Operation response:

```json
{
  "adapterProtocol": "urn:aduc:full-core-conformance-adapter:0.1",
  "operation": "validate",
  "implementation": {
    "id": "urn:example:implementation",
    "kind": "external"
  },
  "report": {},
  "exitCode": 0
}
```

The `report` object is the implementation's own validation, comparison or formatting report. The conformance runner inspects stable public fields only.

## Required Stable Fields

Validation expectations may inspect:

- `valid`
- `outcome`
- diagnostic `code`
- profile evaluation `status`
- operation `exitCode`

Comparison expectations may inspect:

- `overall`
- `overallAssessment`
- change `code`
- change `assessment`
- operation `exitCode`

Formatter expectations may inspect:

- `formatted`
- `outcome`
- operation `exitCode`
- optional formatted output digest metadata

## Runner Report

The JSON report contains:

- `reportVersion`
- `protocol`
- suite identity and manifest digest
- adapter protocol
- implementation declaration
- claimed conformance classes
- evidence mode and self/independent flags
- result summary
- sorted case results

No timestamp or duration is part of normative report content.

## Case Results

Case-level results are:

- `pass`
- `fail`
- `unsupported`
- `invalidAdapterResponse`
- `timeout`
- `resourceFailure`

The runner preserves `unknown`, `contested`, `prohibited` and `requiresHumanReview` as observable expected outcomes.

## Resource Limits

The manifest defines:

- adapter timeout in seconds
- maximum stdout bytes

If an adapter exceeds either limit, the runner reports `timeout` or `resourceFailure`.

## Independence Boundary

`selfConformance` means the reference or implementation tests itself through the public adapter. `independentConformance` is true only when the implementation is external, explicitly attests separate implementation, and passes the frozen suite in independent evidence mode.

The bundled reference and demonstration adapters do not claim independent conformance.

## Non-Goals

The runner does not implement:

- JSON/CSV compilation
- review UI
- SDK packaging
- hosted conformance service
- registry service
- MCP adapter
- extension certification
- legal permission evaluation
- external multi-AI proof
