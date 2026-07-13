# ADR-0011 — Uncertainty, Confidence, Missingness, and Data Quality

- Status: accepted
- Date: 2026-07-13
- Issue: #39
- Pull request: #40
- Decision owners: ADUC maintainers

## Context

A data value can be correctly identified, bound to its source, expressed in a compatible unit, aligned in time, linked to the correct entity, and fully traceable while still being uncertain or unsuitable for a particular use.

ADUC must not collapse these distinct concerns into one generic `confidence` field:

```text
measurement or value uncertainty
statistical interval
model probability or score
semantic-mapping confidence
data-quality measurement
epistemic authority
```

A canonical assertion records source authority; it does not imply statistical certainty. A model score is not a probability without calibration. A dataset-quality score does not replace uncertainty attached to an individual value.

## Decision

### 1. Keep five concerns separate

| Concern | Representation |
|---|---|
| measurement/value uncertainty | uncertainty assertion |
| semantic confidence | ADR-0005 epistemic confidence |
| model confidence | calibrated model-output evidence or categorical distribution |
| data quality | DQV-compatible quality measurement |
| epistemic authority | ADR-0005 authority level |

No property may silently substitute for another.

### 2. Reuse established standards

ADUC profiles concepts from JCGM GUM/VIM for quantitative measurement uncertainty and W3C DQV for data-quality metadata. It reuses ADR-0006 for target binding, ADR-0007 for units and quantity roles, ADR-0010 for production and propagation provenance, and ADR-0005 for authority, conflict, and lifecycle.

ADUC does not create a universal statistical theory or a universal quality score.

### 3. Common uncertainty record

Every uncertainty assertion identifies:

```text
uncertaintyId
targetBinding
uncertaintyType
quantityKind
quantityRole
unit where numeric
method
provenanceActivity
authorityLevel
assertedBy
evidence
conflictState
lifecycleState
```

Numeric values are decimal strings. Material identifiers and evidence are absolute IRIs.

### 4. Supported v0.1 forms

```text
standard
expanded
relativeStandard
asymmetric
interval
distribution
categorical
unknown
```

Requirements include:

- non-negative uncertainty magnitudes;
- explicit unit and compatible quantity role for numeric forms;
- coverage probability, interpretation, and method for intervals;
- explicit family and parameters for distributions;
- calibrated probabilities summing to one for categorical distributions;
- a reason and no fabricated numeric parameters for `unknown`.

### 5. Statistical uncertainty is not authority

A canonical assertion may remain highly uncertain. Zero uncertainty is accepted only when a value is exact by definition and that exactness has a declared method and evidence. Decimal formatting, repeated values, or source authority do not establish exactness.

For inferred assertions, `epistemicConfidence` and `confidenceMethod` describe support for the assertion itself, not measurement uncertainty.

### 6. Affine and multiplicative conversion

For a unit conversion:

```text
y = (x + offset) × multiplier
```

an absolute uncertainty magnitude is converted as:

```text
u(y) = |multiplier| × u(x)
```

The affine offset is never applied to the uncertainty magnitude.

Reference result:

```text
89 °C ± 0.5 °C
→ 192.2 °F ± 0.9 °F
```

Relative uncertainty is preserved generically only for purely multiplicative conversion in v0.1. Every converted uncertainty retains a provenance activity.

### 7. Interval interpretation

A statement such as “95% interval” is invalid without:

```text
coverageProbability
intervalInterpretation
coverageMethod
```

Supported reference interpretations are:

```text
coverage
frequentistConfidence
bayesianCredible
prediction
```

### 8. Model probabilities require calibration

A model score is represented as probability only when the record includes:

```text
calibration method
evaluation dataset binding
calibration evidence
model-execution provenance
category probabilities summing exactly to one
```

Similarity values, logits, confidence labels, and self-reported LLM confidence are not probabilities by default.

### 9. Missingness and censoring

Observation state is separate from uncertainty:

```text
observed
missing
censoredBelow
censoredAbove
intervalCensored
```

Missing and censored values must not be replaced silently by exact values. Censoring records detection or interval limits, compatible units, and method. Imputation is a separate provenance activity that retains the original observation state.

### 10. Resolution and false precision

Displayed decimal places do not establish uncertainty. A documented rectangular instrument-resolution contribution may use:

```text
u = resolution / sqrt(12)
```

Reference result:

```text
resolution 0.1 → standard uncertainty 0.028867513459481
```

### 11. Dependence and propagation

A propagation request declares one of:

```text
independent
correlated
unknown
```

Independence requires evidence. Correlated propagation requires a coefficient in `[-1, 1]` and evidence. Unknown dependence blocks generic propagation.

The v0.1 evaluator supports a limited deterministic subset:

1. scale-only conversion of standard uncertainty;
2. two-input additive propagation of standard uncertainty;
3. two-input multiplicative propagation of relative standard uncertainty;
4. rectangular resolution contribution.

For addition:

```text
u² = u₁² + u₂² + 2ρu₁u₂
```

Reference results:

```text
3 and 4 independent → 5
0.03 and 0.04 independent relative uncertainties → 0.05
```

Unsupported nonlinear, multivariate, simulation-based, or domain-specific propagation is blocked or delegated to an extension.

### 12. Distribution records

Distribution families are identified by IRIs and carry explicit parameters. The reference subset validates normal and rectangular distributions plus calibrated categorical distributions. Declaring a family does not prove it is appropriate; authority and evidence remain separate.

### 13. DQV-compatible quality records

A quality bundle identifies:

```text
bundleId
computedOn
requiredMetrics
measurements
disclosureState
missingMetrics
redactedMetrics
redactionPolicy when needed
provenanceActivity
authority and evidence
```

Each measurement identifies its metric, dimension, target, value, unit where relevant, method, provenance, and authority. Numeric quality values are not comparable merely because they share a numeric range.

Supported disclosure states are:

```text
complete
partial
redacted
unknown
```

A complete claim is invalid when required metrics are missing or redacted. Redaction requires a policy reference.

### 14. Consumer blocking rules

Automatic reliance or propagation is blocked when:

- uncertainty is contested or deprecated;
- units or quantity roles are absent or incompatible;
- bounds or coverage claims are invalid;
- categorical probabilities are uncalibrated;
- dependence is unknown;
- provenance is absent;
- quality disclosure is inconsistent;
- an unsupported propagation model is required.

`unknown` is valid information and must never be converted to zero.

### 15. Error families

```text
ADUC-UNC-001..011  uncertainty structure, meaning, interval, distribution, calibration, and exactness
ADUC-PROP-001..004 dependence and propagation
ADUC-DATA-001..003 observation state, missingness, and censoring
ADUC-DQV-001..004 quality measurement and disclosure
```

The detailed error contract is implemented by `tools/aduc_uncertainty.py` and tested through the official fixtures.

### 16. Core boundary

The following remain outside generic v0.1 unless supplied by external method profiles or extensions:

- complex covariance matrices;
- Monte Carlo propagation;
- spatial uncertainty;
- stochastic processes and time-series models;
- ensembles and fuzzy membership;
- domain-specific clinical, safety, or legal risk models;
- universal model-calibration procedures.

## Consequences

### Positive

- measurement uncertainty cannot be confused with mapping confidence;
- canonical data can remain statistically uncertain;
- uncalibrated scores cannot masquerade as probability;
- missing, censored, and unknown information remains explicit;
- conversions preserve uncertainty correctly;
- DQV quality metadata is reusable without creating one universal score;
- unsupported propagation fails safely.

### Costs

- producers must document units, methods, coverage, dependence, and provenance;
- some calculations remain blocked until evidence exists;
- quality metrics must remain tied to their method and purpose;
- probability claims require calibration evidence.

## Rejected alternatives

- one generic `confidence` field;
- assuming independence when covariance is absent;
- deriving uncertainty from decimal places;
- treating every model score as probability;
- setting uncertainty to zero for canonical data;
- inventing an ADUC-specific universal quality ontology.

## References

- JCGM 100:2008 — Guide to the expression of uncertainty in measurement: https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf
- JCGM publications: https://www.bipm.org/en/committees/jc/jcgm/publications
- NIST Technical Note 1297: https://www.nist.gov/pml/nist-technical-note-1297
- W3C Data Quality Vocabulary: https://www.w3.org/TR/vocab-dqv/
- W3C PROV-O: https://www.w3.org/TR/prov-o/

## Acceptance evidence

- fourteen valid uncertainty, propagation, missingness, censoring, and quality cases;
- twenty-four required invalid counterexamples;
- ten deterministic evaluator and CLI tests;
- reference calculations for affine conversion, additive and multiplicative propagation, and rectangular resolution;
- GitHub Actions passed the uncertainty suite and every pre-existing validation suite in PR #40.

## Follow-up

1. define general relation semantics;
2. define policy and permitted-use boundaries;
3. freeze the normative full-Core object model;
4. implement the full-Core JSON Schema family;
5. unify comparison across all accepted profiles.
