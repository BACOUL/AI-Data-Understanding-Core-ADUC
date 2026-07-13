# Prior-Art and Standards Matrix

- Status: Gate 0 research artifact
- Date: 2026-07-13
- Issue: #3
- Scope: official specifications and project documentation only

## 1. Research question

Does ADUC need to invent a new universal data-understanding model, or can the proposed capabilities already be expressed by composing established standards?

The proposed capability is intentionally tested as a falsifiable claim:

> A source can be described once so that independent AI systems can identify its structure, field meaning, context, provenance, uncertainty or quality, relations, and declared usage conditions without a separate provider-specific semantic mapping.

This document distinguishes:

1. **expressive capability** — whether existing standards can represent the information;
2. **operational interoperability** — whether independent AI consumers receive a small, deterministic profile telling them which standards to use and how to treat uncertain mappings;
3. **adoption and tooling** — whether a practical authoring, review, validation, and multi-model test workflow exists.

## 2. Executive conclusion

### 2.1 No broad expressive void was found

Existing standards can already represent almost every category initially proposed for the ADUC Core:

| Requirement | Existing foundation |
|---|---|
| JSON structure and constraints | JSON Schema |
| Global identifiers and semantic relations | JSON-LD / RDF |
| Dataset resources, fields, extraction and ML portability | Croissant |
| Provenance | PROV-O |
| Dataset and service discovery | DCAT |
| Event envelope and transport metadata | CloudEvents |
| API operations and input/output schemas | OpenAPI |
| LLM access to resources and tools | MCP |
| Quality metadata and measurements | DQV |
| Permissions, prohibitions and duties | ODRL |
| Observations, sensors, procedures and features of interest | SOSA / SSN |
| RDF graph validation | SHACL |
| Operational data-product contracts | Open Data Contract Standard (ODCS) |

Therefore, ADUC must **not** claim that structure, semantics, provenance, quality, policy, observations, APIs or datasets currently lack standard representations.

### 2.2 The defensible gap is operational, not ontological

No reviewed standard provides, as one small cross-resource AI profile, all of the following together:

1. a deterministic declaration of which existing descriptions apply to a source;
2. local-field or local-value mappings to semantic identifiers;
3. an explicit epistemic state for every mapping, such as `inferred`, `reviewed`, `verified`, `canonical`, `contested` or `unknown`;
4. machine-readable confidence and evidence for non-authoritative mappings;
5. authority rules preventing inferred mappings from being silently promoted to canonical meaning;
6. common consumer behavior when mappings are missing, contested or below a confidence threshold;
7. a conformance suite proving that different AI providers interpret the same source compatibly;
8. an authoring workflow that moves from machine inference to human or publisher validation.

This is a **profile, conformance and tooling gap**. It is not evidence for a new universal ontology or a replacement for the standards below.

## 3. Detailed matrix

### 3.1 JSON Schema Draft 2020-12

| Dimension | Assessment |
|---|---|
| Official scope | A JSON-based media type for describing JSON document structure, validation, annotations, references and dialect vocabularies. |
| Resource types | JSON documents and data compatible with the JSON Schema data model. |
| Semantics | Supports annotations and custom vocabularies, but standard keywords primarily describe structural and validation semantics rather than domain meaning. |
| Provenance | No general provenance model. |
| Uncertainty / quality | Constraints can validate numeric ranges or required properties, but no standard epistemic or quality model. |
| Policy | No standard rights or purpose model. |
| AI/model independence | Yes. |
| Reuse by ADUC | Contract shape, validation, versioned dialect and extension vocabulary mechanism. |
| Remaining gap | It does not define domain concept mappings, mapping authority, provenance, policy or AI interpretation behavior. |

**Decision:** ADUC contracts expressed as JSON must be validated with JSON Schema rather than a custom validator language.

### 3.2 JSON-LD 1.1 and RDF

| Dimension | Assessment |
|---|---|
| Official scope | JSON-LD serializes Linked Data in JSON and provides a transition path from existing JSON. RDF is the graph-based abstract data model connecting RDF languages and vocabularies. |
| Resource types | General Web resources, statements and datasets represented as graphs. |
| Semantics | Strong: IRIs, typed values, vocabularies, graphs and relations provide global semantic identity. |
| Provenance | Expressible through vocabularies such as PROV-O; not intrinsic to every statement. |
| Uncertainty / quality | Expressible through additional vocabularies or statement annotations; no mandatory universal model. |
| Policy | Expressible through vocabularies such as ODRL; not intrinsic. |
| AI/model independence | Yes. |
| Reuse by ADUC | Concept identifiers, namespaces, relations, external vocabularies and graph interoperability. |
| Remaining gap | RDF/JSON-LD deliberately provides a general semantic foundation, not a small AI-specific profile with mapping status, confidence thresholds and required consumer behavior. |

RDF 1.2 also introduces triple terms that make statements about statements easier to represent. This further reduces any justification for ADUC to invent a separate graph or assertion model.

**Decision:** ADUC must reuse resolvable identifiers and JSON-LD/RDF compatibility. It must not define a competing universal concept graph.

### 3.3 MLCommons Croissant 1.1

| Dimension | Assessment |
|---|---|
| Official scope | A metadata format that simplifies dataset use by ML models and supports discoverability, portability, reproducibility and responsible-AI use cases. |
| Resource types | Datasets, files, file sets, record sets, fields and live datasets. |
| Semantics | Strong for dataset structure, extraction, field data types, references, enumerations and external semantic identifiers through JSON-LD. |
| Provenance | Strong: Croissant 1.1 recommends PROV-O and permits provenance at dataset, resource, record-set, field and individual-value levels. |
| Uncertainty / quality | Supports validation and annotations, but does not define a general mapping-confidence or epistemic-authority model. |
| Policy | Supports machine-readable data-use conditions through external vocabularies such as DUO and ODRL. |
| AI/model independence | Yes; designed for interchange among ML frameworks and tools. |
| Reuse by ADUC | Dataset/resource/record/field description, extraction, live-dataset handling, JSON-LD integration, provenance and use-condition patterns. |
| Remaining gap | It is dataset-centered and does not standardize the lifecycle and authority of automatically inferred semantic mappings or cross-provider interpretation tests. |

Croissant is the closest existing specification to the initial ADUC vision. Recreating its dataset, resource, field, extraction, provenance or policy structures under ADUC names would be duplication.

**Decision:** For JSON/CSV datasets, ADUC should profile or extend Croissant rather than create an independent dataset description model.

### 3.4 PROV-O

| Dimension | Assessment |
|---|---|
| Official scope | An OWL2 ontology representing and interchanging provenance across systems and contexts. |
| Resource types | General entities, activities and agents. |
| Semantics | Strong for provenance relationships and specializable domain models. |
| Provenance | Primary purpose. |
| Uncertainty / quality | Can record derivation and responsible agents, but does not itself define confidence or data quality. |
| Policy | Not its primary scope. |
| AI/model independence | Yes. |
| Reuse by ADUC | Source, generation, attribution, derivation, activities, agents and bundles. |
| Remaining gap | It explains origin and transformation, not whether a semantic mapping is inferred, accepted, contested or canonical. |

**Decision:** ADUC must reference PROV-O terms instead of defining a second provenance vocabulary.

### 3.5 DCAT 3

| Dimension | Assessment |
|---|---|
| Official scope | RDF vocabulary for interoperability between Web data catalogs. |
| Resource types | Catalogs, datasets, distributions, data services and related resources. |
| Semantics | Metadata and classification of catalog resources; compatible with controlled vocabularies. |
| Provenance | Can be combined with PROV-O and Dublin Core terms. |
| Uncertainty / quality | Can be extended with DQV; no general field-level uncertainty model. |
| Policy | Rights and licenses can be described; detailed usage policies need complementary vocabularies. |
| AI/model independence | Yes. |
| Reuse by ADUC | Dataset/service discovery, distributions, access services, coverage and catalog integration. |
| Remaining gap | DCAT helps an agent find a dataset or service but does not define field-level interpretation or mapping authority. |

**Decision:** ADUC discovery must build on DCAT rather than create a global source catalog model.

### 3.6 CloudEvents

| Dimension | Assessment |
|---|---|
| Official scope | Common formats for describing event data across services, platforms and systems. |
| Resource types | Events and event payloads. |
| Semantics | Standard envelope attributes such as identity, source, type and time; payload meaning remains application-defined. |
| Provenance | Source and event identity provide limited origin metadata, not a full provenance graph. |
| Uncertainty / quality | Not standard in the core event envelope. |
| Policy | Not standard in the core event envelope. |
| AI/model independence | Yes. |
| Reuse by ADUC | Event envelope, identifiers, source, type, time and content-type conventions. |
| Remaining gap | Does not define the domain semantics, evidence or confidence of event payload fields. |

**Decision:** Live-event support should use CloudEvents envelopes with referenced semantic profiles; ADUC must not define another event transport format.

### 3.7 Model Context Protocol (MCP)

| Dimension | Assessment |
|---|---|
| Official scope | Open protocol integrating LLM applications with external data sources and tools through JSON-RPC. |
| Resource types | Resources, prompts, tools and protocol messages. |
| Semantics | Resources have URIs and metadata; tools have names and input/output schemas. Domain meaning is supplied by server descriptions and schemas, not globally standardized. |
| Provenance | No general data-provenance model. |
| Uncertainty / quality | No general mapping-confidence or data-quality model. |
| Policy | Security and authorization guidance exists, but MCP is not a general data-usage policy vocabulary. |
| AI/model independence | Yes, explicitly intended for composable LLM integrations. |
| Reuse by ADUC | Discovery and delivery of semantic profiles as resources; exposure of authoring, validation and comparison tools. |
| Remaining gap | MCP standardizes access and invocation, not a shared semantic contract for arbitrary payloads. |

**Decision:** ADUC artifacts can be exposed through MCP, but ADUC must remain transport-independent.

### 3.8 OpenAPI 3.2

| Dimension | Assessment |
|---|---|
| Official scope | Language-agnostic interface description for HTTP APIs, enabling humans and computers to discover service capabilities and interact with minimal implementation logic. |
| Resource types | HTTP APIs, operations, parameters, requests, responses and schemas. |
| Semantics | Strong operational and structural description; domain semantics rely on names, descriptions, references and extensions. |
| Provenance | Not a general provenance model. |
| Uncertainty / quality | Constraints can be expressed through schemas; no general epistemic model. |
| Policy | Security schemes describe authentication; not general purpose or reuse policy. |
| AI/model independence | Yes. |
| Reuse by ADUC | API discovery, operations, JSON Schema-compatible payload shapes and extension points. |
| Remaining gap | A machine can know how to call an API without knowing that two differently named response fields denote the same domain concept or that a mapping is only inferred. |

**Decision:** API support should be an OpenAPI semantic profile or overlay, not an alternative API-description language.

### 3.9 Data Quality Vocabulary (DQV)

| Dimension | Assessment |
|---|---|
| Official scope | Extension to DCAT for publishing, exchanging and consuming quality metadata throughout a dataset lifecycle. |
| Resource types | Datasets and metadata, with quality measurements, annotations, policies and certificates. |
| Semantics | Uses RDF vocabularies and quality dimensions/metrics. |
| Provenance | Can be combined with PROV-O. |
| Uncertainty / quality | Primary purpose is quality metadata; uncertainty may be represented through domain metrics but is not reduced to one universal confidence value. |
| Policy | Includes quality policies and certificates, not general usage permission semantics. |
| AI/model independence | Yes. |
| Reuse by ADUC | Quality dimensions, metrics, measurements, annotations and certificates. |
| Remaining gap | Does not define the authority state and evidence of field-to-concept mappings or consumer fallback behavior. |

**Decision:** ADUC must distinguish data quality from semantic-mapping confidence and reuse DQV for quality claims.

### 3.10 ODRL Information Model 2.2

| Dimension | Assessment |
|---|---|
| Official scope | Standard model for permissions, prohibitions, duties and constraints associated with resources. |
| Resource types | General assets/resources and policies. |
| Semantics | Strong for machine-readable policy expressions. |
| Provenance | Can identify policy parties but is not a provenance model. |
| Uncertainty / quality | Not its scope. |
| Policy | Primary purpose. |
| AI/model independence | Yes. |
| Reuse by ADUC | Permissions, prohibitions, duties, purposes, parties and constraints. |
| Remaining gap | Declaring a policy does not enforce it, and ODRL does not describe field semantics or mapping confidence. |

**Decision:** ADUC policy declarations should reference ODRL expressions and must state that declarations are not enforcement.

### 3.11 SOSA / SSN

| Dimension | Assessment |
|---|---|
| Official scope | Ontologies describing sensors, observations, procedures, features of interest, samples, observed properties and actuators. |
| Resource types | Sensors, observations, samples, actuations and related entities. |
| Semantics | Strong for observation context, phenomenon time, result time, procedure and feature/property relationships. |
| Provenance | Some observational origin is represented; full lineage can use PROV-O. |
| Uncertainty / quality | Domain extensions can represent accuracy and quality; no universal field-mapping status workflow. |
| Policy | Not its scope. |
| AI/model independence | Yes. |
| Reuse by ADUC | Observation semantics, temporal distinctions, procedures, results and features of interest. |
| Remaining gap | Domain-specific to observations and sensing; not a cross-resource AI interpretation profile. |

**Decision:** ADUC must use SOSA/SSN for sensor and observation examples rather than invent generic sensor terms.

### 3.12 SHACL 1.2

| Dimension | Assessment |
|---|---|
| Official scope | Language for describing and validating RDF graphs. |
| Resource types | RDF data graphs and shapes graphs. |
| Semantics | Validates semantic graph structures and constraints. |
| Provenance | Not a provenance model. |
| Uncertainty / quality | Can constrain fields carrying uncertainty/quality values but does not define their meaning. |
| Policy | Not a policy model. |
| AI/model independence | Yes. |
| Reuse by ADUC | Validation of RDF/JSON-LD representations and semantic constraints. |
| Remaining gap | It validates graph conformance but does not specify the AI interpretation profile or mapping lifecycle. |

**Decision:** JSON-native profiles may use JSON Schema; graph-native profiles should publish SHACL shapes where useful.

### 3.13 Open Data Contract Standard (ODCS)

| Dimension | Assessment |
|---|---|
| Official scope | YAML data contracts covering schema, references, data quality, support, pricing, team, roles, SLA, infrastructure and custom properties. |
| Resource types | Operational data products, tables, streams and related infrastructure. |
| Semantics | Strong operational schema and ownership contract; domain semantic identifiers are not its sole focus. |
| Provenance | Ownership and operational metadata exist; not a substitute for PROV-O lineage. |
| Uncertainty / quality | Dedicated data-quality sections; no standard inferred-to-canonical semantic mapping lifecycle. |
| Policy | Operational responsibilities, support, pricing and SLA; not a full ODRL-equivalent usage policy model. |
| AI/model independence | Yes. |
| Reuse by ADUC | Data-product ownership, service levels, quality requirements and operational contracts. |
| Remaining gap | It governs producer-consumer expectations but does not standardize how independent AI models interpret ambiguous local concepts. |

**Decision:** ADUC should interoperate with data contracts and avoid duplicating operational ownership, SLA and infrastructure sections.

## 4. Capability coverage by composition

A realistic source can already be described through a composed stack:

```text
Source structure        → JSON Schema / OpenAPI / Croissant / ODCS
Semantic identifiers    → JSON-LD / RDF and domain vocabularies
Dataset discovery       → DCAT
Dataset loading         → Croissant
Events                   → CloudEvents
Observations             → SOSA / SSN
Provenance               → PROV-O
Quality                  → DQV
Usage policy             → ODRL
Graph validation         → SHACL
LLM access               → MCP
```

This composition is powerful enough to express the majority of the original ADUC Core categories. The remaining problem is that producers and AI consumers have no single, constrained agreement about:

- which subset of this stack is mandatory;
- where mappings are located;
- how mapping authority is represented;
- how confidence and evidence apply to a mapping;
- what a consumer must do with unknown or contested meaning;
- how compatibility is tested across model providers.

## 5. Precisely bounded gap

The matrix supports the following narrower problem statement:

> Existing standards can describe data structure, semantics, provenance, quality, policy, APIs, datasets and events, but no reviewed cross-resource profile was found that standardizes the epistemic lifecycle and consumer behavior of AI-oriented semantic mappings and proves that those mappings are interpreted compatibly by independent AI systems.

The key object under investigation is therefore not a new universal `resource`, `provenance`, `quality` or `policy` model. It is a **semantic mapping assertion** connecting a local source location to an existing semantic identifier, with explicit authority and evidence.

Conceptual example, not a frozen schema:

```json
{
  "localPath": "$.flow",
  "mapsTo": "https://example.org/concepts/WaterDischarge",
  "status": "inferred",
  "confidence": 0.91,
  "assertedBy": "urn:model:mapping-agent:1",
  "evidence": ["unit:m3/s", "documentation:river-flow"],
  "validFor": "source-schema-version-4"
}
```

A conforming consumer would need deterministic rules such as:

- never treat `inferred` as `canonical`;
- display or preserve unresolved ambiguity;
- reject or request review below a declared threshold for critical operations;
- retain the mapping's evidence and provenance;
- preserve the local term when no standard concept is confirmed;
- make no hidden provider-specific mapping during conformance tests.

## 6. Required project pivot

The initial repository name may remain a working title, but the technical direction must change from **inventing a universal data model** to evaluating an **AI Data Understanding Profile** over existing standards.

### ADUC should become

- a lightweight profile selecting and composing existing standards;
- a mapping-status and authority model;
- deterministic consumer rules;
- a conformance suite;
- authoring, review and validation tooling;
- a multi-model interoperability demonstration.

### ADUC should not become

- a replacement for Croissant datasets;
- a replacement for JSON-LD/RDF semantics;
- a replacement for PROV-O provenance;
- a replacement for DQV quality;
- a replacement for ODRL policy;
- a replacement for OpenAPI, CloudEvents or MCP;
- a universal ontology;
- a claim that every unknown source can be understood with certainty.

## 7. Gate 0 decision

**Result: conditional continuation with a narrowed scope.**

A distinct gap remains only if ADUC can prove all of the following:

1. a smaller implementation burden than directly composing the full standards stack;
2. lossless references to the underlying standards;
3. explicit separation of inferred and authoritative semantics;
4. deterministic behavior across independent consumers;
5. a reproducible multi-model test showing reduced provider-specific remapping.

If the next artifacts cannot demonstrate these properties, ADUC should stop defining a standard and become only an authoring/validation tool for Croissant, JSON-LD and related standards.

## 8. Official references

- JSON Schema Core, Draft 2020-12: https://json-schema.org/draft/2020-12/json-schema-core
- JSON Schema Validation, Draft 2020-12: https://json-schema.org/draft/2020-12/json-schema-validation
- JSON-LD 1.1: https://www.w3.org/TR/json-ld11/
- RDF 1.2 Concepts: https://www.w3.org/TR/rdf12-concepts/
- MLCommons Croissant 1.1: https://docs.mlcommons.org/croissant/docs/croissant-spec-1.1.html
- PROV-O: https://www.w3.org/TR/prov-o/
- DCAT 3: https://www.w3.org/TR/vocab-dcat-3/
- CloudEvents specification: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md
- MCP specification: https://modelcontextprotocol.io/specification/2025-11-25
- OpenAPI 3.2.0: https://spec.openapis.org/oas/v3.2.0.html
- Data Quality Vocabulary: https://www.w3.org/TR/vocab-dqv/
- ODRL Information Model 2.2: https://www.w3.org/TR/odrl-model/
- SOSA / SSN: https://www.w3.org/TR/vocab-ssn/
- SHACL 1.2 Core: https://www.w3.org/TR/shacl12-core/
- Open Data Contract Standard: https://bitol-io.github.io/open-data-contract-standard/latest/
