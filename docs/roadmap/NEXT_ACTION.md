# Next Action

## Single active task

Define and implement the migration path from the standalone semantic-mapping profile into complete ADUC Core contracts.

## Objective

Provide a deterministic local migration workflow that maps the already implemented semantic-mapping profile artifacts into the accepted ten-block Core envelope without weakening ADR-0014, ADR-0015 or ADR-0016.

The result must help existing semantic-profile users move toward complete Core contracts while preserving authority, confidence, evidence, source binding, unknowns, conflicts and policy boundaries.

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
ADR-0016  unified Core validation and comparison
```

ADR-0016 includes the independent-audit corrections for real ADR-0005 through ADR-0013 evaluator orchestration, explicit non-evaluable profile states, separated comparator `changeType` and normative `assessment`, dangerous-index blocking and iterative JSON-depth limits.

## Required work

1. inventory the standalone semantic-mapping profile fields and their Core destinations;
2. define deterministic mappings into `aduc`, `resource`, `structure`, `semantics`, `provenance` and other modules only when evidence exists;
3. preserve missing information as `unknown`, `notDescribed`, `indeterminate` or `requiresHumanReview` instead of inventing facts;
4. provide migration fixtures from existing semantic-profile examples to complete Core contracts;
5. validate migrated outputs with `tools/aduc_core.py validate`;
6. compare migrated outputs with accepted Core examples where useful;
7. document unsupported fields, required review and non-goals.

## Scope boundary

Do not implement the JSON/CSV compiler, review UI, registry service, MCP adapter, extensions, anticipation engine, production access control, value benchmark or external multi-model proof in this task.

Do not treat a migrated semantic-profile contract as publisher authority unless the source artifact already carries the required evidence and authority state.

## Completion test

An independent implementer must be able to:

1. run the migration workflow locally;
2. inspect which source fields mapped into which Core modules;
3. validate every migrated complete Core contract with `tools/aduc_core.py validate`;
4. see every unsupported or review-required fact in a stable report;
5. confirm that no compiler inference, legal permission or identity merge was silently introduced.

## Next action after acceptance

Choose the next task from `MASTER_PLAN.md` and the adoption gates. The JSON/CSV compiler remains blocked until the migration path is accepted and the review-tax/value measurement setup is ready to run.

## Cross-cutting adoption constraint

[`ADOPTION_AND_VALUE_VALIDATION.md`](ADOPTION_AND_VALUE_VALIDATION.md) remains mandatory. Do not implement the JSON/CSV compiler now.
