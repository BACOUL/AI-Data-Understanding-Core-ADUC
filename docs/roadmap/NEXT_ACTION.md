# Next Action

## Single active task

Implement Gate 3 by creating a user-facing ADUC validator and machine-readable conformance report.

Create:

```text
tools/aduc_validate.py
spec/VALIDATION_ERROR_CATALOG_0_1.md
tests/validator/
```

## Required behavior

The validator must:

1. validate a supplied profile against `schema/aduc-mapping-profile.schema.json`;
2. return a non-zero exit code for non-conforming input;
3. produce readable text output and optional JSON output;
4. assign stable error codes;
5. detect duplicate assertion identifiers;
6. reject an assertion that supersedes itself;
7. detect `supersedes` cycles within one profile document;
8. report incompatible canonical targets for the same local reference;
9. distinguish schema errors, semantic-profile errors and unverifiable trust claims;
10. state clearly that canonical source authority cannot be proven without external trust configuration.

## Required tests

- conforming profile exits successfully;
- each semantic error produces its expected stable code;
- JSON report has a documented shape;
- command works from the repository root;
- existing 4 valid and 10 invalid schema fixtures continue to pass.

## Scope boundary

Do not implement cryptographic signatures, network resolution, remote authority verification, inference, registry, RDF round-trip or multi-model evaluation in this task.

## Completion test

A third party must be able to run one documented command against an arbitrary local profile and receive deterministic, actionable validation results.
