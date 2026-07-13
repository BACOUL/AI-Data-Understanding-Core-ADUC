#!/usr/bin/env python3
"""Validate ADUC uncertainty, propagation, missingness, censoring, and DQV-like quality cases."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "examples" / "uncertainty"
UNITLESS = "http://qudt.org/vocab/unit/UNITLESS"
TYPES = {"standard", "expanded", "relativeStandard", "asymmetric", "interval", "distribution", "categorical", "unknown"}
AUTHORITIES = {"inferred", "reviewed", "verified", "canonical"}
ROLES = {"ordinary", "absolute", "difference"}
INTERVALS = {"coverage", "frequentistConfidence", "bayesianCredible", "prediction"}
DEPENDENCE = {"independent", "correlated", "unknown"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def err(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def iri(value: Any) -> bool:
    return isinstance(value, str) and bool(value) and bool(urlparse(value).scheme)


def number(value: Any, name: str) -> Decimal:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a decimal string")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"{name} is not a valid decimal string") from exc
    if not result.is_finite():
        raise ValueError(f"{name} must be finite")
    return result


def fmt(value: Decimal) -> str:
    with localcontext() as context:
        context.prec = 60
        result = value.quantize(Decimal("1e-15"))
    text = f"{result:f}".rstrip("0").rstrip(".")
    return text or "0"


def authority(record: dict[str, Any], prefix: str) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    level = record.get("authorityLevel")
    if level not in AUTHORITIES:
        errors.append(err(f"{prefix}-001", "unsupported authorityLevel"))
    if not iri(record.get("assertedBy")):
        errors.append(err(f"{prefix}-001", "assertedBy must be an absolute IRI"))
    evidence = record.get("evidence")
    if not isinstance(evidence, list) or not evidence or not all(iri(item) for item in evidence):
        errors.append(err(f"{prefix}-001", "non-empty IRI evidence is required"))
    if level == "inferred":
        confidence = record.get("epistemicConfidence")
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1 or not iri(record.get("confidenceMethod")):
            errors.append(err(f"{prefix}-002", "inferred assertion requires calibrated epistemic confidence"))
    elif "epistemicConfidence" in record:
        errors.append(err(f"{prefix}-002", "epistemic confidence is reserved for inferred assertions"))
    if record.get("conflictState", "clear") not in {"clear", "contested"}:
        errors.append(err(f"{prefix}-001", "unsupported conflictState"))
    if record.get("lifecycleState", "active") not in {"active", "deprecated"}:
        errors.append(err(f"{prefix}-001", "unsupported lifecycleState"))
    return errors


def nonnegative(record: dict[str, Any], field: str, code: str) -> tuple[Decimal | None, list[dict[str, str]]]:
    try:
        value = number(record.get(field), field)
        if value < 0:
            raise ValueError(f"{field} must not be negative")
        return value, []
    except ValueError as exc:
        return None, [err(code, str(exc))]


def validate_uncertainty(raw: Any) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    if not isinstance(raw, dict):
        return None, [err("ADUC-UNC-001", "uncertainty assertion must be an object")]
    errors: list[dict[str, str]] = []
    for field in ("uncertaintyId", "targetBinding", "quantityKind", "method", "provenanceActivity"):
        if not iri(raw.get(field)):
            errors.append(err("ADUC-UNC-001", f"{field} must be an absolute IRI"))
    kind = raw.get("uncertaintyType")
    if kind not in TYPES:
        return raw, errors + [err("ADUC-UNC-003", "unsupported uncertaintyType")]
    if raw.get("quantityRole") not in ROLES:
        errors.append(err("ADUC-UNC-001", "unsupported quantityRole"))
    errors.extend(authority(raw, "ADUC-UNC"))
    if raw.get("assumeExactFromAuthority") is True:
        errors.append(err("ADUC-UNC-002", "authority must not imply zero statistical uncertainty"))
    if raw.get("uncertaintyBasis") == "displayFormatting":
        errors.append(err("ADUC-UNC-009", "display formatting does not establish uncertainty"))
    unit = raw.get("unit")
    if kind not in {"categorical", "unknown"} and not iri(unit):
        errors.append(err("ADUC-UNC-004", "numeric uncertainty requires a global unit"))
    if kind == "relativeStandard" and unit != UNITLESS:
        errors.append(err("ADUC-UNC-004", "relative uncertainty must be explicitly unitless"))

    if kind == "standard":
        value, found = nonnegative(raw, "standardUncertainty", "ADUC-UNC-005")
        errors += found
        if value == 0 and raw.get("exactByDefinition") is not True:
            errors.append(err("ADUC-UNC-002", "zero uncertainty requires exactByDefinition"))
    elif kind == "expanded":
        value, found = nonnegative(raw, "expandedUncertainty", "ADUC-UNC-005")
        errors += found
        try:
            factor = number(raw.get("coverageFactor"), "coverageFactor")
            probability = number(raw.get("coverageProbability"), "coverageProbability")
            if factor <= 0 or not Decimal("0") < probability <= Decimal("1"):
                raise ValueError("invalid coverage factor or probability")
        except ValueError as exc:
            errors.append(err("ADUC-UNC-006", str(exc)))
        if raw.get("intervalInterpretation") not in INTERVALS or not iri(raw.get("coverageMethod")):
            errors.append(err("ADUC-UNC-006", "coverage interpretation and method are required"))
        if value == 0 and raw.get("exactByDefinition") is not True:
            errors.append(err("ADUC-UNC-002", "zero uncertainty requires exactByDefinition"))
    elif kind == "relativeStandard":
        errors += nonnegative(raw, "relativeStandardUncertainty", "ADUC-UNC-005")[1]
    elif kind == "asymmetric":
        lower, low_errors = nonnegative(raw, "lowerDeviation", "ADUC-UNC-005")
        upper, high_errors = nonnegative(raw, "upperDeviation", "ADUC-UNC-005")
        errors += low_errors + high_errors
        if lower == 0 and upper == 0 and raw.get("exactByDefinition") is not True:
            errors.append(err("ADUC-UNC-002", "zero uncertainty requires exactByDefinition"))
    elif kind == "interval":
        try:
            lower = number(raw.get("lowerBound"), "lowerBound")
            upper = number(raw.get("upperBound"), "upperBound")
            probability = number(raw.get("coverageProbability"), "coverageProbability")
            if lower >= upper or not Decimal("0") < probability <= Decimal("1"):
                raise ValueError("invalid interval bounds or probability")
        except ValueError as exc:
            errors.append(err("ADUC-UNC-006", str(exc)))
        if raw.get("intervalInterpretation") not in INTERVALS or not iri(raw.get("coverageMethod")):
            errors.append(err("ADUC-UNC-006", "interval interpretation and method are required"))
    elif kind == "distribution":
        family, params = raw.get("distributionFamily"), raw.get("parameters")
        if not iri(family) or not isinstance(params, dict):
            errors.append(err("ADUC-UNC-007", "distribution family and parameters are required"))
        elif family == "urn:aduc:distribution:normal":
            try:
                number(params.get("mean"), "mean")
                if number(params.get("standardDeviation"), "standardDeviation") < 0:
                    raise ValueError("standardDeviation must not be negative")
            except ValueError as exc:
                errors.append(err("ADUC-UNC-007", str(exc)))
        elif family == "urn:aduc:distribution:rectangular":
            try:
                if number(params.get("lower"), "lower") >= number(params.get("upper"), "upper"):
                    raise ValueError("rectangular bounds are invalid")
            except ValueError as exc:
                errors.append(err("ADUC-UNC-007", str(exc)))
    elif kind == "categorical":
        categories = raw.get("categories")
        total = Decimal("0")
        if not isinstance(categories, list) or len(categories) < 2:
            errors.append(err("ADUC-UNC-008", "at least two categories are required"))
        else:
            for item in categories:
                try:
                    if not isinstance(item, dict) or not iri(item.get("category")):
                        raise ValueError("category must be an absolute IRI")
                    probability = number(item.get("probability"), "probability")
                    if not Decimal("0") <= probability <= Decimal("1"):
                        raise ValueError("probability must be in [0,1]")
                    total += probability
                except ValueError as exc:
                    errors.append(err("ADUC-UNC-008", str(exc)))
            if total != 1:
                errors.append(err("ADUC-UNC-008", "categorical probabilities must sum exactly to 1"))
        calibration = raw.get("calibration")
        if not isinstance(calibration, dict) or not iri(calibration.get("method")) or not iri(calibration.get("evaluationDatasetBinding")) or not isinstance(calibration.get("evidence"), list) or not calibration.get("evidence") or not all(iri(item) for item in calibration.get("evidence", [])):
            errors.append(err("ADUC-UNC-010", "calibration method, dataset binding, and evidence are required"))
    elif kind == "unknown":
        if not isinstance(raw.get("unknownReason"), str) or not raw.get("unknownReason"):
            errors.append(err("ADUC-UNC-011", "unknown uncertainty requires a reason"))
        numeric_fields = {"standardUncertainty", "expandedUncertainty", "relativeStandardUncertainty", "lowerDeviation", "upperDeviation", "lowerBound", "upperBound", "coverageProbability", "parameters", "categories"}
        if any(field in raw for field in numeric_fields):
            errors.append(err("ADUC-UNC-011", "unknown uncertainty must not fabricate numeric parameters"))
    return raw, errors


def validate_state(raw: Any) -> list[dict[str, str]]:
    if raw is None:
        return []
    if not isinstance(raw, dict):
        return [err("ADUC-DATA-001", "observationState must be an object")]
    state = raw.get("state")
    if state == "observed":
        return [] if "value" in raw else [err("ADUC-DATA-001", "observed state requires value")]
    if state == "missing":
        return [] if "value" not in raw and isinstance(raw.get("missingReason"), str) else [err("ADUC-DATA-002", "missing state requires reason and no value")]
    if state in {"censoredBelow", "censoredAbove"}:
        errors = []
        if "value" in raw:
            errors.append(err("ADUC-DATA-003", "censored state must not expose an exact value"))
        try:
            number(raw.get("detectionLimit"), "detectionLimit")
        except ValueError as exc:
            errors.append(err("ADUC-DATA-003", str(exc)))
        if not iri(raw.get("unit")) or not iri(raw.get("method")):
            errors.append(err("ADUC-DATA-003", "censoring requires unit and method"))
        return errors
    if state == "intervalCensored":
        errors = []
        if "value" in raw:
            errors.append(err("ADUC-DATA-003", "interval censoring must not expose an exact value"))
        try:
            if number(raw.get("lowerLimit"), "lowerLimit") >= number(raw.get("upperLimit"), "upperLimit"):
                raise ValueError("interval censoring bounds are invalid")
        except ValueError as exc:
            errors.append(err("ADUC-DATA-003", str(exc)))
        if not iri(raw.get("unit")) or not iri(raw.get("method")):
            errors.append(err("ADUC-DATA-003", "interval censoring requires unit and method"))
        return errors
    return [err("ADUC-DATA-001", "unsupported observation state")]


def dependence(raw: Any) -> tuple[Decimal | None, list[dict[str, str]]]:
    if not isinstance(raw, dict) or raw.get("type") not in DEPENDENCE:
        return None, [err("ADUC-PROP-001", "dependence declaration is required")]
    evidence = raw.get("evidence")
    if not isinstance(evidence, list) or not evidence or not all(iri(item) for item in evidence):
        return None, [err("ADUC-PROP-001", "dependence requires evidence")]
    if raw["type"] == "unknown":
        return None, [err("ADUC-PROP-002", "unknown dependence blocks propagation")]
    if raw["type"] == "independent":
        return Decimal("0"), []
    try:
        rho = number(raw.get("correlationCoefficient"), "correlationCoefficient")
        if not Decimal("-1") <= rho <= Decimal("1"):
            raise ValueError("correlationCoefficient must be in [-1,1]")
        return rho, []
    except ValueError as exc:
        return None, [err("ADUC-PROP-001", str(exc))]


def validate_quality(raw: Any) -> list[dict[str, str]]:
    if not isinstance(raw, dict):
        return [err("ADUC-DQV-001", "quality bundle must be an object")]
    errors: list[dict[str, str]] = []
    for field in ("bundleId", "computedOn", "provenanceActivity"):
        if not iri(raw.get(field)):
            errors.append(err("ADUC-DQV-001", f"{field} must be an absolute IRI"))
    errors += authority(raw, "ADUC-DQV")
    state = raw.get("disclosureState")
    required = raw.get("requiredMetrics", [])
    measurements = raw.get("measurements", [])
    missing = raw.get("missingMetrics", [])
    redacted = raw.get("redactedMetrics", [])
    if state not in {"complete", "partial", "redacted", "unknown"}:
        errors.append(err("ADUC-DQV-002", "unsupported disclosureState"))
    if not isinstance(required, list) or not all(iri(item) for item in required):
        errors.append(err("ADUC-DQV-001", "requiredMetrics must be an IRI array")); required = []
    if not isinstance(measurements, list):
        errors.append(err("ADUC-DQV-001", "measurements must be an array")); measurements = []
    if not isinstance(missing, list) or not all(iri(item) for item in missing):
        errors.append(err("ADUC-DQV-002", "missingMetrics must be an IRI array")); missing = []
    if not isinstance(redacted, list) or not all(iri(item) for item in redacted):
        errors.append(err("ADUC-DQV-002", "redactedMetrics must be an IRI array")); redacted = []
    seen: set[str] = set()
    for item in measurements:
        if not isinstance(item, dict):
            errors.append(err("ADUC-DQV-001", "quality measurement must be an object")); continue
        for field in ("measurementId", "metric", "dimension", "computedOn", "method", "provenanceActivity"):
            if not iri(item.get(field)):
                errors.append(err("ADUC-DQV-001", f"quality measurement {field} must be an absolute IRI"))
        metric = item.get("metric")
        if isinstance(metric, str):
            if metric in seen:
                errors.append(err("ADUC-DQV-001", f"duplicate quality metric: {metric}"))
            seen.add(metric)
        if "value" not in item:
            errors.append(err("ADUC-DQV-001", "quality measurement requires value"))
        errors += authority(item, "ADUC-DQV")
    unresolved = set(required) - seen
    if state == "complete" and (unresolved or missing or redacted):
        errors.append(err("ADUC-DQV-003", "complete disclosure conflicts with missing or redacted metrics"))
    if state == "partial" and not (missing or unresolved):
        errors.append(err("ADUC-DQV-002", "partial disclosure must identify missing metrics"))
    if state == "redacted" and (not redacted or not iri(raw.get("redactionPolicy"))):
        errors.append(err("ADUC-DQV-004", "redacted quality requires metrics and policy"))
    if set(missing) & set(redacted):
        errors.append(err("ADUC-DQV-002", "metric cannot be both missing and redacted"))
    return errors


def magnitude(record: dict[str, Any]) -> tuple[str, Decimal] | None:
    fields = {"standard": "standardUncertainty", "expanded": "expandedUncertainty", "relativeStandard": "relativeStandardUncertainty"}
    field = fields.get(record.get("uncertaintyType"))
    return None if field is None else (field, number(record.get(field), field))


def evaluate(case: Any) -> dict[str, Any]:
    if not isinstance(case, dict):
        return {"valid": False, "errors": [err("ADUC-UNC-001", "case must be an object")]}
    action, errors = case.get("action"), []
    if action == "validate":
        record, found = validate_uncertainty(case.get("uncertainty")); errors += found + validate_state(case.get("observationState"))
        usable = bool(record) and record.get("conflictState", "clear") == "clear" and record.get("lifecycleState", "active") == "active"
        return {"valid": not errors, "usable": usable and not errors, "errors": errors}
    if action == "quality":
        errors = validate_quality(case.get("qualityBundle"))
        return {"valid": not errors, "errors": errors}
    if action == "resolution":
        for field in ("targetBinding", "quantityKind", "unit", "method", "provenanceActivity"):
            if not iri(case.get(field)):
                errors.append(err("ADUC-UNC-001", f"{field} must be an absolute IRI"))
        if case.get("distribution") != "rectangular":
            errors.append(err("ADUC-UNC-007", "resolution contribution requires rectangular distribution"))
        try:
            resolution = number(case.get("resolution"), "resolution")
            if resolution <= 0: raise ValueError("resolution must be positive")
        except ValueError as exc:
            errors.append(err("ADUC-UNC-005", str(exc))); resolution = Decimal("0")
        if errors: return {"valid": False, "errors": errors}
        with localcontext() as context:
            context.prec = 60
            value = resolution / Decimal(12).sqrt()
        return {"valid": True, "result": {"uncertaintyType": "standard", "standardUncertainty": fmt(value), "unit": case["unit"], "method": case["method"], "provenanceActivity": case["provenanceActivity"]}, "errors": []}
    if action == "convert":
        record, found = validate_uncertainty(case.get("input")); errors += found
        conversion, output = case.get("conversion"), case.get("output")
        if not isinstance(conversion, dict) or not isinstance(output, dict):
            return {"valid": False, "errors": errors + [err("ADUC-PROP-003", "conversion and output are required")]}
        try:
            multiplier, offset = number(conversion.get("multiplier"), "multiplier"), number(conversion.get("offset", "0"), "offset")
        except ValueError as exc:
            errors.append(err("ADUC-PROP-003", str(exc))); multiplier = offset = Decimal("0")
        if conversion.get("uncertaintyRule") != "scale-only":
            errors.append(err("ADUC-PROP-004", "affine offset must not be applied to uncertainty"))
        if not iri(conversion.get("method")) or not iri(output.get("unit")) or not iri(output.get("provenanceActivity")):
            errors.append(err("ADUC-PROP-003", "method, output unit, and provenance are required"))
        info = magnitude(record) if record else None
        if info is None:
            errors.append(err("ADUC-PROP-003", "unsupported conversion uncertainty type"))
        if errors: return {"valid": False, "errors": errors}
        field, value = info
        if record["uncertaintyType"] == "relativeStandard":
            if offset != 0: return {"valid": False, "errors": [err("ADUC-PROP-004", "relative uncertainty is not preserved through affine conversion")]}
            result = value
        else:
            result = abs(multiplier) * value
        return {"valid": True, "result": {"uncertaintyType": record["uncertaintyType"], field: fmt(result), "unit": output["unit"], "provenanceActivity": output["provenanceActivity"], "conversionMethod": conversion["method"]}, "errors": []}
    if action in {"propagate-add", "propagate-multiply"}:
        inputs = case.get("inputs")
        if not isinstance(inputs, list) or len(inputs) != 2:
            return {"valid": False, "errors": [err("ADUC-PROP-001", "exactly two inputs are required")]}
        expected = "standard" if action == "propagate-add" else "relativeStandard"
        records, values = [], []
        for item in inputs:
            record, found = validate_uncertainty(item); errors += found
            if record:
                records.append(record)
                if record.get("uncertaintyType") != expected:
                    errors.append(err("ADUC-PROP-003", f"{action} requires {expected} inputs"))
                else:
                    values.append(magnitude(record)[1])
        rho, found = dependence(case.get("dependence")); errors += found
        output = case.get("output")
        if not isinstance(output, dict) or not iri(output.get("provenanceActivity")):
            errors.append(err("ADUC-PROP-003", "output provenance is required"))
        if action == "propagate-add" and len(records) == 2 and records[0].get("unit") != records[1].get("unit"):
            errors.append(err("ADUC-UNC-004", "additive propagation requires identical reference units"))
        if errors or len(values) != 2 or rho is None:
            return {"valid": False, "errors": errors}
        variance = values[0] ** 2 + values[1] ** 2 + Decimal("2") * rho * values[0] * values[1]
        if variance < 0:
            return {"valid": False, "errors": [err("ADUC-PROP-001", "negative propagated variance")]}
        with localcontext() as context:
            context.prec = 60
            result = variance.sqrt()
        field = "standardUncertainty" if action == "propagate-add" else "relativeStandardUncertainty"
        unit = records[0]["unit"] if action == "propagate-add" else UNITLESS
        return {"valid": True, "result": {"uncertaintyType": expected, field: fmt(result), "unit": unit, "provenanceActivity": output["provenanceActivity"], "dependenceType": case["dependence"]["type"]}, "errors": []}
    return {"valid": False, "errors": [err("ADUC-UNC-001", "unsupported action")]}


def patch(document: dict[str, Any], operations: Any) -> dict[str, Any]:
    result = copy.deepcopy(document)
    if not isinstance(operations, list):
        raise ValueError("patch must be an array")
    for operation in operations:
        path = operation.get("path") if isinstance(operation, dict) else None
        if operation.get("op") not in {"set", "remove"} or not isinstance(path, list) or not path:
            raise ValueError("invalid patch operation")
        target: Any = result
        for part in path[:-1]:
            target = target[part]
        leaf = path[-1]
        if operation["op"] == "set":
            target[leaf] = operation.get("value")
        elif isinstance(target, list):
            target.pop(leaf)
        else:
            target.pop(leaf, None)
    return result


def materialize(spec: dict[str, Any], references: dict[str, dict[str, Any]]) -> dict[str, Any]:
    base = copy.deepcopy(references[spec["baseCaseId"]]); base.pop("expected", None)
    base["caseId"] = spec["caseId"]
    result = patch(base, spec.get("patch", []))
    result["expectedErrorCode"] = spec.get("expectedErrorCode")
    return result


def suites(reference_path: Path, invalid_path: Path) -> dict[str, Any]:
    references = load(reference_path).get("cases", [])
    index = {case["caseId"]: case for case in references}
    invalid_specs = load(invalid_path).get("cases", [])
    failures, accepted, rejected = [], 0, 0
    for case in references:
        result = evaluate(case)
        if not result.get("valid"):
            failures.append(f"reference {case['caseId']} failed: {result.get('errors')}"); continue
        before = len(failures)
        for key, expected in case.get("expected", {}).items():
            if result.get(key) != expected:
                failures.append(f"reference {case['caseId']} expected {key}={expected!r}, got {result.get(key)!r}")
        if len(failures) == before:
            accepted += 1
    for specification in invalid_specs:
        try:
            case = materialize(specification, index)
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            failures.append(f"invalid {specification.get('caseId')} cannot be materialized: {exc}"); continue
        result = evaluate(case)
        codes = {item.get("code") for item in result.get("errors", [])}
        if result.get("valid"):
            failures.append(f"invalid {case['caseId']} was accepted")
        elif case.get("expectedErrorCode") not in codes:
            failures.append(f"invalid {case['caseId']} expected {case.get('expectedErrorCode')}, got {sorted(codes)}")
        else:
            rejected += 1
    return {"ok": not failures, "referenceAccepted": accepted, "invalidRejected": rejected, "failures": failures}


run_suites = suites
evaluate_case = evaluate
materialize_invalid_case = materialize


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", nargs="?", type=Path, default=DEFAULT / "reference-cases.json")
    parser.add_argument("invalid", nargs="?", type=Path, default=DEFAULT / "invalid-cases.json")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    try:
        report = suites(args.reference, args.invalid)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ADUC-UNC-IO: {exc}", file=sys.stderr); return 2
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Validated {report['referenceAccepted']} reference cases and rejected {report['invalidRejected']} counterexamples.")
        for failure in report["failures"]: print(f"- {failure}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
