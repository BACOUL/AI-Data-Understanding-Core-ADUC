# ADR-0010 — Provenance and Transformation Lineage

- Status: accepted
- Date: 2026-07-13
- Issue: #37
- Pull request: #38
- Decision owners: ADUC maintainers

## Context

Semantic compatibility, unit conversion, temporal alignment, and entity resolution are not trustworthy by themselves when a consumer cannot determine where a result came from, which inputs were used, who or what performed each transformation, and whether the result can be reproduced.

ADUC must preserve this lineage without creating a competing provenance ontology. W3C PROV already defines interoperable concepts for entities, activities, agents, generation, usage, derivation, attribution, association, delegation, invalidation, plans, roles, and qualified relations.

## Decision

### 1. Reuse PROV-O

ADUC maps directly to established PROV concepts, including:

```text
prov:Entity
prov:Activity
prov:Agent
prov:SoftwareAgent
prov:Person
prov:Organization
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
prov:Plan
prov:Role
prov:Bundle
```

The ADUC profile adds constrained JSON fields and deterministic consumer rules; it does not replace the PROV ontology.

### 2. Separate record families

ADUC distinguishes:

```text
artifact/entity
transformation/activity
responsible agent
software or model execution evidence
derivation assertion
invalidation event
disclosure state
reproducibility claim
```

A prose statement that one file came from another is not sufficient lineage.

### 3. Bind material artifacts

Every material digital input and output requires:

```text
entityId
entityType
contentHash
sourceBinding
lifecycleState
```

Version 0.1 uses `sha256:<64 lowercase hexadecimal characters>`. Mutable URLs, filenames, labels, model names, and version strings are not integrity evidence.

### 4. Activity records

Every material activity records:

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
authority and evidence
conflict and lifecycle state
```

A transformation uses at least one bound input and generates at least one bound output. An invalidation-only activity may omit generated entities.

### 5. Execution modes

| Mode | Meaning |
|---|---|
| `deterministic` | The same pinned inputs and execution evidence are expected to produce the same output. |
| `nondeterministic` | Output may vary even when replay evidence is supplied. |
| `manual` | A human materially created, changed, selected, or approved the result. |
| `externalAttestation` | An identified third party attests to lineage not directly observed by the recorder. |
| `reconstructed` | The lineage was inferred after the event. |

### 6. Lineage states

| State | Meaning |
|---|---|
| `observed` | Captured by the executing system while the activity occurred. |
| `attested` | Asserted by an identified external authority with evidence. |
| `inferred` | Reconstructed algorithmically or analytically. |
| `partial` | Material segments are missing. |
| `redacted` | Material segments exist but are intentionally undisclosed. |

Lineage state is separate from epistemic authority. Inferred lineage uses `authorityLevel: inferred`, confidence, a confidence method, and cannot claim completeness.

### 7. Automated execution evidence

A deterministic or replayable automated activity identifies:

```text
software agent
software name and version
build or immutable artifact digest
environment digest
parameters digest
method identifier
```

A software name alone is insufficient.

### 8. AI execution evidence

A `modelInference` activity additionally records:

```text
model identifier
model version or immutable snapshot
provider or publisher
prompt or template entity with content hash
parameters digest
environment digest
tool configuration digest when tools are used
seed when the replay claim depends on it
```

A model family name or prompt text alone is not sufficient AI provenance.

### 9. Manual intervention

A material human decision or edit is represented as a `manual` activity associated with a person or responsible organization. It identifies the affected input, output, decision, and evidence. A later automated activity must not hide the manual step.

### 10. Reproducibility claims

| Claim | Requirement |
|---|---|
| `notClaimed` | No reproduction promise. |
| `deterministic` | Deterministic mode, pinned inputs/outputs/software/build/environment/parameters, complete disclosure, and no material hidden step. |
| `replayable` | Pinned model, prompt, environment, parameters, tools, and seed where applicable; identical output is not guaranteed. |
| `notReproducible` | Material evidence is unavailable, unstable, manual, missing, or redacted. |

`replayable` is not equivalent to deterministic reproduction.

### 11. Derivations

Supported reference derivation kinds are:

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

When a derivation names an activity, that activity must use the upstream entity and generate the downstream entity.

### 12. Graph integrity

Consumers reject:

- provenance cycles;
- activity end before start;
- use of an entity after invalidation unless an explicit historical-use rule permits it;
- one immutable output generated by multiple activities;
- unknown endpoints;
- derivation/activity disagreement;
- duplicate identifiers;
- malformed or broken content hashes.

Retries are separate activities. Branches generate separate output entities. Aggregations enumerate material inputs or explicitly declare partial lineage.

### 13. Revision and invalidation

A revision is a new entity linked with `prov:wasRevisionOf`. Replacing an existing output hash in place is forbidden.

Invalidation creates an immutable event identifying the affected entity, responsible activity, time, reason, evidence, and authority. Earlier provenance remains available.

### 14. Disclosure

A bundle declares:

```text
disclosureState: complete | partial | redacted | unknown
missingSegments
redactedSegments
redactionPolicy
```

`complete` forbids missing or redacted material segments. Redaction is not interpreted as absence. Complete reproducibility cannot be claimed when required lineage is missing or redacted.

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

Contested or deprecated lineage remains visible and blocks claims that depend on it.

### 16. Integration with existing ADUC profiles

The reference chain is:

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

Every stage binds its exact input and output and reuses ADR-0006, ADR-0007, ADR-0008, and ADR-0009 rather than duplicating their rules.

### 17. Privacy

Provenance may be redacted or pseudonymized, but the disclosure state and policy reference remain visible. Protected identifiers or digests may replace private values. A bundle cannot claim complete reproducibility when hidden information is materially required.

## Stable error families

```text
ADUC-PROV-001   malformed or duplicate provenance object
ADUC-PROV-002   missing or invalid entity binding/hash
ADUC-PROV-003   missing agent, role, method, or evidence
ADUC-PROV-004   invalid activity time or ordering
ADUC-PROV-005   broken use/generation/derivation reference
ADUC-PROV-006   provenance cycle
ADUC-PROV-007   conflicting or duplicate generation
ADUC-PROV-008   invalid invalidation or revision lifecycle
ADUC-PROV-009   lineage state and authority are incompatible
ADUC-REPRO-001  deterministic claim lacks pinned execution evidence
ADUC-REPRO-002  replay claim lacks model/seed/prompt/environment evidence
ADUC-REPRO-003  manual intervention is hidden or unbound
ADUC-REPRO-004  AI provenance is insufficient
ADUC-DISC-001   completeness conflicts with missing or redacted lineage
ADUC-DISC-002   redaction lacks policy or protected reference
```

## Consequences

### Positive

- ADUC provenance remains interoperable with PROV-O;
- inputs and outputs are cryptographically bound;
- deterministic, replayable, manual, inferred, and attested transformations are not conflated;
- AI execution evidence is inspectable;
- missing and redacted segments remain explicit;
- cycles, impossible ordering, hidden edits, and unsupported reproduction claims are detectable.

### Costs

- tools must capture hashes, versions, roles, parameters, and environments;
- model and prompt artifacts need stable identifiers;
- complete reproducibility is intentionally difficult to claim;
- privacy-preserving provenance requires explicit disclosure metadata.

## Rejected alternatives

- **Free-text audit log only:** not machine-validatable or traversable.
- **Filenames or URLs as immutable identity:** mutable and insufficient.
- **Model name and prompt only:** omits material version, environment, tool, and parameter evidence.
- **Infer missing lineage and call it complete:** destroys epistemic distinctions.
- **Replace an output hash after correction:** destroys immutable history.
- **Hide manual review in an automated pipeline:** misrepresents responsibility and reproducibility.

## References

- W3C PROV-O Recommendation: https://www.w3.org/TR/prov-o/
- W3C PROV Data Model: https://www.w3.org/TR/prov-dm/
- W3C PROV Constraints: https://www.w3.org/TR/prov-constraints/
- OpenLineage specification: https://openlineage.io/docs/spec/

## Acceptance evidence

- seven valid provenance reference cases;
- twenty required invalid mutation fixtures;
- eight deterministic evaluator and CLI tests;
- the main case traces source parsing, unit conversion, temporal resolution, identity linking, and comparison;
- GitHub Actions passed the provenance suite and every pre-existing validation suite.

## Follow-up

1. define the complete uncertainty and quality profile;
2. define general relation and policy boundaries;
3. freeze the normative full-Core object model;
4. implement the full-Core JSON Schema family;
5. unify comparison across semantics, units, time, identity, provenance, uncertainty, and policy.
