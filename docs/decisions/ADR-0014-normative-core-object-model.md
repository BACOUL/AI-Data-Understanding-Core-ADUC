# ADR-0014 — Normative Core Object Model and Module Boundaries

- Status: accepted
- Date: 2026-07-14
- Issue: #47
- Pull request: #48
- Decision owners: ADUC maintainers

## Context

ADR-0005 through ADR-0013 define nine accepted domain profiles, but they did not define one normative envelope. Without a frozen object model, independent implementers could choose incompatible top-level blocks, identifiers, references, cardinalities, extension rules or ownership boundaries while still claiming to implement ADUC.

This decision composes the accepted profiles. It does not replace or weaken them and does not implement the official JSON Schema family.

## Decision

### Ten top-level Core blocks

A Core contract reserves exactly these top-level names in canonical documentation order:

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
| `relations` | no | 0..n | array of assertions |
| `policy` | no | 0..1 | object |

The minimum interoperable envelope is `aduc + resource + structure`. An absent optional block means `notDescribed`, not false, exact, trusted or permitted.

### Contract identity and publication

`aduc` owns:

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

`contractId` is an absolute IRI. Published contracts are immutable. A correction or replacement creates a new identifier and may link to the earlier contract through `supersedes`. Rewriting published content under the same identifier is non-conforming.

### One owner for every normative fact

Each normative fact has one owning module:

- source identity, media type, digest, version and locator belong to `resource`;
- records, fields, paths and primitive types belong to `structure`;
- concepts, units and semantic mappings belong to `semantics`;
- entities, identifiers and identity decisions belong to `identity`;
- temporal, spatial and operational interpretation belongs to `context`;
- agents, activities, evidence and derivation belong to `provenance`;
- measurement uncertainty, missingness, censoring and quality belong to `uncertainty`;
- general graph assertions belong to `relations`;
- permissions, prohibitions and duties belong to `policy`.

Competing representations in multiple modules are conflicts. Consumers must not merge or choose between them silently.

### Stable identifiers and deterministic references

Every addressable Core object has an `id` containing an absolute IRI. Local labels, array positions, mutable locations and undocumented JSON Pointers are not portable identities.

Internal references use properties ending in `Ref` or `Refs` and resolve to exactly one object in the same contract. External vocabulary terms use absolute IRIs and are never inferred from labels.

Duplicate identifiers, missing references and ambiguous references block the operation that depends on them.

### Structural precondition

Semantic, identity, contextual and uncertainty assertions may refer to a field only after it is declared in `structure` and the structure is bound to the exact `resource`.

`structure.resourceRef` resolves to `resource.id`. A structural field owns:

```text
id
name
sourcePath
primitiveType
required
```

External JSON Schema, Croissant, CSVW or OpenAPI descriptions are referenced through identified descriptors. ADUC does not embed renamed copies of those standards.

### Shared assertion qualification

Assertions remain owned by their domain module but use consistent qualification names where applicable:

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

ADR-0005, ADR-0010 and ADR-0011 govern these meanings. Measurement uncertainty is not semantic confidence. Confidence does not upgrade authority. Inferred assertions are never silently promoted.

### External standards boundary

ADUC composes established standards by reference:

- JSON Schema, Croissant, CSVW and OpenAPI for structure;
- QUDT and UCUM for units;
- RFC 3339, RFC 9557, IANA TZDB and OWL-Time for time;
- PROV-O for provenance;
- DQV for quality;
- RDF, RDFS, OWL and SKOS for relations and identity;
- ODRL for policy.

A module may add exact binding, qualification and deterministic consumer rules but must not create a competing complete copy of an external standard.

### JSON and JSON-LD boundary

Ordinary JSON with absolute identifiers is the canonical authoring representation. JSON-LD is a deterministic projection, not a second object model.

The JSON-LD projection uses a pinned versioned context, preserves Core meaning and qualifications, and does not require remote context retrieval. Aliases must not create duplicate normative properties.

### Extensions

Extensions are declared in `aduc.extensionDeclarations` using:

```text
namespace
profileIri
version
required
```

Payloads appear only in an `extensions` object on the hosting Core object. An extension must not use an ADUC Core namespace, overwrite a Core property, redefine a Core term or create a hidden mandatory dependency.

Unknown optional extensions are preserved and reported as unsupported. Unknown required extensions block conformance-dependent processing. Consumers must not treat unknown extension content as understood.

### Module boundaries and dependency graph

Hard dependencies are acyclic:

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

Optional references do not make an optional module globally mandatory, but an unresolved optional reference blocks the operation that requires it. `relations` may reference any declared Core object but never owns or redefines that object.

### Compatibility and replacement

A compatible change may add optional information when older consumers can preserve it safely without changing existing meaning.

Removing a property, changing meaning, cardinality, ownership, reference semantics or a safety default requires a new incompatible model version. Migration creates new documents and never rewrites published history.

### Existing semantic-mapping profile migration

The implemented mapping profile migrates into `structure` and `semantics.assertions`:

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

Fields first receive stable structural identifiers. Existing authority, evidence, confidence, conflict and lifecycle information is preserved. Missing information remains missing or unknown; migration must not invent it.

### Deterministic unsafe-information behavior

- absent optional module: report `notDescribed`;
- missing required Core data: reject the envelope or block the dependent operation;
- incomplete or redacted assertion: preserve and require review where applicable;
- contested assertion: do not select an authoritative interpretation automatically;
- deprecated object: follow an explicit compatible replacement or block;
- probable identity: do not merge as exact;
- unknown relation semantics: do not infer inverse, transitivity or causality;
- prohibited policy outcome: do not perform the governed use;
- indeterminate policy outcome: do not treat it as permission;
- unsupported required extension: block conformance-dependent processing;
- unsupported optional extension: preserve and report without interpretation.

## Rejected designs

- an envelope where every block is optional;
- multiple competing representations of one fact;
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
- all accepted profiles compose without losing their safety rules;
- schema implementers have fixed module boundaries;
- extensions remain possible without weakening Core.

### Costs

- producers must mint stable identifiers for addressable objects;
- compact local maps may require migration to identified arrays;
- external standards remain separate dependencies;
- consumers must preserve unsupported extensions and unresolved dimensions;
- schema evolution must respect ownership and compatibility rules.

## Acceptance evidence

PR #48 provides:

- `spec/ADUC_CORE_MODEL_0_1.md`;
- `docs/architecture/CORE_MODULE_BOUNDARIES_0_1.md`;
- machine-readable `spec/core-module-manifest.json`;
- one complete ten-block model containing 38 addressable objects with resolved references;
- twenty-five rejected architectural counterexamples;
- `tools/aduc_core_model.py`;
- eleven architecture and CLI tests;
- updated Core specification, roadmap, schema documentation, website and CI;
- correction of the review finding that distinguished the existing historical bootstrap schema from the future official modular schema family;
- every repository validation suite passing on the final reviewed head.

The architectural checker enforces the frozen object-model invariants. It is not the future official full-Core JSON Schema validator.

## Follow-up

1. implement the official modular Draft 2020-12 JSON Schema family;
2. create complete valid and invalid schema conformance fixtures;
3. build the unified Core validator and comparator;
4. validate the complete example against the official schemas;
5. implement migration tooling from the current mapping profile.