# Project Status

- Project: AI Data Understanding Core (working name)
- Current phase: Phase 0 — Full-Core definition and public foundation
- Current release: unreleased
- Target release: `0.1.0-alpha.0`
- Overall status: full-Core mission and architecture are defined; the implemented mapping profile remains a partial experimental subset

## Official direction

ADUC is an open, model-independent contract intended to let data describe:

```text
structure
semantics
identity
context
provenance
uncertainty
relations
policy
```

to AI systems, agents, and applications.

The complete candidate contract is organized into ten blocks:

```text
aduc
resource
structure
semantics
identity
context
provenance
uncertainty
relations
policy
```

`spec/ADUC_CORE_SPEC_0_1.md` is the authoritative full-Core working draft.

ADR-0004 preserves the current semantic-mapping work as the first implemented experimental subset of the `semantics` block. It is not the complete Core.

## Completed project foundation

- repository governance and contribution structure;
- project charter and non-goals;
- execution method and decision records;
- prior-art matrix covering thirteen standards and approaches;
- official project structure;
- official master plan;
- complete full-Core working draft;
- ADR-0004 positioning the existing semantic profile inside the full Core;
- first informative ten-block full-Core example;
- English static public website source;
- GitHub Pages deployment workflow;
- website and example validation script.

## Completed experimental semantic-mapping implementation

- minimal semantic-mapping assertion model;
- immutable assertion lifecycle;
- implemented statuses: `inferred`, `reviewed`, `canonical`, and `contested`;
- Draft 2020-12 semantic-mapping profile schema;
- four valid and ten invalid official mapping fixtures;
- text and JSON CLI validator;
- stable validation error catalogue;
- duplicate-ID, lifecycle-cycle, canonical-conflict, and authority-warning checks;
- manual authoring and review workflow;
- river and machine authoring examples;
- deterministic semantic comparison protocol and CLI;
- French and US comparison sources with differently named fields;
- explicit `notEvaluated` behavior for absent unit, time, and identity dimensions;
- ADR-0003 JSON-LD namespace and offline context strategy;
- protected local context `urn:aduc:context:0.1`;
- JSON-LD expansion, compaction, and URDNA2015 RDF normalization;
- provider-neutral multi-model conformance protocol, frozen package, result schema, and deterministic evaluator.

## Evidence-based findings

- Existing standards collectively cover most individual capabilities in the original vision and must be reused rather than duplicated.
- Croissant is a strong foundation for dataset description but does not alone provide the complete ADUC consumer contract.
- Semantic mapping status, authority, evidence, uncertainty, and deterministic consumer behavior remain useful integration concerns.
- Comparable semantic targets alone do not establish compatible units, time alignment, or entity identity.
- Same-looking local field names are insufficient when semantic targets differ.
- Unknown or contested interpretations must not be silently upgraded.
- JSON Schema cannot prove publisher authority, factual truth, global identity, or legal permission.
- A frozen provider-neutral harness can test agreement, but illustrative results are not external interoperability proof.
- The public website must distinguish the full-Core vision from the currently implemented subset.

## Full-Core version 0.1 scoreboard

| Deliverable | Status |
|---|---|
| Core specification | Working draft created |
| Official full-Core JSON Schema | Not implemented |
| Ten valid full-Core examples | 1 informative example created |
| Ten invalid full-Core examples | Not implemented |
| CLI validator | Partial: semantic-mapping profile only |
| JSON/CSV compiler | Not implemented |
| Minimal review interface | Not implemented |
| Core vocabulary | Partial: semantic-mapping JSON-LD context only |
| Two-source comparison | Partial: semantic targets; units/time/identity absent |
| Two-model demonstration | Harness exists; external proof absent |
| Conformance suite | Partial implementation |
| Try in 5 minutes | English website guide created for current tools |

## Not yet validated

- normative cardinalities and rules for all ten Core blocks;
- complete seven-state epistemic lifecycle;
- unit identifier and conversion strategy;
- temporal semantics and alignment;
- entity identity and equivalence;
- complete policy profile;
- migration from the mapping-profile document to the full Core envelope;
- full-Core JSON Schema;
- JSON and CSV compiler;
- review interface;
- qualifying external runs from two independent AI consumers;
- public HTTPS namespace and final project name;
- commercial adoption model.

## Active blockers

- full-Core normative ADRs have not been accepted;
- full-Core schema family does not exist;
- the first complete example is informative rather than schema-validatable;
- unit, time, and identity comparison cannot be demonstrated from the current semantic-only profile;
- no qualifying external model runs have been committed;
- the public name remains provisional.

## Next gate

Accept the complete epistemic-lifecycle decision and define how `unknown`, `inferred`, `reviewed`, `verified`, `canonical`, `contested`, and `deprecated` interact with immutable assertions, authority, confidence, evidence, and replacements.

## Rule

This file reports evidence, not optimism. Do not mark an item complete without a linked artifact or passing check.
