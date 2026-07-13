# Project Status

- Project: AI Data Understanding Core (working title)
- Current phase: Gate 3 — Reference validator
- Current release: unreleased
- Target release: `0.1.0-alpha.0`
- Overall status: Gate 2 implemented; independent CI evidence pending merge

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
- Reference fixture runner validating the active mapping-profile schema
- Documented boundary between structural schema conformance and semantic/trust validation

## Evidence-based findings

- Existing standards collectively cover almost all categories proposed for the original ADUC Core.
- Croissant is the closest existing foundation for datasets and must not be duplicated.
- ADUC focuses on mapping status, authority, confidence/evidence, explicit relation, deterministic AI-consumer behavior and cross-model conformance.
- `unknown`, `verified` and `deprecated` are not required as mapping authority states in v0.1.
- JSON Schema can enforce conditional field rules but cannot prove publisher authority, target equivalence or cross-document trust.

## Not yet validated

- GitHub Actions result for the active mapping-profile fixtures
- User-facing semantic validator and stable error catalogue
- JSON-LD context and RDF round-trip
- Falsifiable multi-model demonstration protocol details
- Public name and acronym
- Commercial model

## Active blockers

- Gate 2 PR and CI not yet merged
- Semantic validation rules not implemented
- Authority verification mechanism not defined
- Demonstration fixtures and evaluation protocol not frozen

## Rule

This file reports evidence, not optimism. Do not mark an item complete without a linked artifact or passing check.
