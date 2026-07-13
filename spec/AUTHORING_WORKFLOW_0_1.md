# ADUC Authoring and Review Workflow 0.1

- Status: Gate 4 candidate
- Date: 2026-07-13
- Issue: #13
- Applies to: ADUC semantic mapping profiles 0.1

## 1. Purpose

This document defines a manual, auditable workflow for producing ADUC semantic mapping profiles from existing JSON or CSV sources.

It specifies how a local field mapping moves from an initial proposal to a reviewed, contested or publisher-canonical assertion without losing uncertainty, evidence, provenance or prior versions.

The workflow is deliberately defined before automatic model-based inference. Automation may later assist individual steps, but it must preserve the same artifacts and invariants.

## 2. Separation of artifacts

ADUC distinguishes two classes of artifact.

### 2.1 Portable profile

The portable profile is the interoperable output consumed by independent tools and AI systems. It contains only source binding and immutable semantic mapping assertions conforming to:

```text
schema/aduc-mapping-profile.schema.json
```

It must not contain internal task queues, reviewer comments, UI state, prompts, private chain-of-thought or provider-specific execution metadata.

### 2.2 Authoring state

The authoring state is an internal or project-local record used to create and audit the portable profile. It may contain:

- field coverage;
- proposal status;
- review decisions;
- responsible roles;
- authoring events;
- validation results;
- links to evidence;
- unpublished candidate mappings.

The authoring state is not automatically interoperable and is not part of the ADUC Core profile. Organizations may store it in their own systems as long as the resulting portable assertions preserve the required meaning and provenance.

## 3. Roles

### 3.1 Source curator

The source curator identifies the source, its structure and the exact version to which mappings apply.

Responsibilities:

- provide or select the source description;
- freeze a source version or digest;
- enumerate local fields;
- record known units, code lists and documentation;
- identify the source authority.

The source curator does not automatically possess authority to publish canonical meaning.

### 3.2 Inference producer

The inference producer proposes mappings. It may be a human, script, rules engine or AI model.

Responsibilities:

- produce one candidate target per assertion;
- select an explicit mapping relation;
- assign a confidence score only through an identified method;
- attach evidence;
- publish the result as `inferred`;
- avoid claiming source authority.

### 3.3 Reviewer

The reviewer evaluates an inferred mapping and may accept, revise, reject or contest it.

Responsibilities:

- inspect source documentation and values;
- verify the local reference;
- verify target meaning and relation strength;
- evaluate evidence and confidence method;
- create a new immutable assertion rather than editing the proposal;
- publish accepted non-authoritative work as `reviewed`;
- publish unresolved disputes as `contested`.

A reviewer cannot publish `canonical` unless separately authorized by the source publisher.

### 3.4 Source authority

The source authority is the person or organization entitled to define the official meaning of fields for the identified source version.

Responsibilities:

- verify control or delegated authority over the source description;
- publish canonical mappings;
- create a new immutable assertion that supersedes earlier proposals or reviews;
- avoid attaching a probability score to canonicality;
- maintain versioned source descriptions.

### 3.5 Consumer

The consumer validates and applies published mappings.

Responsibilities:

- enforce source-version binding;
- preserve assertion status and relation;
- report conflicts and contested mappings;
- avoid hidden provider-specific mappings in conformance mode;
- apply local policy to reviewed or inferred mappings;
- verify source authority through configured trust mechanisms when canonicality matters.

## 4. Authoring artifacts

A complete manual authoring package contains:

```text
source data
source description
portable ADUC profile(s)
authoring-state record
coverage report
evidence references
validator report
```

### 4.1 Source data

The original JSON or CSV data remains unchanged.

### 4.2 Source description

For v0.1, the source description is a versioned Croissant description or JSON Schema.

It provides structure and field identity. ADUC must not duplicate that structure.

### 4.3 Portable profile

Each published profile contains one or more immutable mapping assertions.

### 4.4 Coverage report

Coverage records which described fields currently have usable assertions and which remain unmapped.

Coverage is kept outside the portable profile because absence of an assertion already means that no mapping is published.

Recommended field states:

- `unmapped`;
- `inferred`;
- `reviewed`;
- `canonical`;
- `contested`.

A coverage entry should contain:

```json
{
  "localReference": "/properties/flow",
  "state": "reviewed",
  "assertionIds": [
    "urn:aduc:assertion:river-flow-reviewed-1"
  ]
}
```

### 4.5 Authoring ledger

The ledger records authoring events without modifying prior events.

Recommended event properties:

```json
{
  "event": "review-completed",
  "assertion": "urn:aduc:assertion:river-flow-reviewed-1",
  "actor": "urn:person:reviewer-7",
  "at": "2026-07-13T14:55:00Z"
}
```

Suggested events:

- `source-inspected`;
- `proposal-created`;
- `proposal-published`;
- `review-started`;
- `review-completed`;
- `proposal-rejected`;
- `mapping-contested`;
- `canonical-publication`;
- `profile-validated`;
- `source-version-changed`.

The ledger is evidence of process. It does not replace PROV-O for portable provenance.

## 5. End-to-end workflow

## Step 1 — Identify and freeze the source

The curator must record:

- source-description identifier;
- source version or SHA-256 digest;
- local-reference scheme;
- field inventory;
- source authority identifier when known.

A mutable `latest` URL without version or digest is insufficient.

Output:

```text
source data
+ immutable source description
+ field inventory
```

## Step 2 — Enumerate every local field

Every field in the selected source description is added to the coverage report.

Example:

```json
[
  {
    "localReference": "/properties/station",
    "state": "unmapped",
    "assertionIds": []
  },
  {
    "localReference": "/properties/flow",
    "state": "unmapped",
    "assertionIds": []
  }
]
```

No targetless `unknown` assertion is created.

## Step 3 — Collect evidence

Evidence may include:

- source documentation;
- data dictionaries;
- declared units;
- code lists;
- representative values;
- field descriptions;
- publisher statements;
- existing ontology mappings;
- review records.

Evidence must be referenced by stable identifier. Sensitive evidence may remain private, but consumers must then know that it is inaccessible rather than treating it as verified.

## Step 4 — Produce an inferred proposal

The inference producer creates a new immutable assertion with:

- unique assertion identifier;
- local reference;
- semantic target;
- explicit mapping relation;
- `status: inferred`;
- confidence;
- identified confidence method;
- asserting agent;
- assertion time;
- evidence references.

The proposal is validated before review.

## Step 5 — Review the proposal

The reviewer answers the minimum questions in section 8.

Possible decisions:

### Accept as reviewed

Create a new `reviewed` assertion with a new identifier and `supersedes` pointing to the inferred assertion.

### Revise

Create a new inferred or reviewed assertion with a corrected target, relation or evidence. Do not edit the published proposal.

### Reject

Do not publish a new positive mapping. Record the rejection in the authoring ledger and return the field to `unmapped` unless another assertion remains active.

### Contest

Create a `contested` assertion with evidence describing the dispute. Automatic use is blocked.

## Step 6 — Publish canonically when authorized

Only the recognized source authority may publish a `canonical` assertion.

The source authority creates a new assertion that:

- uses a new assertion identifier;
- identifies the source authority in `assertedBy`;
- contains no confidence score;
- preserves relation strength;
- may supersede the reviewed or inferred assertion;
- remains bound to the exact source version.

A canonical assertion can still be challenged. Canonicality means publisher authority, not universal truth.

## Step 7 — Validate the profile

Run:

```bash
python tools/aduc_validate.py path/to/profile.aduc.json --format json
```

For a canonical profile, a deployment may declare its locally trusted authority:

```bash
python tools/aduc_validate.py path/to/profile.aduc.json \
  --trusted-authority https://publisher.example/id/data-authority
```

The command must exit successfully before publication. Warnings must be reviewed and retained with the validation record.

## Step 8 — Update coverage and ledger

After publication:

- update the field coverage state;
- append the new assertion identifier;
- append the authoring event;
- record validator result and tool version;
- preserve all earlier profiles and assertions.

## Step 9 — Handle source changes

When the source schema changes:

1. create a new source-description version;
2. create a new authoring package;
3. mark every mapping as requiring revalidation;
4. copy mappings only after checking that the local reference and meaning remain valid;
5. issue new assertions bound to the new source version.

Mappings must never migrate silently across source versions.

## 6. Immutable lifecycle

```text
source inspected
      ↓
inferred assertion A
      ↓ human review
reviewed assertion B ──supersedes──> A
      ↓ source authority publication
canonical assertion C ──supersedes──> B
```

A dispute creates an additional immutable record:

```text
canonical assertion C
      ↓ challenged
contested assertion D ──references evidence of challenge
```

No published assertion is edited in place.

## 7. Proposal and review records

These records belong to authoring state, not the portable profile.

### 7.1 Proposal record

Recommended shape:

```json
{
  "localReference": "/properties/flow",
  "candidateTarget": "https://example.org/environment/WaterDischarge",
  "mappingRelation": "http://www.w3.org/2004/02/skos/core#exactMatch",
  "confidence": 0.91,
  "confidenceMethod": "urn:method:manual-evidence-score:1",
  "evidence": [
    "urn:evidence:river-doc-flow",
    "urn:evidence:unit-m3-per-second"
  ],
  "producer": "urn:tool:authoring-example"
}
```

### 7.2 Review record

Recommended shape:

```json
{
  "proposalAssertion": "urn:aduc:assertion:river-flow-inferred-1",
  "decision": "accept",
  "reviewer": "urn:person:hydrology-reviewer-7",
  "at": "2026-07-13T14:55:00Z",
  "reason": "Documentation and declared unit confirm the proposed concept.",
  "resultingAssertion": "urn:aduc:assertion:river-flow-reviewed-1"
}
```

Allowed decision values for an implementation profile may include:

- `accept`;
- `revise`;
- `reject`;
- `contest`.

These shapes are informative and are not yet part of the normative ADUC schema.

## 8. Minimum human-review questions

A reviewer must answer:

1. Does the local reference resolve uniquely in the declared source version?
2. Does the target identifier resolve to the intended concept?
3. Is the selected mapping relation no stronger than the evidence supports?
4. Are units, code lists and temporal meaning consistent with the target?
5. Does the evidence come from a credible and relevant source?
6. Is the confidence method identified and appropriate?
7. Is the proposal confusing semantic correspondence with data quality or factual truth?
8. Does another active assertion conflict with this proposal?
9. Is the reviewer entitled only to review, or also authorized to publish canonical meaning?
10. Does the resulting assertion preserve the earlier assertion through `supersedes`?

## 9. Failure cases

### 9.1 Silent in-place promotion

Changing an existing assertion from `inferred` to `canonical` is forbidden.

### 9.2 Reviewer impersonates the source authority

A reviewer must not publish `canonical` merely because the mapping appears correct.

### 9.3 Targetless unknown assertion

An unmapped field belongs in the coverage report, not in a targetless mapping assertion.

### 9.4 Missing source version

A profile without immutable source-version binding must not be published.

### 9.5 Confidence reused after target change

If a reviewer changes the semantic target or relation, the previous confidence cannot be copied automatically. It must be recomputed or omitted according to status.

### 9.6 Evidence discarded after review

The reviewed or canonical assertion must remain traceable to review or publisher evidence. Superseding the earlier assertion must not erase its evidence.

### 9.7 Canonical assertion with probability

Canonical authority must not be expressed as `confidence: 1.0` or any other score.

### 9.8 Hidden field omission

An authoring system must not claim full coverage while silently omitting fields from the coverage report.

### 9.9 Mutable source reused

A mapping must not be copied from one schema version to another without explicit revalidation.

### 9.10 Private reasoning substituted for evidence

A model's private reasoning or chain-of-thought is not portable evidence. Evidence must be an identifiable document, value pattern, rule, review or other auditable artifact.

## 10. Example A — River data review

Files:

```text
examples/authoring/river/source.json
examples/authoring/river/source.schema.json
examples/authoring/river/inferred.aduc.json
examples/authoring/river/reviewed.aduc.json
examples/authoring/river/authoring-state.json
```

Lifecycle:

1. Three source fields are enumerated.
2. `flow` is proposed as `WaterDischarge` with inferred confidence.
3. A hydrology reviewer confirms the mapping.
4. A new reviewed assertion supersedes the inferred assertion.
5. `station` and `quality` remain explicitly unmapped in coverage.

## 11. Example B — Factory canonical publication

Files:

```text
examples/authoring/machine/source.json
examples/authoring/machine/source.schema.json
examples/authoring/machine/inferred.aduc.json
examples/authoring/machine/canonical.aduc.json
examples/authoring/machine/authoring-state.json
```

Lifecycle:

1. `motor_heat` is initially inferred as a close match to generic temperature.
2. The source authority determines the precise meaning is motor winding temperature.
3. A new canonical exact mapping supersedes the inferred assertion.
4. No confidence is attached to the canonical assertion.
5. `equipment_id` and `unit` remain explicitly unmapped in coverage.

## 12. Manual completion checklist

A manual authoring package is complete only when:

- [ ] source description is immutable or versioned;
- [ ] every source field appears in coverage;
- [ ] every published assertion has a unique identifier;
- [ ] inferred assertions contain confidence, method and evidence;
- [ ] reviewed and canonical promotion creates new assertions;
- [ ] canonical publisher authority is identified;
- [ ] relation strength is explicit;
- [ ] evidence remains traceable;
- [ ] the portable profile passes `tools/aduc_validate.py`;
- [ ] the validation event is appended to the ledger;
- [ ] earlier profiles and assertions are retained.

## 13. Gate 4 completion criterion

Gate 4 passes when an independent developer can manually follow this workflow and produce a schema-valid, semantically valid profile while preserving:

- source-version binding;
- field coverage;
- inferred uncertainty;
- reviewer and authority separation;
- immutable assertion history;
- validator evidence.

Automatic inference, UI design and registry work remain blocked until this manual workflow proves usable.
