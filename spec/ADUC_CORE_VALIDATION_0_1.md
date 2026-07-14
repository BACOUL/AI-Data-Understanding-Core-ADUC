# ADUC Core Validation Report 0.1

- Status: implemented reference report
- Producer: `tools/aduc_core.py validate`

## Command

```text
python tools/aduc_core.py validate contract.json
python tools/aduc_core.py validate contract.json --format json
python tools/aduc_core.py validate contract.json --schema-only
python tools/aduc_core.py validate contract.json --no-profile-evaluation
```

`--schema-only` runs the Draft 2020-12 schema family without the ADR-0014 architecture checker or profile evaluation. `--no-profile-evaluation` keeps schema and architecture checks but skips the additional full-Core profile pass.

## JSON Report

```json
{
  "reportVersion": "0.1.0",
  "valid": false,
  "outcome": "blocked",
  "contractId": "urn:example:contract:1",
  "coreVersion": "0.1.0-alpha.0",
  "summary": {
    "errors": 1,
    "warnings": 0,
    "humanReview": 0
  },
  "pipeline": {
    "jsonLoaded": true,
    "schemaValid": true,
    "architectureValid": false,
    "profileEvaluation": true
  },
  "modules": {
    "aduc": {"status": "valid"},
    "resource": {"status": "valid"},
    "structure": {"status": "valid"}
  },
  "profileEvaluations": [],
  "diagnostics": []
}
```

The global `outcome` is one of `valid`, `validWithWarnings`, `requiresHumanReview` or `blocked`.

Module status is one of `valid`, `validWithWarnings`, `requiresHumanReview`, `invalid` or `notDescribed`.

`profileEvaluations` records the accepted profile adapter that was considered for ADR-0005 through ADR-0013. Each item identifies the profile, evaluator, whether it was called, the status, applied rules, non-applicable rules, missing data, required operational requests and diagnostic codes. Missing registry data, absent local bytes, absent operational policy requests or absent standalone profile fields are reported as `unknown`, `notApplicable`, `indeterminate` or `requiresHumanReview`; they are not silently promoted to success.

## Diagnostic Object

```json
{
  "code": "ADUC-CORE-REF-001",
  "severity": "error",
  "category": "reference",
  "path": "$.semantics.assertions[0].subjectRef",
  "message": "Referenced Core object does not exist.",
  "module": "semantics",
  "relatedPaths": [],
  "blocking": true
}
```

The report is sorted deterministically and does not depend on JSON object member order.

Input size, node-count and depth checks are iterative and produce `ADUC-CORE-INPUT-*` diagnostics without Python tracebacks for ordinary CLI input errors.
