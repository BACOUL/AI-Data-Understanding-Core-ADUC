# ADR-0003: Experimental JSON-LD context and RDF representation

- Status: accepted
- Date: 2026-07-13
- Issue: #17

## Context

ADUC profiles require `@context`, but the existing examples reference `https://example.org/aduc/context/0.1`. That URI is a placeholder and cannot support interoperable JSON-LD processing.

The project does not currently control a dedicated public namespace domain and must not publish identifiers under a domain it does not own. Conformance tests must also run without network access.

At the same time, the profile must prove that its JSON representation preserves the semantic graph needed by independent consumers.

## Decision

### Experimental context identifier

Version 0.1 uses:

```text
urn:aduc:context:0.1
```

as the JSON-LD context identifier.

Conformance tools resolve this identifier through the repository-local document:

```text
context/aduc-context-0.1.jsonld
```

No network request is permitted for this context during conformance tests.

### Experimental term namespace

ADUC-specific terms use:

```text
urn:aduc:term:
```

Examples:

```text
urn:aduc:term:describes
urn:aduc:term:semanticTarget
urn:aduc:term:status
urn:aduc:term:reviewed
```

This avoids a false claim of ownership over an HTTP domain. A future public namespace may replace these identifiers only through an explicitly versioned migration and compatibility mapping.

### Reused vocabularies

The context reuses:

- Dublin Core Terms for conformance, version and issue time;
- PROV-O for attribution, generation time, derivation and revision;
- SKOS IRIs as values of mapping relation;
- XML Schema datatypes for decimal confidence and timestamps.

ADUC-specific predicates remain limited to concepts not directly supplied by those vocabularies, including local reference, semantic target, mapping status, confidence method, source binding and reference scheme.

### Mapping relation representation

`mappingRelation` expands to an ADUC predicate whose object is a SKOS mapping-property IRI.

The SKOS property is not directly asserted between the source field and semantic target because the v0.1 local field is represented as a deterministic string reference rather than as an RDF concept node.

This preserves the exact relation selected by the author without making invalid SKOS domain assumptions.

### Source binding

`validFor` expands to a source-binding node containing:

- source identifier;
- version and/or digest.

The binding remains an ADUC-specific structure because no reviewed existing vocabulary directly represents the exact validation contract required by the profile.

### Deterministic RDF normalization

The reference implementation uses JSON-LD expansion followed by RDF Dataset Canonicalization using URDNA2015 and N-Quads output.

The normalized N-Quads representation is the deterministic comparison artifact for conformance tests. It is not a cryptographic signature format by itself.

### Offline resolution

The reference loader resolves only the official experimental context identifier. Any other remote context fails explicitly unless a future tool is configured with an approved resolver.

This prevents accidental network dependency and context substitution during conformance tests.

## Consequences

### Positive

- Official profiles can be expanded without network access.
- ADUC terms receive stable experimental IRIs.
- Existing PROV-O and Dublin Core semantics are reused.
- N-Quads output becomes deterministic across assertion ordering.
- Context substitution and unresolved remote contexts fail visibly.

### Negative

- A URN context is not directly dereferenceable by generic JSON-LD processors.
- Generic processors need the local context document or a configured document loader.
- Public-alpha adoption will eventually benefit from a controlled HTTPS context endpoint.
- A future namespace migration may be necessary.

## Alternatives rejected

### Continue using `example.org`

Rejected because placeholder identifiers cannot become authoritative project identifiers.

### Use an unregistered `w3id.org` path

Rejected because the project has not registered or been granted that namespace.

### Use an unverified project domain

Rejected because the repository does not establish control of a dedicated domain for this standard.

### Inline the complete context in every profile

Rejected as the sole v0.1 mechanism because it increases profile size and permits unnoticed context drift. Inline contexts may be evaluated later as an optional transport mode.

### Use raw GitHub URLs as permanent semantic terms

Rejected because repository paths and branches are implementation locations, not stable semantic namespaces.

## Migration

All official fixtures and examples must replace:

```text
https://example.org/aduc/context/0.1
```

with:

```text
urn:aduc:context:0.1
```

The JSON Schema continues to accept an absolute URI string, but conformance-mode JSON-LD processing accepts only the official context identifier.

## Reversal plan

A future ADR may introduce a controlled HTTPS namespace. It must provide:

- a persistent context endpoint;
- mappings from experimental URNs;
- a versioned migration process;
- tests proving old profiles remain interpretable;
- no silent change to existing term meaning.
