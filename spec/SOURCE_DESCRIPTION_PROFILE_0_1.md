# ADUC Source Description Profile 0.1

- Status: working draft
- Date: 2026-07-13
- Decision: ADR-0006
- Scope: source identity, description identity, cryptographic binding, and deterministic local references

## 1. Purpose

This profile defines how an ADUC contract identifies the exact resource and structural description to which its assertions apply.

It does not redefine dataset structure, API operations, JSON Schema validation, catalog metadata, units, time, entity identity, provenance, policy, or semantic concepts.

The profile answers five questions:

1. Which resource is described?
2. Which exact description or schema governs its structure?
3. Which bytes or canonical object were used?
4. How does a local field reference resolve?
5. What must a consumer do when the source has changed or is unavailable?

## 2. Normative language

The terms MUST, MUST NOT, REQUIRED, SHOULD, SHOULD NOT, and MAY are to be interpreted as normative requirements for this candidate profile.

## 3. Source-binding object

Candidate shape:

```json
{
  "bindingMode": "content-and-description",
  "resource": {},
  "description": {},
  "localReferenceDefaults": {}
}
```

### 3.1 `bindingMode`

Allowed values:

| Value | Meaning |
|---|---|
| `content` | Assertions apply only to exact resource bytes. |
| `description` | Assertions apply to instances governed by one exact description and selected scope. |
| `content-and-description` | Both resource bytes and structural description are verified. |

Required subjects:

| Binding mode | Resource digest | Description digest |
|---|---:|---:|
| `content` | required | optional |
| `description` | optional | required |
| `content-and-description` | required | required |

A location or version label without verifiable integrity evidence MUST NOT satisfy these requirements.

## 4. Resource subject

Candidate properties:

| Property | Requirement | Meaning |
|---|---|---|
| `identifier` | required | Absolute IRI or URN identifying the resource or source family. |
| `location` | optional | URI reference or repository-relative path used to retrieve bytes. |
| `mediaType` | required | Media type of the selected resource representation. |
| `version` | optional | Publisher version or snapshot label. |
| `digest` | conditional | Cryptographic binding for exact content bytes. |
| `role` | optional | `data`, `response-snapshot`, `document`, or other registered role. |

Example:

```json
{
  "identifier": "urn:example:river-observation:R42:2026-07-13T12:00:00Z",
  "location": "./river-data.json",
  "mediaType": "application/json",
  "digest": {
    "algorithm": "sha-256",
    "value": "521c901337e1fc50e31a00e09919a1932e5ce770de0fd93c554ac0223024f7a6",
    "scope": "raw-bytes"
  }
}
```

## 5. Description subject

Candidate properties:

| Property | Requirement | Meaning |
|---|---|---|
| `kind` | required | `croissant`, `json-schema`, `openapi`, `dcat`, or `custom`. |
| `identifier` | required | Canonical or publisher identifier of the exact description resource. |
| `location` | linked form | Location of the description bytes. |
| `embedded` | embedded form | Embedded JSON description object. |
| `mediaType` | required | Media type of the description representation. |
| `conformsTo` | required | Versioned specification or custom profile identifier. |
| `version` | recommended | Description or governed interface version. |
| `digest` | required | Digest of linked raw bytes or embedded canonical JSON. |
| `scope` | optional | Selected RecordSet, schema resource, operation, response, distribution, or custom scope. |

Exactly one of `location` and `embedded` MUST be present in v0.1.

### 5.1 Linked description digest

```json
{
  "algorithm": "sha-256",
  "value": "501e7c9a5b0f1b4cfd27c734e14ed81f5038a98b7a029a25bc0d269fd1528aff",
  "scope": "raw-bytes"
}
```

The digest is calculated over the exact retrieved or cached bytes.

### 5.2 Embedded JSON description digest

```json
{
  "algorithm": "sha-256",
  "value": "6f1eff80295d7bd66a83dcfe221045c39b0283b792f627e71fab108315730956",
  "scope": "jcs"
}
```

The digest is calculated over RFC 8785 JSON Canonicalization Scheme output.

An implementation MUST NOT hash an implementation-specific pretty-printed serialization and label it `jcs`.

## 6. Digest object

Candidate properties:

| Property | v0.1 rule |
|---|---|
| `algorithm` | MUST equal `sha-256`. |
| `value` | MUST be 64 lowercase hexadecimal characters. |
| `scope` | MUST equal `raw-bytes` or `jcs`. |

`raw-bytes` is valid for linked files and source content. `jcs` is valid only for parsed embedded JSON values.

Future versions may register additional algorithms and canonicalization profiles through explicit identifiers.

## 7. Description-kind rules

### 7.1 Croissant

Required interpretation:

- `conformsTo` identifies the versioned Croissant specification;
- `identifier` identifies the Croissant dataset description;
- selected fields use resolved JSON-LD `@id` values;
- Croissant `FileObject.sha256` may satisfy resource integrity only when it unambiguously applies to the selected file;
- ADUC does not copy `distribution`, `RecordSet`, `Field.source`, extraction, transformation, join, or data-type rules.

A Croissant description version and description digest are distinct. Both SHOULD be retained.

### 7.2 JSON Schema

Required interpretation:

- `conformsTo` identifies the JSON Schema dialect, normally Draft 2020-12 for v0.1 examples;
- `identifier` equals the schema resource canonical `$id` when present;
- a selected embedded schema resource retains its own `$id`;
- local schema references use RFC 6901 JSON Pointer or resolved schema-resource URIs;
- ADUC does not copy `type`, `properties`, `required`, applicators, formats, or validation constraints.

A `$id` is identity, not proof that the schema bytes are unchanged.

### 7.3 OpenAPI

Required interpretation:

- `conformsTo` identifies the OpenAPI Specification version;
- `identifier` uses `$self` when present, otherwise an immutable assigned identifier;
- `version` retains `info.version`;
- the description digest binds the complete entry document or declared multi-document package manifest;
- operations use `openapi-operation-ref` URI references;
- `operationId` may be retained as an annotation but MUST NOT replace a resolvable reference when ambiguity is possible;
- ADUC does not copy paths, parameters, response definitions, schemas, security, or callbacks.

### 7.4 DCAT

Required interpretation:

- `identifier` selects a dataset, distribution, data service, or catalog resource IRI;
- `version` may reuse `dcat:version`;
- integrity may reuse an unambiguous SPDX checksum record;
- field-level references require Croissant, JSON Schema, OpenAPI, or another field-capable description;
- ADUC does not copy catalog, distribution, or service records.

### 7.5 Custom profile

A custom description is allowed only when:

- `conformsTo` is an absolute versioned IRI or URN;
- deterministic parsing and reference-resolution rules are public or included in a verified local package;
- `version` is present;
- a digest is present;
- the contract does not claim cross-implementation portability until at least two consumers implement that profile.

An undocumented private path syntax is not a conforming custom profile.

## 8. Local reference object

Candidate shape:

```json
{
  "scheme": "json-pointer",
  "base": "description",
  "value": "/properties/flow"
}
```

Properties:

| Property | Requirement | Meaning |
|---|---|---|
| `scheme` | required | Registered reference-resolution scheme. |
| `base` | required | `resource`, `description`, or selected named scope. |
| `value` | required | Reference value interpreted only under the declared scheme. |
| `expectedKind` | optional | Expected target kind, such as field, operation, schema, or distribution. |

Consumers MUST NOT infer a scheme from the string syntax.

## 9. Reference schemes

### 9.1 `json-pointer`

- resolution follows RFC 6901;
- the pointer begins at the declared base JSON value;
- `~1` decodes to `/` and `~0` decodes to `~` in that order;
- member names compare by exact Unicode code points without normalization;
- resolution failure blocks automatic use;
- array-index field identity is prohibited for reusable description bindings unless tuple stability is explicitly declared.

### 9.2 `croissant-field-id`

- `value` is an absolute resolved IRI;
- the IRI MUST identify exactly one Croissant Field in the verified description;
- field-array order is irrelevant;
- a publisher changing the Field `@id` creates a new field identity.

### 9.3 `csv-header`

A CSV description MUST declare:

```json
{
  "encoding": "utf-8",
  "delimiter": ",",
  "quoteChar": "\"",
  "headerRow": 1,
  "headerPolicy": "exact-codepoints",
  "uniqueHeaders": true
}
```

Rules:

- bytes are decoded using the declared encoding;
- the declared CSV dialect is used to parse the header row;
- headers MUST be unique;
- `value` compares exactly to the decoded header value;
- reordering preserves identity;
- renaming, normalization, or duplicate introduction invalidates the reference.

### 9.4 `openapi-operation-ref`

- `value` is a URI reference resolving to one Operation Object;
- relative references resolve against the verified OpenAPI entry document identity or location;
- multi-document references MUST retain their document part;
- `operationId` alone is insufficient when the resolver cannot prove uniqueness in the bound description.

### 9.5 `openapi-schema-pointer`

The reference additionally declares:

- operation reference;
- response status or request scope;
- media type;
- JSON Pointer into the selected Schema Object.

All enclosing selections must resolve before the pointer is evaluated.

### 9.6 `dcat-resource-iri`

- selects one verified DCAT resource;
- valid for dataset/distribution/service-level assertions;
- MUST NOT be used as field-level identity.

### 9.7 `custom-iri`

- valid only under a verified custom description profile;
- the profile supplies deterministic resolution and target-kind rules.

## 10. CSV table description profile

Until a suitable external CSV structural description is selected, the reference implementation may use:

```text
urn:aduc:source-description:csv-table:0.1
```

This temporary profile contains only:

- description identifier;
- version;
- `text/csv` media type;
- complete CSV dialect;
- ordered header inventory.

It does not define semantic concepts, units, provenance, uncertainty, or policy.

The profile is replaceable by a future established standard without changing the Core binding principles.

## 11. Consumer verification algorithm

A conforming consumer performs:

```text
1. validate bindingMode
2. locate required resource and description subjects
3. verify supported digest algorithm and syntax
4. load local/cached bytes or embedded JSON
5. recompute required digests
6. parse description under its declared kind and conformsTo value
7. verify parsed identifier and version
8. resolve every local reference under its declared scheme and base
9. detect copied-structure conflict
10. return verified, unavailable, or blocked result with stable errors
```

Consumers MUST NOT fetch an untrusted new version to repair a mismatch automatically.

## 12. Stale and unavailable results

### `verified`

All required bytes, digests, identifiers, versions, and local references match.

### `unavailable`

A required linked subject cannot be loaded and no verified cache exists.

### `blocked`

A loaded subject differs, a reference fails, the dialect is ambiguous, or copied structure conflicts.

`unavailable` and `blocked` MUST NOT drive automatic semantic substitution.

## 13. Structural conflict rule

An ADUC contract MAY carry a non-normative human summary, but it MUST NOT contain a second normative source structure.

If a contract contains copied structural claims and one conflicts with the verified external description:

```text
ADUC-DESC-001
```

is emitted and the external description remains authoritative.

## 14. Reference error codes

| Code | Meaning |
|---|---|
| `ADUC-BIND-001` | Resource digest mismatch. |
| `ADUC-BIND-002` | Description digest mismatch. |
| `ADUC-BIND-003` | Required binding evidence missing or malformed. |
| `ADUC-BIND-004` | Parsed description identity or version mismatch. |
| `ADUC-BIND-005` | Required source unavailable without verified cache. |
| `ADUC-REF-001` | Local reference failed to resolve. |
| `ADUC-REF-002` | Reference scheme or base missing/unsupported. |
| `ADUC-REF-003` | CSV header is duplicate or ambiguous. |
| `ADUC-REF-004` | CSV dialect is incomplete or unsupported. |
| `ADUC-DESC-001` | Copied structure conflicts with authoritative description. |
| `ADUC-DESC-002` | Custom description profile is unversioned or unresolved. |

## 15. Migration rules

### Directly migratable legacy profile

A legacy profile can migrate automatically only when its fields unambiguously identify:

- the resource or description subject;
- exact version or SHA-256 digest;
- local-reference scheme;
- reference base.

### Migration mapping

```text
describes             -> description.identifier or resource.identifier
validFor.source       -> resource.identifier
validFor.version      -> resource.version or description.version
validFor.sha256       -> selected digest object
referenceScheme       -> localReferenceDefaults.scheme
localReference string -> localReference.value
```

### `legacy-unverified`

Migration returns `legacy-unverified` when:

- `describes` could mean either the source or its schema;
- only a mutable URL exists;
- version has no digest or immutable identity;
- local reference base is unknown;
- CSV dialect is absent;
- a legacy `contested` assertion also lacks recoverable authority information.

No migration tool may guess these values.

## 16. Reference examples

```text
examples/source-description/json/
examples/source-description/csv/
examples/source-description/reference-cases.json
examples/source-description/invalid-cases.json
```

The reference evaluator verifies exact file bytes, description identity, JSON Pointer resolution, CSV dialect and header resolution, and required failures.

## 17. Conformance limits

This profile does not prove:

- that a remote publisher controls an identifier;
- that source data values are factually correct;
- that an API response actually conforms to its OpenAPI schema;
- that a JSON instance validates against JSON Schema;
- that a Croissant extraction produces the claimed records;
- that a policy permits a use;
- that two entity identifiers denote the same object.

Those checks belong to authority verification, validation tooling, provenance, policy, or later Core blocks.

## 18. References

- Croissant 1.1: https://docs.mlcommons.org/croissant/docs/croissant-spec-1.1.html
- JSON Schema Core 2020-12: https://json-schema.org/draft/2020-12/json-schema-core
- OpenAPI 3.2.0: https://spec.openapis.org/oas/v3.2.0.html
- DCAT 3: https://www.w3.org/TR/vocab-dcat-3/
- RFC 6901: https://www.rfc-editor.org/rfc/rfc6901.html
- RFC 8785: https://www.rfc-editor.org/rfc/rfc8785.html
