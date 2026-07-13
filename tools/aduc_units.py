#!/usr/bin/env python3
"""Evaluate ADUC unit compatibility and deterministic reference conversions."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXAMPLES = ROOT / "examples" / "units"
HEX_64 = re.compile(r"^[0-9a-f]{64}$")
GLOBAL_SCHEMES = {"http", "https", "urn"}
CONVERTIBLE_STATES = {"known", "unitless"}
SUPPORTED_ROLES = {"ordinary", "absolute", "difference"}
SUPPORTED_CONVERSIONS = {"identity", "multiplicative", "affine"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_local_path(root: Path, value: str) -> Path | None:
    parsed = urlparse(value)
    if parsed.scheme or parsed.netloc:
        return None
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def error(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def is_global_identifier(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    parsed = urlparse(value)
    return parsed.scheme.lower() in GLOBAL_SCHEMES


def decimal_fraction(value: Any) -> Fraction:
    if isinstance(value, dict):
        numerator = value.get("numerator")
        denominator = value.get("denominator")
        if not isinstance(numerator, str) or not isinstance(denominator, str):
            raise ValueError("rational values require string numerator and denominator")
        result = Fraction(int(numerator), int(denominator))
        if result.denominator == 0:
            raise ValueError("rational denominator must not be zero")
        return result
    if not isinstance(value, str):
        raise ValueError("numeric values must be decimal strings or rational objects")
    try:
        return Fraction(Decimal(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"invalid decimal string: {value}") from exc


def finite_decimal_places(value: Fraction) -> int | None:
    denominator = value.denominator
    twos = 0
    fives = 0
    while denominator % 2 == 0:
        denominator //= 2
        twos += 1
    while denominator % 5 == 0:
        denominator //= 5
        fives += 1
    return max(twos, fives) if denominator == 1 else None


def fraction_to_exact_string(value: Fraction) -> str:
    places = finite_decimal_places(value)
    if places is None:
        return f"{value.numerator}/{value.denominator}"
    scale = 10**places
    scaled = value.numerator * scale // value.denominator
    sign = "-" if scaled < 0 else ""
    digits = str(abs(scaled))
    if places == 0:
        return sign + digits
    digits = digits.rjust(places + 1, "0")
    output = sign + digits[:-places] + "." + digits[-places:]
    output = output.rstrip("0").rstrip(".")
    return output if output not in {"", "-"} else "0"


def round_fraction(value: Fraction, decimal_places: int) -> str:
    with localcontext() as context:
        context.prec = max(80, decimal_places + 40)
        decimal_value = Decimal(value.numerator) / Decimal(value.denominator)
        quantum = Decimal(1).scaleb(-decimal_places)
        rounded = decimal_value.quantize(quantum, rounding=ROUND_HALF_EVEN)
    return f"{rounded:.{decimal_places}f}"


def load_registry(
    registry_ref: Any,
    examples_root: Path,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, list[dict[str, str]]]:
    if not isinstance(registry_ref, dict):
        return None, None, [error("ADUC-CONV-004", "registry reference is required")]
    path_value = registry_ref.get("path")
    expected_digest = registry_ref.get("sha256")
    if not isinstance(path_value, str) or not isinstance(expected_digest, str) or not HEX_64.fullmatch(expected_digest):
        return None, None, [error("ADUC-CONV-004", "registry path and SHA-256 digest are required")]
    path = safe_local_path(examples_root, path_value)
    if path is None or not path.exists():
        return None, None, [error("ADUC-CONV-004", "pinned unit registry is unavailable")]
    actual_digest = sha256_file(path)
    if actual_digest != expected_digest:
        return None, None, [error("ADUC-CONV-004", f"registry digest mismatch: expected {expected_digest}, got {actual_digest}")]
    try:
        registry = load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        return None, None, [error("ADUC-CONV-004", f"registry is not valid JSON: {exc}")]
    if not isinstance(registry, dict):
        return None, None, [error("ADUC-CONV-004", "registry root must be an object")]
    if registry.get("registryId") != registry_ref.get("registryId"):
        return None, None, [error("ADUC-CONV-004", "registry identifier mismatch")]
    if registry.get("registryVersion") != registry_ref.get("registryVersion"):
        return None, None, [error("ADUC-CONV-004", "registry version mismatch")]
    if registry.get("conversionConvention") != "reference=(value+offsetBeforeScale)*multiplier":
        return None, None, [error("ADUC-CONV-004", "unsupported registry conversion convention")]
    units = registry.get("units")
    if not isinstance(units, dict):
        return None, None, [error("ADUC-CONV-004", "registry units must be an object")]
    provenance = {
        "id": registry.get("registryId"),
        "version": registry.get("registryVersion"),
        "sha256": actual_digest,
        "sourceVocabulary": registry.get("sourceVocabulary"),
    }
    return registry, provenance, []


def validate_assertion(
    assertion: Any,
    registry: dict[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, list[dict[str, str]]]:
    errors: list[dict[str, str]] = []
    if not isinstance(assertion, dict):
        return None, None, [error("ADUC-UNIT-004", "unit assertion must be an object")]

    if not assertion.get("sourceBinding") or not isinstance(assertion.get("localReference"), dict):
        errors.append(error("ADUC-UNIT-004", "source binding and structured local reference are required"))

    quantity_kind = assertion.get("quantityKind")
    dimension = assertion.get("dimensionVector")
    role = assertion.get("quantityRole")
    state = assertion.get("unitState")
    if not is_global_identifier(quantity_kind) or not is_global_identifier(dimension):
        errors.append(error("ADUC-UNIT-004", "global quantity kind and dimension vector are required"))
    if role not in SUPPORTED_ROLES:
        errors.append(error("ADUC-UNIT-004", "quantityRole must be ordinary, absolute, or difference"))

    if assertion.get("conflictState", "clear") != "clear" or assertion.get("lifecycleState", "active") != "active":
        errors.append(error("ADUC-CONV-003", "contested or deprecated unit assertion blocks conversion"))

    if state == "contextual":
        errors.append(error("ADUC-CONV-002", "contextual unit requires a dedicated context profile"))
        return assertion, None, errors
    if state in {"unknown", "arbitrary"}:
        errors.append(error("ADUC-CONV-003", f"unit state {state} is not generically convertible"))
        return assertion, None, errors
    if state not in CONVERTIBLE_STATES:
        errors.append(error("ADUC-UNIT-002", "unitState is missing or unsupported"))
        return assertion, None, errors

    unit = assertion.get("unit")
    if not isinstance(unit, dict):
        errors.append(error("ADUC-UNIT-002", "known or unitless assertion requires a unit object"))
        return assertion, None, errors
    identifier = unit.get("identifier")
    if not is_global_identifier(identifier):
        errors.append(error("ADUC-UNIT-003", "global unit identifier is required; local codes and symbols are not identifiers"))
        return assertion, None, errors
    if state == "unitless" and identifier != "http://qudt.org/vocab/unit/UNITLESS":
        errors.append(error("ADUC-UNIT-002", "unitless state requires the explicit unitless identifier"))

    entry = registry.get("units", {}).get(identifier)
    if not isinstance(entry, dict):
        errors.append(error("ADUC-UNIT-001", f"unit identifier is absent from the pinned registry: {identifier}"))
        return assertion, None, errors

    if entry.get("dimensionVector") != dimension:
        errors.append(error("ADUC-UNIT-004", "assertion dimension vector disagrees with registry entry"))
    quantity_kinds = entry.get("quantityKinds")
    if not isinstance(quantity_kinds, list) or quantity_kind not in quantity_kinds:
        errors.append(error("ADUC-UNIT-004", "assertion quantity kind is not supported by the registry entry"))
    conversion = entry.get("conversion")
    if not isinstance(conversion, dict) or conversion.get("type") not in SUPPORTED_CONVERSIONS:
        errors.append(error("ADUC-CONV-001", "registry conversion type is unsupported"))
    try:
        decimal_fraction(conversion.get("multiplier"))
        decimal_fraction(conversion.get("offsetBeforeScale", "0"))
    except ValueError as exc:
        errors.append(error("ADUC-CONV-001", str(exc)))

    return assertion, entry, errors


def validate_rounding(value: Any) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    if not isinstance(value, dict):
        return None, [error("ADUC-CONV-005", "rounding policy is required")]
    mode = value.get("roundingMode")
    places = value.get("decimalPlaces")
    if mode != "half-even" or not isinstance(places, int) or isinstance(places, bool) or not 0 <= places <= 18:
        return None, [error("ADUC-CONV-005", "v0.1 requires half-even rounding and 0 to 18 decimal places")]
    return value, []


def convert_case(case: Any, examples_root: Path = DEFAULT_EXAMPLES) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    if not isinstance(case, dict):
        return {"valid": False, "errors": [error("ADUC-UNIT-004", "case must be an object")]}

    registry, registry_provenance, registry_errors = load_registry(case.get("registry"), examples_root)
    errors.extend(registry_errors)
    if registry is None:
        return {"valid": False, "errors": errors}

    source = case.get("source")
    target = case.get("target")
    if not isinstance(source, dict) or not isinstance(target, dict):
        return {"valid": False, "errors": [error("ADUC-UNIT-004", "source and target objects are required")]}

    source_assertion, source_entry, source_errors = validate_assertion(source.get("assertion"), registry)
    target_assertion, target_entry, target_errors = validate_assertion(target.get("assertion"), registry)
    errors.extend(source_errors)
    errors.extend(target_errors)

    rounding, rounding_errors = validate_rounding(case.get("rounding"))
    errors.extend(rounding_errors)

    uncertainty = source.get("uncertainty")
    if uncertainty is not None:
        if not isinstance(uncertainty, dict) or uncertainty.get("model") != "symmetric-absolute" or not isinstance(uncertainty.get("value"), str):
            errors.append(error("ADUC-UNC-001", "only symmetric-absolute uncertainty is supported in v0.1"))

    if source_assertion and target_assertion:
        if source_assertion.get("dimensionVector") != target_assertion.get("dimensionVector"):
            errors.append(error("ADUC-COMPAT-001", "source and target dimension vectors differ"))
        elif source_assertion.get("quantityKind") != target_assertion.get("quantityKind"):
            errors.append(error("ADUC-COMPAT-002", "source and target quantity kinds differ"))
        elif source_assertion.get("quantityRole") != target_assertion.get("quantityRole"):
            errors.append(error("ADUC-COMPAT-003", "source and target quantity roles differ"))

    if source_entry and target_entry and source_entry.get("referenceUnit") != target_entry.get("referenceUnit"):
        errors.append(error("ADUC-COMPAT-002", "units do not share a common reference unit"))

    unique = {(item["code"], item["message"]): item for item in errors}
    sorted_errors = sorted(unique.values(), key=lambda item: (item["code"], item["message"]))
    if sorted_errors:
        return {"valid": False, "errors": sorted_errors}

    assert source_assertion is not None
    assert target_assertion is not None
    assert source_entry is not None
    assert target_entry is not None
    assert rounding is not None

    try:
        input_value = decimal_fraction(source.get("value"))
        source_conversion = source_entry["conversion"]
        target_conversion = target_entry["conversion"]
        source_multiplier = decimal_fraction(source_conversion["multiplier"])
        target_multiplier = decimal_fraction(target_conversion["multiplier"])
        source_offset = decimal_fraction(source_conversion.get("offsetBeforeScale", "0"))
        target_offset = decimal_fraction(target_conversion.get("offsetBeforeScale", "0"))
    except (KeyError, ValueError) as exc:
        return {"valid": False, "errors": [error("ADUC-CONV-001", str(exc))]}

    role = source_assertion["quantityRole"]
    if role == "difference":
        reference_value = input_value * source_multiplier
        output_value = reference_value / target_multiplier
        formula = "difference-multiplicative-v0.1"
    else:
        reference_value = (input_value + source_offset) * source_multiplier
        output_value = reference_value / target_multiplier - target_offset
        formula = "affine-v0.1" if source_offset or target_offset else "multiplicative-v0.1"

    places = rounding["decimalPlaces"]
    result: dict[str, Any] = {
        "valid": True,
        "errors": [],
        "status": "converted",
        "input": {
            "value": source.get("value"),
            "unit": source_assertion["unit"]["identifier"],
        },
        "output": {
            "exactValue": fraction_to_exact_string(output_value),
            "displayValue": round_fraction(output_value, places),
            "unit": target_assertion["unit"]["identifier"],
        },
        "quantityKind": source_assertion["quantityKind"],
        "quantityRole": role,
        "dimensionVector": source_assertion["dimensionVector"],
        "registry": registry_provenance,
        "formula": formula,
        "rounding": {
            "mode": "half-even",
            "decimalPlaces": places,
        },
        "sourceBinding": source_assertion["sourceBinding"],
        "referenceValue": fraction_to_exact_string(reference_value),
    }

    if uncertainty is not None:
        try:
            input_uncertainty = decimal_fraction(uncertainty["value"])
        except ValueError as exc:
            return {"valid": False, "errors": [error("ADUC-UNC-001", str(exc))]}
        scale = abs(source_multiplier / target_multiplier)
        output_uncertainty = scale * input_uncertainty
        result["uncertainty"] = {
            "model": "symmetric-absolute",
            "exactValue": fraction_to_exact_string(output_uncertainty),
            "displayValue": round_fraction(output_uncertainty, places),
        }

    return result


def expected_matches(report: dict[str, Any], expected: Any) -> bool:
    if not isinstance(expected, dict):
        return True
    output = report.get("output", {})
    uncertainty = report.get("uncertainty", {})
    actual = {
        "status": report.get("status"),
        "exactValue": output.get("exactValue"),
        "displayValue": output.get("displayValue"),
    }
    if "exactUncertainty" in expected:
        actual["exactUncertainty"] = uncertainty.get("exactValue")
    if "displayUncertainty" in expected:
        actual["displayUncertainty"] = uncertainty.get("displayValue")
    return all(actual.get(key) == value for key, value in expected.items())


def evaluate_cases(path: Path, examples_root: Path = DEFAULT_EXAMPLES) -> dict[str, Any]:
    document = load_json(path)
    cases = document.get("cases") if isinstance(document, dict) else None
    if not isinstance(cases, list):
        raise ValueError("case document must contain a cases array")

    results: list[dict[str, Any]] = []
    suite_matches = True
    for case in cases:
        if not isinstance(case, dict) or not isinstance(case.get("caseId"), str):
            raise ValueError("each case requires a string caseId")
        report = convert_case(case, examples_root)
        expected_valid = case.get("expectedValid")
        expected_error = case.get("expectedError")
        codes = {item["code"] for item in report.get("errors", [])}
        matches = report.get("valid") is expected_valid
        if expected_error is not None:
            matches = matches and expected_error in codes
        if expected_valid is True:
            matches = matches and expected_matches(report, case.get("expected"))
        suite_matches = suite_matches and matches
        results.append(
            {
                "caseId": case["caseId"],
                "expectedValid": expected_valid,
                "expectedError": expected_error,
                "matchesExpectation": matches,
                **report,
            }
        )

    return {
        "protocol": "urn:aduc:unit-conversion-evaluation:0.1",
        "caseFile": str(path),
        "valid": suite_matches,
        "results": results,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_files", nargs="+", type=Path)
    parser.add_argument("--examples-root", type=Path, default=DEFAULT_EXAMPLES)
    parser.add_argument("--compact", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        reports = [evaluate_cases(path, args.examples_root) for path in args.case_files]
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, indent=2))
        return 2

    payload = {
        "valid": all(report["valid"] for report in reports),
        "reports": reports,
    }
    if args.compact:
        print(json.dumps(payload, separators=(",", ":"), sort_keys=True))
    else:
        print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if payload["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
