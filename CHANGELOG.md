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

### Changed

- Narrowed the candidate project direction from a standalone universal data model to an AI semantic mapping profile that reuses established standards
- Made mapping authority, confidence/evidence, deterministic consumer behavior and multi-model conformance the candidate differentiators requiring validation
- Marked the broad bootstrap schema as non-normative and subject to replacement during Gate 2
- Reduced v0.1 authority states to `inferred`, `reviewed`, `canonical` and `contested`
- Required explicit mapping relation and method-bound confidence for inferred mappings
