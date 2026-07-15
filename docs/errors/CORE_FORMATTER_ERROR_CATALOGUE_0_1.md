# ADUC Core formatter error catalogue 0.1

| Code | Exit | Meaning |
|---|---:|---|
| `ADUC-FMT-INPUT-001` | 3 | Input cannot be found, inspected or read |
| `ADUC-FMT-INPUT-002` | 3 | Invalid JSON or duplicate object member |
| `ADUC-FMT-INPUT-003` | 3 | Input byte limit exceeded |
| `ADUC-FMT-INPUT-004` | 3 | JSON node limit exceeded |
| `ADUC-FMT-INPUT-005` | 3 | JSON depth limit exceeded |
| `ADUC-FMT-INPUT-006` | 3 | Non-JSON or non-finite numeric value |
| `ADUC-FMT-INPUT-007` | 3 | Input is not strict UTF-8 |
| `ADUC-FMT-VALIDATION-001` | 1 | Input contract is blocked by full-Core validation |
| `ADUC-FMT-VALIDATION-002` | 1 | Formatted output is blocked by full-Core validation |
| `ADUC-FMT-PRESERVE-001` | 1 | Complete JSON value or array order changed |
| `ADUC-FMT-OUTPUT-001` | 1 or 3 | Output path cannot be used or written |
| `ADUC-FMT-OUTPUT-002` | 3 | Destination exists without `--force` |
| `ADUC-FMT-OUTPUT-003` | 3 | Input and output paths are identical |
| `ADUC-FMT-OUTPUT-004` | 1 | Formatted output byte limit exceeded |
| `ADUC-FMT-INTERNAL-001` | 1 | Unsupported internal JSON value |
| `ADUC-FMT-INTERNAL-002` | 1 | Reference output could not be parsed |

Diagnostics are stable machine-readable objects containing `code`, `path` and `message`. Core validation diagnostics remain available under `inputValidation.diagnosticCodes` and `outputValidation.diagnosticCodes`.
