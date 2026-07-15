#!/usr/bin/env python3
"""Provider-neutral conformance adapter for the ADUC Python reference tools."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import aduc_core  # noqa: E402
import aduc_core_format  # noqa: E402

ADAPTER_PROTOCOL = "urn:aduc:full-core-conformance-adapter:0.1"
IMPLEMENTATION = {
    "id": "urn:aduc:implementation:python-reference",
    "name": "ADUC Python reference implementation",
    "version": "0.1.0",
    "kind": "reference",
    "provider": "ADUC repository",
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
                "scope": "Reference implementation self-conformance only.",
            },
        )
    )


def validate(path: Path) -> int:
    report = aduc_core.validate_path(path)
    exit_code = aduc_core.validation_exit(report)
    return emit(envelope("validate", report=report, exitCode=exit_code))


def compare(left: Path, right: Path) -> int:
    report = aduc_core.compare_paths(left, right)
    exit_code = aduc_core.compare_exit(report)
    return emit(envelope("compare", report=report, exitCode=exit_code))


def format_contract(path: Path) -> int:
    with tempfile.TemporaryDirectory(prefix="aduc-conformance-format-") as root:
        output = Path(root) / "formatted.json"
        report, exit_code = aduc_core_format.format_path(path, output, force=True)
        payload: dict[str, Any] = envelope("format", report=report, exitCode=exit_code)
        if output.exists():
            data = output.read_bytes()
            payload["formattedSha256"] = "sha256:" + hashlib.sha256(data).hexdigest()
            payload["formattedBytes"] = len(data)
        return emit(payload)


def usage(operation: str | None = None) -> int:
    return emit(
        envelope(
            operation or "usage",
            report={
                "outcome": "usageError",
                "diagnostics": [
                    {
                        "code": "ADUC-CONF-REF-ADAPTER-USAGE-001",
                        "message": "Unsupported adapter invocation.",
                    }
                ],
            },
            exitCode=3,
        )
    )


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        return usage()
    operation = args[0]
    try:
        if operation == "declareCapabilities" and len(args) == 1:
            return declare_capabilities()
        if operation == "validate" and len(args) == 2:
            return validate(Path(args[1]))
        if operation == "compare" and len(args) == 3:
            return compare(Path(args[1]), Path(args[2]))
        if operation == "format" and len(args) == 2:
            return format_contract(Path(args[1]))
    except Exception as exc:  # pragma: no cover - stable adapter boundary
        return emit(
            envelope(
                operation,
                report={
                    "outcome": "usageError",
                    "diagnostics": [
                        {
                            "code": "ADUC-CONF-REF-ADAPTER-ERROR-001",
                            "message": str(exc),
                        }
                    ],
                },
                exitCode=3,
            )
        )
    return usage(operation)


if __name__ == "__main__":
    sys.exit(main())
