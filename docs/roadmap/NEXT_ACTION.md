# Next Action

## Single active task

Begin Gate 6 by freezing the provider-neutral multi-model conformance protocol without claiming that interoperability has already been demonstrated.

Create:

```text
spec/MULTI_MODEL_CONFORMANCE_PROTOCOL_0_1.md
schema/model-conformance-result.schema.json
examples/conformance/
tests/conformance/
tools/aduc_conformance.py
```

## Objective

Define a reproducible evaluation in which at least two independent AI consumers receive the same source descriptions, ADUC profiles and task instructions, then return normalized results that can be compared without provider-specific hidden mappings.

## Required protocol decisions

1. fixed input package and cryptographic file inventory;
2. provider-neutral task instructions;
3. prohibited hidden context, memory, browsing and ontology lookup;
4. required output fields and evidence references;
5. normalization of model output before scoring;
6. pass/fail rules for comparable, candidate, blocked and unmapped mappings;
7. preservation of authority status, relation and `notEvaluated` dimensions;
8. recording of provider, model, version, date, parameters and raw output;
9. disagreement and failure reporting;
10. distinction between deterministic tool conformance and probabilistic model behavior.

## Required test package

At minimum include scenarios for:

- differently named fields with one reviewed/canonical exact target;
- an inferred mapping that must remain a candidate;
- a `closeMatch` that must not become exact;
- a contested mapping that must remain blocked;
- identical local names with different targets that must not be joined;
- unit, time and entity dimensions that must remain `notEvaluated` when absent.

## Required tooling

The local harness must:

- create a frozen conformance package;
- validate the package inventory;
- validate normalized result files against the result schema;
- compare independent result files deterministically;
- generate a machine-readable conformance report;
- never call a model provider automatically in CI.

## Scope boundary

Do not embed API keys, call paid model APIs in GitHub Actions, tune prompts for one provider, add hidden semantic aliases, claim interoperability before real external runs, build a public registry or implement the anticipation engine.

## Completion test

Gate 6 protocol preparation passes when an independent tester can download one frozen package, run it manually against two different AI systems, store raw and normalized outputs, and obtain a deterministic local pass/fail comparison. Actual multi-model interoperability remains unproven until two qualifying external runs are committed with reproducible evidence.
