# AI Data Understanding Core 0.1 — Initial Draft Skeleton

> Non-normative bootstrap document. The information model is not frozen.

## 1. Scope

ADUC defines a portable contract describing how an AI system may interpret a data resource.

## 2. Conformance language

Future normative requirements will use MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY.

## 3. Core objects under evaluation

- `aduc`: contract identity, version, and status
- `resource`: described source
- `structure`: machine representation
- `semantics`: meaning of fields or values
- `identity`: described entities and identifier schemes
- `context`: temporal, spatial, and domain context
- `provenance`: origin and production process
- `uncertainty`: quantified or qualified uncertainty
- `relations`: links to other resources or concepts
- `policy`: declared usage conditions

## 4. Mapping status

Candidate statuses:

- `unknown`
- `inferred`
- `reviewed`
- `verified`
- `canonical`
- `contested`
- `deprecated`

## 5. Critical invariant

A consumer MUST NOT silently treat `inferred` semantics as `verified` or `canonical` semantics.

## 6. Extension principle

The Core should provide stable extension points while avoiding domain-specific concepts.

## 7. Open questions

- Which fields are mandatory?
- Should JSON-LD contexts be required, optional, or external?
- How are concept identifiers resolved?
- How are policies declared without pretending they are automatically enforced?
- How should uncertainty apply at contract, resource, field, and mapping levels?
- How should compatibility with Croissant and PROV-O be expressed?
