# ADR-0014 — Normative Core Object Model and Module Boundaries

- Status: accepted
- Date: 2026-07-14
- Issue: #47
- Pull request: pending
- Decision owners: ADUC maintainers

## Context

ADR-0005 through ADR-0013 define nine accepted domain profiles, but they do not yet define one normative envelope. Without a frozen object model, separate implementers could choose incompatible top-level blocks, identifiers, references, cardinalities, extension rules, or ownership boundaries while still claiming to implement ADUC.

This decision composes the accepted profiles. It does not replace or weaken them and does not implement the JSON Schema family.

## Decision

### 1. Ten top-level Core blocks

A Core contract has exactly these reserved top-level names, in canonical documentation order:

```text
aduc
resource
structure
semantics
identity
context
provenance
uncertainty
relations
policy
```

Cardinalities:

| Block | Required | Cardinality | Representation |
|---|---:|---:|---|
| `aduc` | yes | exactly 1 | object |
| `resource` | yes | exactly 1 | object |
| `structure` | yes | exactly 1 | object |
| `semantics` | no | 0..1 | object |
| `identity` | no | 0..1 | object |
| `context` | no | 0..1 | object |
| `provenance` | no | 0..1 | object |
| `uncertainty` | no | 0..1 | object |
| `relations` | no | 0..n | array of assertion objects |
| `policy` | no | 0..1 | object |

The minimum interoperable envelope is `aduc + resource + structure`. A document containing only `aduc`, or a document in which every domain block is optional, is not a Core contract.

### 2. Contract identity and publication

`aduc` owns contract identity and publication metadata:

```text
contractId
coreVersion
modelVersion
status
createdAt
publisher
conformsTo
supersedes
extensionDeclarations
```

`contractId` is an absolute IRI. Published contracts are immutable. Correction or replacement creates a new `contractId` and may identify the prior contract through `supersedes`. Reusing the same identifier for changed published content is non-conforming.

`coreVersion` identifies the ADUC release line. `modelVersion` identifies this object-model version. Module profile versions are declared in `conformsTo` and are not inferred from field presence.

### 3. One owner for every normative fact

Each normative fact has one owning module. A consumer must not merge competing representations from different blocks.

Examples:

- source bytes, media type, digest, version and locator belong to `resource`;
- record layout, fields, source paths and primitive types belong to `structure`;
- concepts, units and semantic mappings belong to `semantics`;
- entity identifiers and identity decisions belong to `identity`;
- temporal, spatial and operational interpretation belongs to `context`;
- agents, activities, evidence and derivation belong to `provenance`;
- measurement uncertainty, missingness, censoring and quality belong to `uncertainty`;
- general graph assertions belong to `relations`;
- permissions, prohibitions and duties belong to `policy`.

A convenience copy is allowed only when explicitly marked non-normative and derived from a canonical reference. It must never compete with the owning property.

### 4. Stable identifiers and references

Every addressable Core object has an `id` containing an absolute IRI. Local labels, array positions, mutable URLs without version binding, and undocumented JSON Pointers are not portable identities.

Cross-module references use properties ending in `Ref` or `Refs` and contain exact identifiers of objects declared in the same contract. External vocabulary terms use properties ending in `Iri` or vocabulary-specific names and are not Core object references.

A Core reference must resolve deterministically. Missing, ambiguous, or duplicate identifiers block the operation that depends on them.

### 5. Structural precondition

Semantic, identity, contextual, uncertainty, relation and policy assertions may refer to a field only after that field is declared by `structure` and the structure is bound to the exact `resource`.

`structure.resourceRef` is mandatory and resolves to `resource.id`. A field owns:

```text
id
name
sourcePath
primitiveType
required
```

External JSON Schema, Croissant, CSVW or OpenAPI descriptions are referenced through an identified descriptor reference. ADUC does not embed a renamed copy of those standards.

### 6. Shared assertion qualification

Assertions remain owned by their domain module, but qualifying semantics are consistent across modules. An assertion that claims authority carries the applicable subset of:

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

The meaning of these properties is governed by ADR-0005, ADR-0010 and ADR-0011. Measurement uncertainty is not semantic confidence. Confidence never upgrades authority. Inferred assertions are not silently promoted.

### 7. External standards boundary

ADUC composes established standards by reference:

- JSON Schema, Croissant, CSVW and OpenAPI for structure;
- QUDT and UCUM for units;
- RFC 3339, RFC 9557, IANA TZDB and OWL-Time for time;
- PROV-O for provenance;
- DQV for quality;
- RDF, RDFS, OWL and SKOS for relations and identity;
- ODRL for policy.

A Core module may add binding, qualification and deterministic consumer rules, but must not embed a competing complete copy of an external standard.

### 8. JSON and JSON-LD boundary

Canonical authoring uses ordinary JSON with absolute identifiers. JSON-LD is a deterministic projection, not a second object model.

The Core JSON representation:

- uses reserved top-level block names;
- uses absolute IRIs for identifiers and vocabulary terms;
- does not depend on remote context retrieval;
- preserves unknown extension payloads.

The JSON-LD representation uses a pinned, versioned context and must round-trip without changing Core meaning. A JSON-LD alias must not create a second normative property.

### 9. Extensions

Extensions are declared in `aduc.extensionDeclarations`. Each declaration includes:

```text
namespace
profileIri
version
required
```

Extension payloads appear only in an `extensions` object owned by a Core object. Each key is an absolute namespace IRI declared by the contract. An extension must not:

- use an ADUC Core namespace;
- overwrite a Core property;
- redefine a Core term;
- create a hidden mandatory dependency.

Unknown optional extensions are preserved and reported as unsupported. Unknown required extensions block conformance-dependent processing. Consumers must not treat an unknown extension as understood.

### 10. Module boundaries and dependency graph

Hard dependencies are acyclic:

```text
aduc
resource -> aduc
structure -> resource
provenance -> resource
context -> structure
semantics -> structure
identity -> structure
uncertainty -> structure
relations -> aduc
policy -> resource + provenance
```

A module may make optional references to another present module without making that module globally mandatory. `relations` may reference any declared Core object, but it does not own or redefine those objects.

### 11. Compatibility and replacement

Patch-compatible changes may add optional properties or controlled values when old consumers can preserve them safely. Removing a property, changing its meaning, changing cardinality, changing ownership, or weakening a safety rule requires a new incompatible model version.

Published objects are immutable. Replacement uses new identifiers and explicit replacement links. Migration tools create new documents; they do not rewrite history.

### 12. Existing semantic-mapping profile migration

The current mapping profile migrates into `semantics.assertions`:

```text
source.field -> subjectRef
semanticTarget -> conceptIri
mappingRelation -> mappingRelationIri
mappingStatus -> status
assertedBy -> assertedByRef
assertedAt -> assertedAt
evidence -> evidenceRefs
confidence -> confidence
confidenceMethod -> confidenceMethodIri
```

Source fields first receive stable `structure.fields[].id` values. Existing authority, evidence, confidence, conflict and lifecycle information must be preserved. Missing information remains missing or unknown; migration must not invent it.

### 13. Deterministic unsafe-information behavior

- absent optional module: report the dimension as not described;
- unknown required Core data: block the dependent operation;
- incomplete or redacted assertion: preserve and require review where the profile requires it;
- contested assertion: do not select one authoritative interpretation automatically;
- deprecated object: follow an explicit compatible replacement or block;
- prohibited policy result: do not perform the governed use;
- unsupported required extension: block conformance-dependent processing;
- unsupported optional extension: preserve and report, but do not interpret.

## Rejected designs

- an envelope where all blocks are optional;
- multiple competing representations of the same fact;
- local identifiers without issuer or namespace;
- array-position references;
- circular mandatory module dependencies;
- hidden prompts, provider fields or consumer-specific mappings in Core;
- embedded copies of complete external standards;
- a second JSON-LD-only object model;
- extensions that overwrite Core terms;
- unknown extensions treated as understood;
- in-place rewriting of published history.

## Consequences

### Positive

- the Core envelope and minimum contract are unambiguous;
- every normative fact has one owner;
- references and module dependencies are deterministic;
- accepted profiles compose without losing their safety rules;
- schema implementers have fixed module boundaries;
- extensions remain possible without weakening Core.

### Costs

- producers must mint stable identifiers for addressable objects;
- compact local maps may require migration to identified arrays;
- external standards remain separate dependencies;
- consumers must preserve unsupported extensions and unresolved dimensions;
- schema evolution must respect ownership and compatibility rules.

## Acceptance evidence

Acceptance requires:

- `spec/ADUC_CORE_MODEL_0_1.md`;
- `docs/architecture/CORE_MODULE_BOUNDARIES_0_1.md`;
- a machine-readable module manifest;
- one complete ten-block example;
- architectural counterexamples and deterministic checks;
- updated Core specification, roadmap, website and CI;
- all repository checks passing in the acceptance pull request.

## Follow-up

1. implement the official modular JSON Schema family;
2. create complete valid and invalid Core conformance examples;
3. build the unified Core validator;
4. update the complete example against the schemas;
5. define migration tooling from the current mapping profile.