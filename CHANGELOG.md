# Changelog

All notable changes to this experimental project are recorded here.

The format follows Keep a Changelog loosely. This project is not yet a recognized standard.

## Unreleased

### Added

- Public website redesign aligned with the completed Core model, schema family, unified validator, deterministic comparator and cross-cutting Master Plan.
- Dedicated public pages for Why ADUC, Core, Validate, Compare, Trust and Conformance evidence.
- Website source-of-truth data file for repeated public metrics, canonical URL, active task and implementation status.
- Website tests for canonical definition, real commands, ten Core blocks, obsolete-claim prevention, sitemap/canonical coherence, broken internal links and old invalid JSON syntax.
- Prior-art matrix covering thirteen relevant standards and approaches.
- Official full-Core program, ten-block object model, complete example and strict construction order.
- English public website with GitHub Pages and Vercel static deployment.
- Seven-state epistemic lifecycle with deterministic evaluator.
- Source description and immutable source-binding profile.
- Unit identifier, dimensional compatibility and deterministic conversion profile.
- Temporal semantics, timezone evidence and deterministic alignment profile.
- Entity identity, issuer authority and safe equivalence profile.
- Provenance, transformation lineage, disclosure and reproducibility profile.
- Uncertainty, missingness, propagation and data-quality profile.
- General relation semantics and deterministic graph behavior profile.
- Policy and permitted-use profile with deterministic safe outcomes.
- Normative ten-block Core object model, module manifest and architecture checker.
- Official modular Draft 2020-12 Core JSON Schema family and local schema-plus-architecture validator.
- Unified full-Core validator and deterministic comparator with stable JSON/text reports.
- ADR-0018 deterministic complete-contract formatter with strict JSON parsing, exact-decimal preservation, frozen Core ordering, unchanged array order, atomic output, stable reports and byte idempotence.

### Evidence

- Semantic mapping profile: 4 valid fixtures, 10 invalid fixtures, 8 validator tests and 9 comparator tests.
- JSON-LD/RDF projection: 6 deterministic round-trip tests.
- Provider-neutral conformance harness: 6 scenarios and 9 tests, with illustrative non-qualifying runs.
- Epistemic lifecycle: 9 valid cases, 8 invalid cases and 7 tests.
- Source binding: 3 valid cases, 10 invalid cases and 7 tests.
- Units: 5 valid cases, 15 invalid cases and 9 tests.
- Time: 9 valid cases, 15 invalid cases and 7 tests.
- Identity: 9 valid cases, 17 invalid cases and 9 tests.
- Provenance: 7 valid cases, 20 invalid cases and 8 tests.
- Uncertainty and data quality: fourteen valid cases, twenty-four invalid cases, ten tests.
- General relations: thirteen valid cases, twenty invalid cases, ten tests.
- Policy: twenty valid cases, thirty-two invalid cases, thirteen tests.
- ADR-0018 - deterministic complete-contract formatting: valid, review-required and rejected fixtures; exact-decimal and Unicode preservation; duplicate-key, path-collision and overwrite-race regressions; 13 focused tests.
- ADR-0017 - deterministic semantic-profile migration: explicit manifest, conservative mappings, stable reports, complete Core revalidation and 19 focused tests.
- ADR-0016 - unified Core validation and comparison: 24 official comparison scenarios, evaluator-adapter orchestration, separated change type and semantic assessments, dangerous-index blocking, iterative JSON-depth protection, 15 validator tests and 13 comparator tests.
- ADR-0014 — normative Core object model: complete ten-block example, twenty-five invalid architecture mutations, module manifest and eleven tests.
- ADR-0015 — modular Core JSON Schema family: fourteen schemas, eleven valid contracts, fifteen invalid contracts, local validator and thirteen tests.

### Changed

- README and roadmap now reflect the implemented validator, comparator, migration and deterministic formatter, with the provider-neutral conformance runner as the single next engine task. Website redesign remains isolated in PR #63.
- Public website navigation, visual hierarchy, code examples, SEO metadata, sitemap, robots file and structured data now use the GitHub Pages canonical base already declared by the repository.
- Root Vercel configuration now publishes the static website from `website/`.

### Not yet done

- Provider-neutral full-Core conformance runner.
- TypeScript and Python SDKs.
- JSON/CSV compiler and review UI.
- MCP adapter, registry service, extensions and anticipation engine.
- Qualifying external multi-model interoperability proof.
- Value benchmark and adoption evidence.

## 2026-07-14

### ADR-0016 - Unified Core validation and comparison

- Added `tools/aduc_core.py` with `validate` and `compare` commands.
- Added stable validation and comparison JSON reports with deterministic diagnostics, summaries and exit codes.
- Added `spec/ADUC_CORE_VALIDATION_0_1.md`, `spec/ADUC_CORE_COMPARISON_0_1.md`, `docs/architecture/CORE_VALIDATION_PIPELINE_0_1.md` and `docs/errors/CORE_ERROR_CATALOGUE_0_1.md`.
- Added 24 official comparison scenarios in `examples/core/comparison/cases.json`.
- Added `tests/core_validator/` and `tests/core_comparator/`.
- Corrected independent-audit P1 findings: the unified validator now calls accepted ADR-0005 through ADR-0013 evaluator functions where applicable, reports non-evaluable profile rules explicitly, separates comparator `changeType` from normative `assessment`, blocks dangerous architecture diagnostics before indexing, and rejects excessively deep JSON without traceback.

### ADR-0015 — Modular Core JSON Schema family

- Replaced the historical Core bootstrap with the official experimental Draft 2020-12 root and envelope.
- Added module schemas for resource, structure, semantics, identity, context, provenance, uncertainty, relations and policy.
- Added reusable metadata, qualification and extension schemas.
- Added 11 valid complete Core contracts and 15 invalid complete Core contracts.
- Added `tools/aduc_core_validate.py`, combining JSON Schema validation with the ADR-0014 architecture checker.
- Added schema tests for local refs, offline operation, fixture behavior, closed objects, architecture complementarity and stable JSON error paths.
- Added CI execution for the Core schema suite and the complete ten-block model.

### ADR-0014 — Normative Core object model

- Added the accepted ten-block Core model and machine-readable module manifest.
- Added the complete ten-block example and 25 invalid architectural counterexamples.
- Added `tools/aduc_core_model.py` and Core model tests.

## 2026-07-13

### Initial public foundation

- Repository structure, governance, license and CI.
- Prior-art and standards boundary.
- Semantic mapping profile, validator, comparator and JSON-LD/RDF projection.
- Provider-neutral conformance harness foundation.
- Public website, roadmap and project status files.
