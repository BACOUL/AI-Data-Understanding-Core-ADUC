# ADUC Adoption and Value Validation

- Status: official cross-cutting validation plan
- Date: 2026-07-13
- Applies to: compiler, review workflow, interoperability demonstrations, and adoption tooling
- Does not replace: Core conformance, source binding, schema validation, or authority verification

## 1. Purpose

ADUC succeeds only if it reduces the cost of making data understandable to AI systems while preserving or improving semantic correctness.

Technical conformance alone is insufficient. The project must prove that:

1. creating and reviewing an ADUC contract is faster than producing an equivalent manual mapping;
2. ADUC reduces model-specific semantic instructions;
3. independent consumers interpret the same contract more consistently;
4. uncertainty, conflict, and unknown fields remain visible;
5. the review burden does not exceed the value created by automatic inference.

This document defines the evidence required before the compiler, review interface, and multi-model claims may be described as successful.

## 2. Standard, tools, and products

The project is separated into three layers:

```text
ADUC open specification
        ↓
reference tools
validator · compiler · review UI · SDK · conformance harness
        ↓
optional commercial services
hosting · enterprise connectors · private registry · monitoring · support
```

The open specification must remain usable without a hosted ADUC service. Reference tools are necessary for adoption, but they must not become a proprietary dependency of the Core.

## 3. Inference evidence modes

Every compiler run must declare one of the following modes and the evidence actually used.

### 3.1 `structure-only`

Available evidence may include:

- field names;
- primitive types;
- nesting;
- declared schema constraints;
- nullability and cardinality.

This mode may propose candidates, but ambiguous business meaning must remain unknown or low-support inferred information.

### 3.2 `sample-assisted`

Adds bounded source samples and may inspect:

- value distributions;
- formats and ranges;
- repeated patterns;
- correlations between fields;
- missing-value behavior.

Sample values may improve a proposal but cannot establish publisher authority or universal business meaning.

### 3.3 `documentation-assisted`

Adds documentation such as:

- OpenAPI descriptions;
- JSON Schema annotations;
- Croissant metadata;
- data dictionaries;
- README files;
- API documentation;
- SQL comments or catalog descriptions.

The compiler must retain references or digests for the documentation used as evidence.

### 3.4 `publisher-assisted`

Adds material supplied or approved by the source publisher.

Publisher material may support a stronger proposal, but compiler output remains `inferred` until an accountable review, verification procedure, or source-authority publication creates a new immutable assertion with the appropriate authority status.

### 3.5 Required inference record

Each inferred proposal must record at least:

```text
inference mode
method identifier and version
evidence references
source binding
candidate semantic target
mapping relation
support or confidence output
unresolved alternatives
```

Missing evidence must never be reconstructed or implied after the run.

## 4. Confidence and calibration

A model saying that it is "90% confident" is not evidence that the proposal is correct 90% of the time.

Rules:

1. every numeric value must identify its method and version;
2. values from different methods are not directly comparable unless a calibration study proves comparability;
3. a numeric output must not be called a calibrated probability without a labeled evaluation set and a published calibration report;
4. uncalibrated values must be presented as method-specific support or ranking scores;
5. high scores never change authority status;
6. review thresholds are deployment policy, not universal Core truth.

A review policy may use a threshold such as `0.80`, but it must identify the method to which the threshold applies and must still surface contradictions, contested mappings, and policy-defined high-risk fields.

## 5. Review-tax gate

### 5.1 Definition

The review tax is the human effort required to turn compiler output into an acceptable portable contract.

Measure:

```text
assisted total time
= compiler setup
+ generation wait handled by the user
+ review time
+ correction time
+ unresolved-field handling
+ final validation
```

Compare it with:

```text
manual total time
= source inspection
+ documentation reading
+ manual mapping
+ conversion rules
+ validation
+ equivalent portable documentation
```

The baseline must produce an equivalent documented result. Comparing ADUC with an undocumented throwaway script is invalid unless the benchmark task explicitly measures throwaway integration work.

### 5.2 Required metrics

For every benchmark task, record:

- total elapsed human time;
- active human interaction time;
- number of fields;
- proposals accepted without change;
- proposals edited;
- proposals rejected;
- unknown fields remaining;
- false mappings;
- critical false mappings;
- review actions per field;
- final semantic correctness;
- participant experience level.

### 5.3 Initial alpha targets

These are project targets, not requirements imposed on every ADUC implementation:

1. median assisted human time is at least 30% lower than the equivalent manual baseline;
2. final mapping correctness is not lower than the manual baseline;
3. unresolved and low-support mappings are surfaced rather than silently accepted;
4. no critical false mapping is silently accepted in the reference benchmark;
5. results are reported by inference mode, source type, and participant experience.

The targets may be revised only through a documented decision using collected evidence.

### 5.4 Failure condition

The compiler/review approach fails its adoption gate when assisted work is not materially faster than the equivalent manual workflow, or when time savings depend on hiding unresolved or incorrect mappings.

A failed gate requires one of:

- improve inference evidence or calibration;
- reduce the scope of automatic inference;
- redesign the review workflow;
- narrow supported source types;
- stop or pivot the compiler feature.

## 6. With-ADUC versus without-ADUC evaluation

The interoperability demonstration must compare two controlled conditions.

### Condition A — raw source baseline

Consumers receive:

- the original frozen data;
- the task instruction;
- no ADUC contract;
- no hidden semantic mapping;
- no provider-specific explanatory prompt beyond the common task instruction.

### Condition B — ADUC-assisted

Consumers receive:

- the same frozen data;
- the same task instruction;
- the corresponding ADUC contract;
- no hidden provider-specific semantic mapping.

### Required measurements

- task correctness;
- semantic-field identification accuracy;
- unit-conversion accuracy;
- temporal-alignment accuracy;
- entity-resolution restraint and accuracy;
- preservation of unknown, inferred, contested, and deprecated states;
- hallucinated facts or relationships;
- agreement between independent consumers;
- model-specific instruction tokens or rules required;
- integration and execution time.

The demonstration supports an ADUC value claim only when the ADUC-assisted condition improves correctness or consistency, or materially reduces model-specific instructions, without hiding uncertainty.

## 7. Multi-model qualification

A qualifying interoperability result requires:

- frozen and hashed inputs;
- at least two independent providers or implementations;
- raw outputs and normalized outputs;
- deterministic evaluation;
- disclosure of model versions and parameters;
- no undeclared external context or private mapping;
- publication of disagreements as well as successes.

Identical answers alone do not prove that ADUC caused the agreement. The baseline comparison is mandatory.

## 8. MCP integration boundary

MCP is a potential adoption channel, not a Core dependency.

A future adapter may expose:

```text
MCP resource or tool
+ associated ADUC contract
= technical access plus portable semantic description
```

Rules:

- ADUC contracts must remain usable without MCP;
- the Core must not copy MCP transport or tool-discovery concepts;
- an MCP adapter starts only after the relevant Core contract is stable and conformance-tested;
- MCP adoption must be measured against direct non-MCP consumption rather than assumed to create value.

## 9. Required future artifacts

Before compiler implementation is declared complete:

```text
docs/evaluation/INFERENCE_EVIDENCE_PROTOCOL.md
docs/evaluation/MANUAL_VS_ASSISTED_BENCHMARK.md
docs/evaluation/CONFIDENCE_CALIBRATION.md
examples/evaluation/
```

Before the review interface is declared complete:

```text
docs/evaluation/REVIEW_TAX_REPORT.md
```

Before multi-model interoperability is claimed:

```text
docs/evaluation/WITH_WITHOUT_ADUC_PROTOCOL.md
examples/conformance/external-runs/
public deterministic evaluation report
```

Before an MCP integration is called official:

```text
spec/integrations/MCP_ADAPTER_PROFILE.md
adapter conformance fixtures
```

## 10. Sequencing

This plan does not interrupt the current Core-design order.

```text
now: source-description and immutable source binding
then: units, time, identity, remaining Core decisions
then: full-Core schema and examples
before compiler: inference evidence and benchmark protocols
compiler + review UI: measured against manual baseline
multi-model proof: with/without ADUC comparison
later: optional MCP adapter
```

## 11. Stop and pivot rules

The project must narrow, revise, or stop a tool or claim when:

- review cost cancels the time saved by inference;
- numeric confidence is not empirically calibrated but is presented as probability;
- ADUC does not improve or preserve correctness against the raw-source baseline;
- agreement requires provider-specific hidden mappings;
- adoption requires a proprietary hosted service;
- MCP or another integration begins to dictate the Core architecture;
- uncertainty is silently converted into authority.

## 12. Completion criterion

This validation plan is satisfied only when a third party can reproduce the benchmarks from committed inputs and reports, verify the calculations, and explain both successful and failed cases without private guidance.