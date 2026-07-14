# ADUC Core Comparison Report 0.1

- Status: implemented reference report
- Producer: `tools/aduc_core.py compare`

## Command

```text
python tools/aduc_core.py compare old.json new.json
python tools/aduc_core.py compare old.json new.json --format json
```

The comparator validates both inputs first. If either input is not JSON-Schema-valid, the report is `notComparable`. If an input is schema-valid but has dangerous architecture diagnostics, comparison is also `notComparable` because identifier-based indexing would be unsafe. Dangerous diagnostics include duplicate identifiers, unresolved references, ownership or binding violations, namespace conflicts and unsupported required extensions. Other profile diagnostics remain visible in endpoint metadata and may produce contested, deprecated, prohibited or review-required assessments.

## JSON Report

```json
{
  "reportVersion": "0.1.0",
  "comparable": true,
  "overall": "potentiallyIncompatible",
  "overallAssessment": "unknown",
  "left": {
    "contractId": "urn:example:contract:1",
    "valid": true,
    "outcome": "valid"
  },
  "right": {
    "contractId": "urn:example:contract:2",
    "valid": true,
    "outcome": "valid"
  },
  "summary": {
    "unchanged": 0,
    "added": 0,
    "removed": 0,
    "modified": 0,
    "compatible": 0,
    "potentiallyIncompatible": 1,
    "incompatible": 0,
    "requiresHumanReview": 0,
    "notComparable": 0,
    "humanReview": 0,
    "assessments": {
      "equivalent": 0,
      "convertible": 0,
      "compatible": 0,
      "incompatible": 0,
      "unknown": 1,
      "contested": 0,
      "deprecated": 0,
      "prohibited": 0,
      "requiresHumanReview": 0
    }
  },
  "changes": []
}
```

`overall` is one of:

```text
unchanged
compatible
modified
potentiallyIncompatible
incompatible
requiresHumanReview
notComparable
```

## Change Object

```json
{
  "code": "ADUC-COMPARE-STRUCTURE-REQUIRED-001",
  "classification": "incompatible",
  "changeType": "modified",
  "assessment": "incompatible",
  "module": "structure",
  "dimension": "structure",
  "objectId": "urn:example:field:flow",
  "path": "$.structure.records[0].fields[1].required",
  "message": "A previously optional field is now required.",
  "before": false,
  "after": true
}
```

Addressable arrays are indexed by Core object identifiers, not by list position. The report does not duplicate full contracts.

`classification` is the compatibility-risk bucket kept for stable comparison summaries. `changeType` records the mechanical diff shape: `unchanged`, `added`, `removed` or `modified`. `assessment` records the normative semantic result for the dimension:

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

A unit change is `convertible` only when ADR-0007 confirms a verified local registry, matching dimension and quantity kind, compatible roles, supported conversion, available rounding policy and preserved uncertainty. Otherwise the assessment remains `unknown`, `incompatible` or `requiresHumanReview`.

## Official Fixtures

The official scenario suite is `examples/core/comparison/cases.json`. It contains 24 deterministic cases covering identical contracts with reordered JSON, structure changes, semantic changes, unit conversion, authority promotion, identity, context, provenance, uncertainty, relations, policy, extensions, dangerous architecture diagnostics and invalid left/right inputs.
