# Project Status

- Project: AI Data Understanding Core (working title)
- Current phase: Gate 6 — Multi-model conformance protocol
- Current release: unreleased
- Target release: `0.1.0-alpha.0`
- Overall status: JSON-LD/RDF interoperability passed; multi-model protocol work authorized

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
- ADR-0003 experimental JSON-LD namespace and offline context strategy
- Protected local context `urn:aduc:context:0.1`
- ADUC experimental term namespace `urn:aduc:term:`
- RDF representation reusing Dublin Core Terms, PROV-O, SKOS IRIs and XSD datatypes
- JSON-LD expansion, compaction and URDNA2015 N-Quads normalization tool
- Migration of all official profiles and fixtures from the placeholder context URI
- Six JSON-LD/RDF tests covering ten official profiles, graph evidence, ordering independence and offline context rejection
- GitHub Actions execution of 14 fixtures, 6 published profiles, 8 validator tests, 9 comparator tests and 6 JSON-LD/RDF tests

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
- Deterministic semantic comparison is possible using only shared targets, relations and authority states.
- Official profiles can be expanded and round-tripped as RDF without network access or graph loss.
- URN-based experimental identifiers avoid false ownership claims but are not yet dereferenceable public Web identifiers.

## Not yet validated

- Provider-neutral multi-model conformance package and result schema
- Actual runs against two independent AI consumers
- Public HTTPS namespace
- Public name and acronym
- Commercial model

## Active blockers

- Multi-model evaluation protocol and normalized result schema are not frozen
- No qualifying external model runs have been committed
- Authority verification mechanism is not defined
- Public namespace migration is deferred

## Rule

This file reports evidence, not optimism. Do not mark an item complete without a linked artifact or passing check.
