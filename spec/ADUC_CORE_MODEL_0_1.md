# ADUC Normative Core Object Model 0.1

- Status: Normative draft accepted by ADR-0014
- Model version: `0.1.0`
- Core release target: `0.1.0-alpha.0`
- Machine-readable manifest: [`core-module-manifest.json`](core-module-manifest.json)

## 1. Purpose

This document defines the normative ADUC object model implemented by the official modular JSON Schema family. It fixes the envelope, object ownership, identifiers, references, cardinalities, module dependencies, extension rules, lifecycle behavior, compatibility boundaries and migration target.

The accepted domain profiles remain authoritative for their domain-specific semantics. This model defines where they live and how they compose.

## 2. Normative language

`MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT` and `MAY` are normative requirements.

A **Core object** is an addressable object declared by a Core module. A **Core reference** is an exact identifier reference to such an object. An **external term** is an IRI owned by another standard or vocabulary.

## 3. Canonical envelope

```json
{
  "aduc": {},
  "resource": {},
  "structure": {},
  "semantics": {},
  "identity": {},
  "context": {},
  "provenance": {},
  "uncertainty": {},
  "relations": [],
  "policy": {}
}
```

Reserved top-level names are exactly:

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

Unknown top-level properties are non-conforming. Extension payloads do not create new top-level blocks.

## 4. Cardinality and minimum envelope

| Module | Required | Cardinality | Empty value allowed |
|---|---:|---:|---:|
| `aduc` | yes | exactly one object | no |
| `resource` | yes | exactly one object | no |
| `structure` | yes | exactly one object | no |
| `semantics` | no | zero or one object | no |
| `identity` | no | zero or one object | no |
| `context` | no | zero or one object | no |
| `provenance` | no | zero or one object | no |
| `uncertainty` | no | zero or one object | no |
| `relations` | no | zero or more assertions in one array | an empty array SHOULD be omitted |
| `policy` | no | zero or one object | no |

The minimum interoperable contract is:

```json
{
  "aduc": {},
  "resource": {},
  "structure": {}
}
```

A consumer MUST report every absent optional module as `notDescribed`, not as false, zero, permitted, exact or trusted.

## 5. Universal representation rules

### 5.1 Identifiers

Every addressable object MUST have an `id` with an absolute IRI. `aduc.contractId` is the contract identifier and follows the same rule.

Identifiers MUST be unique inside the contract. Array positions, display names, local labels and unqualified strings are not portable identifiers.

### 5.2 Internal references

Properties ending in `Ref` contain one Core object identifier. Properties ending in `Refs` contain a list of Core object identifiers.

Every Core reference MUST resolve to exactly one object in the same contract. A reference to an external resource is represented as an external IRI property, not as an unresolved Core reference.

### 5.3 External terms

Properties ending in `Iri` identify terms owned by an external standard or vocabulary. Examples include `conceptIri`, `unitIri`, `predicateIri`, `actionIri`, `purposeIris`, `timezoneIri` and `qualityMetricIri`.

External terms MUST be absolute IRIs. ADUC does not infer them from labels.

### 5.4 Arrays

Addressable repeated objects use arrays of objects with stable `id` values. A consumer MUST NOT use array order as semantic identity. Canonical serialization SHOULD order addressable arrays by `id` unless a domain profile defines meaningful order.

### 5.5 Published immutability

A published contract or published object MUST NOT be modified in place. Replacement creates a new identifier and explicit replacement relation.

## 6. `aduc` module

The `aduc` module owns metadata about the contract, not the described data.

Required properties:

| Property | Cardinality | Meaning |
|---|---:|---|
| `contractId` | 1 | absolute IRI identifying this immutable contract |
| `coreVersion` | 1 | ADUC Core release line |
| `modelVersion` | 1 | object-model version |
| `status` | 1 | epistemic/publication status |
| `createdAt` | 1 | timezone-aware creation instant |
| `publisher` | 1 | absolute IRI of publishing agent |
| `conformsTo` | 1..n | implemented Core and profile IRIs |

Optional properties:

| Property | Cardinality | Meaning |
|---|---:|---|
| `supersedes` | 0..1 | prior contract identifier |
| `extensionDeclarations` | 0..n | declared extension profiles |
| `extensions` | 0..1 | extension payload map for contract metadata |

`status` follows ADR-0005. `publisher` does not by itself prove ownership or trust.

## 7. `resource` module

The `resource` module owns the identity and immutable binding of the described resource.

Required:

```text
id
kind
mediaType
digest
```

Optional:

```text
version
locator
descriptorRefs
extensions
```

`digest` MUST use the source-binding format accepted by ADR-0006. A mutable `locator` is discovery information, not identity. A semantic assertion MUST NOT be consumed until its field reference ultimately resolves to this exact resource binding.

The resource module MUST NOT own producer, measurement method, concept, unit, uncertainty or permission facts.

## 8. `structure` module

The `structure` module defines how to read the bound resource.

Required:

```text
id
resourceRef
representation
records
```

A record object owns:

```text
id
name
sourcePath
fields
```

A field object owns:

```text
id
name
sourcePath
primitiveType
required
```

Optional structural properties include keys, nullability, repeated-value behavior and `externalSchemaRef`.

`externalSchemaRef` identifies an external JSON Schema, Croissant, CSVW or OpenAPI descriptor represented as a provenance entity or resource descriptor. The complete external schema MUST NOT be copied into renamed ADUC properties.

## 9. `semantics` module

The `semantics` module contains semantic mapping assertions. It owns concepts, mapping relations, units and value mappings, but not field structure or measurement uncertainty.

```json
{
  "assertions": [
    {
      "id": "urn:example:semantic:flow",
      "subjectRef": "urn:example:field:flow",
      "conceptIri": "https://example.org/vocab/WaterDischarge",
      "mappingRelationIri": "http://www.w3.org/2004/02/skos/core#exactMatch",
      "unitIri": "https://qudt.org/vocab/unit/M3-PER-SEC",
      "status": "reviewed",
      "assertedByRef": "urn:example:agent:reviewer",
      "assertedAt": "2026-07-14T08:00:00Z",
      "evidenceRefs": ["urn:example:evidence:data-dictionary"],
      "provenanceRef": "urn:example:activity:semantic-review"
    }
  ]
}
```

Every `subjectRef` MUST resolve to a structural object. Domain semantics follow the accepted semantic-mapping profile and unit profile.

## 10. `identity` module

The `identity` module owns entities, identifiers and identity decisions.

Recommended collections:

```text
entities
identifiers
identityAssertions
```

An identifier records its scheme and issuer. An identity assertion distinguishes exact, probable, related, negative and unresolved identity. Probable identity MUST NOT be encoded as exact identity. `owl:sameAs` remains gated by ADR-0009.

## 11. `context` module

The `context` module owns interpretation of time, space and operational environment.

Recommended collections:

```text
temporal
spatial
operational
```

Temporal objects may bind a field through `fieldRef` and declare role, timezone, precision, interval or duration semantics. Spatial and operational objects use absolute identifiers where portable identity is required.

Raw field type remains owned by `structure`; temporal meaning belongs to `context`.

## 12. `provenance` module

The `provenance` module owns traceability objects and evidence.

Collections:

```text
entities
activities
agents
evidence
derivationAssertions
```

Core objects referenced by `assertedByRef`, `evidenceRefs` and `provenanceRef` MUST resolve here when those qualifiers are present.

The module reuses PROV-O. It records claims and bindings; it does not independently prove authenticity.

## 13. `uncertainty` module

The `uncertainty` module owns measurement uncertainty, missingness, censoring, detection limits, distributional information and DQV-compatible quality measurements.

Collections:

```text
statements
qualityMeasurements
```

Every statement identifies its target through `subjectRef`. Measurement uncertainty MUST NOT be reused as semantic confidence or identity probability. Propagation follows ADR-0011.

## 14. `relations` module

`relations` is one array of general relation assertions. Every relation assertion has an `id` and follows ADR-0012.

Typical properties:

```text
id
subjectRef
predicateIri
objectRef or literalObject
polarity
methodIri
qualification fields
```

The relation module may reference any declared Core object. It MUST NOT recreate an object already owned by another module. Predicate semantics are never inferred from labels.

## 15. `policy` module

The `policy` module owns one or more ODRL-aligned policy records.

```text
policies
```

Each policy binds its `targetRef` to the resource or a declared version object and preserves target digest, mode, disclosure, authority, evidence, provenance, conflict, lifecycle, validity and rules.

Classification is descriptive. It is not executable permission. Evaluation outcomes remain those accepted by ADR-0013.

## 16. Shared qualification model

The following property names are shared qualification vocabulary, not a separate top-level module:

| Property | Meaning owner |
|---|---|
| `status` | ADR-0005 |
| `authority` | ADR-0005 |
| `assertedByRef` | domain assertion, resolved through provenance/identity |
| `assertedAt` | assertion event time |
| `evidenceRefs` | provenance evidence objects |
| `provenanceRef` | provenance activity or assertion |
| `confidence` | domain-specific calibrated confidence |
| `confidenceMethodIri` | calibration or scoring method |
| `uncertaintyRef` | uncertainty object |
| `conflict` | ADR-0005/domain profile |
| `lifecycle` | ADR-0005/domain profile |
| `validDuringRef` | context temporal object |

A module MAY require a stricter subset. Sharing these names does not transfer ownership of the underlying domain fact.

## 17. Ownership constraints

The following duplicate representations are forbidden:

- `resource.producer` competing with `provenance.agents` or activities;
- `structure.fields[].unit` competing with `semantics.assertions[].unitIri`;
- `semantics.assertions[].measurementUncertainty` competing with `uncertainty.statements`;
- `context.fields` competing with structural field definitions;
- `relations[].source` containing an embedded copy of a resource;
- `policy.classification` used as an executable permission;
- extension properties redefining a Core-owned property.

Consumers MUST use the owning module and MUST report competing representations as a conflict rather than choosing silently.

## 18. Module dependency graph

Hard dependencies:

| Module | Hard dependencies |
|---|---|
| `aduc` | none |
| `resource` | `aduc` |
| `structure` | `resource` |
| `provenance` | `resource` |
| `context` | `structure` |
| `semantics` | `structure` |
| `identity` | `structure` |
| `uncertainty` | `structure` |
| `relations` | `aduc` |
| `policy` | `resource`, `provenance` |

Hard dependencies MUST be acyclic. Optional references do not make the referenced module globally mandatory, but an operation depending on that reference is blocked when it cannot resolve.

## 19. Extensions

An extension declaration is:

```json
{
  "namespace": "https://example.org/aduc-extension/",
  "profileIri": "https://example.org/aduc-extension/profile/1.0",
  "version": "1.0.0",
  "required": false
}
```

An extension payload is stored under the host object's `extensions` map:

```json
{
  "extensions": {
    "https://example.org/aduc-extension/": {
      "customTerm": "value"
    }
  }
}
```

Rules:

1. the namespace MUST be declared;
2. the namespace MUST be absolute and MUST NOT be an ADUC Core namespace;
3. the payload MUST NOT contain a key owned by the host Core object;
4. an unknown optional extension is preserved and reported;
5. an unknown required extension blocks processing that claims full conformance;
6. consumers MUST NOT infer extension meaning from labels.

## 20. JSON-LD projection

The ordinary JSON model is normative. JSON-LD projection:

- uses a pinned local context;
- maps Core identifiers to `@id` without changing identity;
- maps external terms to their authoritative IRIs;
- preserves qualification nodes;
- preserves unknown extensions;
- produces deterministic normalized RDF for qualifying records.

Remote context retrieval MUST NOT be required for validation or interpretation.

## 21. Versioning and compatibility

A model change is backward compatible only when an older consumer can safely preserve or ignore the new information without changing existing meaning.

Compatible candidates:

- a new optional property;
- a new optional module profile;
- a new controlled value whose unknown behavior is defined as preserve-and-report.

Incompatible changes:

- property removal or renaming;
- ownership transfer between modules;
- cardinality change;
- changed reference semantics;
- changed safety default;
- weaker evidence, authority, conflict or lifecycle requirement;
- changed meaning of an existing controlled value.

Incompatible changes require a new model version and migration guidance.

## 22. Migration from the semantic-mapping profile

Migration steps:

1. bind the exact source in `resource`;
2. create `structure` records and stable field identifiers;
3. create one semantic assertion per existing mapping;
4. replace local field references with `subjectRef` identifiers;
5. preserve concept, relation, status, authority, evidence, confidence and lifecycle data;
6. materialize referenced evidence and agents in `provenance` where required;
7. leave unavailable information absent or explicitly unknown;
8. publish the migrated contract under a new immutable identifier.

Migration MUST NOT infer reviewed, verified or canonical authority from successful parsing or high confidence.

## 23. Consumer behavior matrix

| Condition | Required behavior |
|---|---|
| optional module absent | report `notDescribed` |
| required block absent | reject Core envelope |
| unknown Core property | reject or preserve only under declared extension rules |
| unresolved Core reference | block dependent operation |
| duplicate identifier | reject ambiguous graph |
| inferred assertion | preserve method/confidence; do not promote |
| contested assertion | require review or report multiple interpretations |
| deprecated object | follow explicit compatible replacement or block |
| probable identity | do not merge as exact |
| unknown relation predicate semantics | do not infer inverse/transitivity/causality |
| policy `deny` | do not perform governed use |
| policy `indeterminate` | do not interpret as permission |
| unknown optional extension | preserve and report |
| unknown required extension | block full-conformance processing |

## 24. Schema-family contract

The official schema family implements this object model without revisiting architecture. The module list is fixed in `core-module-manifest.json`.

The root schema enforces the ten-block envelope and delegates to modular schemas. Shared qualification and extension definitions are reusable `$defs` or referenced schemas. Cross-object architectural checks remain complementary to JSON Schema.

## 25. Complete example

[`../examples/core/complete-model.example.json`](../examples/core/complete-model.example.json) demonstrates every Core module, stable identifiers, internal references, external terms, qualification, exact resource binding and an optional declared extension.

The example is schema-valid and architecture-valid under the accepted Core schema family and complementary ADR-0014 checker.
