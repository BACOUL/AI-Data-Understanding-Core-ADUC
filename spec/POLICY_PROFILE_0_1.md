# ADUC Policy Profile 0.1

Status: working draft  
Decision: ADR-0013  
Scope: portable policy declarations and a deterministic offline permitted-use evaluation subset

## 1. Purpose

This profile defines how an ADUC contract communicates machine-readable use conditions without claiming that ADUC determines legal validity, ownership, consent, jurisdiction, fairness, regulatory compliance, or enforceable access rights.

The profile integrates ODRL policy expressions with the accepted ADUC source-binding, identity, time, provenance, epistemic, uncertainty, and relation profiles.

## 2. Normative layers

A conforming implementation keeps three layers separate:

```text
policy source and human statements
machine-evaluable policy rules
consumer evaluation outcomes
```

A descriptive classification, recommendation, or legal notice is not an executable permission.

## 3. Pinned policy registry

The reference evaluator uses a pinned registry identified by:

```text
path
registryId
registryVersion
sha256
```

The registry records only the subset required for deterministic offline evaluation:

```text
recognized ODRL actions
controlled purpose identifiers
recognized environment identifiers
policy modes
disclosure states
rule effects
safe outcomes
conflict strategy
external authority sources
```

The registry does not redefine ODRL.

## 4. Policy model

A policy document contains:

```json
{
  "id": "urn:policy:river:v1",
  "target": "urn:resource:river-data:v1",
  "targetDigest": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "mode": "open",
  "disclosure": "complete",
  "method": "urn:aduc:method:policy-review-v1",
  "prov": "urn:aduc:activity:policy-publication-v1",
  "auth": "verified",
  "by": "urn:org:river-agency",
  "evidence": ["urn:evidence:policy-document"],
  "conflict": "clear",
  "life": "active",
  "valid": {
    "start": "2026-01-01T00:00:00Z",
    "end": "2027-01-01T00:00:00Z"
  },
  "rules": []
}
```

### 4.1 Required policy properties

```text
id
target
targetDigest
mode
disclosure
method
prov
auth
by
evidence
conflict
life
valid
rules
```

### 4.2 Target binding

The target must:

- be an absolute identifier;
- resolve to a bound ADUC resource or version;
- carry a lowercase SHA-256 digest;
- match the digest recorded for the bound object.

A request using the same target identifier with a different digest is a version mismatch and must not be evaluated as permission.

### 4.3 Authority

Allowed authority levels are:

```text
inferred
reviewed
verified
canonical
```

An inferred policy must preserve explicit calibrated confidence and a confidence method. The reference evaluator still returns `requiresHumanReview` for inferred policy.

### 4.4 Disclosure

Allowed disclosure states are:

```text
complete
partial
redacted
externallyGoverned
```

Only `complete` is eligible for automatic `permit` in the reference subset.

### 4.5 Conflict and lifecycle

Supported states are:

```text
conflict: clear | contested
life: active | deprecated
```

Contested or deprecated policy is preserved but not automatically relied upon.

## 5. Rule model

A rule identifies:

```text
id
effect
machineEvaluable
action where executable
assigner where executable
controlled purposes for permission or prohibition
optional assignee
optional recipient
optional spatial scope
optional environment
optional duties
```

### 5.1 Effects

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

An executable effect must set:

```json
"machineEvaluable": true
```

A human-only effect must set:

```json
"machineEvaluable": false
```

### 5.2 Permission

Example:

```json
{
  "id": "urn:rule:permit-research",
  "effect": "permission",
  "action": "http://www.w3.org/ns/odrl/2/use",
  "purposes": ["urn:aduc:purpose:research"],
  "assigner": "urn:org:river-agency",
  "machineEvaluable": true
}
```

A permission requires at least one controlled purpose.

### 5.3 Prohibition

Example:

```json
{
  "id": "urn:rule:deny-credit",
  "effect": "prohibition",
  "action": "http://www.w3.org/ns/odrl/2/use",
  "purposes": ["urn:aduc:purpose:individual-credit-scoring"],
  "assigner": "urn:org:river-agency",
  "machineEvaluable": true
}
```

A matching prohibition overrides a matching permission in the deterministic reference subset.

### 5.4 Duty

Example:

```json
{
  "id": "urn:rule:attribute",
  "effect": "duty",
  "action": "http://www.w3.org/ns/odrl/2/attribute",
  "phase": "preUse",
  "assigner": "urn:org:river-agency",
  "requiredEvidenceKind": "attribution",
  "machineEvaluable": true
}
```

Allowed phases:

```text
preUse
postUse
```

A permission references duties by absolute rule identifier.

## 6. Request model

The reference request contains:

```json
{
  "target": "urn:resource:river-data:v1",
  "targetDigest": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "requester": "urn:org:research-lab",
  "recipient": "urn:org:research-lab",
  "action": "http://www.w3.org/ns/odrl/2/use",
  "purpose": "urn:aduc:purpose:research",
  "at": "2026-07-14T12:00:00Z",
  "spatial": "urn:place:france",
  "environment": "urn:aduc:environment:research",
  "evidence": []
}
```

All identifiers must be absolute. Action, purpose, and environment must occur in the pinned registry.

## 7. Matching

A permission or prohibition matches only when all declared conditions match:

```text
target and target digest
action
purpose
assignee/requester where declared
recipient where declared
spatial scope where declared
environment where declared
time validity
```

No value is inferred from a label or free text.

## 8. Duties and evidence

### 8.1 Pre-use duty

A missing pre-use duty satisfaction blocks use:

```text
deny
```

### 8.2 Post-use duty

A post-use duty may remain outstanding in a qualifying result:

```json
{
  "outcome": "permit",
  "outstandingDuties": ["urn:rule:delete"]
}
```

### 8.3 Satisfaction evidence

A duty is satisfied only by bound evidence referenced by the request and accepted by the rule.

The following is insufficient:

```json
{"satisfied": true}
```

without a bound evidence reference.

## 9. Sensitive claims

Rules claiming any of the following require typed evidence and provenance:

```text
consent
ownership
legalCompliance
```

Required evidence kinds in the reference subset are:

```text
consent -> consent
ownership -> ownership
legalCompliance -> legalAssessment
```

The evaluator validates evidence representation, not the legal truth of the claim.

## 10. Policy modes and absence

### 10.1 Open mode

No applicable executable rule:

```text
indeterminate
```

### 10.2 Closed mode

No applicable permission:

```text
deny
```

The mode must be explicit.

## 11. Deterministic evaluation order

The reference evaluator applies this order:

1. validate registry, policy, rules, evidence, and request;
2. return `notApplicable` for a different target;
3. block a target-version mismatch;
4. escalate contested, deprecated, incomplete, redacted, externally governed, or inferred policy;
5. deny outside the validity interval;
6. apply matching prohibitions;
7. test matching permissions and pre-use duties;
8. expose post-use duties;
9. escalate an applicable human-only legal statement;
10. apply closed-mode default denial;
11. otherwise return open-mode `indeterminate`.

This order is a profile rule for deterministic safety. It is not universal legal interpretation.

## 12. Outcomes

### `permit`

A qualifying permission applies, no matching prohibition applies, and every pre-use duty is satisfied.

### `deny`

A matching prohibition applies, the policy is outside validity, a required pre-use duty is unsatisfied, or closed mode denies by default.

### `notApplicable`

The request targets a different resource.

### `indeterminate`

The policy is open and contains no applicable executable rule.

### `requiresHumanReview`

Automatic reliance is blocked because policy authority, disclosure, lifecycle, conflict, composition, or human-only interpretation is insufficient.

## 13. Composition and versioning

A policy may contain:

```text
supersedes
inheritsFrom
compositionState
compositionEvidence
```

Rules:

- `supersedes` and `inheritsFrom` use absolute policy identifiers;
- a policy cannot supersede or inherit from itself;
- inherited policy must be explicitly resolved for the offline subset;
- resolved composition requires bound evidence;
- unresolved composition blocks automatic evaluation;
- replacement creates a new immutable policy record.

## 14. Classification and legal statements

A classification such as:

```text
public
```

is descriptive. It does not mean:

```text
permission for every action, purpose, party, territory, or time
```

A legal notice remains human-only unless an independently valid executable rule expresses the intended machine behavior.

## 15. JSON-LD/RDF export

The reference exporter emits:

```text
odrl:Policy
odrl:Permission
odrl:Prohibition
odrl:Duty
```

and ADUC qualification for:

```text
target digest
authority
disclosure
policy mode
provenance activity
controlled purpose
```

Ordering is deterministic by rule identifier.

## 16. Error families

```text
ADUC-POL-VOCAB-*    registry identity and integrity
ADUC-POL-DOC-*      policy document and mode
ADUC-POL-TARGET-*   exact target binding and version
ADUC-POL-REQUEST-*  request structure and identifiers
ADUC-POL-AUTH-*     authority and calibrated confidence
ADUC-POL-EVIDENCE-* evidence binding
ADUC-POL-STATE-*    disclosure, conflict, and lifecycle
ADUC-POL-SCOPE-*    time, space, and environment
ADUC-POL-COMPOSE-*  inheritance, replacement, and composition
ADUC-POL-RULE-*     rule identity and supported effects
ADUC-POL-ACTION-*   controlled actions
ADUC-POL-PURPOSE-*  controlled purposes
ADUC-POL-PARTY-*    assigner, assignee, requester, and recipient
ADUC-POL-DUTY-*     duty definition, references, and satisfaction
ADUC-POL-CLAIM-*    consent, ownership, and compliance claims
ADUC-POL-LEGAL-*    human-only statement misuse
```

## 17. Core boundary

This profile does not:

- grant legal permission;
- replace ODRL;
- determine consent validity;
- determine ownership;
- determine jurisdiction;
- determine regulatory compliance;
- determine fairness;
- enforce access control;
- execute deletion, reporting, attribution, or other duties;
- resolve arbitrary policy languages;
- implement a legal-advice system;
- implement the full-Core object model or JSON Schema.

## 18. Conformance

A conforming implementation must:

1. reproduce the official valid cases;
2. reject the official invalid counterexamples for the documented error family;
3. preserve all five outcomes;
4. preserve prohibition precedence;
5. preserve open-mode uncertainty;
6. require evidence for duties and sensitive claims;
7. block wrong target versions;
8. export qualifying policy records deterministically;
9. avoid model-specific prompts, private memory, or online services.

The official harness contains twenty valid cases, thirty-two invalid counterexamples, and thirteen evaluator/CLI tests.
