# ADR-0002: ADUC as an AI semantic mapping and conformance profile

- Status: partially superseded
- Date: 2026-07-13
- Issue: #5
- Originally superseded: the broad standalone universal-data-model hypothesis in the bootstrap draft
- Superseded for global project scope by: ADR-0004 and ADR-0004A
- Retained scope: semantic-mapping lifecycle, authority, evidence, consumer behavior, interoperability tests and stop/pivot rules

## Decision relationship clarification

ADR-0004 restores the broader ten-block AI Data Understanding Core as the official global project direction. ADR-0004A makes the precedence explicit.

Therefore, this ADR no longer governs statements that limit ADUC permanently to a narrow semantic-mapping profile or reject the broader Core as the global project. Those statements remain part of the historical Gate 0 reasoning.

This ADR remains authoritative for the standalone semantic-mapping profile and for the safeguards it introduced: reuse of established standards, mapping authority, evidence, method-bound confidence, preservation of uncertainty and conflict, deterministic consumer behavior, prohibition of hidden provider-specific mappings, independent-consumer testing and stop/pivot conditions.

## Context

The initial vision proposed a model-independent contract describing a source's structure, semantics, identity, context, provenance, uncertainty, relations and usage policy to AI systems.

Gate 0 research found that established standards already express almost every proposed category when composed:

- JSON Schema describes JSON structure and validation;
- JSON-LD and RDF provide global semantic identifiers and relations;
- Croissant describes datasets, resources, records, fields and extraction for machine-learning use;
- PROV-O describes provenance;
- DQV describes data quality;
- ODRL describes permissions, prohibitions and duties;
- DCAT supports dataset and service discovery;
- OpenAPI describes HTTP APIs;
- CloudEvents describes event envelopes;
- SOSA/SSN describes observations and sensors;
- SHACL validates RDF graphs;
- MCP exposes resources and tools to AI applications;
- operational data-contract standards describe ownership, service levels and quality expectations.

Creating independent ADUC objects for all these concerns would duplicate existing work, increase the developer burden and weaken interoperability.

A narrower gap remains: independent AI systems lack a small, deterministic profile governing the lifecycle and consumption of semantic mappings that may initially be inferred rather than authoritative.

## Decision

ADUC will continue as a lightweight **AI semantic mapping and conformance profile over established standards** for the bounded experimental profile defined by this ADR.

This profile does not define a new universal data model or ontology. Its purpose is to make semantic mappings portable, reviewable and consistently consumed by independent AI systems. The broader project scope is now governed by ADR-0004 and ADR-0004A.

### Exact bounded problem

A source often contains local names such as `tmp`, `q`, `quality`, `MAIN-B` or `recorded_at`. A model, developer or publisher may map these local locations or values to existing semantic identifiers. Today, that mapping is commonly hidden in prompts, connector code or provider-specific configuration, and its authority or uncertainty is easily lost.

ADUC addresses this question:

> How can a local source location or value be mapped to an existing semantic identifier while preserving who asserted the mapping, whether it is inferred or authoritative, what evidence supports it, how certain it is, and how every conforming consumer must behave when the mapping is uncertain or contested?

### Target users

The initial target users are:

- data and AI platform engineers integrating the same source with multiple models;
- dataset publishers wanting machine-consumable mappings without replacing their existing formats;
- agent developers requiring portable meaning across providers;
- governance and audit teams reviewing which mappings are inferred, verified or publisher-authoritative;
- tool builders implementing authoring, validation and conformance testing.

### v0.1 resource boundary

Version 0.1 of this standalone profile is limited to:

- JSON and CSV datasets;
- tabular or record-oriented data;
- fields and, where required, enumerated values;
- existing source descriptions represented through Croissant and/or JSON Schema;
- local references expressed as a Croissant field identifier, JSON Pointer, or an equivalent deterministic field reference defined by the selected source profile.

The following are outside this standalone profile's v0.1 boundary:

- arbitrary PDFs, images, audio and video;
- live events and sensor streams;
- full API-operation semantics;
- agent memory;
- decisions and actions;
- domain ontologies;
- automatic policy enforcement;
- the anticipation engine.

These exclusions do not define the permanent limits of the broader full-Core program. Future source horizons remain gated by ADR-0004A and `docs/project/SOURCE_AND_EXTENSION_HORIZONS.md`.

### Standards that must be reused

The v0.1 profile must reuse rather than duplicate:

- **JSON Schema Draft 2020-12** for JSON validation;
- **JSON-LD / RDF** for semantic identifiers and relations;
- **Croissant 1.1** for dataset, resource, record and field description when applicable;
- **PROV-O** for mapping provenance;
- **DQV** for data-quality claims rather than semantic-mapping confidence;
- **ODRL** for detailed usage policies when needed.

DCAT, OpenAPI, CloudEvents, SOSA/SSN, SHACL and MCP remain integration targets or future profiles, not v0.1 replacements.

### Smallest candidate mapping assertion

The first Gate 1 model will test whether the following conceptual information is both necessary and sufficient:

```json
{
  "localReference": "records/flow",
  "semanticTarget": "https://example.org/concepts/WaterDischarge",
  "status": "inferred",
  "confidence": 0.91,
  "assertedBy": "urn:model:mapping-agent:1",
  "evidence": [
    "urn:evidence:unit-m3-per-second",
    "urn:evidence:source-documentation"
  ],
  "validFor": "urn:source-schema:river-api:4",
  "createdAt": "2026-07-13T12:00:00Z"
}
```

This example is conceptual and not yet normative. Gate 1 must prove every field is required or remove it.

Candidate statuses are:

- `unknown`;
- `inferred`;
- `reviewed`;
- `verified`;
- `canonical`;
- `contested`;
- `deprecated`.

The status vocabulary and transitions are not normative until Gate 1 completes.

### Deterministic consumer rules

A conforming consumer must eventually be testable against rules including:

1. It must not silently promote an `inferred` mapping to `verified` or `canonical`.
2. It must preserve the local source term or reference alongside the semantic target.
3. It must expose unresolved or contested mappings rather than selecting one invisibly.
4. It must retain mapping provenance and evidence references.
5. It must not treat semantic-mapping confidence as data quality or factual truth.
6. It must support a declared policy for low-confidence mappings, such as reject, request review or continue with warning.
7. It must not add hidden provider-specific mappings during a conformance test.
8. A `canonical` mapping must identify the authority entitled to publish meaning for the source.

Gate 1 will refine these rules into normative requirements and negative fixtures.

### Falsifiable interoperability promise

The first claim to test is:

> Given two incompatible JSON or CSV datasets, existing Croissant/JSON Schema descriptions, and the same ADUC mapping assertions, at least two independent AI consumers can identify the same comparable concepts, preserve the same mapping authority states, perform declared unit and time alignment, and expose the same unresolved identity ambiguity without provider-specific hidden mappings.

The claim fails if:

- the consumers require separate semantic mappings;
- either consumer silently promotes inferred meaning;
- comparable fields cannot be identified from the shared artifacts;
- uncertainty or contested mappings are lost;
- the result depends on undocumented prompts or private configuration.

### Stop or pivot condition

The standalone semantic-mapping profile must stop defining a separate profile and become tooling or an upstream contribution to an existing standard if any of the following becomes true:

1. Croissant, a recognized JSON-LD profile or another maintained standard provides equivalent mapping status, authority, evidence, consumer behavior and conformance semantics.
2. The profile does not reduce provider-specific remapping in the reference demonstration.
3. Independent implementers cannot reproduce the same interpretation rules.
4. The required profile becomes more complex than directly using the underlying standards.
5. No external developer can author or consume a basic profile from the documentation without maintainer assistance.

These conditions continue to govern the profile and relevant full-Core claims. They do not by themselves cancel the broader Core when another Core dimension remains distinct and justified.

### Consequences for the bootstrap schema

The historical bootstrap `schema/aduc-core.schema.json` was a repository-validation scaffold only. Its broad top-level objects were not accepted by this ADR as the immediate mapping-profile model.

Subsequent ADRs, beginning with ADR-0004, later established and implemented the normative full-Core object model and schema family. The historical Gate 0 statement must not be read as invalidating those later accepted decisions.

### Consequences for the project name

`AI Data Understanding Core` and `ADUC` remained working names during the original profile research. ADR-0004 restored the broader project meaning while retaining the requirement for naming and trademark review before any public name freeze.

## Options rejected during Gate 0

### Build the original universal Core as the immediate Gate 1 implementation

Rejected at that stage because it would duplicate established specifications and require unnecessary new vocabulary before the mapping and conformance gap was tested. ADR-0004 later restored the broader Core program with explicit composition boundaries and sequential gates.

### Build only a proprietary SaaS mapper

Rejected as the primary direction because mappings would remain vendor-dependent and could not establish cross-provider interoperability. Commercial tooling may later implement the open profile.

### Extend Croissant immediately without a separate profile experiment

Not yet selected because the mapping lifecycle and consumer conformance rules must first be proved. If successful and acceptable to the Croissant community, upstream contribution is preferred over permanent duplication.

## Consequences

### Positive

- The semantic-mapping profile has a precise and testable problem.
- Existing standards remain authoritative for their own domains.
- The initial implementation surface becomes much smaller.
- The project can test the mapping gap early instead of spending years on a broad ontology.
- A future commercial compiler or review service can remain compatible with an open profile.
- The profile remains a validated subset of the broader Core.

### Negative

- The profile's value depends on proving behavior across independent consumers, not merely publishing a schema.
- The profile may ultimately become an extension or upstream contribution even while the broader Core continues.
- Readers must follow ADR-0004 and ADR-0004A for the current global project scope.

## Gate decision

Gate 0 passed with the narrowed profile hypothesis as the first implementation experiment.

The subsequent Gate 1 work defined and tested the minimal semantic mapping assertion and status transition model. The broader full-Core direction is governed by ADR-0004, ADR-0004A and the current Core specification.
