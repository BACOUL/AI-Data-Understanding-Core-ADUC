# ADUC Multi-Model Conformance Protocol 0.1

- Status: Gate 6 candidate
- Date: 2026-07-13
- Issue: #19
- Automated provider calls: prohibited in CI

## 1. Purpose

This protocol defines a reproducible test for determining whether two independent AI consumers interpret the same ADUC artifacts compatibly without provider-specific hidden semantic mappings.

The protocol separates:

1. a frozen input package;
2. a raw model response;
3. a normalized result document;
4. a deterministic local evaluation.

Publishing a schema or two illustrative result files does not prove multi-model interoperability. The claim becomes eligible only after qualifying external runs exist.

## 2. Falsifiable claim

The tested claim is:

> Given the same frozen source descriptions, source samples, ADUC profiles and provider-neutral instructions, two independent AI consumers preserve the same semantic targets, mapping relations, authority states, blocked conditions and unevaluated dimensions without using hidden mappings.

The claim fails when either consumer:

- upgrades an inferred mapping to reviewed or canonical;
- upgrades a non-exact relation to exact equivalence;
- automatically uses a contested mapping;
- joins same-looking local names whose semantic targets differ;
- invents unit, time or entity alignment absent from the package;
- omits required evidence references;
- requires provider-specific semantic instructions;
- returns a result that cannot be normalized to the common schema.

## 3. Frozen conformance package

A package directory contains:

```text
instructions.md
cases.json
result-template.json
manifest.json
```

`manifest.json` inventories every package file except itself with:

- relative path;
- byte size;
- SHA-256 digest.

The package digest is computed from the sorted inventory using:

```text
relative-path NUL sha256-digest LF
```

and then SHA-256 hashing the concatenated UTF-8 bytes.

A tester must verify the manifest before submitting the package to a model.

## 4. Required scenarios

The official package contains six scenarios.

### 4.1 `exact-different-names`

Two differently named local fields share the same target. One mapping is reviewed and the other canonical; both relations are exact.

Expected classification: `comparable`.

### 4.2 `inferred-candidate`

One exact mapping is inferred and one is reviewed.

Expected classification: `candidate`.

### 4.3 `close-match-candidate`

The semantic target is shared, but one relation is `skos:closeMatch`.

Expected classification: `candidate`.

### 4.4 `contested-blocked`

One mapping is contested.

Expected classification: `blocked`.

### 4.5 `same-name-different-targets`

The local field names are identical but the semantic targets differ.

Expected classification: `unmapped`.

### 4.6 `missing-dimensions`

The semantic target is shared and exact, but no unit, time or entity contract is supplied.

Expected classification: `comparable`, with unit, time and entity all `notEvaluated`.

## 5. Provider-neutral instructions

The model receives only the verified package contents. Instructions must:

- identify the task as classification and preservation, not free-form ontology inference;
- forbid browsing, external tools, remembered private mappings and hidden aliases;
- prohibit chain-of-thought disclosure;
- require concise result records and evidence references;
- state that local-name similarity is not evidence;
- state that missing dimensions remain `notEvaluated`;
- require the raw response to be retained unchanged.

The same instruction bytes must be supplied to every qualifying consumer.

## 6. Clean execution environment

A qualifying run must use:

- a fresh conversation or process;
- no prior project memory supplied to the model;
- no browsing or external retrieval;
- no provider-specific examples beyond the package;
- deterministic or lowest-available sampling settings where supported;
- the same package digest;
- no manual correction of the raw model output.

Any deviation is recorded and makes the run non-qualifying unless the protocol explicitly permits it.

## 7. Raw output

The unmodified model response is stored as a separate file. Its SHA-256 digest and relative path are recorded in the normalized result.

Raw output may be text or JSON. It must not be overwritten after normalization.

The normalized result is an audit artifact derived from the raw response. It is not permitted to repair a semantically wrong answer silently. Any human normalization decision must be recorded in `normalizationNotes`.

## 8. Normalized result

A result conforming to:

```text
schema/model-conformance-result.schema.json
```

contains:

- run identity and kind;
- provider, model, version and execution time;
- exact package digest;
- model parameters where known;
- declaration that no external context was used;
- raw-output path and digest;
- one result for every required scenario;
- preserved assertion IDs, local references, targets, statuses and relations;
- classification and reasons;
- unit, time and entity dimension states;
- evidence references;
- optional normalization notes.

## 9. Run kinds

### `illustrative`

Created by project maintainers or fixtures to demonstrate tooling. It never counts toward interoperability proof.

### `external`

Produced from an actual independent AI consumer execution under this protocol. It may qualify when all metadata and evidence rules pass.

A filename, provider name or maintainer claim cannot turn an illustrative result into an external run. The `kind` field and evidence must be truthful.

## 10. Deterministic evaluation

The local harness performs:

1. package inventory verification;
2. package digest verification;
3. result-schema validation;
4. scenario-ID completeness and uniqueness checks;
5. package-digest equality across results;
6. raw-output digest verification when files are available;
7. comparison with the official expected result set;
8. pairwise semantic agreement comparison;
9. qualification analysis;
10. machine-readable report generation.

Run metadata is excluded from semantic-agreement comparison. Scenario records are compared deterministically after sorting by scenario ID.

## 11. Pass rules

A result passes the expected semantics only when all six scenarios match the official expected records for:

- classification;
- semantic targets;
- statuses;
- relations;
- local references;
- blocked/candidate reasons where normative;
- `notEvaluated` dimensions.

A pair of results agrees only when their normalized semantic scenario records are identical.

## 12. Qualification rules

ADUC multi-model interoperability is **not proven** unless the repository contains at least two runs that:

1. are marked `external`;
2. come from distinct independent providers or independently implemented consumers;
3. use the same verified package digest;
4. record complete model and execution metadata;
5. declare `externalContextUsed: false`;
6. reference raw outputs whose digests verify;
7. pass the result schema and semantic expected set;
8. agree with each other after normalization;
9. disclose normalization notes;
10. are reproducible by an independent tester.

The evaluation report must contain:

```json
{
  "qualifyingExternalRuns": 0,
  "interoperabilityProven": false
}
```

until these rules are met.

## 13. Distinct-consumer rule

Two model names from the same provider may be informative but do not automatically constitute independent providers.

The report records both:

- distinct provider count;
- distinct implementation identity count when declared.

For the initial public claim, two distinct providers or independently maintained open implementations are required.

## 14. Expected-result isolation

The expected-result file is used by the local evaluator and must not be supplied to the tested model.

The frozen model package contains cases and an empty result template, not the expected answers.

## 15. Deterministic tools versus probabilistic models

The ADUC schema validator, comparator, package verifier and evaluator are deterministic reference tools.

A model consumer may be probabilistic. Conformance therefore records:

- exact model/version when available;
- parameters;
- execution time;
- raw output;
- repeat number.

A future robustness profile may require multiple repetitions. Version 0.1 requires at least one qualifying run per independent consumer and reports repeat count.

## 16. Security and privacy

The official package contains synthetic data only.

Testers must not add credentials, personal data or confidential source material. Raw outputs must be reviewed for accidental secret disclosure before public commit without modifying their semantic content.

## 17. Prohibited claims

Before qualifying evidence exists, documentation may state:

- the protocol is implemented;
- illustrative results pass the harness;
- deterministic tools agree.

It must not state:

- multiple AI providers are interoperable;
- ADUC is an industry standard;
- the test proves general understanding of arbitrary data;
- the test proves unit, time or entity interoperability.

## 18. Completion criteria

Protocol preparation passes when:

- the package is self-contained and hash-verifiable;
- all six scenarios are present;
- the result schema is machine-validatable;
- the harness detects tampering, invalid results and semantic disagreement;
- illustrative runs are explicitly non-qualifying;
- CI performs no provider call;
- an independent tester can produce and evaluate external results manually.

Gate 6 evidence passes only after two qualifying external runs are committed and evaluated successfully.
