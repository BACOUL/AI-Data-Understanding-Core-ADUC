# Semantic-Profile Migration Milestone Evidence

- Issue: #55
- Pull request: #59
- Decision: ADR-0017
- Migration format: `semantic-profile-migration-manifest.schema.json`
- Reference command: `tools/aduc_migrate_semantic_profile.py`

## Verified behavior

The migration is deterministic, local and additive. It converts an accepted standalone semantic-mapping profile plus an explicit source/structure manifest into a complete ten-block ADUC Core contract.

The implementation does not infer missing source bindings, publisher authority, legal permission, entity equivalence or policy decisions. Unverified canonical assertions remain review-required. Contested assertions preserve conflict and uncertainty. Unsupported source fields and missing bindings are reported through stable migration diagnostics.

Every emitted contract is revalidated through `tools/aduc_core.py validate`.

## Frozen scenarios

- inferred mapping with explicit source and field bindings;
- canonical mapping without sufficient authority, demoted to review-required state;
- contested mapping preserving conflict, alternatives and review requirements.

## Reproducible checks

```bash
python tools/validate_contracts.py
python -m unittest discover -s tests/core_migration -p "test_*.py"
python -m unittest discover -s tests -p "test_*.py"
python tools/aduc_migrate_semantic_profile.py \
  examples/migration/inferred.profile.json \
  examples/migration/inferred.manifest.json \
  --output migrated.core.json \
  --report migration.report.json
python tools/aduc_core.py validate migrated.core.json --format json
python tools/validate_website.py
```

## Evidence counts

- 19 focused migration tests;
- 188 total repository tests;
- three frozen end-to-end migration scenarios;
- contract, Core and website validation retained;
- no network, hosted model or remote schema dependency.

Final GitHub Actions and deployment identifiers are recorded in pull request #59 because they belong to the final PR-head execution rather than the implementation source itself.
