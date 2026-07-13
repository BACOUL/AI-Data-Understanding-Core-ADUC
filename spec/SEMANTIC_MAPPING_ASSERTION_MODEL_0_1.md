# ADUC Semantic Mapping Assertion Model 0.1

- Status: accepted Gate 1 information-model candidate
- Date: 2026-07-13
- Issue: #7
- Normative schema: not yet published
- Compatibility: profile over existing standards; not a replacement vocabulary

## 1. Purpose

This document defines the smallest candidate information model needed to make a semantic mapping portable between independent AI consumers while preserving its authority, uncertainty and evidence.

It does **not** describe a dataset, API, event, observation, provenance graph, quality model or usage policy. Those concerns remain in Croissant, JSON Schema, JSON-LD/RDF, PROV-O, DQV, ODRL and other established standards.

The model answers one bounded question:

> What minimum information must travel with a mapping from a local source field or value to an existing semantic identifier so that independent consumers can use it without silently changing its meaning or authority?

## 2. Design principles

1. **Profile, do not replace.** Source structure and dataset metadata remain external.
2. **One assertion, one target.** Ambiguity is represented by multiple assertions, not an array of hidden alternatives inside one assertion.
3. **Assertions are immutable.** Review, promotion, challenge or replacement creates a new assertion linked to the earlier one.
4. **Authority is not confidence.** A publisher-authoritative mapping is not a probability score.
5. **Mapping confidence is not data quality.** It estimates the correctness of the semantic correspondence, not the accuracy of the source value.
6. **No silent inference.** Consumers preserve the local reference, status and provenance.
7. **Absolute semantic identifiers.** Semantic targets and mapping relations are IRIs.
8. **Source-version binding.** A mapping cannot be applied safely to an unidentified or changed source schema.

## 3. Profile document

A mapping profile document groups assertions applying to one identified source description and source version.

### 3.1 Candidate document properties

| Property | Cardinality | Purpose |
|---|---:|---|
| `@context` | exactly 1 | Gives the JSON document JSON-LD meaning and binds profile terms to IRIs. |
| `id` | exactly 1 | Stable identifier for the mapping profile document. |
| `conformsTo` | exactly 1 | Identifies the ADUC profile version. |
| `describes` | exactly 1 | References the Croissant dataset, JSON Schema, or other accepted source description. |
| `validFor` | exactly 1 | Binds assertions to a source/schema version, immutable identifier or cryptographic digest. |
| `referenceScheme` | exactly 1 | Declares how `localReference` values are resolved. |
| `issuedAt` | exactly 1 | Records publication time of this profile document. |
| `assertions` | one or more | Contains semantic mapping assertions. |

### 3.2 Accepted local-reference schemes for v0.1

The first schema should support only:

- `croissant-field-id`: a Croissant `Field` identifier;
- `json-pointer`: an RFC 6901 JSON Pointer resolved against the described JSON record shape;
- `csv-header`: an exact CSV header name, permitted only when the described source fixes header identity and encoding.

A profile uses one declared default scheme. A future schema may allow an assertion-level override, but v0.1 should avoid it unless a concrete fixture proves it necessary.

### 3.3 Source-version binding

`validFor` must identify the exact source contract or schema to which mappings apply. Acceptable forms include:

- immutable Croissant metadata identifier and version;
- immutable JSON Schema `$id` and version;
- source schema digest;
- versioned source-description URI.

A mutable unversioned URL is insufficient by itself.

## 4. Semantic mapping assertion

### 4.1 Required properties

| Property | Cardinality | Requirement |
|---|---:|---|
| `id` | exactly 1 | Absolute IRI or URN identifying the immutable assertion. |
| `localReference` | exactly 1 | Deterministic reference to the local field or enumerated value. |
| `semanticTarget` | exactly 1 | Absolute IRI identifying the external concept. |
| `mappingRelation` | exactly 1 | IRI expressing the strength or direction of the semantic correspondence. |
| `status` | exactly 1 | Authority state: `inferred`, `reviewed`, `canonical`, or `contested`. |
| `assertedBy` | exactly 1 | IRI identifying the model, human, organization or source authority making this assertion. |
| `assertedAt` | exactly 1 | Date-time at which this immutable assertion was issued. |

### 4.2 Conditional and optional properties

| Property | Cardinality | Rule |
|---|---:|---|
| `confidence` | zero or one | Required for `inferred`; optional for `reviewed`; forbidden for `canonical`; range 0 to 1. |
| `confidenceMethod` | zero or one | Required whenever `confidence` is present; identifies scoring/calibration method. |
| `evidence` | zero or more | Required for `inferred` and `contested`; references documentation, samples, rules or review records. |
| `supersedes` | zero or one | Links a new immutable assertion to the assertion it replaces. |
| `note` | zero or one | Human-readable explanation; never normative and never a substitute for structured evidence. |

### 4.3 Why `mappingRelation` is required

A local field may correspond exactly to a target concept, be narrower, broader or merely close. Treating every mapping as exact creates false interoperability.

The profile should reuse mapping-relation IRIs rather than inventing opaque strings. Candidate relations include:

- `http://www.w3.org/2004/02/skos/core#exactMatch`;
- `http://www.w3.org/2004/02/skos/core#closeMatch`;
- `http://www.w3.org/2004/02/skos/core#broadMatch`;
- `http://www.w3.org/2004/02/skos/core#narrowMatch`;
- `http://www.w3.org/2004/02/skos/core#relatedMatch`.

Gate 2 must verify that their use is semantically valid for the local-term representation selected by the JSON-LD context. If not, the profile must define the smallest relation vocabulary while documenting its relationship to SKOS.

## 5. Minimal status model

### 5.1 Accepted statuses

#### `inferred`

The mapping was produced by an automated process or by a non-authoritative guess and has not been accepted by a human reviewer or source authority.

Requirements:

- `confidence` required;
- `confidenceMethod` required;
- at least one `evidence` reference required;
- consumer must not present it as authoritative.

#### `reviewed`

A human or accountable process reviewed the mapping, but the assertion is not published as the canonical meaning by the source authority.

Requirements:

- reviewer identified through `assertedBy`;
- confidence optional;
- if confidence exists, `confidenceMethod` required;
- review evidence recommended.

#### `canonical`

The organization or publisher authorized to define the source meaning publishes the mapping as authoritative for the identified source version.

Requirements:

- `assertedBy` must resolve to, or be verifiably associated with, the source authority;
- `confidence` forbidden because canonicality is an authority claim, not probability;
- consumer must still preserve source version and provenance;
- multiple incompatible canonical assertions are a conflict, not a choice opportunity.

#### `contested`

The mapping is actively challenged or unresolved after review.

Requirements:

- at least one evidence or challenge reference;
- automatic semantic substitution forbidden;
- consumer must preserve all competing assertions and expose the conflict.

### 5.2 Statuses intentionally removed

#### `unknown`

Removed from mapping assertions. If a described local field has no assertion, its mapping is unknown. Creating a targetless mapping assertion adds no semantic information.

#### `verified`

Removed because it was ambiguous between human review and publisher authority. `reviewed` and `canonical` provide the distinction needed by consumers.

#### `deprecated`

Removed from the authority state. Assertions are immutable; replacement is represented with a new assertion and `supersedes`. Historical assertions remain auditable.

## 6. Immutable lifecycle

A mapping assertion is never edited in place after publication.

### 6.1 Promotion

An inferred assertion is not changed to reviewed or canonical. A new assertion is issued:

```text
inferred assertion A
        ↓ reviewed by human
reviewed assertion B --supersedes--> A
        ↓ published by source authority
canonical assertion C --supersedes--> B
```

### 6.2 Challenge

A challenge creates a new `contested` assertion or challenge record linked through `supersedes` in the initial profile. Gate 2 may introduce a more precise `challenges` relation if fixtures show that challenge and replacement must coexist.

### 6.3 Source change

When the described source schema changes, existing assertions do not automatically apply. A new profile document with a new `validFor` value must be issued. Assertions may be copied only after revalidation.

## 7. Consumer invariants

A conforming consumer must obey the following candidate invariants.

### I1 — Preserve status

The consumer must not output a stronger authority status than the input assertion.

### I2 — Preserve source identity

The consumer must retain the `describes`, `validFor` and `localReference` values in any derived mapping result.

### I3 — No hidden mappings in conformance mode

During a conformance test, the consumer must not use provider-private mappings, memories or prompts that are not declared by the test protocol.

### I4 — Canonical authority validation

A consumer must not accept `canonical` solely because the string appears in the document. It must verify the configured authority relationship or report the assertion as unverified canonical input.

### I5 — Conflict preservation

Multiple non-equivalent canonical targets for the same local reference and source version must produce a conflict result.

### I6 — Contested mappings are non-automatic

A contested mapping must not drive silent conversion, joining or automated action.

### I7 — Confidence is scoped

`confidence` applies only to the semantic mapping assertion. It must not be interpreted as:

- source data accuracy;
- probability that a measured fact is true;
- model prediction confidence;
- data completeness;
- legal permission.

### I8 — Confidence methods matter

Consumers must not compare or threshold confidence values from different unidentified methods as if they were calibrated identically.

### I9 — Mapping relation matters

`closeMatch`, `broadMatch`, `narrowMatch` and `relatedMatch` must not be treated as `exactMatch`.

### I10 — Source-version mismatch blocks automatic application

If `validFor` does not match the source description or schema version being consumed, the mapping must be rejected or explicitly revalidated.

## 8. Deterministic selection behavior

For each local reference, a conforming consumer should process assertions in this order:

1. validate the profile and source-version binding;
2. reject malformed assertions;
3. group assertions by local reference;
4. identify incompatible canonical assertions as conflict;
5. block automatic use when an active contested assertion applies;
6. prefer a valid canonical assertion from the recognized source authority;
7. otherwise apply deployment policy to reviewed assertions;
8. otherwise apply deployment policy and recognized confidence method to inferred assertions;
9. otherwise preserve the local reference as unmapped;
10. return status, relation, evidence and provenance with the selected result.

The profile does not impose one universal risk threshold. It standardizes the inputs and required visibility so deployments can define thresholds without losing meaning.

## 9. Necessity analysis

| Candidate property | What fails if absent? | Decision |
|---|---|---|
| `@context` | Terms cannot be interpreted consistently as Linked Data. | Required at document level. |
| `id` for document | The profile cannot be versioned, signed or referenced reliably. | Required. |
| `conformsTo` | Consumers cannot select the correct processing rules. | Required. |
| `describes` | Mappings are detached from the source description. | Required. |
| `validFor` | Stale mappings may be applied to changed schemas. | Required. |
| `referenceScheme` | A local path may resolve differently across consumers. | Required. |
| `issuedAt` | Consumers cannot order or audit profile publications. | Required. |
| assertion `id` | Promotion, challenge, evidence and replacement cannot target an immutable claim. | Required. |
| `localReference` | No local field or value is identified. | Required. |
| `semanticTarget` | No external meaning is asserted. | Required. |
| `mappingRelation` | Approximate or directional mappings are silently treated as exact. | Required. |
| `status` | Inference and authority become indistinguishable. | Required. |
| `assertedBy` | Authority and accountability cannot be evaluated. | Required. |
| `assertedAt` | Assertion order and auditability are lost. | Required. |
| `confidence` | Automated mappings cannot express their assessed uncertainty. | Conditionally required for `inferred`. |
| `confidenceMethod` | Confidence numbers from different methods appear falsely comparable. | Required when confidence exists. |
| `evidence` | An inferred or contested mapping cannot be audited. | Conditionally required. |
| `supersedes` | Immutable promotion or replacement cannot be followed. | Optional but necessary when replacing. |
| `note` | No machine behavior fails; only human readability decreases. | Optional and non-normative. |

## 10. Relationship to existing standards

### Croissant

- `describes` should reference the Croissant dataset or record-set description.
- `localReference` should prefer stable Croissant `Field` identifiers when available.
- ADUC must not redefine files, record sets, extraction rules, field data types or dataset provenance.

### JSON Schema

- JSON Pointer may identify a property in a source JSON Schema or record shape.
- Gate 2 will use JSON Schema Draft 2020-12 to validate the ADUC JSON serialization.

### JSON-LD / RDF

- `@context`, `id`, `semanticTarget`, `mappingRelation`, `assertedBy`, `evidence` and `supersedes` should expand to IRIs.
- The JSON serialization must round-trip to an RDF graph without losing authority state or confidence metadata.

### SKOS

- Candidate mapping relations reuse SKOS mapping properties.
- Gate 2 must validate that source-local semantic nodes meet the expectations of those properties.

### PROV-O

A future JSON-LD context should map:

- `assertedBy` to an attribution relationship compatible with `prov:wasAttributedTo`;
- `assertedAt` or profile `issuedAt` to a generation/publication time compatible with `prov:generatedAtTime`;
- `evidence` to derivation or source relationships compatible with `prov:wasDerivedFrom`;
- the mapping assertion to a provenance entity.

The profile does not redefine agents, entities, activities or derivation graphs.

### DQV

DQV remains the vocabulary for source and dataset quality. ADUC mapping confidence is intentionally separate and must not be exported as a DQV quality score unless a specific DQV metric explicitly measures mapping quality.

### ODRL

ODRL remains the mechanism for detailed permissions, prohibitions and duties. An ADUC mapping assertion does not grant access or authorize data use.

## 11. Complete example A — inferred exact mapping

```json
{
  "@context": "https://example.org/aduc/context/0.1",
  "id": "urn:aduc:profile:river-api-v4",
  "conformsTo": "https://example.org/aduc/profile/0.1",
  "describes": "https://data.example.org/croissant/river-api-v4",
  "validFor": "urn:sha256:source-schema-v4-example",
  "referenceScheme": "croissant-field-id",
  "issuedAt": "2026-07-13T12:00:00Z",
  "assertions": [
    {
      "id": "urn:aduc:assertion:flow-water-discharge-1",
      "localReference": "records/flow",
      "semanticTarget": "https://example.org/concepts/WaterDischarge",
      "mappingRelation": "http://www.w3.org/2004/02/skos/core#exactMatch",
      "status": "inferred",
      "confidence": 0.91,
      "confidenceMethod": "urn:method:semantic-mapper-calibration-v1",
      "assertedBy": "urn:model:semantic-mapper:1.3",
      "assertedAt": "2026-07-13T11:58:00Z",
      "evidence": [
        "urn:evidence:field-unit-m3-per-second",
        "urn:evidence:river-api-documentation-flow"
      ]
    }
  ]
}
```

Expected consumer behavior:

- preserve `inferred`;
- permit use only under a deployment policy accepting the method and threshold;
- retain evidence and source-version binding;
- do not claim that the measured flow value is 91% accurate.

## 12. Complete example B — publisher-canonical narrower mapping

```json
{
  "@context": "https://example.org/aduc/context/0.1",
  "id": "urn:aduc:profile:factory-schema-12",
  "conformsTo": "https://example.org/aduc/profile/0.1",
  "describes": "https://factory.example/schema/croissant/12",
  "validFor": "https://factory.example/schema/12",
  "referenceScheme": "croissant-field-id",
  "issuedAt": "2026-07-13T13:00:00Z",
  "assertions": [
    {
      "id": "urn:aduc:assertion:motor-heat-canonical-2",
      "localReference": "measurements/motor_heat",
      "semanticTarget": "https://example.org/industry/MotorWindingTemperature",
      "mappingRelation": "http://www.w3.org/2004/02/skos/core#narrowMatch",
      "status": "canonical",
      "assertedBy": "https://factory.example/id/data-publisher",
      "assertedAt": "2026-07-13T12:55:00Z",
      "supersedes": "urn:aduc:assertion:motor-heat-reviewed-1"
    }
  ]
}
```

Expected consumer behavior:

- verify that the publisher is authorized for the described source;
- preserve `narrowMatch` rather than treating the term as exactly equivalent to generic temperature;
- reject any added confidence score as invalid for a canonical assertion.

## 13. Invalid or unsafe counterexamples

### 13.1 Hidden authority promotion

```json
{
  "localReference": "records/flow",
  "semanticTarget": "https://example.org/concepts/WaterDischarge",
  "status": "canonical",
  "assertedBy": "urn:model:mapper"
}
```

Unsafe because a model is not automatically the source authority and required identity, time, relation and source binding are absent.

### 13.2 Inferred mapping without confidence method

```json
{
  "status": "inferred",
  "confidence": 0.94
}
```

Invalid because the score has no identified calibration method and the mapping itself is incomplete.

### 13.3 Canonical mapping with confidence

```json
{
  "status": "canonical",
  "confidence": 0.99
}
```

Invalid because canonicality is an authority assertion, not a probability estimate.

### 13.4 Approximate relation treated as exact

```json
{
  "mappingRelation": "http://www.w3.org/2004/02/skos/core#closeMatch"
}
```

Unsafe if a consumer converts it internally to `exactMatch` or joins values as fully equivalent.

### 13.5 Mutable source binding

```json
{
  "describes": "https://example.org/schema/latest",
  "validFor": "https://example.org/schema/latest"
}
```

Unsafe when both URIs can change without a version or digest.

### 13.6 Targetless `unknown` assertion

```json
{
  "localReference": "records/qc",
  "status": "unknown"
}
```

Rejected because absence of a mapping already communicates that the described field is unmapped.

### 13.7 Silent in-place status mutation

```text
Yesterday: assertion A status = inferred
Today:     assertion A status = canonical
```

Rejected. A new immutable assertion must be created and linked through `supersedes`.

### 13.8 Multiple incompatible canonical targets silently selected

Two canonical assertions for the same local field map to non-equivalent targets. Selecting one based on model preference is unsafe; the consumer must report a conflict.

### 13.9 Confidence mistaken for factual truth

A mapping confidence of `0.91` must not cause the consumer to state that the source value or real-world event is true with 91% probability.

## 14. Explicit exclusions

This model does not define:

- source fields, data types or extraction rules;
- units or unit conversion vocabularies;
- entity resolution;
- data quality metrics;
- factual claims or model predictions;
- policy enforcement;
- full provenance bundles;
- signatures and trust infrastructure;
- discovery registries;
- inference algorithms;
- model prompts;
- private chain-of-thought;
- API, event, sensor or agent-memory profiles.

## 15. Open questions for Gate 2

1. Is a dedicated `challenges` relation required instead of using `supersedes` for contested mappings?
2. Should `referenceScheme` permit mixed schemes in one document?
3. Which JSON-LD context terms map cleanly to PROV-O and SKOS without invalid domain/range assumptions?
4. How is source-authority verification represented without defining a trust framework?
5. Should confidence be required for `reviewed`, or remain optional?
6. What minimum evidence representation is valid: IRI only, structured evidence object, or PROV-O entity?
7. How should equivalent semantic targets be compared when vocabularies publish `owl:sameAs`, SKOS mappings or no relation?
8. Does `issuedAt` duplicate assertion `assertedAt` in single-assertion documents enough to justify removal?

## 16. Gate 1 decision

The information-model candidate is accepted for schema design with the following narrowing:

- the profile document contains source binding and assertions;
- one assertion maps one deterministic local reference to one semantic target;
- required authority states are `inferred`, `reviewed`, `canonical` and `contested`;
- assertions are immutable;
- confidence is conditional and method-bound;
- mapping relation is explicit;
- existing standards remain authoritative for dataset structure, semantic identifiers, provenance, quality and policy.

Gate 2 must encode these rules in JSON Schema and fixtures. Any schema difficulty that reveals an unnecessary or ambiguous property must be resolved by revising this model through an ADR or specification change, not by silently weakening validation.
