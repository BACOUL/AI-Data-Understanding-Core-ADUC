# Repository Execution Method

This repository is the project operating system. Work must advance through gates. A later gate cannot begin before the previous gate has objective evidence of completion.

## Permanent workflow

```text
Idea or problem
→ Issue
→ Scope decision
→ ADR when architectural
→ One bounded implementation task
→ Tests and evidence
→ Pull request
→ Review
→ Merge
→ Status, ledger, and next action updated
```

## Gate 0 — Prior-art and problem definition

Required evidence:

- exact problem statement;
- target users;
- existing standards matrix;
- non-goals;
- falsifiable initial promise.

Exit criterion: the proposed Core does not merely rename an existing standard.

## Gate 1 — Core information model

Required evidence:

- minimal concepts;
- required and optional fields;
- uncertainty/status model;
- extension mechanism;
- complete worked example.

Exit criterion: every Core element is necessary for the initial proof.

## Gate 2 — Machine-readable schema

Required evidence:

- JSON Schema;
- valid fixtures;
- invalid fixtures;
- automated validation.

Exit criterion: CI reliably enforces the written rules.

## Gate 3 — Reference validator

Required evidence:

- deterministic validator;
- actionable errors;
- conformance report;
- documented command.

Exit criterion: independent users can verify a contract locally.

## Gate 4 — Source authoring workflow

Required evidence:

- manual authoring guide;
- inference proposal format;
- review states;
- export process.

Exit criterion: inferred semantics cannot silently become authoritative.

## Gate 5 — Comparator

Required evidence:

- concept matching;
- unit compatibility;
- temporal alignment;
- candidate entity matching;
- explicit unresolved differences.

Exit criterion: the reference demonstration passes without hidden mappings.

## Gate 6 — Multi-model interoperability

Required evidence:

- fixed input contracts;
- fixed questions/tasks;
- outputs normalized for comparison;
- documented failures and disagreements.

Exit criterion: at least two different systems reach compatible interpretations.

## Gate 7 — Public alpha

Required evidence:

- stable repository structure;
- license files;
- governance;
- contribution process;
- release notes;
- security policy;
- five-minute tutorial.

Exit criterion: a third party can evaluate and challenge the project independently.

## Scope-control rules

- Only one gate is active at a time.
- Only one `NEXT_ACTION` is active at a time.
- New ideas go to issues or `docs/backlog/IDEAS.md`; they do not interrupt active work.
- Extensions stay blocked until Gate 6 passes.
- Marketing claims must cite a passing test or published evidence.
