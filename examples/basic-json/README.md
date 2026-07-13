# Basic JSON — River R42

This directory contains the first complete full-Core example requested by the project plan.

## Files

- `river-r42.data.json`: the original unchanged source data;
- `river-r42.aduc.json`: the accompanying ADUC Core draft contract.

## What the raw data does not explain

The source alone does not define:

- what `flow` represents;
- the unit of the value;
- the meaning of `quality = 2`;
- the observation time semantics;
- the identity scheme for `station`;
- the producing organization and method;
- the expected measurement uncertainty;
- the permitted purposes.

## What the contract adds

The contract describes all ten candidate Core blocks:

```text
aduc
resource
structure
semantics
identity
context
provenance
uncertainty
relations
policy
```

## Important draft limitation

`river-r42.aduc.json` is an informative full-Core draft example. The repository does not yet contain the final `schema/aduc-core.schema.json`; therefore this example MUST NOT be described as validated full-Core conformance.

The existing validator currently validates the narrower semantic-mapping profile. Full-Core schema and validator migration are planned in `docs/roadmap/MASTER_PLAN.md`.

## Expected interpretation

A compatible consumer should be able to determine that:

- `station` is a hydrometric-station identifier;
- `flow` represents water discharge;
- the value is expressed in cubic metres per second;
- `quality = 2` means provisional quality;
- `timestamp` is observation time in UTC;
- the source is an official sensor network;
- the measurement has a declared relative error and confidence level;
- the declared public uses include research and flood-risk analysis.

The consumer must preserve the difference between reviewed and canonical mappings.
