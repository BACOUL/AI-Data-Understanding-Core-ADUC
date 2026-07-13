# Instructions for AI coding agents

These rules are mandatory for every automated contribution.

## Required reading order

1. `docs/project/PROJECT_CHARTER.md`
2. `docs/project/NON_GOALS.md`
3. `docs/method/METHOD.md`
4. `docs/roadmap/PROJECT_STATUS.md`
5. `docs/roadmap/NEXT_ACTION.md`
6. Relevant specification, schema, examples, tests, and ADRs

## Execution discipline

- Execute only the task explicitly written in `docs/roadmap/NEXT_ACTION.md`.
- Do not add adjacent features, rename the project, or redesign the architecture without an approved ADR.
- One pull request must have one primary objective.
- Never change normative behavior without updating the specification, schema, examples, tests, changelog, and compatibility notes as applicable.
- Never claim completion unless the required quality gates pass.
- Preserve uncertainty. Do not convert inferred semantics into verified or canonical semantics.
- Prefer compatibility with established standards over custom invention.
- Do not implement extensions before the Core gate is complete.

## Required completion updates

Every completed task must update:

- `docs/roadmap/EXECUTION_LEDGER.md`
- `docs/roadmap/PROJECT_STATUS.md`
- `docs/roadmap/NEXT_ACTION.md`
- `CHANGELOG.md` when user-visible or normative behavior changed

## Pull request evidence

A pull request must contain:

- objective;
- files changed;
- validation commands and results;
- specification impact;
- compatibility impact;
- security/privacy impact;
- next action.

If any required information is unknown, state `unknown`; do not guess.
