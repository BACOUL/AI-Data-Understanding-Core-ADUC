# Next Action

## Single active task

Define the public SDK and package publication boundary for the accepted Core CLI tools.

## Objective

Define the narrow public API, package threat model and publication controls for future TypeScript and Python packages without changing the existing Core CLI behavior.

The task must make package boundaries, compatibility expectations, SBOM/signing requirements and installation-test obligations explicit before any public PyPI/npm or SDK availability claim.

## Completed dependencies

- ADR-0014 normative Core object model and module boundaries;
- ADR-0015 official modular Core JSON Schema family;
- ADR-0016 unified Core validation and comparison;
- ADR-0017 deterministic semantic-profile migration;
- ADR-0018 deterministic complete-contract formatting;
- ADR-0019 provider-neutral full-Core conformance runner;
- stable validator, comparator, migration, formatter and conformance reports.

## Required work

1. define the supported SDK surface for validation, comparison, formatting and conformance invocation;
2. define package names, versioning, compatibility and deprecation rules without publishing packages yet;
3. define the package threat model, dependency policy, SBOM expectations and signing or attestation plan;
4. define installation tests for Windows, Linux and macOS;
5. define how SDK behavior maps to existing CLI exit codes and stable reports;
6. define documentation and Try in 5 minutes updates needed before package publication.

## Scope boundary

Do not implement the JSON/CSV compiler, review UI, hosted service, MCP adapter, registry, extensions, anticipation engine or external multi-model proof in this task.

Do not publish public packages or claim stable SDK availability until the package boundary and release controls are accepted. Do not claim independent conformance until a genuinely separate implementation executes the frozen suite. The JSON/CSV compiler remains blocked until the adoption and review-tax gates are ready to run.

## Completion test

An implementer must be able to identify the planned SDK API boundary, package names, versioning rules, installation-test matrix, signing/SBOM expectations and compatibility policy before any package is published.
