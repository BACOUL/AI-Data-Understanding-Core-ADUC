# ADR-0013 — Policy and Permitted-Use Conditions

- Status: accepted
- Date: 2026-07-14
- Issue: #45
- Pull request: pending
- Decision owners: ADUC maintainers

## Context

ADUC already defines source binding, semantic mappings, units, time, identity, provenance, uncertainty, quality, and general relations. The remaining Core domain profile must describe conditions of use without inventing legal authority or pretending that a machine-readable declaration overrides law, contracts, consent requirements, access controls, or jurisdiction-specific interpretation.

A policy layer is unsafe when it silently assumes that:

- a descriptive `public` classification grants permission for every purpose;
- free text such as `research` is a portable purpose identifier;
- absence of a permission means either permission or prohibition;
- a legal notice is an executable authorization;
- a permission overrides a matching prohibition;
- an unidentified requester satisfies a named-assignee rule;
- a duty is satisfied without bound evidence;
- consent, ownership, or legal compliance can be claimed without evidence and provenance;
- a rule remains valid after expiry or outside its target, territory, environment, conflict, or lifecycle scope;
- a partial, redacted, inherited, or externally governed policy is complete enough for automatic reliance.

## Decision

### 1. Reuse ODRL and established identifiers

ADUC reuses the W3C ODRL Information Model and Vocabulary for policy, permission, prohibition, duty, target, assigner, assignee, action, and related policy concepts.

ADUC adds only the qualification needed to integrate policy with the accepted Core profiles:

```text
exact target binding and digest
controlled purpose identifier
requester and recipient identity
disclosure state
authority, evidence, provenance, conflict, and lifecycle
temporal, spatial, and environment scope
deterministic consumer outcome
```

ADUC does not create a competing general-purpose rights language and does not override ODRL semantics.

### 2. Separate description, rule, and decision

The profile separates:

```text
descriptive classification or legal statement
machine-evaluable policy rule
consumer evaluation result
```

A classification, recommendation, or legal notice may inform a person but cannot grant permission or impose an executable duty merely because it appears in a policy document.

### 3. Policy record

Every policy identifies:

```text
policy id
exact target binding
target digest
policy mode
disclosure state
method
provenance activity
authority level
asserting party
bound evidence
conflict state
lifecycle state
validity interval
rules
optional supersedes and inheritance references
```

The target is bound through ADR-0006. Parties use absolute identifiers consistent with ADR-0009. Time follows ADR-0008. Provenance follows ADR-0010. Authority, conflict, and lifecycle follow ADR-0005.

### 4. Controlled actions and purposes

Actions and purposes use absolute identifiers from a pinned profile.

A consumer must not equate:

```text
"research"
urn:aduc:purpose:research
```

Free-text matching, label similarity, and model guesses do not establish purpose equivalence.

### 5. Executable rule types

The offline Core subset supports:

```text
permission
prohibition
duty
```

It also preserves non-executable:

```text
recommendation
legalNotice
classification
```

Executable rules must explicitly declare that they are machine-evaluable, identify a controlled action, identify an assigner, and satisfy their type-specific requirements.

### 6. Parties and recipients

A rule may restrict:

```text
assignee
recipient
```

A named assignee requires an identified requester. A named recipient requires an identified recipient. Missing or local party labels do not satisfy identity requirements.

### 7. Duties

A permission may reference duties.

Duties are divided into:

```text
preUse
postUse
```

An unsatisfied pre-use duty blocks permission. A post-use duty may remain visible as an outstanding obligation in a `permit` result.

Duty satisfaction requires bound evidence. A boolean such as `satisfied: true` is insufficient by itself.

### 8. Open and closed policy modes

In `open` mode, absence of an applicable rule yields:

```text
indeterminate
```

In `closed` mode, absence of an applicable permission yields:

```text
deny
```

Neither behavior may be inferred without an explicit governing mode.

### 9. Deterministic precedence

The reference subset uses:

```text
matching prohibition overrides matching permission
```

This is a deterministic consumer-safety rule for the profile, not a claim of universal legal precedence.

A qualifying permission may produce `permit` only when no matching prohibition applies and all pre-use duties are satisfied.

### 10. Safe outcomes

The evaluator returns one of:

```text
permit
deny
notApplicable
indeterminate
requiresHumanReview
```

Meaning:

- `permit`: a qualifying permission applies, no matching prohibition applies, and pre-use duties are satisfied;
- `deny`: a prohibition applies, the policy is outside validity, a pre-use duty is unsatisfied, or closed mode denies by default;
- `notApplicable`: the request targets a different bound resource;
- `indeterminate`: an open policy contains no applicable executable rule;
- `requiresHumanReview`: the policy is inferred, partial, redacted, externally governed, contested, deprecated, or dependent on a human-only statement.

These results describe profile evaluation. They are not legal advice and do not themselves grant access.

### 11. Claims requiring external evidence

Claims of:

```text
consent
ownership
legal compliance
```

require typed, bound evidence with provenance. ADUC records that evidence; it does not independently determine legal validity.

### 12. Scope

Policy evaluation may restrict:

```text
time
space
environment
requester
recipient
purpose
action
target version
```

A request for the same resource identifier with a different digest is blocked as a target-version mismatch.

### 13. Composition, versioning, and replacement

A policy may identify `supersedes` and `inheritsFrom`.

The offline subset automatically evaluates inherited policy only when composition is explicitly resolved and supported by bound composition evidence. Self-reference, unresolved inheritance, and missing composition evidence are blocked.

Published policy records are immutable. Replacement creates a new identified policy.

### 14. Disclosure, conflict, and lifecycle

Automatic reliance is blocked or escalated when a policy is:

```text
partial
redacted
externally governed
contested
deprecated
```

An inferred policy requires explicit calibrated confidence and method but still yields `requiresHumanReview` in the reference subset.

### 15. Deterministic JSON-LD/RDF export

The reference exporter emits:

1. an ODRL policy node;
2. ODRL permission, prohibition, and duty nodes where applicable;
3. ADUC qualification for target digest, authority, disclosure, mode, and provenance;
4. absolute identifiers;
5. deterministic rule ordering.

Export does not convert human-only statements into executable rules.

## Consequences

### Positive

- policy conditions are portable without creating a competing rights language;
- descriptive labels cannot silently become permissions;
- prohibitions, duties, parties, purposes, target versions, and policy states remain explicit;
- open-world uncertainty is preserved;
- evidence is required for duty satisfaction and sensitive legal claims;
- consumers receive deterministic safe outcomes;
- JSON-LD/RDF exchange is reproducible.

### Costs

- producers must use controlled identifiers and exact target binding;
- consumers need a pinned policy profile;
- many real legal questions remain `requiresHumanReview`;
- inherited or externally governed policies need additional evidence before automatic use;
- technical evaluation does not replace enforcement or legal review.

## Rejected alternatives

- custom ADUC-only rights vocabulary;
- free-text purpose matching;
- treating `public` as universal permission;
- permission by absence;
- prohibition by absence without closed mode;
- legal notices as executable authorizations;
- boolean duty satisfaction without evidence;
- automatic consent, ownership, jurisdiction, or compliance claims;
- silent policy inheritance;
- universal legal-precedence claims;
- direct access-control enforcement in the Core.

## References

- ODRL Information Model 2.2: https://www.w3.org/TR/odrl-model/
- ODRL Vocabulary & Expression 2.2: https://www.w3.org/TR/odrl-vocab/
- PROV-O: https://www.w3.org/TR/prov-o/
- RDF 1.1 Concepts: https://www.w3.org/TR/rdf11-concepts/

## Acceptance evidence

- twenty valid policy and evaluation cases;
- thirty-two invalid counterexamples;
- thirteen deterministic evaluator and CLI tests;
- pinned policy-registry identity and SHA-256 validation;
- permission, prohibition, duty, party, purpose, target, time, disclosure, authority, composition, consent, and open/closed-mode checks;
- deterministic JSON-LD/RDF export;
- GitHub Actions passed the policy suite and every pre-existing validation suite in the acceptance pull request.

## Follow-up

1. freeze the normative full-Core object model and modular boundaries;
2. update the complete Core example to the frozen model;
3. implement the official full-Core JSON Schema family;
4. create complete valid and invalid Core examples;
5. unify validation and comparison across accepted profiles.
