# Changelog

All notable changes are documented here. The project follows Semantic Versioning after a public interface is defined. During `0.y.z`, breaking changes remain possible and must still be documented.

## Unreleased

### Project foundation

- Repository governance, contribution rules, ADR method, execution ledger, roadmap, CI, licenses, security policy and agent instructions.
- Prior-art matrix covering thirteen relevant standards and approaches.
- Official full-Core program, ten-block working draft, complete object-model example and strict construction order.
- English public website with GitHub Pages and Vercel static deployment.
- Adoption and value-validation plan requiring manual-versus-assisted and with-versus-without-ADUC evidence.

### Semantic mapping foundation

- Semantic-mapping assertion model and experimental Draft 2020-12 bootstrap schema.
- Valid and invalid fixtures, semantic validator, stable error catalogue, trusted-authority handling and CLI reports.
- Authoring and review workflow with immutable publication history.
- Deterministic semantic comparator and two-source comparison examples.
- Protected local JSON-LD context, RDF representation, URDNA2015 normalization and offline round-trip tests.
- Provider-neutral multi-model conformance harness with frozen package and explicitly non-qualifying illustrative runs.

### Accepted Core profiles and model

- ADR-0005 — epistemic lifecycle: nine valid cases, eight invalid cases, deterministic evaluator.
- ADR-0006 — immutable source binding: three valid cases, ten invalid cases, seven tests.
- ADR-0007 — units and conversions: five valid cases, fifteen invalid cases, nine tests.
- ADR-0008 — temporal semantics: nine valid cases, fifteen invalid cases, seven tests.
- ADR-0009 — identity and safe equivalence: nine valid cases, seventeen invalid cases, nine tests.
- ADR-0010 — provenance and transformation lineage: seven valid cases, twenty invalid cases, eight tests.
- ADR-0011 — uncertainty and data quality: fourteen valid cases, twenty-four invalid cases, ten tests.
- ADR-0012 — general relation semantics: thirteen valid cases, twenty invalid cases, ten tests.
- ADR-0013 — policy and permitted-use conditions: twenty valid cases, thirty-two invalid cases, thirteen tests.
- ADR-0014 — normative Core object model: complete ten-block example, twenty-five invalid architecture mutations, machine-readable module manifest and eleven tests.

### ADR-0012 — General relation semantics

- Pinned predicate profile reusing RDF, OWL, SKOS, PROV-O, Dublin Core Terms and explicit ADUC experimental predicates.
- Separate vocabulary definitions, relation assertions and consumer inferences.
- Bound resource and literal endpoints with authority, evidence, provenance, temporal/contextual scope, uncertainty, conflict and lifecycle.
- Authorized inverse, symmetry and transitive-closure behavior only.
- `skos:closeMatch` kept distinct from exact equality.
- `skos:broader` closure emits `skos:broaderTransitive`, not a fabricated direct broader assertion.
- Strict `owl:sameAs` identity-profile gate.
- Open-world unknown behavior and explicit negative assertions.
- Causal inference blocked for correlation, dependency and temporal order.
- Functional, inverse-functional, disjoint-predicate, positive/negative and acyclic-graph conflict checks.
- Deterministic qualified JSON-LD/RDF export.

### ADR-0013 — Policy and permitted-use conditions

- Pinned policy profile reusing the W3C ODRL Information Model and Vocabulary.
- Exact policy-target identity and SHA-256 version binding.
- Separate executable permissions, prohibitions and duties from recommendations, legal notices and descriptive classifications.
- Controlled absolute identifiers for actions, purposes, requesters, recipients, places and environments.
- `public` classification kept distinct from permission.
- Free-text purpose matching blocked.
- Deterministic prohibition-overrides behavior for the offline reference subset.
- Pre-use duties require bound satisfaction evidence; post-use duties remain visible.
- Explicit open and closed policy modes.
- Five safe outcomes: `permit`, `deny`, `notApplicable`, `indeterminate` and `requiresHumanReview`.
- Inferred, partial, redacted, externally governed, contested and deprecated policy blocks automatic reliance.
- Consent, ownership and legal-compliance claims require typed evidence and provenance.
- Resolved inheritance requires bound composition evidence.
- Deterministic qualified JSON-LD/RDF export.
- Explicit boundary: ADUC does not provide legal advice, grant access or replace enforcement.

### ADR-0014 — Normative Core object model and boundaries

- Frozen ten-block top-level envelope and canonical order.
- Required minimum `aduc + resource + structure`.
- Singular module objects with `relations` as the only repeated top-level array.
- Absolute-IRI identifiers for every addressable object.
- Deterministic `Ref` and `Refs` cross-module references.
- One owning module for each normative fact and explicit duplicate-fact conflicts.
- Shared assertion qualification without conflating authority, confidence and measurement uncertainty.
- Machine-readable acyclic module dependency graph and planned schema-family manifest.
- External standards referenced rather than copied into competing ADUC structures.
- Ordinary JSON as canonical authoring and JSON-LD as deterministic projection.
- Declared namespaced extensions with collision prevention and safe unsupported-extension behavior.
- Immutable publication, explicit replacement and compatibility rules.
- Migration mapping from the existing semantic-mapping profile.
- Complete ten-block example with 38 addressable objects and fully resolved internal references.
- Twenty-five invalid architecture mutations covering envelope, cardinality, identifiers, references, ownership, external-standard boundaries, authority, identity, relations, policy, extensions, dependencies and history.
- Explicit distinction between the existing bootstrap schema and the future official modular Core schema family.

### Changed

- Reused established standards rather than creating competing structure, unit, time, identity, provenance, uncertainty, quality, relation or policy vocabularies.
- Required measurable user value, review cost, confidence calibration and controlled baselines before compiler or interoperability success claims.
- Required exact source, execution, predicate, policy-target, party, purpose, Core-object and evidence binding instead of mutable locations, local labels or model names.
- Blocked silent assumptions about uncertainty, independence, exactness, identity, time, provenance, relation inverse, transitivity, causality, permission, duty satisfaction, consent, ownership or authority.
- Removed fabricated confidence defaults for inferred relation assertions and blocked authoritative positive/negative contradictions.
- Expanded CI through policy and Core-model architecture checks.
- Advanced the single active task from Core-model definition to the official modular JSON Schema family.