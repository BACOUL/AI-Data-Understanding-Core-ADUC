# Next Action

## Single active task

Implement the official modular ADUC Core JSON Schema family from the frozen object model and module manifest.

Create:

```text
schema/aduc-core.schema.json
schema/aduc-envelope.schema.json
schema/aduc-metadata.schema.json
schema/resource.schema.json
schema/structure.schema.json
schema/semantics.schema.json
schema/identity.schema.json
schema/context.schema.json
schema/provenance.schema.json
schema/uncertainty.schema.json
schema/relations.schema.json
schema/policy.schema.json
schema/qualification.schema.json
schema/extension.schema.json
examples/core/valid/
examples/core/invalid/
tests/core_schema/
tools/aduc_core_validate.py
```

## Objective

Translate ADR-0014, `spec/ADUC_CORE_MODEL_0_1.md`, `spec/core-module-manifest.json`, the accepted domain profiles and the complete model example into a Draft 2020-12 schema family that enforces every structural rule possible in JSON Schema without revisiting architecture.

## Completed dependencies

```text
ADR-0005  epistemic lifecycle
ADR-0006  source description and immutable binding
ADR-0007  units and deterministic conversion
ADR-0008  temporal semantics and timezone alignment
ADR-0009  entity identity and safe equivalence
ADR-0010  provenance and transformation lineage
ADR-0011  uncertainty and data quality
ADR-0012  general relation semantics
ADR-0013  policy and permitted-use conditions
ADR-0014  normative Core object model and module boundaries
```

The schema family must implement these decisions rather than renaming, weakening or duplicating them.

## Required decisions already frozen

The schema task must preserve:

1. exactly ten reserved top-level Core blocks;
2. required minimum `aduc + resource + structure`;
3. singular objects for every module except the `relations` array;
4. stable absolute-IRI identifiers;
5. deterministic `Ref` / `Refs` reference convention;
6. one owner for each normative fact;
7. shared qualification fields without competing copies;
8. external standards referenced rather than embedded as ADUC replacements;
9. declared extension namespaces and collision prevention;
10. immutable publication and explicit replacement;
11. the module dependency graph in `core-module-manifest.json`;
12. migration compatibility with the existing semantic-mapping profile.

## Required implementation work

1. build the root schema and modular `$ref` graph;
2. define reusable identifier, digest, timestamp, qualification and extension definitions;
3. enforce module types, required fields, cardinalities and closed Core objects;
4. enforce profile-controlled enums where already accepted;
5. create at least ten complete valid Core examples;
6. create at least ten intentionally invalid complete Core examples;
7. implement a local validator with stable user-facing error paths;
8. document constraints that JSON Schema cannot enforce alone, especially cross-object uniqueness and reference resolution;
9. keep the architectural checker as a complementary invariant test;
10. integrate every schema and fixture into CI.

## Required invalid coverage

The schema fixtures must reject at least:

- missing `aduc`, `resource` or `structure`;
- unknown top-level Core blocks;
- a repeated singular module;
- malformed absolute identifiers;
- malformed SHA-256 digests;
- invalid module cardinality;
- missing required assertion qualification;
- undeclared or Core-colliding extension namespaces where structurally detectable;
- policy classification made executable;
- incompatible relation endpoint forms;
- embedded external schema copies where the Core requires a reference;
- unsafe migration fields that bypass the frozen modules.

Cross-reference resolution, duplicate identifiers and graph-level conflicts may require the reference validator in addition to JSON Schema and must be documented explicitly.

## Scope boundary

Do not build the JSON/CSV compiler, review UI, registry service, MCP adapter, extensions, anticipation engine, production access control, value benchmark or external multi-model proof in this task.

## Completion test

An independent implementer must be able to:

1. validate the complete example locally;
2. validate every official valid fixture;
3. reject every official invalid fixture for the documented reason;
4. trace each schema module to its owning Core module;
5. identify every rule that requires the complementary reference validator;
6. use the schema family without remote context retrieval or provider-specific behavior.

## Next action after acceptance

Build the unified full-Core validator and comparator on top of the accepted schema family and complete fixtures.

## Cross-cutting adoption constraint

[`ADOPTION_AND_VALUE_VALIDATION.md`](ADOPTION_AND_VALUE_VALIDATION.md) remains mandatory. Do not implement the JSON/CSV compiler now.