# ADR-0010 — Provenance and Transformation Lineage

- Status: proposed
- Date: 2026-07-13
- Issue: #37
- Decision owners: ADUC maintainers

## Context

A correct semantic mapping, unit conversion, timestamp, or entity link is not sufficient if a consumer cannot determine where the result came from, which transformation produced it, which inputs were used, who or what was responsible, and whether the result can be reproduced.

ADUC must preserve lineage without creating a competing provenance ontology. The W3C PROV model already defines interoperable concepts for entities, activities, agents, generation, usage, derivation, attribution, association, delegation, invalidation, plans, roles, and qualified relations.

The ADUC contribution is a constrained AI-consumption profile that binds PROV records to exact source bytes and versions, separates observed from reconstructed lineage, records software/model execution evidence, exposes missing or redacted segments, and defines deterministic blocking rules.

## Decision

### 1. Reuse PROV-O

ADUC uses the following PROV-O concepts directly or by one-to-one profile mapping:

```text
prov:Entity
prov:Activity
prov:Agent
prov:SoftwareAgent
prov:Organization
prov:Person
prov:used
prov:wasGeneratedBy
prov:wasDerivedFrom
prov:wasAttributedTo
prov:wasAssociatedWith
prov:actedOnBehalfOf
prov:wasInformedBy
prov:hadPrimarySource
prov:wasRevisionOf
prov:wasInvalidatedBy
prov:invalidatedAtTime
prov:Plan
prov:Role
prov:Bundle
```

ADUC does not rename these concepts into an incompatible ontology. The JSON profile supplies deterministic field names and additional conformance rules.

### 2. Separate artifacts, activities, and responsibility

ADUC distinguishes:

```text
artifact/entity
transformation/activity
responsible agent
software/model execution evidence
derivation assertion
invalidation event
lineage disclosure state
reproducibility claim
```

A result cannot claim derivation merely by naming an upstream file in prose.

### 3. Bind every material artifact

Every material digital input and output must have:

```text
entityId
entityType
contentHash
sourceBinding or embedded evidence reference
lifecycle state
```

`contentHash` uses `sha256:<64 lowercase hexadecimal characters>` in v0.1.

Mutable URLs, labels, filenames, model names, or version strings are not integrity evidence.

### 4. Activity records

An activity records:

```text
activityId
activityType
method
startedAt
endedAt
executionMode
lineageState
associated agents and roles
used entities and roles
generated entities and roles
evidence
authority
lifecycle/conflict state
```

An activity must use at least one bound input and generate at least one bound output unless it is explicitly an invalidation-only activity.

### 5. Execution modes

Supported v0.1 execution modes are:

| Mode | Meaning |
|---|---|
| `deterministic` | Same bound inputs and execution evidence are expected to produce the same bound output. |
| `nondeterministic` | Output may vary; replay evidence may narrow but not erase nondeterminism. |
| `manual` | A human materially created, changed, selected, or approved the result. |
| `externalAttestation` | A third party attests to lineage not directly observed by the recorder. |
| `reconstructed` | Lineage was inferred after the event from available evidence. |

### 6. Lineage states

Supported v0.1 lineage states are:

| State | Meaning |
|---|---|
| `observed` | Recorded by the executing system while the activity occurred. |
| `attested` | Asserted by an identified external authority with evidence. |
| `inferred` | Reconstructed algorithmically or analytically. |
| `partial` | Known segments are present but material segments are missing. |
| `redacted` | Material segments exist but are intentionally undisclosed. |

Lineage state is separate from epistemic authority. `inferred` lineage must use `authorityLevel: inferred`, include confidence and an inference method, and cannot claim completeness.

### 7. Software and environment evidence

A deterministic or replayable automated activity must identify:

```text
software agent
software name
version
build or immutable artifact digest
environment digest
parameters digest
method identifier
```

A software name alone is not enough.

### 8. AI and model execution evidence

A `modelInference` activity must additionally record:

```text
model identifier
model version or immutable snapshot identifier
provider or publisher identifier
prompt/template entity with content hash
parameters digest
tool/configuration digest when tools are used
seed when a replay claim depends on it
```

A prompt string or model family name alone is not sufficient provenance.

### 9. Manual intervention

Any material human decision or edit must be represented as a `manual` activity associated with a `prov:Person` or responsible organization and must identify the affected input and output.

A later automated activity cannot hide or collapse the manual step.

### 10. Reproducibility claims

Supported claims are:

| Claim | Requirement |
|---|---|
| `notClaimed` | No reproduction promise. |
| `deterministic` | Deterministic mode, pinned inputs/outputs, pinned software/build/environment/parameters, complete lineage, no redaction. |
| `replayable` | Nondeterministic or model process with pinned model, prompt, environment, parameters, and seed where applicable; identical output is not guaranteed. |
| `notReproducible` | Known to depend on unavailable, unstable, manual, or redacted material. |

`replayable` is not equivalent to deterministic reproduction.

### 11. Derivations

A derivation links one bound entity to another and may identify the responsible activity.

Supported derivation kinds are:

```text
derivation
primarySource
revision
quotation
aggregation
normalization
conversion
resolution
comparison
```

If an activity is named, the activity must use the upstream entity and generate the downstream entity.

### 12. Ordering and graph integrity

Consumers must reject:

- provenance cycles;
- activity end before start;
- use of an entity after its invalidation unless an explicit historical-use policy permits it;
- one immutable output entity generated by multiple activities;
- missing relation endpoints;
- derivation/activity disagreement;
- duplicate IDs;
- broken or malformed content hashes.

Retries are separate activities with `attempt` and optional `parentActivity`. Branches create distinct outputs. Aggregation identifies all material inputs or explicitly declares partial lineage.

### 13. Invalidation and revision

Invalidation never deletes prior provenance. It creates an immutable event identifying:

```text
invalidated entity
responsible activity
time
reason
evidence
authority
```

A revision is a new entity linked with `prov:wasRevisionOf`; replacing a hash in place is forbidden.

### 14. Completeness, redaction, and missing lineage

A bundle declares:

```text
disclosureState: complete | partial | redacted | unknown
missingSegments
redactedSegments
redactionPolicy
```

`complete` forbids missing or redacted material segments. Redaction must not be interpreted as absence. A consumer must not claim full reproducibility when material lineage is redacted or missing.

### 15. Authority and lifecycle

Provenance assertions reuse ADR-0005:

```text
authorityLevel
assertedBy
evidence
confidence and confidenceMethod when inferred
conflictState
lifecycleState
```

Contested or deprecated material lineage remains visible and blocks claims that depend on it.

### 16. Existing ADUC profiles become provenance activities

The reference flow is:

```text
source bytes
  → parsing activity
parsed observation
  → unit conversion activity
normalized quantity
  → temporal resolution activity
normalized instant
  → identity-link activity
entity-qualified observation
  → comparison activity
comparison result
```

Every stage binds the exact input and output entity and references the accepted source, unit, time, and identity profiles.

### 17. Privacy and policy

Provenance may be redacted or pseudonymized, but the disclosure state and policy reference must remain visible. Private information is not required to be exposed merely to satisfy ADUC.

A redacted agent or parameter may be represented by a protected identifier or digest, but the bundle cannot claim complete reproducibility when the undisclosed material is necessary.

## Reference error families

```text
ADUC-PROV-001   malformed or duplicate provenance object
ADUC-PROV-002   missing or invalid entity binding/hash
ADUC-PROV-003   missing agent, role, method, or evidence
ADUC-PROV-004   invalid activity time or ordering
ADUC-PROV-005   broken use/generation/derivation reference
ADUC-PROV-006   provenance cycle
ADUC-PROV-007   conflicting or duplicate generation
ADUC-PROV-008   invalid invalidation or revision lifecycle
ADUC-PROV-009   inferred/attested lineage represented with incompatible authority
ADUC-REPRO-001  deterministic claim lacks pinned execution evidence
ADUC-REPRO-002  replay claim lacks model/seed/prompt/environment evidence
ADUC-REPRO-003  manual intervention is hidden or unbound
ADUC-REPRO-004  AI provenance is insufficient
ADUC-DISC-001   completeness claim conflicts with missing/redacted lineage
ADUC-DISC-002   material redaction lacks policy or protected reference
```

## Consequences

### Positive

- lineage is interoperable through PROV-O rather than a private ontology;
- exact inputs and outputs are cryptographically bound;
- deterministic, replayable, manual, inferred, and attested transformations are not conflated;
- AI execution provenance becomes inspectable;
- missing and redacted segments remain explicit;
- cycles, impossible ordering, hidden edits, and unsupported reproducibility claims are detectable.

### Costs

- tools must capture hashes, versions, roles, parameters, and environments;
- model and prompt artifacts need stable identifiers;
- complete reproducibility is intentionally difficult to claim;
- privacy-preserving provenance requires explicit disclosure metadata.

## Rejected alternatives

### Store only a free-text audit log

Rejected because it cannot be validated, traversed, compared, or deterministically consumed.

### Treat filenames and URLs as immutable provenance

Rejected because they can change without changing identity.

### Record only the final model name and prompt

Rejected because the model version, environment, tools, parameters, and inputs materially affect execution.

### Infer missing lineage and call it complete

Rejected because reconstructed provenance is epistemically different from observed provenance.

### Replace an output hash after correction

Rejected because it destroys the original entity and lifecycle.

### Omit manual review from an automated pipeline

Rejected because a material human decision changes responsibility and reproducibility.

## References

- W3C PROV-O Recommendation: https://www.w3.org/TR/prov-o/
- W3C PROV Data Model: https://www.w3.org/TR/prov-dm/
- W3C PROV Constraints: https://www.w3.org/TR/prov-constraints/
- OpenLineage specification: https://openlineage.io/docs/spec/

## Acceptance evidence

To be completed after CI:

- valid provenance reference cases;
- required invalid counterexamples;
- deterministic evaluator and CLI tests;
- GitHub Actions results.

## Follow-up

1. define the complete uncertainty profile;
2. define general relation and policy boundaries;
3. freeze the normative full-Core object model;
4. implement the full-Core JSON Schema family;
5. unify comparison across semantics, units, time, identity, provenance, uncertainty, and policy.
