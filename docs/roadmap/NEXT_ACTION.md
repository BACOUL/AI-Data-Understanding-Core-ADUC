# Next Action

## Single active task

Define and accept the ADUC temporal semantics and timezone alignment strategy before implementing the full-Core JSON Schema.

Create:

```text
docs/decisions/ADR-0008-temporal-semantics.md
spec/TEMPORAL_PROFILE_0_1.md
examples/time/
```

## Objective

Define exactly how ADUC represents instants, local date-times, dates, durations, intervals, recurrence or sampling resolution, validity periods, timezone evidence, ambiguous civil times, and deterministic alignment between sources.

## Completed dependencies

The source-description binding model and unit and conversion profile are now specified and reference-tested through:

```text
docs/decisions/ADR-0006-source-description-and-binding.md
spec/SOURCE_DESCRIPTION_PROFILE_0_1.md
docs/decisions/ADR-0007-units-and-conversion.md
spec/UNIT_PROFILE_0_1.md
tools/aduc_source_binding.py
tools/aduc_units.py
```

Every temporal assertion must remain bound to the exact source and local field established by ADR-0006. Contextual conversions identified by ADR-0007, such as currencies and calendar periods, must not be enabled until the temporal evidence they require is explicit.

## Cross-cutting adoption constraint

The official [`ADOPTION_AND_VALUE_VALIDATION.md`](ADOPTION_AND_VALUE_VALIDATION.md) plan remains mandatory for later compiler, review, and interoperability work.

Do not implement the JSON/CSV compiler now. The future compiler may propose temporal interpretations only as `inferred`, must record the source format, locale, timezone evidence, parser or model version, and unresolved alternatives, and must surface ambiguous local times for review.

## Required decisions

1. which established temporal standards and identifiers ADUC reuses rather than replaces;
2. how to distinguish an instant, local date-time, date, time-of-day, duration, interval, validity period, observation time, event time, publication time, and processing time;
3. how RFC 3339/ISO 8601 lexical values, IANA timezone identifiers, UTC offsets, and locale-specific source formats are represented;
4. how a local date-time becomes an instant only when sufficient timezone and daylight-saving evidence exists;
5. how ambiguous and nonexistent civil times during timezone transitions are represented and blocked;
6. how interval boundaries and inclusivity are represented;
7. how resolution, sampling period, aggregation window, and validity precision differ;
8. how exact durations differ from calendar periods such as months and years;
9. how two sources are aligned, compared, or declared temporally incompatible;
10. how uncertainty, precision, inferred parsing, timezone-database version, and transformation provenance are preserved;
11. how live or mutable timezone rules are pinned for reproducibility;
12. how legacy fields such as `timeField`, `timezone`, `timeResolution`, and date strings migrate into the full-Core model.

## Required counterexamples

The specification must reject or explicitly block:

- interpreting `13/07/2026 14:00` without a declared format or locale;
- treating a local date-time without timezone evidence as a UTC instant;
- equating a fixed UTC offset with a stable named timezone for future dates;
- silently choosing one occurrence of an ambiguous daylight-saving time;
- accepting a nonexistent civil time during a forward clock transition;
- comparing observation time with publication time as if they were the same role;
- treating a calendar month as a fixed number of seconds without context;
- aligning intervals whose boundary conventions are unknown;
- hiding timestamp precision or rounding;
- using an unversioned timezone database for a reproducibility claim;
- applying an inferred temporal interpretation as canonical;
- declaring two records simultaneous when their uncertainty intervals do not justify that conclusion.

## Compatibility requirement

Current examples that use values such as:

```text
2026-07-13T12:00:00Z
13/07/2026 14:00
Europe/Paris
PT15M
```

must receive a documented migration path. The model must preserve the distinction between source lexical text, parsed local civil time, resolved instant, timezone identifier, UTC offset, resolution, interval, and epistemic authority.

## Scope boundary

Do not implement the full-Core schema, entity-identity strategy, complete policy profile, compiler, review UI, registry service, MCP adapter, extensions, or anticipation engine in this task.

## Completion test

An independent implementer must be able to:

1. resolve the reference French local date-time in `Europe/Paris` to the same instant as `2026-07-13T12:00:00Z` using pinned timezone evidence;
2. distinguish observation, publication, and processing times;
3. align two compatible intervals and reject incompatible or underspecified intervals;
4. detect at least one ambiguous and one nonexistent civil time;
5. distinguish an exact duration from a calendar period;
6. preserve lexical value, precision, uncertainty, timezone-database provenance, and parsing authority without private guidance.
