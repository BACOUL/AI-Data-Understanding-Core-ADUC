# Changelog

All notable changes are documented here. The project follows Semantic Versioning after a public interface is defined. During `0.y.z`, breaking changes remain possible and must still be documented.

## Unreleased

### Project foundation

- Repository governance, contribution rules, ADR method, execution ledger, roadmap, CI, licenses, security policy and agent instructions.
- Prior-art matrix covering thirteen relevant standards and approaches.
- Official full-Core program, ten-block object model, complete example and strict construction order.
- English public website with GitHub Pages and Vercel static deployment.
- Adoption and value-validation plan requiring manual-versus-assisted and with-versus-without-ADUC evidence.

### Semantic mapping foundation

- Standalone semantic-mapping assertion model and compatibility schema.
- Valid and invalid fixtures, semantic validator, stable error catalogue and CLI reports.
- Authoring and review workflow with immutable publication history.
- Deterministic semantic comparator and two-source comparison examples.
- Protected local JSON-LD context, RDF representation, URDNA2015 normalization and offline round-trip tests.
- Provider-neutral multi-model conformance harness with explicitly non-qualifying illustrative runs.

### Accepted Core profiles, model and schema

- ADR-0005 — epistemic lifecycle: nine valid cases, eight invalid cases, deterministic evaluator.
- ADR-0006 — immutable source binding: three valid cases, ten invalid cases, seven tests.
- ADR-0007 — units and conversions: five valid cases, fifteen invalid cases, nine tests.
- ADR-0008 — temporal semantics: nine valid cases, fifteen invalid cases, seven tests.
- ADR-0009 — identity and safe equivalence: nine valid cases, seventeen invalid cases, nine tests.
- ADR-0010 — provenance and transformation lineage: seven valid cases, twenty invalid cases, eight tests.
- ADR-0011 — uncertainty and data quality: fourteen valid cases, twenty-four invalid cases, ten tests.
- ADR-0012 — general relation semantics: thirteen valid cases, twenty invalid cases, ten tests.
- ADR-0013 — policy and permitted-use conditions: twenty valid cases, thirty-two invalid cases, thirteen tests.
- ADR-0014 — normative Core object model: complete ten-block example, twenty-five invalid architecture mutations, module manifest and eleven tests.
- ADR-0015 — modular Core JSON Schema family: fourteen schemas, eleven valid contracts, fifteen invalid contracts, local validator and ten tests.

### ADR-0012 — General relation semantics

- Reused RDF, OWL, SKOS, PROV-O, Dublin Core Terms and explicit ADUC predicates.
- Kept vocabulary definitions, relation assertions and consumer inferences separate.
- Preserved endpoint binding, authority, evidence, provenance, scope, uncertainty, conflict and lifecycle.
- Blocked unauthorized inverse, transitive and causal inference.
- Kept `skos:closeMatch` distinct from equality and gated `owl:sameAs` through identity decisions.
- Applied open-world unknown behavior and explicit negative assertions.
- Added deterministic qualified JSON-LD/RDF export.

### ADR-0013 — Policy and permitted-use conditions

- Reused the W3C ODRL Information Model and Vocabulary.
- Bound policies to exact resource identity and SHA-256 version.
- Separated permissions, prohibitions and duties from recommendations, legal notices and classifications.
- Controlled actions, purposes, parties, recipients, places and environments.
- Kept `public` classification distinct from permission.
- Required bound evidence for pre-use duty satisfaction.
- Preserved open and closed modes and five safe outcomes.
- Required evidence for consent, ownership and legal-compliance claims.
- Explicitly excluded legal advice and access-control enforcement.

### ADR-0014 — Normative Core object model and boundaries

- Frozen ten top-level blocks and the minimum `aduc + resource + structure` envelope.
- Kept `relations` as the only repeated top-level module.
- Required absolute-IRI identifiers and deterministic `Ref` / `Refs` references.
- Assigned every normative fact to one owning module.
- Preserved qualification without conflating authority, confidence and measurement uncertainty.
- Defined an acyclic module dependency graph.
- Referenced external standards rather than copying them.
- Defined JSON authoring, JSON-LD projection, namespaced extensions, immutable publication and migration rules.
- Added a complete ten-block example with 38 addressable objects and twenty-five rejected architecture mutations.

### ADR-0015 — Modular Core JSON Schema family

- Replaced the historical Core bootstrap with the official experimental Draft 2020-12 root and envelope.
- Added module schemas for resource, structure, semantics, identity, context, provenance, uncertainty, relations and policy.
- Added shared metadata, qualification and extension schemas.
- Required `structure.records` according to the frozen object model.
- Closed Core objects and confined extension payloads to declared external namespaces.
- Enforced absolute IRIs, lowercase SHA-256 digests, controlled enums and qualification dependencies.
- Enforced exclusive relation endpoint forms and non-executable descriptive policy rules.
- Required provenance when policy is present.
- Added eleven complete valid contracts and fifteen intentionally invalid contracts.
- Added `tools/aduc_core_validate.py` with local schema resolution, stable JSON paths and complementary architecture checks.
- Added ten schema, fixture, CLI and orchestration tests.

### Changed

- Required measurable user value, review cost, confidence calibration and controlled baselines before compiler or interoperability success claims.
- Required exact source, execution, predicate, policy-target, party, purpose, Core-object and evidence binding.
- Blocked silent assumptions about uncertainty, identity, time, provenance, relations, permissions or authority.
- Expanded CI through Core-model and modular-schema checks.
- Advanced the single active task to the unified full-Core validator and deterministic comparator.
