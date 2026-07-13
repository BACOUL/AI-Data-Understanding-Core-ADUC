# ADUC Identity Profile 0.1

Status: Working Draft

This profile defines the minimum portable representation and consumer behavior for entity identifiers and identity relations in ADUC.

## 1. Scope

The profile covers:

- entity records;
- local, global, pseudonymous, and linkage-token identifiers;
- labels kept separate from identifiers;
- namespace, scheme, issuer, canonicalization, and validity;
- possible, exact, negative, broader, and narrower identity relations;
- authority, confidence, evidence, conflict, lifecycle, and privacy;
- deterministic merge decisions;
- recycled identifier detection.

It does not define a universal entity registry or replace GS1, LEI, DID, ORCID, or other identifier systems.

## 2. Required separation

A conforming implementation MUST keep these objects distinct:

```text
EntityRecord
IdentifierRecord
LabelRecord
IdentityRelationAssertion
IdentityEvaluationResult
```

A label MUST NOT be interpreted as a portable identifier.

## 3. Entity record

```json
{
  "entityId": "urn:aduc:entity:motor-42",
  "entityType": "urn:aduc:type:ElectricMotor",
  "labels": [
    {
      "value": "Main production motor",
      "language": "en",
      "labelType": "preferred"
    }
  ]
}
```

Requirements:

- `entityId` MUST be an absolute IRI;
- `entityType` MUST be an absolute IRI;
- labels are presentation metadata only;
- labels MUST NOT be used as equality keys.

## 4. Identifier record

```json
{
  "identifierId": "urn:aduc:idrecord:factory-fr-m42",
  "identifierKind": "local",
  "lexicalValue": "M42",
  "canonicalValue": "M42",
  "namespace": "urn:factory-fr:asset-id",
  "scheme": "urn:aduc:scheme:local-asset-id",
  "issuer": "urn:org:factory-fr",
  "subjectEntity": "urn:aduc:entity:motor-42",
  "entityType": "urn:aduc:type:ElectricMotor",
  "sourceBinding": "urn:binding:factory-fr-machine-field",
  "validity": {
    "start": "2020-01-01T00:00:00Z",
    "end": "2027-01-01T00:00:00Z"
  },
  "authorityLevel": "canonical",
  "assertedBy": "urn:org:factory-fr",
  "evidence": ["urn:evidence:factory-fr-asset-register"],
  "conflictState": "clear",
  "lifecycleState": "active"
}
```

### 4.1 Common required properties

Every identifier record MUST contain:

```text
identifierId
identifierKind
namespace
scheme
issuer
subjectEntity
entityType
sourceBinding
validity
authorityLevel
assertedBy
evidence
conflictState
lifecycleState
```

### 4.2 Identifier kinds

#### `local`

Requires:

```text
lexicalValue
canonicalValue
namespace
scheme
issuer
```

The portable comparison key is:

```text
scheme + namespace + issuer + canonicalValue + applicable time
```

#### `global`

Requires `globalIdentifier`, which MUST be an absolute IRI. The source scheme remains authoritative for canonicalization.

#### `pseudonymous`

Requires:

```text
protectedValue
protectionMethod
methodVersion
linkageDomain
permittedPurposes
```

The record MUST NOT contain `lexicalValue`, `canonicalValue`, `rawValue`, or the original secret identifier.

#### `linkageToken`

Requires the same protection metadata as `pseudonymous`, plus a declared token issuer and purpose. It is not a general identifier and MUST NOT be reused outside its permitted scope.

## 5. Validity

`validity.start` is inclusive. `validity.end`, when present, is exclusive. Values MUST be RFC 3339 instants.

An identifier is active at time `t` when:

```text
start <= t < end
```

or `start <= t` when no end is declared.

Two assignments of the same namespace-qualified canonical key to different entities MUST NOT overlap.

## 6. Identity relation assertion

```json
{
  "assertionId": "urn:aduc:identity-assertion:m42-main-b",
  "subjectIdentifier": "urn:aduc:idrecord:factory-fr-m42",
  "objectIdentifier": "urn:aduc:idrecord:factory-us-main-b",
  "relation": "sameEntity",
  "authorityLevel": "canonical",
  "assertedBy": "urn:org:global-asset-registry",
  "method": "urn:method:authoritative-crosswalk",
  "evidence": ["urn:evidence:asset-crosswalk-2026"],
  "validity": {
    "start": "2026-01-01T00:00:00Z"
  },
  "conflictState": "clear",
  "lifecycleState": "active",
  "privacy": {
    "permittedPurposes": ["maintenance-analysis"]
  }
}
```

### 6.1 Relations

```text
possibleMatch
sameEntity
differentEntity
broaderEntity
narrowerEntity
```

`unresolved` is an evaluation outcome, not a fabricated relation assertion.

### 6.2 Authority constraints

| Relation | Allowed authority |
|---|---|
| `possibleMatch` | `inferred`, `reviewed` |
| `sameEntity` | `verified`, `canonical` |
| `differentEntity` | `reviewed`, `verified`, `canonical` |
| `broaderEntity` | `verified`, `canonical` |
| `narrowerEntity` | `verified`, `canonical` |

For `inferred`, `confidence`, `method`, and evidence are mandatory. Confidence MUST be between 0 and 1 and remains separate from authority.

Canonical assertions MUST NOT include confidence.

## 7. Evaluation outcomes

A reference consumer returns one of:

```text
mergeAllowed
candidateOnly
differentEntity
relationOnly
mergeBlocked
unresolved
```

### 7.1 `mergeAllowed`

Requires all of:

- explicit `sameEntity`;
- `verified` or `canonical` authority;
- active, non-contested relation;
- active endpoint identifier assignments at the evaluation time;
- identified asserting authority, method, and evidence;
- compatible entity types or a verified compatibility assertion;
- no contradictory active relation;
- no overlapping reassignment conflict;
- privacy permission for the declared purpose.

### 7.2 `candidateOnly`

Returned for `possibleMatch` or any non-qualifying suggestion. It MUST NOT trigger record fusion.

### 7.3 `differentEntity`

Returned when an active qualifying negative assertion is present. It blocks fusion.

### 7.4 `relationOnly`

Returned for broader/narrower relations. These relations do not imply record equality.

### 7.5 `mergeBlocked`

Returned when exact identity is claimed but conflict, expiry, lifecycle, type, privacy, or assignment checks fail.

### 7.6 `unresolved`

Returned when no qualifying relation exists.

## 8. Contradictions

For the same unordered endpoint pair and overlapping validity:

- `sameEntity` and `differentEntity` conflict;
- multiple active canonical relations with incompatible conclusions conflict;
- an active `sameEntity` plus a contested or deprecated relation blocks merge;
- overlapping assignment of one identifier key to different entities conflicts.

Assertions remain immutable. Resolution creates a separate record under the epistemic lifecycle model.

## 9. `owl:sameAs` export

A consumer MAY export `owl:sameAs` only when the evaluation result is `mergeAllowed` and the identity scope is exact.

A consumer MUST NOT export `owl:sameAs` for:

```text
possibleMatch
broaderEntity
narrowerEntity
reviewed-only suggestions
contested assertions
time-incompatible assignments
privacy-blocked linkage
```

## 10. Privacy-preserving linkage

A protected identifier record MUST:

- omit raw secret values;
- declare protection method and version;
- declare issuer and linkage domain;
- declare permitted purposes;
- bind to source and evidence;
- prevent use outside the permitted purpose.

A matching digest alone does not override purpose or authority constraints.

## 11. Reassignment, alias, merger, and split

- changing a label does not change entity identity;
- replacement identifiers create new immutable records;
- reassignment uses non-overlapping validity intervals;
- mergers and splits are explicit entity relations with their own validity and authority;
- history is never rewritten;
- transitivity is not inferred through possible, broader, narrower, contested, or expired relations.

## 12. Source, temporal, and epistemic dependencies

Every identity object MUST reuse:

- ADR-0005 for authority, confidence, conflict, lifecycle, and immutable events;
- ADR-0006 for exact source and field binding;
- ADR-0008 for validity intervals and evaluation time.

## 13. Consumer invariants

A conforming consumer MUST:

1. compare local identifiers only with namespace, scheme, issuer, and applicable time;
2. keep labels outside equality keys;
3. treat `possibleMatch` as non-merging;
4. block expired, recycled, contested, deprecated, contradictory, or privacy-incompatible identity;
5. keep confidence separate from authority;
6. refuse strong equality when endpoint records are absent;
7. avoid transitive closure across non-exact relations;
8. preserve all evidence and original assertions;
9. export `owl:sameAs` only after `mergeAllowed`;
10. report unresolved identity instead of guessing.

## 14. Migration examples

### Local machine identifier

```json
{
  "identifierKind": "local",
  "lexicalValue": "M42",
  "canonicalValue": "M42",
  "namespace": "urn:factory-fr:asset-id",
  "issuer": "urn:org:factory-fr"
}
```

### Separate US identifier

```json
{
  "identifierKind": "local",
  "lexicalValue": "MAIN-B",
  "canonicalValue": "MAIN-B",
  "namespace": "urn:factory-us:equipment-id",
  "issuer": "urn:org:factory-us"
}
```

No identity relation is created until evidence supports it.

### River station identifier

```json
{
  "identifierKind": "local",
  "lexicalValue": "R42",
  "canonicalValue": "R42",
  "namespace": "urn:river-agency:station-id",
  "issuer": "urn:org:river-agency"
}
```

## 15. Conformance

The reference implementation is:

```bash
python tools/aduc_identity.py \
  examples/identity/reference-cases.json \
  examples/identity/invalid-cases.json
```

A conforming implementation must produce equivalent validity and decision outcomes for the official cases.