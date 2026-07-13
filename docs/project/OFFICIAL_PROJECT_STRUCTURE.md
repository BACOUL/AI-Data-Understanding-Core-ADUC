# Official ADUC Project Structure

- Status: Maintainer-approved project structure
- Working name: AI Data Understanding Core (ADUC)
- Name status: Provisional; do not register or freeze before verification
- Public language: English
- Date: 2026-07-13

## Mission

> Create an open standard that allows any data resource to describe its structure, meaning, context, provenance, uncertainty, relations, and conditions of use to any AI system.

## Initial promise

> Two incompatible sources described with ADUC can be understood and compared correctly by multiple AI systems without a different semantic integration for every model.

## Problem solved

Data formats describe syntax better than meaning. A value such as `flow: 118` does not state its concept, unit, time, producer, reliability, comparability, or permitted use. Organizations repeatedly rebuild those explanations in prompts, mappings, connectors, dictionaries, conversion code, and domain-specific integration layers.

ADUC turns this repeated work into a portable, versioned, inspectable contract.

## Product boundary

ADUC is not a JSON replacement, database, universal ontology, AI model, anticipation engine, or agent communication protocol. It is not a direct competitor to MCP, Croissant, JSON-LD, RDF, PROV-O, DQV, ODRL, OpenAPI, or CloudEvents.

ADUC reuses these standards and adds a coherent AI-facing contract layer.

```text
Original data
    ↓
ADUC contract
    ↓
Shared understanding
    ↓
AI systems, agents and applications
```

## Six project components

```text
ADUC
├── 1. Core Specification
├── 2. Contract Format
├── 3. Compiler
├── 4. Validator
├── 5. Semantic Registry
└── 6. Extensions
```

### 1. Core Specification

Defines common blocks, identifiers, semantic states, confidence, versioning, compatibility, consumer obligations, and extension rules. The Core must remain small and domain-independent.

### 2. Contract Format

The contract accompanies the original resource without rewriting it.

```text
measurements.csv
measurements.aduc.json
```

### 3. Compiler

Reference compiler pipeline:

```text
JSON or CSV
    ↓
Structural analysis
    ↓
Semantic inference
    ↓
Ambiguity detection
    ↓
Provisional ADUC contract
```

All automatic proposals begin as inferred and require explicit review or canonical publication.

### 4. Validator

Checks schema conformance, required information, references, status and confidence rules, units, versions, contradictions, and locally determinable semantic conflicts.

### 5. Semantic Registry

References reusable concepts, definitions, namespaces, owners, versions, equivalent concepts, broader or narrower concepts, and compatible units. It does not store enterprise data.

### 6. Extensions

Planned extension families:

- Dataset Extension;
- Live Data Extension;
- Document Extension;
- Agent Memory Extension;
- Scientific Data Extension;
- Situation & Action Extension;
- domain vocabularies.

The anticipation engine is a later application of ADUC Core plus Live Data and Situation & Action extensions. It remains a separate project.

## Core information blocks

The complete v0.1 candidate contains:

```text
aduc
resource
structure
semantics
identity
context
provenance
uncertainty
relations
policy
```

The authoritative working draft is `spec/ADUC_CORE_SPEC_0_1.md`.

## Epistemic states

The intended full Core lifecycle distinguishes:

- `unknown`;
- `inferred`;
- `reviewed`;
- `verified`;
- `canonical`;
- `contested`;
- `deprecated`.

The current implemented semantic-mapping profile supports only `inferred`, `reviewed`, `canonical`, and `contested`. This limitation is explicit and must not be mistaken for the complete final Core.

## Strict MVP

The first release supports only:

- JSON and CSV;
- tabular or record-oriented sources;
- primitive types;
- dates and times;
- units;
- identifiers;
- concepts;
- elementary provenance;
- uncertainty;
- human validation;
- two-source comparison.

## Required operations

- `infer`
- `review`
- `validate`
- `compare`
- `export`

## Version 0.1 deliverables

Version 0.1 is complete only when all twelve deliverables exist:

1. Core specification;
2. official JSON Schema;
3. ten valid examples;
4. ten invalid examples;
5. CLI validator;
6. JSON and CSV compiler;
7. minimal review interface;
8. Core vocabulary;
9. two-source comparison;
10. two-model demonstration;
11. conformance suite;
12. "Try in 5 minutes" documentation.

## Mandatory construction order

```text
1. Core
2. Schema
3. Validator
4. Examples
5. JSON/CSV compiler
6. Multi-model demonstration
7. Extensions
8. Anticipation engine
```

This order is a project constraint. A change requires a documented ADR.

## Repository target structure

```text
aduc/
├── README.md
├── LICENSE
├── GOVERNANCE.md
├── CONTRIBUTING.md
├── CHANGELOG.md
│
├── spec/
│   ├── ADUC_CORE_SPEC_0_1.md
│   ├── CONFORMANCE.md
│   ├── VERSIONING.md
│   └── EXTENSIONS.md
│
├── schema/
│   ├── aduc-core.schema.json
│   ├── aduc-resource.schema.json
│   ├── aduc-semantics.schema.json
│   └── aduc-policy.schema.json
│
├── vocabulary/
│   ├── core.jsonld
│   ├── units.jsonld
│   └── README.md
│
├── packages/
│   ├── validator/
│   ├── compiler/
│   ├── registry-client/
│   └── comparator/
│
├── sdk/
│   ├── typescript/
│   └── python/
│
├── cli/
│   └── aduc/
│
├── examples/
│   ├── basic-json/
│   ├── basic-csv/
│   ├── temperature-comparison/
│   ├── valid/
│   └── invalid/
│
├── tests/
│   ├── schema/
│   ├── interoperability/
│   ├── mappings/
│   └── conformance/
│
├── apps/
│   ├── review-ui/
│   ├── validator-web/
│   └── interoperability-demo/
│
├── website/
│   ├── index.html
│   ├── specification.html
│   ├── architecture.html
│   ├── roadmap.html
│   ├── example.html
│   ├── docs.html
│   └── assets/
│
└── docs/
    ├── architecture/
    ├── decisions/
    ├── project/
    ├── use-cases/
    └── roadmap/
```

The repository may reach this target incrementally. Empty directories must not be created merely to imitate completion.

## Relationship to TimeProofs

TimeProofs may later timestamp and prove published ADUC releases. It must not own the Core, define Core semantics, or be required to validate an ADUC contract. Both projects remain independently usable.

## Governance

Initial governance:

- one principal maintainer;
- public specifications;
- written proposals;
- public ADRs;
- versioned releases;
- no silent normative changes.

Future governance after multi-organization adoption:

- technical committee;
- public comment periods;
- extension working groups;
- Core governance separated from commercial products.

## Licensing

- Specification and documentation: CC BY 4.0 target.
- Reference code: Apache License 2.0.

## Business model

The standard remains open. Commercial value comes from adoption tooling:

- hosted compiler;
- large-volume automated analysis;
- enterprise connectors;
- collaborative review UI;
- private semantic registry;
- change monitoring;
- hosted versioning;
- on-premises installation;
- support, audit, and certification.

Central commercial product:

> Transform an organization's existing data into assets that remain understandable and portable across its AI systems.

## Success criteria

The project succeeds when:

- a person understands the format in less than thirty minutes;
- a developer creates a contract without maintainer assistance;
- one contract is usable by at least two independent AI systems;
- incompatible sources become comparable;
- uncertainty is preserved rather than hidden;
- no model provider is required;
- an extension can be added without changing the Core.
