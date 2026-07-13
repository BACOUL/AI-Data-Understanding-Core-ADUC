# Next Action

## Single active task

Define and accept the ADUC uncertainty and data-quality strategy before implementing the full-Core JSON Schema.

Create:

```text
docs/decisions/ADR-0011-uncertainty-and-data-quality.md
spec/UNCERTAINTY_PROFILE_0_1.md
examples/uncertainty/
tools/aduc_uncertainty.py
tests/uncertainty/
```

## Objective

Define how ADUC represents uncertainty about measured, declared, estimated, inferred, converted, aggregated, and model-produced values without confusing uncertainty with epistemic authority, source quality, or confidence in a semantic mapping.

## Completed dependencies

The following Core decisions are specified and reference-tested:

```text
ADR-0005  epistemic lifecycle
ADR-0006  source description and immutable binding
ADR-0007  units and deterministic conversion
ADR-0008  temporal semantics and timezone alignment
ADR-0009  entity identity and safe equivalence
ADR-0010  provenance and transformation lineage
```

Every uncertainty assertion must bind its target through ADR-0006, use compatible units through ADR-0007, identify its production method through ADR-0010, and preserve ADR-0005 authority, evidence, conflict, and lifecycle.

## Cross-cutting adoption constraint

The official [`ADOPTION_AND_VALUE_VALIDATION.md`](ADOPTION_AND_VALUE_VALIDATION.md) plan remains mandatory for later compiler, review, and interoperability work.

Do not implement the JSON/CSV compiler now. A future compiler may propose uncertainty models only as `inferred`, must expose unsupported assumptions, and must never fabricate measurement precision from display formatting or sample size alone.

## Required decisions

1. separate measurement uncertainty, semantic confidence, data quality, model confidence, and epistemic authority;
2. represent absolute, relative, asymmetric, interval, distributional, categorical, and unknown uncertainty;
3. declare coverage probability, confidence level, method, assumptions, sample size, and calibration evidence when applicable;
4. reuse established vocabularies such as DQV and appropriate metrology/statistical standards instead of creating a universal statistical ontology;
5. define how units attach to uncertainty values and how affine conversions affect absolute and relative uncertainty;
6. define deterministic propagation for supported arithmetic and conversion operations;
7. distinguish independent, correlated, and unknown dependence between inputs;
8. define aggregation, missingness, censoring, detection limits, rounding, and resolution effects;
9. represent qualitative quality dimensions separately from numeric uncertainty;
10. define consumer behavior when uncertainty is missing, incompatible, contested, deprecated, or impossible to propagate;
11. preserve provenance for every derived uncertainty result;
12. define the boundary between Core uncertainty and domain-specific extensions.

## Required counterexamples

The specification must reject or explicitly block:

- treating semantic mapping confidence as measurement uncertainty;
- treating a canonical assertion as statistically certain;
- expressing an uncertainty value without a compatible unit or quantity role;
- claiming a 95% interval without a method or interpretation;
- propagating independent-error formulas when inputs are correlated or dependence is unknown;
- converting absolute temperature uncertainty with an affine offset;
- deriving false precision from decimal places;
- silently dropping uncertainty during conversion or aggregation;
- using negative standard uncertainty;
- accepting reversed or impossible bounds;
- presenting an uncalibrated model score as probability;
- claiming complete quality when material metrics are missing or redacted;
- hiding censoring, detection limits, or missing-data assumptions;
- using a domain-specific uncertainty model as a universal Core rule.

## Scope boundary

Do not implement the full-Core schema, complete general-relation or policy profiles, compiler, review UI, registry service, MCP adapter, extensions, or anticipation engine in this task.

## Completion test

An independent implementer must be able to:

1. represent a measured value with absolute and relative uncertainty;
2. convert and propagate uncertainty through at least one unit conversion;
3. distinguish a statistical interval from a semantic confidence score;
4. preserve uncertainty through one deterministic transformation lineage;
5. block one unsupported correlated propagation;
6. represent missing, qualitative, and contested quality information without inventing precision;
7. reproduce reference calculations from pinned methods and evidence.
