# ADUC Epistemic Status Model 0.1

- Status: full-Core working draft
- Date: 2026-07-13
- Issue: #23
- Decision: ADR-0005
- Scope: semantic understanding records and deterministic consumer behavior

## 1. Purpose

This specification defines how ADUC represents and consumes the effective states:

```text
unknown
inferred
reviewed
verified
canonical
contested
deprecated
```

The model preserves four independent facts:

1. whether any semantic assertion exists;
2. how an assertion was established;
3. whether it is disputed;
4. whether it remains current.

The seven effective states are therefore computed from several immutable record types rather than stored in one overloaded enum.

## 2. Normative language

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY and OPTIONAL are to be interpreted as normative requirements.

## 3. Record families

A full-Core implementation MUST support the conceptual record families below. Exact JSON property names remain candidate names until the full-Core schema is accepted.

### 3.1 Coverage record

A coverage record states whether a described local reference currently has a semantic resolution.

Candidate properties:

| Property | Requirement | Purpose |
|---|---|---|
| `id` | REQUIRED | Immutable record identifier |
| `source` | REQUIRED | Identified source |
| `validFor` | REQUIRED | Exact source or schema version |
| `localReference` | REQUIRED | Field or value being assessed |
| `resolutionStatus` | REQUIRED | `unknown` in this version |
| `reason` | REQUIRED | Structured unresolved reason |
| `recordedBy` | REQUIRED | Actor or process recording coverage |
| `recordedAt` | REQUIRED | Record issuance time |
| `evidence` | OPTIONAL | Documentation or inspection references |

A coverage record with `resolutionStatus: unknown` MUST NOT contain `semanticTarget`, `mappingRelation`, `confidence` or `confidenceMethod`.

Candidate unknown reason codes:

```text
noCandidate
ambiguousCandidates
missingDocumentation
unsupportedRepresentation
insufficientEvidence
withheldByPolicy
notYetReviewed
```

The reason codes explain why the mapping is unresolved; they do not create semantic meaning.

### 3.2 Semantic assertion

A semantic assertion binds one local reference to one semantic target.

Candidate common properties:

| Property | Requirement |
|---|---|
| `id` | REQUIRED, immutable |
| `source` or enclosing source reference | REQUIRED |
| `validFor` | REQUIRED |
| `localReference` | REQUIRED |
| `semanticTarget` | REQUIRED absolute identifier |
| `mappingRelation` | REQUIRED |
| `authorityStatus` | REQUIRED: `inferred`, `reviewed`, `verified`, or `canonical` |
| `assertedBy` | REQUIRED |
| `assertedAt` | REQUIRED |
| `evidence` | Conditional by authority level |
| `supersedes` | OPTIONAL when replacing another assertion |

One assertion MUST contain exactly one semantic target. Competing interpretations require separate assertions.

### 3.3 Challenge record

A challenge record disputes an assertion or all assertions for a local reference and source version.

Candidate properties:

| Property | Requirement |
|---|---|
| `id` | REQUIRED, immutable |
| `targetsAssertion` or `targetsReference` | exactly one REQUIRED |
| `validFor` | REQUIRED |
| `challengeStatus` | REQUIRED: `open` or `resolved` |
| `reason` | REQUIRED |
| `challengedBy` | REQUIRED |
| `challengedAt` | REQUIRED |
| `evidence` | REQUIRED, one or more |
| `resolves` | REQUIRED only for a resolution record |

An open challenge produces effective state `contested`. A resolution MUST be a new record and MUST NOT mutate the open challenge.

### 3.4 Deprecation record

A deprecation record retires an assertion from current automatic use.

Candidate properties:

| Property | Requirement |
|---|---|
| `id` | REQUIRED, immutable |
| `targetsAssertion` | REQUIRED |
| `reason` | REQUIRED |
| `deprecatedBy` | REQUIRED |
| `effectiveAt` | REQUIRED |
| `replacementAssertion` | OPTIONAL |
| `evidence` | RECOMMENDED |

A replacement is optional because a meaning may be withdrawn without replacement.

## 4. Effective-state model

A consumer computes an effective state for a local reference in the following precedence order:

```text
open conflict       → contested
usable active claim → canonical / verified / reviewed / inferred
only retired claims → deprecated
no active claim     → unknown
```

An explicit open challenge or an incompatible active canonical conflict takes precedence over authority level.

A deprecated assertion is excluded from current selection but remains visible for historical interpretation.

## 5. Authority states

### 5.1 Inferred

Definition:

> A proposed semantic mapping produced by automation or by a non-authoritative inference process and not yet accepted through review, verification or source authority publication.

Required fields in addition to common assertion fields:

```text
confidence
confidenceMethod
evidence[1..n]
```

Consumer behavior:

- MUST preserve `inferred`;
- MUST NOT describe it as verified, canonical or factual source meaning;
- SHOULD expose it as a candidate;
- MAY use it automatically only under explicit deployment policy, a recognized confidence method and a declared threshold;
- MUST retain evidence and confidence method in derived output.

### 5.2 Reviewed

Definition:

> A mapping examined and accepted by an identified human or accountable review process for a declared scope, without claiming reproducible verification or source-owner authority.

Required information:

```text
reviewedBy
reviewedAt
reviewScope
reviewEvidence[1..n]
```

A reviewed assertion MAY include mapping confidence. If confidence is present, `confidenceMethod` is REQUIRED.

Consumer behavior:

- MAY use the assertion when local policy accepts the reviewer and scope;
- MUST NOT present it as independently verified;
- MUST NOT present it as source-authoritative;
- MUST preserve review provenance.

### 5.3 Verified

Definition:

> A mapping that passed a declared, evidence-based verification method performed by an identified verifier for a declared scope or criterion set.

Required information:

```text
verifiedBy
verifiedAt
verificationMethod
verificationScope
verificationEvidence[1..n]
```

A verified assertion MAY contain confidence only when the verification method explicitly defines a calibrated score. When confidence is present, `confidenceMethod` is REQUIRED.

Consumer behavior:

- MAY use the assertion when local policy recognizes the verifier, method and scope;
- MUST report unrecognized verification rather than silently treating it as trusted;
- MUST NOT treat verification as source-owner authority;
- MUST preserve verification evidence.

### 5.4 Canonical

Definition:

> The meaning published by the authority entitled to define the identified source and source version.

Required information:

```text
sourceAuthority
authorityEvidence[1..n]
exact source-version binding
```

Mapping confidence is forbidden.

Consumer behavior:

- MUST verify or locally recognize the asserted source-authority relationship before automatic authoritative use;
- MUST report a self-declared but unrecognized canonical assertion as unverified canonical input;
- MUST preserve source and version binding;
- MUST treat incompatible active canonical assertions as conflict;
- MUST NOT rank canonical assertions by probability.

## 6. Difference tests

An implementation can distinguish the authority states using the questions below.

| Question | Inferred | Reviewed | Verified | Canonical |
|---|---:|---:|---:|---:|
| Automated or tentative proposal permitted? | Yes | No | No | No |
| Accountable review record required? | No | Yes | Not sufficient alone | Not sufficient alone |
| Declared verification method required? | No | No | Yes | No |
| Verification evidence required? | Evidence for inference | Review evidence | Yes | Authority evidence |
| Source authority required? | No | No | No | Yes |
| Confidence required? | Yes | No | No | Forbidden |
| Defines intended source meaning? | No | No | No | Yes |

## 7. Conflict model

### 7.1 Explicit challenge

An unresolved challenge targeting an active assertion or local reference creates effective state `contested`.

Consumers MUST:

- expose the challenge and affected assertions;
- block silent automatic joining, conversion, substitution or action;
- retain each competing target and its underlying authority state;
- avoid selecting a lower-authority assertion merely to bypass a challenge to a higher-authority assertion.

### 7.2 Implicit canonical conflict

Two active, recognized canonical assertions with incompatible targets or mapping relations for the same local reference and source version create effective state `contested` even without a challenge record.

### 7.3 Resolution

A resolution record identifies the challenge it resolves and the evidence for resolution. It does not delete the challenge. A new assertion may supersede earlier assertions.

## 8. Deprecation model

Deprecation affects current applicability, not historical truth or original authority.

Consumers MUST:

- exclude deprecated assertions from current automatic selection;
- retain them for audit and historical replay;
- follow an explicit replacement when compatible with the current source version;
- report `deprecated` when no active replacement or other active assertion is available;
- preserve the deprecation reason and effective time.

A deprecated canonical assertion remains historically canonical for the source version and period where it applied. Its effective current state is nevertheless `deprecated`.

## 9. Immutability and transition records

No published record is edited in place.

### 9.1 Valid progression example

```text
coverage U: unknown
        ↓ new record
assertion A: inferred
        ↓ new assertion B supersedes A
assertion B: reviewed
        ↓ new assertion C supersedes B
assertion C: verified
        ↓ new assertion D issued by source authority
assertion D: canonical
        ↓ new challenge E targets D
reference effective state: contested
        ↓ new resolution F and replacement G
assertion G: canonical
        ↓ new deprecation H targets G
reference effective state: deprecated
```

The sequence is illustrative, not mandatory. A source authority may issue a canonical assertion directly.

### 9.2 Invalid in-place mutation

Invalid:

```json
{
  "id": "urn:assertion:42",
  "authorityStatus": "inferred"
}
```

later replaced under the same identifier with:

```json
{
  "id": "urn:assertion:42",
  "authorityStatus": "canonical"
}
```

The second record reuses an immutable identifier with changed meaning and MUST be rejected.

## 10. Confidence

Confidence is scoped only to semantic mapping correctness under an identified method.

### 10.1 Required

`inferred` requires:

```text
0 ≤ confidence ≤ 1
confidenceMethod present
evidence present
```

### 10.2 Optional

`reviewed` and `verified` may include confidence only when:

- the score has a declared method;
- the method's scope is documented;
- consumers do not compare scores from different methods as if calibrated identically.

### 10.3 Forbidden

Confidence is forbidden on:

- unknown coverage;
- canonical assertions;
- challenge records as mapping confidence;
- deprecation records.

## 11. Evidence requirements

| Effective state or record | Minimum evidence requirement |
|---|---|
| unknown | structured reason; evidence optional |
| inferred | one or more source, sample, documentation or rule references |
| reviewed | review record and evidence |
| verified | verification method and verification evidence |
| canonical | authority evidence and exact source-version binding |
| contested | challenge reason and one or more evidence references |
| deprecated | deprecation reason; replacement behavior explicit |

Human-readable notes never substitute for required structured records.

## 12. Deterministic consumer algorithm

For each `(source, validFor, localReference)` tuple:

1. collect coverage, assertions, challenge, resolution and deprecation records;
2. validate immutable identifiers and references;
3. reject records that do not match the source version;
4. mark assertions targeted by effective deprecations as inactive;
5. apply valid replacements without deleting history;
6. detect unresolved open challenges affecting active assertions or the local reference;
7. detect incompatible active recognized canonical assertions;
8. if conflict exists, return `contested` and action `blocked`;
9. otherwise select one active assertion by authority order and deployment trust policy:
   - recognized canonical;
   - accepted verified;
   - accepted reviewed;
   - inferred candidate under recognized method and threshold;
10. if selected, return its authority state and the corresponding action;
11. if only retired assertions remain, return `deprecated` and action `historical`;
12. otherwise return `unknown` and action `unmapped`.

Suggested actions:

| Effective state | Default action |
|---|---|
| unknown | `unmapped` |
| inferred | `candidate` |
| reviewed | `usable` only under review policy |
| verified | `usable` only under verification policy |
| canonical | `authoritative` only when authority recognized |
| contested | `blocked` |
| deprecated | `historical` |

## 13. Required counterexample handling

### CE-1 — Unknown with fabricated target

Input: unknown coverage contains a semantic target.

Required outcome: invalid.

### CE-2 — Automatic inference labeled verified

Input: `authorityStatus: verified` without a verification method and verifier record.

Required outcome: invalid.

### CE-3 — Reviewed presented as canonical

Input: reviewed assertion claims source authority but has not been issued as a new canonical assertion.

Required outcome: remains reviewed; canonical claim ignored or validation fails if contradictory metadata is present.

### CE-4 — Canonical confidence

Input: canonical assertion contains `confidence: 0.99`.

Required outcome: invalid.

### CE-5 — Silent contested selection

Input: active assertion has an unresolved challenge and consumer selects it automatically.

Required outcome: conformance failure; effective state must be contested and action blocked.

### CE-6 — Deprecation without reason

Input: deprecation record has no structured reason.

Required outcome: invalid.

### CE-7 — In-place mutation

Input: two records reuse one assertion identifier with different authority state or target.

Required outcome: invalid.

## 14. Legacy migration

The experimental mapping-profile `status` property remains valid only under its original profile version.

### 14.1 Direct migration

```text
status=inferred  → authorityStatus=inferred
status=reviewed  → authorityStatus=reviewed
status=canonical → authorityStatus=canonical
```

Existing conditional requirements remain applicable during migration.

### 14.2 Non-automatic migration

```text
status=contested
```

cannot be directly converted because the old value does not state whether the challenged mapping was inferred, reviewed or canonical.

Migration requires an explicit authority assertion plus a separate challenge record. Until then the legacy record remains blocked and is processed using the legacy profile rules.

### 14.3 Verified has no legacy equivalent

No existing four-state assertion may be promoted to verified without a new verification record and a new immutable assertion identifier.

## 15. Relationship to the full Core

The epistemic model applies primarily to the `semantics` block but may also be referenced by:

- identity-resolution assertions;
- provenance associations;
- relation assertions;
- uncertainty descriptions;
- policy interpretation records.

The future full-Core schema should define reusable record definitions rather than duplicating state logic in every block.

## 16. Conformance boundary

This document does not define:

- the complete full-Core JSON Schema;
- a global authority registry;
- universal verifier accreditation;
- one mandatory confidence threshold;
- a user interface;
- a compiler;
- extension-specific risk or action states.

It defines the minimum records and deterministic rules required to preserve epistemic meaning across compatible consumers.
