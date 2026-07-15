# ADR-0019 Cross-Cutting Review

## AI-first

The conformance runner exposes a machine-readable adapter contract and stable JSON report. Implementations can be exercised without a human-specific UI and without provider-specific APIs.

## Human review

The suite requires preservation of `requiresHumanReview`; it is not converted to `pass` semantics. Text reports remain readable for maintainers and reviewers.

## Privacy

The runner uses only local fixtures and adapter processes. It performs no network requests and sends no contract content to remote services.

## Security

Adapters are invoked through argv lists with `shell=False`. The runner applies timeout and output-size limits, rejects invalid JSON and does not expose tracebacks in normal reports.

## Conformance

The suite is versioned, frozen and manifest-driven. It tests validation, comparison and formatting through the same public boundary used by the reference and non-reference adapters.

## Determinism

Cases are sorted by identifier. Reports exclude timestamps and durations. Repeated reference runs produce byte-identical normative JSON.

## Claim Limits

Reference runs are self-conformance only. Independent conformance requires external implementation kind, explicit independence attestation and a passing suite. This is still not a multi-AI interoperability proof.
