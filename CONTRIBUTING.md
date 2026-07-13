# Contributing

## Before proposing work

Read the charter, non-goals, execution method, project status, and next action.

## Contribution rules

- Open an issue before a normative or architectural change.
- Keep one primary objective per pull request.
- Add or update tests for behavioral changes.
- Use an ADR for Core architecture, compatibility, governance, or versioning decisions.
- Do not introduce domain-specific concepts into the Core without proving they are universally necessary.
- Do not hide uncertainty or silently promote inferred mappings.

## Local check

```bash
python -m pip install jsonschema
python tools/validate_contracts.py
```

## Commit style

Use clear imperative subjects, for example:

```text
Add bootstrap Core schema
Document inferred mapping invariant
Reject out-of-range confidence values
```
