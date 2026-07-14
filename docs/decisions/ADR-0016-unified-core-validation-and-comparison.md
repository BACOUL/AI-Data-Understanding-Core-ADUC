# ADR-0016: Unified Core Validation and Comparison

- Status: Accepted
- Date: 2026-07-14
- Supersedes: none
- Depends on: ADR-0005 through ADR-0015

## Context

ADR-0014 froze the ten-block ADUC Core object model. ADR-0015 delivered the official modular JSON Schema Draft 2020-12 family and the complementary architectural checker. Implementers now need one local interface that validates a complete Core contract and compares two complete contracts without relying on network access, AI providers or accidental JSON member order.

This ADR records the reference orchestration layer. It does not redefine Core modules, ownership boundaries, profile semantics or extension rules.

## Decision

The reference implementation provides one CLI in `tools/aduc_core.py` with two commands:

```text
python tools/aduc_core.py validate contract.json
python tools/aduc_core.py compare old.json new.json
```

The validator runs:

```text
JSON loading
  -> modular JSON Schema family
  -> ADR-0014 architecture checker
  -> accepted ADR-0005 through ADR-0013 evaluator adapters
  -> profile and cross-module evaluation
  -> deterministic diagnostic aggregation
```

The profile pass calls the accepted domain evaluators where Core contains enough information to do so. When a profile requires a concrete request, a pinned local registry, local bytes or a standalone profile bundle that is not present in the Core contract, the report records `notApplicable`, `unknown`, `indeterminate` or `requiresHumanReview` in `profileEvaluations` instead of pretending that the rule was evaluated.

The comparator runs validation first, blocks comparison when either input is not JSON-Schema-valid, then indexes addressable Core objects by stable identifiers rather than array order. Schema-valid contracts are also `notComparable` when architecture diagnostics make identifier-based indexing unsafe, including duplicate identifiers, unresolved references, ownership or binding violations, namespace conflicts and unsupported required extensions. Other contested, deprecated, prohibited or review-required states remain comparable and are reported as semantic assessments.

Reports are JSON-compatible, versioned with `reportVersion: "0.1.0"` and deterministic. Text output is a human-readable rendering of the same result.

## Validation Outcomes

The validator exposes:

```text
valid
validWithWarnings
requiresHumanReview
blocked
```

The policy profile may still produce policy-specific states such as `permit`, `deny`, `notApplicable`, `indeterminate` or `requiresHumanReview`; those are not the global validation outcome.

## Comparison Classifications

The comparator separates mechanical change type from semantic assessment.

`changeType` is one of:

```text
unchanged
added
removed
modified
```

`classification` remains the legacy compatibility-risk bucket:

```text
compatible
potentiallyIncompatible
incompatible
requiresHumanReview
notComparable
```

Each change also carries an `assessment` selected from:

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

The overall result is derived from the highest-risk change. The comparator reports compatibility risk; it does not prove legal permission, authority, truth or trust.

## Exit Codes

```text
0  valid validation or non-blocking comparison
1  blocked validation, incompatible comparison or not-comparable comparison
2  human review or potential incompatibility required
3  usage, read or JSON input error
```

## Consequences

Existing semantic-profile tools remain in place. `tools/aduc_validate.py` and `tools/aduc_compare.py` are not replaced by weaker full-Core duplicates; the unified full-Core CLI is `tools/aduc_core.py`.

The official comparison fixture suite lives in `examples/core/comparison/cases.json` and is tested by `tests/core_comparator/`.

The next implementation step can build migration and authoring workflows on top of these accepted reports instead of re-implementing validation or comparison logic.
