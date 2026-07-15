# Next Action

## Single active task

Define and implement the provider-neutral full-Core conformance runner.

## Objective

Provide a deterministic local runner that executes frozen ADUC conformance cases against validator, comparator and formatter implementations and produces a stable implementation report.

The runner must test declared behavior without treating the Python reference engine as the specification or presenting a self-test as independent interoperability proof.

## Completed dependencies

- ADR-0014 normative Core object model and module boundaries;
- ADR-0015 official modular Core JSON Schema family;
- ADR-0016 unified Core validation and comparison;
- ADR-0017 deterministic semantic-profile migration;
- ADR-0018 deterministic complete-contract formatting;
- stable validator, comparator, migration and formatter reports.

## Required work

1. define versioned conformance classes for contracts, validators, comparators and formatters;
2. create a frozen machine-readable test manifest with required, optional and unsupported capabilities;
3. provide a local runner and an explicit adapter contract for non-reference implementations;
4. compare actual reports and exit behavior with normative expected outcomes without requiring byte-identical implementation internals;
5. preserve unknown, contested, prohibited and `requiresHumanReview` outcomes in conformance evidence;
6. emit deterministic JSON and text implementation reports with stable diagnostics;
7. include positive, negative, adversarial, resource-limit and repeatability fixtures;
8. document the boundary between reference self-conformance, independent implementation evidence and external AI-consumer proof.

## Scope boundary

Do not implement the JSON/CSV compiler, TypeScript or Python public SDK packages, review UI, hosted service, MCP adapter, registry, extensions, anticipation engine or external multi-model proof in this task.

Do not claim independent conformance until a genuinely separate implementation executes the frozen suite. The JSON/CSV compiler remains blocked until the adoption and review-tax gates are ready to run.

## Completion test

An independent implementer must be able to declare supported conformance classes, run the frozen suite locally through the adapter contract, inspect every pass, failure, unsupported capability and review-required result in a deterministic report, and reproduce the same assessment without hidden network access or provider-specific logic.
