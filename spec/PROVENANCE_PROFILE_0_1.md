# ADUC Provenance Profile 0.1

- Status: Working draft
- Decision: ADR-0010
- Scope: provenance and transformation lineage for the ADUC Core
- Normative vocabulary basis: W3C PROV-O

## 1. Purpose

This profile defines a portable JSON representation and deterministic consumer rules for tracing ADUC data and assertions through transformations.

It does not replace PROV-O. Each ADUC object maps to PROV concepts, while ADUC adds exact source binding, epistemic state, execution evidence, disclosure state, and reproducibility gates required by AI consumers.

## 2. Top-level profile

```json
{
  "profileVersion": "0.1",
  "bundleId": "urn:aduc:provenance:example",
  "evaluationAt": "2026-07-13T12:10:00Z",
  "disclosure": {},
  "entities": [],
  "agents": [],
  "activities": [],
  "derivations": [],
  "invalidations": []
}
```

## 3. Entity

An entity is a fixed artifact or claim state.

```json
{
  "entityId": "urn:artifact:normalized-temperature",
  "entityType": "urn:aduc:artifact:Observation",
  "contentHash": "sha256:...",
  "sourceBinding": "urn:aduc:binding:normalized-temperature",
  "lifecycleState": "active"
}
```

### Required

- absolute IRI `entityId`;
- absolute IRI `entityType`;
- `sha256:` content hash for material digital artifacts;
- absolute IRI `sourceBinding` or an explicitly embedded evidence entity;
- `lifecycleState` equal to `active` or `deprecated`.

A collection entity may list members. Omitted members require bundle disclosure `partial`, `redacted`, or `unknown`.

## 4. Agent

```json
{
  "agentId": "urn:software:aduc-units",
  "agentType": "softwareAgent",
  "name": "aduc_units",
  "version": "0.1.0",
  "buildDigest": "sha256:...",
  "publisher": "urn:org:aduc"
}
```

Supported types:

```text
person
organization
softwareAgent
modelAgent
```

Software and model agents used by deterministic or replayable activities require immutable version/build evidence.

## 5. Activity

```json
{
  "activityId": "urn:activity:convert-temperature",
  "activityType": "unitConversion",
  "method": "urn:aduc:method:qudt-affine-conversion",
  "startedAt": "2026-07-13T12:00:01Z",
  "endedAt": "2026-07-13T12:00:02Z",
  "executionMode": "deterministic",
  "lineageState": "observed",
  "authorityLevel": "verified",
  "assertedBy": "urn:org:aduc",
  "evidence": ["urn:evidence:conversion-log"],
  "associatedAgents": [
    {"agentId": "urn:software:aduc-units", "role": "executor"}
  ],
  "used": [
    {"entityId": "urn:artifact:temperature-c", "role": "input"}
  ],
  "generated": [
    {"entityId": "urn:artifact:temperature-f", "role": "output"}
  ],
  "execution": {
    "softwareAgent": "urn:software:aduc-units",
    "environmentDigest": "sha256:...",
    "parametersDigest": "sha256:..."
  },
  "reproducibilityClaim": "deterministic"
}
```

### Activity types

The profile is extensible. Reference types include:

```text
parse
unitConversion
temporalResolution
identityLink
comparison
aggregation
manualReview
modelInference
invalidation
```

### Authority

- observed activity: `reviewed`, `verified`, or `canonical`;
- attested activity: `reviewed`, `verified`, or `canonical`, with attestation evidence;
- inferred activity: `inferred`, confidence, and confidence method;
- partial/redacted activity: any compatible authority, but no deterministic claim.

## 6. Associated agents and roles

Every transformation activity requires at least one responsible agent association.

Roles are IRIs or stable profile tokens. Reference roles:

```text
executor
reviewer
publisher
operator
model
attestor
```

Delegation uses a separate association or PROV `actedOnBehalfOf` mapping and must not erase the executing agent.

## 7. Usage and generation

`used` and `generated` reference existing entities.

- every material transformation uses at least one entity;
- every material transformation generates at least one entity;
- one immutable entity has at most one generating activity;
- a retry generates a distinct entity, even when content hashes match;
- invalidation-only activity may omit generated entities.

## 8. Execution evidence

### Automated deterministic activity

Required:

```text
softwareAgent
software version
build digest
environment digest
parameters digest
method
bound inputs
bound outputs
```

### Model inference

Required `aiExecution`:

```json
{
  "modelAgent": "urn:model:provider:model:snapshot",
  "modelIdentifier": "urn:model:provider:model",
  "modelVersion": "snapshot-2026-07-01",
  "provider": "urn:org:model-provider",
  "promptEntity": "urn:artifact:prompt-template",
  "parametersDigest": "sha256:...",
  "environmentDigest": "sha256:...",
  "toolConfigurationDigest": "sha256:...",
  "seed": 42
}
```

A seed is required for `replayable` when the execution method supports or depends on seeded sampling. The profile does not promise identical output for nondeterministic inference.

### Manual activity

Required:

- person or organization association;
- `manualIntervention` object;
- description or decision code;
- affected input/output entities;
- evidence.

## 9. Derivation

```json
{
  "derivationId": "urn:derivation:c-to-f",
  "kind": "conversion",
  "usedEntity": "urn:artifact:temperature-c",
  "generatedEntity": "urn:artifact:temperature-f",
  "activityId": "urn:activity:convert-temperature",
  "authorityLevel": "verified",
  "assertedBy": "urn:org:aduc",
  "evidence": ["urn:evidence:conversion-log"]
}
```

The activity must actually use and generate the declared endpoints.

## 10. Invalidation

```json
{
  "invalidationId": "urn:invalidation:old-result",
  "entityId": "urn:artifact:old-result",
  "activityId": "urn:activity:retract-old-result",
  "invalidatedAt": "2026-07-13T12:20:00Z",
  "reason": "superseded",
  "authorityLevel": "canonical",
  "assertedBy": "urn:org:publisher",
  "evidence": ["urn:evidence:retraction"]
}
```

The event cannot precede generation. The original entity and lineage remain addressable.

## 11. Disclosure

```json
{
  "disclosureState": "redacted",
  "redactedSegments": ["agent:operator"],
  "missingSegments": [],
  "redactionPolicy": "urn:policy:employee-privacy"
}
```

Rules:

- `complete`: both segment arrays empty;
- `partial`: `missingSegments` non-empty;
- `redacted`: `redactedSegments` non-empty and policy present;
- `unknown`: completeness cannot be established.

## 12. Reproducibility

### Deterministic

A deterministic claim passes only when:

- execution mode is deterministic;
- lineage state is observed or attested;
- disclosure is complete;
- all inputs and outputs are hashed;
- software version and build are pinned;
- environment and parameters are hashed;
- no material manual or redacted segment exists;
- activity is active and clear.

### Replayable

A replayable claim passes only when:

- model/software snapshot is pinned;
- prompt/template entity is hashed;
- parameters and environment are hashed;
- tools/configuration are pinned when used;
- seed is recorded when applicable;
- disclosure is complete;
- identical output is not claimed.

### Not reproducible

Use when material evidence is unavailable, redacted, manual, unstable, or externally inaccessible.

## 13. Graph validation

The evaluator constructs dependency edges:

```text
used entity → activity
activity → generated entity
used entity → generated entity (derivation)
```

The graph must be acyclic.

## 14. Existing ADUC reference chain

The official end-to-end reference must trace:

1. raw source bytes;
2. parsed observation;
3. converted quantity;
4. resolved timestamp;
5. identity-qualified observation;
6. comparison result.

Each output becomes the next activity's bound input.

## 15. Consumer decisions

The reference evaluator returns:

```text
valid
traceable
reproducibility
disclosureState
errors
warnings
```

`valid: true` means the profile is internally conformant. It does not prove that a historical claim is true.

## 16. Stable error families

See ADR-0010. Implementations may add detail codes but must preserve the family meaning.

## 17. Out of scope

- universal workflow orchestration;
- storage or transport protocol;
- complete software supply-chain attestation;
- legal proof of authorship;
- secret disclosure;
- full uncertainty and policy profiles;
- the full-Core JSON Schema.
