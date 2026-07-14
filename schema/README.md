# ADUC Schemas

## Official experimental Core family

ADR-0015 implements the frozen ADR-0014 object model as a local JSON Schema Draft 2020-12 family:

```text
aduc-core.schema.json
aduc-envelope.schema.json
aduc-metadata.schema.json
resource.schema.json
structure.schema.json
semantics.schema.json
identity.schema.json
context.schema.json
provenance.schema.json
uncertainty.schema.json
relations.schema.json
policy.schema.json
qualification.schema.json
extension.schema.json
```

`aduc-core.schema.json` is the validation entry point. All operational `$ref` values are relative and resolve from the local schema registry assembled by `tools/aduc_core_validate.py`. No remote schema or JSON-LD context retrieval is required.

The family enforces:

- the ten reserved Core blocks;
- the minimum `aduc + resource + structure` envelope;
- module types and top-level cardinalities;
- closed Core objects;
- absolute identifiers and vocabulary IRIs;
- lowercase 64-hex SHA-256 digests;
- accepted controlled enums;
- assertion qualification fields;
- relation endpoint exclusivity;
- policy rule structure and the policy-to-provenance dependency;
- collision-safe extension namespaces.

## Semantic-mapping compatibility schema

`aduc-mapping-profile.schema.json` remains the schema for the earlier standalone semantic-mapping profile. It is preserved for compatibility and migration tests; it is not the root schema for full-Core contracts.

## Validation

```bash
python tools/aduc_core_validate.py examples/core/complete-model.example.json
python tools/aduc_core_validate.py examples/core/valid/cases.json
python tools/aduc_core_validate.py examples/core/invalid/cases.json --schema-only
python -m unittest discover -s tests/core_schema -p "test_*.py"
```

The CLI reports stable JSON paths and schema error families. By default it also executes the ADR-0014 architecture checker.

For full-Core orchestration across schema, architecture and profile checks, use:

```bash
python tools/aduc_core.py validate examples/core/complete-model.example.json
python tools/aduc_core.py compare examples/core/complete-model.example.json examples/core/complete-model.example.json
python -m unittest discover -s tests/core_validator -p "test_*.py"
python -m unittest discover -s tests/core_comparator -p "test_*.py"
```

`tools/aduc_core.py` produces the versioned reports documented in `spec/ADUC_CORE_VALIDATION_0_1.md` and `spec/ADUC_CORE_COMPARISON_0_1.md`.

## Rules not enforceable by JSON Schema alone

The complementary architecture and domain validators check:

- uniqueness of Core identifiers across modules;
- deterministic resolution of `Ref` and `Refs` references;
- extension payload namespaces against declarations;
- one-owner rules across modules;
- whether a canonical assertion has qualifying authority and evidence;
- replacement or supersession cycles;
- conflicting authoritative assertions;
- source and policy digest equality across objects;
- identity, relation, provenance, uncertainty and policy semantics;
- JSON-LD/RDF round-trip behavior;
- signature and trust verification when introduced.

Passing JSON Schema proves structural conformance only. It does not prove factual truth, authority, legal permission or operational safety.
