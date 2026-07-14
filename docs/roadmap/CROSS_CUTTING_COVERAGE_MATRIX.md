# Cross-Cutting Coverage Matrix

- Status: mandatory program-control document
- Applies to: every normative, implementation, product, website, release and ecosystem milestone
- Rule: a missing assessment is not equivalent to `notApplicable`

## Purpose

ADUC cannot rely on maintainers remembering every horizontal requirement during each technical milestone. This matrix turns those requirements into explicit planning, test and evidence obligations.

Every milestone issue and pull request must review the applicable rows below and record one of these statuses:

```text
notStarted
planned
inProgress
implemented
verified
deferredWithReason
notApplicableWithReason
```

A phase may close only when each applicable row is `verified`, or when an accepted decision records why it is deferred.

## Required fields for milestone assessments

Each applicable requirement must identify:

| Field | Required content |
|---|---|
| Requirement | The exact cross-cutting concern |
| Principle | The design rule it protects |
| Phase/track | Where it must be addressed |
| Deliverable | The concrete artifact or behavior |
| Tests | Automated, manual, adversarial or independent checks |
| Evidence | Report, audit, fixture, metric, review or release artifact |
| Status | One controlled status value |
| Responsible role | Maintainer, implementer, reviewer, security reviewer or external assessor |
| Reassessment trigger | Version, new interface, hosted service, new data class or release gate |

## Core matrix

| ID | Requirement | Principle | First mandatory phase | Minimum deliverable | Minimum test/evidence | Reassessment trigger |
|---|---|---|---|---|---|---|
| X-001 | Provider-neutral machine-readable contracts and reports | AI-first | Phase 1 | Stable JSON schemas, reports and codes | Determinism and cross-implementation fixtures | Any report/schema version |
| X-002 | Human-readable diagnostics and remediation | Human-first | Phase 2 | Text reports and documented fixes | Independent developer usability test | CLI/UI wording change |
| X-003 | Explicit review of consequential ambiguity | Review-first | Phase 2 | `requiresHumanReview` behavior | Positive and negative review-required fixtures | New inference or evaluator |
| X-004 | Local processing by default | Privacy by design | Phase 2 | Offline validator/comparator | Network-denial tests | Hosted or model-backed feature |
| X-005 | No silent upload, retention, telemetry or training | Privacy by default | Phase 3 | Explicit consent and retention design | Privacy review and data-flow test | Any upload, analytics or model integration |
| X-006 | Data minimization and redaction | Privacy by design | Phase 3 | Sensitive-data handling policy | Redaction and logging tests | New data class or sector |
| X-007 | Contract and description content treated as untrusted | Security by design | Phase 2 | Input validation and escaping rules | Malicious JSON and injection fixtures | New parser, UI or AI projection |
| X-008 | Resource, depth, graph and cycle limits | Failure-safe | Phase 2 | Documented safe limits | Fuzzing, deep JSON and cyclic graph tests | Limit or parser change |
| X-009 | No unapproved remote resolution | Supply-chain safety | Phase 1 | Local schema/vocabulary resolution | Offline CI | New external reference type |
| X-010 | Dependency inventory and vulnerability handling | Supply-chain security | Phase 2 | Dependency policy and vulnerability process | Dependency scan | Package or dependency release |
| X-011 | SBOM, signed or attestable packages and build provenance | Release integrity | Phase 2 | Release integrity plan | Reproducible build/release evidence | Public package publication |
| X-012 | Preserve unknown, unsupported and indeterminate states | Unknown-safe | Phase 0 | Normative state model | Counterexamples and comparator tests | Any new profile or extension |
| X-013 | Preserve conflict, deprecation and prohibition separately | Epistemic safety | Phase 0 | Qualified assertion states | Lifecycle and policy tests | New evaluator or migration |
| X-014 | No unsafe identity merge or semantic promotion | Conservative inference | Phase 0 | Identity/authority rules | Negative merge/promotion fixtures | Compiler or review workflow |
| X-015 | Accessibility target WCAG 2.2 AA | Accessibility by design | Phase 4, website earlier | Accessible website and review UI | Keyboard, contrast, focus and screen-reader audit | Material UI change |
| X-016 | Unicode, locale, timezone, number and unit support | Internationalization by design | Phase 1 | Language-independent identifiers and locale rules | Multilingual and locale fixtures | New locale or translation |
| X-017 | Versioned translations preserve normative meaning | Internationalization | Phase 4 | Translation/version policy | Terminology review | Translation release |
| X-018 | Stable versioning, compatibility, migration and deprecation | Compatibility by design | Phase 1 | Version policy and migration tools | Cross-version fixtures | Any public interface change |
| X-019 | Normative requirement-to-test traceability | Testability by design | Phase 1 | Requirement/test matrix | Coverage audit | ADR or specification change |
| X-020 | Separate conformance classes | Independent conformance | Phase 2 | Contract/producer/validator/comparator/compiler/consumer classes | Conformance suite | New implementation class |
| X-021 | Independent implementation evidence | Standards maturity | Phase 5 | Independent implementation/report | Published implementation result | Candidate Specification gate |
| X-022 | Deterministic offline baseline | Reliability | Phase 2 | Non-LLM reference operation | Repeated byte-identical reports | Engine or dependency change |
| X-023 | Performance, memory and latency budgets | Reliability and sustainability | Phase 2 | Measured budgets | Benchmark report | New algorithm or input limit |
| X-024 | Privacy-preserving observability | Observability by design | Hosted phase | Log/metric data classification | Log inspection and retention test | New telemetry or service |
| X-025 | Service objectives, incident and recovery process | Operational reliability | Hosted phase | SLO and incident plan | Recovery exercise | Production launch/change |
| X-026 | Cost and model-call accounting | Sustainability and viability | Phase 3 | Cost metrics | Cost benchmark | New provider/model workflow |
| X-027 | Crawlable, versioned public documentation | Discoverability | Phase 1 | Stable pages, sitemap and canonical metadata | Website audit | New release/site structure |
| X-028 | Problem-oriented SEO content | SEO | Phase 2 | Pages targeting real interoperability problems | Search-console and crawl checks | Content/release cycle |
| X-029 | Explicit answer-oriented definitions and evidence | AEO | Phase 2 | FAQ, definitions and cited technical pages | Query-set review | Major positioning change |
| X-030 | Generative-system discoverability measured, not promised | GEO | Phase 2 | Stable raw artifacts, clear claims and query set | Dated multi-engine citation observations | Model/search ecosystem change |
| X-031 | Developer installation and first-use experience | Developer experience | Phase 2 | “Try in 5 minutes”, examples and actionable errors | Independent install test | Package/CLI change |
| X-032 | Package distribution and compatibility policy | Distribution | Phase 2 | PyPI/npm/release plan | Clean-environment install tests | Package release |
| X-033 | Pilots use explicit success and stop criteria | Adoption evidence | Phase 5 | Pilot protocol | Pilot report | New sector/use case |
| X-034 | Manual-vs-assisted and with-vs-without benchmark | Value evidence | Phase 5 | Frozen benchmark | Timing, correctness and review-tax report | Compiler/inference change |
| X-035 | Dated prior-art watch | Novelty discipline | Phase 0 | Standards/papers/repos/patents matrix | Periodic review record | Announcement or stable release |
| X-036 | Precise novelty claim and non-claim boundary | First-world claim safety | Phase 5 | Claim dossier | Independent specialist review | Public novelty statement |
| X-037 | Two independent AI consumers and deterministic baseline | Interoperability proof | Phase 5 | Frozen full-Core package | Raw hashes and normalized results | Model/provider/version change |
| X-038 | Naming and trademark research | Identity protection | Phase 0 | Name clearance record | Professional search before freeze | Geography/class expansion |
| X-039 | Code, specification, test and example licenses | Open-standard governance | Phase 1 | Explicit license mapping | License audit | New dependency/contributor |
| X-040 | Patent policy | Implementer confidence | Candidate Specification | Published patent policy | Legal/governance review | Governance transition |
| X-041 | Contribution, decision, objection and appeal process | Governance | Phase 2 | Governance process | Process review | Multi-maintainer/adoption threshold |
| X-042 | Extension namespace and registration policy | Ecosystem safety | Phase 6 | Registry/governance rules | Collision and compatibility tests | New official/community extension |
| X-043 | Legal claims remain bounded | Legal safety | All phases | Disclaimers and policy boundaries | Legal wording review | Regulatory/use-case change |
| X-044 | Sector-specific obligations are extensions or applications, not silent Core rules | Architectural integrity | Phase 6 | Extension boundary decision | Architecture review | New regulated sector |
| X-045 | Environmental and maintenance cost is measured | Sustainability | Phase 3 | Resource/cost report | Benchmark | Scale or hosting change |

## Milestone review template

Every important PR must include:

```text
## Cross-cutting impact review

- AI-first:
- Human review and contestability:
- Privacy by design/default:
- Security and supply chain:
- Unknown-safe/failure-safe behavior:
- Accessibility:
- Internationalization:
- Versioning and migration:
- Performance/reliability/cost:
- Independent conformance:
- Documentation and developer experience:
- SEO/AEO/GEO:
- Prior art and public claims:
- Legal/licensing/governance:
- Tests and evidence:

Deferred or not applicable items must include a reason and reassessment trigger.
```

## Phase-closing audit

Before a phase is closed:

1. list all matrix rows applicable to the phase;
2. link each row to its deliverable and evidence;
3. record unresolved risks and accepted deferrals;
4. verify public documentation and claims against the evidence;
5. confirm that `NEXT_ACTION.md` contains exactly one authorized next task;
6. append the result to the execution ledger.

## Current priority

The matrix does not change the active technical task. The current task remains migration from the standalone semantic-mapping profile into complete Core contracts.
