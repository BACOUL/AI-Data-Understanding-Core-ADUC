# ADUC Source and Extension Horizons

- Status: proposed authoritative scope clarification
- Date: 2026-07-15
- Issue: #66
- Relationship: clarifies ADR-0004 and the long-term source scope without changing the Core object model

## 1. One project direction

ADUC is the broader, model-independent AI Data Understanding Core defined by ADR-0004 and `spec/ADUC_CORE_SPEC_0_1.md`.

Its long-term mission is:

> Allow any data resource accompanied by an ADUC contract to make its structure, meaning, identity, context, provenance, uncertainty, relations and conditions of use explicit to compatible AI systems, agents, analytics and applications.

The standalone semantic-mapping profile defined during the first experimental gates remains a supported and useful subset of the `semantics` module. It is not the complete project and does not limit the long-term mission.

## 2. Three horizons that must not be confused

### Horizon A — Long-term Core mission

The Core is source-category-independent. Its ten reserved modules define portable binding, qualification, lifecycle, references and deterministic consumer behavior.

The long-term mission is not limited to JSON or CSV. It is intended to support data resources including datasets, APIs, databases, events, sensor streams, documents, media-derived observations, scientific resources and agent memory through source-specific descriptions and extensions.

This horizon is a design direction, not a claim that every source category is implemented today.

### Horizon B — Initial proof boundary

The first reproducible product and interoperability proof remains deliberately limited to:

- JSON and CSV;
- tabular or record-oriented sources;
- deterministic local field references;
- concepts and units;
- temporal context;
- entity identifiers and cautious identity decisions;
- provenance;
- uncertainty and quality;
- relations;
- declared conditions of use;
- comparison of two described sources;
- at least two independent consumers without hidden provider-specific mappings.

JSON and CSV are the first proof boundary because they permit a bounded, reproducible and independently testable implementation. They are not the permanent limit of ADUC.

### Horizon C — Future source profiles and extensions

Future work may add the following gated families after the complete Core passes its value and interoperability requirements:

1. **Dataset Profile**
   - JSON, CSV and dataset packages;
   - reuse Croissant, CSVW, JSON Schema and relevant catalog vocabularies;
   - never duplicate complete dataset-description models.

2. **API Profile**
   - request and response payload meaning;
   - operation context and result interpretation;
   - reuse OpenAPI and JSON Schema;
   - ADUC does not replace API discovery, invocation or authentication.

3. **Database / SQL Profile**
   - schemas, tables, views, columns, keys and stable queryable objects;
   - business meanings, identities, units, lineage and constraints linked to exact database versions;
   - reuse database catalogs, SQL metadata, dbt or other maintained semantic descriptions where applicable;
   - no claim that introspection alone discovers hidden business truth.

4. **Live Event and Sensor Profile**
   - events, observations, sampling, freshness and stream context;
   - reuse CloudEvents and SOSA/SSN where applicable;
   - preserve temporal uncertainty, missingness and source identity.

5. **Document and Media Profile**
   - PDF, text, image, audio and video resources;
   - bind extracted entities, observations and regions to exact source bytes and extraction provenance;
   - preserve model version, evidence, uncertainty and review requirements;
   - ADUC does not itself perform universal perception or document understanding.

6. **Scientific Data Profile**
   - experimental variables, procedures, units, uncertainty, derivations and reproducibility evidence;
   - reuse maintained scientific vocabularies rather than creating one universal scientific ontology.

7. **Agent Memory Profile**
   - portable entities, observations, assertions and relations used by agents;
   - preserve provenance, temporal validity, authority and policy;
   - exclude private chain-of-thought and provider-specific hidden memory.

8. **Situation & Action Extension**
   - situations, hypotheses, possible developments, risks, actions, constraints and outcomes;
   - remain separate from the Core;
   - never treat the data model alone as authorization for consequential autonomous action.

## 3. Structural-description boundary

The ADUC `structure` module is a stable interoperability index and binding layer for the objects referenced by the other Core modules.

It may carry the minimum normalized information needed to:

- identify records, fields and source paths;
- bind them to an exact resource or version;
- provide stable internal references;
- expose primitive shape and key information required for deterministic validation and comparison;
- reference the external structural description that owns the complete source model.

It must not become a renamed replacement for JSON Schema, Croissant, CSVW, OpenAPI, SQL catalogs or other maintained source-description standards.

When an established external description exists:

```text
external source description
        +
ADUC stable structural bindings
        ↓
semantics · identity · context · provenance · uncertainty · relations · policy
```

ADUC owns the binding, qualification and safe cross-module behavior. The external standard retains authority for its complete structural model.

## 4. Automatic understanding boundary

ADUC may support automated inspection and inference, but it must never claim that opaque data can reveal unavailable business meaning with certainty.

The permitted workflow is:

```text
source and available descriptions
        ↓
structural inspection
        ↓
provisional proposals with evidence
        ↓
unknown · inferred · contested · requiresHumanReview
        ↓
accountable review or source-authority publication
        ↓
reviewed · verified · canonical where justified
```

Automation may reduce repeated integration work. It must not fabricate meaning, authority, identity, permission, provenance or certainty.

## 5. Implementation order remains unchanged

This document does not authorize any future profile or extension ahead of the accepted gates.

The active order remains:

```text
complete Core reference tooling
→ provider-neutral conformance runner
→ SDK and packaging foundations
→ compiler evidence and benchmark protocols
→ JSON/CSV compiler
→ review workflow
→ with/without-ADUC and independent-consumer proof
→ first source extension
→ Situation & Action extension
→ separately governed anticipation engine
```

`docs/roadmap/NEXT_ACTION.md` remains the sole active-task authority.

## 6. Claim boundary

The repository may state that ADUC is designed as a general data-understanding Core with an initial JSON/CSV proof boundary.

Until implementation and independent evidence exist, it must not state that:

- every source category is already supported;
- arbitrary data can explain itself without supplied context or review;
- every AI system is automatically ADUC-compatible;
- ADUC replaces established structural, semantic, provenance, quality or policy standards;
- cross-provider interoperability is proven;
- ADUC is a recognized or definitively world-first standard.
