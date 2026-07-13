# Project Status

- Project: AI Data Understanding Core (working title)
- Current phase: Gate 5 — Semantic comparison
- Current release: unreleased
- Target release: `0.1.0-alpha.0`
- Overall status: Gate 4 passed; semantic-comparison work authorized

## Completed

- Initial repository operating structure
- Initial project charter
- Initial non-goals
- Initial execution method
- Prior-art matrix covering structure, semantics, datasets, APIs, events, provenance, quality, policy, observations, validation and operational data contracts
- ADR-0002 accepting ADUC as an AI semantic mapping and conformance profile over established standards
- v0.1 boundary limited to semantic mappings for JSON and CSV datasets
- Falsifiable initial interoperability promise and explicit stop/pivot conditions
- Minimal semantic mapping assertion model
- Reduced status model: `inferred`, `reviewed`, `canonical`, `contested`
- Immutable assertion lifecycle and deterministic consumer invariants
- Candidate Draft 2020-12 semantic mapping profile schema
- Four valid and ten invalid official schema fixtures
- GitHub Actions validation of all 14 official mapping-profile fixtures
- User-facing text and JSON validator
- Stable validation error catalogue
- Semantic checks for duplicate IDs, self-replacement, replacement cycles and canonical conflicts
- Local trusted-authority warnings for canonical mappings
- Eight validator unit tests including CLI exit codes
- GitHub Actions execution of schema fixtures and all eight validator tests
- Manual authoring and review workflow
- Separation of portable profiles from authoring-state and coverage records
- Role definitions for curator, inference producer, reviewer, source authority and consumer
- Two end-to-end authoring examples covering reviewed and canonical publication
- Four published authoring profiles validated in GitHub Actions

## Evidence-based findings

- Existing standards collectively cover almost all categories proposed for the original ADUC Core.
- Croissant is the closest existing foundation for datasets and must not be duplicated.
- ADUC focuses on mapping status, authority, confidence/evidence, explicit relation, deterministic AI-consumer behavior and cross-model conformance.
- `unknown`, `verified` and `deprecated` are not required as mapping authority states in v0.1.
- JSON Schema can enforce conditional field rules but cannot prove publisher authority, target equivalence or cross-document trust.
- A local trust option can suppress an authority warning but does not constitute cryptographic or global proof.
- Unmapped fields belong in a coverage report rather than targetless portable assertions.
- Authoring history is useful operational evidence but must remain separate from the minimal portable profile.

## Not yet validated

- Deterministic comparison of two semantic mapping profiles
- JSON-LD context and RDF round-trip
- Falsifiable multi-model demonstration protocol details
- Public name and acronym
- Commercial model

## Active blockers

- Comparison protocol and reference comparator not implemented
- Authority verification mechanism not defined
- Demonstration fixtures and evaluation protocol not frozen

## Rule

This file reports evidence, not optimism. Do not mark an item complete without a linked artifact or passing check.
