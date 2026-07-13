# Schemas

## Active candidate

`aduc-mapping-profile.schema.json` is the active Gate 2 candidate schema. It validates the portable semantic mapping profile defined in `spec/SEMANTIC_MAPPING_ASSERTION_MODEL_0_1.md`.

## Bootstrap schema

`aduc-core.schema.json` is retained only as an historical bootstrap scaffold. It is not the accepted future normative ADUC model and is no longer used by the reference validator.

## Rules not enforceable by JSON Schema alone

A later semantic validator must check at least:

- whether a `canonical` assertion was actually published by the recognized source authority;
- duplicate assertion identifiers within or across profile documents;
- whether `supersedes` targets an existing assertion and does not create a cycle;
- conflicting canonical targets for the same local reference and source version;
- whether a source URI or version is truly immutable;
- whether the selected SKOS mapping relation is semantically valid for the modeled local term;
- equivalence or incompatibility between semantic target IRIs;
- JSON-LD expansion and RDF round-trip preservation;
- signature and trust verification when introduced.

Passing the JSON Schema proves structural conformance only. It does not prove that a mapping is true, authoritative or safe for a particular operation.
