#!/usr/bin/env python3
"""Deterministically format one complete ADUC Core contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from decimal import Decimal
from pathlib import Path
from typing import Any

TOOLS_DIR = Path(__file__).resolve().parent
ROOT = TOOLS_DIR.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import aduc_core  # noqa: E402

REPORT_VERSION = "0.1.0"
FORMATTER_VERSION = "0.1.0"
TOP_LEVEL_ORDER = (
    "aduc",
    "resource",
    "structure",
    "semantics",
    "identity",
    "context",
    "provenance",
    "uncertainty",
    "relations",
    "policy",
)
TOP_LEVEL_INDEX = {name: index for index, name in enumerate(TOP_LEVEL_ORDER)}
EXIT_FORMATTED = 0
EXIT_BLOCKED = 1
EXIT_HUMAN_REVIEW = 2
EXIT_USAGE = 3
MAX_INPUT_BYTES = getattr(aduc_core, "MAX_INPUT_BYTES", 5_000_000)
MAX_JSON_DEPTH = getattr(aduc_core, "MAX_JSON_DEPTH", 100)
MAX_JSON_NODES = getattr(aduc_core, "MAX_JSON_NODES", 50_000)
MAX_OUTPUT_BYTES = 10_000_000


class FormatterError(Exception):
    """Stable formatter error."""

    def __init__(self, code: str, message: str, *, path: str = "$", usage: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.path = path
        self.usage = usage


class DuplicateKeyError(ValueError):
    """Raised when a JSON object contains the same member more than once."""

    def __init__(self, key: str) -> None:
        super().__init__(key)
        self.key = key


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def reject_non_json_constant(value: str) -> None:
    raise FormatterError(
        "ADUC-FMT-INPUT-006",
        f"Non-JSON numeric constant {value!r} is not accepted.",
        usage=True,
    )


def parse_json_text(text: str, *, decimal_numbers: bool = False) -> Any:
    kwargs: dict[str, Any] = {
        "object_pairs_hook": reject_duplicate_pairs,
        "parse_constant": reject_non_json_constant,
    }
    if decimal_numbers:
        kwargs["parse_float"] = Decimal
        kwargs["parse_int"] = Decimal
    try:
        return json.loads(text, **kwargs)
    except DuplicateKeyError as exc:
        raise FormatterError(
            "ADUC-FMT-INPUT-002",
            f"Duplicate JSON object member {exc.key!r} is not allowed.",
            usage=True,
        ) from exc
    except FormatterError:
        raise
    except json.JSONDecodeError as exc:
        raise FormatterError(
            "ADUC-FMT-INPUT-002",
            f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}",
            usage=True,
        ) from exc
    except ValueError as exc:
        raise FormatterError(
            "ADUC-FMT-INPUT-006",
            "JSON numeric value exceeds the supported parser limit.",
            usage=True,
        ) from exc
    except RecursionError as exc:
        raise FormatterError(
            "ADUC-FMT-INPUT-005",
            f"Input exceeds depth {MAX_JSON_DEPTH}.",
            usage=True,
        ) from exc


def load_input(path: Path) -> tuple[str, Any, Any]:
    try:
        size = path.stat().st_size
    except FileNotFoundError as exc:
        raise FormatterError("ADUC-FMT-INPUT-001", "Input file does not exist.", usage=True) from exc
    except OSError as exc:
        raise FormatterError("ADUC-FMT-INPUT-001", f"Unable to inspect input file: {exc}", usage=True) from exc
    if size > MAX_INPUT_BYTES:
        raise FormatterError(
            "ADUC-FMT-INPUT-003",
            f"Input exceeds {MAX_INPUT_BYTES} bytes.",
            usage=True,
        )
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise FormatterError("ADUC-FMT-INPUT-007", "Input is not valid UTF-8.", usage=True) from exc
    except OSError as exc:
        raise FormatterError("ADUC-FMT-INPUT-001", f"Unable to read input file: {exc}", usage=True) from exc

    document = parse_json_text(raw)
    decimal_document = parse_json_text(raw, decimal_numbers=True)
    nodes, depth = aduc_core.json_limit_stats(document)
    if nodes > MAX_JSON_NODES:
        raise FormatterError("ADUC-FMT-INPUT-004", f"Input exceeds {MAX_JSON_NODES} JSON nodes.", usage=True)
    if depth > MAX_JSON_DEPTH:
        raise FormatterError("ADUC-FMT-INPUT-005", f"Input exceeds depth {MAX_JSON_DEPTH}.", usage=True)
    return raw, document, decimal_document


def object_keys(value: dict[str, Any], *, top_level: bool) -> list[str]:
    if top_level:
        return sorted(value, key=lambda key: (TOP_LEVEL_INDEX.get(key, len(TOP_LEVEL_ORDER)), key))
    return sorted(value)


def render_number(value: Decimal) -> str:
    if not value.is_finite():
        raise FormatterError("ADUC-FMT-INPUT-006", "Non-finite JSON numbers are not accepted.", usage=True)
    if value.is_zero():
        return "-0" if value.is_signed() else "0"

    sign, coefficient, exponent = value.as_tuple()
    digits = list(coefficient)
    while len(digits) > 1 and digits[-1] == 0:
        digits.pop()
        exponent += 1

    digit_text = "".join(str(digit) for digit in digits)
    adjusted = len(digit_text) + exponent - 1
    prefix = "-" if sign else ""

    if -6 <= adjusted < 21:
        point = len(digit_text) + exponent
        if point <= 0:
            return f"{prefix}0.{('0' * -point)}{digit_text}"
        if point >= len(digit_text):
            return f"{prefix}{digit_text}{'0' * (point - len(digit_text))}"
        return f"{prefix}{digit_text[:point]}.{digit_text[point:]}"

    mantissa = digit_text[0]
    if len(digit_text) > 1:
        mantissa += f".{digit_text[1:]}"
    return f"{prefix}{mantissa}e{adjusted}"


def render_json(value: Any, *, level: int = 0, top_level: bool = False) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, Decimal):
        return render_number(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        if not value:
            return "[]"
        indent = "  " * (level + 1)
        closing = "  " * level
        body = ",\n".join(
            f"{indent}{render_json(item, level=level + 1)}" for item in value
        )
        return f"[\n{body}\n{closing}]"
    if isinstance(value, dict):
        if not value:
            return "{}"
        indent = "  " * (level + 1)
        closing = "  " * level
        body = ",\n".join(
            f"{indent}{json.dumps(key, ensure_ascii=False)}: "
            f"{render_json(value[key], level=level + 1)}"
            for key in object_keys(value, top_level=top_level)
        )
        return f"{{\n{body}\n{closing}}}"
    raise FormatterError(
        "ADUC-FMT-INTERNAL-001",
        f"Unsupported internal JSON value type: {type(value).__name__}.",
    )


def array_snapshot(value: Any, path: tuple[Any, ...] = ()) -> dict[tuple[Any, ...], Any]:
    arrays: dict[tuple[Any, ...], Any] = {}
    if isinstance(value, list):
        arrays[path] = value
        for index, child in enumerate(value):
            arrays.update(array_snapshot(child, path + (("index", index),)))
    elif isinstance(value, dict):
        for key, child in value.items():
            arrays.update(array_snapshot(child, path + (("key", key),)))
    return arrays


def validation_summary(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "valid": bool(report.get("valid")),
        "outcome": report.get("outcome"),
        "summary": report.get("summary", {}),
        "diagnosticCodes": sorted(
            {str(item.get("code")) for item in report.get("diagnostics", []) if isinstance(item, dict)}
        ),
    }


def diagnostic(code: str, message: str, *, path: str = "$") -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def base_report(source: str, output: str | None) -> dict[str, Any]:
    return {
        "reportVersion": REPORT_VERSION,
        "formatterVersion": FORMATTER_VERSION,
        "source": source,
        "output": output,
        "outcome": "blocked",
        "formatted": False,
        "contractId": None,
        "ordering": {
            "topLevel": list(TOP_LEVEL_ORDER),
            "nestedObjects": "unicode-code-point",
            "arrays": "preserved",
        },
        "inputValidation": None,
        "outputValidation": None,
        "preservation": {
            "semanticEqual": False,
            "arrayOrderPreserved": False,
            "duplicateKeysRejected": True,
        },
        "bytes": {"input": None, "output": None, "sha256": None},
        "diagnostics": [],
    }


def format_loaded(
    source: str,
    raw: str,
    document: Any,
    decimal_document: Any,
    *,
    output_label: str | None = None,
) -> tuple[bytes | None, dict[str, Any], int]:
    report = base_report(source, output_label)
    report["bytes"]["input"] = len(raw.encode("utf-8"))
    input_validation = aduc_core.validate_contract(document, source=source)
    report["inputValidation"] = validation_summary(input_validation)
    if isinstance(document, dict) and isinstance(document.get("aduc"), dict):
        report["contractId"] = document["aduc"].get("contractId")

    if not input_validation.get("valid"):
        report["diagnostics"].append(
            diagnostic("ADUC-FMT-VALIDATION-001", "Input contract is blocked by the accepted Core validation pipeline.")
        )
        return None, report, EXIT_BLOCKED

    rendered = render_json(decimal_document, top_level=True) + "\n"
    encoded = rendered.encode("utf-8")
    if len(encoded) > MAX_OUTPUT_BYTES:
        report["diagnostics"].append(
            diagnostic("ADUC-FMT-OUTPUT-004", f"Formatted output exceeds {MAX_OUTPUT_BYTES} bytes.")
        )
        return None, report, EXIT_BLOCKED

    try:
        output_document = parse_json_text(rendered)
        decimal_output_document = parse_json_text(rendered, decimal_numbers=True)
    except FormatterError as exc:
        report["diagnostics"].append(diagnostic("ADUC-FMT-INTERNAL-002", exc.message, path=exc.path))
        return None, report, EXIT_BLOCKED

    semantic_equal = decimal_document == decimal_output_document
    arrays_equal = array_snapshot(decimal_document) == array_snapshot(decimal_output_document)
    report["preservation"]["semanticEqual"] = semantic_equal
    report["preservation"]["arrayOrderPreserved"] = arrays_equal
    if not semantic_equal or not arrays_equal:
        report["diagnostics"].append(
            diagnostic("ADUC-FMT-PRESERVE-001", "Formatting did not preserve the complete JSON value and array order.")
        )
        return None, report, EXIT_BLOCKED

    output_validation = aduc_core.validate_contract(output_document, source=output_label or "<formatted>")
    report["outputValidation"] = validation_summary(output_validation)
    if not output_validation.get("valid"):
        report["diagnostics"].append(
            diagnostic("ADUC-FMT-VALIDATION-002", "Formatted output failed the accepted Core validation pipeline.")
        )
        return None, report, EXIT_BLOCKED

    report["bytes"]["output"] = len(encoded)
    report["bytes"]["sha256"] = hashlib.sha256(encoded).hexdigest()
    report["formatted"] = True
    if output_validation.get("outcome") == "requiresHumanReview":
        report["outcome"] = "formattedRequiresHumanReview"
        return encoded, report, EXIT_HUMAN_REVIEW
    report["outcome"] = "formatted"
    return encoded, report, EXIT_FORMATTED


def format_path(input_path: Path, output_path: Path, *, force: bool = False) -> tuple[dict[str, Any], int]:
    report = base_report(str(input_path), str(output_path))
    try:
        if input_path.resolve() == output_path.resolve():
            raise FormatterError(
                "ADUC-FMT-OUTPUT-003",
                "Input and output paths must be different.",
                usage=True,
            )
        if output_path.exists() and not force:
            raise FormatterError(
                "ADUC-FMT-OUTPUT-002",
                "Output file already exists; pass --force to replace it.",
                usage=True,
            )
        if not output_path.parent.exists():
            raise FormatterError(
                "ADUC-FMT-OUTPUT-001",
                "Output directory does not exist.",
                usage=True,
            )
        raw, document, decimal_document = load_input(input_path)
        encoded, report, exit_code = format_loaded(
            str(input_path),
            raw,
            document,
            decimal_document,
            output_label=str(output_path),
        )
        if encoded is None:
            return report, exit_code
        write_atomic(output_path, encoded, force=force)
        return report, exit_code
    except FormatterError as exc:
        if report.get("formatted"):
            report["formatted"] = False
            report["bytes"]["output"] = None
            report["bytes"]["sha256"] = None
        report["outcome"] = "usageError" if exc.usage else "blocked"
        report["diagnostics"].append(diagnostic(exc.code, exc.message, path=exc.path))
        return report, EXIT_USAGE if exc.usage else EXIT_BLOCKED


def write_atomic(path: Path, payload: bytes, *, force: bool) -> None:
    fd = -1
    temp_name = ""
    try:
        fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
        with os.fdopen(fd, "wb") as stream:
            fd = -1
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        if force:
            os.replace(temp_name, path)
            temp_name = ""
        else:
            try:
                os.link(temp_name, path, follow_symlinks=False)
            except FileExistsError as exc:
                raise FormatterError(
                    "ADUC-FMT-OUTPUT-002",
                    "Output file appeared during formatting; pass --force to replace it.",
                    usage=True,
                ) from exc
            os.unlink(temp_name)
            temp_name = ""
    except FormatterError:
        raise
    except OSError as exc:
        raise FormatterError("ADUC-FMT-OUTPUT-001", f"Unable to write formatted output: {exc}") from exc
    finally:
        if fd >= 0:
            os.close(fd)
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)


def render_report_text(report: dict[str, Any]) -> str:
    lines = [f"FORMAT {str(report['outcome']).upper()}"]
    lines.append(f"Source: {report['source']}")
    if report.get("output"):
        lines.append(f"Output: {report['output']}")
    if report.get("contractId"):
        lines.append(f"Contract: {report['contractId']}")
    for item in report.get("diagnostics", []):
        lines.append(f"{item['code']} {item['path']}: {item['message']}")
    if report.get("formatted"):
        lines.append(
            f"Bytes: {report['bytes']['output']} sha256:{report['bytes']['sha256']}"
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path, help="Complete ADUC Core contract to format")
    parser.add_argument("--output", "-o", type=Path, required=True, help="Destination JSON file")
    parser.add_argument("--force", action="store_true", help="Replace an existing destination")
    parser.add_argument(
        "--report-format",
        choices=("text", "json"),
        default="text",
        help="Formatting report representation",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report, exit_code = format_path(args.contract, args.output, force=args.force)
    if args.report_format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(render_report_text(report))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
