# ADUC Unit Profile 0.1

- Status: working draft
- Date: 2026-07-13
- Decision: ADR-0007
- Scope: quantity kinds, unit identity, dimensional compatibility, conversion, uncertainty, and provenance

## 1. Purpose

This profile defines how an ADUC contract associates a source-bound field with a quantity kind and unit, and how consumers decide whether two values can be converted.

It does not create a new unit catalog. It profiles external identifiers and pinned conversion data.

## 2. Normative foundations

The v0.1 reference profile uses:

- QUDT quantity-kind IRIs;
- QUDT unit IRIs;
- QUDT dimension-vector IRIs;
- case-sensitive UCUM codes as compact aliases where available;
- a pinned and hashed conversion-registry snapshot;
- ADR-0005 epistemic authority;
- ADR-0006 source and local-reference binding.

A consumer MUST preserve the vocabulary/version and registry digest used for each conversion.

## 3. Unit assertion

Candidate shape:

```json
{
  "id": "urn:aduc:unit-assertion:temperature-fr",
  "localReference": {
    "scheme": "json-pointer",
    "base": "resource",
    "value": "/temp"
  },
  "quantityKind": "http://qudt.org/vocab/quantitykind/Temperature",
  "dimensionVector": "http://qudt.org/vocab/dimensionvector/A0E0L0I0M0H1T0D0",
  "quantityRole": "absolute",
  "unitState": "known",
  "unit": {
    "identifier": "http://qudt.org/vocab/unit/DEG_C",
    "ucumCode": "Cel",
    "localUnitCode": "C",
    "displaySymbol": "°C"
  },
  "authorityStatus": "reviewed",
  "assertedBy": "urn:person:reviewer",
  "assertedAt": "2026-07-13T12:00:00Z",
  "evidence": ["urn:evidence:api-documentation"]
}
```

### 3.1 Required properties

| Property | Requirement |
|---|---|
| `id` | Stable identifier of the immutable unit assertion. |
| `localReference` | ADR-0006 structured reference to the source field. |
| `quantityKind` | Absolute IRI identifying the kind of quantity. |
| `dimensionVector` | Absolute IRI identifying the dimensional vector. |
| `quantityRole` | `absolute`, `difference`, or `ordinary`. |
| `unitState` | One of the states defined below. |
| `authorityStatus` | ADR-0005 authority status. |
| `assertedBy` and `assertedAt` | Assertion provenance. |

`unit` is required for `known` and `unitless`, conditional for `arbitrary` and `contextual`, and forbidden for `unknown` unless it contains only unresolved local-code evidence.

## 4. Unit states

### 4.1 `known`

Requirements:

- global `unit.identifier` required;
- registry entry required;
- quantity kind and dimension vector must agree with the registry;
- UCUM code, local code, and display symbol are optional aliases;
- automatic conversion is possible only after all compatibility checks.

### 4.2 `unitless`

Requirements:

- explicit unitless global identifier required;
- dimension vector must be dimensionless;
- quantity kind must be declared;
- absence of a source unit is insufficient evidence.

Reference identifier:

```text
http://qudt.org/vocab/unit/UNITLESS
```

### 4.3 `unknown`

Requirements:

- no global unit identifier;
- unresolved local code may be retained as evidence;
- automatic conversion forbidden;
- consumer output must preserve the unknown state.

### 4.4 `arbitrary`

Requirements:

- procedure identifier and version required;
- measurement method evidence required;
- no generic dimension vector may be invented;
- conversion forbidden unless a procedure-specific verified mapping is supplied.

### 4.5 `contextual`

Requirements:

- context type required;
- required context fields declared;
- generic converter returns `contextRequired` until a suitable context profile is supplied.

Examples include currency, calendar periods, standard-volume gas units, and nonlinear reference-dependent scales.

## 5. Unit object

Candidate properties:

| Property | Meaning |
|---|---|
| `identifier` | Global unit IRI, preferably QUDT in the reference profile. |
| `ucumCode` | Case-sensitive UCUM expression. |
| `localUnitCode` | Exact source code, preserved as source evidence. |
| `displaySymbol` | Human presentation only. |
| `registryEntry` | Optional registry entry identifier when different from unit IRI. |

Rules:

- `localUnitCode` and `displaySymbol` MUST NOT replace `identifier`;
- aliases MUST agree with the pinned registry or remain unverified annotations;
- a source code mapping has its own epistemic authority and evidence.

## 6. Quantity role

Allowed values:

| Role | Meaning |
|---|---|
| `ordinary` | Ratio-scale or otherwise standard value using the unit conversion definition. |
| `absolute` | Point on an affine or other absolute scale. |
| `difference` | Difference or interval; affine offsets do not apply. |

The converter MUST block `absolute` to `difference` and `difference` to `absolute` operations unless a separate transformation explicitly defines the operation.

## 7. Pinned unit registry

Candidate registry metadata:

```json
{
  "registryId": "urn:aduc:unit-registry:reference:0.1",
  "registryVersion": "0.1.0",
  "sourceVocabulary": "http://qudt.org/3.4.0/vocab/unit",
  "digest": {
    "algorithm": "sha-256",
    "value": "...",
    "scope": "raw-bytes"
  },
  "conversionConvention": "reference=(value+offsetBeforeScale)*multiplier"
}
```

A registry entry contains:

```json
{
  "identifier": "http://qudt.org/vocab/unit/DEG_F",
  "ucumCode": "[degF]",
  "quantityKinds": [
    "http://qudt.org/vocab/quantitykind/Temperature",
    "http://qudt.org/vocab/quantitykind/TemperatureDifference"
  ],
  "dimensionVector": "http://qudt.org/vocab/dimensionvector/A0E0L0I0M0H1T0D0",
  "referenceUnit": "http://qudt.org/vocab/unit/K",
  "conversion": {
    "type": "affine",
    "multiplier": {"numerator": "5", "denominator": "9"},
    "offsetBeforeScale": "459.67"
  }
}
```

The registry is evidence used by the converter, not a replacement public vocabulary.

## 8. Numeric representation

Normative conversion parameters use:

- decimal strings; or
- rational objects with integer string numerator and non-zero denominator.

Examples:

```json
"0.01"
```

```json
{"numerator": "5", "denominator": "9"}
```

JSON binary floating-point numbers MUST NOT be normative conversion constants.

## 9. Compatibility algorithm

For source and target assertions:

```text
1. verify source bindings
2. verify assertion authority and active lifecycle
3. reject unknown, contested, deprecated, or unsupported units
4. load and verify the pinned registry
5. resolve both unit identifiers
6. compare declared and registry quantity kinds
7. compare dimension vectors
8. compare quantity roles
9. verify supported conversion types
10. calculate with exact decimal/rational arithmetic
11. propagate supported uncertainty
12. apply declared rounding policy
13. return result and provenance
```

### 9.1 Dimension rule

Dimension vectors MUST be equal.

Equality does not by itself establish semantic compatibility.

### 9.2 Quantity-kind rule

The reference converter requires equal quantity-kind IRIs. A later version may accept an explicit compatibility assertion with its own authority and evidence.

### 9.3 Role rule

- `ordinary` converts to `ordinary`;
- `absolute` converts to `absolute`;
- `difference` converts to `difference`;
- other role combinations are blocked.

## 10. Conversion arithmetic

Each supported unit resolves to a common reference unit for its compatible quantity family.

### 10.1 Absolute or ordinary value

```text
reference = (sourceValue + sourceOffset) × sourceMultiplier
result = reference ÷ targetMultiplier - targetOffset
```

### 10.2 Difference

```text
referenceDifference = sourceValue × sourceMultiplier
resultDifference = referenceDifference ÷ targetMultiplier
```

### 10.3 Example

```text
source: 89 DEG_C
reference: (89 + 273.15) × 1 = 362.15 K
target: 362.15 ÷ (5/9) - 459.67 = 192.2 DEG_F
```

## 11. Rounding and output precision

Every operation declares:

```json
{
  "roundingMode": "half-even",
  "decimalPlaces": 1
}
```

The exact intermediate value is preserved in the report. The rounded output is never substituted for the exact value in provenance.

Supported v0.1 rounding mode:

```text
half-even
```

Additional modes require explicit registration and tests.

## 12. Uncertainty

Supported v0.1 input:

```json
{
  "model": "symmetric-absolute",
  "value": "0.2"
}
```

For scale factor:

```text
scale = |sourceMultiplier / targetMultiplier|
```

propagation is:

```text
outputUncertainty = scale × inputUncertainty
```

Offsets are not applied to uncertainty magnitude.

Unsupported uncertainty models are preserved and reported with `ADUC-UNC-001`; they are not silently discarded.

## 13. Dimensionless values

### 13.1 Explicit unitless

Reference unit:

```text
http://qudt.org/vocab/unit/UNITLESS
```

Reference multiplier:

```text
1
```

### 13.2 Percent

Reference unit:

```text
http://qudt.org/vocab/unit/PERCENT
```

Reference multiplier:

```text
0.01
```

`50 %` therefore converts to unitless ratio `0.5`, only when the quantity kind is compatible.

Counts, angles, logarithmic values, and procedure-defined units remain distinct even if their dimensions are dimensionless.

## 14. Contextual and unsupported conversions

The generic converter blocks:

| Category | Required later context |
|---|---|
| currency | rate, timestamp, source, market/context |
| calendar month/year | calendar, start/end or interpretation |
| standard gas volume | reference temperature and pressure |
| logarithmic scale | nonlinear function and reference quantity |
| arbitrary/procedure unit | method and verified procedure mapping |

A contextual unit may be validly described while remaining non-convertible by the generic v0.1 engine.

## 15. Conversion report

Candidate output:

```json
{
  "status": "converted",
  "input": {
    "value": "89",
    "unit": "http://qudt.org/vocab/unit/DEG_C"
  },
  "output": {
    "exactValue": "192.2",
    "displayValue": "192.2",
    "unit": "http://qudt.org/vocab/unit/DEG_F"
  },
  "quantityKind": "http://qudt.org/vocab/quantitykind/Temperature",
  "quantityRole": "absolute",
  "dimensionVector": "http://qudt.org/vocab/dimensionvector/A0E0L0I0M0H1T0D0",
  "registry": {
    "id": "urn:aduc:unit-registry:reference:0.1",
    "version": "0.1.0",
    "sha256": "..."
  },
  "formula": "affine-v0.1",
  "rounding": {
    "mode": "half-even",
    "decimalPlaces": 1
  },
  "sourceBinding": "urn:aduc:source-binding:temperature-fr"
}
```

## 16. Error codes

| Code | Meaning |
|---|---|
| `ADUC-UNIT-001` | Unit identifier is absent from the pinned registry. |
| `ADUC-UNIT-002` | Unit state and unit object are inconsistent. |
| `ADUC-UNIT-003` | A local symbol/code is used as a global identifier. |
| `ADUC-UNIT-004` | Quantity kind or dimension vector is missing/inconsistent. |
| `ADUC-COMPAT-001` | Dimension vectors differ. |
| `ADUC-COMPAT-002` | Quantity kinds differ. |
| `ADUC-COMPAT-003` | Quantity roles differ. |
| `ADUC-CONV-001` | Conversion type is unsupported. |
| `ADUC-CONV-002` | Required contextual conversion data is missing. |
| `ADUC-CONV-003` | Unknown, arbitrary, contested, or unresolved unit blocks conversion. |
| `ADUC-CONV-004` | Registry identifier, version, or digest mismatch. |
| `ADUC-CONV-005` | Rounding policy is absent or unsupported. |
| `ADUC-UNC-001` | Uncertainty model cannot be propagated. |

## 17. Migration

Migration retains the original source code and creates a separate mapping:

```json
{
  "localUnitCode": "C",
  "identifier": "http://qudt.org/vocab/unit/DEG_C",
  "authorityStatus": "reviewed",
  "evidence": ["urn:evidence:source-documentation"]
}
```

A legacy value such as `C` or `F` without documentation remains unresolved or inferred. It is not canonicalized by string matching alone.

## 18. Reference artifacts

```text
examples/units/registry.json
examples/units/reference-cases.json
examples/units/invalid-cases.json
tools/aduc_units.py
tests/units/test_units.py
```

## 19. Conformance limits

This profile does not prove:

- that a quantity kind is factually correct for a field;
- that a QUDT or UCUM mapping was published by the source owner;
- that an input measurement is accurate;
- that currency or calendar conversion context is valid;
- that a nonlinear conversion is safe;
- that measurement uncertainty is complete.

Those claims require epistemic evidence, provenance, temporal context, policy, or later profiles.

## 20. References

- QUDT overview: https://www.qudt.org/pages/QUDToverviewPage.html
- QUDT Unit schema: https://qudt.org/schema/qudt/Unit
- QUDT units 3.4.0: https://qudt.org/3.4.0/vocab/unit
- QUDT quantity kinds 3.4.0: https://qudt.org/3.4.0/vocab/quantitykind
- UCUM 2.2: https://ucum.org/ucum
