# ADUC Core Error Catalogue 0.1

- Status: implemented reference catalogue
- Tool: `tools/aduc_core.py`

## Diagnostic Shape

Every validation diagnostic contains:

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

`severity` is one of `error`, `warning`, `humanReview` or `info`. `blocking` indicates whether automatic use is blocked by that diagnostic.

## Code Families

`ADUC-CORE-INPUT-*` covers local input and JSON loading failures.

`ADUC-SCHEMA-*` is emitted by the modular JSON Schema family. It covers structural failures such as missing required properties, unknown properties, enum mismatches, dependency failures, invalid formats and `oneOf`/`anyOf` violations.

`ADUC-CORE-ID-*`, `ADUC-CORE-REF-*`, `ADUC-CORE-BINDING-*`, `ADUC-CORE-DEPENDENCY-*`, `ADUC-CORE-OWNER-*`, `ADUC-CORE-EXT-*`, `ADUC-CORE-EXTERNAL-*`, `ADUC-CORE-IDENTITY-*` and `ADUC-CORE-POLICY-*` are architecture-checker diagnostics inherited from ADR-0014 and the accepted profile decisions.

`ADUC-CORE-QUAL-*`, `ADUC-CORE-CONFLICT-*`, `ADUC-CORE-LIFECYCLE-*`, `ADUC-CORE-RELATION-*`, `ADUC-CORE-PROVENANCE-*` and `ADUC-CORE-POLICY-*` are unified full-Core diagnostics for cross-module profile evaluation.

`ADUC-COMPARE-*` codes are comparison changes, not validation errors. They appear only in comparison reports.

## Comparison Change Codes

Comparison changes contain:

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

`classification` is one of:

```text
unchanged
added
removed
modified
compatible
potentiallyIncompatible
incompatible
requiresHumanReview
notComparable
```

`changeType` is one of `unchanged`, `added`, `removed` or `modified`.

`assessment` is one of:

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

`classification` describes comparison risk. `assessment` describes the normative semantic result for the dimension. The two fields must not be collapsed.

The comparator does not claim legal permission, truth, trust or authority. It reports differences, compatibility risk and review requirements.

## Stability Rule

Existing codes must not be silently reused with a different meaning. New behavior receives a new code. Reports are sorted deterministically by classification or severity, module, JSON path, code and object identifier.
