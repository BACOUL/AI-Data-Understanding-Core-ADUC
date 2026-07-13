# ADUC model conformance task 0.1

You receive six synthetic scenarios in `cases.json`. Each scenario contains two JSON source descriptions, two source samples and two ADUC semantic mapping profiles.

For every scenario:

1. Use only the supplied artifacts.
2. Do not browse, call tools, retrieve ontologies or use remembered private mappings.
3. Do not infer equivalence from similar field names.
4. Preserve each assertion ID, local reference, semantic target, status and mapping relation exactly.
5. Classify the pair as one of:
   - `comparable`: same target, both exact, neither inferred nor contested;
   - `candidate`: same target but at least one assertion is inferred or one relation is non-exact;
   - `blocked`: at least one assertion is contested;
   - `unmapped`: targets differ and no explicit shared target exists.
6. Never upgrade `inferred`, `closeMatch`, `broadMatch`, `narrowMatch`, `relatedMatch` or `contested`.
7. Report unit, time and entity as `notEvaluated` because the package does not provide contracts for these dimensions.
8. Cite both assertion IDs as evidence.
9. Return concise JSON matching `result-template.json`.
10. Do not provide chain-of-thought. Give only the requested result records and short reasons.

The expected answer file is not part of this package and must not be requested.
