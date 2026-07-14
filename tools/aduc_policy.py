#!/usr/bin/env python3
"""Deterministic reference evaluator for ADUC Policy Profile 0.1."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "examples" / "policy"
HEX = re.compile(r"^[0-9a-f]{64}$")
AUTH = {"inferred": 0, "reviewed": 1, "verified": 2, "canonical": 3}
EXECUTABLE_EFFECTS = {"permission", "prohibition", "duty"}
HUMAN_ONLY_EFFECTS = {"recommendation", "legalNotice", "classification"}
ODRL = "http://www.w3.org/ns/odrl/2/"
ADUC = "urn:aduc:term:"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def iri(value: Any) -> bool:
    return isinstance(value, str) and bool(urlparse(value).scheme)


def error(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def parse_time(value: str) -> datetime:
    normalized = value[:-1] + "+00:00" if isinstance(value, str) and value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError("timezone offset required")
    return parsed.astimezone(timezone.utc)


def registry(reference: Any, base: Path):
    if (
        not isinstance(reference, dict)
        or not isinstance(reference.get("path"), str)
        or not HEX.fullmatch(str(reference.get("sha256", "")))
    ):
        return None, [error("ADUC-POL-VOCAB-001", "pinned registry required")]

    path = (base / reference["path"]).resolve()
    try:
        path.relative_to(base.resolve())
    except ValueError:
        return None, [error("ADUC-POL-VOCAB-001", "unsafe registry path")]

    if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != reference["sha256"]:
        return None, [error("ADUC-POL-VOCAB-001", "registry unavailable or changed")]

    loaded = load(path)
    if (
        loaded.get("registryId") != reference.get("registryId")
        or loaded.get("registryVersion") != reference.get("registryVersion")
    ):
        return None, [error("ADUC-POL-VOCAB-001", "registry identity mismatch")]
    return loaded, []


def validate_request(request: Any, objects: dict[str, Any], policy_registry: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    if not isinstance(request, dict):
        return [error("ADUC-POL-REQUEST-001", "request required")]

    for key in ("target", "requester", "recipient", "action", "purpose", "spatial", "environment"):
        if not iri(request.get(key)):
            errors.append(error("ADUC-POL-REQUEST-001", f"{key} must be IRI"))

    target = request.get("target")
    if target not in objects or objects.get(target, {}).get("kind") not in {"resource", "version"}:
        errors.append(error("ADUC-POL-TARGET-001", "request target not bound"))
    if not HEX.fullmatch(str(request.get("targetDigest", ""))):
        errors.append(error("ADUC-POL-TARGET-002", "request digest required"))
    if request.get("action") not in policy_registry.get("actions", {}):
        errors.append(error("ADUC-POL-ACTION-002", "unknown request action"))
    if request.get("purpose") not in policy_registry.get("purposes", {}):
        errors.append(error("ADUC-POL-PURPOSE-002", "unknown request purpose"))
    if request.get("environment") not in policy_registry.get("environments", {}):
        errors.append(error("ADUC-POL-SCOPE-002", "unknown environment"))

    try:
        parse_time(request.get("at"))
    except Exception:
        errors.append(error("ADUC-POL-SCOPE-002", "invalid request time"))

    evidence = request.get("evidence", [])
    if not isinstance(evidence, list) or not all(iri(item) for item in evidence):
        errors.append(error("ADUC-POL-EVIDENCE-001", "invalid request evidence"))
    return errors


def validate_policy(policy: Any, objects: Any, evidence_table: Any, policy_registry: dict[str, Any]):
    errors: list[dict[str, str]] = []
    if not isinstance(policy, dict):
        return None, [error("ADUC-POL-DOC-001", "policy required")]
    if not isinstance(objects, dict):
        return None, [error("ADUC-POL-TARGET-001", "object table required")]
    if not isinstance(evidence_table, dict):
        return None, [error("ADUC-POL-EVIDENCE-001", "evidence table required")]

    policy_id = policy.get("id")
    target = policy.get("target")
    if not iri(policy_id):
        errors.append(error("ADUC-POL-DOC-001", "policy id must be IRI"))
    if not iri(target) or target not in objects:
        errors.append(error("ADUC-POL-TARGET-001", "target not bound"))
    elif objects[target].get("kind") not in {"resource", "version"}:
        errors.append(error("ADUC-POL-TARGET-001", "invalid target kind"))

    target_digest = policy.get("targetDigest")
    if not HEX.fullmatch(str(target_digest or "")):
        errors.append(error("ADUC-POL-TARGET-002", "target digest required"))
    elif target in objects and objects[target].get("digest") != target_digest:
        errors.append(error("ADUC-POL-TARGET-002", "target digest mismatch"))

    if policy.get("mode") not in policy_registry.get("policyModes", []):
        errors.append(error("ADUC-POL-DOC-001", "invalid mode"))
    if policy.get("disclosure") not in policy_registry.get("disclosureStates", []):
        errors.append(error("ADUC-POL-STATE-001", "invalid disclosure"))
    if policy.get("auth") not in AUTH:
        errors.append(error("ADUC-POL-AUTH-001", "invalid authority"))

    for key in ("method", "prov", "by"):
        if not iri(policy.get(key)):
            errors.append(error("ADUC-POL-AUTH-001", f"{key} must be IRI"))

    policy_evidence = policy.get("evidence")
    if (
        not isinstance(policy_evidence, list)
        or not policy_evidence
        or not all(iri(item) and item in evidence_table for item in policy_evidence)
    ):
        errors.append(error("ADUC-POL-EVIDENCE-001", "bound policy evidence required"))

    if policy.get("auth") == "inferred":
        confidence = policy.get("confidence")
        if (
            not isinstance(confidence, (int, float))
            or isinstance(confidence, bool)
            or not 0 <= confidence <= 1
            or not iri(policy.get("confidenceMethod"))
        ):
            errors.append(error("ADUC-POL-AUTH-002", "calibrated confidence required"))

    if (
        policy.get("conflict", "clear") not in {"clear", "contested"}
        or policy.get("life", "active") not in {"active", "deprecated"}
    ):
        errors.append(error("ADUC-POL-STATE-001", "invalid conflict or lifecycle"))

    validity = policy.get("valid")
    try:
        if not isinstance(validity, dict) or parse_time(validity["start"]) >= parse_time(validity["end"]):
            raise ValueError("invalid bounds")
    except Exception:
        errors.append(error("ADUC-POL-SCOPE-002", "invalid validity interval"))

    supersedes = policy.get("supersedes")
    if supersedes is not None and (not iri(supersedes) or supersedes == policy_id):
        errors.append(error("ADUC-POL-COMPOSE-001", "invalid supersedes"))

    inherited = policy.get("inheritsFrom", [])
    if inherited:
        if not isinstance(inherited, list) or not all(iri(item) and item != policy_id for item in inherited):
            errors.append(error("ADUC-POL-COMPOSE-001", "invalid inheritance"))
        if policy.get("compositionState") != "resolved":
            errors.append(error("ADUC-POL-COMPOSE-001", "inheritance unresolved"))
        composition_evidence = policy.get("compositionEvidence")
        if (
            not isinstance(composition_evidence, list)
            or not composition_evidence
            or not all(iri(item) and item in evidence_table for item in composition_evidence)
        ):
            errors.append(error("ADUC-POL-COMPOSE-001", "composition evidence required"))

    rules = policy.get("rules")
    if not isinstance(rules, list):
        return None, errors + [error("ADUC-POL-RULE-001", "rules array required")]

    rule_ids: list[str] = []
    normalized_rules: list[dict[str, Any]] = []
    for rule in rules:
        if not isinstance(rule, dict):
            errors.append(error("ADUC-POL-RULE-001", "rule object required"))
            continue

        rule_id = rule.get("id")
        effect = rule.get("effect")
        if not iri(rule_id):
            errors.append(error("ADUC-POL-RULE-001", "rule id must be IRI"))
        else:
            rule_ids.append(rule_id)
        if effect not in policy_registry.get("effects", []):
            errors.append(error("ADUC-POL-RULE-001", "unsupported effect"))
        if effect in EXECUTABLE_EFFECTS and rule.get("machineEvaluable") is not True:
            errors.append(error("ADUC-POL-RULE-002", "executable rule not declared"))
        if effect in HUMAN_ONLY_EFFECTS and rule.get("machineEvaluable") is not False:
            errors.append(error("ADUC-POL-LEGAL-001", "human statement made executable"))

        if effect in EXECUTABLE_EFFECTS:
            action = rule.get("action")
            if not iri(action):
                errors.append(error("ADUC-POL-ACTION-001", "action must be IRI"))
            elif action not in policy_registry.get("actions", {}):
                errors.append(error("ADUC-POL-ACTION-002", "unknown action"))
            elif (
                effect in {"permission", "prohibition"}
                and policy_registry["actions"][action].get("category") != "primary"
            ):
                errors.append(error("ADUC-POL-ACTION-002", "primary action required"))
            elif effect == "duty" and policy_registry["actions"][action].get("category") != "duty":
                errors.append(error("ADUC-POL-DUTY-001", "duty action required"))
            if not iri(rule.get("assigner")):
                errors.append(error("ADUC-POL-PARTY-001", "assigner required"))

        purposes = rule.get("purposes", [])
        if effect in {"permission", "prohibition"}:
            if not isinstance(purposes, list) or not purposes or not all(iri(item) for item in purposes):
                errors.append(error("ADUC-POL-PURPOSE-001", "controlled purposes required"))
            elif not all(item in policy_registry.get("purposes", {}) for item in purposes):
                errors.append(error("ADUC-POL-PURPOSE-002", "unknown purpose"))
        elif purposes:
            if not isinstance(purposes, list) or not all(
                iri(item) and item in policy_registry.get("purposes", {}) for item in purposes
            ):
                errors.append(error("ADUC-POL-PURPOSE-002", "invalid optional purpose restriction"))

        for key in ("assignee", "recipient", "spatial", "environment"):
            if rule.get(key) is not None and not iri(rule.get(key)):
                code = "ADUC-POL-PARTY-001" if key in {"assignee", "recipient"} else "ADUC-POL-SCOPE-002"
                errors.append(error(code, f"invalid {key}"))
        if (
            rule.get("environment") is not None
            and rule["environment"] not in policy_registry.get("environments", {})
        ):
            errors.append(error("ADUC-POL-SCOPE-002", "unknown rule environment"))

        if effect == "duty":
            if rule.get("phase") not in {"preUse", "postUse"}:
                errors.append(error("ADUC-POL-DUTY-001", "invalid duty phase"))
            if rule.get("satisfied") is True and not rule.get("satisfiedBy"):
                errors.append(error("ADUC-POL-DUTY-002", "satisfaction evidence required"))
            satisfaction_evidence = rule.get("satisfiedBy", [])
            if satisfaction_evidence and (
                not isinstance(satisfaction_evidence, list)
                or not all(iri(item) and item in evidence_table for item in satisfaction_evidence)
            ):
                errors.append(error("ADUC-POL-DUTY-002", "invalid satisfaction evidence"))

        claim = rule.get("claim")
        if claim in {"consent", "legalCompliance", "ownership"}:
            required_kind = {
                "consent": "consent",
                "legalCompliance": "legalAssessment",
                "ownership": "ownership",
            }[claim]
            claim_evidence = rule.get("claimEvidence")
            if (
                not isinstance(claim_evidence, list)
                or not claim_evidence
                or not all(
                    iri(item)
                    and item in evidence_table
                    and evidence_table[item].get("kind") == required_kind
                    and iri(evidence_table[item].get("provenance"))
                    for item in claim_evidence
                )
            ):
                errors.append(error("ADUC-POL-CLAIM-001", f"{claim} evidence required"))

        normalized_rules.append(copy.deepcopy(rule))

    if len(rule_ids) != len(set(rule_ids)):
        errors.append(error("ADUC-POL-RULE-003", "duplicate rule id"))

    by_id = {rule.get("id"): rule for rule in normalized_rules if iri(rule.get("id"))}
    for rule in normalized_rules:
        duty_references = rule.get("duties", [])
        if rule.get("effect") == "permission" and duty_references and (
            not isinstance(duty_references, list)
            or not all(
                iri(item) and item in by_id and by_id[item].get("effect") == "duty"
                for item in duty_references
            )
        ):
            errors.append(error("ADUC-POL-DUTY-001", "unresolved duty reference"))

    normalized = copy.deepcopy(policy)
    normalized["rules"] = normalized_rules
    return normalized, errors


def matches(rule: dict[str, Any], request: dict[str, Any]) -> bool:
    return (
        rule.get("effect") in {"permission", "prohibition"}
        and rule.get("action") == request.get("action")
        and request.get("purpose") in rule.get("purposes", [])
        and (rule.get("assignee") is None or rule["assignee"] == request.get("requester"))
        and (rule.get("recipient") is None or rule["recipient"] == request.get("recipient"))
        and (rule.get("spatial") is None or rule["spatial"] == request.get("spatial"))
        and (rule.get("environment") is None or rule["environment"] == request.get("environment"))
    )


def duty_satisfied(rule: dict[str, Any], request: dict[str, Any], evidence_table: dict[str, Any]) -> bool:
    explicit = rule.get("satisfiedBy", [])
    request_evidence = set(request.get("evidence", []))
    if explicit:
        return bool(set(explicit) & request_evidence)
    required_kind = rule.get("requiredEvidenceKind")
    return bool(
        required_kind
        and any(evidence_table.get(item, {}).get("kind") == required_kind for item in request_evidence)
    )


def export_policy(policy: dict[str, Any]) -> dict[str, Any]:
    graph: list[dict[str, Any]] = [
        {
            "@id": policy["id"],
            "@type": ODRL + "Policy",
            ODRL + "target": {"@id": policy["target"]},
            ADUC + "targetDigest": policy["targetDigest"],
            ADUC + "authorityLevel": policy["auth"],
            ADUC + "disclosureState": policy["disclosure"],
            ADUC + "policyMode": policy["mode"],
            ADUC + "provenanceActivity": {"@id": policy["prov"]},
        }
    ]
    types = {
        "permission": ODRL + "Permission",
        "prohibition": ODRL + "Prohibition",
        "duty": ODRL + "Duty",
        "recommendation": ADUC + "Recommendation",
        "legalNotice": ADUC + "LegalNotice",
        "classification": ADUC + "Classification",
    }
    for rule in sorted(policy["rules"], key=lambda item: item["id"]):
        node: dict[str, Any] = {"@id": rule["id"], "@type": types[rule["effect"]]}
        if iri(rule.get("action")):
            node[ODRL + "action"] = {"@id": rule["action"]}
        if iri(rule.get("assigner")):
            node[ODRL + "assigner"] = {"@id": rule["assigner"]}
        if iri(rule.get("assignee")):
            node[ODRL + "assignee"] = {"@id": rule["assignee"]}
        if rule.get("purposes"):
            node[ADUC + "purpose"] = [{"@id": item} for item in sorted(rule["purposes"])]
        if rule.get("duties"):
            node[ODRL + "duty"] = [{"@id": item} for item in sorted(rule["duties"])]
        graph.append(node)
    return {"@graph": graph}


def evaluate(case: dict[str, Any], policy_registry: dict[str, Any]) -> dict[str, Any]:
    evidence_table = case.get("evidence", {})
    objects = case.get("objects", {})
    policy, errors = validate_policy(case.get("policy"), objects, evidence_table, policy_registry)
    request = case.get("request", {})
    errors += validate_request(request, objects, policy_registry)
    action = case.get("act", {}).get("t")

    if policy is None:
        return {"valid": False, "errors": errors}
    if action == "export":
        if errors:
            return {"valid": False, "errors": errors}
        return {
            "valid": True,
            "errors": [],
            "result": {
                "policies": 1,
                "rules": len(policy["rules"]),
                "jsonld": export_policy(policy),
            },
        }
    if action != "evaluate":
        errors.append(error("ADUC-POL-ACTION-003", "unsupported harness action"))
    if errors:
        return {"valid": False, "errors": errors}

    if request["target"] != policy["target"]:
        return {"valid": True, "errors": [], "result": {"outcome": "notApplicable"}}
    if request["targetDigest"] != policy["targetDigest"]:
        return {
            "valid": False,
            "errors": [error("ADUC-POL-TARGET-002", "target versions differ")],
        }
    if policy.get("conflict", "clear") != "clear" or policy.get("life", "active") != "active":
        return {
            "valid": True,
            "errors": [],
            "result": {"outcome": "requiresHumanReview", "reason": "policyNotReliablyActive"},
        }
    if policy["disclosure"] != "complete":
        return {
            "valid": True,
            "errors": [],
            "result": {"outcome": "requiresHumanReview", "reason": "incompleteDisclosure"},
        }
    if AUTH[policy["auth"]] < AUTH["reviewed"]:
        return {
            "valid": True,
            "errors": [],
            "result": {"outcome": "requiresHumanReview", "reason": "insufficientAuthority"},
        }
    if not parse_time(policy["valid"]["start"]) <= parse_time(request["at"]) < parse_time(policy["valid"]["end"]):
        return {
            "valid": True,
            "errors": [],
            "result": {"outcome": "deny", "reason": "policyOutsideValidity"},
        }

    applicable = [rule for rule in policy["rules"] if matches(rule, request)]
    prohibitions = [rule for rule in applicable if rule["effect"] == "prohibition"]
    if prohibitions:
        return {
            "valid": True,
            "errors": [],
            "result": {
                "outcome": "deny",
                "reason": "prohibition",
                "ruleIds": sorted(rule["id"] for rule in prohibitions),
            },
        }

    by_id = {rule["id"]: rule for rule in policy["rules"] if iri(rule.get("id"))}
    blocked_pre_use_duties: set[str] = set()
    for permission in sorted(
        (rule for rule in applicable if rule["effect"] == "permission"),
        key=lambda item: item["id"],
    ):
        duties = [by_id[item] for item in permission.get("duties", [])]
        unsatisfied_pre = sorted(
            duty["id"]
            for duty in duties
            if duty.get("phase") == "preUse" and not duty_satisfied(duty, request, evidence_table)
        )
        if unsatisfied_pre:
            blocked_pre_use_duties.update(unsatisfied_pre)
            continue

        outstanding_post = sorted(
            duty["id"]
            for duty in duties
            if duty.get("phase") == "postUse" and not duty_satisfied(duty, request, evidence_table)
        )
        result: dict[str, Any] = {"outcome": "permit", "ruleId": permission["id"]}
        if outstanding_post:
            result["outstandingDuties"] = outstanding_post
        return {"valid": True, "errors": [], "result": result}

    if blocked_pre_use_duties:
        return {
            "valid": True,
            "errors": [],
            "result": {
                "outcome": "deny",
                "reason": "unsatisfiedPreUseDuty",
                "dutyIds": sorted(blocked_pre_use_duties),
            },
        }
    if any(rule.get("effect") == "legalNotice" for rule in policy["rules"]):
        return {
            "valid": True,
            "errors": [],
            "result": {"outcome": "requiresHumanReview", "reason": "humanOnlyStatement"},
        }
    if policy["mode"] == "closed":
        return {
            "valid": True,
            "errors": [],
            "result": {"outcome": "deny", "reason": "closedPolicyDefault"},
        }
    return {
        "valid": True,
        "errors": [],
        "result": {"outcome": "indeterminate", "reason": "noApplicableRule"},
    }


def patch(document: Any, operations: list[list[Any]]) -> Any:
    document = copy.deepcopy(document)
    for operation, path, *rest in operations:
        target = document
        for key in path[:-1]:
            target = target[key]
        key = path[-1]
        value = rest[0] if rest else None
        if operation == "set":
            target[key] = copy.deepcopy(value)
        elif operation == "remove":
            target.pop(key, None) if isinstance(target, dict) else target.pop(key)
        elif operation == "append":
            target[key].append(copy.deepcopy(value))
        else:
            raise ValueError(operation)
    return document


def contains(actual: Any, expected: Any) -> bool:
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(
            key in actual and contains(actual[key], value)
            for key, value in expected.items()
        )
    return actual == expected


def materialize(reference: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    return patch(reference["base"], case.get("patch", []))


def run(reference_path: Path, invalid_path: Path) -> dict[str, Any]:
    reference = load(reference_path)
    invalid = load(invalid_path)
    policy_registry, registry_errors = registry(reference.get("registry"), reference_path.parent)
    if not policy_registry:
        return {
            "ok": False,
            "referenceAccepted": 0,
            "invalidRejected": 0,
            "failures": registry_errors,
        }

    materialized = {
        case["id"]: materialize(reference, case)
        for case in reference["cases"]
    }
    failures: list[dict[str, Any]] = []
    accepted = 0
    rejected = 0

    for case in reference["cases"]:
        actual = evaluate(materialized[case["id"]], policy_registry)
        if contains(actual, case["expect"]):
            accepted += 1
        else:
            failures.append({"id": case["id"], "actual": actual, "expected": case["expect"]})

    for case in invalid["cases"]:
        actual = evaluate(patch(materialized[case["base"]], case["patch"]), policy_registry)
        codes = {item["code"] for item in actual.get("errors", [])}
        if not actual["valid"] and case["code"] in codes:
            rejected += 1
        else:
            failures.append({"id": case["id"], "actual": actual, "expectedCode": case["code"]})

    return {
        "ok": not failures,
        "referenceAccepted": accepted,
        "invalidRejected": rejected,
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "reference",
        nargs="?",
        type=Path,
        default=DEFAULT / "reference-cases.json",
    )
    parser.add_argument(
        "invalid",
        nargs="?",
        type=Path,
        default=DEFAULT / "invalid-cases.json",
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    arguments = parser.parse_args()
    result = run(arguments.reference, arguments.invalid)
    if arguments.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            f"Accepted {result['referenceAccepted']} reference cases.\n"
            f"Rejected {result['invalidRejected']} invalid cases."
        )
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
