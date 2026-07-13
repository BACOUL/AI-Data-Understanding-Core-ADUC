# ADUC Temporal Profile 0.1

- Status: working draft
- Date: 2026-07-13
- Decision: ADR-0008
- Scope: temporal kinds, roles, lexical evidence, timezone resolution, intervals, duration classes, uncertainty, and deterministic alignment

## 1. Purpose

This profile defines how ADUC records temporal meaning without guessing locale, timezone, role, precision, or calendar context.

It does not replace RFC 3339, RFC 9557, ISO 8601, the IANA Time Zone Database, or OWL-Time.

## 2. Normative principles

1. Every temporal assertion is bound to an exact source and local field through ADR-0006.
2. A lexical value and its interpreted value are separate records.
3. A local date-time is not an instant until timezone resolution succeeds.
4. A fixed UTC offset is not a timezone identifier.
5. Timezone rules used for reproducible resolution are pinned by version and digest.
6. Ambiguous and nonexistent civil times block automatic use.
7. Temporal roles are explicit.
8. Precision and uncertainty are explicit and separate.
9. Interval boundaries are explicit.
10. Exact durations and calendar periods are distinct.
11. Inferred parsing never becomes reviewed, verified, or canonical automatically.

## 3. Temporal assertion envelope

A temporal assertion contains:

```json
{
  "kind": "localDateTime",
  "role": "observation",
  "sourceBinding": "urn:aduc:binding:machine-fr",
  "localReference": {
    "scheme": "json-pointer",
    "value": "/date"
  },
  "lexicalValue": "13/07/2026 14:00",
  "lexicalFormat": "%d/%m/%Y %H:%M",
  "locale": "fr-FR",
  "precision": "minute",
  "timeZone": "Europe/Paris",
  "authorityStatus": "reviewed",
  "parser": {
    "id": "urn:aduc:parser:declared-format",
    "version": "1"
  }
}
```

## 4. Kinds

### 4.1 `instant`

A fixed timestamp with an explicit RFC 3339 offset.

```json
{
  "kind": "instant",
  "lexicalValue": "2026-07-13T12:00:00Z",
  "precision": "second"
}
```

### 4.2 `localDateTime`

A civil date-time that requires format, locale where relevant, named timezone, and pinned timezone evidence.

### 4.3 `date`

A calendar date. It does not identify a UTC instant without an application rule.

### 4.4 `timeOfDay`

A local clock value without a date. It does not identify an instant.

### 4.5 `exactDuration`

Elapsed duration reducible to seconds using day/hour/minute/second components.

```json
{
  "kind": "exactDuration",
  "lexicalValue": "PT15M"
}
```

### 4.6 `calendarPeriod`

Calendar-relative period requiring an anchor and method for elapsed-time conversion.

```json
{
  "kind": "calendarPeriod",
  "lexicalValue": "P1M"
}
```

### 4.7 `interval`

```json
{
  "kind": "interval",
  "start": {},
  "end": {},
  "startBoundary": "inclusive",
  "endBoundary": "exclusive"
}
```

## 5. Roles

Allowed v0.1 roles:

```text
observation
event
publication
processing
validity
sampling
aggregation
```

Consumers must not align different roles automatically.

## 6. Lexical evidence

### 6.1 RFC 3339

Fixed instants use RFC 3339. The reference implementation requires uppercase `T` and `Z` and an explicit offset.

### 6.2 Local syntax

Local values require `lexicalFormat`. Locale-dependent formats also require `locale`.

The reference evaluator supports only the formats needed by official examples:

```text
%d/%m/%Y %H:%M
%Y-%m-%dT%H:%M
%Y-%m-%dT%H:%M:%S
```

This limited parser is a conformance tool, not a universal date parser.

## 7. Timezone registry reference

```json
{
  "path": "tzdb-reference-2026c.json",
  "registryId": "urn:aduc:tzdb-reference:2026c:subset-1",
  "registryVersion": "2026c",
  "sha256": "22ce17e221227695651a96d27f35f05af7381d1db59ff22394e89cadd0079f27"
}
```

The registry digest covers exact repository bytes. The snapshot is a minimal reference subset derived from IANA TZDB 2026c.

## 8. Resolution algorithm

For each applicable timezone period:

1. subtract the period offset from the local civil value;
2. test whether the resulting UTC candidate falls inside that period;
3. collect valid candidates.

Outcomes:

- zero candidates: nonexistent civil time;
- one candidate: resolved;
- two candidates: ambiguous and requires `occurrence`;
- more than two candidates: unsupported registry data.

For an overlap:

```json
{
  "occurrence": "earlier"
}
```

or:

```json
{
  "occurrence": "later"
}
```

is mandatory.

## 9. Precision

Allowed values:

```text
date
hour
minute
second
fraction
```

The declaration must agree with the lexical value. Precision does not imply measurement accuracy.

## 10. Uncertainty

```json
{
  "uncertainty": {
    "beforeSeconds": 5,
    "afterSeconds": 10
  }
}
```

The comparator derives a closed uncertainty interval around the resolved instant.

## 11. Interval semantics

Both boundaries are mandatory:

```text
inclusive
exclusive
```

The reference implementation reports:

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

RDF representations should reuse OWL-Time relations.

## 12. Alignment

### 12.1 Instants

Two exact instants with the same UTC value and zero uncertainty are `equal`.

If uncertainty intervals overlap but exact equality is not established, the relation is `possibleOverlap`.

If uncertainty intervals are disjoint, the relation is `before` or `after`.

### 12.2 Intervals

Intervals are compared only after both endpoints resolve and boundary conventions are known.

### 12.3 Role compatibility

Different temporal roles return `ADUC-TIME-ROLE-001`.

## 13. Duration rules

`PT15M` is an exact duration of 900 seconds.

`P1M` is a calendar period and returns `contextRequired`. It must not be normalized to a fixed number of seconds without an anchor and method.

## 14. Transformation report

A successful local resolution records:

```json
{
  "sourceLexicalValue": "13/07/2026 14:00",
  "sourceLexicalFormat": "%d/%m/%Y %H:%M",
  "locale": "fr-FR",
  "localDateTime": "2026-07-13T14:00:00",
  "timeZone": "Europe/Paris",
  "utcOffset": "+02:00",
  "instantUtc": "2026-07-13T12:00:00Z",
  "precision": "minute",
  "authorityStatus": "reviewed",
  "timezoneProvenance": {
    "registryVersion": "2026c",
    "sha256": "22ce17e221227695651a96d27f35f05af7381d1db59ff22394e89cadd0079f27"
  }
}
```

## 15. Required reference conclusions

The reference suite proves:

1. `13/07/2026 14:00` in `Europe/Paris` resolves to `2026-07-13T12:00:00Z`;
2. the French and UTC source values align as the same observation instant;
3. `2026-10-25T02:30:00` in Paris is ambiguous;
4. `2026-03-29T02:30:00` in Paris does not exist;
5. explicit earlier and later overlap occurrences resolve differently;
6. `PT15M` equals 900 exact seconds;
7. `P1M` remains calendar-relative;
8. compatible intervals align deterministically;
9. overlapping uncertainty does not prove exact simultaneity.

## 16. Non-goals for v0.1

The reference implementation does not yet support:

- leap-second normalization;
- non-Gregorian calendars;
- recurring schedules;
- open-ended intervals;
- historical Paris rules outside the bundled reference periods;
- timezone boundary geography;
- live timezone registry updates;
- natural-language date parsing.

## 17. Conformance command

```bash
python tools/aduc_time.py \
  examples/time/reference-cases.json \
  examples/time/invalid-cases.json
```

Success requires all valid cases and all expected rejections to pass.
