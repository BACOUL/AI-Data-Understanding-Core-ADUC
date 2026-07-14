# ADUC Core Validation Pipeline 0.1

- Status: implemented reference pipeline
- Applies to: ADUC Core contracts using `coreVersion` `0.1.0-alpha.0`
- CLI: `python tools/aduc_core.py`

## Pipeline

```text
JSON loading
  -> input size, depth and node-count limits
  -> Draft 2020-12 JSON Schema validation
  -> ADR-0014 architectural checker
  -> reference and identifier indexing
  -> ADR-0005..ADR-0013 evaluator adapters
  -> profile-oriented cross-module checks
  -> diagnostic aggregation and deduplication
  -> stable JSON or text report
```

The pipeline is local and offline. The schema registry is built from files in `schema/`; remote `$ref` loading is not used.

## Responsibilities

JSON Schema remains responsible for structural assertions: types, required properties, enums, cardinalities, object closure, exclusive forms, formats, digest shape and structural dependencies.

The architecture and profile layers report invariants that JSON Schema cannot guarantee alone: global identifier uniqueness, internal reference resolution, exact bindings, extension declaration/use consistency, namespace conflicts, ownership conflicts, graph cycles, relation contradictions, authority promotion risk, contested or deprecated assertions, unsupported required extensions and policy states that require review.

The profile layer calls the accepted local evaluators for ADR-0005 through ADR-0013 where the Core contract contains an applicable shape. Rules that require a concrete request, local bytes, a pinned registry or a standalone profile record not carried by the Core contract are recorded in `profileEvaluations` as `notApplicable`, `unknown`, `indeterminate` or `requiresHumanReview`; those states are not counted as successful evaluation.

## Report Outcomes

The validation report uses these global outcomes:

```text
valid
validWithWarnings
requiresHumanReview
blocked
```

These outcomes are distinct from policy evaluator results such as `permit`, `deny`, `notApplicable`, `indeterminate` and `requiresHumanReview`.

## Exit Codes

```text
0  valid or validWithWarnings
1  blocked validation or incompatible/not-comparable comparison
2  human review or potential incompatibility required
3  input, read or usage error
```

The CLI does not print Python tracebacks for ordinary user input errors.

## Determinism

Diagnostics are deduplicated only when code, severity, category, path, message, module, related paths and blocking flag match exactly. The final order is:

1. severity;
2. canonical module order;
3. JSON path;
4. code;
5. message.

JSON object member order does not affect the report.

## Limits

The reference CLI rejects inputs above 5 MB, JSON depth above 100 and JSON node count above 50,000. Depth and node checks use iterative traversal so deeply nested JSON fails with a stable input diagnostic rather than a Python traceback. These are implementation safety limits, not Core semantics.
