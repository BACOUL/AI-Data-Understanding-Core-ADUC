# ADR-0004A: Full-Core Scope Reconciliation

- Status: Proposed amendment
- Date: 2026-07-15
- Issue: #66
- Amends: ADR-0004
- Partially supersedes: ADR-0002

## Context

ADR-0002 was accepted after Gate 0 research narrowed the first implementation experiment to a semantic-mapping and conformance profile over established standards. It rejected the broad Core as the immediate normative implementation target because the individual representational categories already existed across maintained standards.

ADR-0004 later restored the maintainer-approved broader ADUC mission and defined the semantic-mapping profile as the first implemented subset of the complete ten-block Core.

Both ADRs remain discoverable as accepted decisions. Without an explicit precedence rule, a reader can reasonably conclude that ADUC has two incompatible official definitions:

- a narrow semantic-mapping profile only; or
- the broader AI Data Understanding Core.

The repository must preserve the useful Gate 0 constraints without allowing the earlier experimental scope to override the later full-Core decision.

## Decision

### 1. Global project scope

ADR-0004 governs the global project scope.

ADUC is the broader, model-independent data-understanding Core with the ten reserved modules:

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

ADR-0002 is superseded only where it states or implies that the semantic-mapping profile is the complete or permanent scope of ADUC, that the broad Core is globally rejected, or that the ADUC name necessarily overstates the official project direction.

### 2. Decisions preserved from ADR-0002

ADR-0002 remains authoritative for the standalone semantic-mapping profile and for cross-cutting safeguards that continue to apply to the full Core, including:

- reuse of maintained standards rather than duplication;
- portable local-reference-to-semantic-target mappings;
- explicit authority and epistemic state;
- evidence and method-bound confidence for inferred mappings;
- no silent promotion from inferred to reviewed, verified or canonical;
- preservation of unknown, contested and unresolved mappings;
- deterministic consumer behavior;
- prohibition of hidden provider-specific mappings in conformance evidence;
- independent-consumer testing;
- stop or pivot rules when direct use of an existing standard is simpler or equivalent.

The semantic-mapping profile remains a supported experimental input and migration source for the `semantics` module.

### 3. Standards boundary

The full Core does not reverse the Gate 0 finding that established standards already own many representational domains.

ADUC must compose and qualify them rather than duplicate them. In particular:

- JSON Schema, Croissant, CSVW and OpenAPI retain ownership of their complete structural descriptions;
- JSON-LD, RDF, SKOS and OWL retain ownership of general semantic identifiers and graph semantics;
- PROV-O retains ownership of general provenance vocabulary;
- DQV retains ownership of general data-quality vocabulary;
- ODRL retains ownership of general permissions, prohibitions and duties;
- QUDT and UCUM retain ownership of maintained quantity and unit identifiers;
- CloudEvents and SOSA/SSN remain external foundations for event and observation profiles;
- MCP remains an optional access and delivery channel, not a Core dependency.

ADUC adds exact source binding, stable cross-module references, qualification, lifecycle, conflict preservation, uncertainty separation and deterministic safety behavior for compatible consumers.

### 4. Source horizons

The long-term Core mission is source-category-independent, while the first implementation proof remains limited to JSON and CSV.

The authoritative distinction between long-term mission, initial proof boundary and gated future profiles is recorded in:

```text
docs/project/SOURCE_AND_EXTENSION_HORIZONS.md
```

Future profiles do not become active work merely because they are named there.

### 5. Structure-module boundary

The Core `structure` module is a normalized interoperability index and stable binding layer. It provides the local objects and references required by other Core modules and may expose minimum primitive shape and key facts needed for deterministic processing.

It must not become a renamed replacement for complete source-description standards. When an external structural description exists, ADUC references it and binds Core assertions to stable structural objects derived from that exact source or description version.

### 6. Technical order

This amendment changes no schema, validator, comparator, formatter, migration or conformance behavior.

It does not authorize the compiler, SDK packages, review UI, hosted service, MCP adapter, source extensions, Situation & Action extension, anticipation engine or external multi-model proof ahead of their accepted gates.

`docs/roadmap/NEXT_ACTION.md` remains unchanged and continues to define the provider-neutral full-Core conformance runner as the sole active technical task.

## Consequences

### Positive

- the repository has one unambiguous global product direction;
- the original full-Core vision is preserved;
- the narrow semantic-mapping work remains valid and reusable;
- the Gate 0 standards boundary remains enforceable;
- JSON/CSV is clearly the first proof boundary rather than the permanent project limit;
- future source categories are visible without creating out-of-order implementation pressure.

### Negative

- readers must understand that ADR-0002 is only partially superseded rather than fully obsolete;
- future documentation must distinguish Core mission, implemented source support and planned extensions precisely;
- source-profile work will require separate ADRs, threat models, compatibility rules and conformance tests.

## Rejected alternatives

### Fully supersede ADR-0002

Rejected because its mapping lifecycle, evidence, authority, consumer-safety and stop/pivot decisions remain central to ADUC.

### Return to the narrow mapping profile as the entire project

Rejected because it does not match the maintainer-approved full-Core mission and would leave the other understanding dimensions fragmented across provider-specific integration layers.

### Implement every source category in the Core

Rejected because the Core must remain source-category-independent and small. Source-specific details belong in maintained external descriptions, profiles or declared extensions.

## Acceptance gate

This amendment may move from Proposed to Accepted only after:

1. manual maintainer review;
2. roadmap regression tests pass;
3. the active `NEXT_ACTION.md` remains unchanged;
4. no normative engine or schema behavior changes;
5. the PR explicitly states that it must not merge automatically.
