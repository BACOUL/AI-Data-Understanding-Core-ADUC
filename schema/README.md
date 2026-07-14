# Schemas

## Active implemented subset

`aduc-mapping-profile.schema.json` is the active schema for the currently implemented semantic-mapping subset. It validates the portable semantic mapping profile defined in `spec/SEMANTIC_MAPPING_ASSERTION_MODEL_0_1.md`.

## Historical bootstrap scaffold

`aduc-core.schema.json` is retained only as an historical bootstrap scaffold. It is not the official full-Core schema, does not implement ADR-0014, does not use `spec/core-module-manifest.json`, and is not used by the reference mapping validator.

The next active task will replace or supersede this scaffold with the official modular Draft 2020-12 family:

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

The official family must implement ADR-0014 and `spec/ADUC_CORE_MODEL_0_1.md` without revisiting module ownership or dependencies.

## Rules not enforceable by JSON Schema alone

The complementary reference validator must check at least:

- uniqueness of Core identifiers across modules;
- deterministic resolution of `Ref` and `Refs` references;
- whether a `canonical` assertion was actually published by the recognized source authority;
- whether replacement or supersession targets exist and do not create cycles;
- conflicting authoritative assertions across the contract graph;
- whether source identity and version bindings match actual immutable bytes;
- whether external vocabulary relations are semantically valid;
- graph integrity, relation closure and cycle constraints;
- policy-target digest and evidence consistency where cross-object comparison is required;
- JSON-LD expansion and RDF round-trip preservation;
- signature and trust verification when introduced.

Passing JSON Schema proves structural conformance only. It does not prove factual truth, authority, legal permission or operational safety.