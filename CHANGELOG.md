# Changelog

All notable changes will be documented here.

The project follows Semantic Versioning after a public interface is defined. During `0.y.z`, breaking changes remain possible and must still be documented.

## Unreleased

### Added

- Initial repository operating structure
- Bootstrap specification skeleton
- Bootstrap JSON Schema
- Example fixtures and validation workflow
- Gate 0 prior-art matrix covering thirteen relevant standards and approaches
- ADR-0002 defining ADUC as an AI semantic mapping and conformance profile
- Explicit v0.1 resource boundary, falsifiable promise and stop/pivot conditions
- Gate 1 semantic mapping assertion model with necessity analysis, examples and unsafe counterexamples
- Immutable assertion lifecycle and deterministic consumer invariants
- Candidate semantic mapping profile JSON Schema based on Draft 2020-12
- Four valid and ten invalid official mapping-profile fixtures
- Active fixture validator and documented schema limitations
- Reproducible development dependency file including JSON Schema format validation support
- User-facing semantic validator with text and JSON conformance reports
- Stable Gate 3 validation error catalogue and exit-code contract
- Semantic checks for duplicate assertion identifiers, self-superseding assertions, supersedes cycles and canonical conflicts
- Local trusted-authority option with explicit unverified-authority warnings
- Eight semantic-validator unit tests including CLI behavior
- Manual authoring and review workflow with role separation and immutable publication steps
- Separate authoring-state coverage and event ledgers
- River example progressing from inferred to reviewed mapping
- Machine example progressing from inferred to publisher-canonical mapping
- CI discovery of published authoring profile examples
- Gate 5 deterministic semantic comparison protocol
- Reference text/JSON profile comparator
- Nine comparator tests covering exact, inferred, non-exact, contested, unmatched and deterministic-output behavior
- French and US comparison examples with differently named fields sharing a semantic target
- Explicit `notEvaluated` output for unit, time and entity dimensions
- ADR-0003 defining the experimental JSON-LD namespace and offline context strategy
- Protected local JSON-LD context identified by `urn:aduc:context:0.1`
- Experimental ADUC RDF term namespace `urn:aduc:term:`
- RDF representation specification reusing Dublin Core Terms, PROV-O, SKOS IRIs and XSD datatypes
- JSON-LD expansion, compaction and URDNA2015 normalization CLI
- Six JSON-LD/RDF tests covering ten official profiles and deterministic round-trip behavior
- Stable JSON-LD processing error codes
- Provider-neutral multi-model conformance protocol and frozen package
- Normalized model-result schema and deterministic conformance evaluator
- Official full-Core working draft `spec/ADUC_CORE_SPEC_0_1.md`
- Official project structure and master roadmap
- ADR-0004 positioning the existing semantic-mapping implementation inside the broader ADUC Core
- First informative ten-block full-Core JSON example
- English static public website with Home, Specification, Architecture, Roadmap, Example and Try in 5 Minutes pages
- GitHub Pages deployment workflow
- Website metadata, robots policy and XML sitemap
- Deterministic website and full-Core example validation script
- ADR-0005 defining the complete seven-state effective epistemic lifecycle
- `spec/EPISTEMIC_STATUS_MODEL_0_1.md` with authority, conflict, lifecycle, confidence, evidence, and migration rules
- Separate coverage, semantic assertion, challenge, resolution, and deprecation record families
- Reference epistemic evaluator `tools/aduc_epistemic.py`
- Nine valid lifecycle cases covering all seven effective states
- Eight rejected lifecycle counterexamples
- Epistemic lifecycle unit and CLI tests
- Official `docs/roadmap/ADOPTION_AND_VALUE_VALIDATION.md` cross-cutting plan
- Four inference evidence modes: structure-only, sample-assisted, documentation-assisted, and publisher-assisted
- Review-tax measurement model and provisional alpha targets
- Manual mapping versus `infer + review` benchmark requirements
- Controlled with-ADUC versus without-ADUC multi-model protocol requirements
- Confidence-calibration rules prohibiting uncalibrated model self-confidence from being presented as probability
- MCP integration boundary defining it as an optional future adapter
- Roadmap tests enforcing adoption-plan discoverability
- ADR-0006 defining source description and immutable source binding
- `spec/SOURCE_DESCRIPTION_PROFILE_0_1.md` covering content, description, and combined bindings
- SHA-256 raw-byte binding and RFC 8785 embedded-JSON canonicalization scope
- Explicit Croissant, JSON Schema, OpenAPI, DCAT, custom-profile, JSON Pointer, CSV-header, and operation-reference behavior
- JSON, CSV, and embedded OpenAPI source-binding examples
- Three valid and ten invalid source-binding cases
- Reference source-binding evaluator `tools/aduc_source_binding.py`
- Seven source-binding unit and CLI tests
- Stable source-binding error families for digest, identity, availability, reference, dialect, and structural-conflict failures

### Changed

- Narrowed the initial implementation direction from a standalone universal data model to a semantic mapping profile that reuses established standards
- Subsequently clarified through ADR-0004 that the semantic mapping profile is the first implemented subset of the maintainer-approved full ADUC Core program
- Made mapping authority, confidence/evidence, deterministic consumer behavior and multi-model conformance implemented differentiators requiring validation
- Marked the broad bootstrap schema as historical and removed it from active fixture validation
- Reduced the implemented mapping-profile authority states to `inferred`, `reviewed`, `canonical` and `contested`
- Required explicit mapping relation and method-bound confidence for inferred mappings
- Bound active profiles to an identified source plus a version or SHA-256 digest
- Updated CI to install explicit format-checking and JSON-LD dependencies
- Expanded CI to execute semantic-validator, comparator, JSON-LD/RDF, conformance, epistemic-lifecycle, source-binding, roadmap, and website checks
- Updated the README to distinguish the full-Core mission from the implemented semantic-mapping subset
- Required unmapped fields to be represented through separate coverage reporting rather than targetless assertions
- Extended published-example validation to comparison profiles
- Migrated official mapping profiles and fixtures from the placeholder `example.org` context to the pinned experimental context
- Replaced the obsolete Gate 6 next action with the full epistemic-lifecycle decision required before the full-Core schema
- Replaced the proposed one-property seven-state model with separate authority, conflict, deprecation, and unknown-coverage representations
- Defined `reviewed`, `verified`, and `canonical` as distinct claims with different evidence and consumer rules
- Required legacy `status=contested` migration to recover its underlying authority level instead of guessing it
- Made measurable user value, review cost, confidence calibration, and controlled baseline comparison mandatory before compiler or interoperability success claims
- Required exact resource and description integrity rather than relying on mutable locations or version labels
- Kept Croissant, JSON Schema, OpenAPI, and DCAT authoritative for their structural models instead of copying them into ADUC
- Advanced the single active task from source binding to unit identifiers, dimensional compatibility, and conversions
