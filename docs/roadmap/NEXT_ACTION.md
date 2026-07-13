# Next Action

## Single active task

Define and accept the ADUC general-relation semantics before implementing the full-Core JSON Schema.

Create:

```text
docs/decisions/ADR-0012-general-relation-semantics.md
spec/RELATION_PROFILE_0_1.md
examples/relations/
tools/aduc_relations.py
tests/relations/
```

## Objective

Define how ADUC represents portable relationships between resources, fields, concepts, entities, assertions, activities, versions, and results without inventing equality, transitivity, symmetry, or causal meaning that the relation does not explicitly support.

## Completed dependencies

```text
ADR-0005  epistemic lifecycle
ADR-0006  source description and immutable binding
ADR-0007  units and deterministic conversion
ADR-0008  temporal semantics and timezone alignment
ADR-0009  entity identity and safe equivalence
ADR-0010  provenance and transformation lineage
ADR-0011  uncertainty and data quality
```

Every relation assertion must bind its endpoints through accepted profiles, preserve authority and lifecycle through ADR-0005, use ADR-0008 for temporal scope, retain ADR-0010 provenance, and preserve ADR-0011 uncertainty where the relation is probabilistic or incomplete.

## Required decisions

1. distinguish relation assertion, relation vocabulary definition, and consumer inference;
2. reuse RDF, RDFS, OWL, SKOS, PROV-O, DC Terms, and domain vocabularies rather than inventing duplicate predicates;
3. define subject, predicate, object, direction, inverse, scope, validity, authority, method, evidence, and provenance;
4. distinguish object relations from literal-valued properties;
5. define when symmetry, transitivity, reflexivity, functionality, inverse functionality, and inverse relations may be used;
6. forbid consumers from assuming these characteristics when they are not declared by an authoritative vocabulary;
7. define exact, broader, narrower, related, part-whole, version, derivation, causal-candidate, and dependency behavior without conflation;
8. define temporal and contextual qualification of relations;
9. define conflict, challenge, deprecation, replacement, and contradictory relation handling;
10. define relation-chain and graph-cycle rules;
11. preserve open-world unknowns rather than interpreting absence as falsehood;
12. define safe export to RDF/JSON-LD and deterministic consumer outcomes.

## Required counterexamples

The specification must reject or explicitly block:

- treating `skos:closeMatch` as exact equality;
- using `owl:sameAs` for a candidate or partial match;
- assuming transitivity for a non-transitive relation;
- reversing a directed relation without an explicit inverse;
- inferring causation from correlation or temporal order;
- applying a relation outside its temporal or contextual scope;
- accepting missing or unbound endpoints;
- silently merging contradictory canonical relations;
- treating absent relations as proof of negation;
- creating cycles where the declared relation is acyclic;
- applying deprecated or contested relations automatically;
- allowing local predicate labels to act as global relation identifiers.

## Scope boundary

Do not implement the complete policy profile, full-Core schema, compiler, review UI, registry service, MCP adapter, extensions, or anticipation engine in this task.

## Completion test

An independent implementer must be able to:

1. represent a directed, qualified relation between two bound ADUC objects;
2. distinguish exact, close, broader, narrower, part-whole, version, and derivation relations;
3. derive an inverse only when the vocabulary authorizes it;
4. block unsupported transitive or causal inference;
5. preserve authority, evidence, time, context, provenance, uncertainty, conflict, and lifecycle;
6. reject one contradictory, cyclic, or out-of-scope relation graph;
7. serialize qualifying relations to deterministic JSON-LD/RDF without private guidance.
