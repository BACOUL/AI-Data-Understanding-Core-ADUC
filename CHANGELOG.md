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

### Changed

- Narrowed the candidate project direction from a standalone universal data model to an AI semantic mapping profile that reuses established standards
- Made mapping authority, confidence/evidence, deterministic consumer behavior and multi-model conformance the candidate differentiators requiring validation
- Marked the broad bootstrap schema as historical and removed it from active fixture validation
- Reduced v0.1 authority states to `inferred`, `reviewed`, `canonical` and `contested`
- Required explicit mapping relation and method-bound confidence for inferred mappings
- Bound active profiles to an identified source plus a version or SHA-256 digest
- Updated CI to install explicit format-checking dependencies so URI validation is reproducible
- Expanded CI to execute semantic-validator and comparator unit tests
- Updated the README with authoring, validation and comparison commands
- Required unmapped fields to be represented through separate coverage reporting rather than targetless assertions
- Extended published-example validation to comparison profiles
