# ADR-0007 — Unit Identifiers, Dimensional Compatibility, and Conversions

- Status: proposed
- Date: 2026-07-13
- Issue: #29
- Decision owners: ADUC maintainers

## Context

A semantic field mapping is not sufficient to compare numeric values. Consumers must know the quantity being expressed, the exact unit, whether the quantity is absolute or a difference, whether conversion is mathematically valid, and which source supplied the conversion rule.

Display symbols are unsafe identifiers. `C` may denote coulomb, Celsius in an informal source, or a private code. `%` is not the same numeric scale as the unitless ratio `1`. Celsius and Fahrenheit are affine scales for absolute temperature, not simple multiplicative units. Currency, calendar duration, logarithmic scales, and procedure-defined units require context that cannot be reduced to a universal constant factor.

ADUC must reuse established unit vocabularies rather than create a competing catalog.

## Decision

### 1. Separate quantity kind, dimension, unit, and local code

A unit assertion contains distinct claims:

```text
source-bound local field
quantity kind
dimension vector
unit state
global unit identifier or local procedure identifier
local source code or display symbol
epistemic authority and evidence
```

A symbol or source code never acts as a global identifier by itself.

### 2. Prefer QUDT IRIs and retain UCUM codes

For v0.1 reference profiles:

- QUDT quantity-kind IRIs are the preferred semantic identifiers for kinds of quantity;
- QUDT unit IRIs are the preferred global unit identifiers;
- QUDT dimension-vector IRIs are the preferred dimensional compatibility identifiers;
- case-sensitive UCUM codes are retained as compact machine-exchange codes where QUDT supplies an unambiguous mapping;
- display symbols remain non-normative presentation metadata.

An implementation may support another established vocabulary through a versioned mapping profile, but it must not silently equate identifiers from different vocabularies.

### 3. Pin the unit registry used for conversion

Conversions do not rely on a mutable remote vocabulary at execution time.

A conversion operation identifies a verified unit-registry snapshot by:

```text
registry identifier
vocabulary/version
SHA-256 digest
conversion convention
```

The registry may be a pinned QUDT-derived subset or another accepted profile. Unit identifiers remain external vocabulary identifiers; the pinned registry supplies the exact conversion data used by the operation.

### 4. Define unit states

ADUC distinguishes:

| State | Meaning | Automatic conversion |
|---|---|---|
| `known` | Resolved global unit identifier and verified registry entry. | Allowed when compatibility rules pass. |
| `unitless` | Explicitly no unit, with a declared dimensionless quantity kind. | Allowed only among compatible dimensionless scales. |
| `unknown` | Source unit is absent or unresolved. | Forbidden. |
| `arbitrary` | Procedure-defined unit whose meaning depends on a declared method. | Forbidden except through an explicit procedure-specific mapping. |
| `contextual` | Conversion requires external context such as exchange rate, calendar interval, or reference condition. | Forbidden without the required context profile. |

`unknown` is not equivalent to `unitless`.

### 5. Require quantity-kind compatibility

Matching dimension vectors are necessary but not always sufficient.

The v0.1 reference converter requires:

1. equal dimension vectors;
2. equal quantity-kind identifiers, or an explicit versioned compatibility assertion;
3. compatible quantity roles;
4. supported conversion type;
5. active, non-contested unit assertions.

This prevents a consumer from treating every dimensionless value as interchangeable or converting absolute temperature as a temperature difference.

### 6. Distinguish absolute values from differences

Temperature fields declare:

```text
quantityRole: absolute
```

or:

```text
quantityRole: difference
```

For an absolute affine unit, conversion to the reference unit is:

```text
reference = (value + offsetBeforeScale) × multiplier
```

For a difference, the offset is ignored:

```text
referenceDifference = value × multiplier
```

An absolute value and a difference are not automatically comparable even when they share a dimension vector.

### 7. Support exact multiplicative and affine conversions in v0.1

Supported conversion types:

- `identity`;
- `multiplicative`;
- `affine`.

Numeric parameters are represented as exact decimal strings or rational numerator/denominator pairs. Binary floating-point constants are not normative conversion data.

Nonlinear, logarithmic, table-based, currency, calendar-dependent, and other contextual conversions are outside the generic v0.1 converter and return `contextRequired` or `unsupported`.

### 8. Conversion formula

For source value `x`, source multiplier `ms`, source offset `os`, target multiplier `mt`, and target offset `ot`:

```text
reference = (x + os) × ms
result = reference ÷ mt - ot
```

For `quantityRole: difference`, both offsets are zero for the operation.

The reference converter uses decimal/rational arithmetic and a declared rounding policy.

### 9. Preserve precision, uncertainty, and provenance

A conversion report records:

```text
input lexical value
exact intermediate value
output lexical value
rounding mode and scale
source and target unit identifiers
quantity kind and role
dimension vector
registry identifier, version, and digest
conversion formula type
source field binding
```

For a symmetric absolute uncertainty `u` under an affine conversion, only the scale factor applies:

```text
u_target = |ms ÷ mt| × u_source
```

Offsets do not change uncertainty magnitude. More complex uncertainty models are preserved as unresolved unless a declared method supports them.

### 10. Handle dimensionless scales explicitly

`unitless` and percent share a dimension vector but not the same scale.

- unitless ratio uses multiplier `1`;
- percent uses multiplier `0.01`;
- conversion requires a compatible dimensionless quantity kind;
- counts, angles, logarithmic values, and arbitrary units are not collapsed into one generic dimensionless category.

### 11. Block contextual conversions without context

Examples:

- currency requires rate, timestamp, source, and applicable market/context;
- calendar months require a start/end or calendar interpretation;
- standard-volume gas units require reference temperature and pressure;
- logarithmic units require their defined reference and nonlinear function;
- arbitrary assay units require the measurement procedure.

The generic converter must not invent this context.

### 12. Bind unit assertions to sources

Every unit assertion uses ADR-0006 source binding and a deterministic local reference. A unit inferred from a field name remains `inferred` with evidence; it does not become canonical because its symbol is common.

### 13. Migration

Legacy examples migrate as follows:

| Legacy value | Migration |
|---|---|
| `unit:DegreeCelsius` | map through a reviewed migration table to `http://qudt.org/vocab/unit/DEG_C` |
| `unit:CubicMetrePerSecond` | map to `http://qudt.org/vocab/unit/M3-PER-SEC` |
| local `C` | preserve as `localUnitCode`; create a separate epistemic mapping to the QUDT unit |
| local `F` | preserve as `localUnitCode`; never infer Fahrenheit without evidence |
| absent unit | `unknown`, unless the source explicitly declares a unitless quantity |

Migration never upgrades authority.

## Reference error families

```text
ADUC-UNIT-001  unit identifier is unknown to the pinned registry
ADUC-UNIT-002  unit state and identifier are inconsistent
ADUC-UNIT-003  local symbol or code is used as a global identifier
ADUC-UNIT-004  quantity kind or dimension vector is missing
ADUC-COMPAT-001 dimension vectors are incompatible
ADUC-COMPAT-002 quantity kinds are incompatible
ADUC-COMPAT-003 quantity roles are incompatible
ADUC-CONV-001  conversion type is unsupported
ADUC-CONV-002  contextual conversion data is missing
ADUC-CONV-003  ambiguous, contested, or unknown unit blocks conversion
ADUC-CONV-004  registry digest or version does not match
ADUC-CONV-005  rounding or precision policy is missing
ADUC-UNC-001   uncertainty model cannot be propagated by the declared method
```

## Consequences

### Positive

- the reference Celsius/Fahrenheit conversion is deterministic;
- dimensions are checked before arithmetic;
- percent and ratio remain distinct;
- unknown, arbitrary, and contextual units do not silently become convertible;
- unit conversion can be reproduced from pinned evidence;
- QUDT and UCUM are reused instead of duplicated.

### Costs

- a unit-registry snapshot must be pinned and maintained;
- quantity kinds must be declared, not merely dimensions;
- some common conversions remain blocked until temporal or contextual profiles exist;
- legacy symbols require reviewed mappings.

## Rejected alternatives

### Use display symbols as identifiers

Rejected because symbols are ambiguous and presentation-oriented.

### Use only dimension vectors

Rejected because quantities with the same dimensions are not necessarily semantically interchangeable.

### Put every conversion formula directly in each contract

Rejected because it duplicates authority, increases drift, and allows unreviewed formulas to masquerade as standard conversions.

### Treat unknown as unitless

Rejected because it creates false comparability.

### Convert every dimensionless value freely

Rejected because ratio, percent, count, angle, logarithmic scales, and arbitrary units have different semantics.

### Use binary floating point as normative conversion data

Rejected because results may vary and exact decimal/rational relationships are lost.

## References

- QUDT Ontologies Overview: https://www.qudt.org/pages/QUDToverviewPage.html
- QUDT Unit schema: https://qudt.org/schema/qudt/Unit
- QUDT unit vocabulary: https://qudt.org/3.4.0/vocab/unit
- QUDT quantity-kind vocabulary: https://qudt.org/3.4.0/vocab/quantitykind
- UCUM 2.2: https://ucum.org/ucum
- BIPM SI Brochure and digital SI resources: https://www.bipm.org/en/measurement-units

## Follow-up

After acceptance:

1. define temporal semantics and timezone alignment;
2. define entity identity and equivalence;
3. define remaining Core blocks and schema boundaries;
4. implement the first full-Core JSON Schema family.
