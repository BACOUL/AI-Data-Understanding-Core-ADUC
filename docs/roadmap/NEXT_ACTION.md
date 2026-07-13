# Next Action

## Single active task

Implement Gate 2 by replacing the broad bootstrap validation model with the first machine-readable semantic mapping profile schema.

Create or update:

```text
schema/aduc-mapping-profile.schema.json
tests/fixtures/mapping-profile/valid/
tests/fixtures/mapping-profile/invalid/
tools/validate_contracts.py
```

## Required schema behavior

The schema must enforce:

1. profile identity, conformance version, source description and immutable source-version binding;
2. one declared local-reference scheme per v0.1 document;
3. one or more immutable mapping assertions;
4. absolute identifiers for documents, assertions, semantic targets, relations and asserting agents;
5. statuses limited to `inferred`, `reviewed`, `canonical` and `contested`;
6. confidence required for `inferred`, optional for `reviewed` and forbidden for `canonical`;
7. confidence method required whenever confidence is present;
8. evidence required for `inferred` and `contested`;
9. explicit mapping relation;
10. rejection of the unsafe counterexamples documented in `spec/SEMANTIC_MAPPING_ASSERTION_MODEL_0_1.md` where structurally enforceable.

## Required fixtures

At minimum:

- two complete valid fixtures matching the specification examples;
- valid reviewed mapping;
- valid contested mapping;
- invalid inferred mapping without confidence;
- invalid confidence without method;
- invalid canonical mapping with confidence;
- invalid contested mapping without evidence;
- invalid status;
- invalid missing source-version binding;
- invalid relative semantic target;
- invalid empty assertion list.

## Scope boundary

Do not add compiler, inference, registry, signatures, API/event support or anticipation-engine behavior. Cross-assertion conflicts and authority verification that JSON Schema cannot prove must be listed for the future semantic validator.

## Completion test

GitHub Actions must accept every official valid fixture and reject every official invalid fixture. The schema, validator and fixture count must be reported in the Pull Request evidence.
