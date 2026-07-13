# Next Action

## Single active task

Define and accept the ADUC unit identifier and conversion strategy before implementing the full-Core JSON Schema.

Create:

```text
docs/decisions/ADR-0007-units-and-conversion.md
spec/UNIT_PROFILE_0_1.md
examples/units/
```

## Objective

Define exactly how ADUC identifies units, distinguishes quantities from units, verifies dimensional compatibility, represents unitless and unknown values, and permits deterministic conversions without inventing domain meaning.

## Completed dependency

The source-description binding model is now specified and reference-tested through:

```text
docs/decisions/ADR-0006-source-description-and-binding.md
spec/SOURCE_DESCRIPTION_PROFILE_0_1.md
tools/aduc_source_binding.py
examples/source-description/
```

Every future unit assertion and conversion test must remain bound to the exact source, description version, and local field established by that model.

## Cross-cutting adoption constraint

The official [`ADOPTION_AND_VALUE_VALIDATION.md`](ADOPTION_AND_VALUE_VALIDATION.md) plan remains mandatory for later compiler, review, and interoperability work.

Do not implement the JSON/CSV compiler now. The future compiler may propose units only as `inferred`, must declare its evidence mode and method version, and must expose ambiguous or incompatible units for review.

## Required decisions

1. which existing unit vocabularies or code systems ADUC reuses rather than replaces;
2. how a field identifies its physical quantity or kind of quantity separately from its unit;
3. the canonical identifier form for SI and non-SI units in v0.1;
4. how compound units, prefixes, scale, offset, and affine conversions are represented;
5. how consumers determine dimensional compatibility before conversion;
6. how unitless, count, ratio, percentage, currency, logarithmic, calendar, and unknown-unit values are represented;
7. whether conversion formulas are embedded, referenced, or both;
8. how exact, approximate, contextual, and forbidden conversions are distinguished;
9. how precision, rounding, significant figures, uncertainty, and provenance are preserved;
10. how legacy mapping-profile examples migrate into the full-Core unit model.

## Required counterexamples

The specification must reject or explicitly block:

- treating Celsius and Fahrenheit as simple multiplicative conversions;
- converting incompatible dimensions because their values look similar;
- assuming a unit from a field name without an inferred assertion and evidence;
- treating an unknown unit as unitless;
- treating percentage and ratio as interchangeable without an explicit scale;
- applying a currency conversion without time, rate source, and provenance;
- converting calendar months to fixed seconds without a declared context;
- dropping uncertainty or precision during conversion;
- using an unversioned private unit code as if it were globally portable;
- silently selecting one interpretation when a unit symbol is ambiguous.

## Compatibility requirement

Current examples that use strings such as:

```text
unit:DegreeCelsius
unit:CubicMetrePerSecond
C
F
```

must receive a documented migration path. The new model must preserve the difference between a human display symbol, a local source code, and a globally resolvable unit identifier.

## Scope boundary

Do not implement the full-Core schema, temporal strategy, entity-identity strategy, compiler, review UI, registry, MCP adapter, extensions, or anticipation engine in this task.

## Completion test

An independent implementer must be able to:

1. identify and compare units for the reference Celsius/Fahrenheit and river-flow examples;
2. prove dimensional compatibility before conversion;
3. calculate 89 °C = 192.2 °F deterministically;
4. reject at least one dimensionally incompatible conversion;
5. preserve uncertainty and conversion provenance;
6. distinguish unknown unit, unitless value, local unit code, and global unit identifier without private guidance.
