# Next Action

## Single active task

Create:

```text
spec/SEMANTIC_MAPPING_ASSERTION_MODEL_0_1.md
```

## Objective

Define the smallest information model required to express one portable semantic mapping assertion without duplicating Croissant, JSON-LD/RDF, PROV-O, DQV or ODRL.

## Candidate concepts to test

- local source reference;
- semantic target identifier;
- mapping status;
- confidence for non-authoritative mappings;
- mapping authority or asserting agent;
- evidence references;
- source/schema version for which the mapping is valid;
- creation or publication time.

Every candidate concept must be justified by a concrete interoperability failure that occurs when it is absent. Unnecessary concepts must be removed.

## Required output

1. normative terminology candidates;
2. required versus optional properties;
3. status definitions and allowed transitions;
4. invariants preventing authority promotion;
5. relationship to Croissant fields and JSON-LD/RDF identifiers;
6. provenance representation through PROV-O;
7. distinction between mapping confidence, data quality and factual truth;
8. at least two complete examples;
9. at least five invalid or unsafe counterexamples;
10. unresolved questions and explicit exclusions.

## Completion test

Gate 1 cannot proceed to a normative JSON Schema until the model demonstrates that each required property is necessary, provider-independent and representable without duplicating an established standard.
