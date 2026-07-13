# Project Status

- Project: AI Data Understanding Core (working title)
- Current phase: Gate 2 — Machine-readable schema
- Current release: unreleased
- Target release: `0.1.0-alpha.0`
- Overall status: Gate 1 passed; schema implementation authorized

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
- Necessity analysis for document and assertion properties

## Evidence-based findings

- Existing standards collectively cover almost all categories proposed for the original ADUC Core.
- Croissant is the closest existing foundation for datasets and must not be duplicated.
- ADUC focuses on mapping status, authority, confidence/evidence, explicit relation, deterministic AI-consumer behavior and cross-model conformance.
- `unknown`, `verified` and `deprecated` are not required as mapping authority states in v0.1.
- The current broad bootstrap schema is not the accepted future normative model.

## Not yet validated

- Machine-readable mapping-profile schema
- JSON-LD context and RDF round-trip
- Semantic checks that JSON Schema cannot enforce
- Falsifiable multi-model demonstration protocol details
- Public name and acronym
- Commercial model

## Active blockers

- Gate 2 schema and official fixtures not implemented
- Authority verification mechanism not defined
- Demonstration fixtures and evaluation protocol not frozen

## Rule

This file reports evidence, not optimism. Do not mark an item complete without a linked artifact or passing check.
