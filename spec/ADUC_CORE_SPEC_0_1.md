# AI Data Understanding Core — Core Specification 0.1

- Status: Working Draft
- Working name: AI Data Understanding Core (ADUC)
- Version: `0.1.0-draft`
- Language: English
- Date: 2026-07-13
- License target: Creative Commons Attribution 4.0

> ADUC is a working name. It must not be treated as a registered, protected, or final public name until naming and trademark checks are complete.

## 1. Mission

ADUC defines an open, model-independent contract that allows a data resource to describe its structure, meaning, context, provenance, uncertainty, relations, and conditions of use to AI systems, agents, and applications.

The initial promise is:

> Two incompatible sources described with ADUC can be understood and compared consistently by multiple AI systems without rebuilding a different semantic integration for every model.

This specification defines the intended full Core. The repository's existing semantic-mapping profile is the first implemented subset of this Core, not the final complete Core.

## 2. Problem statement

A machine-readable value is often syntactically readable but semantically incomplete.

Example input:

```json
{
  "station": "R42",
  "flow": 118,
  "quality": 2
}
```

A consumer cannot determine from this object alone:

- what `flow` represents;
- the unit of `118`;
- the meaning of `quality = 2`;
- the observation time;
- the producing organization or instrument;
- the reliability and uncertainty of the measurement;
- whether the value is comparable to another source;
- the permitted purposes and restrictions.

Organizations repeatedly encode this missing meaning in prompts, ETL pipelines, connector code, data dictionaries, conversion rules, and undocumented domain knowledge. This work is duplicated across systems and model providers.

ADUC makes that meaning portable, inspectable, versioned, and reusable.

## 3. What ADUC is not

ADUC is not:

- a replacement for JSON, CSV, Parquet, RDF, or databases;
- a universal ontology containing all human knowledge;
- an AI model;
- an anticipation or decision engine;
- an agent communication protocol;
- a replacement for MCP, JSON-LD, Croissant, PROV-O, DQV, ODRL, OpenAPI, or CloudEvents;
- proof that a declared mapping or source is factually correct;
- a mechanism that grants legal permission by declaration alone.

ADUC is an additional portable contract layer:

```text
Original data
    ↓
ADUC contract
    ↓
Shared machine-readable understanding
    ↓
AI systems, agents, analytics and applications
```

## 4. Design principles

### 4.1 Preserve the original resource

An ADUC contract accompanies a source. It does not require rewriting the source.

```text
measurements.csv
measurements.aduc.json
```

### 4.2 Reuse established standards

ADUC MUST reuse existing identifiers, vocabularies, units, provenance terms, policy expressions, and data-description standards when they already express the required meaning.

### 4.3 Small Core, extensible profiles

The Core defines common portable concepts. Domain-specific knowledge belongs in extensions and vocabularies.

### 4.4 Explicit uncertainty

Unknown, inferred, reviewed, canonical, contested, and deprecated information MUST remain distinguishable. Consumers MUST NOT silently promote uncertain information to authoritative information.

### 4.5 Deterministic conformance

Structural and semantic rules that can be checked deterministically SHOULD be enforced by machine-readable schemas and reference tools.

### 4.6 Provider independence

No Core property may depend on a single AI model, vendor, prompt format, hosted registry, or proprietary embedding.

### 4.7 No hidden mappings

A conforming comparison or interoperability test MUST NOT rely on undocumented aliases, private memory, browsing, or provider-specific semantic instructions.

## 5. Core architecture

The project has six principal components:

```text
ADUC
├── 1. Core Specification
├── 2. Contract Format
├── 3. Compiler
├── 4. Validator
├── 5. Semantic Registry
└── 6. Extensions
```

### 5.1 Core Specification

Defines:

- required and optional objects;
- identifiers and references;
- semantic mapping states;
- uncertainty and confidence;
- compatibility behavior;
- versioning and extension rules;
- minimum consumer obligations.

### 5.2 Contract Format

A portable JSON or JSON-LD document accompanying the resource.

### 5.3 Compiler

A reference implementation that analyses JSON and CSV sources and proposes a provisional contract. Compiler output is inferred until reviewed or canonically published.

### 5.4 Validator

Checks structural conformance, references, status rules, units, version compatibility, and semantic conflicts that can be determined locally.

### 5.5 Semantic Registry

A reusable concept catalogue. The registry stores definitions and relations, not enterprise source data.

### 5.6 Extensions

Planned extension families:

- Dataset Extension;
- Live Data Extension;
- Document Extension;
- Agent Memory Extension;
- Scientific Data Extension;
- Situation & Action Extension;
- domain vocabularies.

The anticipation engine is a later application of ADUC Core plus Live Data and Situation & Action extensions. It is not part of the Core.

## 6. Core document model

A candidate complete Core contract uses nine top-level blocks:

```json
{
  "aduc": {},
  "resource": {},
  "structure": {},
  "semantics": {},
  "identity": {},
  "context": {},
  "provenance": {},
  "uncertainty": {},
  "relations": [],
  "policy": {}
}
```

During the draft phase, implementations MAY support only a declared profile of these blocks. They MUST state which blocks and properties they implement.

## 7. `aduc` block

Describes the contract itself.

```json
{
  "version": "0.1.0",
  "contractId": "urn:aduc:contract:river-r42",
  "status": "inferred",
  "createdAt": "2026-07-13T12:00:00Z",
  "conformsTo": [
    "urn:aduc:core:0.1"
  ]
}
```

Candidate properties:

- `version`: ADUC contract version;
- `contractId`: globally unique contract identifier;
- `status`: publication or authoring status;
- `createdAt`: creation timestamp;
- `updatedAt`: optional new-document publication timestamp;
- `conformsTo`: implemented Core and extension profiles;
- `supersedes`: prior contract identifier;
- `publisher`: contract publisher identifier.

Published contracts are immutable. A corrected contract creates a new identified version.

## 8. `resource` block

Identifies the described data resource.

```json
{
  "type": "dataset",
  "format": "text/csv",
  "location": "./measurements.csv",
  "hash": "sha256:..."
}
```

Candidate properties:

- `type`;
- `format`;
- `location`;
- `hash`;
- `version`;
- `size`;
- `encoding`;
- `schema`;
- `accessMethod`.

A portable contract SHOULD bind to a version or cryptographic digest of the source or source schema.

## 9. `structure` block

Describes how to read the source.

```json
{
  "representation": "table",
  "recordType": "observation",
  "primaryKey": ["station", "timestamp"],
  "fields": {
    "station": {"type": "string"},
    "flow": {"type": "number"},
    "quality": {"type": "integer"},
    "timestamp": {"type": "datetime"}
  }
}
```

The Core SHOULD reuse JSON Schema, Croissant, CSVW, OpenAPI, or another declared structural description instead of duplicating their complete capabilities.

## 10. `semantics` block

Maps local fields to reusable semantic identifiers.

```json
{
  "fields": {
    "flow": {
      "concept": "https://example.org/env/WaterDischarge",
      "unit": "https://qudt.org/vocab/unit/M3-PER-SEC",
      "mappingRelation": "http://www.w3.org/2004/02/skos/core#exactMatch",
      "mappingStatus": "reviewed",
      "confidence": 0.96,
      "confidenceMethod": "urn:aduc:method:human-review-v1",
      "assertedBy": "urn:person:hydrologist-7",
      "evidence": ["urn:evidence:river-dictionary-4"]
    }
  }
}
```

The repository's current semantic-mapping assertion model is the first implemented representation of this block.

A semantic mapping MUST preserve:

- the deterministic local field reference;
- the semantic target;
- the mapping relation;
- the epistemic status;
- the asserting agent or authority;
- the assertion time;
- evidence when required;
- confidence and method when probabilistic;
- lifecycle links when replaced or contested.

## 11. `identity` block

Describes the entities represented by the data.

```json
{
  "subjectField": "station",
  "subjectType": "https://example.org/env/HydrometricStation",
  "identifierScheme": "urn:org-river:station-id"
}
```

Identity claims MUST distinguish:

- exact identity;
- probable identity;
- related entity;
- unresolved identity;
- conflicting identity.

A consumer MUST NOT treat probable identity as exact identity without declared evidence.

## 12. `context` block

Describes temporal, spatial, jurisdictional, and operational context.

```json
{
  "timeField": "timestamp",
  "timezone": "Europe/Paris",
  "spatialCoverage": "France",
  "timeResolution": "PT15M"
}
```

Candidate properties include:

- observation time field;
- event time versus ingestion time;
- timezone;
- interval and resolution;
- spatial coverage;
- coordinate reference system;
- jurisdiction;
- operational environment;
- language and locale.

## 13. `provenance` block

Describes origin and production history.

```json
{
  "producer": "https://example.org/agency/river-monitoring",
  "sourceType": "officialSensorNetwork",
  "method": "ultrasonicMeasurement",
  "generatedAt": "2026-07-13T12:00:00Z"
}
```

ADUC SHOULD reuse PROV-O and other established provenance terms.

A provenance declaration does not itself prove authenticity. Cryptographic signatures and external trust mechanisms are separate concerns.

## 14. `uncertainty` block

Describes known uncertainty, quality limitations, and confidence.

```json
{
  "relativeError": 0.04,
  "confidenceLevel": 0.95,
  "appliesTo": ["flow"],
  "method": "urn:method:sensor-calibration-2026"
}
```

The Core MUST distinguish:

- uncertainty of a measured value;
- confidence in a semantic mapping;
- confidence in entity resolution;
- source quality;
- factual truth;
- authority or publication status.

These are not interchangeable values.

## 15. `relations` block

Links resources, concepts, entities, and derivations.

```json
[
  {
    "type": "derivedFrom",
    "target": "urn:dataset:raw-measurements",
    "status": "canonical"
  }
]
```

Relations SHOULD reuse established vocabularies. Unknown or domain-specific relation types require an explicit namespace and definition.

## 16. `policy` block

Declares intended usage conditions.

```json
{
  "classification": "public",
  "permittedPurposes": [
    "research",
    "floodRiskAnalysis"
  ],
  "prohibitedPurposes": [
    "individualCreditScoring"
  ]
}
```

ADUC SHOULD reuse ODRL or another established policy language when full machine-actionable policy is required.

Policy declarations inform consumers. They do not override law, contracts, access controls, or technical enforcement.

## 17. Epistemic status model

Candidate Core statuses:

| Status | Meaning | Minimum consumer behavior |
|---|---|---|
| `unknown` | No supported interpretation exists | Do not infer a target silently |
| `inferred` | Produced automatically or heuristically | Preserve confidence and evidence; do not treat as authoritative |
| `reviewed` | Examined by a human reviewer | Preserve reviewer identity and review evidence |
| `verified` | Validated by a competent reviewer under a declared process | Preserve process and verifier; do not equate with source ownership |
| `canonical` | Published by the declared source owner or authority | Prefer when authority is trusted and no conflict exists |
| `contested` | Multiple supported interpretations exist | Block automatic authoritative selection |
| `deprecated` | Replaced or no longer recommended | Follow the replacement link when compatible |

The current implemented mapping profile supports `inferred`, `reviewed`, `canonical`, and `contested`. The complete seven-state model is a candidate for the full Core and requires a normative lifecycle ADR before schema implementation.

## 18. Confidence rules

- Confidence MUST be a value from `0` to `1` when used.
- Confidence MUST name its scoring method.
- Confidence expresses uncertainty about the declared claim only.
- `canonical` MUST NOT be assigned a probability merely to imitate authority.
- `unknown` MUST NOT include a fabricated semantic target.
- `contested` MUST include evidence or references for the conflict.

## 19. Consumer obligations

A conforming consumer MUST:

1. validate the declared supported profile;
2. preserve semantic target and mapping relation;
3. preserve epistemic status;
4. preserve unresolved and contested information;
5. avoid hidden target aliases in conformance mode;
6. avoid unit conversion unless units and conversion rules are known;
7. avoid temporal alignment unless time semantics and timezone are known;
8. avoid identity merging unless identity evidence is sufficient;
9. report dimensions that were not evaluated;
10. expose conformance errors rather than silently repairing the contract.

## 20. MVP scope

ADUC v0.1 targets:

- JSON;
- CSV;
- tabular or record-oriented data;
- primitive types;
- dates and times;
- units;
- identifiers;
- semantic concepts;
- elementary provenance;
- uncertainty;
- human validation;
- comparison of two described sources.

Out of scope for the MVP:

- arbitrary documents and images;
- live streaming semantics;
- agent memory;
- autonomous action policy;
- public registry federation;
- anticipation engine behavior.

## 21. Reference operations

### 21.1 `infer`

Analyse a JSON or CSV source and propose:

- field types;
- probable concepts;
- probable units;
- temporal fields;
- identifiers;
- possible relations;
- confidence and evidence.

All proposals begin as `inferred`.

### 21.2 `review`

Prioritize:

- unknown fields;
- mappings below a confidence threshold;
- ambiguous units;
- contradictions;
- unresolved identifiers;
- contested interpretations.

### 21.3 `validate`

Check structural and locally determinable semantic conformance.

### 21.4 `compare`

Determine:

- comparable fields;
- required unit conversions;
- compatible periods;
- possible entity matches;
- unresolved incompatibilities.

### 21.5 `export`

Produce the final portable contract and its versioned manifest.

## 22. Reference demonstration

French source:

```json
{
  "machine": "M42",
  "temp": 89,
  "unite": "C",
  "date": "13/07/2026 14:00"
}
```

US source:

```json
{
  "equipment_id": "MAIN-B",
  "motor_heat": 192.2,
  "unit": "F",
  "recorded_at": "2026-07-13T12:00:00Z"
}
```

The target demonstration MUST show that:

- `temp` and `motor_heat` map to a compatible temperature concept;
- Celsius and Fahrenheit are explicitly convertible;
- `89 °C` equals `192.2 °F` within declared precision;
- the timestamps represent the same instant when timezone information is applied;
- `M42` and `MAIN-B` may represent the same machine;
- machine identity remains uncertain without sufficient evidence;
- two independent AI consumers preserve the same conclusions and uncertainty.

## 23. Version 0.1 completion criteria

Version 0.1 is complete only when all of the following exist:

1. Core specification;
2. official JSON Schema;
3. at least ten valid examples;
4. at least ten intentionally invalid examples;
5. CLI validator;
6. JSON and CSV compiler;
7. minimal review interface;
8. Core vocabulary;
9. comparison of two sources including units, time, and identity uncertainty;
10. demonstration with two independent AI consumers;
11. conformance suite;
12. "Try in 5 minutes" documentation.

Existing tools may satisfy part of these criteria, but the version MUST NOT be declared complete until the full list passes.

## 24. Construction order

The mandatory order is:

1. Core;
2. Schema;
3. Validator;
4. Examples;
5. JSON/CSV compiler;
6. multi-model demonstration;
7. extensions;
8. anticipation engine.

Later implementation work MUST NOT bypass this order without an accepted ADR.

## 25. Governance and licensing

- Specification and documentation target: CC BY 4.0.
- Reference code target: Apache License 2.0.
- Decisions require public ADRs.
- Breaking changes require versioned migration notes.
- No silent normative modifications.
- The Core must remain separable from commercial products.

## 26. Relationship to the current repository implementation

The repository already contains:

- a semantic-mapping assertion model;
- a mapping-profile schema;
- semantic validation;
- comparison tooling;
- JSON-LD/RDF representation;
- a provider-neutral conformance harness.

These artifacts are retained as the current experimental implementation of the `semantics` block and its consumer behavior. They do not by themselves implement the complete Core contract described in this document.

## 27. Open normative decisions

Before `0.1.0-alpha.0`, the project must accept ADRs for:

- exact Core block cardinalities;
- seven-state epistemic lifecycle;
- unit identifier and conversion strategy;
- temporal representation and alignment;
- entity identity and equivalence;
- Core policy profile;
- source structural-description profiles;
- extension discovery;
- registry governance;
- migration from the existing mapping-profile document to the full Core envelope.
