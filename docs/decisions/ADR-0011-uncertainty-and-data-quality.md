# ADR-0011 — Uncertainty, Confidence, Missingness, and Data Quality

- Status: proposed
- Date: 2026-07-13
- Issue: #39
- Decision owners: ADUC maintainers

## Context

A value can be correctly identified, bound to its source, expressed in a compatible unit, aligned in time, linked to the correct entity, and fully traceable while still being uncertain or unsuitable for a particular use.

Several concepts are routinely conflated:

```text
measurement uncertainty
statistical interval
model probability or score
semantic-mapping confidence
data-quality measurement
epistemic authority
```

Treating these as one generic `confidence` field would cause unsafe comparisons and false claims. A canonical assertion is authoritative about what a publisher declared; it is not statistically certain. A high model score is not a calibrated probability. A dataset may have high completeness while an individual measurement remains uncertain.

ADUC needs a constrained profile that preserves these distinctions, reuses established metrology and data-quality work, and defines deterministic behavior for a small v0.1 propagation subset.

## Decision

### 1. Keep five concerns separate

ADUC separates:

| Concern | Meaning | Core representation |
|---|---|---|
| measurement/value uncertainty | dispersion or range reasonably attributable to a value | uncertainty assertion |
| semantic confidence | support for an inferred mapping | ADR-0005 epistemic confidence |
| model confidence | model-produced score or calibrated probability | model-output evidence or categorical distribution |
| data quality | fitness-related measurement against a declared metric | DQV-compatible quality measurement |
| epistemic authority | who may assert, verify, or canonically publish a claim | ADR-0005 authority level |

No field may silently substitute for another.

### 2. Reuse GUM/VIM and DQV

For quantitative measurement uncertainty, ADUC profiles concepts from the JCGM Guide to the Expression of Uncertainty in Measurement (GUM) and related metrology guidance instead of defining a new theory of measurement.

For dataset and resource quality, ADUC maps to the W3C Data Quality Vocabulary (DQV):

```text
dqv:QualityMeasurement
dqv:Metric
dqv:Dimension
dqv:computedOn
dqv:value
dqv:QualityMetadata
```

DQV describes quality information and lets consumers judge fitness for purpose. ADUC adds source binding, authority, provenance, disclosure, lifecycle, and deterministic AI-consumer rules.

### 3. Uncertainty assertion identity and binding

Every uncertainty assertion contains:

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

The target uses ADR-0006. Units and quantity roles use ADR-0007. Production method and derivation use ADR-0010. Authority, conflict, and lifecycle use ADR-0005.

### 4. Supported v0.1 uncertainty forms

The Core profile supports:

| Type | Required information |
|---|---|
| `standard` | non-negative standard uncertainty in a compatible unit |
| `expanded` | expanded uncertainty, coverage factor, coverage probability, interpretation, and method |
| `relativeStandard` | non-negative unitless relative standard uncertainty |
| `asymmetric` | non-negative lower and upper deviations |
| `interval` | ordered bounds, coverage probability, interpretation, and method |
| `distribution` | distribution IRI and explicit parameters |
| `categorical` | categories, probabilities summing to one, and calibration evidence |
| `unknown` | explicit reason and no fabricated numeric parameter |

The profile does not assert that every domain can be represented adequately by these forms. Domain-specific distributions, spatial uncertainty, ensembles, fuzzy membership, and advanced Bayesian models remain extension territory.

### 5. Absolute, relative, and affine-unit behavior

Numeric uncertainty must use a globally identified compatible unit.

- absolute uncertainty carries the corresponding difference/ordinary quantity role;
- relative uncertainty uses the explicit unitless identifier;
- an affine conversion transforms an absolute uncertainty magnitude using only the absolute scale multiplier;
- the affine offset is applied to the measured value, never to the uncertainty magnitude;
- relative uncertainty is preserved only for purely multiplicative conversion in v0.1;
- conversion output must retain a provenance activity.

For example:

```text
89 °C ± 0.5 °C
→ 192.2 °F ± 0.9 °F
```

The `32` degree offset affects the value, not the `0.5` uncertainty.

### 6. Interval semantics are mandatory

A numeric interval does not explain itself. A coverage interval must declare:

```text
coverageProbability
intervalInterpretation
coverageMethod
```

Supported interpretations are:

```text
coverage
frequentistConfidence
bayesianCredible
prediction
```

A claim such as “95% interval” without a method and interpretation is invalid.

### 7. Model scores and categorical probability

A model score becomes a probability distribution only when the record includes:

```text
calibration method
evaluation dataset binding
calibration evidence
category probabilities summing exactly to one
model-execution provenance
```

Uncalibrated logits, similarity values, confidence labels, or self-reported LLM confidence must not be serialized as probability.

### 8. Exact and zero uncertainty

Zero uncertainty is not inferred from authority, formatting, or repeated identical values.

A zero numeric uncertainty is allowed only when the value is exact by definition and the exactness is backed by a declared method and evidence. Canonical publication alone never establishes exactness.

### 9. Missingness and censoring

Observation state is separate from uncertainty:

```text
observed
missing
censoredBelow
censoredAbove
intervalCensored
```

- missing observations provide a reason and no value;
- censored observations provide a detection or interval limit, compatible unit, and method;
- consumers must not replace censored or missing values with invented exact values;
- imputation is a separate provenance activity and must retain the original observation state.

### 10. Resolution and rounding

Displayed decimal places do not establish uncertainty.

An instrument or encoding resolution may contribute to uncertainty only when resolution is explicitly documented. The v0.1 reference evaluator supports a rectangular resolution contribution:

```text
u = resolution / sqrt(12)
```

Rounding and quantization remain explicit transformation activities.

### 11. Dependence and correlation

Propagation requires a dependence declaration:

```text
independent
correlated
unknown
```

Independent propagation requires evidence. Correlated propagation requires a coefficient in `[-1, 1]` and evidence. Unknown dependence blocks generic propagation.

For the v0.1 reference subset:

```text
u(x + y)^2 = u(x)^2 + u(y)^2 + 2ρu(x)u(y)
```

For multiplication/division, the same expression is applied to relative standard uncertainties in the limited two-input reference case.

The Core does not assume independence merely because no covariance was supplied.

### 12. Deterministic propagation subset

The reference evaluator supports:

1. scale-only uncertainty conversion for exact multiplicative and affine unit conversions;
2. two-input additive propagation of standard uncertainty;
3. two-input multiplicative propagation of relative standard uncertainty;
4. documented rectangular resolution contribution.

Every derived result records its provenance activity and method. Unsupported nonlinear, discontinuous, multivariate, simulation-based, or domain-specific propagation is blocked or delegated to an extension.

### 13. Distribution records

A distribution record identifies its family with an IRI and provides explicit parameters.

The reference subset validates:

- normal distribution with finite mean and non-negative standard deviation;
- rectangular distribution with ordered lower and upper bounds;
- categorical probability distribution with calibration evidence.

The profile does not claim that the named family is correct; authority and evidence remain separate.

### 14. DQV-compatible quality records

Quality is represented through a bundle containing:

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

Each quality measurement identifies:

```text
measurementId
metric
dimension
computedOn
value
unit when applicable
method
provenanceActivity
authority and evidence
```

A quality metric is meaningful only under its declared procedure and target. A score from one metric must not be compared with another metric merely because both are numeric.

### 15. Quality disclosure

Supported disclosure states are:

```text
complete
partial
redacted
unknown
```

`complete` is invalid if a required metric is absent or redacted. `redacted` requires a policy reference. Redaction does not mean the metric was not evaluated.

### 16. Consumer behavior

Automatic use is blocked when:

- uncertainty is contested or deprecated and the result depends on it;
- numeric units are absent or incompatible;
- bounds are reversed or invalid;
- interval interpretation is absent;
- categorical probabilities are uncalibrated;
- dependence is unknown for a requested propagation;
- provenance is missing;
- a quality completeness claim conflicts with missing/redacted metrics;
- an unsupported propagation model would be required.

Unknown uncertainty remains valid information. Consumers must preserve `unknown` rather than replacing it with zero.

### 17. Error families

```text
ADUC-UNC-001   malformed, unbound, or unprovenanced uncertainty assertion
ADUC-UNC-002   authority or exactness is confused with statistical certainty
ADUC-UNC-003   unsupported or conflated uncertainty type
ADUC-UNC-004   uncertainty unit or quantity role is missing/incompatible
ADUC-UNC-005   invalid numeric uncertainty magnitude
ADUC-UNC-006   invalid or uninterpreted interval/coverage claim
ADUC-UNC-007   invalid distribution family or parameters
ADUC-UNC-008   invalid categorical distribution
ADUC-UNC-009   false precision inferred from formatting
ADUC-UNC-010   uncalibrated model score presented as probability
ADUC-UNC-011   unknown uncertainty contains fabricated precision
ADUC-PROP-001  invalid dependence or propagation declaration
ADUC-PROP-002  unknown dependence blocks propagation
ADUC-PROP-003  unsupported or incomplete propagation
ADUC-PROP-004  invalid affine/relative uncertainty transformation
ADUC-DATA-001  invalid observation state
ADUC-DATA-002  missingness is hidden or contradicted
ADUC-DATA-003  censoring or detection-limit evidence is invalid
ADUC-DQV-001   malformed DQV-compatible quality bundle or measurement
ADUC-DQV-002   inconsistent quality disclosure
ADUC-DQV-003   false completeness claim
ADUC-DQV-004   redaction lacks policy or target
```

### 18. Core boundary

The Core standardizes representation, provenance, disclosure, and a small deterministic propagation subset.

The following remain outside generic v0.1 unless expressed by an extension or an external method profile:

- complex covariance matrices;
- Monte Carlo propagation;
- stochastic processes and time-series uncertainty;
- spatial error surfaces;
- ensembles;
- fuzzy sets;
- domain-specific clinical or safety risk scores;
- legal standards of proof;
- universal model calibration procedures.

## Consequences

### Positive

- measurement uncertainty is not confused with mapping confidence;
- canonical data can remain statistically uncertain;
- uncalibrated model scores cannot masquerade as probability;
- unknown, missing, and censored information remains explicit;
- deterministic conversions preserve uncertainty;
- DQV quality metadata can be reused without making quality universal or context-free;
- downstream systems can block unsupported propagation rather than inventing precision.

### Costs

- producers must document methods, units, coverage interpretation, dependence, and provenance;
- some useful calculations remain blocked until domain-specific evidence is supplied;
- quality metrics require explicit definitions and cannot be reduced to one universal score;
- calibrated model probabilities require evaluation evidence.

## Rejected alternatives

### One generic `confidence` property

Rejected because it collapses incompatible semantic, statistical, model, quality, and authority concepts.

### Assume independence when covariance is missing

Rejected because it can systematically understate or overstate propagated uncertainty.

### Infer uncertainty from decimal places

Rejected because display formatting is not metrological evidence.

### Treat every model score as probability

Rejected because probability requires interpretation and calibration evidence.

### Set uncertainty to zero for canonical data

Rejected because authority does not imply exactness.

### Create an ADUC-specific universal quality ontology

Rejected because DQV already provides a framework and quality remains fitness-for-purpose dependent.

## References

- JCGM 100:2008, Evaluation of measurement data — Guide to the expression of uncertainty in measurement: https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf
- JCGM publications: https://www.bipm.org/en/committees/jc/jcgm/publications
- NIST Technical Note 1297: https://www.nist.gov/pml/nist-technical-note-1297
- W3C Data Quality Vocabulary: https://www.w3.org/TR/vocab-dqv/
- W3C PROV-O: https://www.w3.org/TR/prov-o/

## Acceptance evidence

To be completed after CI:

- valid uncertainty and quality reference cases;
- required invalid counterexamples;
- deterministic evaluator and CLI tests;
- GitHub Actions results.

## Follow-up

1. define general relation semantics;
2. define policy and permitted-use boundaries;
3. freeze the normative full-Core object model;
4. implement the full-Core JSON Schema family;
5. unify comparison across semantics, units, time, identity, provenance, uncertainty, relations, and policy.
