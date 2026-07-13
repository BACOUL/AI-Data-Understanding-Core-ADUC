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

### ADR-0005 — Epistemic lifecycle

- Separate representations for unknown coverage, assertion authority, conflict, and deprecation.
- Effective states: `unknown`, `inferred`, `reviewed`, `verified`, `canonical`, `contested`, and `deprecated`.
- Nine valid lifecycle cases, eight invalid counterexamples, deterministic evaluator, and tests.

### ADR-0006 — Source description and immutable binding

- Exact resource, descriptor, version, SHA-256, and local-field binding.
- Croissant, JSON Schema, OpenAPI, and DCAT remain authoritative for their structures.
- JSON, CSV, and embedded OpenAPI examples; three valid and ten invalid cases; deterministic evaluator and seven tests.

### ADR-0007 — Units and conversions

- Quantity kind, dimension, quantity role, global unit identity, local aliases, conversion, rounding, uncertainty, and provenance.
- Pinned QUDT/UCUM-derived reference subset and exact decimal/rational conversion.
- Five valid and fifteen invalid cases, nine tests, including `89 °C = 192.2 °F`.

### ADR-0008 — Temporal semantics

- Fixed instants, local civil time, timezone evidence, roles, intervals, precision, uncertainty, exact durations, and calendar periods.
- Pinned IANA TZDB reference evidence.
- Nine valid and fifteen invalid cases, seven tests, including Paris local-time alignment and DST ambiguity detection.

### ADR-0009 — Entity identity and safe equivalence

- Separate entity, identifier, label, relation assertion, and merge decision.
- Namespace-qualified local identity, protected identifiers, temporal validity, conflict, privacy, and strict `owl:sameAs` gates.
- Nine valid and seventeen invalid cases, nine tests.

### ADR-0010 — Provenance and transformation lineage

- PROV-O-based entities, activities, agents, derivations, invalidations, disclosure, and reproducibility.
- Bound inputs and outputs, software/model versions, environments, parameters, prompts, tools, seeds, and manual interventions.
- Seven valid provenance cases, twenty invalid mutations, eight tests, and one end-to-end source-to-comparison chain.

### ADR-0011 — Uncertainty and data quality

- Separate measurement uncertainty, semantic confidence, model probability, DQV-compatible data quality, and epistemic authority.
- Standard, expanded, relative, asymmetric, interval, distributional, categorical, and unknown uncertainty.
- Missingness, censoring, exactness, calibration, dependence, affine conversion, deterministic propagation, and quality disclosure.
- Fourteen valid reference cases, twenty-four invalid mutations, deterministic evaluator, and ten tests.
- Reference results:

```text
0.5 °C standard uncertainty -> 0.9 °F
3 and 4 independent standard uncertainties -> 5
0.03 and 0.04 independent relative uncertainties -> 0.05
resolution 0.1 rectangular contribution -> 0.028867513459481
```

### Changed

- Narrowed the implemented differentiator to portable semantic mappings and deterministic consumer behavior while preserving the maintainer-approved full-Core program.
- Required measurable user value, review cost, confidence calibration, and controlled baselines before compiler or interoperability success claims.
- Reused established standards rather than creating competing structure, unit, time, identity, provenance, uncertainty, or quality vocabularies.
- Required exact source and execution evidence instead of mutable locations, labels, or model names.
- Blocked silent assumptions about uncertainty, independence, exactness, identity, time, provenance, or authority.
- Expanded CI through uncertainty and quality checks.
- Advanced the single active task from uncertainty and data quality to general relation semantics.
