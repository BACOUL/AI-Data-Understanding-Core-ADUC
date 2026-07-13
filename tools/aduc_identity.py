#!/usr/bin/env python3
"""Validate ADUC identity records and produce deterministic merge decisions."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXAMPLES = ROOT / "examples" / "identity"

IDENTIFIER_KINDS = {"local", "global", "pseudonymous", "linkageToken"}
AUTHORITY_LEVELS = {"inferred", "reviewed", "verified", "canonical"}
RELATIONS = {"possibleMatch", "sameEntity", "differentEntity", "broaderEntity", "narrowerEntity"}
RELATION_AUTHORITIES = {
    "possibleMatch": {"inferred", "reviewed"},
    "sameEntity": {"verified", "canonical"},
    "differentEntity": {"reviewed", "verified", "canonical"},
    "broaderEntity": {"verified", "canonical"},
    "narrowerEntity": {"verified", "canonical"},
}
PROTECTED_KINDS = {"pseudonymous", "linkageToken"}
HEX_64 = re.compile(r"^[0-9a-f]{64}$")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def error(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def is_iri(value: Any) -> bool:
    return isinstance(value, str) and bool(value) and bool(urlparse(value).scheme)


def parse_instant(value: Any) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError("RFC 3339 instant is required")
    text = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        result = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"invalid RFC 3339 instant: {value}") from exc
    if result.tzinfo is None:
        raise ValueError(f"timezone offset is required: {value}")
    return result.astimezone(timezone.utc)


def parse_validity(value: Any) -> tuple[datetime | None, datetime | None, list[dict[str, str]]]:
    if not isinstance(value, dict):
        return None, None, [error("ADUC-ID-006", "validity object with start is required")]
    try:
        start = parse_instant(value.get("start"))
        end = parse_instant(value["end"]) if "end" in value else None
    except ValueError as exc:
        return None, None, [error("ADUC-ID-006", str(exc))]
    if end is not None and end <= start:
        return None, None, [error("ADUC-ID-006", "validity end must be later than start")]
    return start, end, []


def active(start: datetime, end: datetime | None, instant: datetime) -> bool:
    return start <= instant and (end is None or instant < end)


def overlaps(a_start: datetime, a_end: datetime | None, b_start: datetime, b_end: datetime | None) -> bool:
    latest = max(a_start, b_start)
    if a_end is None and b_end is None:
        return True
    if a_end is None:
        return latest < b_end  # type: ignore[operator]
    if b_end is None:
        return latest < a_end
    return latest < min(a_end, b_end)


def validate_entities(value: Any) -> tuple[dict[str, dict[str, Any]], list[dict[str, str]]]:
    entities: dict[str, dict[str, Any]] = {}
    errors: list[dict[str, str]] = []
    if not isinstance(value, list):
        return entities, [error("ADUC-ID-001", "entities must be an array")]
    for item in value:
        if not isinstance(item, dict) or not is_iri(item.get("entityId")) or not is_iri(item.get("entityType")):
            errors.append(error("ADUC-ID-001", "entityId and entityType must be absolute IRIs"))
            continue
        entity_id = item["entityId"]
        if entity_id in entities:
            errors.append(error("ADUC-ID-001", f"duplicate entityId: {entity_id}"))
            continue
        labels = item.get("labels", [])
        if not isinstance(labels, list) or any(not isinstance(label, dict) or not isinstance(label.get("value"), str) for label in labels):
            errors.append(error("ADUC-ID-001", f"invalid labels for {entity_id}"))
        entities[entity_id] = item
    return entities, errors


def validate_authority(record: dict[str, Any], relation: bool = False) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    authority = record.get("authorityLevel")
    if authority not in AUTHORITY_LEVELS:
        errors.append(error("ADUC-ID-001", "unsupported authorityLevel"))
    confidence = record.get("confidence")
    if authority == "inferred" and (
        not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1
    ):
        errors.append(error("ADUC-ID-001", "inferred assertion requires confidence between 0 and 1"))
    if authority == "canonical" and confidence is not None:
        errors.append(error("ADUC-REL-002" if relation else "ADUC-ID-001", "canonical assertion must not include confidence"))
    if not is_iri(record.get("assertedBy")):
        errors.append(error("ADUC-REL-003" if relation else "ADUC-ID-001", "asserting authority must be an absolute IRI"))
    evidence = record.get("evidence")
    if not isinstance(evidence, list) or not evidence or not all(is_iri(item) for item in evidence):
        errors.append(error("ADUC-REL-003" if relation else "ADUC-ID-001", "non-empty IRI evidence array is required"))
    return errors


def validate_identifier(record: Any, entities: dict[str, dict[str, Any]]) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    if not isinstance(record, dict):
        return None, [error("ADUC-ID-001", "identifier record must be an object")]
    errors: list[dict[str, str]] = []
    kind = record.get("identifierKind")
    if kind == "label":
        return record, [error("ADUC-ID-004", "labels must not be used as identifier records")]
    if kind not in IDENTIFIER_KINDS:
        errors.append(error("ADUC-ID-001", "unsupported identifierKind"))
    if not is_iri(record.get("identifierId")):
        errors.append(error("ADUC-ID-001", "identifierId must be an absolute IRI"))
    for field in ("namespace", "scheme", "issuer", "sourceBinding"):
        if not is_iri(record.get(field)):
            errors.append(error("ADUC-ID-002" if kind == "local" else "ADUC-ID-001", f"{field} must be an absolute IRI"))
    subject = record.get("subjectEntity")
    if subject not in entities:
        errors.append(error("ADUC-ID-001", f"subjectEntity does not exist: {subject}"))
    elif entities[subject].get("entityType") != record.get("entityType"):
        errors.append(error("ADUC-ID-001", "identifier entityType disagrees with entity record"))
    if not is_iri(record.get("entityType")):
        errors.append(error("ADUC-ID-001", "entityType must be an absolute IRI"))
    errors.extend(validate_authority(record))
    if record.get("conflictState", "clear") not in {"clear", "contested"}:
        errors.append(error("ADUC-ID-001", "unsupported conflictState"))
    if record.get("lifecycleState", "active") not in {"active", "deprecated"}:
        errors.append(error("ADUC-ID-001", "unsupported lifecycleState"))
    _, _, validity_errors = parse_validity(record.get("validity"))
    errors.extend(validity_errors)

    if kind == "local":
        if not isinstance(record.get("lexicalValue"), str) or not record.get("lexicalValue"):
            errors.append(error("ADUC-ID-002", "local identifier requires lexicalValue"))
        if not isinstance(record.get("canonicalValue"), str) or not record.get("canonicalValue"):
            errors.append(error("ADUC-ID-002", "local identifier requires canonicalValue"))
    elif kind == "global":
        if not is_iri(record.get("globalIdentifier")):
            errors.append(error("ADUC-ID-003", "globalIdentifier must be an absolute IRI"))
    elif kind in PROTECTED_KINDS:
        if any(field in record for field in ("lexicalValue", "canonicalValue", "rawValue")):
            errors.append(error("ADUC-ID-005", "protected identifier must not expose raw or canonical secret values"))
        if not isinstance(record.get("protectedValue"), str) or not HEX_64.fullmatch(record["protectedValue"]):
            errors.append(error("ADUC-ID-005", "protectedValue must be a lowercase 64-character digest/token"))
        if not is_iri(record.get("protectionMethod")) or not isinstance(record.get("methodVersion"), str):
            errors.append(error("ADUC-ID-005", "protection method and version are required"))
        if not is_iri(record.get("linkageDomain")):
            errors.append(error("ADUC-ID-005", "linkageDomain must be an absolute IRI"))
        purposes = record.get("permittedPurposes")
        if not isinstance(purposes, list) or not purposes or not all(isinstance(item, str) and item for item in purposes):
            errors.append(error("ADUC-ID-005", "protected identifier requires permittedPurposes"))
    return record, errors


def identifier_key(record: dict[str, Any]) -> tuple[Any, ...] | None:
    kind = record.get("identifierKind")
    if kind == "local":
        return (kind, record.get("scheme"), record.get("namespace"), record.get("issuer"), record.get("canonicalValue"))
    if kind == "global":
        return (kind, record.get("globalIdentifier"))
    if kind in PROTECTED_KINDS:
        return (kind, record.get("scheme"), record.get("namespace"), record.get("issuer"), record.get("linkageDomain"), record.get("protectedValue"))
    return None


def validate_relation(record: Any, identifiers: dict[str, dict[str, Any]]) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    if not isinstance(record, dict):
        return None, [error("ADUC-REL-003", "identity relation must be an object")]
    errors: list[dict[str, str]] = []
    if not is_iri(record.get("assertionId")):
        errors.append(error("ADUC-REL-003", "assertionId must be an absolute IRI"))
    subject = record.get("subjectIdentifier")
    obj = record.get("objectIdentifier")
    if subject not in identifiers or obj not in identifiers:
        errors.append(error("ADUC-REL-001", "relation endpoints must reference existing identifier records"))
        return record, errors
    if subject == obj:
        errors.append(error("ADUC-REL-003", "relation endpoints must be distinct identifier records"))
    relation = record.get("relation")
    authority = record.get("authorityLevel")
    if relation not in RELATIONS or authority not in RELATION_AUTHORITIES.get(relation, set()):
        errors.append(error("ADUC-REL-002", f"authority {authority} is not allowed for {relation}"))
    errors.extend(validate_authority(record, relation=True))
    if not is_iri(record.get("method")):
        errors.append(error("ADUC-REL-003", "relation method must be an absolute IRI"))
    _, _, validity_errors = parse_validity(record.get("validity"))
    errors.extend(validity_errors)
    if record.get("conflictState", "clear") not in {"clear", "contested"}:
        errors.append(error("ADUC-REL-003", "unsupported conflictState"))
    if record.get("lifecycleState", "active") not in {"active", "deprecated"}:
        errors.append(error("ADUC-REL-003", "unsupported lifecycleState"))
    if relation == "sameEntity":
        type_a = identifiers[subject].get("entityType")
        type_b = identifiers[obj].get("entityType")
        if type_a != type_b and record.get("typeCompatibilityVerified") is not True:
            errors.append(error("ADUC-REL-005", "sameEntity endpoints have incompatible entity types"))
    return record, errors


def evaluate_case(case: Any) -> dict[str, Any]:
    if not isinstance(case, dict):
        return {"valid": False, "decision": "mergeBlocked", "errors": [error("ADUC-ID-001", "case must be an object")]}
    errors: list[dict[str, str]] = []
    try:
        evaluation_at = parse_instant(case.get("evaluationAt"))
    except ValueError as exc:
        return {"valid": False, "decision": "mergeBlocked", "errors": [error("ADUC-ID-006", str(exc))]}

    entities, entity_errors = validate_entities(case.get("entities"))
    errors.extend(entity_errors)
    identifiers: dict[str, dict[str, Any]] = {}
    intervals: dict[str, tuple[datetime, datetime | None]] = {}
    raw_identifiers = case.get("identifiers")
    if not isinstance(raw_identifiers, list):
        raw_identifiers = []
        errors.append(error("ADUC-ID-001", "identifiers must be an array"))
    for raw in raw_identifiers:
        record, record_errors = validate_identifier(raw, entities)
        errors.extend(record_errors)
        if not record or not isinstance(record.get("identifierId"), str):
            continue
        identifier_id = record["identifierId"]
        if identifier_id in identifiers:
            errors.append(error("ADUC-ID-001", f"duplicate identifierId: {identifier_id}"))
            continue
        identifiers[identifier_id] = record
        start, end, validity_errors = parse_validity(record.get("validity"))
        if not validity_errors and start is not None:
            intervals[identifier_id] = (start, end)

    grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for record in identifiers.values():
        key = identifier_key(record)
        if key is not None:
            grouped.setdefault(key, []).append(record)
    for records in grouped.values():
        for index, left in enumerate(records):
            for right in records[index + 1 :]:
                if left.get("subjectEntity") == right.get("subjectEntity"):
                    continue
                left_interval = intervals.get(str(left.get("identifierId")))
                right_interval = intervals.get(str(right.get("identifierId")))
                if left_interval and right_interval and overlaps(*left_interval, *right_interval):
                    errors.append(error("ADUC-ID-007", "identifier key is assigned to different entities during overlapping validity"))

    relations: list[dict[str, Any]] = []
    relation_intervals: dict[str, tuple[datetime, datetime | None]] = {}
    raw_relations = case.get("relations", [])
    if not isinstance(raw_relations, list):
        raw_relations = []
        errors.append(error("ADUC-REL-003", "relations must be an array"))
    seen_assertions: set[str] = set()
    for raw in raw_relations:
        record, record_errors = validate_relation(raw, identifiers)
        errors.extend(record_errors)
        if not record or not isinstance(record.get("assertionId"), str):
            continue
        assertion_id = record["assertionId"]
        if assertion_id in seen_assertions:
            errors.append(error("ADUC-REL-003", f"duplicate assertionId: {assertion_id}"))
        seen_assertions.add(assertion_id)
        relations.append(record)
        start, end, validity_errors = parse_validity(record.get("validity"))
        if not validity_errors and start is not None:
            relation_intervals[assertion_id] = (start, end)

    for index, left in enumerate(relations):
        left_pair = frozenset((left.get("subjectIdentifier"), left.get("objectIdentifier")))
        for right in relations[index + 1 :]:
            right_pair = frozenset((right.get("subjectIdentifier"), right.get("objectIdentifier")))
            if left_pair != right_pair or {left.get("relation"), right.get("relation")} != {"sameEntity", "differentEntity"}:
                continue
            a = relation_intervals.get(str(left.get("assertionId")))
            b = relation_intervals.get(str(right.get("assertionId")))
            if a and b and overlaps(*a, *b):
                errors.append(error("ADUC-REL-004", "contradictory sameEntity and differentEntity assertions overlap"))

    active_identifiers = {
        identifier_id: record
        for identifier_id, record in identifiers.items()
        if identifier_id in intervals and active(*intervals[identifier_id], evaluation_at)
    }
    active_subjects = sorted({str(record.get("subjectEntity")) for record in active_identifiers.values()})
    active_relations = [
        relation
        for relation in relations
        if str(relation.get("assertionId")) in relation_intervals
        and active(*relation_intervals[str(relation.get("assertionId"))], evaluation_at)
    ]

    purpose = case.get("purpose")
    for relation in active_relations:
        subject = str(relation.get("subjectIdentifier"))
        obj = str(relation.get("objectIdentifier"))
        if subject not in active_identifiers or obj not in active_identifiers:
            errors.append(error("ADUC-ID-007", "identity relation uses an identifier outside its validity interval"))
            continue
        if relation.get("conflictState", "clear") != "clear" or relation.get("lifecycleState", "active") != "active":
            errors.append(error("ADUC-MERGE-002", "contested or deprecated identity relation blocks automatic use"))
        privacy = relation.get("privacy")
        if isinstance(privacy, dict) and purpose is not None:
            permitted = privacy.get("permittedPurposes")
            if not isinstance(permitted, list) or purpose not in permitted:
                errors.append(error("ADUC-PRIV-001", "requested purpose is not permitted by identity relation"))
        for endpoint in (active_identifiers[subject], active_identifiers[obj]):
            if endpoint.get("identifierKind") in PROTECTED_KINDS and purpose is not None:
                permitted = endpoint.get("permittedPurposes")
                if not isinstance(permitted, list) or purpose not in permitted:
                    errors.append(error("ADUC-PRIV-001", "requested purpose is not permitted by protected identifier"))

    relation_names = {relation.get("relation") for relation in active_relations}
    if "differentEntity" in relation_names:
        decision = "differentEntity"
    elif "sameEntity" in relation_names:
        decision = "mergeAllowed"
    elif "possibleMatch" in relation_names:
        decision = "candidateOnly"
    elif relation_names & {"broaderEntity", "narrowerEntity"}:
        decision = "relationOnly"
    else:
        decision = "unresolved"

    if errors and decision not in {"differentEntity", "relationOnly"}:
        decision = "mergeBlocked"
    owl_same_as_allowed = decision == "mergeAllowed" and not errors
    if case.get("exportOwlSameAs") is True and not owl_same_as_allowed:
        errors.append(error("ADUC-REL-006", "owl:sameAs export requires a qualifying exact identity merge"))
        decision = "mergeBlocked"
        owl_same_as_allowed = False

    return {
        "caseId": case.get("id"),
        "valid": not errors,
        "decision": decision,
        "owlSameAsAllowed": owl_same_as_allowed,
        "activeSubjects": active_subjects,
        "errors": errors,
    }


def check_reference_file(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    document = load_json(path)
    cases = document.get("cases") if isinstance(document, dict) else None
    if not isinstance(cases, list):
        return [], [f"{path}: cases array is required"]
    results: list[dict[str, Any]] = []
    failures: list[str] = []
    for case in cases:
        result = evaluate_case(case)
        results.append(result)
        expected = case.get("expected", {}) if isinstance(case, dict) else {}
        for field in ("valid", "decision", "owlSameAsAllowed", "activeSubjects"):
            if field in expected and result.get(field) != expected.get(field):
                failures.append(f"{case.get('id')}: expected {field}={expected.get(field)!r}, got {result.get(field)!r}")
    return results, failures


def check_invalid_file(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    document = load_json(path)
    cases = document.get("cases") if isinstance(document, dict) else None
    if not isinstance(cases, list):
        return [], [f"{path}: cases array is required"]
    results: list[dict[str, Any]] = []
    failures: list[str] = []
    for case in cases:
        result = evaluate_case(case)
        results.append(result)
        expected = case.get("expectedError") if isinstance(case, dict) else None
        codes = {item.get("code") for item in result.get("errors", [])}
        if result.get("valid") is not False:
            failures.append(f"{case.get('id')}: invalid case was accepted")
        if expected not in codes:
            failures.append(f"{case.get('id')}: expected error {expected}, got {sorted(code for code in codes if code)}")
    return results, failures


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", nargs="?", type=Path, default=DEFAULT_EXAMPLES / "reference-cases.json")
    parser.add_argument("invalid", nargs="?", type=Path, default=DEFAULT_EXAMPLES / "invalid-cases.json")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        reference_results, reference_failures = check_reference_file(args.reference)
        invalid_results, invalid_failures = check_invalid_file(args.invalid)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"identity evaluation failed: {exc}", file=sys.stderr)
        return 2
    failures = reference_failures + invalid_failures
    report = {
        "validCases": len(reference_results),
        "invalidCases": len(invalid_results),
        "failures": failures,
        "referenceResults": reference_results,
        "invalidResults": invalid_results,
    }
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Validated {len(reference_results)} identity reference cases and {len(invalid_results)} required counterexamples.")
        for failure in failures:
            print(f"FAIL: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
