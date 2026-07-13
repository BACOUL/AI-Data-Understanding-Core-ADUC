# Authoring workflow examples

These examples demonstrate the manual workflow defined in `spec/AUTHORING_WORKFLOW_0_1.md`.

## River

```text
river/source.json
river/source.schema.json
river/inferred.aduc.json
river/reviewed.aduc.json
river/authoring-state.json
```

The `flow` field begins as an inferred mapping and becomes a new reviewed assertion. The earlier assertion is preserved through `supersedes`. The other fields remain explicitly unmapped in the coverage report.

## Machine

```text
machine/source.json
machine/source.schema.json
machine/inferred.aduc.json
machine/canonical.aduc.json
machine/authoring-state.json
```

The `motor_heat` field begins as a close match to generic temperature. The publisher later issues a new canonical exact mapping to motor winding temperature. Canonicality carries no confidence score.

## Validate

```bash
python tools/validate_contracts.py
python tools/aduc_validate.py examples/authoring/river/reviewed.aduc.json
python tools/aduc_validate.py examples/authoring/machine/canonical.aduc.json \
  --trusted-authority https://factory.example/id/data-authority
```

The authoring-state files are process records and coverage reports. They are intentionally separate from the portable ADUC profiles.
