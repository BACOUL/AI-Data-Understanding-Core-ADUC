# Project Status

- Project: AI Data Understanding Core (working title)
- Current phase: Gate 6 preparation — JSON-LD and RDF interoperability
- Current release: unreleased
- Target release: `0.1.0-alpha.0`
- Overall status: Gate 5 implemented; independent CI evidence pending merge

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
- Manual authoring and review workflow
- Two end-to-end authoring examples covering reviewed and canonical publication
- Deterministic semantic comparison protocol
- Reference profile comparator with text and JSON reports
- Nine comparator tests covering exact, inferred, non-exact, contested, unmatched and deterministic-output behavior
- French and US source examples with differently named fields mapped to one semantic target
- Explicit `notEvaluated` reporting for missing unit, time and entity information

## Evidence-based findings

- Existing standards collectively cover almost all categories proposed for the original ADUC Core.
- Croissant is the closest existing foundation for datasets and must not be duplicated.
- ADUC focuses on mapping status, authority, confidence/evidence, explicit relation, deterministic AI-consumer behavior and cross-model conformance.
- `unknown`, `verified` and `deprecated` are not required as mapping authority states in v0.1.
- JSON Schema can enforce conditional field rules but cannot prove publisher authority, target equivalence or cross-document trust.
- A local trust option can suppress an authority warning but does not constitute cryptographic or global proof.
- Unmapped fields belong in a coverage report rather than targetless portable assertions.
- Comparable semantics do not by themselves establish unit conversion, temporal alignment or entity identity.
- Same-looking field names are insufficient when their published semantic targets differ.

## Not yet validated

- GitHub Actions result for comparator tests and comparison examples
- JSON-LD context and RDF round-trip
- Stable experimental namespace
- Falsifiable multi-model demonstration protocol details
- Public name and acronym
- Commercial model

## Active blockers

- Gate 5 PR and combined CI not yet merged
- JSON-LD context is still a placeholder URI
- RDF representation and round-trip tests are not defined
- Authority verification mechanism is not defined
- Multi-model evaluation protocol is not frozen

## Rule

This file reports evidence, not optimism. Do not mark an item complete without a linked artifact or passing check.
