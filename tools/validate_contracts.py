#!/usr/bin/env python3
"""Validate official ADUC example fixtures against the bootstrap schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "aduc-core.schema.json"


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def errors_for(validator: Draft202012Validator, path: Path) -> list[str]:
    instance = load_json(path)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))
    output: list[str] = []
    for error in errors:
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        output.append(f"{path.relative_to(ROOT)}:{location}: {error.message}")
    return output


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    valid_files = sorted((ROOT / "examples").rglob("*.aduc.json"))
    valid_files += sorted((ROOT / "tests" / "fixtures" / "valid").glob("*.aduc.json"))
    invalid_files = sorted((ROOT / "tests" / "fixtures" / "invalid").glob("*.aduc.json"))

    failures: list[str] = []

    for path in valid_files:
        errors = errors_for(validator, path)
        if errors:
            failures.append(f"Expected VALID: {path.relative_to(ROOT)}")
            failures.extend(f"  {error}" for error in errors)

    for path in invalid_files:
        errors = errors_for(validator, path)
        if not errors:
            failures.append(f"Expected INVALID: {path.relative_to(ROOT)}")

    if failures:
        print("Validation failed:")
        print("\n".join(failures))
        return 1

    print(f"Validated {len(valid_files)} valid and {len(invalid_files)} invalid fixtures.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
