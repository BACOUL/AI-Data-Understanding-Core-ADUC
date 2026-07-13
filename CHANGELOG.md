# Changelog

All notable changes are documented here. The project follows Semantic Versioning after a public interface is defined. During `0.y.z`, breaking changes remain possible and must still be documented.

## Unreleased

### Project foundation

- Repository governance, contribution rules, ADR method, execution ledger, roadmap, CI, licenses, security policy, and agent instructions.
- Prior-art matrix covering thirteen relevant standards and approaches.
- Official full-Core program, ten-block working draft, first informative complete example, and strict construction order.
- English public website with GitHub Pages and Vercel static deployment.
- Adoption and value-validation plan requiring manual-versus-assisted and with-versus-without-ADUC evidence.

### Semantic mapping foundation

- Semantic-mapping assertion model and experimental Draft 2020-12 schema.
- Valid and invalid fixtures, semantic validator, stable error catalogue, trusted-authority handling, and CLI reports.
- Authoring and review workflow with immutable publication history.
- Deterministic semantic comparator and two-source comparison examples.
- Protected local JSON-LD context, RDF representation, URDNA2015 normalization, and offline round-trip tests.
- Provider-neutral multi-model conformance harness with frozen package and explicitly non-qualifying illustrative runs.

### Accepted Core profiles

- ADR-0005 — epistemic lifecycle: nine valid cases, eight invalid cases, deterministic evaluator.
- ADR-0006 — immutable source binding: three valid cases, ten invalid cases, seven tests.
- ADR-0007 — units and conversions: five valid cases, fifteen invalid cases, nine tests.
- ADR-0008 — temporal semantics: nine valid cases, fifteen invalid cases, seven tests.
- ADR-0009 — identity and safe equivalence: nine valid cases, seventeen invalid cases, nine tests.
- ADR-0010 — provenance and transformation lineage: seven valid cases, twenty invalid cases, eight tests.
- ADR-0011 — uncertainty and data quality: fourteen valid cases, twenty-four invalid cases, ten tests.
- ADR-0012 — general relation semantics: thirteen valid cases, twenty invalid cases, ten tests.

### ADR-0012 — General relation semantics

- Pinned predicate profile reusing RDF, OWL, SKOS, PROV-O, Dublin Core Terms, and explicit ADUC experimental predicates.
- Separate vocabulary definitions, relation assertions, and consumer inferences.
- Bound resource and literal endpoints with authority, evidence, provenance, temporal/contextual scope, uncertainty, conflict, and lifecycle.
- Authorized inverse, symmetry, and transitive-closure behavior only.
- `skos:closeMatch` kept distinct from exact equality.
- `skos:broader` closure emits `skos:broaderTransitive`, not a fabricated direct broader assertion.
- Strict `owl:sameAs` identity-profile gate.
- Open-world unknown behavior and explicit negative assertions.
- Causal inference blocked for correlation, dependency, and temporal order.
- Functional, inverse-functional, disjoint-predicate, and acyclic-graph conflict checks.
- Deterministic qualified JSON-LD/RDF export.

### Changed

- Reused established standards rather than creating competing structure, unit, time, identity, provenance, uncertainty, quality, or relation vocabularies.
- Required measurable user value, review cost, confidence calibration, and controlled baselines before compiler or interoperability success claims.
- Required exact source, execution, predicate, and evidence binding instead of mutable locations, local labels, or model names.
- Blocked silent assumptions about uncertainty, independence, exactness, identity, time, provenance, relation inverse, transitivity, causality, or authority.
- Expanded CI through general-relation checks.
- Advanced the single active task from general relations to policy and permitted-use conditions.
