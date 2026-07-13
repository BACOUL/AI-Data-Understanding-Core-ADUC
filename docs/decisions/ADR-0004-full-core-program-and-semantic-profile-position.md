# ADR-0004: Full-Core Program and Position of the Existing Semantic Mapping Profile

- Status: Accepted
- Date: 2026-07-13
- Decision owner: Principal maintainer

## Context

The repository began from a broad objective: allow data to describe its structure, semantics, identity, context, provenance, uncertainty, relations, and usage policy to AI systems.

Early research showed that many individual capabilities already exist across JSON-LD/RDF, Croissant, PROV-O, DQV, ODRL, JSON Schema, OpenAPI, CloudEvents, MCP, and related standards. To avoid duplicating them, implementation work narrowed to a semantic-mapping and conformance profile.

That narrower work produced useful, validated artifacts:

- immutable semantic mapping assertions;
- epistemic status and confidence rules;
- schema fixtures;
- CLI validation;
- semantic conflict checks;
- comparison behavior;
- JSON-LD/RDF representation;
- a provider-neutral multi-model harness.

The maintainer has now confirmed that the official project remains the broader AI Data Understanding Core program. The narrow mapping profile must therefore be preserved without being mistaken for the complete final product.

## Decision

ADUC is defined as a full data-understanding contract with the following candidate Core blocks:

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

The current semantic-mapping profile is retained as:

> the first implemented experimental profile of the `semantics` block and its consumer-conformance behavior.

It is not renamed as the entire ADUC Core and does not limit the official long-term mission.

## Consequences

### Positive

- validated technical work is preserved;
- the project regains the complete maintainer-approved vision;
- existing standards can be composed rather than replaced;
- the repository can distinguish implemented features from planned Core features;
- the public website can explain the full architecture honestly;
- future schema work has a clear migration target.

### Negative

- the current mapping-profile schema is no longer sufficient to claim full Core conformance;
- documentation and status files must distinguish partial implementation from complete specification;
- future migration or compatibility tooling may be required;
- several normative decisions must be reopened for units, time, identity, policy, and the complete epistemic lifecycle.

## Required rules

1. `spec/ADUC_CORE_SPEC_0_1.md` is the authoritative full-Core working draft.
2. Existing mapping-profile artifacts remain supported experimental work.
3. No release may claim complete ADUC Core conformance until the full-Core schema and conformance suite exist.
4. New implementation work follows the official construction order:

```text
Core
Schema
Validator
Examples
JSON/CSV compiler
Multi-model demonstration
Extensions
Anticipation engine
```

5. The anticipation engine and TimeProofs remain separate projects.
6. The public name ADUC remains provisional.
7. The first public website is English-only and must present current limitations explicitly.

## Rejected alternatives

### Reject the broad Core and keep only the mapping profile

Rejected because it no longer matches the maintainer-approved product vision and would leave structure, units, time, identity, provenance, uncertainty, relations, and policy fragmented across separate integrations.

### Delete the mapping-profile work and restart

Rejected because the work is tested, useful, and directly applicable to the `semantics` block.

### Present the mapping profile as the completed Core

Rejected because it would overstate current capability and contradict the intended reference demonstration involving units, time, and identity uncertainty.

## Follow-up decisions required

- ADR: complete epistemic lifecycle;
- ADR: unit identifiers and conversions;
- ADR: temporal semantics and alignment;
- ADR: entity identity and equivalence;
- ADR: structural source profiles;
- ADR: policy representation;
- ADR: migration from mapping-profile documents to the full Core envelope.
