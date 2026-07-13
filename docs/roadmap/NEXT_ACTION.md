# Next Action

## Single active task

Define and accept the ADUC entity identity and equivalence strategy before implementing the full-Core JSON Schema.

Create:

```text
docs/decisions/ADR-0009-entity-identity-and-equivalence.md
spec/IDENTITY_PROFILE_0_1.md
examples/identity/
```

## Objective

Define how ADUC identifies the entity described by a record, distinguishes identifiers from labels, represents possible and confirmed equivalence, preserves namespace and issuer authority, and prevents two records from being merged without sufficient evidence.

## Completed dependencies

The following Core decisions are now specified and reference-tested:

```text
docs/decisions/ADR-0005-complete-epistemic-lifecycle.md
docs/decisions/ADR-0006-source-description-and-binding.md
docs/decisions/ADR-0007-units-and-conversion.md
docs/decisions/ADR-0008-temporal-semantics.md
spec/EPISTEMIC_STATUS_MODEL_0_1.md
spec/SOURCE_DESCRIPTION_PROFILE_0_1.md
spec/UNIT_PROFILE_0_1.md
spec/TEMPORAL_PROFILE_0_1.md
```

Every identity assertion must remain bound to the exact source and local field through ADR-0006. Time-scoped identifiers and identity evidence must use the temporal profile rather than informal date strings.

## Cross-cutting adoption constraint

The official [`ADOPTION_AND_VALUE_VALIDATION.md`](ADOPTION_AND_VALUE_VALIDATION.md) plan remains mandatory for later compiler, review, and interoperability work.

Do not implement the JSON/CSV compiler now. A future compiler may propose identity matches only as `inferred`, must record the matching method, evidence, source bindings, applicable time, and unresolved alternatives, and must surface possible collisions for review.

## Required decisions

1. which established identifier and entity-linking standards ADUC reuses rather than replaces;
2. how an identifier records namespace, issuer, scheme, lexical value, canonical form, and validity;
3. how local identifiers differ from globally resolvable identifiers;
4. how entity type and identifier type remain separate claims;
5. how `same entity`, `possible match`, `different entity`, `broader/narrower identity`, and unresolved identity are represented;
6. which evidence permits an identity assertion to be inferred, reviewed, verified, or canonical;
7. how aliases, renames, recycled identifiers, mergers, splits, and identifier deprecation are handled;
8. how identity assertions are scoped by source version, organization, domain, and time;
9. how conflicting identity assertions block automatic merging;
10. how privacy-sensitive or pseudonymous identifiers are represented without exposing secret values;
11. how record linkage confidence is calibrated and kept separate from authority;
12. how current examples such as `M42`, `MAIN-B`, and `R42` migrate into the full-Core identity model.

## Required counterexamples

The specification must reject or explicitly block:

- treating a display name as a globally unique identifier;
- merging `M42` and `MAIN-B` because their measurements look similar;
- comparing identifiers without their namespace or issuer;
- treating the same lexical identifier from two organizations as the same entity;
- using an expired or recycled identifier outside its validity interval;
- converting an inferred match into canonical identity without source authority;
- accepting two contradictory canonical identity assertions silently;
- using `owl:sameAs` for a weak or partial match;
- exposing an unhashed private identifier when only pseudonymous linkage is permitted;
- ignoring an entity split, merger, or identifier reassignment;
- treating entity type compatibility as proof of identity;
- declaring identity when the available evidence supports only a possible match.

## Compatibility requirement

Current examples that use values such as:

```text
M42
MAIN-B
R42
org-river:station-id
```

must receive a documented migration path. The model must preserve the difference between a local identifier, a namespace-qualified identifier, a human label, a possible crosswalk, and an authoritative identity assertion.

## Scope boundary

Do not implement the full-Core schema, complete provenance or policy profiles, compiler, review UI, registry service, MCP adapter, extensions, or anticipation engine in this task.

## Completion test

An independent implementer must be able to:

1. represent one entity with multiple identifiers from different namespaces;
2. distinguish a label from an identifier;
3. record a possible match without merging records automatically;
4. verify one authoritative equivalence and reject one unsupported equivalence;
5. detect a recycled identifier using temporal validity evidence;
6. preserve identity evidence, authority, confidence, source binding, and lifecycle without private guidance.
