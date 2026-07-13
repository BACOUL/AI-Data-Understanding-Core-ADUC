# Next Action

## Single active task

Define and accept the ADUC provenance and transformation-lineage strategy before implementing the full-Core JSON Schema.

Create:

```text
docs/decisions/ADR-0010-provenance-and-transformation-lineage.md
spec/PROVENANCE_PROFILE_0_1.md
examples/provenance/
```

## Objective

Define how ADUC records where data and assertions came from, which agents and activities produced them, which transformations were applied, which software and parameters were used, and whether a result can be reproduced or trusted without inventing missing lineage.

## Completed dependencies

The following Core decisions are specified and reference-tested:

```text
ADR-0005  epistemic lifecycle
ADR-0006  source description and immutable binding
ADR-0007  units and deterministic conversion
ADR-0008  temporal semantics and timezone alignment
ADR-0009  entity identity and safe equivalence
```

Every provenance record must bind exact inputs and outputs through ADR-0006, use ADR-0008 for activity time, and preserve ADR-0005 authority, evidence, conflict, and lifecycle.

## Cross-cutting adoption constraint

The official [`ADOPTION_AND_VALUE_VALIDATION.md`](ADOPTION_AND_VALUE_VALIDATION.md) plan remains mandatory for later compiler, review, and interoperability work.

Do not implement the JSON/CSV compiler now. A future compiler may infer missing lineage only as `inferred`, must distinguish observed provenance from reconstructed provenance, and must expose gaps for review.

## Required decisions

1. how ADUC reuses PROV-O rather than creating a competing provenance ontology;
2. how entities, activities, agents, generation, use, derivation, attribution, association, invalidation, and delegation are represented;
3. how source bytes, schema versions, contracts, transformations, and outputs are linked by immutable identifiers and hashes;
4. how software name, version, build, environment, parameters, prompts, models, and configuration are recorded;
5. how deterministic, nondeterministic, manual, inferred, and externally attested transformations differ;
6. how partial, missing, reconstructed, contested, and deprecated lineage is represented;
7. how activity start/end, ordering, retries, branching, aggregation, and batch processing are represented;
8. how a consumer detects cycles, impossible ordering, missing inputs, conflicting outputs, or broken hash chains;
9. how privacy and policy restrict disclosure of provenance without falsely claiming complete lineage;
10. how current source-binding, unit-conversion, temporal-resolution, and identity-crosswalk examples migrate into one provenance model.

## Required counterexamples

The specification must reject or explicitly block:

- claiming a result was derived from an input without binding the input;
- recording a transformation without the responsible agent or method;
- omitting software/model version while claiming reproducibility;
- treating inferred lineage as observed or canonical lineage;
- accepting a provenance cycle;
- accepting activity end before activity start;
- silently replacing one output hash with another;
- claiming deterministic reproduction for a nondeterministic process without seeds and environment evidence;
- hiding a material manual intervention;
- treating a prompt or model name alone as sufficient AI provenance;
- declaring complete lineage when required segments are redacted or missing;
- ignoring invalidation, retraction, conflict, or deprecation events.

## Scope boundary

Do not implement the full-Core schema, complete uncertainty or policy profiles, compiler, review UI, registry service, MCP adapter, extensions, or anticipation engine in this task.

## Completion test

An independent implementer must be able to:

1. trace one value from original source bytes through parsing, unit conversion, temporal resolution, identity linking, and final comparison;
2. identify every responsible agent, activity, method, version, input, and output;
3. distinguish observed, inferred, attested, and incomplete provenance;
4. reproduce one deterministic transformation from pinned evidence;
5. reject one cyclic or broken lineage;
6. preserve redaction status, authority, evidence, time, hashes, and lifecycle without private guidance.
