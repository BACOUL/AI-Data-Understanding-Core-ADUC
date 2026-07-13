# Next Action

## Single active task

Begin Gate 4 by defining the source-authoring and review workflow without implementing automatic AI inference yet.

Create:

```text
spec/AUTHORING_WORKFLOW_0_1.md
examples/authoring/
```

## Objective

Specify how a user or future compiler creates, reviews, promotes, contests and publishes immutable semantic mapping assertions while preserving their provenance and prior versions.

## Required workflow

1. identify the described source and immutable source version;
2. enumerate local fields from Croissant or JSON Schema;
3. create inferred mapping proposals with method-bound confidence and evidence;
4. expose unmapped fields explicitly through coverage reporting rather than targetless assertions;
5. review proposals without editing published assertions in place;
6. create a new reviewed or canonical assertion that supersedes its predecessor;
7. contest a mapping without silently selecting an alternative;
8. export a schema-valid profile;
9. run the Gate 3 validator;
10. preserve a machine-readable authoring ledger.

## Required artifacts

- role definitions: inference producer, reviewer, source authority and consumer;
- immutable lifecycle diagrams;
- proposal and review record shapes;
- minimum human-review questions;
- two end-to-end examples from source field to published profile;
- failure cases preventing silent authority promotion;
- clear separation between authoring metadata and the portable profile.

## Scope boundary

Do not call external models, build a web UI, create a registry, resolve ontology terms over the network or implement the anticipation engine. This task defines the workflow and evidence required before authoring automation is built.

## Completion test

An independent developer must be able to follow the document manually and produce a valid profile whose lifecycle can be audited from inference through review or canonical publication.
