#!/usr/bin/env python3
"""Evaluate ADUC temporal values and deterministic reference alignment."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXAMPLES = ROOT / "examples" / "time"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
RFC3339 = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:(?P<second>\d{2})(?P<fraction>\.\d+)?(?P<offset>Z|[+-]\d{2}:\d{2})$"
)
LOCAL_FORMATS = {
    "%d/%m/%Y %H:%M": (re.compile(r"^(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4}) (?P<hour>\d{2}):(?P<minute>\d{2})$"), "minute"),
    "%Y-%m-%dT%H:%M": (re.compile(r"^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})T(?P<hour>\d{2}):(?P<minute>\d{2})$"), "minute"),
    "%Y-%m-%dT%H:%M:%S": (re.compile(r"^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})T(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})$"), "second"),
}
ROLES = {"observation", "event", "publication", "processing", "validity", "sampling", "aggregation"}
PRECISIONS = {"date", "hour", "minute", "second", "fraction"}
AUTHORITIES = {"inferred", "reviewed", "verified", "canonical"}


def err(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_path(root: Path, value: str) -> Path | None:
    if urlparse(value).scheme:
        return None
    path = (root / value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return None
    return path


def utc_text(value: datetime) -> str:
    value = value.astimezone(timezone.utc)
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


def parse_offset(value: str) -> timedelta:
    if value == "Z":
        return timedelta(0)
    sign = 1 if value[0] == "+" else -1
    hours, minutes = map(int, value[1:].split(":"))
    return sign * timedelta(hours=hours, minutes=minutes)


def parse_rfc3339(value: Any) -> tuple[datetime | None, str | None, list[dict[str, str]]]:
    match = RFC3339.fullmatch(value) if isinstance(value, str) else None
    if not match:
        return None, None, [err("ADUC-TIME-001", "fixed instant requires RFC 3339 with an explicit offset")]
    if match.group("second") == "60":
        return None, None, [err("ADUC-TIME-008", "leap-second processing is outside the v0.1 evaluator")]
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError as exc:
        return None, None, [err("ADUC-TIME-001", f"invalid RFC 3339 value: {exc}")]
    return parsed, "fraction" if match.group("fraction") else "second", []


def parse_local(value: Any, lexical_format: Any) -> tuple[datetime | None, str | None, list[dict[str, str]]]:
    entry = LOCAL_FORMATS.get(lexical_format)
    if entry is None:
        return None, None, [err("ADUC-TIME-002", "unsupported or missing local lexical format")]
    match = entry[0].fullmatch(value) if isinstance(value, str) else None
    if not match:
        return None, None, [err("ADUC-TIME-002", "local value does not match its declared format")]
    parts = {name: int(number) for name, number in match.groupdict(default="0").items()}
    try:
        parsed = datetime(parts["year"], parts["month"], parts["day"], parts.get("hour", 0), parts.get("minute", 0), parts.get("second", 0))
    except ValueError as exc:
        return None, None, [err("ADUC-TIME-002", f"invalid local civil time: {exc}")]
    return parsed, entry[1], []


def load_registry(ref: Any, root: Path) -> tuple[dict[str, Any] | None, dict[str, Any] | None, list[dict[str, str]]]:
    if not isinstance(ref, dict):
        return None, None, [err("ADUC-TZ-001", "timezone registry reference is required")]
    path_value, expected = ref.get("path"), ref.get("sha256")
    if not isinstance(path_value, str) or not isinstance(expected, str) or not HEX64.fullmatch(expected):
        return None, None, [err("ADUC-TZ-001", "registry path and SHA-256 are required")]
    path = safe_path(root, path_value)
    if path is None or not path.exists():
        return None, None, [err("ADUC-TZ-001", "pinned timezone registry is unavailable")]
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        return None, None, [err("ADUC-TZ-001", f"timezone registry digest mismatch: expected {expected}, got {actual}")]
    registry = load_json(path)
    if registry.get("registryId") != ref.get("registryId") or registry.get("registryVersion") != ref.get("registryVersion"):
        return None, None, [err("ADUC-TZ-001", "timezone registry identity or version mismatch")]
    if not isinstance(registry.get("zones"), dict):
        return None, None, [err("ADUC-TZ-001", "timezone registry zones are invalid")]
    provenance = {
        "registryId": registry["registryId"],
        "registryVersion": registry["registryVersion"],
        "sha256": actual,
        "source": registry.get("source"),
        "released": registry.get("released"),
    }
    return registry, provenance, []


def common_errors(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, dict):
        return [err("ADUC-TIME-001", "temporal value must be an object")]
    errors: list[dict[str, str]] = []
    if not value.get("sourceBinding") or not isinstance(value.get("localReference"), dict):
        errors.append(err("ADUC-TIME-009", "source binding and structured local reference are required"))
    if value.get("role") not in ROLES:
        errors.append(err("ADUC-TIME-ROLE-001", "a supported temporal role is required"))
    authority = value.get("authorityStatus")
    if authority not in AUTHORITIES:
        errors.append(err("ADUC-TIME-010", "a supported authority status is required"))
    if value.get("conflictState", "clear") != "clear" or value.get("lifecycleState", "active") != "active":
        errors.append(err("ADUC-TIME-010", "contested or deprecated temporal assertion blocks use"))
    if value.get("consumerUse") == "canonical" and authority != "canonical":
        errors.append(err("ADUC-TIME-010", "non-canonical interpretation cannot be consumed as canonical"))
    return errors


def uncertainty(value: dict[str, Any], instant: datetime) -> tuple[datetime, datetime, list[dict[str, str]]]:
    data = value.get("uncertainty")
    if data is None:
        return instant, instant, []
    if not isinstance(data, dict):
        return instant, instant, [err("ADUC-TIME-007", "temporal uncertainty must be an object")]
    before, after = data.get("beforeSeconds"), data.get("afterSeconds")
    if not isinstance(before, int) or isinstance(before, bool) or before < 0:
        return instant, instant, [err("ADUC-TIME-007", "beforeSeconds must be a non-negative integer")]
    if not isinstance(after, int) or isinstance(after, bool) or after < 0:
        return instant, instant, [err("ADUC-TIME-007", "afterSeconds must be a non-negative integer")]
    return instant - timedelta(seconds=before), instant + timedelta(seconds=after), []


def period_contains(period: dict[str, Any], value: datetime) -> bool:
    for key, lower in (("startUtc", True), ("endUtc", False)):
        lexical = period.get(key)
        if lexical is None:
            continue
        boundary, _, errors = parse_rfc3339(lexical)
        if errors or boundary is None:
            return False
        if (lower and value < boundary) or (not lower and value >= boundary):
            return False
    return True


def instant_result(value: dict[str, Any], instant: datetime, precision: str, provenance: Any = None, **extra: Any) -> dict[str, Any]:
    lower, upper, errors = uncertainty(value, instant)
    if errors:
        return {"valid": False, "errors": errors}
    result = {
        "kind": "instant",
        "role": value["role"],
        "sourceLexicalValue": value.get("lexicalValue"),
        "instantUtc": utc_text(instant),
        "precision": precision,
        "authorityStatus": value["authorityStatus"],
        "uncertaintyStartUtc": utc_text(lower),
        "uncertaintyEndUtc": utc_text(upper),
        "timezoneProvenance": provenance,
        "parser": value.get("parser"),
        "sourceBinding": value.get("sourceBinding"),
        "localReference": value.get("localReference"),
    }
    result.update(extra)
    return {"valid": True, "result": result}


def resolve_fixed(value: dict[str, Any], registry: dict[str, Any], provenance: dict[str, Any]) -> dict[str, Any]:
    errors = common_errors(value)
    instant, parsed_precision, parse_errors = parse_rfc3339(value.get("lexicalValue"))
    errors.extend(parse_errors)
    declared = value.get("precision")
    if declared not in PRECISIONS:
        errors.append(err("ADUC-TIME-006", "temporal precision is required"))
    elif parsed_precision and declared != parsed_precision:
        errors.append(err("ADUC-TIME-006", "declared precision disagrees with lexical precision"))
    if instant is None:
        return {"valid": False, "errors": errors}
    zone_name = value.get("timeZone")
    if zone_name is not None:
        zone = registry["zones"].get(zone_name)
        if not isinstance(zone, dict):
            errors.append(err("ADUC-TZ-002", "annotated timezone is absent from the pinned registry"))
        else:
            offset_match = RFC3339.fullmatch(value["lexicalValue"])
            lexical_offset = offset_match.group("offset") if offset_match else None
            normalized = "+00:00" if lexical_offset == "Z" else lexical_offset
            expected = {p.get("offset") for p in zone.get("periods", []) if period_contains(p, instant)}
            if normalized not in expected:
                errors.append(err("ADUC-TZ-006", "timestamp offset conflicts with named timezone rules"))
    if errors:
        return {"valid": False, "errors": errors}
    return instant_result(value, instant, declared, provenance if zone_name else None, timeZone=zone_name)


def resolve_local(value: dict[str, Any], registry: dict[str, Any], provenance: dict[str, Any]) -> dict[str, Any]:
    errors = common_errors(value)
    if value.get("lexicalFormat") == "%d/%m/%Y %H:%M" and not value.get("locale"):
        errors.append(err("ADUC-TIME-002", "locale is required for locale-specific syntax"))
    local, parsed_precision, parse_errors = parse_local(value.get("lexicalValue"), value.get("lexicalFormat"))
    errors.extend(parse_errors)
    declared = value.get("precision")
    if declared not in PRECISIONS:
        errors.append(err("ADUC-TIME-006", "temporal precision is required"))
    elif parsed_precision and declared != parsed_precision:
        errors.append(err("ADUC-TIME-006", "declared precision disagrees with lexical precision"))
    zone_name = value.get("timeZone")
    if not isinstance(zone_name, str):
        errors.append(err("ADUC-TZ-003" if value.get("utcOffset") else "ADUC-TZ-002", "local date-time requires named timezone evidence"))
        return {"valid": False, "errors": errors}
    zone = registry["zones"].get(zone_name)
    if not isinstance(zone, dict):
        errors.append(err("ADUC-TZ-002", f"timezone is absent from pinned rules: {zone_name}"))
        return {"valid": False, "errors": errors}
    if local is None:
        return {"valid": False, "errors": errors}
    candidates: list[tuple[datetime, str, str | None]] = []
    for period in zone.get("periods", []):
        try:
            candidate = (local - parse_offset(period["offset"])).replace(tzinfo=timezone.utc)
        except (KeyError, ValueError):
            continue
        if period_contains(period, candidate):
            candidates.append((candidate, period["offset"], period.get("abbreviation")))
    candidates = sorted(set(candidates))
    if not candidates:
        errors.append(err("ADUC-TZ-005", "local civil time does not exist in pinned timezone rules"))
        return {"valid": False, "errors": errors}
    if len(candidates) > 1:
        occurrence = value.get("occurrence")
        if occurrence not in {"earlier", "later"}:
            errors.append(err("ADUC-TZ-004", "ambiguous civil time requires earlier or later occurrence"))
            return {"valid": False, "errors": errors}
        chosen = candidates[0] if occurrence == "earlier" else candidates[-1]
    else:
        chosen = candidates[0]
        if value.get("occurrence") is not None:
            errors.append(err("ADUC-TZ-004", "occurrence is only valid for an ambiguous time"))
    if errors:
        return {"valid": False, "errors": errors}
    instant, offset, abbreviation = chosen
    return instant_result(
        value,
        instant,
        declared,
        provenance,
        sourceLexicalFormat=value.get("lexicalFormat"),
        locale=value.get("locale"),
        localDateTime=local.isoformat(timespec="seconds"),
        timeZone=zone_name,
        utcOffset=offset,
        abbreviation=abbreviation,
    )


def resolve_duration(value: dict[str, Any]) -> dict[str, Any]:
    errors = common_errors(value)
    lexical, kind = value.get("lexicalValue"), value.get("kind")
    if kind == "exactDuration":
        match = re.fullmatch(r"P(?:(?P<days>\d+)D)?(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?)?", lexical or "")
        if not match or not any(match.groupdict().values()):
            errors.append(err("ADUC-DURATION-001", "exact duration must use day/hour/minute/second syntax"))
        if errors:
            return {"valid": False, "errors": errors}
        parts = {k: int(v or 0) for k, v in match.groupdict().items()}
        seconds = parts["days"] * 86400 + parts["hours"] * 3600 + parts["minutes"] * 60 + parts["seconds"]
        return {"valid": True, "result": {"kind": kind, "role": value["role"], "sourceLexicalValue": lexical, "exactSeconds": seconds, "authorityStatus": value["authorityStatus"], "sourceBinding": value["sourceBinding"], "localReference": value["localReference"]}}
    if kind == "calendarPeriod":
        if not isinstance(lexical, str) or not re.fullmatch(r"P(?=.*[YM])(?:\d+Y)?(?:\d+M)?", lexical):
            errors.append(err("ADUC-DURATION-002", "calendar period must contain years or months"))
        if value.get("convertToSeconds"):
            errors.append(err("ADUC-DURATION-003", "calendar period cannot become fixed seconds without context"))
        if errors:
            return {"valid": False, "errors": errors}
        return {"valid": True, "result": {"kind": kind, "role": value["role"], "sourceLexicalValue": lexical, "conversionStatus": "contextRequired", "authorityStatus": value["authorityStatus"], "sourceBinding": value["sourceBinding"], "localReference": value["localReference"]}}
    return {"valid": False, "errors": errors + [err("ADUC-DURATION-001", "unsupported duration kind")]}


def resolve_interval(value: dict[str, Any], registry: dict[str, Any], provenance: dict[str, Any]) -> dict[str, Any]:
    errors = common_errors(value)
    if value.get("startBoundary") not in {"inclusive", "exclusive"} or value.get("endBoundary") not in {"inclusive", "exclusive"}:
        errors.append(err("ADUC-INTERVAL-001", "interval boundaries must be explicit"))
    start, end = resolve(value.get("start"), registry, provenance), resolve(value.get("end"), registry, provenance)
    for item in (start, end):
        if not item.get("valid"):
            errors.extend(item.get("errors", []))
    if errors:
        return {"valid": False, "errors": errors}
    start_dt = datetime.fromisoformat(start["result"]["instantUtc"].replace("Z", "+00:00"))
    end_dt = datetime.fromisoformat(end["result"]["instantUtc"].replace("Z", "+00:00"))
    if start_dt > end_dt or (start_dt == end_dt and "exclusive" in {value["startBoundary"], value["endBoundary"]}):
        return {"valid": False, "errors": [err("ADUC-INTERVAL-002", "interval is empty or reversed")]}
    return {"valid": True, "result": {"kind": "interval", "role": value["role"], "startUtc": utc_text(start_dt), "endUtc": utc_text(end_dt), "startBoundary": value["startBoundary"], "endBoundary": value["endBoundary"], "authorityStatus": value["authorityStatus"], "sourceBinding": value["sourceBinding"], "localReference": value["localReference"]}}


def resolve(value: Any, registry: dict[str, Any], provenance: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {"valid": False, "errors": [err("ADUC-TIME-001", "temporal value must be an object")]}
    kind = value.get("kind")
    if kind == "instant":
        return resolve_fixed(value, registry, provenance)
    if kind == "localDateTime":
        return resolve_local(value, registry, provenance)
    if kind in {"exactDuration", "calendarPeriod"}:
        return resolve_duration(value)
    if kind == "interval":
        return resolve_interval(value, registry, provenance)
    return {"valid": False, "errors": [err("ADUC-TIME-001", f"unsupported temporal kind: {kind}")]}


def interval_relation(left: dict[str, Any], right: dict[str, Any]) -> str:
    ls, le = (datetime.fromisoformat(left[k].replace("Z", "+00:00")) for k in ("startUtc", "endUtc"))
    rs, re_ = (datetime.fromisoformat(right[k].replace("Z", "+00:00")) for k in ("startUtc", "endUtc"))
    if ls == rs and le == re_ and left["startBoundary"] == right["startBoundary"] and left["endBoundary"] == right["endBoundary"]:
        return "equal"
    if le < rs:
        return "before"
    if le == rs:
        return "meets"
    if ls > re_:
        return "after"
    if ls == re_:
        return "metBy"
    if ls <= rs and le >= re_:
        return "contains"
    if ls >= rs and le <= re_:
        return "during"
    return "overlaps"


def align(left: dict[str, Any], right: dict[str, Any], required: Any = None) -> dict[str, Any]:
    if left.get("role") != right.get("role"):
        return {"valid": False, "errors": [err("ADUC-TIME-ROLE-001", "temporal roles differ")]}
    if left.get("kind") == right.get("kind") == "instant":
        ls = datetime.fromisoformat(left["uncertaintyStartUtc"].replace("Z", "+00:00"))
        le = datetime.fromisoformat(left["uncertaintyEndUtc"].replace("Z", "+00:00"))
        rs = datetime.fromisoformat(right["uncertaintyStartUtc"].replace("Z", "+00:00"))
        re_ = datetime.fromisoformat(right["uncertaintyEndUtc"].replace("Z", "+00:00"))
        if le < rs:
            relation = "before"
        elif re_ < ls:
            relation = "after"
        elif left["instantUtc"] == right["instantUtc"] and ls == le == rs == re_:
            relation = "equal"
        else:
            relation = "possibleOverlap"
    elif left.get("kind") == right.get("kind") == "interval":
        relation = interval_relation(left, right)
    else:
        return {"valid": False, "errors": [err("ADUC-ALIGN-001", "temporal kinds are not alignable")]}
    if required is not None and relation != required:
        return {"valid": False, "errors": [err("ADUC-ALIGN-003", f"required {required}; actual {relation}")]}
    return {"valid": True, "result": {"relation": relation, "role": left["role"], "left": left, "right": right}}


def evaluate_case(case: Any, examples_root: Path = DEFAULT_EXAMPLES) -> dict[str, Any]:
    if not isinstance(case, dict):
        return {"valid": False, "errors": [err("ADUC-TIME-001", "case must be an object")]}
    registry, provenance, errors = load_registry(case.get("timezoneRegistry"), examples_root)
    if registry is None or provenance is None:
        return {"valid": False, "errors": errors}
    if case.get("operation") == "resolve":
        return resolve(case.get("value"), registry, provenance)
    if case.get("operation") == "align":
        left, right = resolve(case.get("left"), registry, provenance), resolve(case.get("right"), registry, provenance)
        combined = ([] if left.get("valid") else left.get("errors", [])) + ([] if right.get("valid") else right.get("errors", []))
        return {"valid": False, "errors": combined} if combined else align(left["result"], right["result"], case.get("requiredRelation"))
    return {"valid": False, "errors": [err("ADUC-TIME-001", "unsupported operation")]}


def matches(actual: Any, expected: Any) -> bool:
    return all(k in actual and matches(actual[k], v) for k, v in expected.items()) if isinstance(expected, dict) and isinstance(actual, dict) else actual == expected


def evaluate_case_file(path: Path, examples_root: Path = DEFAULT_EXAMPLES) -> tuple[int, list[dict[str, Any]]]:
    document = load_json(path)
    cases = document.get("cases") if isinstance(document, dict) else None
    if not isinstance(cases, list):
        return 1, [{"caseId": None, "passed": False, "message": "case file requires cases array"}]
    shared_registry = document.get("timezoneRegistry")
    failures, reports = 0, []
    for source_case in cases:
        case = dict(source_case)
        case.setdefault("timezoneRegistry", shared_registry)
        actual, expected = evaluate_case(case, examples_root), case.get("expected", {})
        passed = actual.get("valid") == expected.get("valid")
        if passed and expected.get("valid"):
            passed = matches(actual.get("result"), expected.get("result", {}))
        elif passed:
            passed = any(item.get("code") == expected.get("errorCode") for item in actual.get("errors", []))
        failures += not passed
        reports.append({"caseId": case.get("caseId"), "passed": bool(passed), "expected": expected, "actual": actual})
    return failures, reports


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()
    failures, reports = 0, []
    for path in args.files:
        count, items = evaluate_case_file(path)
        failures += count
        reports.extend({"file": str(path), **item} for item in items)
    if args.format == "json":
        print(json.dumps({"ok": failures == 0, "reports": reports}, indent=2, ensure_ascii=False))
    else:
        for report in reports:
            print(f"{'PASS' if report['passed'] else 'FAIL'} {report['file']}::{report['caseId']}")
        print(f"{len(reports) - failures} passed; {failures} failed")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
