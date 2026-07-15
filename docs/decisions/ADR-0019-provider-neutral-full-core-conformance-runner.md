# ADR-0019: Provider-neutral full-Core conformance runner

## Status

Accepted.

## Context

ADUC now has a normative ten-block Core model, local Draft 2020-12 schema family, unified full-Core validator/comparator and deterministic complete-contract formatter. External implementers still need a stable way to test their implementations without importing the Python reference engine or treating it as the specification.

The project also needs to avoid an invalid claim: a reference implementation testing itself is useful self-conformance evidence, but it is not independent interoperability proof.

## Decision

ADUC defines a versioned provider-neutral full-Core conformance runner for Core validators, comparators and formatters.

The frozen suite lives under `conformance/full-core/0.1/`. The local runner is `tools/aduc_conformance.py run`. The public adapter protocol is `urn:aduc:full-core-conformance-adapter:0.1`.

## Conformance Classes

The runner recognizes three v0.1 conformance classes:

- `fullCoreValidator`: validates complete ADUC Core contracts and preserves schema, architecture and profile outcomes.
- `fullCoreComparator`: compares two complete Core contracts and preserves `changeType` plus normative `assessment`.
- `fullCoreFormatter`: formats complete Core contracts deterministically without repair, inference or array reordering.

An adapter may support any subset. Unsupported declared capabilities are reported as `unsupported`, not as failures of unsupported features.

## Adapter Contract

The runner invokes adapters as an argv list and never with `shell=True`.

Adapters must support:

- `declareCapabilities`
- `validate <contract.json>`
- `compare <left.json> <right.json>`
- `format <contract.json>`

Each response is a JSON object with:

- `adapterProtocol`
- `operation`
- `implementation`
- `capabilities` for declaration responses
- `report` and integer `exitCode` for operation responses

The contract is language-neutral. Python imports are not part of the adapter boundary.

## Runner Results

The runner uses these case-level results:

- `pass`
- `fail`
- `unsupported`
- `invalidAdapterResponse`
- `timeout`
- `resourceFailure`

The runner preserves Core report outcomes, especially:

- `unknown`
- `contested`
- `prohibited`
- `requiresHumanReview`

These values remain evidence in the conformance report. They are not converted into ordinary success.

## Self-Conformance And Independent Conformance

Reference runs are self-conformance only.

Independent conformance requires all of the following:

- the runner is executed in `--evidence-mode independent`;
- the implementation declares `implementation.kind` as `external`;
- the adapter declares `independenceAttestation.genuineSeparateImplementation: true`;
- the frozen suite passes without fail, timeout, invalid response or resource failure.

The bundled demonstration adapter is structurally separate but does not attest independence. It proves the public adapter boundary, not independent interoperability.

## Determinism

The runner must:

- load cases in sorted identifier order;
- produce stable JSON and text reports;
- omit timestamps and durations from normative report content;
- compare expected behavior by stable codes, outcomes and classifications rather than byte-identical internal reports;
- produce byte-identical normative JSON for repeated identical runs.

## Security And Resource Limits

The runner:

- performs no network access;
- executes adapters through argv lists only;
- applies timeout and stdout limits from the suite manifest;
- rejects invalid JSON and incomplete adapter responses;
- reports `timeout` and `resourceFailure` without exposing tracebacks by default.

## Claim Limits

Passing the runner does not prove:

- factual truth;
- legal permission;
- runtime access control;
- external AI-consumer interoperability;
- first-in-the-world status.

It proves only that an implementation produced expected behavior against a frozen local suite within the declared conformance class boundary.

## Consequences

The Python reference adapter can be tested through the same public boundary as any external implementation. Future SDKs or external implementations can reuse the adapter protocol without depending on Python internals.

The JSON/CSV compiler, review UI, MCP adapter, public registry, extensions and external multi-model proof remain outside this decision.
