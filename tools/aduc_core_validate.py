#!/usr/bin/env python3
"""Local validator for the ADUC Core Draft 2020-12 schema family."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schema"
DEFAULT_CONTRACT = ROOT / "examples" / "core" / "complete-model.example.json"

SCHEMA_FILES = (
    "aduc-core.schema.json",
    "aduc-envelope.schema.json",
    "aduc-metadata.schema.json",
    "resource.schema.json",
    "structure.schema.json",
    "semantics.schema.json",
    "identity.schema.json",
    "context.schema.json",
    "provenance.schema.json",
    "uncertainty.schema.json",
    "relations.schema.json",
    "policy.schema.json",
    "qualification.schema.json",
    "extension.schema.json",
)

VALIDATOR_CODES = {
    "required": "ADUC-SCHEMA-REQUIRED",
    "additionalProperties": "ADUC-SCHEMA-UNKNOWN",
    "unevaluatedProperties": "ADUC-SCHEMA-UNKNOWN",
    "type": "ADUC-SCHEMA-TYPE",
    "format": "ADUC-SCHEMA-FORMAT",
    "pattern": "ADUC-SCHEMA-PATTERN",
    "enum": "ADUC-SCHEMA-ENUM",
    "const": "ADUC-SCHEMA-CONST",
    "oneOf": "ADUC-SCHEMA-ONEOF",
    "anyOf": "ADUC-SCHEMA-ANYOF",
    "allOf": "ADUC-SCHEMA-ALLOF",
    "dependentRequired": "ADUC-SCHEMA-DEPENDENCY",
    "minItems": "ADUC-SCHEMA-CARDINALITY",
    "maxItems": "ADUC-SCHEMA-CARDINALITY",
    "minProperties": "ADUC-SCHEMA-CARDINALITY",
    "uniqueItems": "ADUC-SCHEMA-UNIQUE",
    "not": "ADUC-SCHEMA-FORBIDDEN",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_schema_family(schema_dir: Path = SCHEMA_DIR) -> tuple[dict[str, Any], Registry]:
    registry = Registry()
    loaded: dict[str, dict[str, Any]] = {}
    for filename in SCHEMA_FILES:
        path = schema_dir / filename
        schema = load_json(path)
        Draft202012Validator.check_schema(schema)
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str):
            raise ValueError(f"{path} has no absolute $id")
        loaded[filename] = schema
        registry = registry.with_resource(schema_id, Resource.from_contents(schema))
    return loaded, registry


def json_path(parts: Iterable[Any]) -> str:
    result = "$"
    for part in parts:
        if isinstance(part, int):
            result += f"[{part}]"
        elif isinstance(part, str) and part.isidentifier():
            result += f".{part}"
        else:
            result += "[" + json.dumps(part, ensure_ascii=False) + "]"
    return result


def schema_error(item: Any) -> dict[str, str]:
    keyword = str(item.validator)
    return {
        "code": VALIDATOR_CODES.get(keyword, "ADUC-SCHEMA-INVALID"),
        "path": json_path(item.absolute_path),
        "message": item.message,
        "keyword": keyword,
    }


def architecture_module() -> Any:
    path = ROOT / "tools" / "aduc_core_model.py"
    spec = importlib.util.spec_from_file_location("aduc_core_model", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load architectural checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_document(document: Any, *, schema_dir: Path = SCHEMA_DIR, architecture: bool = True) -> dict[str, Any]:
    schemas, registry = load_schema_family(schema_dir)
    validator = Draft202012Validator(
        schemas["aduc-core.schema.json"],
        registry=registry,
        format_checker=FormatChecker(),
    )
    schema_errors = [
        schema_error(item)
        for item in sorted(validator.iter_errors(document), key=lambda error: (list(error.absolute_path), error.message))
    ]

    architecture_errors: list[dict[str, str]] = []
    if architecture:
        checker = architecture_module()
        manifest = load_json(ROOT / "spec" / "core-module-manifest.json")
        architecture_errors = checker.validate_document(document, manifest)["errors"]

    return {
        "valid": not schema_errors and not architecture_errors,
        "schemaValid": not schema_errors,
        "architectureValid": not architecture_errors,
        "schemaErrors": schema_errors,
        "architectureErrors": architecture_errors,
    }


def discover_inputs(values: list[str]) -> list[Path]:
    if not values:
        return [DEFAULT_CONTRACT]
    paths: list[Path] = []
    for value in values:
        path = Path(value)
        if path.is_dir():
            paths.extend(sorted(item for item in path.rglob("*.json") if item.name != "manifest.json"))
        else:
            paths.append(path)
    return paths


def result_for_document(document: Any, label: str, architecture: bool) -> dict[str, Any]:
    result = validate_document(document, architecture=architecture)
    return {"path": label, **result}


def validate_path(path: Path, architecture: bool = True) -> list[dict[str, Any]]:
    try:
        payload = load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        return [{
            "path": str(path),
            "valid": False,
            "schemaValid": False,
            "architectureValid": False,
            "schemaErrors": [{"code": "ADUC-JSON-SYNTAX", "path": "$", "message": str(exc), "keyword": "json"}],
            "architectureErrors": [],
        }]
    if isinstance(payload, dict) and isinstance(payload.get("cases"), list):
        results = []
        for index, case in enumerate(payload["cases"]):
            if not isinstance(case, dict) or "document" not in case:
                results.append({
                    "path": f"{path}#cases[{index}]",
                    "valid": False,
                    "schemaValid": False,
                    "architectureValid": False,
                    "schemaErrors": [{"code": "ADUC-FIXTURE-FORMAT", "path": "$", "message": "Fixture case must contain a document", "keyword": "fixture"}],
                    "architectureErrors": [],
                })
                continue
            label = str(case.get("id", index))
            results.append(result_for_document(case["document"], f"{path}#{label}", architecture))
        return results
    return [result_for_document(payload, str(path), architecture)]


def render_text(results: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for result in results:
        lines.append(f"{'VALID' if result['valid'] else 'INVALID'} {result['path']}")
        for item in result["schemaErrors"]:
            lines.append(f"  {item['code']} {item['path']}: {item['message']}")
        for item in result["architectureErrors"]:
            lines.append(f"  {item['code']} {item['path']}: {item['message']}")
    valid_count = sum(1 for result in results if result["valid"])
    lines.append(f"Summary: {valid_count}/{len(results)} valid")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="JSON contracts, fixture suites or directories")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--schema-only", action="store_true", help="Skip complementary architectural checks")
    args = parser.parse_args()

    results: list[dict[str, Any]] = []
    for path in discover_inputs(args.paths):
        results.extend(validate_path(path, architecture=not args.schema_only))
    payload = {
        "ok": all(result["valid"] for result in results),
        "valid": sum(1 for result in results if result["valid"]),
        "invalid": sum(1 for result in results if not result["valid"]),
        "results": results,
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(render_text(results))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
