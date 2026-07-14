#!/usr/bin/env python3
"""Unified ADUC Core validator and deterministic comparator."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

TOOLS_DIR = Path(__file__).resolve().parent
ROOT = TOOLS_DIR.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import aduc_core_validate  # noqa: E402
import aduc_epistemic  # noqa: E402
import aduc_identity  # noqa: E402
import aduc_policy  # noqa: E402
import aduc_provenance  # noqa: E402
import aduc_relations  # noqa: E402
import aduc_source_binding  # noqa: E402
import aduc_time  # noqa: E402
import aduc_uncertainty  # noqa: E402
import aduc_units  # noqa: E402

REPORT_VERSION = "0.1.0"
MODULE_ORDER = (
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
    "extensions",
)
MODULE_INDEX = {module: index for index, module in enumerate(MODULE_ORDER)}
SEVERITY_ORDER = {"error": 0, "humanReview": 1, "warning": 2, "info": 3}
CLASSIFICATION_ORDER = {
    "incompatible": 0,
    "potentiallyIncompatible": 1,
    "requiresHumanReview": 2,
    "notComparable": 3,
    "modified": 4,
    "added": 5,
    "removed": 6,
    "compatible": 7,
    "unchanged": 8,
}
CHANGE_TYPE_ORDER = {"unchanged": 0, "added": 1, "removed": 2, "modified": 3}
ASSESSMENT_ORDER = {
    "incompatible": 0,
    "prohibited": 1,
    "contested": 2,
    "deprecated": 3,
    "requiresHumanReview": 4,
    "unknown": 5,
    "compatible": 6,
    "convertible": 7,
    "equivalent": 8,
}
PROFILE_ORDER = (
    "ADR-0005",
    "ADR-0006",
    "ADR-0007",
    "ADR-0008",
    "ADR-0009",
    "ADR-0010",
    "ADR-0011",
    "ADR-0012",
    "ADR-0013",
)
PROFILE_INDEX = {profile: index for index, profile in enumerate(PROFILE_ORDER)}
DANGEROUS_COMPARE_CODES = {
    "ADUC-CORE-ID-002",
    "ADUC-CORE-REF-001",
    "ADUC-CORE-OWNER-001",
    "ADUC-CORE-BINDING-001",
    "ADUC-CORE-BINDING-002",
    "ADUC-CORE-EXT-001",
    "ADUC-CORE-EXT-003",
    "ADUC-CORE-EXT-004",
}
EXIT_VALID = 0
EXIT_BLOCKED = 1
EXIT_HUMAN_REVIEW = 2
EXIT_USAGE = 3
MAX_INPUT_BYTES = 5_000_000
MAX_JSON_DEPTH = 100
MAX_JSON_NODES = 50_000


class InputError(Exception):
    """Raised for deterministic user input errors."""

    def __init__(self, code: str, message: str, path: str = "$") -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.path = path


def load_json_file(path: Path) -> Any:
    try:
        if path.stat().st_size > MAX_INPUT_BYTES:
            raise InputError("ADUC-CORE-INPUT-003", f"Input exceeds {MAX_INPUT_BYTES} bytes.")
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise InputError("ADUC-CORE-INPUT-001", "Input file does not exist.") from exc
    except OSError as exc:
        raise InputError("ADUC-CORE-INPUT-001", f"Unable to read input file: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise InputError(
            "ADUC-CORE-INPUT-002",
            f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}",
        ) from exc
    except RecursionError as exc:
        raise InputError("ADUC-CORE-INPUT-005", f"Input exceeds depth {MAX_JSON_DEPTH}.") from exc
    nodes, depth = json_limit_stats(payload)
    if nodes > MAX_JSON_NODES:
        raise InputError("ADUC-CORE-INPUT-004", f"Input exceeds {MAX_JSON_NODES} JSON nodes.")
    if depth > MAX_JSON_DEPTH:
        raise InputError("ADUC-CORE-INPUT-005", f"Input exceeds depth {MAX_JSON_DEPTH}.")
    return payload


def json_limit_stats(value: Any) -> tuple[int, int]:
    nodes = 0
    max_depth = 0
    stack: list[tuple[Any, int]] = [(value, 1)]
    while stack:
        current, depth = stack.pop()
        nodes += 1
        max_depth = max(max_depth, depth)
        if isinstance(current, dict):
            stack.extend((child, depth + 1) for child in current.values())
        elif isinstance(current, list):
            stack.extend((child, depth + 1) for child in current)
    return nodes, max_depth


def count_nodes(value: Any) -> int:
    return json_limit_stats(value)[0]


def json_depth(value: Any) -> int:
    return json_limit_stats(value)[1]


def iri(value: Any) -> bool:
    return isinstance(value, str) and bool(urlparse(value).scheme)


def walk(value: Any, path: str = "$") -> Iterable[tuple[str, str | int | None, Any, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if key.isidentifier() else f"{path}[{json.dumps(key, ensure_ascii=False)}]"
            yield child_path, key, child, value
            yield from walk(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_path = f"{path}[{index}]"
            yield child_path, index, child, value
            yield from walk(child, child_path)


def module_for_path(path: str) -> str:
    if path == "$":
        return "contract"
    if path.startswith("$."):
        module = path[2:].split(".", 1)[0].split("[", 1)[0]
        return module if module in MODULE_INDEX else "contract"
    return "contract"


def diagnostic(
    code: str,
    severity: str,
    category: str,
    path: str,
    message: str,
    *,
    module: str | None = None,
    related_paths: list[str] | None = None,
    blocking: bool | None = None,
    profile: str | None = None,
    evaluator: str | None = None,
) -> dict[str, Any]:
    if blocking is None:
        blocking = severity == "error"
    item = {
        "code": code,
        "severity": severity,
        "category": category,
        "path": path,
        "message": message,
        "module": module or module_for_path(path),
        "relatedPaths": sorted(related_paths or []),
        "blocking": blocking,
    }
    if profile is not None:
        item["profile"] = profile
    if evaluator is not None:
        item["evaluator"] = evaluator
    return item


def input_error_report(source: str, exc: InputError) -> dict[str, Any]:
    item = diagnostic(exc.code, "error", "input", exc.path, exc.message, module="contract")
    report = finalize_validation_report(
        source=source,
        document=None,
        diagnostics=[item],
        schema_valid=False,
        architecture_valid=False,
        profile_evaluation=False,
    )
    report["inputError"] = True
    return report


def stable_diagnostics(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[Any, ...]] = set()
    unique: list[dict[str, Any]] = []
    for item in items:
        key = (
            item["code"],
            item["severity"],
            item["category"],
            item["path"],
            item["message"],
            item["module"],
            tuple(item.get("relatedPaths", [])),
            item["blocking"],
            item.get("profile"),
            item.get("evaluator"),
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    unique.sort(
        key=lambda item: (
            SEVERITY_ORDER.get(item["severity"], 99),
            MODULE_INDEX.get(item["module"], 99),
            item["path"],
            item["code"],
            item["message"],
        )
    )
    return unique


def collect_ids(document: Any) -> dict[str, dict[str, Any]]:
    ids: dict[str, dict[str, Any]] = {}
    if not isinstance(document, dict):
        return ids
    contract_id = document.get("aduc", {}).get("contractId") if isinstance(document.get("aduc"), dict) else None
    if isinstance(contract_id, str):
        ids[contract_id] = {"path": "$.aduc.contractId", "module": "aduc", "value": document.get("aduc")}
    for path, key, value, parent in walk(document):
        if key == "id" and isinstance(value, str):
            ids.setdefault(value, {"path": path, "module": module_for_path(path), "value": parent})
    return ids


def schema_diagnostics(document: Any, schema_only: bool) -> tuple[list[dict[str, Any]], bool, bool]:
    result = aduc_core_validate.validate_document(document, architecture=not schema_only)
    diagnostics: list[dict[str, Any]] = []
    for item in result.get("schemaErrors", []):
        diagnostics.append(
            diagnostic(
                item["code"],
                "error",
                "schema",
                item["path"],
                item["message"],
                module=module_for_path(item["path"]),
            )
        )
    if not schema_only:
        for item in result.get("architectureErrors", []):
            diagnostics.append(
                diagnostic(
                    item["code"],
                    "error",
                    architecture_category(item["code"]),
                    item["path"],
                    item["message"],
                    module=module_for_path(item["path"]),
                )
            )
    return diagnostics, bool(result.get("schemaValid")), bool(result.get("architectureValid"))


def architecture_category(code: str) -> str:
    if "-REF-" in code:
        return "reference"
    if "-ID-" in code:
        return "identity"
    if "-EXT-" in code:
        return "extension"
    if "-OWNER-" in code:
        return "ownership"
    if "-POLICY-" in code:
        return "policy"
    if "-BINDING-" in code:
        return "binding"
    return "architecture"


def profile_error_to_diagnostic(
    item: Any,
    *,
    profile: str,
    evaluator: str,
    module: str,
    path: str,
    severity: str = "error",
    category: str = "profile",
    blocking: bool | None = None,
) -> dict[str, Any]:
    if isinstance(item, dict):
        code = str(item.get("code", f"ADUC-CORE-{profile}-001"))
        message = str(item.get("message", "Profile evaluator reported an error."))
    else:
        code = f"ADUC-CORE-{profile}-001"
        message = str(item)
    return diagnostic(
        code,
        severity,
        category,
        path,
        message,
        module=module,
        blocking=blocking,
        profile=profile,
        evaluator=evaluator,
    )


def profile_result(
    profile: str,
    name: str,
    module: str,
    evaluator: str,
    *,
    called: bool = False,
    status: str = "notApplicable",
    rules_applied: list[str] | None = None,
    not_applicable: list[str] | None = None,
    missing_data: list[Any] | None = None,
    requires_request: list[str] | None = None,
    requires_human_review: list[str] | None = None,
    diagnostics: list[dict[str, Any]] | None = None,
    result: Any = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "profile": profile,
        "name": name,
        "module": module,
        "evaluator": evaluator,
        "called": called,
        "status": status,
        "rulesApplied": sorted(rules_applied or []),
        "notApplicable": sorted(not_applicable or []),
        "missingData": sorted((normalize_profile_note(note) for note in (missing_data or [])), key=canonical),
        "requiresRequest": sorted(requires_request or []),
        "requiresHumanReview": sorted(requires_human_review or []),
        "diagnosticCodes": sorted({item["code"] for item in diagnostics or []}),
    }
    if result is not None:
        item["result"] = result
    return item


def normalize_profile_note(value: Any) -> dict[str, str]:
    if isinstance(value, dict):
        return {"code": str(value.get("code", "ADUC-CORE-PROFILE-UNKNOWN")), "message": str(value.get("message", ""))}
    return {"code": "ADUC-CORE-PROFILE-UNKNOWN", "message": str(value)}


def evaluate_profiles(document: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not isinstance(document, dict):
        return [], []
    diagnostics: list[dict[str, Any]] = []
    identifiers = collect_ids(document)
    evaluations: list[dict[str, Any]] = []
    for adapter in (
        epistemic_profile,
        source_binding_profile,
        units_profile,
        temporal_profile,
        identity_profile,
        provenance_profile,
        uncertainty_profile,
        relations_profile,
        policy_profile,
    ):
        found, evaluation = adapter(document, identifiers)
        diagnostics.extend(found)
        evaluations.append(evaluation)
    diagnostics.extend(qualification_diagnostics(document, identifiers))
    diagnostics.extend(relation_conflict_diagnostics(document))
    diagnostics.extend(provenance_cycle_diagnostics(document))
    diagnostics.extend(policy_review_diagnostics(document))
    diagnostics.extend(extension_review_diagnostics(document))
    evaluations.sort(key=lambda item: PROFILE_INDEX.get(item["profile"], 99))
    return diagnostics, evaluations


def profile_diagnostics(document: Any) -> list[dict[str, Any]]:
    return evaluate_profiles(document)[0]


def semantic_record_set(document: dict[str, Any]) -> dict[str, Any] | None:
    semantics = document.get("semantics")
    assertions = semantics.get("assertions", []) if isinstance(semantics, dict) else []
    if not isinstance(assertions, list) or not assertions:
        return None
    aduc = document.get("aduc", {}) if isinstance(document.get("aduc"), dict) else {}
    resource = document.get("resource", {}) if isinstance(document.get("resource"), dict) else {}
    mapped: list[dict[str, Any]] = []
    challenges: list[dict[str, Any]] = []
    deprecations: list[dict[str, Any]] = []
    for index, assertion in enumerate(assertions):
        if not isinstance(assertion, dict):
            continue
        status = assertion.get("status")
        item: dict[str, Any] = {
            "id": assertion.get("id"),
            "semanticTarget": assertion.get("conceptIri"),
            "mappingRelation": assertion.get("mappingRelationIri"),
            "assertedBy": assertion.get("assertedByRef") or aduc.get("publisher"),
            "assertedAt": assertion.get("assertedAt") or aduc.get("createdAt"),
            "authorityStatus": status,
        }
        evidence = assertion.get("evidenceRefs", [])
        if status == "inferred":
            item["confidence"] = assertion.get("confidence")
            item["confidenceMethod"] = assertion.get("confidenceMethodIri")
            item["evidence"] = evidence
        elif status == "reviewed":
            item["review"] = {
                "reviewedBy": assertion.get("assertedByRef") or aduc.get("publisher"),
                "reviewedAt": assertion.get("assertedAt") or aduc.get("createdAt"),
                "reviewScope": "core-semantic-assertion",
                "evidence": evidence,
            }
        elif status == "verified":
            item["verification"] = {
                "verifiedBy": assertion.get("assertedByRef") or aduc.get("publisher"),
                "verifiedAt": assertion.get("assertedAt") or aduc.get("createdAt"),
                "method": assertion.get("provenanceRef") or assertion.get("methodIri") or "urn:aduc:method:core-semantic-verification",
                "scope": "core-semantic-assertion",
                "evidence": evidence,
            }
        elif status == "canonical":
            item["authority"] = {
                "sourceAuthority": assertion.get("assertedByRef") or aduc.get("publisher"),
                "evidence": evidence,
            }
        mapped.append(item)
        if assertion.get("conflict") and assertion.get("conflict") != "clear":
            challenges.append(
                {
                    "id": f"{assertion.get('id')}:challenge",
                    "targetsAssertion": assertion.get("id"),
                    "challengeStatus": "open",
                    "reason": str(assertion.get("conflict")),
                    "challengedBy": assertion.get("assertedByRef") or aduc.get("publisher"),
                    "challengedAt": assertion.get("assertedAt") or aduc.get("createdAt"),
                    "evidence": evidence,
                }
            )
        if assertion.get("lifecycle") == "deprecated":
            deprecations.append(
                {
                    "id": f"{assertion.get('id')}:deprecation",
                    "targetsAssertion": assertion.get("id"),
                    "reason": "Core assertion lifecycle is deprecated.",
                    "deprecatedBy": assertion.get("assertedByRef") or aduc.get("publisher"),
                    "effectiveAt": assertion.get("assertedAt") or aduc.get("createdAt"),
                }
            )
    return {
        "source": aduc.get("contractId", "urn:aduc:core:unknown-contract"),
        "validFor": resource.get("id", aduc.get("contractId", "urn:aduc:core:unknown-resource")),
        "localReference": "$.semantics.assertions",
        "coverage": [],
        "assertions": mapped,
        "challenges": challenges,
        "deprecations": deprecations,
    }


def epistemic_profile(document: dict[str, Any], _identifiers: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    profile, name, module, evaluator = "ADR-0005", "semantic mapping lifecycle", "semantics", "tools.aduc_epistemic.evaluate_record_set"
    record_set = semantic_record_set(document)
    if record_set is None:
        return [], profile_result(profile, name, module, evaluator, not_applicable=["semantics.assertions is absent"])
    result = aduc_epistemic.evaluate_record_set(record_set)
    errors = result.get("errors", []) if isinstance(result, dict) else []
    diagnostics: list[dict[str, Any]] = []
    status = "unknown" if errors else "valid"
    if isinstance(result, dict) and result.get("effectiveState") == "contested":
        status = "requiresHumanReview"
    return diagnostics, profile_result(
        profile,
        name,
        module,
        evaluator,
        called=True,
        status=status,
        rules_applied=["validate_record_set", "evaluate_record_set"],
        missing_data=[{"code": "ADUC-CORE-ADR-0005-001", "message": str(error)} for error in errors],
        diagnostics=diagnostics,
        result={"effectiveState": result.get("effectiveState"), "action": result.get("action")} if isinstance(result, dict) else None,
    )


def source_binding_profile(document: dict[str, Any], _identifiers: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    profile, name, module, evaluator = "ADR-0006", "source binding", "resource", "tools.aduc_source_binding.validate_digest"
    resource = document.get("resource")
    digest = resource.get("digest") if isinstance(resource, dict) else None
    if digest is None:
        return [], profile_result(profile, name, module, evaluator, not_applicable=["resource.digest is absent"])
    errors = aduc_source_binding.validate_digest({"algorithm": "sha-256", "value": digest, "scope": "raw-bytes"}, "raw-bytes")
    diagnostics = [
        profile_error_to_diagnostic(error, profile=profile, evaluator=evaluator, module=module, path="$.resource.digest", category="binding")
        for error in errors
    ]
    return diagnostics, profile_result(
        profile,
        name,
        module,
        evaluator,
        called=True,
        status="invalid" if diagnostics else "valid",
        rules_applied=["validate_digest"],
        diagnostics=diagnostics,
        requires_human_review=["Byte-level subject verification requires the bound local resource bytes."] if isinstance(resource, dict) and resource.get("locator") else [],
    )


def unit_registry_ref() -> dict[str, str]:
    return {
        "path": "registry.json",
        "registryId": "urn:aduc:unit-registry:reference:0.1",
        "registryVersion": "0.1.0",
        "sha256": "6092b9b67993b2ead4bb9efdfbd36946d8c3aae8dc86b4c1fb2d05afa28a1346",
    }


def units_profile(document: dict[str, Any], _identifiers: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    profile, name, module, evaluator = "ADR-0007", "unit conversion", "semantics", "tools.aduc_units.validate_assertion"
    assertions = [
        (index, item)
        for index, item in enumerate(document.get("semantics", {}).get("assertions", []))
        if isinstance(item, dict) and item.get("unitIri")
    ]
    if not assertions:
        return [], profile_result(profile, name, module, evaluator, not_applicable=["No semantic assertion declares unitIri."])
    registry, _provenance, registry_errors = aduc_units.load_registry(unit_registry_ref(), ROOT / "examples" / "units")
    if registry is None:
        return [], profile_result(profile, name, module, evaluator, called=True, status="unknown", missing_data=registry_errors)
    diagnostics: list[dict[str, Any]] = []
    missing: list[Any] = []
    for index, assertion in assertions:
        unit_payload = core_unit_assertion(assertion)
        if unit_payload is None:
            missing.append(
                {
                    "code": "ADUC-CORE-PROFILE-UNIT-DATA",
                    "message": f"$.semantics.assertions[{index}] lacks quantityKind, dimensionVector, quantityRole, and rounding context required for ADR-0007 conversion.",
                }
            )
            continue
        _record, _entry, errors = aduc_units.validate_assertion(unit_payload, registry)
        diagnostics.extend(
            profile_error_to_diagnostic(error, profile=profile, evaluator=evaluator, module=module, path=f"$.semantics.assertions[{index}].unitIri", category="unit")
            for error in errors
        )
    status = "invalid" if diagnostics else "unknown" if missing else "valid"
    return diagnostics, profile_result(
        profile,
        name,
        module,
        evaluator,
        called=True,
        status=status,
        rules_applied=["load_registry", "validate_assertion"],
        missing_data=missing,
        diagnostics=diagnostics,
    )


def core_unit_assertion(assertion: dict[str, Any]) -> dict[str, Any] | None:
    quantity_kind = assertion.get("quantityKindIri") or assertion.get("quantityKind")
    dimension = assertion.get("dimensionVectorIri") or assertion.get("dimensionVector")
    role = assertion.get("quantityRole")
    if not all(isinstance(item, str) and item for item in (quantity_kind, dimension, role)):
        return None
    return {
        "sourceBinding": assertion.get("sourceBindingRef") or assertion.get("subjectRef"),
        "localReference": assertion.get("localReference") or {"scheme": "json-pointer", "base": "description", "value": assertion.get("subjectRef", "")},
        "quantityKind": quantity_kind,
        "dimensionVector": dimension,
        "quantityRole": role,
        "unitState": assertion.get("unitState", "known"),
        "unit": {"identifier": normalize_qudt_iri(assertion.get("unitIri"))},
        "authorityStatus": assertion.get("status", "reviewed"),
        "conflictState": assertion.get("conflict", "clear"),
        "lifecycleState": assertion.get("lifecycle", "active"),
    }


def temporal_profile(document: dict[str, Any], _identifiers: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    profile, name, module, evaluator = "ADR-0008", "temporal", "context", "tools.aduc_time.resolve"
    temporal = document.get("context", {}).get("temporal", []) if isinstance(document.get("context"), dict) else []
    if not temporal:
        return [], profile_result(profile, name, module, evaluator, not_applicable=["context.temporal is absent"])
    missing: list[Any] = []
    diagnostics: list[dict[str, Any]] = []
    for index, item in enumerate(temporal):
        if not isinstance(item, dict):
            continue
        value = core_temporal_value(item)
        if value is None:
            missing.append(
                {
                    "code": "ADUC-CORE-PROFILE-TIME-DATA",
                    "message": f"$.context.temporal[{index}] lacks lexicalValue and pinned timezone registry data required for ADR-0008 resolution.",
                }
            )
            _result = aduc_time.resolve({"kind": "instant"}, {}, {})
            continue
        result = aduc_time.resolve(value, {}, {})
        diagnostics.extend(
            profile_error_to_diagnostic(error, profile=profile, evaluator=evaluator, module=module, path=f"$.context.temporal[{index}]", category="temporal")
            for error in result.get("errors", [])
        )
    status = "invalid" if diagnostics else "unknown" if missing else "valid"
    return diagnostics, profile_result(
        profile,
        name,
        module,
        evaluator,
        called=True,
        status=status,
        rules_applied=["resolve"],
        missing_data=missing,
        diagnostics=diagnostics,
    )


def core_temporal_value(item: dict[str, Any]) -> dict[str, Any] | None:
    if not isinstance(item.get("lexicalValue"), str):
        return None
    return {
        "kind": item.get("kind", "instant"),
        "role": item.get("role", "observation"),
        "lexicalValue": item.get("lexicalValue"),
        "precision": item.get("precision"),
        "authorityStatus": item.get("status", "reviewed"),
        "sourceBinding": item.get("fieldRef"),
        "localReference": item.get("localReference") or {"scheme": "json-pointer", "base": "resource", "value": item.get("fieldRef", "")},
    }


def identity_profile(document: dict[str, Any], _identifiers: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    profile, name, module, evaluator = "ADR-0009", "identity", "identity", "tools.aduc_identity.validate_entities"
    identity = document.get("identity")
    if not isinstance(identity, dict):
        return [], profile_result(profile, name, module, evaluator, not_applicable=["identity module is absent"])
    entities_payload = [{"entityId": item.get("id"), "entityType": item.get("typeIri"), "labels": item.get("labels", [])} for item in identity.get("entities", []) if isinstance(item, dict)]
    _entities, entity_errors = aduc_identity.validate_entities(entities_payload)
    diagnostics = [
        profile_error_to_diagnostic(error, profile=profile, evaluator=evaluator, module=module, path="$.identity.entities", category="identity")
        for error in entity_errors
    ]
    missing: list[Any] = []
    if identity.get("identifiers"):
        missing.append(
            {
                "code": "ADUC-CORE-PROFILE-IDENTITY-DATA",
                "message": "Core identifier records do not carry the full ADR-0009 identifierKind, validity, sourceBinding, and authority bundle.",
            }
        )
    return diagnostics, profile_result(
        profile,
        name,
        module,
        evaluator,
        called=True,
        status="invalid" if diagnostics else "unknown" if missing else "valid",
        rules_applied=["validate_entities"],
        missing_data=missing,
        diagnostics=diagnostics,
    )


def provenance_profile(document: dict[str, Any], _identifiers: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    profile, name, module, evaluator = "ADR-0010", "provenance", "provenance", "tools.aduc_provenance.validate_entities"
    provenance = document.get("provenance")
    if not isinstance(provenance, dict):
        return [], profile_result(profile, name, module, evaluator, not_applicable=["provenance module is absent"])
    entity_payload = [
        {
            "entityId": item.get("id"),
            "entityType": item.get("typeIri"),
            "contentHash": profile_sha256(item.get("digest") or document.get("resource", {}).get("digest")),
            "sourceBinding": item.get("sourceIri") or document.get("resource", {}).get("id"),
            "lifecycleState": item.get("lifecycle", "active"),
        }
        for item in provenance.get("entities", []) + provenance.get("evidence", [])
        if isinstance(item, dict)
    ]
    agent_payload = [
        {"agentId": item.get("id"), "agentType": prov_agent_type(item.get("typeIri")), "name": item.get("externalIdentityIri") or item.get("id")}
        for item in provenance.get("agents", [])
        if isinstance(item, dict)
    ]
    _entities, entity_errors = aduc_provenance.validate_entities(entity_payload)
    _agents, agent_errors = aduc_provenance.validate_agents(agent_payload)
    edges = {
        assertion.get("generatedRef"): set(assertion.get("usedRefs", []))
        for assertion in provenance.get("derivationAssertions", [])
        if isinstance(assertion, dict) and isinstance(assertion.get("generatedRef"), str) and isinstance(assertion.get("usedRefs"), list)
    }
    cycle = aduc_provenance.detect_cycle(edges)
    missing_entity_errors = [
        error for error in [*entity_errors, *agent_errors] if error.get("code") == "ADUC-PROV-002"
    ]
    hard_errors = [
        error for error in [*entity_errors, *agent_errors] if error.get("code") != "ADUC-PROV-002"
    ]
    diagnostics = [
        profile_error_to_diagnostic(error, profile=profile, evaluator=evaluator, module=module, path="$.provenance", category="provenance")
        for error in hard_errors
    ]
    if cycle:
        diagnostics.append(
            profile_error_to_diagnostic(
                {"code": "ADUC-PROV-006", "message": "provenance graph contains a cycle"},
                profile=profile,
                evaluator="tools.aduc_provenance.detect_cycle",
                module=module,
                path="$.provenance.derivationAssertions",
                category="provenance",
            )
        )
    missing = list(missing_entity_errors)
    if provenance.get("activities"):
        missing.append(
            {
                "code": "ADUC-CORE-PROFILE-PROVENANCE-DATA",
                "message": "Core activity records omit the full ADR-0010 execution, disclosure, timing, and reproducibility bundle.",
            }
        )
    return diagnostics, profile_result(
        profile,
        name,
        module,
        evaluator,
        called=True,
        status="invalid" if diagnostics else "unknown" if missing else "valid",
        rules_applied=["validate_entities", "validate_agents", "detect_cycle"],
        missing_data=missing,
        diagnostics=diagnostics,
    )


def prov_agent_type(type_iri: Any) -> str:
    if type_iri == "http://www.w3.org/ns/prov#Person":
        return "person"
    if type_iri == "http://www.w3.org/ns/prov#Organization":
        return "organization"
    if type_iri == "urn:aduc:agent:software":
        return "softwareAgent"
    if type_iri == "urn:aduc:agent:model":
        return "modelAgent"
    return "organization"


def profile_sha256(value: Any) -> Any:
    if isinstance(value, str) and len(value) == 64 and all(char in "0123456789abcdef" for char in value):
        return "sha256:" + value
    return value


def uncertainty_profile(document: dict[str, Any], identifiers: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    profile, name, module, evaluator = "ADR-0011", "uncertainty", "uncertainty", "tools.aduc_uncertainty.validate_uncertainty"
    uncertainty = document.get("uncertainty")
    if not isinstance(uncertainty, dict):
        return [], profile_result(profile, name, module, evaluator, not_applicable=["uncertainty module is absent"])
    diagnostics: list[dict[str, Any]] = []
    missing: list[Any] = []
    semantic_by_uncertainty = {
        item.get("uncertaintyRef"): item
        for item in document.get("semantics", {}).get("assertions", [])
        if isinstance(item, dict) and isinstance(item.get("uncertaintyRef"), str)
    }
    for index, statement in enumerate(uncertainty.get("statements", [])):
        if not isinstance(statement, dict):
            continue
        semantic = semantic_by_uncertainty.get(statement.get("id"), {})
        record = core_uncertainty_record(statement, semantic)
        _normalized, errors = aduc_uncertainty.validate_uncertainty(record)
        hard_errors = [error for error in errors if error.get("code") not in {"ADUC-UNC-001"}]
        missing_errors = [error for error in errors if error.get("code") == "ADUC-UNC-001"]
        diagnostics.extend(
            profile_error_to_diagnostic(error, profile=profile, evaluator=evaluator, module=module, path=f"$.uncertainty.statements[{index}]", category="uncertainty")
            for error in hard_errors
        )
        missing.extend(missing_errors)
        if isinstance(statement.get("subjectRef"), str) and statement["subjectRef"] not in identifiers:
            diagnostics.append(
                diagnostic(
                    "ADUC-CORE-REF-001",
                    "error",
                    "reference",
                    f"$.uncertainty.statements[{index}].subjectRef",
                    "Referenced Core object does not exist.",
                    module=module,
                    profile=profile,
                    evaluator=evaluator,
                )
            )
    return diagnostics, profile_result(
        profile,
        name,
        module,
        evaluator,
        called=True,
        status="invalid" if diagnostics else "unknown" if missing else "valid",
        rules_applied=["validate_uncertainty"],
        missing_data=missing,
        diagnostics=diagnostics,
    )


def core_uncertainty_record(statement: dict[str, Any], semantic: dict[str, Any]) -> dict[str, Any]:
    kind_map = {"relativeStandardUncertainty": "relativeStandard"}
    record: dict[str, Any] = {
        "uncertaintyId": statement.get("id"),
        "targetBinding": statement.get("subjectRef"),
        "quantityKind": semantic.get("conceptIri"),
        "quantityRole": statement.get("quantityRole", "ordinary"),
        "unit": "http://qudt.org/vocab/unit/UNITLESS"
        if kind_map.get(statement.get("kind"), statement.get("kind")) == "relativeStandard"
        else normalize_qudt_iri(semantic.get("unitIri") or statement.get("unitIri")),
        "method": statement.get("methodIri"),
        "provenanceActivity": statement.get("provenanceRef"),
        "uncertaintyType": kind_map.get(statement.get("kind"), statement.get("kind")),
        "authorityLevel": statement.get("authority") or statement.get("status"),
        "assertedBy": statement.get("assertedByRef"),
        "evidence": statement.get("evidenceRefs", []),
        "conflictState": statement.get("conflict", "clear"),
        "lifecycleState": statement.get("lifecycle", "active"),
    }
    if record["uncertaintyType"] == "relativeStandard":
        record["relativeStandardUncertainty"] = str(statement.get("value"))
    else:
        record["standardUncertainty"] = str(statement.get("value"))
    return record


def relation_registry_ref() -> dict[str, str]:
    return {
        "path": "predicate-registry.json",
        "registryId": "urn:aduc:relation-registry:0.1",
        "registryVersion": "0.1.0",
        "sha256": "374746ec62d744244f89a617f2a3d2e4d61a7e5f1b1eb30606b00a578b8bf3e6",
    }


def relations_profile(document: dict[str, Any], _identifiers: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    profile, name, module, evaluator = "ADR-0012", "relations", "relations", "tools.aduc_relations.validate_assertion"
    relations = document.get("relations")
    if not isinstance(relations, list) or not relations:
        return [], profile_result(profile, name, module, evaluator, not_applicable=["relations module is absent or empty"])
    registry, registry_errors = aduc_relations.registry(relation_registry_ref(), ROOT / "examples" / "relations")
    if registry is None:
        return [], profile_result(profile, name, module, evaluator, called=True, status="unknown", missing_data=registry_errors)
    objects = relation_objects(document)
    normalized = []
    diagnostics: list[dict[str, Any]] = []
    for index, relation in enumerate(relations):
        if not isinstance(relation, dict):
            continue
        mapped = core_relation_assertion(relation)
        item, errors = aduc_relations.validate_assertion(mapped, objects, registry)
        if item:
            normalized.append(item)
        hard_errors = [error for error in errors if str(error.get("code", "")).startswith(("ADUC-REL-CONFLICT-", "ADUC-REL-CYCLE-"))]
        missing_errors = [error for error in errors if error not in hard_errors]
        diagnostics.extend(
            profile_error_to_diagnostic(error, profile=profile, evaluator=evaluator, module=module, path=f"$.relations[{index}]", category="relation")
            for error in hard_errors
        )
        registry_errors.extend(missing_errors)
    graph_errors = aduc_relations.graph_errors(normalized, registry)
    diagnostics.extend(
        profile_error_to_diagnostic(error, profile=profile, evaluator="tools.aduc_relations.graph_errors", module=module, path="$.relations", category="relation")
        for error in graph_errors
    )
    return diagnostics, profile_result(
        profile,
        name,
        module,
        evaluator,
        called=True,
        status="invalid" if diagnostics else "unknown" if registry_errors else "valid",
        rules_applied=["registry", "validate_assertion", "graph_errors"],
        missing_data=registry_errors,
        diagnostics=diagnostics,
    )


def relation_objects(document: dict[str, Any]) -> dict[str, str]:
    objects: dict[str, str] = {}
    resource = document.get("resource")
    if isinstance(resource, dict) and isinstance(resource.get("id"), str):
        objects[resource["id"]] = "resource"
    for record in document.get("structure", {}).get("records", []) if isinstance(document.get("structure"), dict) else []:
        if isinstance(record, dict) and isinstance(record.get("id"), str):
            objects[record["id"]] = "result"
        for field in record.get("fields", []) if isinstance(record, dict) else []:
            if isinstance(field, dict) and isinstance(field.get("id"), str):
                objects[field["id"]] = "field"
    for assertion in document.get("semantics", {}).get("assertions", []) if isinstance(document.get("semantics"), dict) else []:
        if isinstance(assertion, dict):
            if isinstance(assertion.get("id"), str):
                objects[assertion["id"]] = "assertion"
            if isinstance(assertion.get("conceptIri"), str):
                objects[assertion["conceptIri"]] = "concept"
    for entity in document.get("identity", {}).get("entities", []) if isinstance(document.get("identity"), dict) else []:
        if isinstance(entity, dict) and isinstance(entity.get("id"), str):
            objects[entity["id"]] = "entity"
    provenance = document.get("provenance", {}) if isinstance(document.get("provenance"), dict) else {}
    for item in provenance.get("entities", []) + provenance.get("evidence", []):
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            objects[item["id"]] = "resource"
    for item in provenance.get("activities", []):
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            objects[item["id"]] = "activity"
    return objects


def core_relation_assertion(relation: dict[str, Any]) -> dict[str, Any]:
    item: dict[str, Any] = {
        "relationId": relation.get("id"),
        "predicate": relation.get("predicateIri"),
        "subject": {"binding": relation.get("subjectRef")},
        "authorityLevel": relation.get("authority") or relation.get("status"),
        "method": relation.get("methodIri"),
        "provenanceActivity": relation.get("provenanceRef"),
        "assertedBy": relation.get("assertedByRef"),
        "evidence": relation.get("evidenceRefs", []),
        "polarity": relation.get("polarity", "positive"),
        "conflictState": relation.get("conflict", "clear"),
        "lifecycleState": relation.get("lifecycle", "active"),
    }
    if "objectRef" in relation:
        item["object"] = {"binding": relation.get("objectRef")}
    else:
        item["object"] = {"literal": relation.get("literalObject")}
    return item


def policy_registry_ref() -> dict[str, str]:
    return {
        "path": "policy-registry.json",
        "registryId": "urn:aduc:policy-registry:0.1",
        "registryVersion": "0.1.0",
        "sha256": "11975dd6eb1c65dd45f19f31b4c7038dddda581e18231f7a6ac681fe84b90b2b",
    }


def policy_profile(document: dict[str, Any], _identifiers: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    profile, name, module, evaluator = "ADR-0013", "policy", "policy", "tools.aduc_policy.validate_policy"
    policy = document.get("policy")
    policies = policy.get("policies", []) if isinstance(policy, dict) else []
    if not policies:
        return [], profile_result(profile, name, module, evaluator, not_applicable=["policy.policies is absent"])
    registry, registry_errors = aduc_policy.registry(policy_registry_ref(), ROOT / "examples" / "policy")
    if registry is None:
        return [], profile_result(profile, name, module, evaluator, called=True, status="unknown", missing_data=registry_errors)
    objects, evidence = policy_objects_and_evidence(document)
    diagnostics: list[dict[str, Any]] = []
    missing: list[Any] = []
    review: list[str] = []
    for index, policy_record in enumerate(policies):
        mapped = core_policy_record(policy_record)
        _normalized, errors = aduc_policy.validate_policy(mapped, objects, evidence, registry)
        hard_errors = [error for error in errors if error.get("code") in {"ADUC-POL-LEGAL-001"}]
        missing.extend(error for error in errors if error not in hard_errors)
        diagnostics.extend(
            profile_error_to_diagnostic(error, profile=profile, evaluator=evaluator, module=module, path=f"$.policy.policies[{index}]", category="policy")
            for error in hard_errors
        )
        if isinstance(policy_record, dict) and policy_record.get("mode") == "closed":
            review.append("Closed policy mode requires an operational request before automatic use.")
    status = "invalid" if diagnostics else "requiresHumanReview" if review else "indeterminate"
    return diagnostics, profile_result(
        profile,
        name,
        module,
        evaluator,
        called=True,
        status="invalid" if diagnostics else "unknown" if missing else status,
        rules_applied=["registry", "validate_policy"],
        missing_data=missing,
        requires_request=["ADR-0013 permit/deny/notApplicable/indeterminate evaluation requires a concrete operational request."],
        requires_human_review=review,
        diagnostics=diagnostics,
    )


def policy_objects_and_evidence(document: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    objects: dict[str, Any] = {}
    resource = document.get("resource", {}) if isinstance(document.get("resource"), dict) else {}
    if isinstance(resource.get("id"), str):
        objects[resource["id"]] = {"kind": "resource", "digest": resource.get("digest")}
    evidence: dict[str, Any] = {}
    provenance = document.get("provenance", {}) if isinstance(document.get("provenance"), dict) else {}
    for item in provenance.get("evidence", []):
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            evidence[item["id"]] = {"kind": "policy", "provenance": item.get("sourceIri") or item.get("id")}
    return objects, evidence


def core_policy_record(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        return {}
    return {
        "id": record.get("id"),
        "target": record.get("targetRef"),
        "targetDigest": record.get("targetDigest"),
        "mode": record.get("mode"),
        "disclosure": record.get("disclosure"),
        "auth": record.get("authority") or record.get("status"),
        "method": record.get("methodIri") or "urn:aduc:method:core-policy-review",
        "prov": record.get("provenanceRef"),
        "by": record.get("assertedByRef"),
        "evidence": record.get("evidenceRefs", []),
        "conflict": record.get("conflict"),
        "life": record.get("lifecycle"),
        "valid": {"start": record.get("validFrom"), "end": record.get("validUntil")},
        "rules": [core_policy_rule(rule) for rule in record.get("rules", []) if isinstance(rule, dict)],
    }


def core_policy_rule(rule: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": rule.get("id"),
        "effect": rule.get("effect"),
        "machineEvaluable": rule.get("machineEvaluable"),
        "assigner": rule.get("assignerRef"),
        "action": rule.get("actionIri"),
        "purposes": rule.get("purposeIris", []),
        "duties": rule.get("duties", []),
        "phase": rule.get("phase"),
        "claim": rule.get("claim"),
        "claimEvidence": rule.get("claimEvidence", []),
        "satisfiedBy": rule.get("satisfiedBy", []),
        "requiredEvidenceKind": rule.get("requiredEvidenceKind"),
        "statement": rule.get("statement"),
    }


def normalize_qudt_iri(value: Any) -> Any:
    if isinstance(value, str) and value.startswith("https://qudt.org/"):
        return "http://qudt.org/" + value.removeprefix("https://qudt.org/")
    return value


def qualification_diagnostics(document: dict[str, Any], identifiers: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    for path, _key, value, _parent in walk(document):
        if not isinstance(value, dict) or "status" not in value:
            continue
        status = value.get("status")
        conflict = value.get("conflict")
        lifecycle = value.get("lifecycle")
        module = module_for_path(path)
        if status in {"canonical", "verified"} and module in {"semantics", "identity", "relations", "policy"}:
            missing = [name for name in ("authority", "assertedByRef", "evidenceRefs", "provenanceRef") if name not in value]
            if missing:
                diagnostics.append(
                    diagnostic(
                        "ADUC-CORE-QUAL-001",
                        "warning",
                        "qualification",
                        path,
                        "Authoritative assertion lacks complete authority, actor, evidence or provenance qualification.",
                        blocking=False,
                    )
                )
        if status == "inferred":
            diagnostics.append(
                diagnostic(
                    "ADUC-CORE-QUAL-002",
                    "humanReview",
                    "qualification",
                    path,
                    "Inferred assertion cannot be used as reviewed, verified or canonical without review.",
                    blocking=False,
                )
            )
        if conflict and conflict != "clear":
            diagnostics.append(
                diagnostic(
                    "ADUC-CORE-CONFLICT-001",
                    "humanReview",
                    "conflict",
                    path + ".conflict",
                    "Contested or conflicting assertion requires human review.",
                    blocking=False,
                )
            )
        if lifecycle == "deprecated":
            diagnostics.append(
                diagnostic(
                    "ADUC-CORE-LIFECYCLE-001",
                    "humanReview",
                    "lifecycle",
                    path + ".lifecycle",
                    "Deprecated Core object requires explicit replacement handling before automatic use.",
                    blocking=False,
                )
            )
        for ref_name in ("assertedByRef", "provenanceRef", "uncertaintyRef", "validDuringRef"):
            ref = value.get(ref_name)
            if isinstance(ref, str) and ref not in identifiers:
                diagnostics.append(
                    diagnostic(
                        "ADUC-CORE-REF-001",
                        "error",
                        "reference",
                        f"{path}.{ref_name}",
                        "Referenced Core object does not exist.",
                    )
                )
        refs = value.get("evidenceRefs")
        if isinstance(refs, list):
            for index, ref in enumerate(refs):
                if isinstance(ref, str) and ref not in identifiers:
                    diagnostics.append(
                        diagnostic(
                            "ADUC-CORE-REF-001",
                            "error",
                            "reference",
                            f"{path}.evidenceRefs[{index}]",
                            "Referenced evidence object does not exist.",
                        )
                    )
    identity = document.get("identity")
    if isinstance(identity, dict):
        for index, assertion in enumerate(identity.get("identityAssertions", [])):
            if not isinstance(assertion, dict):
                continue
            if assertion.get("decision") == "exactEntity" and assertion.get("status") not in {"verified", "canonical"}:
                diagnostics.append(
                    diagnostic(
                        "ADUC-CORE-IDENTITY-002",
                        "humanReview",
                        "identity",
                        f"$.identity.identityAssertions[{index}]",
                        "Exact identity decision is not sufficiently established for automatic merging.",
                        module="identity",
                        blocking=False,
                    )
                )
    return diagnostics


def relation_endpoint(relation: dict[str, Any]) -> str:
    if "objectRef" in relation:
        return "ref:" + str(relation.get("objectRef"))
    if "literalObject" in relation:
        return "literal:" + json.dumps(relation.get("literalObject"), sort_keys=True, ensure_ascii=False)
    return "missing:"


def relation_conflict_diagnostics(document: dict[str, Any]) -> list[dict[str, Any]]:
    relations = document.get("relations")
    if not isinstance(relations, list):
        return []
    by_key: dict[tuple[str, str, str], list[tuple[int, str]]] = {}
    for index, relation in enumerate(relations):
        if not isinstance(relation, dict):
            continue
        key = (str(relation.get("subjectRef")), str(relation.get("predicateIri")), relation_endpoint(relation))
        by_key.setdefault(key, []).append((index, str(relation.get("polarity"))))
    diagnostics: list[dict[str, Any]] = []
    for values in by_key.values():
        polarities = {polarity for _index, polarity in values}
        if {"positive", "negative"}.issubset(polarities):
            paths = [f"$.relations[{index}].polarity" for index, _polarity in values]
            diagnostics.append(
                diagnostic(
                    "ADUC-CORE-RELATION-001",
                    "error",
                    "relation",
                    paths[0],
                    "Positive and negative relation assertions conflict for the same endpoints.",
                    module="relations",
                    related_paths=paths[1:],
                )
            )
    return diagnostics


def provenance_cycle_diagnostics(document: dict[str, Any]) -> list[dict[str, Any]]:
    provenance = document.get("provenance")
    if not isinstance(provenance, dict):
        return []
    edges: dict[str, set[str]] = {}
    for assertion in provenance.get("derivationAssertions", []):
        if not isinstance(assertion, dict):
            continue
        generated = assertion.get("generatedRef")
        used = assertion.get("usedRefs")
        if isinstance(generated, str) and isinstance(used, list):
            edges.setdefault(generated, set()).update(item for item in used if isinstance(item, str))
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, trail: list[str]) -> list[str] | None:
        if node in visiting:
            start = trail.index(node) if node in trail else 0
            return trail[start:] + [node]
        if node in visited:
            return None
        visiting.add(node)
        for target in sorted(edges.get(node, set())):
            cycle = visit(target, trail + [node])
            if cycle:
                return cycle
        visiting.remove(node)
        visited.add(node)
        return None

    for node in sorted(edges):
        cycle = visit(node, [])
        if cycle:
            return [
                diagnostic(
                    "ADUC-CORE-PROVENANCE-001",
                    "error",
                    "provenance",
                    "$.provenance.derivationAssertions",
                    "Derivation graph contains a cycle: " + " -> ".join(cycle),
                    module="provenance",
                )
            ]
    return []


def policy_review_diagnostics(document: dict[str, Any]) -> list[dict[str, Any]]:
    policy = document.get("policy")
    if not isinstance(policy, dict):
        return []
    diagnostics: list[dict[str, Any]] = []
    for p_index, record in enumerate(policy.get("policies", [])):
        if not isinstance(record, dict):
            continue
        base = f"$.policy.policies[{p_index}]"
        if record.get("mode") == "closed":
            diagnostics.append(
                diagnostic(
                    "ADUC-CORE-POLICY-002",
                    "humanReview",
                    "policy",
                    base + ".mode",
                    "Closed policy mode prevents automatic permission assumptions.",
                    module="policy",
                    blocking=False,
                )
            )
        if record.get("disclosure") in {"partial", "redacted"}:
            diagnostics.append(
                diagnostic(
                    "ADUC-CORE-POLICY-003",
                    "humanReview",
                    "policy",
                    base + ".disclosure",
                    "Partial or redacted policy disclosure requires human review.",
                    module="policy",
                    blocking=False,
                )
            )
    return diagnostics


def extension_review_diagnostics(document: dict[str, Any]) -> list[dict[str, Any]]:
    aduc = document.get("aduc")
    if not isinstance(aduc, dict):
        return []
    diagnostics: list[dict[str, Any]] = []
    for index, declaration in enumerate(aduc.get("extensionDeclarations", [])):
        if isinstance(declaration, dict) and declaration.get("required") is True:
            diagnostics.append(
                diagnostic(
                    "ADUC-CORE-EXT-003",
                    "error",
                    "extension",
                    f"$.aduc.extensionDeclarations[{index}]",
                    "Required extension is not supported by the unified Core validator.",
                    module="extensions",
                )
            )
    return diagnostics


def validate_contract(
    document: Any,
    *,
    source: str = "<memory>",
    schema_only: bool = False,
    profile_evaluation: bool = True,
) -> dict[str, Any]:
    diagnostics, schema_valid, architecture_valid = schema_diagnostics(document, schema_only)
    profile_evaluations: list[dict[str, Any]] = []
    if profile_evaluation and not schema_only:
        found, profile_evaluations = evaluate_profiles(document)
        diagnostics.extend(found)
    return finalize_validation_report(
        source=source,
        document=document,
        diagnostics=diagnostics,
        schema_valid=schema_valid,
        architecture_valid=architecture_valid if not schema_only else None,
        profile_evaluation=profile_evaluation and not schema_only,
        profile_evaluations=profile_evaluations,
    )


def finalize_validation_report(
    *,
    source: str,
    document: Any,
    diagnostics: list[dict[str, Any]],
    schema_valid: bool,
    architecture_valid: bool | None,
    profile_evaluation: bool,
    profile_evaluations: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    diagnostics = stable_diagnostics(diagnostics)
    summary = {
        "errors": sum(item["severity"] == "error" for item in diagnostics),
        "warnings": sum(item["severity"] == "warning" for item in diagnostics),
        "humanReview": sum(item["severity"] == "humanReview" for item in diagnostics),
    }
    outcome = "valid"
    if summary["errors"]:
        outcome = "blocked"
    elif summary["humanReview"]:
        outcome = "requiresHumanReview"
    elif summary["warnings"]:
        outcome = "validWithWarnings"
    modules = module_statuses(document, diagnostics)
    aduc = document.get("aduc", {}) if isinstance(document, dict) else {}
    return {
        "reportVersion": REPORT_VERSION,
        "source": source,
        "valid": outcome in {"valid", "validWithWarnings", "requiresHumanReview"},
        "outcome": outcome,
        "contractId": aduc.get("contractId") if isinstance(aduc, dict) else None,
        "coreVersion": aduc.get("coreVersion") if isinstance(aduc, dict) else None,
        "summary": summary,
        "pipeline": {
            "jsonLoaded": document is not None,
            "schemaValid": schema_valid,
            "architectureValid": architecture_valid,
            "profileEvaluation": profile_evaluation,
        },
        "modules": modules,
        "profileEvaluations": profile_evaluations or [],
        "diagnostics": diagnostics,
    }


def module_statuses(document: Any, diagnostics: list[dict[str, Any]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    present = set(document) if isinstance(document, dict) else set()
    for module in MODULE_ORDER:
        if module == "extensions":
            declared = isinstance(document, dict) and isinstance(document.get("aduc"), dict) and bool(document["aduc"].get("extensionDeclarations"))
            if not declared:
                result[module] = {"status": "notDescribed"}
                continue
        elif module not in present:
            result[module] = {"status": "notDescribed"}
            continue
        module_items = [item for item in diagnostics if item["module"] == module]
        if any(item["severity"] == "error" for item in module_items):
            status = "invalid"
        elif any(item["severity"] == "humanReview" for item in module_items):
            status = "requiresHumanReview"
        elif any(item["severity"] == "warning" for item in module_items):
            status = "validWithWarnings"
        else:
            status = "valid"
        result[module] = {"status": status}
    return result


def validate_path(path: Path, *, schema_only: bool = False, profile_evaluation: bool = True) -> dict[str, Any]:
    try:
        payload = load_json_file(path)
    except InputError as exc:
        return input_error_report(str(path), exc)
    if isinstance(payload, dict) and isinstance(payload.get("cases"), list):
        reports = []
        for index, case in enumerate(payload["cases"]):
            label = str(case.get("id", index)) if isinstance(case, dict) else str(index)
            document = case.get("document") if isinstance(case, dict) else None
            reports.append(
                validate_contract(
                    document,
                    source=f"{path}#{label}",
                    schema_only=schema_only,
                    profile_evaluation=profile_evaluation,
                )
            )
        return suite_report(str(path), reports)
    return validate_contract(payload, source=str(path), schema_only=schema_only, profile_evaluation=profile_evaluation)


def suite_report(source: str, reports: list[dict[str, Any]]) -> dict[str, Any]:
    diagnostics: list[dict[str, Any]] = []
    for report in reports:
        diagnostics.extend(report["diagnostics"])
    summary = {
        "errors": sum(report["summary"]["errors"] for report in reports),
        "warnings": sum(report["summary"]["warnings"] for report in reports),
        "humanReview": sum(report["summary"]["humanReview"] for report in reports),
    }
    outcome = "valid"
    if summary["errors"]:
        outcome = "blocked"
    elif summary["humanReview"]:
        outcome = "requiresHumanReview"
    elif summary["warnings"]:
        outcome = "validWithWarnings"
    return {
        "reportVersion": REPORT_VERSION,
        "source": source,
        "valid": outcome in {"valid", "validWithWarnings", "requiresHumanReview"},
        "outcome": outcome,
        "summary": summary,
        "results": reports,
        "diagnostics": stable_diagnostics(diagnostics),
    }


def validation_exit(report: dict[str, Any]) -> int:
    if report.get("inputError"):
        return EXIT_USAGE
    if report.get("outcome") == "blocked":
        return EXIT_BLOCKED
    if report.get("outcome") == "requiresHumanReview":
        return EXIT_HUMAN_REVIEW
    return EXIT_VALID


def render_validation_text(report: dict[str, Any]) -> str:
    if "results" in report:
        lines = [f"SUITE {report['outcome'].upper()} {report['source']}"]
        for item in report["results"]:
            lines.append(f"  {item['outcome'].upper()} {item['source']}")
        lines.append(
            f"Summary: {report['summary']['errors']} errors, {report['summary']['warnings']} warnings, {report['summary']['humanReview']} human-review"
        )
        return "\n".join(lines)
    lines = [f"{report['outcome'].upper()} {report['source']}"]
    for item in report["diagnostics"]:
        lines.append(f"{item['severity'].upper()} {item['code']} {item['path']}: {item['message']}")
    lines.append(
        f"Summary: {report['summary']['errors']} errors, {report['summary']['warnings']} warnings, {report['summary']['humanReview']} human-review"
    )
    return "\n".join(lines)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def compare_contracts(left: Any, right: Any, *, left_source: str = "<left>", right_source: str = "<right>") -> dict[str, Any]:
    left_validation = validate_contract(left, source=left_source)
    right_validation = validate_contract(right, source=right_source)
    left_structural = bool(left_validation["pipeline"]["schemaValid"])
    right_structural = bool(right_validation["pipeline"]["schemaValid"])
    if not left_structural or not right_structural:
        changes = []
        if not left_structural:
            changes.append(change("ADUC-COMPARE-INPUT-LEFT-001", "notComparable", "contract", "$", "Left contract is not valid for comparison."))
        if not right_structural:
            changes.append(change("ADUC-COMPARE-INPUT-RIGHT-001", "notComparable", "contract", "$", "Right contract is not valid for comparison."))
        return finalize_compare_report(left, right, left_validation, right_validation, changes, comparable=False)
    left_dangerous = dangerous_compare_diagnostics(left_validation)
    right_dangerous = dangerous_compare_diagnostics(right_validation)
    if left_dangerous or right_dangerous:
        changes = []
        if left_dangerous:
            changes.append(
                change(
                    "ADUC-COMPARE-INPUT-LEFT-002",
                    "notComparable",
                    "contract",
                    "$",
                    "Left contract has architectural diagnostics that make identifier-based comparison unsafe.",
                    evidence={"diagnosticCodes": sorted({item["code"] for item in left_dangerous})},
                )
            )
        if right_dangerous:
            changes.append(
                change(
                    "ADUC-COMPARE-INPUT-RIGHT-002",
                    "notComparable",
                    "contract",
                    "$",
                    "Right contract has architectural diagnostics that make identifier-based comparison unsafe.",
                    evidence={"diagnosticCodes": sorted({item["code"] for item in right_dangerous})},
                )
            )
        return finalize_compare_report(left, right, left_validation, right_validation, changes, comparable=False)

    changes: list[dict[str, Any]] = []
    changes.extend(compare_contract_metadata(left, right))
    changes.extend(compare_resource(left, right))
    changes.extend(compare_structure(left, right))
    changes.extend(compare_object_collection(left, right, "semantics", "$.semantics.assertions", "assertions", semantic_field_classification))
    changes.extend(compare_object_collection(left, right, "identity", "$.identity.entities", "entities", generic_field_classification("identity")))
    changes.extend(compare_object_collection(left, right, "identity", "$.identity.identifiers", "identifiers", identity_field_classification))
    changes.extend(compare_object_collection(left, right, "identity", "$.identity.identityAssertions", "identityAssertions", identity_assertion_classification))
    changes.extend(compare_context(left, right))
    changes.extend(compare_provenance(left, right))
    changes.extend(compare_object_collection(left, right, "uncertainty", "$.uncertainty.statements", "statements", uncertainty_field_classification))
    changes.extend(compare_object_collection(left, right, "uncertainty", "$.uncertainty.qualityMeasurements", "qualityMeasurements", uncertainty_field_classification))
    changes.extend(compare_relations(left, right))
    changes.extend(compare_policy(left, right))
    changes.extend(compare_extensions(left, right))
    enrich_unit_changes(changes, left, right)
    return finalize_compare_report(left, right, left_validation, right_validation, changes, comparable=True)


def dangerous_compare_diagnostics(validation: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for item in validation.get("diagnostics", []):
        code = item.get("code")
        if code in DANGEROUS_COMPARE_CODES or (
            isinstance(code, str)
            and (
                code.startswith("ADUC-CORE-OWNER-")
                or code.startswith("ADUC-CORE-BINDING-")
                or code.startswith("ADUC-CORE-EXT-")
            )
        ):
            result.append(item)
    return result


def change(
    code: str,
    classification: str,
    module: str,
    path: str,
    message: str,
    *,
    object_id: str | None = None,
    before: Any = None,
    after: Any = None,
    change_type: str | None = None,
    assessment: str | None = None,
    dimension: str | None = None,
    evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "code": code,
        "classification": classification,
        "changeType": change_type or default_change_type(classification),
        "assessment": assessment or default_assessment(classification, code),
        "module": module,
        "dimension": dimension or default_dimension(code, module),
        "path": path,
        "message": message,
    }
    if object_id is not None:
        item["objectId"] = object_id
    if before is not None:
        item["before"] = before
    if after is not None:
        item["after"] = after
    if evidence is not None:
        item["evidence"] = evidence
    return item


def default_change_type(classification: str) -> str:
    if classification in {"added", "removed", "unchanged"}:
        return classification
    return "modified"


def default_assessment(classification: str, code: str) -> str:
    if code.endswith("LIFECYCLE-001") or "-LIFECYCLE-" in code:
        return "deprecated"
    if "CONFLICT" in code or "CONTRADICTION" in code:
        return "contested"
    if "PROHIBITION" in code:
        return "prohibited"
    if classification == "compatible":
        return "compatible"
    if classification == "incompatible":
        return "incompatible"
    if classification == "requiresHumanReview":
        return "requiresHumanReview"
    if classification == "unchanged":
        return "equivalent"
    return "unknown"


def default_dimension(code: str, module: str) -> str:
    parts = code.split("-")
    if len(parts) >= 4 and parts[0:2] == ["ADUC", "COMPARE"]:
        return parts[3].lower()
    return module


def stable_changes(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for item in items:
        key = canonical(item)
        if key not in seen:
            seen.add(key)
            unique.append(item)
    unique.sort(
        key=lambda item: (
            CLASSIFICATION_ORDER.get(item["classification"], 99),
            ASSESSMENT_ORDER.get(item.get("assessment"), 99),
            CHANGE_TYPE_ORDER.get(item.get("changeType"), 99),
            MODULE_INDEX.get(item["module"], 99),
            item.get("path", ""),
            item.get("code", ""),
            item.get("objectId", ""),
        )
    )
    return unique


def finalize_compare_report(
    left: Any,
    right: Any,
    left_validation: dict[str, Any],
    right_validation: dict[str, Any],
    changes: list[dict[str, Any]],
    *,
    comparable: bool,
) -> dict[str, Any]:
    changes = stable_changes(changes)
    if not comparable:
        overall = "notComparable"
        overall_assessment = "unknown"
    elif not changes:
        overall = "unchanged"
        overall_assessment = "equivalent"
    elif any(item["classification"] == "incompatible" for item in changes):
        overall = "incompatible"
        overall_assessment = strongest_assessment(changes)
    elif any(item["classification"] == "potentiallyIncompatible" for item in changes):
        overall = "potentiallyIncompatible"
        overall_assessment = strongest_assessment(changes)
    elif any(item["classification"] == "requiresHumanReview" for item in changes):
        overall = "requiresHumanReview"
        overall_assessment = strongest_assessment(changes)
    elif any(item["classification"] == "modified" for item in changes):
        overall = "modified"
        overall_assessment = strongest_assessment(changes)
    else:
        overall = "compatible"
        overall_assessment = strongest_assessment(changes)
    summary = {name: 0 for name in CLASSIFICATION_ORDER}
    summary["humanReview"] = 0
    assessment_summary = {name: 0 for name in ASSESSMENT_ORDER}
    for item in changes:
        summary[item["classification"]] = summary.get(item["classification"], 0) + 1
        if item["classification"] == "requiresHumanReview":
            summary["humanReview"] += 1
        assessment_summary[item["assessment"]] = assessment_summary.get(item["assessment"], 0) + 1
    summary["assessments"] = assessment_summary
    return {
        "reportVersion": REPORT_VERSION,
        "comparable": comparable,
        "overall": overall,
        "overallAssessment": overall_assessment,
        "left": endpoint_info(left, left_validation),
        "right": endpoint_info(right, right_validation),
        "summary": summary,
        "changes": changes,
    }


def strongest_assessment(changes: list[dict[str, Any]]) -> str:
    if not changes:
        return "equivalent"
    return min((item.get("assessment", "unknown") for item in changes), key=lambda item: ASSESSMENT_ORDER.get(item, 99))


def endpoint_info(document: Any, validation: dict[str, Any]) -> dict[str, Any]:
    aduc = document.get("aduc", {}) if isinstance(document, dict) else {}
    return {
        "contractId": aduc.get("contractId") if isinstance(aduc, dict) else None,
        "valid": validation["valid"],
        "outcome": validation["outcome"],
    }


def compare_contract_metadata(left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    l_aduc = left.get("aduc", {}) if isinstance(left, dict) else {}
    r_aduc = right.get("aduc", {}) if isinstance(right, dict) else {}
    fields = {
        "contractId": ("ADUC-COMPARE-CONTRACT-ID-001", "modified", "Contract identifier changed."),
        "coreVersion": ("ADUC-COMPARE-CONTRACT-VERSION-001", "modified", "Core version changed."),
        "modelVersion": ("ADUC-COMPARE-CONTRACT-MODEL-001", "modified", "Core model version changed."),
        "status": ("ADUC-COMPARE-CONTRACT-STATUS-001", "requiresHumanReview", "Contract publication status changed."),
        "supersedes": ("ADUC-COMPARE-CONTRACT-SUPERSEDES-001", "modified", "Contract replacement relation changed."),
    }
    for field, (code, classification, message) in fields.items():
        if l_aduc.get(field) != r_aduc.get(field):
            changes.append(change(code, classification, "aduc", f"$.aduc.{field}", message, before=l_aduc.get(field), after=r_aduc.get(field)))
    if sorted(l_aduc.get("conformsTo", [])) != sorted(r_aduc.get("conformsTo", [])):
        changes.append(change("ADUC-COMPARE-CONTRACT-PROFILES-001", "requiresHumanReview", "aduc", "$.aduc.conformsTo", "Declared conformance profiles changed.", before=sorted(l_aduc.get("conformsTo", [])), after=sorted(r_aduc.get("conformsTo", []))))
    return changes


def compare_resource(left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    fields = {
        "digest": ("ADUC-COMPARE-RESOURCE-DIGEST-001", "potentiallyIncompatible", "Resource digest changed; this is not simple equality."),
        "version": ("ADUC-COMPARE-RESOURCE-VERSION-001", "modified", "Resource version changed."),
        "kind": ("ADUC-COMPARE-RESOURCE-KIND-001", "incompatible", "Resource kind changed."),
        "mediaType": ("ADUC-COMPARE-RESOURCE-MEDIA-001", "incompatible", "Resource media type changed."),
        "descriptorRefs": ("ADUC-COMPARE-RESOURCE-DESCRIPTOR-001", "potentiallyIncompatible", "Resource structural descriptor references changed."),
    }
    result: list[dict[str, Any]] = []
    l_res = left.get("resource", {}) if isinstance(left, dict) else {}
    r_res = right.get("resource", {}) if isinstance(right, dict) else {}
    for field, (code, classification, message) in fields.items():
        if l_res.get(field) != r_res.get(field):
            result.append(change(code, classification, "resource", f"$.resource.{field}", message, object_id=l_res.get("id") or r_res.get("id"), before=l_res.get(field), after=r_res.get(field)))
    return result


def compare_structure(left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    l_structure = left.get("structure", {}) if isinstance(left, dict) else {}
    r_structure = right.get("structure", {}) if isinstance(right, dict) else {}
    if l_structure.get("externalSchemaRef") != r_structure.get("externalSchemaRef"):
        changes.append(change("ADUC-COMPARE-STRUCTURE-SCHEMA-001", "potentiallyIncompatible", "structure", "$.structure.externalSchemaRef", "External structural schema reference changed.", before=l_structure.get("externalSchemaRef"), after=r_structure.get("externalSchemaRef")))
    changes.extend(compare_object_collection(left, right, "structure", "$.structure.records", "records", record_field_classification))
    l_fields = fields_by_id(l_structure)
    r_fields = fields_by_id(r_structure)
    for object_id in sorted(set(l_fields) | set(r_fields)):
        l_path, l_field = l_fields.get(object_id, (None, None))
        r_path, r_field = r_fields.get(object_id, (None, None))
        path = r_path or l_path or "$.structure.records"
        if l_field is None:
            classification = "compatible" if r_field.get("required") is False else "potentiallyIncompatible"
            code = "ADUC-COMPARE-STRUCTURE-FIELD-ADDED-OPTIONAL-001" if classification == "compatible" else "ADUC-COMPARE-STRUCTURE-FIELD-ADDED-REQUIRED-001"
            changes.append(change(code, classification, "structure", path, "Structural field was added.", object_id=object_id, after=r_field))
            continue
        if r_field is None:
            classification = "incompatible" if l_field.get("required") is True else "potentiallyIncompatible"
            changes.append(change("ADUC-COMPARE-STRUCTURE-FIELD-REMOVED-001", classification, "structure", path, "Structural field was removed.", object_id=object_id, before=l_field))
            continue
        for field in ("sourcePath", "primitiveType", "required", "name"):
            if l_field.get(field) == r_field.get(field):
                continue
            if field == "primitiveType":
                code, classification, message = "ADUC-COMPARE-STRUCTURE-PRIMITIVE-001", "incompatible", "Primitive field type changed."
            elif field == "required":
                if l_field.get(field) is False and r_field.get(field) is True:
                    code, classification, message = "ADUC-COMPARE-STRUCTURE-REQUIRED-001", "incompatible", "A previously optional field is now required."
                else:
                    code, classification, message = "ADUC-COMPARE-STRUCTURE-REQUIRED-002", "compatible", "A previously required field is now optional."
            else:
                code, classification, message = "ADUC-COMPARE-STRUCTURE-FIELD-001", "potentiallyIncompatible", f"Structural field {field} changed."
            changes.append(change(code, classification, "structure", f"{path}.{field}", message, object_id=object_id, before=l_field.get(field), after=r_field.get(field)))
    return changes


def fields_by_id(structure: dict[str, Any]) -> dict[str, tuple[str, dict[str, Any]]]:
    result: dict[str, tuple[str, dict[str, Any]]] = {}
    for r_index, record in enumerate(structure.get("records", [])):
        if not isinstance(record, dict):
            continue
        for f_index, field in enumerate(record.get("fields", [])):
            if isinstance(field, dict) and isinstance(field.get("id"), str):
                result.setdefault(field["id"], (f"$.structure.records[{r_index}].fields[{f_index}]", field))
    return result


def record_field_classification(object_id: str, path: str, left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    fields = {
        "name": ("ADUC-COMPARE-STRUCTURE-RECORD-001", "potentiallyIncompatible", "Record name changed."),
        "sourcePath": ("ADUC-COMPARE-STRUCTURE-RECORD-002", "potentiallyIncompatible", "Record source path changed."),
    }
    left_without_fields = {key: value for key, value in left.items() if key != "fields"}
    right_without_fields = {key: value for key, value in right.items() if key != "fields"}
    if canonical(left_without_fields) == canonical(right_without_fields):
        return []
    return field_changes("structure", object_id, path, left_without_fields, right_without_fields, fields, "ADUC-COMPARE-STRUCTURE-RECORD-MODIFIED-001")


def map_by_id(items: Any, base_path: str) -> dict[str, tuple[str, dict[str, Any]]]:
    result: dict[str, tuple[str, dict[str, Any]]] = {}
    if isinstance(items, list):
        for index, item in enumerate(items):
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                result.setdefault(item["id"], (f"{base_path}[{index}]", item))
    return result


def compare_object_collection(
    left: dict[str, Any],
    right: dict[str, Any],
    module: str,
    base_path: str,
    collection: str,
    classifier,
) -> list[dict[str, Any]]:
    l_module = left.get(module, {}) if isinstance(left, dict) else {}
    r_module = right.get(module, {}) if isinstance(right, dict) else {}
    l_map = map_by_id(l_module.get(collection), base_path) if isinstance(l_module, dict) else {}
    r_map = map_by_id(r_module.get(collection), base_path) if isinstance(r_module, dict) else {}
    changes: list[dict[str, Any]] = []
    for object_id in sorted(set(l_map) | set(r_map)):
        l_path, l_obj = l_map.get(object_id, (None, None))
        r_path, r_obj = r_map.get(object_id, (None, None))
        path = r_path or l_path or base_path
        if l_obj is None:
            changes.append(change(f"ADUC-COMPARE-{module.upper()}-ADDED-001", "added", module, path, f"{module} object was added.", object_id=object_id, after=r_obj))
        elif r_obj is None:
            changes.append(change(f"ADUC-COMPARE-{module.upper()}-REMOVED-001", "removed", module, path, f"{module} object was removed.", object_id=object_id, before=l_obj))
        elif canonical(l_obj) != canonical(r_obj):
            changes.extend(classifier(object_id, path, l_obj, r_obj))
    return changes


def generic_field_classification(module: str):
    def classify(object_id: str, path: str, left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
        return [change(f"ADUC-COMPARE-{module.upper()}-MODIFIED-001", "modified", module, path, f"{module} object changed.", object_id=object_id)]
    return classify


def semantic_field_classification(object_id: str, path: str, left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    fields = {
        "conceptIri": ("ADUC-COMPARE-SEMANTICS-CONCEPT-001", "potentiallyIncompatible", "Semantic concept changed."),
        "unitIri": ("ADUC-COMPARE-SEMANTICS-UNIT-001", "potentiallyIncompatible", "Semantic unit changed."),
        "mappingRelationIri": ("ADUC-COMPARE-SEMANTICS-RELATION-001", "requiresHumanReview", "Semantic mapping relation changed."),
        "authority": ("ADUC-COMPARE-SEMANTICS-AUTHORITY-001", "requiresHumanReview", "Semantic authority changed."),
        "status": ("ADUC-COMPARE-SEMANTICS-STATUS-001", "requiresHumanReview", "Semantic assertion status changed."),
        "conflict": ("ADUC-COMPARE-SEMANTICS-CONFLICT-001", "requiresHumanReview", "Semantic conflict state changed."),
        "lifecycle": ("ADUC-COMPARE-SEMANTICS-LIFECYCLE-001", "requiresHumanReview", "Semantic lifecycle state changed."),
    }
    return field_changes("semantics", object_id, path, left, right, fields, "ADUC-COMPARE-SEMANTICS-MODIFIED-001")


def enrich_unit_changes(changes: list[dict[str, Any]], left: dict[str, Any], right: dict[str, Any]) -> None:
    for item in changes:
        if item.get("code") != "ADUC-COMPARE-SEMANTICS-UNIT-001" or not item.get("objectId"):
            continue
        left_assertion = object_by_id(left.get("semantics", {}).get("assertions", []), item["objectId"])
        right_assertion = object_by_id(right.get("semantics", {}).get("assertions", []), item["objectId"])
        assessment, evidence = assess_unit_change(left, right, left_assertion, right_assertion)
        item["assessment"] = assessment
        item["evidence"] = evidence
        if assessment == "convertible":
            item["classification"] = "compatible"
        elif assessment == "incompatible":
            item["classification"] = "incompatible"
        elif assessment == "requiresHumanReview":
            item["classification"] = "requiresHumanReview"
        else:
            item["classification"] = "potentiallyIncompatible"


def object_by_id(items: Any, object_id: str) -> dict[str, Any] | None:
    if not isinstance(items, list):
        return None
    for item in items:
        if isinstance(item, dict) and item.get("id") == object_id:
            return item
    return None


def assess_unit_change(
    left: dict[str, Any],
    right: dict[str, Any],
    left_assertion: dict[str, Any] | None,
    right_assertion: dict[str, Any] | None,
) -> tuple[str, dict[str, Any]]:
    evidence: dict[str, Any] = {"evaluator": "ADR-0007", "conversionSupported": False}
    if not left_assertion or not right_assertion:
        evidence["missingData"] = ["semantic assertion not found on both sides"]
        return "unknown", evidence
    left_profile = unit_compare_profile(left, str(left_assertion.get("id")))
    right_profile = unit_compare_profile(right, str(right_assertion.get("id")))
    if not left_profile or not right_profile:
        evidence["missingData"] = ["unit comparison profile metadata with registry, quantity, role, rounding, and uncertainty preservation is required"]
        return "unknown", evidence
    if left_assertion.get("uncertaintyRef") or right_assertion.get("uncertaintyRef"):
        if left_profile.get("uncertaintyPreserved") is not True or right_profile.get("uncertaintyPreserved") is not True:
            evidence["missingData"] = ["uncertainty preservation policy is required when uncertaintyRef is present"]
            return "requiresHumanReview", evidence
    registry_ref = right_profile.get("registry") or left_profile.get("registry")
    registry, _provenance, registry_errors = aduc_units.load_registry(registry_ref, ROOT / "examples" / "units")
    if registry is None:
        evidence["errors"] = registry_errors
        return "unknown", evidence
    case = {
        "registry": registry_ref,
        "source": {
            "value": "1",
            "assertion": unit_assertion_for_comparison(left_assertion, left_profile),
        },
        "target": {
            "assertion": unit_assertion_for_comparison(right_assertion, right_profile),
        },
        "rounding": right_profile.get("rounding") or left_profile.get("rounding"),
    }
    report = aduc_units.convert_case(case, ROOT / "examples" / "units")
    evidence["errors"] = report.get("errors", [])
    evidence["registryVerified"] = True
    evidence["conversionSupported"] = bool(report.get("valid"))
    if report.get("valid"):
        evidence["result"] = report.get("result")
        return "convertible", evidence
    codes = {error.get("code") for error in report.get("errors", []) if isinstance(error, dict)}
    if codes & {"ADUC-COMPAT-001", "ADUC-COMPAT-002", "ADUC-COMPAT-003", "ADUC-CONV-003", "ADUC-UNIT-004"}:
        return "incompatible", evidence
    if "ADUC-CONV-005" in codes:
        return "requiresHumanReview", evidence
    return "unknown", evidence


def unit_compare_profile(document: dict[str, Any], assertion_id: str) -> dict[str, Any] | None:
    for payloads in extension_payloads(document).values():
        for payload in payloads:
            found = unit_compare_profile_in_payload(payload, assertion_id)
            if found is not None:
                return found
    return None


def unit_compare_profile_in_payload(payload: Any, assertion_id: str) -> dict[str, Any] | None:
    if isinstance(payload, dict):
        profiles = payload.get("unitProfiles")
        if isinstance(profiles, dict) and isinstance(profiles.get(assertion_id), dict):
            return profiles[assertion_id]
        for child in payload.values():
            found = unit_compare_profile_in_payload(child, assertion_id)
            if found is not None:
                return found
    elif isinstance(payload, list):
        for child in payload:
            found = unit_compare_profile_in_payload(child, assertion_id)
            if found is not None:
                return found
    return None


def unit_assertion_for_comparison(assertion: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    return {
        "sourceBinding": profile.get("sourceBinding", assertion.get("subjectRef")),
        "localReference": profile.get("localReference", {"scheme": "json-pointer", "base": "description", "value": assertion.get("subjectRef", "")}),
        "quantityKind": profile.get("quantityKind"),
        "dimensionVector": profile.get("dimensionVector"),
        "quantityRole": profile.get("quantityRole"),
        "unitState": profile.get("unitState", "known"),
        "unit": {"identifier": normalize_qudt_iri(assertion.get("unitIri"))},
        "authorityStatus": assertion.get("status", "reviewed"),
        "conflictState": assertion.get("conflict", "clear"),
        "lifecycleState": assertion.get("lifecycle", "active"),
    }


def identity_field_classification(object_id: str, path: str, left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    fields = {
        "schemeIri": ("ADUC-COMPARE-IDENTITY-SCHEME-001", "requiresHumanReview", "Identifier scheme changed."),
        "issuerIri": ("ADUC-COMPARE-IDENTITY-ISSUER-001", "requiresHumanReview", "Identifier issuer changed."),
    }
    return field_changes("identity", object_id, path, left, right, fields, "ADUC-COMPARE-IDENTITY-MODIFIED-001")


def identity_assertion_classification(object_id: str, path: str, left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    fields = {
        "decision": ("ADUC-COMPARE-IDENTITY-DECISION-001", "requiresHumanReview", "Identity decision changed."),
        "identityRelationIri": ("ADUC-COMPARE-IDENTITY-RELATION-001", "requiresHumanReview", "Identity relation changed."),
        "conflict": ("ADUC-COMPARE-IDENTITY-CONFLICT-001", "requiresHumanReview", "Identity conflict state changed."),
    }
    changes = field_changes("identity", object_id, path, left, right, fields, "ADUC-COMPARE-IDENTITY-MODIFIED-001")
    if left.get("decision") != "exactEntity" and right.get("decision") == "exactEntity":
        changes.append(change("ADUC-COMPARE-IDENTITY-PROMOTION-001", "requiresHumanReview", "identity", path + ".decision", "Identity changed from possible or unresolved to exact.", object_id=object_id, before=left.get("decision"), after=right.get("decision")))
    return changes


def uncertainty_field_classification(object_id: str, path: str, left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    fields = {
        "kind": ("ADUC-COMPARE-UNCERTAINTY-KIND-001", "potentiallyIncompatible", "Uncertainty kind changed."),
        "value": ("ADUC-COMPARE-UNCERTAINTY-VALUE-001", "potentiallyIncompatible", "Uncertainty value changed."),
        "methodIri": ("ADUC-COMPARE-UNCERTAINTY-METHOD-001", "requiresHumanReview", "Uncertainty method changed."),
        "qualityMetricIri": ("ADUC-COMPARE-UNCERTAINTY-QUALITY-001", "potentiallyIncompatible", "Quality metric changed."),
    }
    return field_changes("uncertainty", object_id, path, left, right, fields, "ADUC-COMPARE-UNCERTAINTY-MODIFIED-001")


def field_changes(
    module: str,
    object_id: str,
    path: str,
    left: dict[str, Any],
    right: dict[str, Any],
    fields: dict[str, tuple[str, str, str]],
    default_code: str,
) -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    seen = False
    for field, (code, classification, message) in fields.items():
        if left.get(field) != right.get(field):
            seen = True
            changes.append(change(code, classification, module, f"{path}.{field}", message, object_id=object_id, before=left.get(field), after=right.get(field)))
    if not seen and canonical(left) != canonical(right):
        changes.append(change(default_code, "modified", module, path, f"{module} object changed.", object_id=object_id))
    return changes


def compare_context(left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    fields = {
        "temporalRoleIri": ("ADUC-COMPARE-CONTEXT-TEMPORAL-ROLE-001", "potentiallyIncompatible", "Temporal role changed."),
        "timezoneIri": ("ADUC-COMPARE-CONTEXT-TIMEZONE-001", "potentiallyIncompatible", "Timezone changed."),
        "precision": ("ADUC-COMPARE-CONTEXT-PRECISION-001", "potentiallyIncompatible", "Temporal precision changed."),
        "spatialCoverageIri": ("ADUC-COMPARE-CONTEXT-SPATIAL-001", "modified", "Spatial scope changed."),
        "environmentIri": ("ADUC-COMPARE-CONTEXT-OPERATIONAL-001", "modified", "Operational context changed."),
    }
    for collection in ("temporal", "spatial", "operational"):
        changes.extend(compare_object_collection(left, right, "context", f"$.context.{collection}", collection, lambda oid, path, l_obj, r_obj: field_changes("context", oid, path, l_obj, r_obj, fields, "ADUC-COMPARE-CONTEXT-MODIFIED-001")))
    return changes


def compare_provenance(left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    for collection in ("agents", "entities", "activities", "evidence", "derivationAssertions"):
        changes.extend(compare_object_collection(left, right, "provenance", f"$.provenance.{collection}", collection, generic_field_classification("provenance")))
    return changes


def compare_relations(left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    changes = compare_relation_collection(left, right)
    right_relations = right.get("relations", []) if isinstance(right, dict) else []
    relation_keys: dict[tuple[str, str, str], set[str]] = {}
    for relation in right_relations if isinstance(right_relations, list) else []:
        if isinstance(relation, dict):
            key = (str(relation.get("subjectRef")), str(relation.get("predicateIri")), relation_endpoint(relation))
            relation_keys.setdefault(key, set()).add(str(relation.get("polarity")))
    for key, polarities in relation_keys.items():
        if {"positive", "negative"}.issubset(polarities):
            changes.append(change("ADUC-COMPARE-RELATION-CONTRADICTION-001", "incompatible", "relations", "$.relations", "Positive and negative relation assertions now contradict each other.", object_id="|".join(key)))
    return changes


def compare_relation_collection(left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    fields = {
        "subjectRef": ("ADUC-COMPARE-RELATION-ORIENTATION-001", "potentiallyIncompatible", "Relation subject changed."),
        "objectRef": ("ADUC-COMPARE-RELATION-ORIENTATION-002", "potentiallyIncompatible", "Relation object changed."),
        "literalObject": ("ADUC-COMPARE-RELATION-LITERAL-001", "modified", "Relation literal object changed."),
        "predicateIri": ("ADUC-COMPARE-RELATION-PREDICATE-001", "potentiallyIncompatible", "Relation predicate changed."),
        "polarity": ("ADUC-COMPARE-RELATION-POLARITY-001", "incompatible", "Relation polarity changed."),
        "status": ("ADUC-COMPARE-RELATION-QUALIFICATION-001", "requiresHumanReview", "Relation qualification changed."),
        "conflict": ("ADUC-COMPARE-RELATION-CONFLICT-001", "requiresHumanReview", "Relation conflict state changed."),
        "lifecycle": ("ADUC-COMPARE-RELATION-LIFECYCLE-001", "requiresHumanReview", "Relation lifecycle state changed."),
    }
    l_items = left.get("relations", []) if isinstance(left, dict) else []
    r_items = right.get("relations", []) if isinstance(right, dict) else []
    l_map = map_by_id(l_items, "$.relations")
    r_map = map_by_id(r_items, "$.relations")
    changes: list[dict[str, Any]] = []
    for object_id in sorted(set(l_map) | set(r_map)):
        l_path, l_obj = l_map.get(object_id, (None, None))
        r_path, r_obj = r_map.get(object_id, (None, None))
        path = r_path or l_path or "$.relations"
        if l_obj is None:
            changes.append(change("ADUC-COMPARE-RELATION-ADDED-001", "added", "relations", path, "Relation was added.", object_id=object_id, after=r_obj))
        elif r_obj is None:
            changes.append(change("ADUC-COMPARE-RELATION-REMOVED-001", "removed", "relations", path, "Relation was removed.", object_id=object_id, before=l_obj))
        elif canonical(l_obj) != canonical(r_obj):
            changes.extend(field_changes("relations", object_id, path, l_obj, r_obj, fields, "ADUC-COMPARE-RELATION-MODIFIED-001"))
    return changes


def compare_policy(left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    changes = compare_object_collection(left, right, "policy", "$.policy.policies", "policies", policy_record_classification)
    l_rules = policy_rules_by_id(left.get("policy", {}) if isinstance(left, dict) else {})
    r_rules = policy_rules_by_id(right.get("policy", {}) if isinstance(right, dict) else {})
    for object_id in sorted(set(l_rules) | set(r_rules)):
        l_path, l_rule = l_rules.get(object_id, (None, None))
        r_path, r_rule = r_rules.get(object_id, (None, None))
        path = r_path or l_path or "$.policy.policies"
        if l_rule is None:
            classification = "potentiallyIncompatible" if r_rule.get("effect") == "prohibition" else "requiresHumanReview"
            code = "ADUC-COMPARE-POLICY-PROHIBITION-ADDED-001" if r_rule.get("effect") == "prohibition" else "ADUC-COMPARE-POLICY-RULE-ADDED-001"
            changes.append(change(code, classification, "policy", path, "Policy rule was added.", object_id=object_id, after=r_rule))
        elif r_rule is None:
            changes.append(change("ADUC-COMPARE-POLICY-RULE-REMOVED-001", "requiresHumanReview", "policy", path, "Policy rule was removed.", object_id=object_id, before=l_rule))
        elif canonical(l_rule) != canonical(r_rule):
            changes.extend(policy_rule_classification(object_id, path, l_rule, r_rule))
    return changes


def policy_rules_by_id(policy: dict[str, Any]) -> dict[str, tuple[str, dict[str, Any]]]:
    result: dict[str, tuple[str, dict[str, Any]]] = {}
    for p_index, policy_record in enumerate(policy.get("policies", [])):
        if not isinstance(policy_record, dict):
            continue
        for r_index, rule in enumerate(policy_record.get("rules", [])):
            if isinstance(rule, dict) and isinstance(rule.get("id"), str):
                result.setdefault(rule["id"], (f"$.policy.policies[{p_index}].rules[{r_index}]", rule))
    return result


def policy_record_classification(object_id: str, path: str, left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    fields = {
        "mode": ("ADUC-COMPARE-POLICY-MODE-001", "requiresHumanReview", "Policy mode changed."),
        "validFrom": ("ADUC-COMPARE-POLICY-VALIDITY-001", "requiresHumanReview", "Policy validity start changed."),
        "validUntil": ("ADUC-COMPARE-POLICY-VALIDITY-002", "requiresHumanReview", "Policy validity end changed."),
        "conflict": ("ADUC-COMPARE-POLICY-CONFLICT-001", "requiresHumanReview", "Policy conflict state changed."),
        "disclosure": ("ADUC-COMPARE-POLICY-DISCLOSURE-001", "requiresHumanReview", "Policy disclosure changed."),
    }
    return field_changes("policy", object_id, path, left, right, fields, "ADUC-COMPARE-POLICY-MODIFIED-001")


def policy_rule_classification(object_id: str, path: str, left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    fields = {
        "effect": ("ADUC-COMPARE-POLICY-EFFECT-001", "potentiallyIncompatible", "Policy rule effect changed."),
        "actionIri": ("ADUC-COMPARE-POLICY-ACTION-001", "potentiallyIncompatible", "Policy action changed."),
        "purposeIris": ("ADUC-COMPARE-POLICY-PURPOSE-001", "potentiallyIncompatible", "Policy purpose changed."),
        "phase": ("ADUC-COMPARE-POLICY-DUTY-001", "requiresHumanReview", "Policy duty phase changed."),
    }
    return field_changes("policy", object_id, path, left, right, fields, "ADUC-COMPARE-POLICY-RULE-MODIFIED-001")


def compare_extensions(left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    l_decls = extension_declarations(left)
    r_decls = extension_declarations(right)
    for namespace in sorted(set(l_decls) | set(r_decls)):
        if namespace not in l_decls:
            classification = "requiresHumanReview" if r_decls[namespace].get("required") else "compatible"
            changes.append(change("ADUC-COMPARE-EXTENSION-DECL-ADDED-001", classification, "extensions", "$.aduc.extensionDeclarations", "Extension declaration was added.", object_id=namespace, after=r_decls[namespace]))
        elif namespace not in r_decls:
            changes.append(change("ADUC-COMPARE-EXTENSION-DECL-REMOVED-001", "requiresHumanReview", "extensions", "$.aduc.extensionDeclarations", "Extension declaration was removed.", object_id=namespace, before=l_decls[namespace]))
        elif canonical(l_decls[namespace]) != canonical(r_decls[namespace]):
            classification = "requiresHumanReview" if r_decls[namespace].get("required") else "modified"
            changes.append(change("ADUC-COMPARE-EXTENSION-DECL-MODIFIED-001", classification, "extensions", "$.aduc.extensionDeclarations", "Extension declaration changed.", object_id=namespace, before=l_decls[namespace], after=r_decls[namespace]))
    l_payloads = extension_payloads(left)
    r_payloads = extension_payloads(right)
    for namespace in sorted(set(l_payloads) | set(r_payloads)):
        if canonical(l_payloads.get(namespace)) != canonical(r_payloads.get(namespace)):
            changes.append(change("ADUC-COMPARE-EXTENSION-PAYLOAD-001", "requiresHumanReview", "extensions", "$..extensions", "Extension payload changed.", object_id=namespace, before=l_payloads.get(namespace), after=r_payloads.get(namespace)))
    return changes


def extension_declarations(document: dict[str, Any]) -> dict[str, dict[str, Any]]:
    aduc = document.get("aduc", {}) if isinstance(document, dict) else {}
    result = {}
    for declaration in aduc.get("extensionDeclarations", []) if isinstance(aduc, dict) else []:
        if isinstance(declaration, dict) and isinstance(declaration.get("namespace"), str):
            result[declaration["namespace"]] = declaration
    return result


def extension_payloads(document: dict[str, Any]) -> dict[str, list[Any]]:
    result: dict[str, list[Any]] = {}
    for _path, key, value, _parent in walk(document):
        if key == "extensions" and isinstance(value, dict):
            for namespace, payload in value.items():
                result.setdefault(namespace, []).append(payload)
    return result


def compare_paths(left_path: Path, right_path: Path) -> dict[str, Any]:
    try:
        left = load_json_file(left_path)
        right = load_json_file(right_path)
    except InputError as exc:
        item = change(exc.code, "notComparable", "contract", exc.path, exc.message)
        summary = {name: 0 for name in CLASSIFICATION_ORDER}
        summary["notComparable"] = 1
        summary["humanReview"] = 0
        return {
            "reportVersion": REPORT_VERSION,
            "comparable": False,
            "overall": "notComparable",
            "left": {"contractId": None, "valid": False, "outcome": "blocked"},
            "right": {"contractId": None, "valid": False, "outcome": "blocked"},
            "summary": summary,
            "changes": [item],
            "inputError": True,
        }
    return compare_contracts(left, right, left_source=str(left_path), right_source=str(right_path))


def compare_exit(report: dict[str, Any]) -> int:
    if report.get("inputError"):
        return EXIT_USAGE
    if not report.get("comparable"):
        return EXIT_BLOCKED
    if report.get("overall") == "incompatible":
        return EXIT_BLOCKED
    if report.get("overall") in {"potentiallyIncompatible", "requiresHumanReview"}:
        return EXIT_HUMAN_REVIEW
    return EXIT_VALID


def render_compare_text(report: dict[str, Any]) -> str:
    lines = [f"COMPARE {report['overall'].upper()}"]
    for item in report["changes"]:
        object_id = f" {item.get('objectId')}" if item.get("objectId") else ""
        lines.append(f"{item['classification'].upper()} {item['code']}{object_id} {item['path']}: {item['message']}")
    return "\n".join(lines)


def emit(payload: dict[str, Any], output_format: str, mode: str) -> None:
    if output_format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
    elif mode == "compare":
        print(render_compare_text(payload))
    else:
        print(render_validation_text(payload))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate", help="Validate one Core contract or fixture suite")
    validate.add_argument("contract", type=Path)
    validate.add_argument("--format", choices=("text", "json"), default="text", dest="output_format")
    validate.add_argument("--schema-only", action="store_true", help="Run only JSON Schema validation")
    validate.add_argument("--no-profile-evaluation", action="store_true", help="Skip cross-module profile safeguards")
    compare = subparsers.add_parser("compare", help="Compare two Core contracts")
    compare.add_argument("left", type=Path)
    compare.add_argument("right", type=Path)
    compare.add_argument("--format", choices=("text", "json"), default="text", dest="output_format")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "validate":
        report = validate_path(
            args.contract,
            schema_only=args.schema_only,
            profile_evaluation=not args.no_profile_evaluation,
        )
        emit(report, args.output_format, "validate")
        return validation_exit(report)
    if args.command == "compare":
        report = compare_paths(args.left, args.right)
        emit(report, args.output_format, "compare")
        return compare_exit(report)
    return EXIT_USAGE


if __name__ == "__main__":
    raise SystemExit(main())
