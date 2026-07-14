# Next Action

## Single active task

Define and implement the deterministic complete-contract formatter for complete ADUC Core contracts.

## Objective

Produce stable UTF-8 JSON for a complete ADUC Core contract without changing meaning, inventing facts, repairing invalid input or becoming a source-data compiler.

The formatter must validate the input and output through the accepted Core pipeline, preserve all identifiers, references, values, qualifications, conflicts, uncertainty, provenance and policy content, and emit a stable machine-readable report.

## Completed dependencies

- ADR-0014 normative Core object model and module boundaries;
- ADR-0015 official modular Core JSON Schema family;
- ADR-0016 unified Core validation and comparison;
- ADR-0017 deterministic semantic-profile migration;
- `tools/aduc_core.py validate` and `tools/aduc_core.py compare`.

## Required work

1. define deterministic object-member ordering while preserving every array order;
2. reject invalid or duplicate-key JSON instead of repairing it silently;
3. preserve Unicode, numbers, identifiers, references and all semantic content;
4. prove byte stability and idempotence;
5. revalidate formatted output with `tools/aduc_core.py validate`;
6. emit stable JSON and text reports with explicit exit codes;
7. provide valid, review-required and rejected fixtures plus focused tests.

## Scope boundary

Do not implement the JSON/CSV compiler, semantic inference, repair UI, registry service, MCP adapter, extensions, anticipation engine, production access control, value benchmark or external multi-model proof in this task.

The JSON/CSV compiler remains blocked until the adoption and review-tax gates are ready to run.

## Completion test

An independent implementer must be able to format a complete validated ADUC Core contract twice and obtain identical bytes, confirm semantic preservation, validate the result through `tools/aduc_core.py validate`, compare it through `tools/aduc_core.py compare`, and inspect any failure in a stable report.
