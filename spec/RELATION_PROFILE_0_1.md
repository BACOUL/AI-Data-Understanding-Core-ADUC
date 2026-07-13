# ADUC Relation Profile 0.1

Status: working draft  
Decision: ADR-0012  
Scope: portable and safely consumable relation assertions

## 1. Purpose

This profile defines how an ADUC consumer represents and evaluates relationships between bound objects without inventing semantics that the predicate vocabulary does not authorize.

## 2. Normative model

A relation document contains:

```json
{
  "registry": {},
  "objects": [],
  "assertions": []
}
```

### 2.1 Registry reference

The registry reference must include:

```text
path
registryId
registryVersion
sha256
```

The referenced registry is immutable for the evaluation. The digest is computed over the exact UTF-8 bytes.

### 2.2 Bound object

```json
{
  "binding": "urn:aduc:entity:machine-42",
  "kind": "entity"
}
```

Allowed Core kinds are:

```text
resource field concept entity assertion activity version result
```

### 2.3 Relation assertion

```json
{
  "relationId": "urn:aduc:relation:part-1",
  "subject": {"binding": "urn:aduc:entity:motor"},
  "predicate": "urn:aduc:predicate:strictPartOf",
  "object": {"binding": "urn:aduc:entity:machine"},
  "polarity": "positive",
  "method": "urn:aduc:method:asset-crosswalk-v1",
  "provenanceActivity": "urn:aduc:activity:relation-assessment-v1",
  "authorityLevel": "verified",
  "assertedBy": "urn:aduc:org:asset-owner",
  "evidence": ["urn:aduc:evidence:asset-registry"],
  "conflictState": "clear",
  "lifecycleState": "active"
}
```

A literal property uses:

```json
{
  "object": {
    "literal": {
      "value": "River observations",
      "language": "en"
    }
  }
}
```

A literal must have exactly one of `datatype` or `language`.

## 3. Predicate definitions

A predicate profile declares:

```text
family
objectMode
subjectKinds
objectKinds
characteristics
inverseOf
transitiveSuperproperty
exactness
disjointWith
minimumAuthority
requiresIdentityProfile
authoritySource
```

Characteristics may include:

```text
symmetric
transitive
reflexive
functional
inverseFunctional
acyclic
```

Missing characteristics are not assumed.

## 4. Consumer rules

### 4.1 Automatic use

An assertion is automatically usable only when it is:

```text
structurally valid
bound to valid endpoints
active
clear of conflict
inside requested temporal scope
inside requested context
sufficiently authoritative for the predicate
```

### 4.2 Inverse

A reverse may be derived only from an authoritative inverse or symmetry declaration.

### 4.3 Transitive closure

A transitive result requires:

- an authoritative transitive predicate or transitive superproperty;
- a qualifying path of active positive assertions;
- compatible predicate semantics;
- no blocked assertion in the path.

### 4.4 Exactness

```text
close ≠ exact
related ≠ broader
part-of ≠ identity
version-of ≠ identity
derived-from ≠ causation
correlated-with ≠ causation
causal-candidate ≠ established cause
```

### 4.5 Open world

A missing relation yields:

```text
unknown
```

Only an explicit qualifying negative assertion yields `false`.

## 5. Conflict rules

The profile blocks:

- duplicate relation IDs;
- incompatible positive and negative strong assertions;
- disjoint predicates on the same pair;
- more than one object for a functional predicate;
- more than one subject for an inverse-functional predicate;
- cycles for an acyclic predicate;
- contested or deprecated automatic use.

## 6. Scope

Temporal scope uses ADR-0008 semantics. Context identifiers are absolute IRIs. A relation outside its declared scope must not be consumed automatically.

## 7. Identity boundary

`owl:sameAs` is accepted only for entity endpoints, verified or canonical authority, and an explicit `identityProfileRef` satisfying ADR-0009.

Concept mappings use SKOS predicates and do not silently merge real-world entities.

## 8. Causality boundary

The Core records dependency, correlation and causal candidates but does not perform causal identification. Causal claims require an external method or extension.

## 9. Export

The reference exporter emits:

1. an RDF statement node for each assertion and its qualification;
2. a direct positive triple only for qualifying active assertions;
3. absolute IRIs;
4. typed or language-tagged literals;
5. deterministic ordering.

## 10. Error families

```text
ADUC-REL-VOCAB-*    registry identity and integrity
ADUC-REL-DOC-*      document and identifier integrity
ADUC-REL-PRED-*     predicate identity and allowed use
ADUC-REL-ENDPOINT-* binding, kind and object-mode errors
ADUC-REL-LIT-*      literal representation
ADUC-REL-AUTH-*     authority, method and evidence
ADUC-REL-SCOPE-*    temporal and contextual scope
ADUC-REL-LIFE-*     conflict and lifecycle
ADUC-REL-ID-*       exact identity gate
ADUC-REL-INF-*      inverse, symmetry and transitivity
ADUC-REL-SEM-*      exactness misuse
ADUC-REL-CAUSE-*    unsupported causality
ADUC-REL-OPEN-*     open-world misuse
ADUC-REL-CONFLICT-* graph contradictions
ADUC-REL-CYCLE-*    forbidden cycles
```

## 11. Core boundary

This profile does not define:

- a universal relation vocabulary;
- domain causal semantics;
- arbitrary OWL reasoning;
- complete SHACL validation;
- policy or rights evaluation;
- the full-Core JSON Schema;
- compiler inference behavior.

## 12. Conformance

A conforming implementation must reproduce the official reference cases and reject the official counterexamples without model-specific instructions.
