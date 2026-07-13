# ADUC Semantic Comparison Protocol 0.1

- Status: Gate 5 candidate
- Date: 2026-07-13
- Issue: #15
- Applies to: validated ADUC semantic mapping profiles 0.1

## 1. Purpose

This protocol defines how two ADUC mapping profiles are compared deterministically without hidden provider-specific mappings, network ontology resolution or name-based guessing.

It answers one bounded question:

> Which local fields in two described sources are semantically comparable according to the mapping assertions explicitly supplied by their publishers, reviewers or inference producers?

It does not compare source values, convert units, align timestamps or resolve entity identities unless those dimensions are supplied by future compatible source-description profiles.

## 2. Inputs

A comparison receives:

- profile A;
- profile B;
- the ADUC mapping-profile schema;
- optional local trusted-authority configuration used only for validation warnings.

Both profiles must pass the Gate 3 validator before comparison. A profile containing schema or semantic errors prevents comparison.

Warnings do not prevent comparison, but they are preserved in the output.

## 3. Prohibited hidden behavior

A conforming comparator must not:

- infer equivalence from similar local field names;
- use private aliases or remembered mappings;
- resolve ontology relations over the network;
- change an assertion's status;
- treat `closeMatch`, `broadMatch`, `narrowMatch` or `relatedMatch` as exact equivalence;
- guess units, time zones, entity identity or value conversions;
- select one contested mapping silently.

## 4. Comparison unit

The comparison unit is a pair of assertions sharing the exact same `semanticTarget` IRI.

One assertion from profile A is paired with one assertion from profile B when:

```text
assertionA.semanticTarget == assertionB.semanticTarget
```

No lexical normalization or ontology expansion is performed.

## 5. Result classes

### 5.1 `comparable`

A pair is `comparable` only when:

- both assertions have the same semantic target;
- both use `skos:exactMatch`;
- neither assertion is `inferred`;
- neither assertion is `contested`;
- both profiles passed validation.

`reviewed` and `canonical` statuses are preserved in the result. `Comparable` does not imply equal source values or identical units.

### 5.2 `candidate`

A pair is `candidate` when the semantic targets are identical but at least one of these conditions applies:

- one assertion is `inferred`;
- one or both mapping relations are non-exact;
- a deployment policy must review the authority state before automatic use.

The comparator must state the reason.

### 5.3 `blocked`

A pair is `blocked` when at least one applicable assertion is `contested`.

The result is preserved for audit, but automatic semantic comparison is forbidden.

### 5.4 `unmapped`

Within this protocol, `unmapped` means **unmatched across the supplied profile pair**: an assertion has no assertion in the other profile with the same semantic target.

It does not mean that the local field lacks a semantic mapping in its own profile.

### 5.5 `notEvaluated`

A dimension is `notEvaluated` when the supplied artifacts do not contain enough standardized information for the comparator to determine it.

Gate 5 always reports these dimensions explicitly:

- unit compatibility and conversion;
- temporal alignment;
- entity identity or equivalence.

They must not be guessed from field names, sample values or model memory.

## 6. Deterministic algorithm

A conforming implementation performs these steps in order:

1. Load both JSON documents.
2. Validate each with the Gate 3 validator.
3. Stop with a comparison error if either profile is invalid.
4. Sort assertions in each profile by semantic target, local reference and assertion ID.
5. Group assertions by exact semantic-target IRI.
6. For every target present in both profiles, create the Cartesian product of assertions from A and B for that target.
7. Classify each pair as `blocked`, `comparable` or `candidate` using sections 5.1–5.3.
8. Place assertions whose targets occur in only one profile into that profile's `unmapped` list.
9. Add `notEvaluated` reports for unit, time and entity dimensions.
10. Sort all output lists deterministically.
11. Serialize JSON with stable key ordering and indentation.

Repeated executions over byte-equivalent inputs must produce byte-equivalent JSON output.

## 7. Classification precedence

The classification order is mandatory:

```text
contested
  → blocked
else same target + both exact + neither inferred
  → comparable
else same target
  → candidate
else
  → unmapped across profiles
```

A canonical status does not override a contested assertion. A matching field name does not override a target mismatch.

## 8. Output model

A JSON report contains:

```json
{
  "protocol": "urn:aduc:comparison:0.1",
  "valid": true,
  "profileA": {
    "path": "a.aduc.json",
    "id": "urn:aduc:profile:a",
    "source": "https://example.org/source/a",
    "warnings": []
  },
  "profileB": {
    "path": "b.aduc.json",
    "id": "urn:aduc:profile:b",
    "source": "https://example.org/source/b",
    "warnings": []
  },
  "summary": {
    "comparable": 1,
    "candidate": 0,
    "blocked": 0,
    "unmappedA": 0,
    "unmappedB": 0
  },
  "matches": [],
  "unmapped": {
    "profileA": [],
    "profileB": []
  },
  "dimensions": {
    "unit": {"status": "notEvaluated", "reason": "..."},
    "time": {"status": "notEvaluated", "reason": "..."},
    "entity": {"status": "notEvaluated", "reason": "..."}
  }
}
```

Each match record preserves:

- classification;
- semantic target;
- assertion ID, local reference, status and relation from profile A;
- assertion ID, local reference, status and relation from profile B;
- deterministic reasons.

## 9. Exact match example

Profile A:

```json
{
  "localReference": "/properties/temp_moteur",
  "semanticTarget": "https://example.org/quantity/MotorTemperature",
  "mappingRelation": "http://www.w3.org/2004/02/skos/core#exactMatch",
  "status": "reviewed"
}
```

Profile B:

```json
{
  "localReference": "/properties/motor_temp",
  "semanticTarget": "https://example.org/quantity/MotorTemperature",
  "mappingRelation": "http://www.w3.org/2004/02/skos/core#exactMatch",
  "status": "canonical"
}
```

Result:

```text
comparable
```

The local names differ, but their published semantic target is identical.

## 10. Negative examples

### 10.1 Same name, different targets

Two local fields named `temperature` map to different semantic targets. They are not paired.

### 10.2 Same target, non-exact relation

One assertion uses `closeMatch`. The pair is a `candidate`, not `comparable`.

### 10.3 Same target, inferred status

One assertion is `inferred`. The pair is a `candidate` even when both relations are exact.

### 10.4 Contested assertion

One assertion is `contested`. The pair is `blocked`.

### 10.5 Missing unit metadata

The comparator reports unit comparison as `notEvaluated`. It must not infer Fahrenheit or Celsius from values or local names.

## 11. Validation failures

When either profile is invalid, the comparison report contains:

- `valid: false`;
- the Gate 3 validation report for each input;
- no semantic matches;
- exit code `1`.

Unreadable files or invalid JSON use exit code `2`.

## 12. Text output

Text output summarizes deterministic records, for example:

```text
COMPARISON VALID
COMPARABLE /properties/temp_moteur <-> /properties/motor_temp
NOT_EVALUATED unit
NOT_EVALUATED time
NOT_EVALUATED entity
```

JSON is the normative machine-readable report.

## 13. Explicit limitations

Gate 5 does not establish:

- unit equivalence or conversion;
- temporal equivalence;
- entity equivalence;
- ontology equivalence between different target IRIs;
- factual equality of source values;
- source-authority trust beyond local configuration;
- cross-document lifecycle resolution;
- model-provider interoperability.

These limitations are surfaced rather than hidden.

## 14. Gate 5 completion criterion

Gate 5 passes when:

- two differently named fields with the same reviewed/canonical exact target are classified as comparable;
- same-looking names with different targets are not matched;
- non-exact or inferred mappings remain candidates;
- contested mappings are blocked;
- missing unit, time and entity information is reported as not evaluated;
- repeated JSON output is byte-for-byte stable;
- all behavior is covered by CI tests.
