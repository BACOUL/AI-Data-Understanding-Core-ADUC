# ADR-0013 — Policy and Permitted-Use Conditions

- Status: accepted
- Date: 2026-07-14
- Issue: #45
- Pull request: #46
- Decision owners: ADUC maintainers

## Context

ADUC already defines source binding, semantics, units, time, identity, provenance, uncertainty, quality, and relations. The remaining Core domain profile must communicate conditions of use without inventing legal authority or pretending that a machine-readable declaration overrides law, contracts, consent requirements, access controls, or jurisdiction-specific interpretation.

Unsafe shortcuts include:

- treating a descriptive `public` classification as permission for every purpose;
- matching free text such as `research` to a controlled purpose identifier;
- treating absence of a permission as permission or prohibition without an explicit policy mode;
- treating a legal notice as executable authorization;
- letting a permission override a matching prohibition;
- accepting unidentified parties where named parties are required;
- treating a duty as satisfied without bound evidence;
- claiming consent, ownership, or legal compliance without evidence and provenance;
- applying expired, misbound, partial, redacted, contested, deprecated, or externally governed policy automatically.

## Decision

### Reuse ODRL

ADUC reuses the W3C ODRL Information Model and Vocabulary for policy, permission, prohibition, duty, target, assigner, assignee, action, and related concepts.

ADUC adds only the qualification required to integrate policy with accepted Core profiles:

```text
exact target binding and digest
controlled purpose identifier
requester and recipient identity
disclosure state
authority, evidence, provenance, conflict, and lifecycle
temporal, spatial, and environment scope
deterministic consumer outcome
```

ADUC does not create a competing rights language and does not override ODRL semantics.

### Separate descriptions, executable rules, and results

The profile separates:

```text
descriptive classification or legal statement
machine-evaluable policy rule
consumer evaluation result
```

A classification, recommendation, or legal notice may inform a person but cannot grant permission or impose an executable duty merely because it appears in a policy document.

### Bind every policy to an exact target

Every policy identifies its own absolute identifier, exact target binding, target digest, mode, disclosure state, method, provenance activity, authority, asserting party, evidence, explicit conflict state, explicit lifecycle state, validity interval, and rules.

The target follows ADR-0006. Parties follow ADR-0009. Time follows ADR-0008. Provenance follows ADR-0010. Authority, conflict, and lifecycle follow ADR-0005.

A request for the same resource identifier with a different digest is blocked as a target-version mismatch.

### Require explicit safety states

`conflict` and `life` are mandatory. They must never default silently to `clear` or `active`.

Allowed states in the reference subset are:

```text
conflict: clear | contested
life: active | deprecated
```

Missing, contested, or deprecated state prevents automatic reliance.

### Use controlled actions, purposes, and parties

Actions and purposes use absolute identifiers from a pinned profile. A consumer must not equate:

```text
"research"
urn:aduc:purpose:research
```

A named assignee requires an identified requester. A named recipient requires an identified recipient. Local labels do not satisfy identity requirements.

### Distinguish executable and human-only effects

Executable effects:

```text
permission
prohibition
duty
```

Human-only effects:

```text
recommendation
legalNotice
classification
```

Executable rules must explicitly declare machine evaluability, identify a controlled action and assigner, and satisfy their type-specific requirements.

### Preserve duty phases and evidence

Duties are divided into:

```text
preUse
postUse
```

An unsatisfied pre-use duty blocks only the permission that references it; another independent qualifying permission may still permit the request. A post-use duty remains visible as an outstanding obligation.

Duty satisfaction requires bound evidence. A boolean such as `satisfied: true` is insufficient by itself.

### Make policy mode explicit

In `open` mode, absence of an applicable rule yields `indeterminate`.

In `closed` mode, absence of an applicable permission yields `deny`.

Neither behavior may be inferred without an explicit mode.

### Use deterministic safe precedence

The reference subset applies:

```text
matching prohibition overrides matching permission
```

This is a deterministic consumer-safety rule for the profile, not a claim of universal legal precedence.

### Return only safe outcomes

The evaluator returns one of:

```text
permit
deny
notApplicable
indeterminate
requiresHumanReview
```

- `permit`: a qualifying permission applies, no matching prohibition applies, and that permission's pre-use duties are satisfied;
- `deny`: a prohibition applies, the policy is outside validity, every matching permission is blocked by a pre-use duty, or closed mode denies by default;
- `notApplicable`: the request targets a different bound resource;
- `indeterminate`: an open policy contains no applicable executable rule;
- `requiresHumanReview`: authority, disclosure, conflict, lifecycle, composition, or human-only interpretation is insufficient.

These are profile-evaluation results. They are not legal advice and do not themselves grant access.

### Require evidence for sensitive claims

Claims of consent, ownership, or legal compliance require typed, bound evidence with provenance. ADUC records that evidence; it does not independently determine legal validity.

### Preserve scope

Policy evaluation may restrict time, space, environment, requester, recipient, purpose, action, and target version. A rule is applicable only when all declared restrictions match.

### Resolve composition explicitly

A policy may identify `supersedes` and `inheritsFrom`.

The offline subset accepts inherited terms only when the producer materializes the resolved rule set, declares composition resolved, and provides bound composition evidence. Self-reference, unresolved inheritance, and missing evidence are blocked.

Published policy records are immutable. Replacement creates a new identified policy.

### Export deterministically

The reference exporter emits an ODRL policy node, applicable ODRL permission/prohibition/duty nodes, ADUC qualification for target digest, authority, disclosure, mode, and provenance, absolute identifiers, and deterministic rule ordering.

Export never converts human-only statements into executable rules.

## Consequences

### Positive

- policy conditions remain portable without creating a competing rights language;
- descriptive labels cannot silently become permissions;
- prohibitions, duties, parties, purposes, target versions, and policy states remain explicit;
- open-world uncertainty is preserved;
- evidence is required for duty satisfaction and sensitive legal claims;
- alternative valid permissions are evaluated independently;
- consumers receive deterministic safe outcomes;
- JSON-LD/RDF exchange is reproducible.

### Costs

- producers must use controlled identifiers and exact target binding;
- consumers need a pinned policy profile;
- many real legal questions remain `requiresHumanReview`;
- inherited or externally governed policies need additional evidence;
- technical evaluation does not replace enforcement or legal review.

## Rejected alternatives

- custom ADUC-only rights vocabulary;
- free-text purpose matching;
- treating `public` as universal permission;
- permission by absence;
- prohibition by absence without closed mode;
- implicit `clear` or `active` state;
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
- thirty-two official invalid fixtures plus explicit missing-state regression checks;
- thirteen deterministic evaluator and CLI test methods;
- pinned policy-registry identity and SHA-256 validation;
- permission, prohibition, alternative-permission, duty, party, purpose, target, time, disclosure, authority, composition, consent, explicit-state, and open/closed-mode checks;
- deterministic JSON-LD/RDF export;
- GitHub Actions passed the policy suite and every pre-existing validation suite in PR #46 after review corrections.

## Follow-up

1. freeze the normative full-Core object model and modular boundaries;
2. update the complete Core example to the frozen model;
3. implement the official full-Core JSON Schema family;
4. create complete valid and invalid Core examples;
5. unify validation and comparison across accepted profiles.
