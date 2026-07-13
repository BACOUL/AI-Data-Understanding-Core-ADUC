# Next Action

## Single active task

Begin Gate 6 preparation by freezing the JSON-LD and RDF representation of the ADUC mapping profile.

Create:

```text
docs/decisions/ADR-0003-json-ld-context-and-rdf-representation.md
context/aduc-context-0.1.jsonld
spec/RDF_REPRESENTATION_0_1.md
tests/jsonld/
```

## Objective

Ensure an ADUC JSON profile expands to an RDF graph and round-trips back to a deterministic normalized representation without losing:

- profile identity;
- source binding;
- local reference;
- semantic target;
- mapping relation;
- mapping status;
- confidence and confidence method;
- asserting agent and assertion time;
- evidence;
- supersedes relationships.

## Required decisions

1. stable namespace strategy during the experimental phase;
2. remote versus inline JSON-LD context support;
3. mapping of provenance terms to PROV-O;
4. mapping-relation compatibility with SKOS;
5. representation of source binding and local references;
6. datatype of confidence and timestamps;
7. deterministic normalized output used for tests;
8. migration path from placeholder `example.org` context URIs in existing fixtures.

## Required tests

- expand every official profile example;
- verify required RDF triples;
- compact or normalize without losing ADUC meaning;
- preserve all assertion identifiers;
- reject or report unresolved context configuration;
- prove that the JSON Schema and RDF representation describe the same information model.

## Scope boundary

Do not begin external model-provider testing, public namespace registration, cryptographic signing, ontology discovery, registry work or the anticipation engine until the representation decision and round-trip tests pass.

## Completion test

Every official ADUC profile example must pass JSON Schema validation, semantic validation, JSON-LD expansion and deterministic RDF round-trip tests in GitHub Actions.
