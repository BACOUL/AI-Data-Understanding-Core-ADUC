# ADUC Core Module Boundaries 0.1

- Status: Normative architecture companion to ADR-0014
- Model: `urn:aduc:core-model:0.1`
- Machine-readable source: [`../../spec/core-module-manifest.json`](../../spec/core-module-manifest.json)

## Purpose

This document assigns every Core responsibility to one module and fixes the dependency graph for the future JSON Schema family. It prevents duplicate representations, circular mandatory dependencies and architecture decisions hidden inside schema implementation.

## Boundary rules

1. A normative fact has exactly one owning module.
2. A module may reference another module but must not copy its objects.
3. Hard dependencies are acyclic.
4. Optional references block only the dependent operation when unresolved.
5. External standards remain external and are referenced by identifiers.
6. Extension payloads never overwrite Core-owned properties.
7. Absence of a module means `notDescribed`, not a negative fact.

## Module responsibility matrix

| Module | Owns | Must not own |
|---|---|---|
| `aduc` | contract identity, versions, publication status, conformance, replacement, extension declarations | resource bytes, fields, concepts, entities, evidence, policy rules |
| `resource` | exact described-resource identity, kind, media type, digest, version, locator, descriptor references | producer, field definitions, semantic meaning, uncertainty, permissions |
| `structure` | record layout, fields, source paths, primitive types, keys and external schema references | concepts, units, temporal meaning, producer, quality, policy |
| `semantics` | field-to-concept mappings, mapping relations, units and value maps | source paths, entity equivalence, measurement uncertainty, general graph relations |
| `identity` | entities, identifier schemes and issuers, identity assertions and merge decisions | semantic field concepts, general graph closure, producer history |
| `context` | temporal role, timezone, intervals, spatial and operational interpretation | primitive field type, source bytes, measurement uncertainty |
| `provenance` | agents, activities, evidence, entities and derivation history | semantic meaning, identity decision, policy result |
| `uncertainty` | measurement uncertainty, missingness, censoring, distributions and quality metrics | semantic confidence, authority, factual truth |
| `relations` | qualified general relation assertions between declared objects | embedded copies of referenced objects, implicit predicate semantics |
| `policy` | ODRL-aligned permissions, prohibitions, duties, target scope and deterministic evaluation conditions | access enforcement, legal validity, resource identity, descriptive classification as permission |

## Hard-dependency graph

```text
aduc
└── resource
    ├── structure
    │   ├── semantics
    │   ├── identity
    │   ├── context
    │   └── uncertainty
    ├── provenance
    │   └── policy
    └── policy

relations -> aduc
```

Canonical dependency list:

```text
aduc: []
resource: [aduc]
structure: [resource]
semantics: [structure]
identity: [structure]
context: [structure]
provenance: [resource]
uncertainty: [structure]
relations: [aduc]
policy: [resource, provenance]
```

No module may add a mandatory dependency that creates a cycle. Optional references are allowed only when missing-reference behavior is explicit.

## Reference directions

| Referring object | Reference | Target owner |
|---|---|---|
| `structure` | `resourceRef` | `resource` |
| semantic assertion | `subjectRef` | `structure` |
| identity identifier/assertion | `fieldRef`, `entityRef`, `identifierRef` | `structure`, `identity` |
| temporal context | `fieldRef` | `structure` |
| provenance activity | `usedRefs`, `generatedRefs` | any already declared object, normally `resource` or provenance entity |
| uncertainty statement | `subjectRef` | `structure`, `semantics` or declared result object |
| relation assertion | `subjectRef`, `objectRef` | any declared Core object |
| policy | `targetRef` | `resource` or declared version object |
| qualification | `assertedByRef`, `evidenceRefs`, `provenanceRef` | `provenance`/`identity` |
| qualification | `uncertaintyRef` | `uncertainty` |
| qualification | `validDuringRef` | `context` |

A reference is always by stable identifier. Embedded duplicate objects are forbidden.

## Shared qualification boundary

Shared qualification field names are reusable, but their host assertion remains owned by its domain module.

```text
status
authority
assertedByRef
assertedAt
evidenceRefs
provenanceRef
confidence
confidenceMethodIri
uncertaintyRef
conflict
lifecycle
validDuringRef
```

Examples:

- `semantics.assertions[].confidence` is semantic-mapping confidence;
- `identity.identityAssertions[].confidence` is identity-resolution confidence;
- `uncertainty.statements[]` represents measurement uncertainty;
- `policy.policies[].authority` represents policy assertion authority.

These values must not be substituted for one another.

## External-standard boundary

| Capability | External authority | ADUC addition |
|---|---|---|
| structural validation | JSON Schema, Croissant, CSVW, OpenAPI | exact source binding and stable field references |
| units | QUDT, UCUM | deterministic use, role and conversion qualification |
| time | RFC 3339, RFC 9557, IANA TZDB, OWL-Time | field binding and safe ambiguity behavior |
| provenance | PROV-O | exact artifact binding and disclosure/replay qualification |
| quality | DQV | integration with uncertainty and consumer blocking rules |
| relations | RDF, RDFS, OWL, SKOS | endpoint binding, authority, scope and safe inference gates |
| policy | ODRL | exact target binding, evidence, lifecycle and safe outcomes |

ADUC must not rename and re-embed a complete external model.

## Planned schema-family boundaries

The future schema family will have one root schema and modular schemas:

```text
schema/aduc-core.schema.json
schema/aduc-envelope.schema.json
schema/aduc-metadata.schema.json
schema/resource.schema.json
schema/structure.schema.json
schema/semantics.schema.json
schema/identity.schema.json
schema/context.schema.json
schema/provenance.schema.json
schema/uncertainty.schema.json
schema/relations.schema.json
schema/policy.schema.json
schema/qualification.schema.json
schema/extension.schema.json
```

Rules for implementation:

- the root schema owns top-level names and required blocks;
- each module schema owns only its module properties;
- shared qualification definitions are reused, not copied with divergent meaning;
- extension validation is centralized;
- module schemas must not require optional modules globally;
- cross-reference integrity may require a reference validator in addition to JSON Schema;
- the schema task must not change this dependency graph without a new ADR.

## Duplicate-fact conflict catalogue

The architecture checker must reject at least:

| Forbidden representation | Correct owner |
|---|---|
| `resource.producer` | `provenance` |
| `resource.license` as executable permission | `policy` |
| `structure.fields[].concept` | `semantics` |
| `structure.fields[].unit` | `semantics` |
| `semantics.assertions[].measurementUncertainty` | `uncertainty` |
| `identity.entities[].semanticMapping` | `semantics` |
| `context.fields` redefining field structure | `structure` |
| `relations[].subject` containing an embedded Core object | referenced object's owning module |
| `policy.classification` treated as executable permission | `policy.rules` with ODRL-aligned effect |
| extension payload containing a host Core property | host module |

## Unsupported-information behavior

| Condition | Behavior |
|---|---|
| missing optional module | `notDescribed` |
| unresolved mandatory reference | block dependent operation |
| duplicate identifier | reject contract graph |
| unknown external predicate semantics | preserve assertion; no inferred closure |
| unknown optional extension | preserve and report unsupported |
| unknown required extension | block full-conformance processing |
| contested assertion | no automatic authoritative selection |
| deprecated object | explicit compatible replacement or block |
| policy prohibition | governed operation must not proceed |
| policy indeterminate | must not be treated as permission |

## Migration boundary

The existing semantic-mapping profile is not retained as a parallel top-level format inside the Core. It migrates to `structure` plus `semantics` and materializes referenced agents/evidence in `provenance` when required.

Migration must preserve:

```text
field identity
semantic target
mapping relation
status
authority
assertedBy
assertedAt
evidence
confidence
confidence method
conflict
lifecycle
```

A migration tool may emit an inferred new contract, but successful migration does not promote authority.