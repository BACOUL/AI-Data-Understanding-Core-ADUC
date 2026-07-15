#!/usr/bin/env python3
"""Structurally separate demonstration adapter for the full-Core runner."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ADAPTER_PROTOCOL = "urn:aduc:full-core-conformance-adapter:0.1"
IMPLEMENTATION = {
    "id": "urn:aduc:implementation:demo-external-adapter",
    "name": "ADUC conformance demonstration adapter",
    "version": "0.1.0",
    "kind": "external",
    "provider": "ADUC fixture adapter",
}


def emit(payload: dict[str, Any]) -> int:
    sys.stdout.write(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    )
    return 0


def envelope(operation: str, **items: Any) -> dict[str, Any]:
    payload = {
        "adapterProtocol": ADAPTER_PROTOCOL,
        "operation": operation,
        "implementation": IMPLEMENTATION,
    }
    payload.update(items)
    return payload


def diagnostic(code: str) -> dict[str, str]:
    return {"code": code, "path": "$", "message": code}


def validate(path: Path) -> int:
    name = path.name
    report: dict[str, Any] = {
        "reportVersion": "0.1.0",
        "valid": True,
        "outcome": "valid",
        "diagnostics": [],
        "profileEvaluations": [],
    }
    exit_code = 0
    if "invalid" in name:
        report["valid"] = False
        report["outcome"] = "blocked"
        report["diagnostics"] = [diagnostic("ADUC-SCHEMA-REQUIRED")]
        exit_code = 1
    elif "review" in name or "profile-unknown" in name:
        report["outcome"] = "requiresHumanReview"
        report["profileEvaluations"] = [
            {"profile": "ADR-0013", "status": "requiresHumanReview"},
            {"profile": "ADR-0007", "status": "unknown"},
        ]
        exit_code = 2
    elif "unknown" in name:
        report["profileEvaluations"] = [{"profile": "ADR-0007", "status": "unknown"}]
    return emit(envelope("validate", report=report, exitCode=exit_code))


def compare(left: Path, right: Path) -> int:
    name = right.name
    report: dict[str, Any] = {
        "reportVersion": "0.1.0",
        "comparable": True,
        "overall": "unchanged",
        "overallAssessment": "equivalent",
        "changes": [],
    }
    exit_code = 0
    if "convertible-unit" in name:
        report.update({"overall": "compatible", "overallAssessment": "convertible"})
        report["changes"] = [
            {
                "code": "ADUC-COMPARE-SEMANTICS-UNIT-001",
                "changeType": "modified",
                "assessment": "convertible",
            }
        ]
    elif "unknown-unit" in name:
        report.update({"overall": "potentiallyIncompatible", "overallAssessment": "unknown"})
        report["changes"] = [
            {
                "code": "ADUC-COMPARE-SEMANTICS-UNIT-001",
                "changeType": "modified",
                "assessment": "unknown",
            }
        ]
        exit_code = 2
    elif "contested" in name:
        report.update({"overall": "requiresHumanReview", "overallAssessment": "contested"})
        report["changes"] = [
            {
                "code": "ADUC-COMPARE-SEMANTICS-CONFLICT-001",
                "changeType": "modified",
                "assessment": "contested",
            }
        ]
        exit_code = 2
    elif "prohibited" in name:
        report.update({"overall": "potentiallyIncompatible", "overallAssessment": "prohibited"})
        report["changes"] = [
            {
                "code": "ADUC-COMPARE-POLICY-PROHIBITION-ADDED-001",
                "changeType": "added",
                "assessment": "prohibited",
            }
        ]
        exit_code = 2
    elif "deprecated" in name:
        report.update({"overall": "requiresHumanReview", "overallAssessment": "deprecated"})
        report["changes"] = [
            {
                "code": "ADUC-COMPARE-SEMANTICS-LIFECYCLE-001",
                "changeType": "modified",
                "assessment": "deprecated",
            }
        ]
        exit_code = 2
    return emit(envelope("compare", report=report, exitCode=exit_code))


def format_contract(path: Path) -> int:
    name = path.name
    outcome = "formattedRequiresHumanReview" if "review" in name else "formatted"
    exit_code = 2 if "review" in name else 0
    data = path.read_bytes()
    report = {
        "reportVersion": "0.1.0",
        "formatted": True,
        "outcome": outcome,
        "diagnostics": [],
    }
    return emit(
        envelope(
            "format",
            report=report,
            exitCode=exit_code,
            formattedSha256="sha256:" + hashlib.sha256(data).hexdigest(),
            formattedBytes=len(data),
        )
    )


def declare_capabilities() -> int:
    return emit(
        envelope(
            "declareCapabilities",
            capabilities={
                "validate": True,
                "compare": True,
                "format": True,
                "classes": [
                    "fullCoreValidator",
                    "fullCoreComparator",
                    "fullCoreFormatter",
                ],
            },
            independenceAttestation={
                "genuineSeparateImplementation": False,
                "scope": "Demonstration adapter for the public boundary; not independent conformance evidence.",
            },
        )
    )


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args == ["declareCapabilities"]:
        return declare_capabilities()
    if len(args) == 2 and args[0] == "validate":
        return validate(Path(args[1]))
    if len(args) == 3 and args[0] == "compare":
        return compare(Path(args[1]), Path(args[2]))
    if len(args) == 2 and args[0] == "format":
        return format_contract(Path(args[1]))
    return emit(envelope(args[0] if args else "usage", status="unsupported"))


if __name__ == "__main__":
    sys.exit(main())
