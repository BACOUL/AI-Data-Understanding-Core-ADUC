# ADR-0018 cross-cutting impact review

- Milestone: deterministic complete-contract formatter
- Issue / PR: #60 / #64
- Phase / track: Phase 2, Track A with Track B and C safeguards
- Status: verified on the reviewed PR head
- Responsible role: maintainer / implementer

| Concern | Status | Deliverable and evidence | Reassessment trigger |
|---|---|---|---|
| AI-first and provider neutrality | verified | Stable JSON/text reports, deterministic UTF-8 output and no model/provider dependency | Report or formatting-profile version change |
| Human review and contestability | verified | Exit code 2 and `formattedRequiresHumanReview` preserve accepted review outcomes before and after formatting | New validation outcome or repair behavior |
| Privacy by design/default | verified | Local file processing; no upload, telemetry, retention or remote resolution | Hosted formatter or telemetry |
| Security and untrusted input | verified | Duplicate-key, invalid UTF-8/JSON, non-finite number, size, depth, node and overwrite-race rejection | Parser, limit or file-write change |
| Unknown-safe and failure-safe | verified | Invalid input is blocked without output or silent repair; policy, conflict and uncertainty data are preserved | New inference or repair feature |
| Accessibility | notApplicableWithReason | CLI and machine-readable artifacts add no visual interaction; public website work remains isolated in PR #63 | Graphical formatter UI |
| Internationalization | verified | UTF-8 output, direct Unicode preservation and exact-decimal rendering independent of locale | Locale-aware presentation layer |
| Versioning and migration | verified | ADR-0018 and formatting spec version output and report semantics | Any ordering, number or report change |
| Performance and reliability | verified | Bounded input bytes, depth, node count and output bytes; atomic writes and idempotence tests | Limit or algorithm change |
| Independent conformance | deferredWithReason | Reference behavior and fixtures are frozen; independent proof requires the next conformance-runner milestone and a separate implementation | Conformance runner or external implementation |
| Documentation and developer experience | verified | ADR, specification, error catalogue, fixtures, CLI commands and README section | CLI or installation change |
| SEO/AEO/GEO | deferredWithReason | No website claim is changed in this engine PR; site alignment remains in draft PR #63 | Website PR or public release |
| Prior art and public claims | verified | The formatter is described as an ADUC profile, not RFC 8785 and not proof of a world-first standard | Public novelty claim |
| Legal, licensing and governance | verified | No permission, authority or legal decision is inferred; existing repository licenses and ADR process apply | Package release or governance change |
| Tests and evidence | verified | 13 focused tests, frozen fixtures, full official suites, double-format byte comparison, Core revalidation and Vercel success | Engine, schema or formatter change |

## Deferred boundaries

The formatter does not close the Phase 2 independent-conformance, SDK, package-publication or installation-usability gates. It does not authorize the compiler, review UI or external interoperability claims.
