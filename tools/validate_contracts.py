#!/usr/bin/env python3
"""Validate official ADUC mapping-profile fixtures against the candidate schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "aduc-mapping-profile.schema.json"
VALID_CASES_PATH = (
    ROOT / "tests" / "fixtures" / "mapping-profile" / "valid" / "cases.json"
)
INVALID_CASES_PATH = (
    ROOT / "tests" / "fixtures" / "mapping-profile" / "invalid" / "cases.json"
)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def format_errors(
    validator: Draft202012Validator, instance: Any
) -> list[str]:
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: [str(part) for part in error.absolute_path],
    )
    output: list[str] = []
    for error in errors:
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        output.append(f"{location}: {error.message}")
    return output


def load_cases(path: Path) -> list[dict[str, Any]]:
    document = load_json(path)
    if not isinstance(document, dict) or not isinstance(document.get("cases"), list):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a 'cases' array")
    cases = document["cases"]
    names: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError(f"{path.relative_to(ROOT)} contains a non-object case")
        name = case.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError(f"{path.relative_to(ROOT)} contains a case without a name")
        if name in names:
            raise ValueError(f"{path.relative_to(ROOT)} duplicates case name {name!r}")
        if "instance" not in case:
            raise ValueError(f"{path.relative_to(ROOT)} case {name!r} has no instance")
        names.add(name)
    return cases


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    valid_cases = load_cases(VALID_CASES_PATH)
    invalid_cases = load_cases(INVALID_CASES_PATH)
    failures: list[str] = []

    for case in valid_cases:
        errors = format_errors(validator, case["instance"])
        if errors:
            failures.append(f"Expected VALID: {case['name']}")
            failures.extend(f"  {error}" for error in errors)

    for case in invalid_cases:
        errors = format_errors(validator, case["instance"])
        if not errors:
            failures.append(f"Expected INVALID: {case['name']}")

    if failures:
        print("Validation failed:")
        print("\n".join(failures))
        return 1

    print(
        f"Validated {len(valid_cases)} valid and "
        f"{len(invalid_cases)} invalid mapping-profile fixtures."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
