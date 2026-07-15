# ADR-0004: Full-Core Program and Position of the Existing Semantic Mapping Profile

- Status: Accepted
- Date: 2026-07-13
- Decision owner: Principal maintainer
- Supersedes: ADR-0002 for global project scope only
- Amended by: ADR-0004A

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

## Decision precedence

This ADR supersedes ADR-0002 only for the global project definition and permanent scope.

ADR-0002 remains authoritative for the semantic-mapping profile and for its preserved rules concerning mapping lifecycle, authority, evidence, method-bound confidence, uncertainty, contestability, deterministic consumer behavior, hidden provider-specific mappings, independent-consumer testing and stop/pivot conditions.

ADR-0004A records the complete reconciliation, source horizons and structure-module boundary. Where ADR-0002 describes ADUC as permanently limited to the narrow profile or globally rejects the broader Core, this ADR and ADR-0004A govern.

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

JSON and CSV remain the first bounded implementation and interoperability proof. They are not the permanent source-category limit of ADUC. Future source profiles remain gated and are documented in `docs/project/SOURCE_AND_EXTENSION_HORIZONS.md`.

The `structure` module provides stable Core objects, local references and exact bindings required by other modules. It composes and references complete external source descriptions; it does not replace JSON Schema, Croissant, CSVW, OpenAPI, SQL catalogs or other maintained structural standards.

## Consequences

### Positive

- validated technical work is preserved;
- the project regains the complete maintainer-approved vision;
- existing standards can be composed rather than replaced;
- the repository can distinguish implemented features from planned Core features;
- the public website can explain the full architecture honestly;
- future schema work has a clear migration target;
- JSON/CSV is explicitly the first proof boundary rather than the permanent project limit;
- API, database, live-data, document/media, scientific-data and agent-memory work can be planned as gated future profiles without expanding the Core prematurely.

### Negative

- the current mapping-profile schema is no longer sufficient to claim full Core conformance;
- documentation and status files must distinguish partial implementation from complete specification;
- future migration or compatibility tooling may be required;
- several normative decisions must be reopened for units, time, identity, policy, and the complete epistemic lifecycle;
- readers must understand that ADR-0002 is partially superseded rather than entirely obsolete.

## Required rules

1. `spec/ADUC_CORE_SPEC_0_1.md` is the authoritative full-Core working draft.
2. Existing mapping-profile artifacts remain supported experimental work.
3. ADR-0002 remains applicable only within the preserved mapping-profile and cross-cutting safety scope described above.
4. No release may claim complete ADUC Core conformance until the full-Core schema and conformance suite exist.
5. New implementation work follows the official construction order:

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

6. Future source categories require separate accepted profiles or extensions and do not become active merely because they are named in the long-term horizon.
7. The anticipation engine and TimeProofs remain separate projects.
8. The public name ADUC remains provisional.
9. The first public website is English-only and must present current limitations explicitly.
10. `docs/roadmap/NEXT_ACTION.md` remains the sole active-task authority.

## Rejected alternatives

### Reject the broad Core and keep only the mapping profile

Rejected because it no longer matches the maintainer-approved product vision and would leave structure, units, time, identity, provenance, uncertainty, relations, and policy fragmented across separate integrations.

### Delete the mapping-profile work and restart

Rejected because the work is tested, useful, and directly applicable to the `semantics` block.

### Present the mapping profile as the completed Core

Rejected because it would overstate current capability and contradict the intended reference demonstration involving units, time, and identity uncertainty.

### Implement every source category directly in Core

Rejected because source-specific structure and transport belong in maintained external standards, profiles or declared extensions. The Core must remain small, source-category-independent and provider-neutral.

## Follow-up decisions required

Completed follow-up decisions include:

- complete epistemic lifecycle;
- unit identifiers and conversions;
- temporal semantics and alignment;
- entity identity and equivalence;
- structural source binding;
- provenance, uncertainty, relation and policy representation;
- migration from mapping-profile documents to the full Core envelope.

Future source-category profiles remain gated by the Core value and interoperability proof and by separate scope, compatibility, privacy, security and conformance decisions.
