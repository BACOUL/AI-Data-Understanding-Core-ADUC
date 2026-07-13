# ADR-0012 — General Relation Semantics

- Status: proposed
- Date: 2026-07-13
- Issue: #42
- Pull request: pending
- Decision owners: ADUC maintainers

## Context

ADUC already defines source binding, semantic mappings, units, time, identity, provenance, uncertainty and data quality. A complete Core still needs a safe way to express relationships between resources, fields, concepts, entities, assertions, activities, versions and results.

A generic relation layer is dangerous when it silently assumes that:

- similar means identical;
- a directed relation can be reversed;
- a relation is transitive or symmetric;
- temporal order or correlation proves causation;
- an absent edge is false;
- a local label identifies a global predicate;
- an assertion remains valid outside its time, context or lifecycle;
- conflicting authoritative assertions can be merged.

## Decision

### 1. Reuse external vocabularies

ADUC uses absolute predicate IRIs from RDF, RDFS, OWL, SKOS, PROV-O, Dublin Core Terms and domain vocabularies. It does not create duplicates of established predicates.

A pinned predicate registry records only the consumer-relevant profile needed for deterministic validation:

```text
family
object mode
allowed endpoint kinds
inverse predicate
symmetry
transitivity
reflexivity
functionality
inverse functionality
acyclicity
disjoint predicates
minimum authority
external authority source
```

The registry never overrides the authoritative vocabulary.

### 2. Separate three layers

```text
vocabulary definition
relation assertion
consumer inference
```

A vocabulary definition declares predicate semantics. A relation assertion claims that the predicate holds between two bound endpoints. A consumer inference is a derived statement permitted only by the vocabulary definition and qualifying assertions.

### 3. Common assertion record

Every assertion identifies:

```text
relationId
subject binding
predicate IRI
object binding or typed/language literal
polarity
method
provenance activity
authority level
assertedBy
evidence
conflict state
lifecycle state
optional temporal validity
optional contexts
optional uncertainty reference
```

Object relations and literal-valued properties are distinct.

### 4. Endpoint binding

Resource endpoints must be declared in the case or contract and typed as one of:

```text
resource
field
concept
entity
assertion
activity
version
result
```

The predicate registry determines which kinds are allowed. Local names and labels are not portable identifiers.

### 5. Inverse and symmetry

A reverse assertion may be derived only when:

- the predicate has an authoritative `inverseOf`; or
- the predicate is authoritatively symmetric.

A directed relation without an inverse remains one-way.

### 6. Transitivity

Transitive closure is allowed only when the authoritative predicate profile declares transitivity.

SKOS direct hierarchy preserves the distinction between:

```text
skos:broader
skos:broaderTransitive
```

Two `skos:broader` assertions may support a `skos:broaderTransitive` inference, but not a new direct `skos:broader` assertion.

### 7. Exactness

`skos:closeMatch` remains a close concept mapping. It must not become equality.

`skos:exactMatch` applies to concepts and follows SKOS characteristics. `owl:sameAs` is restricted to entity endpoints and additionally requires a qualifying identity-profile decision with verified or canonical authority.

### 8. Time and context

A relation may be qualified by:

```text
validDuring
contexts
```

Automatic use outside the declared interval or context is blocked.

### 9. Open-world behavior and negation

Absence of an assertion means `unknown`, not `false`.

Negation requires an explicit negative assertion with the same authority, evidence, provenance and lifecycle requirements as a positive assertion.

### 10. Conflict and graph integrity

Automatic use is blocked for contested or deprecated assertions.

The evaluator detects:

- duplicate relation identifiers;
- functional-property conflicts;
- inverse-functional conflicts;
- positive/negative authoritative contradictions;
- disjoint predicate conflicts;
- cycles for predicates declared acyclic.

### 11. Causality

Correlation, dependency, temporal order and `causalCandidate` never establish causation. A domain extension may define a causal model, but the Core does not invent one.

### 12. JSON-LD/RDF export

Every assertion can be exported as an RDF statement node with qualification metadata. A direct triple is emitted only for an active, clear, positive assertion that passes scope and authority checks.

The export uses absolute IRIs and deterministic ordering. It does not require private prompts or model-specific interpretation.

## Consequences

### Positive

- relation semantics remain owned by their vocabularies;
- consumers do not invent equality, inverse, transitivity or causation;
- temporal, contextual, evidential and lifecycle qualification is preserved;
- open-world unknowns remain explicit;
- conflicts and unsafe graph structures block automation;
- JSON-LD/RDF exchange is deterministic.

### Costs

- producers must bind endpoints and preserve provenance;
- consumers need a pinned vocabulary profile;
- many useful inferences remain blocked until semantics are declared;
- domain-specific causal and graph rules require extensions.

## Rejected alternatives

- one free-text `relationType`;
- inferring predicate semantics from its label;
- treating all mappings as equality;
- assuming graph closure rules from examples;
- closed-world negation by absence;
- automatic causality from correlation;
- unqualified triples with hidden provenance.

## References

- RDF 1.1 Concepts: https://www.w3.org/TR/rdf11-concepts/
- OWL 2 Structural Specification: https://www.w3.org/TR/owl2-syntax/
- SKOS Reference: https://www.w3.org/TR/skos-reference/
- PROV-O: https://www.w3.org/TR/prov-o/
- Dublin Core Terms: http://purl.org/dc/terms/

## Acceptance evidence

Pending PR validation:

- eighteen valid relation and inference cases;
- thirty invalid counterexamples;
- deterministic registry-integrity checks;
- inverse, symmetry, transitivity, scope, conflict, cycle and open-world tests;
- deterministic JSON-LD/RDF export;
- all pre-existing GitHub Actions suites.

## Follow-up

1. define the policy and permitted-use profile;
2. freeze the normative full-Core object model;
3. implement the full-Core JSON Schema family;
4. unify validation and comparison across accepted profiles.
