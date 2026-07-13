# Next Action

## Single active task

Define and accept the ADUC source-description and source-binding model before implementing the full-Core JSON Schema.

Create:

```text
docs/decisions/ADR-0006-source-description-and-binding.md
spec/SOURCE_DESCRIPTION_PROFILE_0_1.md
examples/source-description/
```

## Objective

Define exactly how a full-Core ADUC contract identifies the resource it describes, binds itself to an immutable source or schema version, and references local fields without duplicating established dataset, API, and schema standards.

## Cross-cutting adoption constraint

The official [`ADOPTION_AND_VALUE_VALIDATION.md`](ADOPTION_AND_VALUE_VALIDATION.md) plan applies to later compiler, review, and interoperability work.

This source-binding task remains first because no reliable inference benchmark or with/without ADUC test is valid unless every contract and evidence item is bound to the exact source, schema version, field, and documentation used.

Do not implement the JSON/CSV compiler now. The future compiler must eventually declare its inference evidence mode, method version, evidence references, and source binding.

## Required decisions

1. which existing descriptions ADUC may reference, including Croissant, JSON Schema, OpenAPI, DCAT, and versioned custom descriptions;
2. the minimum `resource`, `structure`, and `validFor` information required in the Core envelope;
3. whether source descriptions are embedded, linked, or both;
4. how a contract binds to a source version, immutable identifier, or SHA-256 digest;
5. supported local-reference schemes for JSON and CSV v0.1;
6. how consumers detect stale contracts after source or schema changes;
7. how field identity survives renaming or reordering;
8. how ADUC avoids redefining Croissant files, record sets, extraction rules, OpenAPI operations, or JSON Schema types;
9. offline and unavailable-reference behavior;
10. migration from the current mapping-profile `describes`, `validFor`, and `referenceScheme` fields.

## Required counterexamples

The specification must reject or explicitly block:

- an unversioned mutable source URL used as the only binding;
- a CSV header reference without a fixed header identity and encoding;
- a JSON Pointer applied to the wrong schema version;
- a contract silently reused after the described source changed;
- an embedded source description whose digest does not match `validFor`;
- a local reference whose resolution scheme is undeclared;
- duplicated source structure that conflicts with the authoritative external description.

## Compatibility requirement

The current semantic-mapping profile fields:

```text
describes
validFor
referenceScheme
localReference
```

must remain interpretable through a versioned migration path. The new model must preserve existing examples without silently changing which source or field an assertion addresses.

## Scope boundary

Do not implement the full-Core schema, units strategy, temporal strategy, identity strategy, compiler, registry, review UI, extensions, MCP adapter, or anticipation engine in this task.

## Completion test

An independent implementer must be able to bind an ADUC contract to one JSON source and one CSV source, resolve every local reference deterministically, detect a source-version mismatch, and explain which structural details remain owned by Croissant, JSON Schema, or OpenAPI rather than ADUC.