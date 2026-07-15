# Core Conformance Error Catalogue 0.1

Stable conformance runner diagnostics use the `ADUC-CONF-*` prefix.

| Code | Meaning | Result |
|---|---|---|
| `ADUC-CONF-ADAPTER-TIMEOUT` | Adapter exceeded the manifest timeout. | `timeout` |
| `ADUC-CONF-ADAPTER-EXEC-001` | Adapter process could not be executed. | `resourceFailure` |
| `ADUC-CONF-ADAPTER-RESOURCE-001` | Adapter stdout exceeded the manifest output limit. | `resourceFailure` |
| `ADUC-CONF-ADAPTER-STDERR-001` | Adapter stderr exceeded the advisory output limit. | `resourceFailure` advisory diagnostic |
| `ADUC-CONF-ADAPTER-JSON-001` | Adapter stdout was not valid JSON. | `invalidAdapterResponse` |
| `ADUC-CONF-ADAPTER-SHAPE-001` | Adapter response was missing or not a JSON object. | `invalidAdapterResponse` |
| `ADUC-CONF-ADAPTER-PROTOCOL-001` | Adapter protocol was missing or unsupported. | `invalidAdapterResponse` |
| `ADUC-CONF-ADAPTER-OPERATION-001` | Response operation did not match the request. | `invalidAdapterResponse` |
| `ADUC-CONF-ADAPTER-IMPLEMENTATION-001` | Response did not declare an implementation object. | `invalidAdapterResponse` |
| `ADUC-CONF-ADAPTER-CAPABILITIES-001` | Capability declaration was missing or malformed. | `invalidAdapterResponse` |
| `ADUC-CONF-ADAPTER-REPORT-001` | Operation response did not contain a report object. | `invalidAdapterResponse` |
| `ADUC-CONF-ADAPTER-EXIT-001` | Operation response did not contain an integer exit code. | `invalidAdapterResponse` |
| `ADUC-CONF-CAPABILITY-UNSUPPORTED` | Adapter did not declare the capability required by a case. | `unsupported` |
| `ADUC-CONF-MANIFEST-OPERATION-001` | Suite case declared an unsupported operation. | `fail` |
| `ADUC-CONF-EXPECTED-EXIT-001` | Adapter exit code differed from expected. | `fail` |
| `ADUC-CONF-EXPECTED-OUTCOME-001` | Validation or formatting outcome differed from expected. | `fail` |
| `ADUC-CONF-EXPECTED-VALID-001` | Validation boolean differed from expected. | `fail` |
| `ADUC-CONF-EXPECTED-DIAGNOSTIC-001` | Expected diagnostic code was missing. | `fail` |
| `ADUC-CONF-EXPECTED-OVERALL-001` | Comparison overall result differed from expected. | `fail` |
| `ADUC-CONF-EXPECTED-ASSESSMENT-001` | Comparison overall assessment differed from expected. | `fail` |
| `ADUC-CONF-EXPECTED-ASSESSMENT-002` | Expected change assessment was missing. | `fail` |
| `ADUC-CONF-EXPECTED-CHANGE-001` | Expected comparison change code was missing. | `fail` |
| `ADUC-CONF-EXPECTED-FORMATTED-001` | Formatter `formatted` result differed from expected. | `fail` |
| `ADUC-CONF-EXPECTED-PRESERVE-001` | `unknown`, `contested`, `prohibited` or `requiresHumanReview` was not preserved. | `fail` |

These diagnostics describe conformance runner behavior only. They do not replace Core validation, comparison or formatting diagnostics.
