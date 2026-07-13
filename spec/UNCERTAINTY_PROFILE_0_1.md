# ADUC Uncertainty and Data Quality Profile 0.1

- Status: Working draft
- Decision source: ADR-0011
- Scope: portable representation and deterministic reference behavior for uncertainty, missingness, censoring, propagation, and data quality
- Normative keywords: MUST, MUST NOT, SHOULD, MAY

## 1. Purpose

This profile defines how an ADUC consumer distinguishes:

```text
uncertainty about a value
confidence in a semantic assertion
confidence or probability emitted by a model
quality measured for a resource
authority of the person or organization making a claim
```

These concepts MUST NOT share one undifferentiated `confidence` field.

## 2. External standards

The profile reuses:

- JCGM GUM/VIM concepts for measurement uncertainty;
- W3C DQV concepts for data-quality measurements;
- QUDT/UCUM-aligned unit identity through ADR-0007;
- PROV-O lineage through ADR-0010;
- source binding through ADR-0006;
- epistemic authority and lifecycle through ADR-0005.

ADUC supplies a JSON consumption profile and blocking behavior. It does not replace those standards.

## 3. Uncertainty assertion

A conforming uncertainty assertion has this common shape:

```json
{
  "uncertaintyId": "urn:aduc:uncertainty:flow-118",
  "targetBinding": "urn:aduc:binding:flow-field",
  "uncertaintyType": "standard",
  "quantityKind": "http://qudt.org/vocab/quantitykind/VolumeFlowRate",
  "quantityRole": "ordinary",
  "unit": "http://qudt.org/vocab/unit/M3-PER-SEC",
  "standardUncertainty": "4.72",
  "uncertaintyBasis": "measurementModel",
  "method": "urn:aduc:method:river-flow-gum-v1",
  "provenanceActivity": "urn:aduc:activity:uncertainty-evaluation-1",
  "authorityLevel": "verified",
  "assertedBy": "urn:aduc:org:river-agency",
  "evidence": ["urn:aduc:evidence:calibration-certificate-1"],
  "conflictState": "clear",
  "lifecycleState": "active"
}
```

### 3.1 Common requirements

The following MUST be absolute IRIs:

```text
uncertaintyId
targetBinding
quantityKind
method
provenanceActivity
assertedBy
evidence entries
unit when numeric
```

`quantityRole` MUST be one of:

```text
ordinary
absolute
difference
```

Numeric values MUST be decimal strings. Binary floating-point serialization is not normative.

## 4. Authority and statistical uncertainty

`authorityLevel` follows ADR-0005:

```text
inferred
reviewed
verified
canonical
```

A canonical assertion MUST NOT be interpreted as zero uncertainty.

For `inferred` assertions:

```json
{
  "epistemicConfidence": 0.72,
  "confidenceMethod": "urn:aduc:method:calibrated-inference-v1"
}
```

`epistemicConfidence` concerns support for the assertion, not the magnitude of measurement uncertainty.

## 5. Uncertainty types

### 5.1 Standard uncertainty

```json
{
  "uncertaintyType": "standard",
  "standardUncertainty": "4.72",
  "unit": "http://qudt.org/vocab/unit/M3-PER-SEC"
}
```

The magnitude MUST be non-negative.

### 5.2 Expanded uncertainty

```json
{
  "uncertaintyType": "expanded",
  "expandedUncertainty": "9.44",
  "coverageFactor": "2",
  "coverageProbability": "0.95",
  "intervalInterpretation": "coverage",
  "coverageMethod": "urn:aduc:method:GUM-expanded-k2"
}
```

Coverage factor MUST be positive. Coverage probability MUST be in `(0, 1]`.

### 5.3 Relative standard uncertainty

```json
{
  "uncertaintyType": "relativeStandard",
  "relativeStandardUncertainty": "0.04",
  "unit": "http://qudt.org/vocab/unit/UNITLESS"
}
```

Relative uncertainty MUST use the explicit unitless identifier.

### 5.4 Asymmetric uncertainty

```json
{
  "uncertaintyType": "asymmetric",
  "lowerDeviation": "3",
  "upperDeviation": "5"
}
```

Both deviations MUST be non-negative.

### 5.5 Interval

```json
{
  "uncertaintyType": "interval",
  "lowerBound": "110",
  "upperBound": "126",
  "coverageProbability": "0.95",
  "intervalInterpretation": "frequentistConfidence",
  "coverageMethod": "urn:aduc:method:bootstrap-v2"
}
```

Lower bound MUST be less than upper bound.

Supported interpretations:

```text
coverage
frequentistConfidence
bayesianCredible
prediction
```

### 5.6 Distribution

```json
{
  "uncertaintyType": "distribution",
  "distributionFamily": "urn:aduc:distribution:normal",
  "parameters": {
    "mean": "118",
    "standardDeviation": "4.72"
  }
}
```

The family MUST be identified by an IRI. Parameters MUST be explicit.

The reference evaluator validates normal and rectangular examples only.

### 5.7 Categorical distribution

```json
{
  "uncertaintyType": "categorical",
  "categories": [
    {"category": "urn:aduc:category:normal", "probability": "0.8"},
    {"category": "urn:aduc:category:warning", "probability": "0.15"},
    {"category": "urn:aduc:category:critical", "probability": "0.05"}
  ],
  "calibration": {
    "method": "urn:aduc:method:classifier-calibration-v1",
    "evaluationDatasetBinding": "urn:aduc:binding:evaluation-set-v1",
    "evidence": ["urn:aduc:evidence:calibration-report-v1"]
  }
}
```

Probabilities MUST sum exactly to `1`.

A model score without calibration evidence MUST NOT be represented as probability.

### 5.8 Unknown uncertainty

```json
{
  "uncertaintyType": "unknown",
  "unknownReason": "The publisher supplies no uncertainty model."
}
```

Unknown uncertainty MUST NOT contain fabricated numeric parameters.

## 6. Exactness

A zero uncertainty requires:

```json
{
  "exactByDefinition": true,
  "method": "urn:aduc:method:exact-constant-definition",
  "evidence": ["urn:aduc:evidence:normative-definition"]
}
```

Repeated identical observations, decimal formatting, high authority, or a canonical label are not evidence of exactness.

## 7. Missingness and censoring

Observation state is separate from uncertainty.

### 7.1 Observed

```json
{"state": "observed", "value": "118"}
```

### 7.2 Missing

```json
{"state": "missing", "missingReason": "Sensor offline"}
```

A missing record MUST NOT include a fabricated value.

### 7.3 Censored

```json
{
  "state": "censoredBelow",
  "detectionLimit": "0.2",
  "unit": "http://qudt.org/vocab/unit/M3-PER-SEC",
  "method": "urn:aduc:method:detection-limit-v1"
}
```

Supported states:

```text
censoredBelow
censoredAbove
intervalCensored
```

Imputation MUST be a separate provenance activity.

## 8. Conversion

For a conversion:

```text
y = (x + offset) × multiplier
```

absolute uncertainty is transformed as:

```text
u(y) = |multiplier| × u(x)
```

The offset MUST NOT be applied to the uncertainty magnitude.

Reference example:

```text
89 °C ± 0.5 °C
→ 192.2 °F ± 0.9 °F
```

Relative uncertainty is preserved only for a purely multiplicative conversion in the generic v0.1 profile.

## 9. Dependence

A propagation request MUST declare:

```json
{
  "type": "independent",
  "evidence": ["urn:aduc:evidence:independence-study"]
}
```

or:

```json
{
  "type": "correlated",
  "correlationCoefficient": "0.6",
  "evidence": ["urn:aduc:evidence:correlation-study"]
}
```

`unknown` dependence blocks generic propagation.

## 10. Reference propagation

### 10.1 Additive standard uncertainty

For two inputs:

```text
u² = u₁² + u₂² + 2ρu₁u₂
```

The reference case uses independent uncertainties `3` and `4` and yields `5`.

### 10.2 Multiplicative relative uncertainty

For the limited two-input multiplication/division case, the same equation is applied to relative standard uncertainties.

The reference case uses `0.03` and `0.04` and yields `0.05`.

### 10.3 Resolution contribution

For explicit rectangular resolution:

```text
u = resolution / sqrt(12)
```

A resolution of `0.1` yields the reference standard uncertainty:

```text
0.028867513459481
```

## 11. Data quality

Quality uses a DQV-compatible bundle.

```json
{
  "bundleId": "urn:aduc:quality:river-dataset-v1",
  "computedOn": "urn:aduc:binding:river-dataset-v1",
  "disclosureState": "complete",
  "requiredMetrics": [
    "urn:aduc:metric:completeness",
    "urn:aduc:metric:validity"
  ],
  "measurements": [
    {
      "measurementId": "urn:aduc:quality-measurement:completeness",
      "metric": "urn:aduc:metric:completeness",
      "dimension": "urn:aduc:dimension:completeness",
      "computedOn": "urn:aduc:binding:river-dataset-v1",
      "value": "0.99",
      "unit": "http://qudt.org/vocab/unit/UNITLESS",
      "method": "urn:aduc:method:completeness-v1",
      "provenanceActivity": "urn:aduc:activity:quality-assessment-v1"
    }
  ]
}
```

A quality score is meaningful only under its metric, dimension, target, method, and provenance.

## 12. Quality disclosure

Supported states:

```text
complete
partial
redacted
unknown
```

- `complete` requires every required metric;
- `partial` identifies missing metrics;
- `redacted` identifies redacted metrics and a policy;
- a metric cannot be both missing and redacted.

## 13. Consumer decisions

A consumer MUST preserve an uncertainty assertion but MUST block automatic reliance when:

```text
conflictState = contested
lifecycleState = deprecated
unit is missing or incompatible
interval interpretation is missing
calibration evidence is missing
dependence is unknown
propagation is unsupported
provenance is missing
quality disclosure is internally inconsistent
```

`unknown` is a valid state. It MUST NOT be converted to zero.

## 14. Reference CLI

```bash
python tools/aduc_uncertainty.py \
  examples/uncertainty/reference-cases.json \
  examples/uncertainty/invalid-cases.json
```

JSON report:

```bash
python tools/aduc_uncertainty.py \
  examples/uncertainty/reference-cases.json \
  examples/uncertainty/invalid-cases.json \
  --format json
```

## 15. Error catalogue

The stable v0.1 error families are defined in ADR-0011 and emitted by the reference evaluator.

## 16. Extension boundary

The following require external method profiles or extensions:

```text
large covariance matrices
Monte Carlo propagation
spatial uncertainty
stochastic processes
ensembles
fuzzy membership
domain-specific risk scores
advanced Bayesian models
```

A Core consumer MUST report unsupported uncertainty rather than approximate it silently.
