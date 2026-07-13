#!/usr/bin/env python3
"""Validate and evaluate ADUC epistemic lifecycle reference cases."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

AUTHORITY_LEVELS = ("inferred", "reviewed", "verified", "canonical")
AUTHORITY_RANK = {name: rank for rank, name in enumerate(AUTHORITY_LEVELS, start=1)}
EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_INPUT = 2


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def nonempty_string_list(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(nonempty_string(item) for item in value)
    )


def validate_record_set(record_set: Any) -> list[str]:
    """Return deterministic validation errors for one reference record set."""
    if not isinstance(record_set, dict):
        return ["recordSet must be an object"]

    errors: list[str] = []
    for key in ("source", "validFor", "localReference"):
        if not nonempty_string(record_set.get(key)):
            errors.append(f"{key} must be a non-empty string")

    collections: dict[str, Any] = {
        "coverage": record_set.get("coverage", []),
        "assertions": record_set.get("assertions", []),
        "challenges": record_set.get("challenges", []),
        "deprecations": record_set.get("deprecations", []),
    }
    for name, value in collections.items():
        if not isinstance(value, list):
            errors.append(f"{name} must be an array")
    if errors:
        return sorted(errors)

    coverage = collections["coverage"]
    assertions = collections["assertions"]
    challenges = collections["challenges"]
    deprecations = collections["deprecations"]

    seen_ids: dict[str, str] = {}

    def register_id(item: dict[str, Any], record_type: str, index: int) -> str | None:
        identifier = item.get("id")
        if not nonempty_string(identifier):
            errors.append(f"{record_type}[{index}].id must be a non-empty string")
            return None
        previous = seen_ids.get(identifier)
        if previous:
            errors.append(
                f"immutable identifier reused: {identifier} appears in "
                f"{previous} and {record_type}[{index}]"
            )
        else:
            seen_ids[identifier] = f"{record_type}[{index}]"
        return identifier

    for index, item in enumerate(coverage):
        if not isinstance(item, dict):
            errors.append(f"coverage[{index}] must be an object")
            continue
        register_id(item, "coverage", index)
        if item.get("resolutionStatus") != "unknown":
            errors.append(f"coverage[{index}].resolutionStatus must be unknown")
        for key in ("reason", "recordedBy", "recordedAt"):
            if not nonempty_string(item.get(key)):
                errors.append(f"coverage[{index}].{key} is required")
        for forbidden in (
            "semanticTarget",
            "mappingRelation",
            "confidence",
            "confidenceMethod",
        ):
            if forbidden in item:
                errors.append(
                    f"coverage[{index}] unknown record must not contain {forbidden}"
                )

    assertion_ids: set[str] = set()
    for index, item in enumerate(assertions):
        if not isinstance(item, dict):
            errors.append(f"assertions[{index}] must be an object")
            continue
        identifier = register_id(item, "assertions", index)
        if identifier:
            assertion_ids.add(identifier)
        for key in (
            "semanticTarget",
            "mappingRelation",
            "assertedBy",
            "assertedAt",
        ):
            if not nonempty_string(item.get(key)):
                errors.append(f"assertions[{index}].{key} is required")

        status = item.get("authorityStatus")
        if status not in AUTHORITY_LEVELS:
            errors.append(
                f"assertions[{index}].authorityStatus must be one of "
                + ", ".join(AUTHORITY_LEVELS)
            )
            continue

        confidence = item.get("confidence")
        if confidence is not None and (
            isinstance(confidence, bool)
            or not isinstance(confidence, (int, float))
            or not 0 <= float(confidence) <= 1
        ):
            errors.append(
                f"assertions[{index}].confidence must be a number from 0 through 1"
            )

        if status == "inferred":
            if confidence is None:
                errors.append(
                    f"assertions[{index}] inferred mapping requires confidence"
                )
            if not nonempty_string(item.get("confidenceMethod")):
                errors.append(
                    f"assertions[{index}] inferred mapping requires confidenceMethod"
                )
            if not nonempty_string_list(item.get("evidence")):
                errors.append(f"assertions[{index}] inferred mapping requires evidence")
            if any(key in item for key in ("review", "verification", "authority")):
                errors.append(
                    f"assertions[{index}] inferred mapping must not claim review, "
                    "verification or authority"
                )

        elif status == "reviewed":
            review = item.get("review")
            if not isinstance(review, dict):
                errors.append(
                    f"assertions[{index}] reviewed mapping requires review record"
                )
            else:
                for key in ("reviewedBy", "reviewedAt", "reviewScope"):
                    if not nonempty_string(review.get(key)):
                        errors.append(f"assertions[{index}].review.{key} is required")
                if not nonempty_string_list(review.get("evidence")):
                    errors.append(
                        f"assertions[{index}].review.evidence is required"
                    )
            if confidence is not None and not nonempty_string(
                item.get("confidenceMethod")
            ):
                errors.append(
                    f"assertions[{index}] confidence requires confidenceMethod"
                )
            if "authority" in item:
                errors.append(
                    f"assertions[{index}] reviewed mapping must not claim source authority"
                )

        elif status == "verified":
            verification = item.get("verification")
            if not isinstance(verification, dict):
                errors.append(
                    f"assertions[{index}] verified mapping requires verification record"
                )
            else:
                for key in ("verifiedBy", "verifiedAt", "method", "scope"):
                    if not nonempty_string(verification.get(key)):
                        errors.append(
                            f"assertions[{index}].verification.{key} is required"
                        )
                if not nonempty_string_list(verification.get("evidence")):
                    errors.append(
                        f"assertions[{index}].verification.evidence is required"
                    )
            if confidence is not None and not nonempty_string(
                item.get("confidenceMethod")
            ):
                errors.append(
                    f"assertions[{index}] confidence requires confidenceMethod"
                )
            if "authority" in item:
                errors.append(
                    f"assertions[{index}] verified mapping must not claim source authority"
                )

        elif status == "canonical":
            if "confidence" in item or "confidenceMethod" in item:
                errors.append(
                    f"assertions[{index}] canonical mapping must not contain confidence"
                )
            authority = item.get("authority")
            if not isinstance(authority, dict):
                errors.append(
                    f"assertions[{index}] canonical mapping requires authority record"
                )
            else:
                if not nonempty_string(authority.get("sourceAuthority")):
                    errors.append(
                        f"assertions[{index}].authority.sourceAuthority is required"
                    )
                if not nonempty_string_list(authority.get("evidence")):
                    errors.append(
                        f"assertions[{index}].authority.evidence is required"
                    )

    for index, item in enumerate(challenges):
        if not isinstance(item, dict):
            errors.append(f"challenges[{index}] must be an object")
            continue
        register_id(item, "challenges", index)
        if item.get("challengeStatus") not in ("open", "resolved"):
            errors.append(
                f"challenges[{index}].challengeStatus must be open or resolved"
            )
        for key in ("reason", "challengedBy", "challengedAt"):
            if not nonempty_string(item.get(key)):
                errors.append(f"challenges[{index}].{key} is required")
        if not nonempty_string_list(item.get("evidence")):
            errors.append(f"challenges[{index}].evidence is required")
        has_assertion = nonempty_string(item.get("targetsAssertion"))
        has_reference = nonempty_string(item.get("targetsReference"))
        if has_assertion == has_reference:
            errors.append(
                f"challenges[{index}] must contain exactly one of "
                "targetsAssertion or targetsReference"
            )
        if has_assertion and item["targetsAssertion"] not in assertion_ids:
            errors.append(
                f"challenges[{index}].targetsAssertion references unknown assertion "
                f"{item['targetsAssertion']}"
            )
        if item.get("challengeStatus") == "resolved" and not nonempty_string(
            item.get("resolves")
        ):
            errors.append(f"challenges[{index}] resolved challenge requires resolves")

    for index, item in enumerate(deprecations):
        if not isinstance(item, dict):
            errors.append(f"deprecations[{index}] must be an object")
            continue
        register_id(item, "deprecations", index)
        for key in ("targetsAssertion", "reason", "deprecatedBy", "effectiveAt"):
            if not nonempty_string(item.get(key)):
                errors.append(f"deprecations[{index}].{key} is required")
        target = item.get("targetsAssertion")
        if nonempty_string(target) and target not in assertion_ids:
            errors.append(
                f"deprecations[{index}].targetsAssertion references unknown assertion "
                f"{target}"
            )
        replacement = item.get("replacementAssertion")
        if replacement is not None and (
            not nonempty_string(replacement) or replacement not in assertion_ids
        ):
            errors.append(
                f"deprecations[{index}].replacementAssertion must reference an "
                "assertion in the record set"
            )

    return sorted(set(errors))


def recognized_canonical(
    assertion: dict[str, Any], policy: dict[str, Any]
) -> bool:
    authority = assertion.get("authority", {})
    return authority.get("sourceAuthority") in set(
        policy.get("recognizedSourceAuthorities", [])
    )


def accepted_verified(assertion: dict[str, Any], policy: dict[str, Any]) -> bool:
    verification = assertion.get("verification", {})
    return (
        verification.get("verifiedBy")
        in set(policy.get("recognizedVerifiers", []))
        and verification.get("method")
        in set(policy.get("recognizedVerificationMethods", []))
    )


def evaluate_record_set(
    record_set: dict[str, Any], policy: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Compute one of the seven effective states and a default consumer action."""
    policy = policy or {}
    errors = validate_record_set(record_set)
    if errors:
        return {
            "valid": False,
            "errors": errors,
            "effectiveState": "invalid",
            "action": "rejected",
            "selectedAssertionId": None,
            "reasons": ["record set failed lifecycle validation"],
        }

    local_reference = record_set["localReference"]
    assertions = list(record_set.get("assertions", []))
    deprecated_ids = {
        item["targetsAssertion"] for item in record_set.get("deprecations", [])
    }
    active = [item for item in assertions if item["id"] not in deprecated_ids]
    active_ids = {item["id"] for item in active}

    open_challenges = [
        item
        for item in record_set.get("challenges", [])
        if item.get("challengeStatus") == "open"
        and (
            item.get("targetsReference") == local_reference
            or item.get("targetsAssertion") in active_ids
        )
    ]
    if open_challenges:
        return {
            "valid": True,
            "errors": [],
            "effectiveState": "contested",
            "action": "blocked",
            "selectedAssertionId": None,
            "reasons": ["one or more unresolved challenges affect the active mapping"],
            "challengeIds": sorted(item["id"] for item in open_challenges),
        }

    recognized_canonicals = [
        item
        for item in active
        if item["authorityStatus"] == "canonical"
        and recognized_canonical(item, policy)
    ]
    canonical_meanings = {
        (item["semanticTarget"], item["mappingRelation"])
        for item in recognized_canonicals
    }
    if len(canonical_meanings) > 1:
        return {
            "valid": True,
            "errors": [],
            "effectiveState": "contested",
            "action": "blocked",
            "selectedAssertionId": None,
            "reasons": ["incompatible active recognized canonical assertions"],
            "challengeIds": [],
        }

    if active:
        highest_rank = max(
            AUTHORITY_RANK[item["authorityStatus"]] for item in active
        )
        highest = [
            item
            for item in active
            if AUTHORITY_RANK[item["authorityStatus"]] == highest_rank
        ]
        meanings = {
            (item["semanticTarget"], item["mappingRelation"]) for item in highest
        }
        if len(meanings) > 1:
            return {
                "valid": True,
                "errors": [],
                "effectiveState": "contested",
                "action": "blocked",
                "selectedAssertionId": None,
                "reasons": [
                    "incompatible active assertions at the highest authority level"
                ],
                "challengeIds": [],
            }

        selected = sorted(
            highest, key=lambda item: (item.get("assertedAt", ""), item["id"])
        )[-1]
        status = selected["authorityStatus"]

        if status == "canonical":
            if recognized_canonical(selected, policy):
                action = "authoritative"
                reasons = ["source authority is recognized by deployment policy"]
            else:
                action = "blocked"
                reasons = [
                    "canonical authority is not recognized by deployment policy"
                ]
        elif status == "verified":
            if accepted_verified(selected, policy):
                action = "usable"
                reasons = [
                    "verifier and method are recognized by deployment policy"
                ]
            else:
                action = "candidate"
                reasons = [
                    "verification exists but is not fully recognized by deployment policy"
                ]
        elif status == "reviewed":
            action = "usable" if policy.get("allowReviewed", False) else "candidate"
            reasons = [
                "reviewed mappings are allowed by deployment policy"
                if action == "usable"
                else "reviewed mapping requires deployment approval"
            ]
        else:
            method_recognized = selected.get("confidenceMethod") in set(
                policy.get("recognizedConfidenceMethods", [])
            )
            threshold = float(policy.get("minimumInferredConfidence", 1.0))
            threshold_met = float(selected["confidence"]) >= threshold
            automatic = bool(policy.get("allowInferredAutomatic", False))
            action = (
                "usable"
                if automatic and method_recognized and threshold_met
                else "candidate"
            )
            reasons = [
                "inferred mapping passed explicit automatic-use policy"
                if action == "usable"
                else "inferred mapping remains a candidate"
            ]

        return {
            "valid": True,
            "errors": [],
            "effectiveState": status,
            "action": action,
            "selectedAssertionId": selected["id"],
            "reasons": reasons,
        }

    if assertions and deprecated_ids.issuperset({item["id"] for item in assertions}):
        return {
            "valid": True,
            "errors": [],
            "effectiveState": "deprecated",
            "action": "historical",
            "selectedAssertionId": None,
            "reasons": ["only deprecated assertions remain"],
        }

    return {
        "valid": True,
        "errors": [],
        "effectiveState": "unknown",
        "action": "unmapped",
        "selectedAssertionId": None,
        "reasons": ["no active semantic assertion is available"],
    }


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "caseId": case.get("caseId"),
        **evaluate_record_set(case.get("recordSet", {}), case.get("policy", {})),
    }


def evaluate_collection(document: Any) -> dict[str, Any]:
    if not isinstance(document, dict) or not isinstance(document.get("cases"), list):
        return {
            "valid": False,
            "expectationsMet": False,
            "errors": ["document must contain a cases array"],
            "results": [],
        }

    results = [evaluate_case(case) for case in document["cases"]]
    expectation_errors: list[str] = []
    for case, result in zip(document["cases"], results):
        expected = case.get("expected")
        if not isinstance(expected, dict):
            continue
        for key in ("valid", "effectiveState", "action", "selectedAssertionId"):
            if key in expected and result.get(key) != expected[key]:
                expectation_errors.append(
                    f"{case.get('caseId')}: expected {key}={expected[key]!r}, "
                    f"got {result.get(key)!r}"
                )

    return {
        "valid": not expectation_errors,
        "expectationsMet": not expectation_errors,
        "allRecordSetsValid": all(result["valid"] for result in results),
        "errors": sorted(expectation_errors),
        "results": results,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path)
    args = parser.parse_args(argv)
    try:
        report = evaluate_collection(load_json(args.document))
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(json.dumps({"valid": False, "error": str(error)}, indent=2))
        return EXIT_INPUT
    print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    return EXIT_PASS if report["valid"] else EXIT_FAIL


if __name__ == "__main__":
    sys.exit(main())
