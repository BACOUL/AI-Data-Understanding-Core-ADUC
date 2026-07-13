# ADR-0002: ADUC as an AI semantic mapping and conformance profile

- Status: accepted
- Date: 2026-07-13
- Issue: #5
- Supersedes: the broad standalone universal-data-model hypothesis in the bootstrap draft

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

ADUC will continue as a lightweight **AI semantic mapping and conformance profile over established standards**.

ADUC will not define a new universal data model or ontology. Its purpose is to make semantic mappings portable, reviewable and consistently consumed by independent AI systems.

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

Version 0.1 is limited to:

- JSON and CSV datasets;
- tabular or record-oriented data;
- fields and, where required, enumerated values;
- existing source descriptions represented through Croissant and/or JSON Schema;
- local references expressed as a Croissant field identifier, JSON Pointer, or an equivalent deterministic field reference defined by the selected source profile.

The following are outside v0.1:

- arbitrary PDFs, images, audio and video;
- live events and sensor streams;
- full API-operation semantics;
- agent memory;
- decisions and actions;
- domain ontologies;
- automatic policy enforcement;
- the anticipation engine.

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

ADUC must stop defining a separate profile and become tooling or an upstream contribution to an existing standard if any of the following becomes true:

1. Croissant, a recognized JSON-LD profile or another maintained standard provides equivalent mapping status, authority, evidence, consumer behavior and conformance semantics.
2. The profile does not reduce provider-specific remapping in the reference demonstration.
3. Independent implementers cannot reproduce the same interpretation rules.
4. The required profile becomes more complex than directly using the underlying standards.
5. No external developer can author or consume a basic profile from the documentation without maintainer assistance.

### Consequences for the bootstrap schema

The current `schema/aduc-core.schema.json` remains a repository-validation scaffold only. Its broad top-level objects are not accepted as the future normative model.

Gate 1 must replace or sharply reduce the bootstrap model around semantic mapping assertions and references to existing source descriptions. No compatibility guarantee applies to the bootstrap schema.

### Consequences for the project name

`AI Data Understanding Core` and `ADUC` remain working names during research. The name may overstate the narrowed scope. Renaming is deferred until the Gate 1 information model and demonstration language are stable.

## Options rejected

### Build the original universal Core

Rejected because it would duplicate established specifications and require unnecessary new vocabulary.

### Build only a proprietary SaaS mapper

Rejected as the primary direction because mappings would remain vendor-dependent and could not establish cross-provider interoperability. Commercial tooling may later implement the open profile.

### Extend Croissant immediately without a separate profile experiment

Not yet selected because the mapping lifecycle and consumer conformance rules must first be proved. If successful and acceptable to the Croissant community, upstream contribution is preferred over permanent duplication.

## Consequences

### Positive

- The project has a precise and testable problem.
- Existing standards remain authoritative for their own domains.
- The implementation surface becomes much smaller.
- The project can fail early instead of spending years on a broad ontology.
- A future commercial compiler or review service can remain compatible with an open profile.

### Negative

- The project is less expansive than the original vision.
- Its value depends on proving behavior across independent consumers, not merely publishing a schema.
- The project may ultimately become an extension or tool rather than a standalone standard.
- The current bootstrap schema will probably be replaced.

## Gate decision

Gate 0 passes with the narrowed profile hypothesis.

The next gate is Gate 1 — Core information model. Its first task is to define and test the minimal semantic mapping assertion and status transition model without adding dataset, provenance, quality or policy models already covered by existing standards.
