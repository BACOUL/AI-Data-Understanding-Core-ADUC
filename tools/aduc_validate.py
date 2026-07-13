#!/usr/bin/env python3
"""Validate one ADUC semantic mapping profile and emit a conformance report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA_PATH = ROOT / "schema" / "aduc-mapping-profile.schema.json"

EXIT_VALID = 0
EXIT_INVALID = 1
EXIT_INPUT_ERROR = 2


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def make_issue(
    code: str,
    severity: str,
    category: str,
    path: str,
    message: str,
) -> dict[str, str]:
    return {
        "code": code,
        "severity": severity,
        "category": category,
        "path": path,
        "message": message,
    }


def pointer(parts: Iterable[Any]) -> str:
    escaped = [
        str(part).replace("~", "~0").replace("/", "~1")
        for part in parts
    ]
    return "/" + "/".join(escaped) if escaped else ""


def schema_issues(instance: Any, schema: dict[str, Any]) -> list[dict[str, str]]:
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: [str(part) for part in error.absolute_path],
    )
    return [
        make_issue(
            "ADUC-SCHEMA-001",
            "error",
            "schema",
            pointer(error.absolute_path),
            error.message,
        )
        for error in errors
    ]


def semantic_issues(
    instance: Any,
    trusted_authorities: set[str] | None = None,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    trusted = trusted_authorities or set()

    if not isinstance(instance, dict):
        return errors, warnings
    assertions = instance.get("assertions")
    if not isinstance(assertions, list):
        return errors, warnings

    id_to_index: dict[str, int] = {}
    duplicate_ids: set[str] = set()

    for index, assertion in enumerate(assertions):
        if not isinstance(assertion, dict):
            continue
        assertion_id = assertion.get("id")
        if not isinstance(assertion_id, str):
            continue
        if assertion_id in id_to_index:
            duplicate_ids.add(assertion_id)
            errors.append(
                make_issue(
                    "ADUC-DOC-001",
                    "error",
                    "semantic",
                    f"/assertions/{index}/id",
                    (
                        f"Duplicate assertion id {assertion_id!r}; first seen at "
                        f"/assertions/{id_to_index[assertion_id]}/id."
                    ),
                )
            )
        else:
            id_to_index[assertion_id] = index

    graph: dict[str, str] = {}
    for index, assertion in enumerate(assertions):
        if not isinstance(assertion, dict):
            continue
        assertion_id = assertion.get("id")
        supersedes = assertion.get("supersedes")
        if not isinstance(assertion_id, str) or not isinstance(supersedes, str):
            continue
        if assertion_id == supersedes:
            errors.append(
                make_issue(
                    "ADUC-LIFE-001",
                    "error",
                    "semantic",
                    f"/assertions/{index}/supersedes",
                    "An assertion must not supersede itself.",
                )
            )
            continue
        if assertion_id not in duplicate_ids and supersedes in id_to_index:
            graph[assertion_id] = supersedes

    state: dict[str, int] = {}
    reported_cycles: set[frozenset[str]] = set()

    def visit(node: str, stack: list[str]) -> None:
        state[node] = 1
        stack.append(node)
        target = graph.get(node)
        if target is not None:
            if state.get(target, 0) == 0:
                visit(target, stack)
            elif state.get(target) == 1:
                start = stack.index(target)
                cycle = stack[start:] + [target]
                cycle_key = frozenset(cycle)
                if cycle_key not in reported_cycles:
                    reported_cycles.add(cycle_key)
                    index = id_to_index[node]
                    errors.append(
                        make_issue(
                            "ADUC-LIFE-002",
                            "error",
                            "semantic",
                            f"/assertions/{index}/supersedes",
                            "Supersedes cycle detected: " + " -> ".join(cycle),
                        )
                    )
        stack.pop()
        state[node] = 2

    for assertion_id in sorted(graph):
        if state.get(assertion_id, 0) == 0:
            visit(assertion_id, [])

    canonical_by_local: dict[str, list[tuple[int, str, str, str]]] = {}
    for index, assertion in enumerate(assertions):
        if not isinstance(assertion, dict) or assertion.get("status") != "canonical":
            continue
        local = assertion.get("localReference")
        target = assertion.get("semanticTarget")
        relation = assertion.get("mappingRelation")
        assertion_id = assertion.get("id")
        asserted_by = assertion.get("assertedBy")
        if all(isinstance(value, str) for value in (local, target, relation, assertion_id)):
            canonical_by_local.setdefault(local, []).append(
                (index, target, relation, assertion_id)
            )
        if isinstance(asserted_by, str) and asserted_by not in trusted:
            warnings.append(
                make_issue(
                    "ADUC-TRUST-001",
                    "warning",
                    "trust",
                    f"/assertions/{index}/assertedBy",
                    (
                        f"Canonical authority {asserted_by!r} was not verified. "
                        "Provide --trusted-authority only for locally trusted authorities."
                    ),
                )
            )

    for local, candidates in sorted(canonical_by_local.items()):
        meanings = {(target, relation) for _, target, relation, _ in candidates}
        if len(meanings) <= 1:
            continue
        ids = ", ".join(candidate[3] for candidate in candidates)
        errors.append(
            make_issue(
                "ADUC-CONFLICT-001",
                "error",
                "semantic",
                "/assertions",
                (
                    f"Incompatible canonical targets for local reference {local!r}: "
                    f"{ids}."
                ),
            )
        )

    errors.sort(key=lambda issue: (issue["code"], issue["path"], issue["message"]))
    warnings.sort(key=lambda issue: (issue["code"], issue["path"], issue["message"]))
    return errors, warnings


def validate_profile(
    instance: Any,
    schema: dict[str, Any],
    *,
    profile_path: str = "",
    trusted_authorities: set[str] | None = None,
) -> dict[str, Any]:
    errors = schema_issues(instance, schema)
    semantic_errors, warnings = semantic_issues(instance, trusted_authorities)
    errors.extend(semantic_errors)
    errors.sort(key=lambda issue: (issue["category"], issue["code"], issue["path"]))

    profile_id = instance.get("id") if isinstance(instance, dict) else None
    return {
        "profile": profile_path,
        "profileId": profile_id if isinstance(profile_id, str) else None,
        "valid": not errors,
        "summary": {
            "errors": len(errors),
            "warnings": len(warnings),
        },
        "errors": errors,
        "warnings": warnings,
    }


def render_text(report: dict[str, Any]) -> str:
    status = "VALID" if report["valid"] else "INVALID"
    profile = report.get("profile") or "<memory>"
    summary = report["summary"]
    lines = [
        (
            f"{status}: {profile} "
            f"({summary['errors']} errors, {summary['warnings']} warnings)"
        )
    ]
    for issue in report["errors"] + report["warnings"]:
        location = issue["path"] or "<root>"
        lines.append(
            f"{issue['severity'].upper()} {issue['code']} "
            f"{location}: {issue['message']}"
        )
    return "\n".join(lines)


def input_error_report(profile_path: str, code: str, message: str) -> dict[str, Any]:
    issue = make_issue(code, "error", "input", "", message)
    return {
        "profile": profile_path,
        "profileId": None,
        "valid": False,
        "summary": {"errors": 1, "warnings": 0},
        "errors": [issue],
        "warnings": [],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate one ADUC semantic mapping profile."
    )
    parser.add_argument("profile", type=Path, help="Path to an ADUC profile JSON file")
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA_PATH,
        help="Path to the ADUC JSON Schema",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        dest="output_format",
        help="Report format",
    )
    parser.add_argument(
        "--trusted-authority",
        action="append",
        default=[],
        help="Locally trusted canonical authority IRI; repeatable",
    )
    return parser


def emit(report: dict[str, Any], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(render_text(report))


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    profile_path = str(args.profile)

    try:
        instance = load_json(args.profile)
    except FileNotFoundError:
        report = input_error_report(
            profile_path, "ADUC-INPUT-001", "Profile file does not exist."
        )
        emit(report, args.output_format)
        return EXIT_INPUT_ERROR
    except OSError as error:
        report = input_error_report(
            profile_path, "ADUC-INPUT-001", f"Unable to read profile: {error}"
        )
        emit(report, args.output_format)
        return EXIT_INPUT_ERROR
    except json.JSONDecodeError as error:
        report = input_error_report(
            profile_path,
            "ADUC-INPUT-002",
            f"Invalid JSON at line {error.lineno}, column {error.colno}: {error.msg}",
        )
        emit(report, args.output_format)
        return EXIT_INPUT_ERROR

    try:
        schema = load_json(args.schema)
        report = validate_profile(
            instance,
            schema,
            profile_path=profile_path,
            trusted_authorities=set(args.trusted_authority),
        )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        report = input_error_report(
            profile_path, "ADUC-INPUT-003", f"Unable to load validator schema: {error}"
        )
        emit(report, args.output_format)
        return EXIT_INPUT_ERROR

    emit(report, args.output_format)
    return EXIT_VALID if report["valid"] else EXIT_INVALID


if __name__ == "__main__":
    sys.exit(main())
