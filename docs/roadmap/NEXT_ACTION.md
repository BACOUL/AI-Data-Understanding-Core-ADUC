# Next Action

## Single active task

Create and accept:

```text
docs/decisions/ADR-0002-aduc-as-an-ai-semantic-mapping-profile.md
```

## Decision to freeze

Determine whether ADUC continues as a lightweight, cross-resource **AI semantic mapping profile** over established standards rather than as a new universal data model.

The candidate profile is centered on:

- mapping a local field or value to an existing semantic identifier;
- explicit mapping status: `unknown`, `inferred`, `reviewed`, `verified`, `canonical`, `contested`, or `deprecated`;
- confidence and evidence for non-authoritative mappings;
- provenance and authority of the mapping assertion;
- deterministic consumer behavior for unknown, inferred, contested, or low-confidence mappings;
- a conformance suite comparing independent AI consumers.

## Required output

The ADR must define:

1. the exact bounded problem;
2. the v0.1 resource boundary;
3. the standards that must be reused rather than duplicated;
4. the smallest candidate mapping assertion;
5. the falsifiable interoperability promise;
6. the stop or pivot condition;
7. consequences for the current bootstrap schema and repository name.

## Completion test

Gate 0 remains active until this ADR is accepted. No new normative schema field, compiler, extension, registry, or anticipation-engine feature may be implemented before the decision is frozen.
