# ADUC Core deterministic formatting 0.1

## Purpose

This specification defines the reference serialization profile for one complete, already-authored ADUC Core contract.

It complements validation and comparison. It does not create a contract from source data and does not repair one.

## Command

```bash
python tools/aduc_core_format.py contract.json --output contract.formatted.json
```

Machine-readable report:

```bash
python tools/aduc_core_format.py contract.json \
  --output contract.formatted.json \
  --report-format json
```

Replacing an existing destination requires `--force`. Input and output paths must differ.

## Processing pipeline

1. Check path and byte limit.
2. Decode strict UTF-8.
3. Parse JSON while rejecting duplicate members and non-JSON constants.
4. Check node and depth limits.
5. Run the accepted full-Core validation pipeline.
6. Stop without output when validation is blocked.
7. Serialize using ADR-0018 ordering and numeric rules.
8. Parse the formatted bytes again.
9. Prove exact-decimal JSON-value equality and recursive array-order preservation using structural paths.
10. Revalidate the formatted document.
11. Write atomically.
12. Emit the stable report.

A `requiresHumanReview` validation outcome is formatable. The same review requirement must remain visible after formatting and produces exit code 2.

## Ordering

Top-level order is loaded from the frozen Core model decision and currently equals:

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

Nested objects use Unicode code-point order. Arrays preserve source order exactly.

## Output encoding

- UTF-8;
- no byte-order mark;
- two spaces per indentation level;
- no trailing spaces;
- one final LF;
- non-ASCII characters are preserved directly;
- finite JSON numbers only;
- deterministic arbitrary-precision decimal normalization defined by ADR-0018, independent of binary floating point and runtime decimal context.

## Report

Stable top-level members:

- `reportVersion`;
- `formatterVersion`;
- `source`;
- `output`;
- `outcome`;
- `formatted`;
- `contractId`;
- `ordering`;
- `inputValidation`;
- `outputValidation`;
- `preservation`;
- `bytes`;
- `diagnostics`.

`bytes.sha256` hashes the exact formatted UTF-8 bytes, including the final LF.

The report does not claim that the contract is factually true, legally permitted or independently conformant. It only records deterministic formatting and the accepted Core validation outcomes.

## Conformance requirements

A conforming implementation must prove:

- duplicate-member rejection;
- invalid-contract rejection without repair;
- deterministic object-member order;
- unchanged recursive array order;
- Unicode preservation;
- deterministic number rendering;
- byte-level idempotence;
- identical exact-decimal JSON value before and after formatting;
- collision-safe structural array-path comparison, including extension member names containing dots or brackets;
- race-safe refusal to overwrite a destination created during formatting;
- full-Core validity before and after formatting;
- stable reports and exit codes;
- bounded local processing with no remote resolution.

## Limits

This profile does not define a source-data compiler, semantic inference, JSON-LD normalization, graph canonicalization, signature format, registry service or hosted API.
