# ADR-0009 — Entity Identity, Identifier Authority, and Equivalence

- Status: accepted
- Date: 2026-07-13
- Issue: #33
- Decision owners: ADUC maintainers

## Context

Semantic, unit, and temporal compatibility do not prove that two records concern the same real-world entity. `M42` and `MAIN-B` may refer to one motor, two different motors, a motor and an assembly, or identifiers that were reassigned at different times.

Unsafe entity resolution can silently merge histories, measurements, permissions, or personal data. ADUC therefore needs a portable identity profile that preserves issuer authority, namespace, validity, evidence, uncertainty, privacy constraints, and lifecycle without creating a new global identifier registry.

## Decision

### 1. Separate entity, identifier, label, equivalence, and merge decision

ADUC distinguishes:

```text
entity
identifier assigned to an entity
human-readable label
cross-identifier relation assertion
consumer merge decision
```

A label is never an identifier. A matching entity type or similar observations are never proof of identity.

### 2. Reuse established identifier systems

ADUC does not replace identifier schemes or registries.

- IRIs/URIs are used for globally addressable identifier forms and namespaces.
- W3C DID identifiers may be preserved when a source uses a conforming DID method.
- GS1 identifiers and Digital Link URIs remain governed by GS1.
- Legal Entity Identifiers remain governed by the Global LEI System.
- ORCID and other domain identifiers remain governed by their issuing systems.
- local enterprise identifiers remain local and require an explicit namespace and issuer.

The profile records a scheme identifier, namespace, issuer, lexical value, canonical value, and validity. It does not copy an external registry into ADUC.

### 3. Identifier record

An identifier record contains:

```text
identifier record ID
identifier kind
lexical or protected value
canonical value or global IRI
namespace
scheme
issuer
subject entity
entity type
source binding
validity interval
authority, evidence, conflict, and lifecycle
privacy metadata where required
```

Supported v0.1 kinds are:

| Kind | Meaning |
|---|---|
| `local` | Identifier unique only under a declared namespace and issuer. |
| `global` | Globally resolvable or globally scoped identifier expressed as an IRI. |
| `pseudonymous` | Protected identifier derived under a declared pseudonymization method. |
| `linkageToken` | Purpose-limited token used only to test permitted linkage. |

### 4. Namespace and issuer are mandatory identity evidence

The identity key for a local identifier is not its lexical value alone:

```text
scheme + namespace + issuer + canonical value + applicable time
```

`M42` issued by one organization is not equal to `M42` issued by another organization.

### 5. Entity type and identifier type are separate

`entityType` describes the identified thing. `scheme` describes the identifier system. Two records having compatible entity types does not prove they identify the same entity.

### 6. Identity relation vocabulary

The v0.1 profile supports:

| Relation | Meaning | Automatic merge |
|---|---|---|
| `possibleMatch` | Evidence suggests a candidate correspondence. | Never. |
| `sameEntity` | Exact identity is established for the declared scope and time. | Only when all merge gates pass. |
| `differentEntity` | The identifiers are known to concern different entities. | Forbidden. |
| `broaderEntity` | Subject identifies a containing or aggregated entity. | Never. |
| `narrowerEntity` | Subject identifies a component or narrower entity. | Never. |

Unresolved identity is represented by the absence of a qualifying relation plus an explicit unresolved coverage/result state, not by a fabricated assertion.

### 7. Authority and confidence remain separate

- `possibleMatch` may be `inferred` or `reviewed`.
- `sameEntity` requires `verified` or `canonical` authority in v0.1.
- `differentEntity` requires at least `reviewed` authority.
- `broaderEntity` and `narrowerEntity` require `verified` or `canonical` authority.
- numeric confidence is required for inferred candidate matches, optional for reviewed candidates, and forbidden for canonical assertions.

A high similarity score never creates source authority.

### 8. Strong equality and `owl:sameAs`

OWL individual equality has strong semantics: the two identifiers denote the same individual. ADUC exports `owl:sameAs` only for an active, clear, verified or canonical `sameEntity` assertion whose temporal, authority, privacy, and endpoint checks all pass.

`possibleMatch`, partial overlap, broader/narrower relations, aliases, and type compatibility must never be serialized as `owl:sameAs`.

### 9. Merge gate

Automatic record merging is allowed only when:

1. an explicit active `sameEntity` assertion exists;
2. its authority is `verified` or `canonical`;
3. both endpoint identifier records exist and are active at the evaluation time;
4. source bindings and evidence are present;
5. the asserting authority is identified;
6. no open challenge, deprecation, contradictory relation, or overlapping identifier reassignment exists;
7. entity types are equal or covered by an explicit verified compatibility rule;
8. privacy and permitted-purpose constraints allow linkage;
9. the relation validity covers the evaluation time.

Otherwise the decision is `candidateOnly`, `mergeBlocked`, `differentEntity`, `relationOnly`, or `unresolved`.

### 10. Recycled identifiers and temporal scope

An identifier may be reassigned. The same namespace-qualified canonical value may identify different entities only when assignment validity intervals do not overlap.

At a given evaluation instant, exactly one active assignment may resolve. Overlapping assignments block automatic identity use.

### 11. Aliases, renames, mergers, and splits

- a label change does not create a new identifier or new entity;
- a replacement identifier creates a new immutable record linked by lifecycle metadata;
- organizational or asset mergers and splits use explicit entity relations and validity, not silent rewriting;
- historical identifiers remain queryable after deprecation;
- transitive closure is not assumed across `possibleMatch`, broader/narrower, contested, or time-scoped relations.

### 12. Privacy-sensitive identifiers

Pseudonymous identifiers and linkage tokens must declare:

```text
protection method identifier
method version
digest or token value
issuer
namespace or linkage domain
permitted linkage purpose
```

They must not contain the original secret identifier. A linkage decision is blocked when purpose, privacy domain, or policy is incompatible.

### 13. Source binding and provenance

Every identifier assertion uses ADR-0006 source binding. Identity relations bind their endpoint identifier records and add explicit relation evidence, method, asserting authority, and temporal validity. Time-scoped records use ADR-0008 temporal semantics. Authority, evidence, challenges, resolutions, and deprecations follow ADR-0005.

### 14. Deterministic conflict rules

Automatic merging is blocked when any active overlapping assertion states `differentEntity`, when two canonical assertions contradict one another, when one identifier is actively assigned to multiple entities, or when privacy policy forbids linkage.

The original assertions remain immutable and visible.

### 15. Migration

Legacy values migrate as follows:

| Legacy value | Migration |
|---|---|
| `M42` | local identifier with explicit scheme, namespace, issuer, canonicalization, source binding, and validity |
| `MAIN-B` | separate local identifier; no crosswalk is inferred solely from measurements |
| `R42` | local station identifier under the river-agency namespace |
| `org-river:station-id` | identifier-scheme reference, not an entity identifier |
| human equipment name | label only |

Migration never creates `sameEntity` without evidence and authority.

## Reference error families

```text
ADUC-ID-001       identifier record is incomplete or inconsistent
ADUC-ID-002       local identifier lacks namespace, scheme, or issuer
ADUC-ID-003       global identifier is not an absolute IRI
ADUC-ID-004       label is used as an identifier
ADUC-ID-005       protected identifier exposes or lacks protected material metadata
ADUC-ID-006       identifier validity is missing or invalid
ADUC-ID-007       identifier is expired, recycled, or multiply assigned
ADUC-REL-001      relation endpoint does not exist
ADUC-REL-002      relation and authority are incompatible
ADUC-REL-003      evidence, method, or asserting authority is missing
ADUC-REL-004      contradictory identity relations are active
ADUC-REL-005      entity types are incompatible without a verified compatibility rule
ADUC-REL-006      `owl:sameAs` export is not justified
ADUC-PRIV-001     privacy or permitted-purpose constraints block linkage
ADUC-MERGE-001    available evidence supports only a candidate match
ADUC-MERGE-002    automatic merge is blocked by conflict or lifecycle
```

## Consequences

### Positive

- local identifiers remain portable without pretending to be global;
- possible matches can be shared without unsafe merging;
- exact identity carries authority, evidence, time, and privacy scope;
- recycled identifiers are detected;
- `owl:sameAs` is reserved for strong equality;
- external identifier systems remain authoritative.

### Costs

- identifier namespaces and issuers must be recorded;
- identity assertions require more evidence than field-name matching;
- some plausible matches remain unresolved until reviewed;
- privacy-preserving linkage needs dedicated methods and policy evidence.

## Rejected alternatives

### Treat matching lexical values as identity

Rejected because namespace, issuer, and validity determine meaning.

### Merge records above a confidence threshold

Rejected because confidence is not authority and may be poorly calibrated.

### Use `owl:sameAs` for every crosswalk

Rejected because its semantics are exact individual equality.

### Infer identity from entity type and matching measurements

Rejected because compatibility and correlation do not prove identity.

### Rewrite old identifiers after reassignment

Rejected because it destroys historical validity and provenance.

### Store raw private identifiers for convenience

Rejected because linkage must preserve privacy and declared purpose.

## References

- OWL 2 Structural Specification — Individual Equality: https://www.w3.org/TR/owl2-syntax/#Individual_Equality
- W3C Decentralized Identifiers (DIDs) v1.0: https://www.w3.org/TR/did-core/
- GS1 Digital Link standard: https://ref.gs1.org/standards/digital-link/
- GLEIF Legal Entity Identifier overview: https://www.gleif.org/en/organizational-identity/lei-vlei/the-legal-entity-identifier-lei
- RFC 3987 — Internationalized Resource Identifiers: https://www.rfc-editor.org/rfc/rfc3987

## Acceptance evidence

- nine valid identity reference cases;
- seventeen required invalid counterexamples;
- nine deterministic evaluator and CLI tests;
- GitHub Actions passed the identity suite and every pre-existing validation suite.

## Follow-up

1. define provenance and transformation lineage;
2. define remaining uncertainty, relation, and policy boundaries;
3. freeze the normative full-Core object model;
4. implement the full-Core JSON Schema family;
5. migrate the reference comparison example to unified source, unit, time, identity, and provenance-aware comparison.
