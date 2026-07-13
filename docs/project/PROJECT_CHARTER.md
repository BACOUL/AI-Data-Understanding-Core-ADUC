# Project Charter

## Mission

Create an open, model-independent contract allowing a data source to describe its structure, semantics, identity, context, provenance, uncertainty, relations, and usage policy to AI systems.

## Initial user problem

Today, data meaning is repeatedly encoded in prompts, ETL pipelines, proprietary connectors, application code, and undocumented domain knowledge. The same source may need to be mapped again for each model or application.

## Initial value proposition

Describe a source semantically once, validate the contract, and reuse it across multiple compatible models and applications.

## v0.1 scope

The first release supports only:

- JSON and CSV sources;
- tabular or record-oriented structures;
- primitive field types;
- concepts and units;
- entity identifiers;
- temporal context;
- elementary provenance;
- uncertainty and mapping status;
- basic usage policy;
- comparison of two described sources.

## Primary proof

Two incompatible sources are accompanied by contracts. Two different AI systems independently identify the same comparable fields, unit conversion, temporal alignment, and unresolved identity uncertainty.

## Success condition

The project succeeds at v0.1 only if the demonstration is reproducible without provider-specific hidden mappings.
