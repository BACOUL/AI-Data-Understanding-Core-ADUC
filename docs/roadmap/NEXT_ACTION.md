# Next Action

## Single active task

Freeze the normative ADUC Core object model and modular boundaries before implementing the official JSON Schema family.

Create or update:

```text
docs/decisions/ADR-0014-normative-core-object-model.md
spec/ADUC_CORE_MODEL_0_1.md
spec/ADUC_CORE_SPEC_0_1.md
docs/architecture/CORE_MODULE_BOUNDARIES_0_1.md
examples/core/complete-model.example.json
```

## Objective

Turn the accepted domain profiles into one coherent Core model whose objects, ownership boundaries, references, cardinalities, extension points, lifecycle behavior, and compatibility rules are precise enough for an independent implementer to build the schema family without inventing architecture.

The model must define the normative relationship between:

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
```

The object model must compose these accepted decisions rather than restating or weakening them.

## Required decisions

1. confirm the ten top-level Core blocks and whether each is required, optional, singular, or repeated;
2. define the contract identity, version, conformance, publication, replacement, and extension mechanism;
3. define which module owns every normative property and forbid duplicate competing representations;
4. define stable object identifiers and deterministic cross-module references;
5. define the minimum resource and structural binding needed before semantic assertions can be consumed;
6. define how status, authority, evidence, provenance, uncertainty, conflict, and lifecycle qualify assertions across modules;
7. define how external standards are referenced without embedding complete copies of JSON Schema, Croissant, PROV-O, DQV, ODRL, QUDT, UCUM, SKOS, or OWL;
8. define JSON and JSON-LD representation boundaries;
9. define extension namespaces, discovery, collision prevention, and unsupported-extension behavior;
10. define module versioning, replacement, migration, and backward-compatibility rules;
11. define the migration boundary from the existing semantic-mapping profile;
12. define the modular schema family and dependency graph without implementing the schemas yet;
13. update the complete example so every accepted Core profile has a coherent place;
14. define deterministic behavior for absent, unknown, incomplete, contested, deprecated, prohibited, or unsupported information.

## Required counterexamples

The decision must reject or block:

- the same fact represented differently in multiple Core blocks;
- local identifiers whose namespace or issuer is unknown;
- cross-module references that cannot be resolved deterministically;
- circular mandatory dependencies between modules;
- an envelope in which every block is optional and no minimum interoperable contract exists;
- hidden mappings or consumer-specific fields in the Core;
- embedding complete external standards as duplicated ADUC properties;
- inferred assertions promoted silently to reviewed, verified, or canonical status;
- measurement uncertainty reused as semantic confidence;
- probable identity represented as exact identity;
- relation semantics inferred from labels;
- descriptive policy classification represented as executable permission;
- extensions that overwrite Core terms;
- unknown extensions treated as understood;
- version replacement that rewrites published history.

## Scope boundary

Do not implement the official JSON Schema family, unified validator, comparator, compiler, review UI, registry service, MCP adapter, extensions, anticipation engine, or production access-control system in this task.

## Completion test

An independent implementer must be able to:

1. identify every normative Core object and its owning module;
2. determine required versus optional content and cardinality;
3. resolve every Core reference without private conventions;
4. map all nine accepted domain profiles into the complete envelope;
5. understand how JSON-LD, external vocabularies, versions, and extensions are represented;
6. implement modular JSON Schemas without making a new architectural decision;
7. migrate the current semantic-mapping profile without losing authority, evidence, confidence, or lifecycle information;
8. explain deterministic consumer behavior for missing, unsafe, prohibited, contested, deprecated, or unsupported information.

## Next action after acceptance

Implement the official modular full-Core JSON Schema family, followed by complete valid and invalid Core examples.

## Cross-cutting adoption constraint

[`ADOPTION_AND_VALUE_VALIDATION.md`](ADOPTION_AND_VALUE_VALIDATION.md) remains mandatory. Do not implement the JSON/CSV compiler now.
