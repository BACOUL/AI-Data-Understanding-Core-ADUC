# Next Action

## Single active task

Build the unified full-Core validator and deterministic comparator on top of the accepted modular schema family and existing domain evaluators.

Create or update:

```text
docs/architecture/CORE_VALIDATION_PIPELINE_0_1.md
docs/decisions/ADR-0016-unified-core-validation-and-comparison.md
tools/aduc_validate.py
tools/aduc_compare.py
tests/core_validator/
tests/core_comparator/
examples/core/comparison/
docs/errors/CORE_ERROR_CATALOGUE_0_1.md
```

## Objective

Provide one local interface that validates a complete ADUC contract through JSON syntax, Draft 2020-12 schemas, object-model invariants and every applicable accepted domain rule, then compares two valid contracts without hiding unknown, incompatible, contested, deprecated or prohibited dimensions.

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
ADR-0015  official modular Core JSON Schema family
```

The unified tools must orchestrate these accepted components rather than replace them with weaker duplicate logic.

## Required validation pipeline

```text
JSON syntax
    ↓
Core JSON Schema family
    ↓
identifier and reference integrity
    ↓
module ownership and dependency checks
    ↓
domain-profile evaluators
    ↓
cross-module consistency checks
    ↓
stable report and exit status
```

The report must preserve schema failures, unresolved references, authority, confidence, uncertainty, conflict, lifecycle, provenance gaps and policy outcomes as distinct facts.

## Required comparator behavior

The comparator must report, by dimension:

```text
equivalent
convertible
compatible
incompatible
unknown
contested
deprecated
prohibited
requiresHumanReview
```

It must not:

- equate fields from labels alone;
- convert units without accepted dimensional rules;
- align time without timezone evidence;
- merge probable identities as exact;
- remove uncertainty during conversion;
- invent relation closure or causality;
- treat missing policy as permission;
- compare invalid contracts as if they were trusted inputs.

## Required implementation work

1. define one stable Core error catalogue without renumbering existing domain errors;
2. orchestrate the schema validator and ADR-0014 architecture checker;
3. call applicable unit, temporal, identity, provenance, uncertainty, relation and policy evaluators;
4. prevent duplicate or contradictory diagnostics from hiding the primary cause;
5. expose human-readable and JSON reports;
6. provide deterministic exit codes for valid, invalid and review-required results;
7. compare two complete contracts field by field and dimension by dimension;
8. include complete compatible, convertible, incompatible and unresolved comparison fixtures;
9. integrate all validation and comparison paths into CI;
10. document which checks are structural, semantic, epistemic or policy-dependent.

## Scope boundary

Do not implement the JSON/CSV compiler, review UI, registry service, MCP adapter, extensions, anticipation engine, production access control, value benchmark or external multi-model proof in this task.

## Completion test

An independent implementer must be able to:

1. validate a complete contract with one command;
2. receive stable JSON paths and error codes from every validation layer;
3. distinguish invalid from valid-but-review-required contracts;
4. compare two complete contracts without private mappings;
5. reproduce every official comparison result locally;
6. verify that no accepted domain safeguard was weakened by orchestration.

## Next action after acceptance

Define and implement the migration path from the standalone semantic-mapping profile into complete Core contracts, then prepare the JSON/CSV compiler only after the adoption and review-tax gates are ready to run.

## Cross-cutting adoption constraint

[`ADOPTION_AND_VALUE_VALIDATION.md`](ADOPTION_AND_VALUE_VALIDATION.md) remains mandatory. Do not implement the JSON/CSV compiler now.
