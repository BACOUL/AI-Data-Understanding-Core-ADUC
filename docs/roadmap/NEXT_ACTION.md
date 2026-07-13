# Next Action

## Single active task

Define and accept the complete ADUC epistemic lifecycle before implementing the full-Core JSON Schema.

Create:

```text
docs/decisions/ADR-0005-complete-epistemic-lifecycle.md
spec/EPISTEMIC_STATUS_MODEL_0_1.md
```

## Objective

Define exactly how ADUC represents and consumes:

```text
unknown
inferred
reviewed
verified
canonical
contested
deprecated
```

The decision must preserve the existing immutable mapping-assertion model while adding the missing full-Core lifecycle states without ambiguous authority or confidence semantics.

## Required decisions

1. whether all seven values are one property or whether publication authority, review state, conflict state, and lifecycle state require separate properties;
2. the precise difference between `reviewed` and `verified`;
3. the precise difference between `verified` and `canonical`;
4. how `unknown` is represented without inventing a semantic target;
5. how `deprecated` relates to immutable replacement and `supersedes`;
6. whether `contested` is a mapping status, conflict state, or separate assertion relation;
7. when confidence is required, optional, or forbidden;
8. evidence requirements for every state;
9. consumer selection and blocking rules;
10. migration from the current four-state semantic-mapping schema.

## Required counterexamples

The specification must reject or explicitly block:

- an `unknown` mapping that includes a fabricated semantic target;
- an automatically inferred mapping marked `verified`;
- a reviewed mapping presented as source-owner canonical;
- a canonical mapping that uses probability as a substitute for authority;
- a contested mapping silently selected as authoritative;
- a deprecated mapping without a documented reason or replacement behavior;
- an in-place mutation of a published assertion.

## Compatibility requirement

The current implemented states:

```text
inferred
reviewed
canonical
contested
```

must remain interpretable. The ADR must define whether they map directly into the full model or require a versioned migration.

## Scope boundary

Do not implement the complete full-Core schema, compiler, review UI, registry, extensions, or anticipation engine in this task. Do not add states merely because they sound useful; every state must change deterministic producer or consumer behavior.

## Completion test

An independent implementer must be able to classify the reference examples and every counterexample consistently, explain the authority and confidence represented by each state, and derive deterministic consumer behavior without private guidance.
