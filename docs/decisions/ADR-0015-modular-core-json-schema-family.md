# ADR-0015 — Modular Core JSON Schema Family

- Status: accepted
- Date: 2026-07-14
- Issue: #49
- Pull request: #50
- Decision owners: ADUC maintainers

## Context

ADR-0014 froze the ten-block Core object model, ownership boundaries, cardinalities and module dependency graph. The repository still retained an historical bootstrap schema that required the wrong minimum blocks and left most modules unconstrained.

A conforming schema family must enforce every structural rule expressible in JSON Schema while preserving the complementary architecture checks required for identifiers, references, ownership and graph semantics.

## Decision

### Draft and local resolution

The official experimental family uses JSON Schema Draft 2020-12. Every schema has a stable experimental `$id` under the reserved `.example` domain:

```text
https://aduc.example/schema/0.1/
```

All operational `$ref` values are local and relative. Validation does not retrieve remote contexts, schemas or vocabularies.

### Schema family

The family is exactly the list frozen in `spec/core-module-manifest.json`:

```text
aduc-core.schema.json
aduc-envelope.schema.json
aduc-metadata.schema.json
resource.schema.json
structure.schema.json
semantics.schema.json
identity.schema.json
context.schema.json
provenance.schema.json
uncertainty.schema.json
relations.schema.json
policy.schema.json
qualification.schema.json
extension.schema.json
```

`aduc-core.schema.json` is the root. `aduc-envelope.schema.json` owns the ten reserved top-level blocks and the minimum `aduc + resource + structure` contract.

### Closed Core objects

Core objects use explicit properties and reject unknown properties. Extension data is allowed only through an `extensions` object whose namespace keys are absolute IRIs outside `urn:aduc:core:`.

External standards remain referenced by IRI or identified Core references. Embedded renamed copies such as `structure.externalSchema` are rejected.

### Structural qualification

Authoritative semantic, identity, uncertainty, relation and policy assertions require explicit status, conflict and lifecycle fields where frozen by the accepted profiles. Confidence and confidence method are mutually dependent. Measurement uncertainty remains separate from semantic confidence.

### Policy and relation safeguards

A relation has exactly one object form: `objectRef` or `literalObject`.

Executable permissions, prohibitions and duties require their controlled fields. Classification, recommendation and legal-notice rules must be non-executable. Presence of `policy` requires `provenance` according to the frozen module dependency graph.

### Complementary architecture validation

JSON Schema intentionally does not claim to enforce:

- uniqueness of identifiers across different arrays and modules;
- resolution of every `Ref` and `Refs` value;
- matching extension payload namespaces to declarations;
- one-owner rules across modules;
- graph conflicts, identity safety or relation semantics;
- target digest equality or published-history immutability.

`tools/aduc_core_validate.py` therefore performs schema validation first and then calls `tools/aduc_core_model.py` for these accepted architectural invariants.

### Stable diagnostics

The reference validator exposes JSON-path locations and stable error families such as:

```text
ADUC-SCHEMA-REQUIRED
ADUC-SCHEMA-UNKNOWN
ADUC-SCHEMA-TYPE
ADUC-SCHEMA-FORMAT
ADUC-SCHEMA-PATTERN
ADUC-SCHEMA-CONST
ADUC-SCHEMA-ONEOF
ADUC-SCHEMA-DEPENDENCY
```

These codes classify validation failures; they do not replace the domain-specific error catalogue planned for the unified validator.

## Acceptance evidence

Acceptance requires:

- all fourteen schemas passing Draft 2020-12 meta-validation;
- the complete ten-block example passing schema and architecture validation;
- at least ten complete valid fixtures;
- at least ten complete invalid fixtures rejected for documented reasons;
- local CLI validation with no remote retrieval;
- all pre-existing repository suites remaining green.

## Consequences

The object model now has an executable structural contract. Independent implementations can validate the same envelope and module shapes without inventing fields or architecture.

Schema validity still does not prove that an assertion is true, authoritative, legally permitted or safe for a requested operation. Those conclusions remain governed by the accepted domain profiles and complementary evaluators.

## Follow-up

Build the unified full-Core validator and comparator on top of this schema family, then consolidate the existing domain-specific diagnostics without weakening their safety rules.
