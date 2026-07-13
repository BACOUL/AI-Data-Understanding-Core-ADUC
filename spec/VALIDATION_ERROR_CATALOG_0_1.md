# ADUC Validation Error Catalog 0.1

- Status: Gate 3 candidate
- Date: 2026-07-13
- Applies to: `tools/aduc_validate.py`

## 1. Report model

Every issue contains:

```json
{
  "code": "ADUC-SCHEMA-001",
  "severity": "error",
  "category": "schema",
  "path": "/assertions/0/confidence",
  "message": "Human-readable explanation"
}
```

Categories:

- `input`: file, JSON or validator-schema loading problem;
- `schema`: Draft 2020-12 structural conformance problem;
- `semantic`: profile-level rule that JSON Schema alone cannot enforce;
- `trust`: assertion requiring external authority configuration or verification.

Severities:

- `error`: profile is non-conforming and the command exits `1`;
- `warning`: profile may be structurally conforming, but a trust or operational limitation remains.

## 2. Exit codes

| Exit | Meaning |
|---:|---|
| `0` | Schema and semantic checks pass. Warnings may remain. |
| `1` | One or more conformance errors exist. |
| `2` | Input file, JSON, schema file or command usage prevents validation. |

## 3. Stable codes

### `ADUC-INPUT-001`

The profile file does not exist or cannot be read.

- Severity: error
- Category: input
- Exit: 2

### `ADUC-INPUT-002`

The profile is not valid JSON.

- Severity: error
- Category: input
- Exit: 2

### `ADUC-INPUT-003`

The selected validator schema cannot be loaded or is invalid.

- Severity: error
- Category: input
- Exit: 2

### `ADUC-SCHEMA-001`

The profile violates `schema/aduc-mapping-profile.schema.json`.

A report may contain this code more than once, with different JSON Pointer paths and messages.

- Severity: error
- Category: schema
- Exit: 1

### `ADUC-DOC-001`

Two assertions in the same profile use the same assertion identifier.

Assertion identifiers must be unique so lifecycle, evidence and conflict references remain unambiguous.

- Severity: error
- Category: semantic
- Exit: 1

### `ADUC-LIFE-001`

An assertion declares that it supersedes itself.

- Severity: error
- Category: semantic
- Exit: 1

### `ADUC-LIFE-002`

Assertions form a `supersedes` cycle within one profile document.

Example:

```text
A supersedes B
B supersedes A
```

An immutable replacement chain must be acyclic.

- Severity: error
- Category: semantic
- Exit: 1

### `ADUC-CONFLICT-001`

Two or more canonical assertions for the same local reference have incompatible semantic target and mapping-relation pairs.

The validator reports the conflict rather than selecting one mapping.

- Severity: error
- Category: semantic
- Exit: 1

### `ADUC-TRUST-001`

A canonical assertion names an authority that is not present in the local trusted-authority configuration.

This code is a warning because the profile can be structurally and semantically consistent while external authority remains unverified. Passing `--trusted-authority` is a local trust decision; it does not provide cryptographic or global proof.

- Severity: warning
- Category: trust
- Exit: 0 when no errors exist

## 4. JSON report

Example shape:

```json
{
  "profile": "example.aduc.json",
  "profileId": "urn:aduc:profile:example",
  "valid": false,
  "summary": {
    "errors": 1,
    "warnings": 1
  },
  "errors": [
    {
      "code": "ADUC-CONFLICT-001",
      "severity": "error",
      "category": "semantic",
      "path": "/assertions",
      "message": "Incompatible canonical targets..."
    }
  ],
  "warnings": [
    {
      "code": "ADUC-TRUST-001",
      "severity": "warning",
      "category": "trust",
      "path": "/assertions/0/assertedBy",
      "message": "Canonical authority was not verified..."
    }
  ]
}
```

## 5. Stability policy

- Existing code meanings must not change silently.
- New checks receive new codes.
- A code may gain clearer human wording without changing its machine meaning.
- Removing or materially changing a code requires a compatibility note and version change.
- JSON Pointer paths are instance locations, not stable identifiers across edited documents.

## 6. Explicit limitations

The Gate 3 validator does not:

- resolve identifiers over the network;
- verify signatures;
- prove that a publisher controls an asserted authority IRI;
- determine whether two ontology concepts are actually equivalent;
- expand JSON-LD or validate RDF semantics;
- validate mappings across multiple profile files;
- prove that source values are accurate or truthful;
- enforce permissions.
