# ADR-0018 — Deterministic complete-contract formatting

Status: Accepted for implementation  
Date: 2026-07-15  
Issue: #60

## Context

ADUC Core contracts are ordinary JSON documents. JSON object-member order and insignificant whitespace are not semantic, but unstable serialization prevents byte-for-byte review, reproducible hashing, deterministic fixtures and independent conformance checks.

The accepted ADR-0014 object model, ADR-0015 schema family, ADR-0016 validator/comparator and ADR-0017 migration pipeline already define what a complete Core contract means. The formatter must therefore serialize an existing valid contract without becoming a compiler, inference engine or repair tool.

## Decision

ADUC defines a local deterministic complete-contract formatter with the following rules.

1. The input must be one UTF-8 JSON object representing one complete ADUC Core contract.
2. Duplicate object members, non-JSON numeric constants, invalid UTF-8, invalid JSON and resource-limit violations are rejected before Core validation.
3. The input is validated through `tools/aduc_core.py`'s accepted full-Core pipeline. Blocked input is not formatted.
4. Top-level Core blocks are emitted in the frozen manifest order:

   `aduc`, `resource`, `structure`, `semantics`, `identity`, `context`, `provenance`, `uncertainty`, `relations`, `policy`.

5. Any additional top-level member is emitted after the reserved Core blocks in Unicode code-point order. Such a member is still subject to the accepted Core extension rules.
6. Members of every nested JSON object are emitted in Unicode code-point order.
7. Array elements are never reordered. Array order is preserved recursively, including arrays that might appear set-like to one implementation.
8. Strings are emitted as UTF-8 JSON strings without mandatory ASCII escaping.
9. Numbers are normalized from their exact parsed decimal value without binary floating-point conversion or runtime decimal-context rounding:
   - finite values only;
   - trailing fractional zeros are removed;
   - `-0` remains negative zero;
   - plain notation is used for adjusted exponents from -6 through 20;
   - otherwise lowercase scientific notation is used without a plus sign or exponent padding.
10. Output uses two-space indentation, `: ` member separators, `,` separators and exactly one final LF.
11. The complete exact-decimal JSON value must compare equal after formatting, and every array path and element order must remain equal. Array paths are represented structurally, not by concatenated member-name strings.
12. The formatted output is validated again through the same full-Core pipeline.
13. Formatting reports are deterministic JSON or text with stable fields, codes and exit statuses.
14. Output is written atomically. Existing files are not replaced without explicit `--force`, including when a destination appears concurrently, and input is never overwritten in place.

## Outcomes and exit codes

| Exit | Outcome | Meaning |
|---:|---|---|
| 0 | `formatted` | Valid contract formatted and revalidated |
| 1 | `blocked` | Core validation, preservation or output safety blocked formatting |
| 2 | `formattedRequiresHumanReview` | Contract remains valid but its accepted Core outcome requires human review |
| 3 | `usageError` | Input JSON, path, duplicate member or resource-limit error |

## Safety boundary

The formatter does not:

- infer or add a missing field;
- delete an unsupported field;
- repair an invalid contract;
- change identifiers, references, status, authority, confidence, conflicts, lifecycle, provenance, uncertainty or policy;
- sort arrays;
- resolve remote schemas or vocabularies;
- compile source JSON, CSV, APIs, documents or databases into ADUC;
- assign legal permission, publisher authority or identity equivalence.

## Consequences

The same accepted contract produces identical UTF-8 bytes when formatted repeatedly by the reference implementation. Implementations can hash, review and compare formatter output reproducibly. This is an ADUC formatting profile, not a claim of RFC 8785 or another external canonicalization standard.

Any future change to ordering, number rendering or report semantics requires a versioned ADR and formatter version change.
