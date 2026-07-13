# Next Action

## Single active task

Begin Gate 5 by specifying and implementing deterministic comparison of two validated ADUC mapping profiles.

Create:

```text
spec/COMPARISON_PROTOCOL_0_1.md
tools/aduc_compare.py
tests/comparator/
examples/comparison/
```

## Objective

Given two schema-valid and semantically valid profiles, identify which local fields are semantically comparable using only the published assertions and without hidden provider-specific mappings.

## Required behavior

1. validate both input profiles before comparison;
2. preserve each local reference, source binding, assertion status and mapping relation;
3. report an exact semantic match only when the declared targets and relation rules justify it;
4. report `closeMatch`, `broadMatch`, `narrowMatch` and `relatedMatch` as non-exact candidates;
5. block automatic comparison when an applicable mapping is `contested`;
6. expose incompatible canonical mappings instead of choosing one;
7. distinguish `comparable`, `candidate`, `blocked`, `unmapped` and `notEvaluated` results;
8. emit deterministic text and JSON reports;
9. avoid network ontology resolution and hidden aliases in conformance mode;
10. state explicitly when unit conversion, temporal alignment or entity resolution cannot be evaluated from the supplied artifacts.

## Required demonstration

Provide two differently named source fields that map to the same semantic target, plus negative cases showing:

- same-looking names without a shared target are not matched;
- a `closeMatch` is not upgraded to exact equivalence;
- a contested mapping blocks automatic use;
- missing unit, time or entity metadata is returned as `notEvaluated`, not guessed.

## Scope boundary

Do not build automatic ontology search, unit conversion, entity resolution, temporal reasoning, model calls, a registry or the anticipation engine. Gate 5 proves portable semantic comparison only and identifies which additional source-description standards are required for later dimensions.

## Completion test

Two independent executions over the same profile pair must produce byte-for-byte equivalent JSON comparison output, and CI must verify all positive and negative cases.
