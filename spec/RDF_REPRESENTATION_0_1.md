# ADUC RDF Representation 0.1

- Status: Gate 6 preparation candidate
- Date: 2026-07-13
- Issue: #17
- Context: `urn:aduc:context:0.1`
- Local context document: `context/aduc-context-0.1.jsonld`

## 1. Purpose

This document defines the RDF meaning of the ADUC JSON mapping-profile serialization and the deterministic normalization process used by conformance tests.

The JSON Schema remains responsible for structural validation. JSON-LD expansion is responsible for semantic graph construction. Neither mechanism proves that a mapping is correct or authoritative.

## 2. Context resolution

Official v0.1 profiles use:

```json
{
  "@context": "urn:aduc:context:0.1"
}
```

During conformance processing, this identifier must resolve to the repository-local document:

```text
context/aduc-context-0.1.jsonld
```

The reference implementation performs no network fetch. An unknown context identifier is an explicit processing error.

## 3. Namespaces

| Prefix | IRI |
|---|---|
| `aduc` | `urn:aduc:term:` |
| `dcterms` | `http://purl.org/dc/terms/` |
| `prov` | `http://www.w3.org/ns/prov#` |
| `rdfs` | `http://www.w3.org/2000/01/rdf-schema#` |
| `xsd` | `http://www.w3.org/2001/XMLSchema#` |

SKOS mapping-property IRIs remain the values already present in `mappingRelation`.

## 4. Profile mapping

Given:

```json
{
  "id": "urn:aduc:profile:example",
  "conformsTo": "urn:aduc:profile:0.1",
  "describes": "https://example.org/schema/1",
  "validFor": {
    "source": "https://example.org/schema",
    "version": "1"
  },
  "referenceScheme": "json-pointer",
  "issuedAt": "2026-07-13T12:00:00Z",
  "assertions": []
}
```

JSON-LD expansion represents:

- profile `id` as the profile node IRI;
- `conformsTo` as `dcterms:conformsTo` with an IRI object;
- `describes` as `aduc:describes` with an IRI object;
- `validFor` as `aduc:validFor` pointing to a source-binding node;
- source binding `source` as `aduc:source` with an IRI object;
- source binding `version` as `dcterms:hasVersion` with a literal object;
- source binding `digest` as `aduc:digest` with a literal object;
- `referenceScheme` as `aduc:referenceScheme` with an ADUC vocabulary IRI;
- `issuedAt` as `dcterms:issued` with `xsd:dateTime` datatype;
- `assertions` as `aduc:assertion` links.

## 5. Assertion mapping

| JSON term | RDF representation |
|---|---|
| assertion `id` | assertion node IRI |
| `localReference` | `aduc:localReference` literal |
| `semanticTarget` | `aduc:semanticTarget` IRI |
| `mappingRelation` | `aduc:mappingRelation` IRI value |
| `status` | `aduc:status` ADUC vocabulary IRI |
| `confidence` | `aduc:confidence` `xsd:decimal` literal |
| `confidenceMethod` | `aduc:confidenceMethod` IRI |
| `assertedBy` | `prov:wasAttributedTo` IRI |
| `assertedAt` | `prov:generatedAtTime` `xsd:dateTime` literal |
| `evidence` | `prov:wasDerivedFrom` IRI links |
| `supersedes` | `prov:wasRevisionOf` IRI link |
| `note` | `rdfs:comment` literal |

## 6. Status values

JSON values expand as:

```text
inferred  → urn:aduc:term:inferred
reviewed  → urn:aduc:term:reviewed
canonical → urn:aduc:term:canonical
contested → urn:aduc:term:contested
```

The RDF representation preserves authority state; it does not infer transitions.

## 7. Mapping relations

The JSON value:

```text
http://www.w3.org/2004/02/skos/core#exactMatch
```

is represented as the IRI object of `aduc:mappingRelation`.

ADUC does not directly assert:

```text
local field skos:exactMatch semantic target
```

because a v0.1 local field is a deterministic source reference string, not necessarily an RDF concept node. This avoids asserting a SKOS relation with inappropriate subjects.

## 8. Provenance

The assertion node is treated as the provenance entity being attributed, generated and derived.

The following terms are reused:

- `prov:wasAttributedTo` for the asserting human, model or organization;
- `prov:generatedAtTime` for assertion time;
- `prov:wasDerivedFrom` for evidence references;
- `prov:wasRevisionOf` for immutable replacement history.

A complete PROV activity graph may be supplied externally. The profile does not require one.

## 9. Confidence

`confidence` expands as an `xsd:decimal` literal.

Its meaning remains strictly scoped to the semantic mapping assertion. RDF consumers must not reinterpret it as:

- data quality;
- factual probability;
- prediction confidence;
- source accuracy;
- publisher authority.

`confidenceMethod` identifies the scoring or calibration method as an IRI.

## 10. Deterministic normalization

The reference process is:

```text
ADUC JSON profile
→ resolve official local context
→ JSON-LD expansion
→ RDF dataset conversion
→ URDNA2015 canonicalization
→ application/n-quads
```

The canonical N-Quads output is used to test graph equivalence and ordering independence.

The normalized output must be byte-for-byte stable for semantically equivalent official fixtures processed with the same context and library behavior.

## 11. Round-trip test

A conforming round-trip test performs:

1. expand the original profile;
2. normalize it to N-Quads;
3. compact the expanded graph with the official context;
4. normalize the compacted document again;
5. compare both N-Quads byte-for-byte.

The compacted JSON does not need to preserve the original property order or formatting. It must preserve the RDF graph.

## 12. Required graph evidence

For every official profile, tests must verify:

- profile node is present;
- every assertion node identifier is present;
- every semantic target is present;
- every mapping relation is present;
- status is represented as an ADUC term IRI;
- source binding is present;
- asserting agent and assertion timestamp are present;
- evidence and replacement links are preserved when supplied;
- confidence and confidence method are preserved when supplied.

## 13. Context integrity

Conformance mode accepts only:

```text
urn:aduc:context:0.1
```

for official v0.1 fixtures.

Unknown or remote context identifiers produce an explicit error. A future implementation may support approved remote contexts, but conformance tests must continue to pin the exact context document.

## 14. Schema relationship

The JSON Schema and JSON-LD context describe different aspects of the same profile:

- JSON Schema validates required properties, datatypes and conditional rules;
- JSON-LD supplies RDF identifiers and graph meaning.

A profile must pass both. Passing only JSON-LD expansion does not establish schema conformance.

## 15. Explicit limitations

The RDF representation does not:

- verify source authority;
- prove evidence authenticity;
- sign or timestamp the graph;
- resolve semantic-target equivalence;
- enforce policies;
- define units, time alignment or entity identity;
- provide an ontology of domain concepts;
- publish a globally dereferenceable namespace during the experimental phase.

## 16. Migration from placeholder context

All official profiles and fixture cases must replace:

```text
https://example.org/aduc/context/0.1
```

with:

```text
urn:aduc:context:0.1
```

A profile retaining the placeholder may remain JSON-Schema-valid but is not an official ADUC RDF conformance fixture.

## 17. Completion criterion

JSON-LD/RDF interoperability passes when every official published profile:

- passes JSON Schema validation;
- passes semantic validation;
- expands using the pinned local context;
- contains the required graph evidence;
- round-trips to identical normalized N-Quads;
- produces identical normalized output regardless of assertion ordering.
