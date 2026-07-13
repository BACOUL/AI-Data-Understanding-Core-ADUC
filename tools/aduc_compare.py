#!/usr/bin/env python3
"""Compare two validated ADUC semantic mapping profiles deterministically."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from aduc_validate import (  # noqa: E402
    DEFAULT_SCHEMA_PATH,
    input_error_report,
    load_json,
    validate_profile,
)

EXIT_VALID = 0
EXIT_INVALID = 1
EXIT_INPUT_ERROR = 2

PROTOCOL_ID = "urn:aduc:comparison:0.1"
EXACT_MATCH = "http://www.w3.org/2004/02/skos/core#exactMatch"

NOT_EVALUATED_DIMENSIONS = {
    "entity": {
        "status": "notEvaluated",
        "reason": (
            "Entity identity is not represented by the supplied mapping profiles "
            "and was not guessed."
        ),
    },
    "time": {
        "status": "notEvaluated",
        "reason": (
            "Temporal fields, formats and zones are not represented by the supplied "
            "mapping profiles and were not guessed."
        ),
    },
    "unit": {
        "status": "notEvaluated",
        "reason": (
            "Unit identifiers and conversion rules are not represented by the supplied "
            "mapping profiles and were not guessed."
        ),
    },
}


def assertion_key(assertion: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(assertion.get("semanticTarget", "")),
        str(assertion.get("localReference", "")),
        str(assertion.get("id", "")),
    )


def assertion_view(assertion: dict[str, Any]) -> dict[str, str]:
    return {
        "assertionId": str(assertion["id"]),
        "localReference": str(assertion["localReference"]),
        "mappingRelation": str(assertion["mappingRelation"]),
        "semanticTarget": str(assertion["semanticTarget"]),
        "status": str(assertion["status"]),
    }


def classify_pair(
    assertion_a: dict[str, Any],
    assertion_b: dict[str, Any],
) -> tuple[str, list[str]]:
    statuses = {assertion_a["status"], assertion_b["status"]}
    relations = {
        assertion_a["mappingRelation"],
        assertion_b["mappingRelation"],
    }

    if "contested" in statuses:
        return "blocked", ["at least one mapping assertion is contested"]

    reasons: list[str] = []
    if "inferred" in statuses:
        reasons.append("at least one mapping assertion is inferred")
    if relations != {EXACT_MATCH}:
        reasons.append("at least one mapping relation is not skos:exactMatch")

    if not reasons:
        return "comparable", [
            "identical semantic target with non-inferred exact mappings"
        ]
    return "candidate", reasons


def profile_info(
    profile: dict[str, Any],
    report: dict[str, Any],
    path: str,
) -> dict[str, Any]:
    binding = profile.get("validFor", {})
    return {
        "id": profile.get("id"),
        "path": path,
        "source": binding.get("source") if isinstance(binding, dict) else None,
        "sourceBinding": binding if isinstance(binding, dict) else None,
        "warnings": report.get("warnings", []),
    }


def compare_profiles(
    profile_a: Any,
    profile_b: Any,
    schema: dict[str, Any],
    *,
    path_a: str = "",
    path_b: str = "",
    trusted_authorities_a: set[str] | None = None,
    trusted_authorities_b: set[str] | None = None,
) -> dict[str, Any]:
    validation_a = validate_profile(
        profile_a,
        schema,
        profile_path=path_a,
        trusted_authorities=trusted_authorities_a,
    )
    validation_b = validate_profile(
        profile_b,
        schema,
        profile_path=path_b,
        trusted_authorities=trusted_authorities_b,
    )

    if not validation_a["valid"] or not validation_b["valid"]:
        return {
            "protocol": PROTOCOL_ID,
            "valid": False,
            "profileA": {
                "path": path_a,
                "id": profile_a.get("id") if isinstance(profile_a, dict) else None,
                "validation": validation_a,
            },
            "profileB": {
                "path": path_b,
                "id": profile_b.get("id") if isinstance(profile_b, dict) else None,
                "validation": validation_b,
            },
            "summary": {
                "blocked": 0,
                "candidate": 0,
                "comparable": 0,
                "unmappedA": 0,
                "unmappedB": 0,
            },
            "matches": [],
            "unmapped": {"profileA": [], "profileB": []},
            "dimensions": dict(NOT_EVALUATED_DIMENSIONS),
        }

    assertions_a = sorted(profile_a["assertions"], key=assertion_key)
    assertions_b = sorted(profile_b["assertions"], key=assertion_key)

    by_target_a: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_target_b: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for assertion in assertions_a:
        by_target_a[assertion["semanticTarget"]].append(assertion)
    for assertion in assertions_b:
        by_target_b[assertion["semanticTarget"]].append(assertion)

    targets_a = set(by_target_a)
    targets_b = set(by_target_b)
    common_targets = sorted(targets_a & targets_b)

    matches: list[dict[str, Any]] = []
    for target in common_targets:
        for assertion_a in by_target_a[target]:
            for assertion_b in by_target_b[target]:
                classification, reasons = classify_pair(assertion_a, assertion_b)
                matches.append(
                    {
                        "classification": classification,
                        "semanticTarget": target,
                        "reasons": reasons,
                        "profileA": assertion_view(assertion_a),
                        "profileB": assertion_view(assertion_b),
                    }
                )

    classification_order = {"blocked": 0, "candidate": 1, "comparable": 2}
    matches.sort(
        key=lambda item: (
            item["semanticTarget"],
            classification_order[item["classification"]],
            item["profileA"]["localReference"],
            item["profileB"]["localReference"],
            item["profileA"]["assertionId"],
            item["profileB"]["assertionId"],
        )
    )

    unmapped_a = [
        assertion_view(assertion)
        for target in sorted(targets_a - targets_b)
        for assertion in by_target_a[target]
    ]
    unmapped_b = [
        assertion_view(assertion)
        for target in sorted(targets_b - targets_a)
        for assertion in by_target_b[target]
    ]

    summary = {
        "blocked": sum(item["classification"] == "blocked" for item in matches),
        "candidate": sum(item["classification"] == "candidate" for item in matches),
        "comparable": sum(item["classification"] == "comparable" for item in matches),
        "unmappedA": len(unmapped_a),
        "unmappedB": len(unmapped_b),
    }

    return {
        "protocol": PROTOCOL_ID,
        "valid": True,
        "profileA": profile_info(profile_a, validation_a, path_a),
        "profileB": profile_info(profile_b, validation_b, path_b),
        "summary": summary,
        "matches": matches,
        "unmapped": {
            "profileA": unmapped_a,
            "profileB": unmapped_b,
        },
        "dimensions": dict(NOT_EVALUATED_DIMENSIONS),
    }


def serialize_json(report: dict[str, Any]) -> str:
    return json.dumps(
        report,
        indent=2,
        ensure_ascii=False,
        sort_keys=True,
    ) + "\n"


def render_text(report: dict[str, Any]) -> str:
    if report.get("inputErrors"):
        lines = ["COMPARISON INPUT ERROR"]
        for input_report in report["inputErrors"]:
            for issue in input_report.get("errors", []):
                lines.append(f"{issue['code']}: {issue['message']}")
        return "\n".join(lines)

    if not report["valid"]:
        lines = ["COMPARISON INVALID"]
        for label in ("profileA", "profileB"):
            validation = report[label].get("validation", {})
            for issue in validation.get("errors", []):
                location = issue.get("path") or "<root>"
                lines.append(
                    f"{label.upper()} {issue['code']} {location}: {issue['message']}"
                )
        return "\n".join(lines)

    lines = [
        (
            f"COMPARISON VALID: {report['profileA'].get('id')} "
            f"<-> {report['profileB'].get('id')}"
        )
    ]
    for match in report["matches"]:
        lines.append(
            (
                f"{match['classification'].upper()} "
                f"{match['profileA']['localReference']} <-> "
                f"{match['profileB']['localReference']} "
                f"[{match['semanticTarget']}]"
            )
        )
    for side in ("profileA", "profileB"):
        for assertion in report["unmapped"][side]:
            lines.append(
                (
                    f"UNMAPPED_{side[-1].upper()} "
                    f"{assertion['localReference']} "
                    f"[{assertion['semanticTarget']}]"
                )
            )
    for dimension in sorted(report["dimensions"]):
        item = report["dimensions"][dimension]
        lines.append(f"{item['status'].upper()} {dimension}: {item['reason']}")
    return "\n".join(lines)


def emit(report: dict[str, Any], output_format: str) -> None:
    if output_format == "json":
        sys.stdout.write(serialize_json(report))
    else:
        print(render_text(report))


def load_profile_or_report(
    path: Path,
    label: str,
) -> tuple[Any | None, dict[str, Any] | None]:
    try:
        return load_json(path), None
    except FileNotFoundError:
        return None, input_error_report(
            str(path), "ADUC-INPUT-001", f"{label} file does not exist."
        )
    except OSError as error:
        return None, input_error_report(
            str(path), "ADUC-INPUT-001", f"Unable to read {label}: {error}"
        )
    except json.JSONDecodeError as error:
        return None, input_error_report(
            str(path),
            "ADUC-INPUT-002",
            (
                f"Invalid JSON in {label} at line {error.lineno}, "
                f"column {error.colno}: {error.msg}"
            ),
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare two ADUC semantic mapping profiles."
    )
    parser.add_argument("profile_a", type=Path)
    parser.add_argument("profile_b", type=Path)
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA_PATH,
        help="Path to the ADUC mapping-profile schema",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        dest="output_format",
    )
    parser.add_argument(
        "--trusted-authority-a",
        action="append",
        default=[],
        help="Locally trusted canonical authority IRI for profile A; repeatable",
    )
    parser.add_argument(
        "--trusted-authority-b",
        action="append",
        default=[],
        help="Locally trusted canonical authority IRI for profile B; repeatable",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    profile_a, input_error_a = load_profile_or_report(args.profile_a, "profile A")
    profile_b, input_error_b = load_profile_or_report(args.profile_b, "profile B")
    if input_error_a or input_error_b:
        report = {
            "protocol": PROTOCOL_ID,
            "valid": False,
            "inputErrors": [
                item
                for item in (input_error_a, input_error_b)
                if item is not None
            ],
        }
        emit(report, args.output_format)
        return EXIT_INPUT_ERROR

    try:
        schema = load_json(args.schema)
    except (OSError, json.JSONDecodeError) as error:
        report = {
            "protocol": PROTOCOL_ID,
            "valid": False,
            "inputErrors": [
                input_error_report(
                    str(args.schema),
                    "ADUC-INPUT-003",
                    f"Unable to load validator schema: {error}",
                )
            ],
        }
        emit(report, args.output_format)
        return EXIT_INPUT_ERROR

    report = compare_profiles(
        profile_a,
        profile_b,
        schema,
        path_a=str(args.profile_a),
        path_b=str(args.profile_b),
        trusted_authorities_a=set(args.trusted_authority_a),
        trusted_authorities_b=set(args.trusted_authority_b),
    )
    emit(report, args.output_format)
    return EXIT_VALID if report["valid"] else EXIT_INVALID


if __name__ == "__main__":
    sys.exit(main())
