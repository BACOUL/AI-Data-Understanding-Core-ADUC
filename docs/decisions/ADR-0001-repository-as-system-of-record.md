# ADR-0001: Repository as the system of record

- Status: accepted
- Date: 2026-07-13

## Context

The project requires durable scope control, traceability, and reliable execution across human and AI contributors.

## Decision

GitHub issues, pull requests, ADRs, versioned specifications, automated tests, the execution ledger, project status, and the single next-action file form the authoritative project record.

Private chat discussions are not authoritative until their decisions are written into the repository.

## Consequences

- Work is reproducible and reviewable.
- Scope changes become explicit.
- Contributors must update repository records as part of completion.
- The process adds modest documentation overhead.
