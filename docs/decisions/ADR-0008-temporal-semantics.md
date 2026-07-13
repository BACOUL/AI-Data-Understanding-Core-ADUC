# ADR-0008 — Temporal Semantics, Timezone Evidence, and Deterministic Alignment

- Status: accepted
- Date: 2026-07-13
- Issue: #31
- Decision owners: ADUC maintainers

## Context

A semantic mapping and a unit declaration are not sufficient to compare observations across sources. Consumers must distinguish the role of a timestamp, its lexical syntax, precision, timezone evidence, uncertainty, interval boundaries, and whether a duration is elapsed time or a calendar-relative period.

The same local civil text can identify zero, one, or two instants when daylight-saving rules are applied. Timezone rules can change after publication. A numeric UTC offset identifies the offset at one instant but does not identify the rules of a named timezone. Locale-specific strings such as `13/07/2026 14:00` are not portable without an explicit format and locale.

ADUC must reuse established temporal standards rather than create a new calendar or timezone database.

## Decision

### 1. Reuse established temporal standards

ADUC v0.1 uses:

- RFC 3339 for fixed instants with an explicit UTC offset;
- RFC 9557 / IXDTF when a fixed timestamp carries additional timezone annotations;
- IANA Time Zone Database identifiers and pinned releases for civil-time resolution;
- ISO 8601 lexical forms for dates, durations, and periods;
- OWL-Time identifiers and interval relations where RDF interoperability is required.

ADUC adds source binding, epistemic authority, uncertainty, role separation, pinned evidence, and deterministic consumer rules. It does not replace those standards.

### 2. Separate temporal kinds

The Core distinguishes:

| Kind | Meaning | Automatic instant comparison |
|---|---|---|
| `instant` | A fixed point with a UTC relationship. | Allowed. |
| `localDateTime` | A civil date-time requiring timezone evidence. | Allowed only after deterministic resolution. |
| `date` | A calendar date without a time-of-day. | Not an instant without an explicit interpretation. |
| `timeOfDay` | A clock reading without a date. | Not an instant. |
| `exactDuration` | Elapsed duration reducible to exact seconds in v0.1. | Allowed as a duration. |
| `calendarPeriod` | Calendar-relative years or months. | Context required. |
| `interval` | Start, end, and explicit boundary semantics. | Allowed after both endpoints resolve. |

No consumer may silently upgrade a date, time-of-day, or unresolved local date-time into an instant.

### 3. Separate temporal roles

Temporal values declare one role:

```text
observation
event
publication
processing
validity
sampling
aggregation
```

Values with different roles are not automatically interchangeable. Observation time and publication time may be compared only through an explicit application rule, never by default.

### 4. Preserve lexical and parsed representations

A temporal assertion preserves:

```text
source lexical value
declared lexical format
locale when relevant
parsed local or fixed value
precision
timezone or offset evidence
parser or method identifier and version
epistemic authority
source binding and local reference
```

Non-standard or locale-dependent syntax requires a declared format. The reference parser never guesses whether `10/11/2026` is day-first or month-first.

### 5. Fixed instants

A fixed instant uses RFC 3339 with `Z` or a numeric offset. A named timezone annotation may accompany the timestamp, but the offset must agree with the pinned timezone rules at that instant.

A fixed offset is not equivalent to a named timezone. It describes one UTC relationship, not future or historical civil-time rules.

### 6. Local civil time resolution

A `localDateTime` becomes an instant only when all of the following exist:

1. a source-bound lexical value;
2. a declared lexical format and locale where needed;
3. a named IANA timezone identifier;
4. a pinned timezone database release and SHA-256 digest;
5. an active, non-contested temporal assertion;
6. an explicit occurrence when the civil time is ambiguous.

Resolution outcomes are:

```text
resolved
ambiguous
nonexistent
insufficientEvidence
```

The reference evaluator rejects ambiguous and nonexistent values rather than choosing silently.

### 7. Pin timezone evidence

Reproducible resolution identifies:

```text
timezone registry identifier
IANA release
release or derived-snapshot date
SHA-256 digest
timezone identifier
offset selected
transition evidence
```

The repository reference snapshot is a small, test-only subset derived from IANA TZDB `2026c`, released 2026-07-08. It is not a competing timezone database.

### 8. Civil-time gaps and overlaps

During a forward transition, some local times do not exist. They return `ADUC-TZ-005`.

During a backward transition, some local times occur twice. They return `ADUC-TZ-004` unless the assertion declares:

```text
occurrence: earlier
```

or:

```text
occurrence: later
```

The occurrence is evidence and remains in transformation provenance.

### 9. Precision and uncertainty

Precision and uncertainty are separate.

Examples:

- `2026-07-13T12:00Z` has minute precision;
- `2026-07-13T12:00:00Z` has second precision;
- a sensor may report second precision with ±5 seconds uncertainty.

A resolved instant may carry asymmetric uncertainty:

```text
beforeSeconds
afterSeconds
```

Comparators use the resulting uncertainty interval. Overlapping uncertainty ranges establish only `possibleOverlap`, not exact simultaneity.

### 10. Intervals and boundaries

An interval requires:

```text
start
end
startBoundary: inclusive | exclusive
endBoundary: inclusive | exclusive
```

Unknown boundary semantics block comparison. The reference evaluator reports deterministic relations including:

```text
equal
before
after
meets
metBy
contains
during
overlaps
```

The model reuses OWL-Time interval relation identifiers when serialized as RDF.

### 11. Distinguish exact durations and calendar periods

`exactDuration` supports ISO 8601 day/hour/minute/second values that reduce deterministically to elapsed seconds, such as `PT15M`.

`calendarPeriod` preserves values such as `P1M` or `P1Y`. It is not converted to fixed seconds without a calendar anchor and explicit method.

### 12. Distinguish resolution, sampling, aggregation, and validity

These are separate claims:

- `precision`: smallest expressed component of one temporal value;
- `sampling`: intended spacing between observations;
- `aggregation`: time window summarized by one value;
- `validity`: interval during which a statement or contract applies.

The string `PT15M` must not be reused for all four without explicit roles.

### 13. Transformation provenance

Every temporal normalization report records:

```text
input lexical value
parsed value
resolved UTC instant or interval
timezone identifier and selected offset
timezone registry identifier, version, and digest
parser or method identifier and version
precision and uncertainty
epistemic authority
source field binding
```

### 14. Migration

Legacy fields migrate as follows:

| Legacy field | Migration |
|---|---|
| `timeField` | source-bound temporal assertion with a structured local reference |
| `timezone` | named timezone evidence, never a complete instant by itself |
| `timeResolution` | sampling or precision only after reviewed role classification |
| RFC 3339 string | `instant` with preserved lexical value and offset |
| local date string | `localDateTime`; remains unresolved until format, locale, and timezone evidence exist |

Migration never upgrades authority or invents an occurrence for an ambiguous civil time.

## Reference error families

```text
ADUC-TIME-001       invalid or unsupported temporal value
ADUC-TIME-002       lexical format or locale evidence is missing
ADUC-TIME-006       precision is missing or inconsistent
ADUC-TIME-007       temporal uncertainty is invalid
ADUC-TIME-008       unsupported leap-second processing
ADUC-TIME-009       source binding or local reference is missing
ADUC-TIME-010       epistemic or lifecycle state blocks use
ADUC-TIME-ROLE-001  temporal roles are incompatible
ADUC-TZ-001         timezone registry evidence is missing or mismatched
ADUC-TZ-002         named timezone evidence is missing or unknown
ADUC-TZ-003         fixed offset is used as a substitute for timezone rules
ADUC-TZ-004         civil time is ambiguous
ADUC-TZ-005         civil time does not exist
ADUC-TZ-006         timestamp offset conflicts with named timezone rules
ADUC-DURATION-001   exact duration syntax is invalid
ADUC-DURATION-002   calendar period syntax is invalid
ADUC-DURATION-003   contextual calendar conversion was requested
ADUC-INTERVAL-001   interval boundary semantics are missing
ADUC-INTERVAL-002   interval is empty or reversed
ADUC-ALIGN-001      temporal kinds cannot be aligned
ADUC-ALIGN-003      requested relation is not justified
```

## Consequences

### Positive

- the French and UTC reference timestamps resolve to the same instant;
- timezone rule changes are visible through registry version and digest;
- DST gaps and overlaps cannot be hidden;
- temporal roles remain distinct;
- uncertainty prevents false simultaneity;
- exact durations and calendar periods remain distinct;
- interval comparison is deterministic.

### Costs

- timezone snapshots or releases must be pinned;
- local date parsing requires explicit metadata;
- some temporal values remain unresolved until human review;
- leap seconds, non-Gregorian calendars, recurrences, and open-ended intervals need later profiles.

## Rejected alternatives

### Treat every timestamp-looking string as UTC

Rejected because unqualified local times are not globally interoperable.

### Store only a UTC offset

Rejected because an offset does not represent timezone rules across dates.

### Always select the first DST occurrence

Rejected because it silently changes meaning.

### Convert every ISO duration to seconds

Rejected because months and years are calendar-relative.

### Treat all timestamps as the same role

Rejected because observation, publication, and processing time answer different questions.

### Depend on the live system timezone database

Rejected for reproducible claims because results can change after timezone rule updates.

## References

- RFC 3339: https://www.rfc-editor.org/rfc/rfc3339
- RFC 9557: https://www.rfc-editor.org/rfc/rfc9557
- IANA Time Zone Database: https://www.iana.org/time-zones
- W3C Time Ontology in OWL: https://www.w3.org/TR/owl-time/
- ISO 8601 overview: https://www.iso.org/iso-8601-date-and-time-format.html

## Follow-up

After acceptance:

1. define entity identity and equivalence;
2. define remaining Core blocks and schema boundaries;
3. implement the first full-Core JSON Schema family;
4. upgrade comparison and interoperability examples with source, unit, time, and identity evidence.
