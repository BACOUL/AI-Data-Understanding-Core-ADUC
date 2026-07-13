# ADR-0006 — Source Description and Immutable Source Binding

- Status: accepted
- Date: 2026-07-13
- Issue: #27
- Decision owners: ADUC maintainers

## Context

An ADUC assertion is unsafe if consumers cannot determine exactly which source, schema version, operation, record shape, or field it addresses.

A location alone is insufficient because URLs and files may change. A human-readable version string alone is also insufficient because it may be reused, omitted, or interpreted differently. At the same time, ADUC must not duplicate the structural models already defined by Croissant, JSON Schema, OpenAPI, or DCAT.

The Core therefore needs a small binding layer that connects ADUC assertions to established source descriptions and verifies that the referenced material has not changed.

## Decision

### 1. Separate resource content from structural description

ADUC represents two independently verifiable subjects:

1. **resource content** — the actual JSON, CSV, document, response snapshot, or other bytes;
2. **source description** — the Croissant, JSON Schema, OpenAPI, DCAT, or custom versioned description used to interpret the resource.

A contract declares one binding mode:

```text
content
description
content-and-description
```

- `content` applies only to exact resource bytes;
- `description` applies to instances governed by one exact structural description and selected scope;
- `content-and-description` verifies both.

### 2. Require cryptographic binding in v0.1

For v0.1, every selected content or description subject must include SHA-256 evidence unless it is identified by a recognized content-addressed identifier whose digest can be verified locally.

A mutable URL, filename, version label, `$id`, `@id`, `$self`, or catalog IRI is identity information but not sufficient integrity evidence by itself.

The binding record contains:

```json
{
  "algorithm": "sha-256",
  "value": "lowercase hexadecimal digest",
  "scope": "raw-bytes"
}
```

For an embedded JSON description, `scope` is `jcs` and the digest is calculated from RFC 8785 JSON Canonicalization Scheme output.

### 3. Linked and embedded descriptions are both allowed

A description may be:

- **linked**, with a path or URI plus a digest of the retrieved bytes;
- **embedded**, as a JSON object plus an RFC 8785 digest;
- **cached**, where a linked description is stored locally and verified against the declared digest.

An unavailable linked description may be retained for audit, but automatic application is blocked unless a verified cache is available.

### 4. Reuse description profiles

Supported description kinds for the v0.1 design are:

| Kind | ADUC reuses | ADUC does not copy |
|---|---|---|
| `croissant` | dataset, distribution, RecordSet, Field `@id`, extraction and checksum metadata | files, record sets, extraction rules, joins, field data types |
| `json-schema` | `$id`, `$schema`, schema resources and JSON Pointer locations | types, properties, constraints, validation semantics |
| `openapi` | OpenAPI version, entry document identity, operation references, response/schema locations | paths, parameters, operations, response models, security schemes |
| `dcat` | dataset/distribution IRIs, versions, version relationships and checksums | catalog records, distributions, services and catalog semantics |
| `custom` | an absolute profile identifier, explicit version, resolver rules and digest | undocumented private structure |

DCAT identifies catalog resources and distributions. It does not provide field-level identity by itself, so field mappings require an additional description profile.

### 5. Local references are profile-aware

The v0.1 design recognizes:

- `json-pointer` — RFC 6901 pointer against a declared JSON instance or description document;
- `croissant-field-id` — resolved JSON-LD IRI of a Croissant `Field`;
- `csv-header` — exact decoded header value under a fixed CSV dialect;
- `openapi-operation-ref` — URI reference resolving to an OpenAPI Operation Object;
- `openapi-schema-pointer` — an operation/response/media-type scope plus JSON Pointer into its schema;
- `dcat-resource-iri` — resource-level reference only;
- `custom-iri` — allowed only when the custom profile defines deterministic resolution.

Every local reference records its scheme and base. Consumers must not guess either.

### 6. CSV field identity requires a fixed dialect

A reusable `csv-header` reference requires:

```text
encoding
delimiter
quote character
header row
exact code-point comparison
unique headers
```

Header reordering does not invalidate a header reference when headers remain unique and exact. Renaming a header invalidates the reference. Duplicate headers block deterministic resolution.

### 7. JSON reference behavior

JSON Pointer resolution follows RFC 6901. No Unicode normalization is applied to member names. A failed pointer is an error.

For description-bound reusable mappings, array-index pointers are prohibited as field identifiers unless the referenced description explicitly declares positional tuple stability. Object-property reordering does not affect a JSON Pointer; property renaming does.

### 8. OpenAPI reference behavior

An OpenAPI description is bound by its exact document digest and declared OpenAPI version. `$self`, when present, supplies document identity; `info.version` is retained as version information but is not integrity evidence.

`operationRef`-style URI references are preferred for multi-document descriptions. `operationId` may be recorded as an annotation but must not replace an unambiguous bound reference.

### 9. Croissant reference behavior

ADUC references the Croissant description and its versioned `conformsTo` value. Field references resolve through JSON-LD `@id` values. Croissant resource checksums may be reused as resource integrity evidence when the algorithm, digest, and exact referenced `FileObject` are unambiguous.

### 10. DCAT reference behavior

ADUC may reuse DCAT resource and distribution IRIs, `dcat:version`, version relationships, and SPDX checksum values. A DCAT version indicator without a checksum or immutable content-addressed identifier does not satisfy the v0.1 integrity requirement.

### 11. Structural ownership is singular

An ADUC Core contract may summarize a description kind and selected scope, but it must not copy structural definitions in a way that creates a second authority.

If copied structure conflicts with the bound external description, the external description remains authoritative and automatic use is blocked with a conflict error.

### 12. Stale detection is mandatory

Before automatic use, a consumer verifies:

1. selected files or embedded objects exist;
2. digest algorithms and values are supported;
3. current digests match the contract;
4. declared description identity and version match parsed content;
5. every local reference resolves under the declared scheme and base;
6. no conflicting copied structure is present.

Any mismatch blocks automatic application. Consumers do not silently "update" the contract to the new source.

### 13. Offline behavior

Offline processing is permitted when all required bytes are local or cached and their digests match.

If a required remote description is unavailable and no verified cache exists, the result is `unavailable`, not `valid`. The contract remains auditable but cannot drive automatic semantic mapping.

### 14. Migration from the mapping profile

Legacy fields migrate as follows:

| Legacy field | Full-Core destination |
|---|---|
| `describes` | `sourceBinding.description.identifier` or `resource.identifier`, depending on what it identified |
| `validFor.source` | `sourceBinding.resource.identifier` |
| `validFor.version` | `sourceBinding.resource.version` or description version |
| `validFor.sha256` | corresponding SHA-256 binding |
| `referenceScheme` | default local-reference scheme |
| assertion `localReference` | structured local reference with explicit scheme and base |

A legacy profile without enough information to distinguish resource identity from description identity is marked `legacy-unverified`. Migration tooling must request evidence rather than guess.

## Reference error families

```text
ADUC-BIND-001  resource digest mismatch
ADUC-BIND-002  description digest mismatch
ADUC-BIND-003  required binding evidence missing
ADUC-BIND-004  description identity or version mismatch
ADUC-BIND-005  required source unavailable without verified cache
ADUC-REF-001   local reference does not resolve
ADUC-REF-002   local-reference scheme or base is missing
ADUC-REF-003   duplicate or ambiguous CSV header
ADUC-REF-004   CSV dialect is incomplete
ADUC-DESC-001  copied structure conflicts with authoritative description
ADUC-DESC-002  unsupported or unversioned custom description profile
```

## Consequences

### Positive

- contracts cannot be silently reused on changed data or schemas;
- existing structural standards remain authoritative;
- JSON and CSV field references become deterministic;
- offline verification is possible;
- future inference benchmarks can prove exactly which source and documentation were used.

### Costs

- publishers or gateways must retain exact descriptor bytes or canonical embedded objects;
- mutable and live sources require description-level binding and later live-data rules;
- legacy profiles may require manual migration;
- YAML and non-JSON embedding need explicit byte-level handling rather than implicit reserialization.

## Rejected alternatives

### URL-only binding

Rejected because content may change without the contract changing.

### Version-only binding

Rejected because version labels do not prove which bytes were used.

### Copying every source structure into ADUC

Rejected because it creates conflicting authorities and duplicates established standards.

### Inferring a reference scheme from syntax

Rejected because the same string may be a JSON Pointer, URI fragment, header, field ID, or private path.

### Editing a stale contract in place

Rejected because it destroys audit history and may silently change semantic meaning.

## References

- Croissant Format Specification 1.1: https://docs.mlcommons.org/croissant/docs/croissant-spec-1.1.html
- JSON Schema Draft 2020-12 Core: https://json-schema.org/draft/2020-12/json-schema-core
- OpenAPI Specification 3.2.0: https://spec.openapis.org/oas/v3.2.0.html
- DCAT Version 3: https://www.w3.org/TR/vocab-dcat-3/
- RFC 6901 JSON Pointer: https://www.rfc-editor.org/rfc/rfc6901.html
- RFC 8785 JSON Canonicalization Scheme: https://www.rfc-editor.org/rfc/rfc8785.html

## Follow-up

After acceptance:

1. define units and conversion binding;
2. define temporal semantics;
3. define entity identity;
4. use these decisions to design the first full-Core schema family.
