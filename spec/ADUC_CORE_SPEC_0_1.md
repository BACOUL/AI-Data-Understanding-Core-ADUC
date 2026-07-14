# AI Data Understanding Core — Core Specification 0.1

- Status: Working Draft with frozen object model
- Working name: AI Data Understanding Core (ADUC)
- Core version target: `0.1.0-alpha.0`
- Object-model version: `0.1.0`
- Language: English
- Date: 2026-07-14
- License target: Creative Commons Attribution 4.0

> ADUC is a working name. It must not be treated as a registered, protected, or recognized standard until naming, trademark, adoption, and governance requirements are met.

## 1. Mission

ADUC defines an open, model-independent contract allowing a data resource to describe its structure, meaning, identity, context, provenance, uncertainty, relations, and conditions of use to AI systems, agents, analytics and applications.

The initial falsifiable promise is:

> Two incompatible sources described with ADUC can be interpreted and compared consistently by multiple independent consumers without rebuilding provider-specific hidden mappings.

## 2. Normative document set

This specification is the Core overview. Normative details are split across:

- [`ADUC_CORE_MODEL_0_1.md`](ADUC_CORE_MODEL_0_1.md) — envelope, cardinalities, identifiers, references, ownership, dependencies, extensions and compatibility;
- [`core-module-manifest.json`](core-module-manifest.json) — machine-readable module and schema-family boundaries;
- accepted domain profiles for lifecycle, source binding, units, time, identity, provenance, uncertainty, relations and policy;
- ADR-0014 — architectural decision freezing the Core object model.

Where this overview conflicts with an accepted domain profile, the domain profile governs its own semantics. Where module placement or ownership is disputed, ADR-0014 and the Core object model govern.

## 3. What ADUC is not

ADUC is not:

- a replacement for JSON, CSV, JSON Schema, RDF, JSON-LD, Croissant, CSVW, OpenAPI, PROV-O, DQV, ODRL, SKOS, OWL, QUDT or UCUM;
- a universal ontology;
- an AI model, agent protocol or anticipation engine;
- a mechanism that proves factual truth, legal validity, ownership, consent or compliance;
- a production access-control system;
- a provider-specific prompt or hidden mapping format;
- proof of interoperability until independent qualifying runs exist.

ADUC composes established standards and adds portable binding, qualification, lifecycle and deterministic safety behavior.

## 4. Design principles

### 4.1 Preserve original data

An ADUC contract accompanies a resource. It does not require rewriting the resource.

```text
measurements.csv
measurements.aduc.json
```

### 4.2 Reuse established standards

External standards retain authority for their domain. ADUC references them rather than copying their complete models.

### 4.3 One normative owner per fact

A fact must have one owning Core module. Duplicate competing representations are non-conforming.

### 4.4 Explicit uncertainty and authority

Unknown, inferred, reviewed, verified, canonical, contested and deprecated information remain distinguishable. Confidence does not upgrade authority.

### 4.5 Deterministic local conformance

Structural and architectural rules must be checkable without private prompts, proprietary memory or remote context retrieval.

### 4.6 Provider independence

No Core property may depend on one model vendor, hosted registry, prompt format or embedding system.

## 5. Normative Core envelope

A Core contract reserves exactly ten top-level blocks:

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

Required minimum:

```text
aduc       exactly one object
resource   exactly one object
structure  exactly one object
```

Optional modules:

```text
semantics   zero or one object
identity    zero or one object
context     zero or one object
provenance  zero or one object
uncertainty zero or one object
relations   zero or more assertions in one array
policy      zero or one object
```

Unknown top-level blocks are forbidden. Extensions are declared in `aduc` and carried under an `extensions` property of the owning Core object.

## 6. Universal object rules

### 6.1 Stable identity

Every addressable object has an absolute-IRI `id`. The contract itself uses `aduc.contractId`. Identifiers are immutable and unique inside a contract.

### 6.2 Core references

Properties ending in `Ref` or `Refs` identify objects declared in the same contract and must resolve exactly once. External vocabulary identifiers use absolute IRIs and are never inferred from labels.

### 6.3 Published immutability

Published contracts are immutable. Replacement creates a new identifier and explicit replacement link. Migration never rewrites prior published history.

### 6.4 Shared qualification

Domain assertions may use the applicable subset of:

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

Their meaning is governed by the accepted lifecycle, provenance and uncertainty profiles.

## 7. `aduc` block

`aduc` owns contract metadata:

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

Required properties are `contractId`, `coreVersion`, `modelVersion`, `status`, `createdAt`, `publisher` and `conformsTo`.

A publisher identifier is a claim of publication source, not automatic proof of trust or ownership.

## 8. `resource` block

`resource` owns exact binding of the described resource:

```text
id
kind
mediaType
digest
version
locator
descriptorRefs
```

`id`, `kind`, `mediaType` and `digest` are required. Mutable location is discovery information, not identity. Source-binding rules follow ADR-0006.

Producer, concepts, units, uncertainty and permissions do not belong here.

## 9. `structure` block

`structure` owns records, fields, source paths, primitive types, keys and external schema references.

Required:

```text
id
resourceRef
representation
records
```

Every field has a stable `id`. Semantic, identity, contextual and uncertainty assertions may refer to a field only after it is declared here and bound to the exact resource.

JSON Schema, Croissant, CSVW and OpenAPI descriptions are referenced, not reimplemented as renamed ADUC fields.

## 10. `semantics` block

`semantics.assertions` maps structural objects to reusable concepts and units.

A semantic assertion preserves:

```text
id
subjectRef
conceptIri
mappingRelationIri
unitIri or valueMap when applicable
status and authority
asserting agent and time
evidence and provenance
confidence and method when probabilistic
conflict and lifecycle
```

The existing semantic-mapping profile migrates into this module without losing authority, evidence, confidence or lifecycle information.

## 11. `identity` block

`identity` owns entities, identifiers, schemes, issuers and identity decisions.

It must distinguish exact identity, probable identity, related entities, negative identity, unresolved identity and conflict. Probable identity must not be represented as exact identity. `owl:sameAs` remains restricted by ADR-0009.

## 12. `context` block

`context` owns temporal, spatial and operational interpretation.

Recommended collections:

```text
temporal
spatial
operational
```

Primitive field type remains structural. Temporal role, timezone, interval, precision and ambiguity behavior belong to context and follow ADR-0008.

## 13. `provenance` block

`provenance` owns agents, activities, evidence, entities and derivation assertions.

```text
agents
activities
entities
evidence
derivationAssertions
```

Qualifying references such as `assertedByRef`, `evidenceRefs` and `provenanceRef` resolve to declared objects here when present. PROV-O remains the external vocabulary authority.

## 14. `uncertainty` block

`uncertainty` owns measurement uncertainty, missingness, censoring, detection limits, distributions and DQV-compatible quality measurements.

```text
statements
qualityMeasurements
```

Measurement uncertainty is not semantic confidence, model probability, source authority or factual truth. Propagation follows ADR-0011.

## 15. `relations` block

`relations` is one array of qualified general assertions. A relation identifies stable endpoints, an absolute predicate IRI, polarity, method, evidence, provenance, scope, authority, conflict and lifecycle as required by ADR-0012.

Predicate meaning, inverse, symmetry, transitivity and causality are never inferred from labels or examples.

## 16. `policy` block

`policy` contains ODRL-aligned policy records. Every policy binds to the exact resource or version and preserves mode, disclosure, authority, evidence, provenance, validity, conflict, lifecycle and rules.

Descriptive classification is not executable permission. Safe outcomes remain:

```text
permit
deny
notApplicable
indeterminate
requiresHumanReview
```

These outcomes do not replace law, legal advice, access control or enforcement.

## 17. Module ownership constraints

At minimum, the Core rejects:

- producer information placed in `resource` instead of `provenance`;
- concepts or units placed in structural field definitions;
- measurement uncertainty placed in semantic assertions;
- structural fields redefined in context;
- embedded Core objects inside relation endpoints;
- descriptive policy classification made executable;
- extension payloads overwriting Core-owned properties.

A consumer must report the conflict rather than selecting one representation silently.

## 18. Dependency graph

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

Optional references do not make an optional module globally mandatory, but an operation depending on an unresolved reference is blocked.

## 19. Extensions

Extensions are declared through:

```text
namespace
profileIri
version
required
```

Extension payloads are stored under an `extensions` object on the owning Core object.

Rules:

- namespace and profile are absolute IRIs;
- ADUC Core namespaces cannot be claimed by extensions;
- Core terms cannot be overwritten or redefined;
- unknown optional extensions are preserved and reported;
- unknown required extensions block full-conformance processing;
- unknown extensions are never treated as understood.

## 20. JSON and JSON-LD

Ordinary JSON is the canonical authoring model. JSON-LD is a deterministic projection using a pinned local context.

JSON-LD must preserve identifiers, qualification and extension payloads and must not introduce a second property model. Remote context retrieval is not required for validation.

## 21. Versioning and compatibility

Compatible evolution may add optional information whose unknown behavior is safe and defined.

A new incompatible model version is required for:

- property removal or changed meaning;
- ownership transfer between modules;
- changed cardinality;
- changed reference semantics;
- weaker safety, evidence, lifecycle or authority requirements;
- changed interpretation of an existing controlled value.

## 22. Migration from the current mapping profile

Migration:

1. binds the exact source in `resource`;
2. creates stable records and fields in `structure`;
3. creates semantic assertions in `semantics`;
4. materializes agents and evidence in `provenance` where required;
5. preserves status, authority, evidence, confidence, conflict and lifecycle;
6. publishes a new immutable contract.

Migration must not promote inferred content merely because conversion succeeded.

## 23. Deterministic consumer behavior

| Condition | Required behavior |
|---|---|
| optional module absent | report `notDescribed` |
| required block absent | reject envelope |
| unresolved Core reference | block dependent operation |
| duplicate identifier | reject ambiguous graph |
| inferred assertion | preserve method and confidence; do not promote |
| contested assertion | no automatic authoritative selection |
| deprecated object | follow explicit compatible replacement or block |
| probable identity | do not merge as exact |
| unknown relation semantics | do not infer closure or causality |
| policy `deny` | do not perform governed use |
| policy `indeterminate` | do not interpret as permission |
| unknown optional extension | preserve and report |
| unknown required extension | block full-conformance processing |

## 24. Reference implementation status

Implemented reference profiles currently include lifecycle, source binding, units, time, identity, provenance, uncertainty, relations and policy.

ADR-0014 freezes the complete object model and module boundaries. ADR-0015 implements the official modular JSON Schema family and complete schema-valid fixtures. ADR-0016 implements the unified Core validator and deterministic comparator.

The architectural checker:

```bash
python tools/aduc_core_model.py
```

validates the frozen envelope and architecture invariants. It complements the official JSON Schema family and is orchestrated by the unified full-Core validator.

## 25. Complete model example

[`../examples/core/complete-model.example.json`](../examples/core/complete-model.example.json) demonstrates all ten blocks, exact bindings, stable identifiers, internal references, external terms, shared qualification and an optional declared extension.

The example validates against the official JSON Schema family and the complementary ADR-0014 architecture checker.

## 26. Release gate

Version `0.1.0-alpha.0` still requires:

- migration from the standalone semantic-mapping profile into full Core;
- JSON/CSV compiler and review workflow;
- value benchmark;
- qualifying independent multi-model interoperability evidence;
- naming and trademark decision.
