#!/usr/bin/env python3
"""Architectural checker for the ADUC Core Object Model 0.1.

This is not the official full-Core JSON Schema validator. It enforces only the
object-model invariants frozen by ADR-0014.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXAMPLE = ROOT / "examples" / "core" / "complete-model.example.json"
DEFAULT_INVALID = ROOT / "examples" / "core" / "invalid-model-cases.json"
DEFAULT_MANIFEST = ROOT / "spec" / "core-module-manifest.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
HIDDEN_KEYS = {"prompt", "consumerPrompt", "consumerInstructions", "hiddenMapping", "providerMapping", "modelInstructions"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def iri(value: Any) -> bool:
    return isinstance(value, str) and bool(urlparse(value).scheme)


def error(code: str, message: str, path: str = "$") -> dict[str, str]:
    return {"code": code, "message": message, "path": path}


def walk(value: Any, path: str = "$") -> Iterable[tuple[str, str | int | None, Any, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            yield child_path, key, child, value
            yield from walk(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_path = f"{path}[{index}]"
            yield child_path, index, child, value
            yield from walk(child, child_path)


def patch(document: Any, operations: list[list[Any]]) -> Any:
    result = copy.deepcopy(document)
    for operation, path, *rest in operations:
        target = result
        for key in path[:-1]:
            target = target[key]
        key = path[-1]
        value = rest[0] if rest else None
        if operation == "set":
            target[key] = copy.deepcopy(value)
        elif operation == "remove":
            if isinstance(target, dict):
                target.pop(key, None)
            else:
                target.pop(key)
        elif operation == "append":
            target[key].append(copy.deepcopy(value))
        else:
            raise ValueError(f"Unsupported patch operation: {operation}")
    return result


def dependency_errors(manifest: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    modules = manifest.get("modules", {})
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(module: str, trail: list[str]) -> None:
        if module in visiting:
            errors.append(error("ADUC-CORE-DEPENDENCY-002", f"circular hard dependency: {' -> '.join(trail + [module])}", "$.modules"))
            return
        if module in visited:
            return
        if module not in modules:
            errors.append(error("ADUC-CORE-DEPENDENCY-002", f"unknown dependency module {module}", "$.modules"))
            return
        visiting.add(module)
        for dependency in modules[module].get("hardDependencies", []):
            visit(dependency, trail + [module])
        visiting.remove(module)
        visited.add(module)

    for name in modules:
        visit(name, [])
    return errors


def collect_ids(document: dict[str, Any]) -> tuple[set[str], list[dict[str, str]]]:
    identifiers: set[str] = set()
    errors: list[dict[str, str]] = []
    contract_id = document.get("aduc", {}).get("contractId") if isinstance(document.get("aduc"), dict) else None
    candidates: list[tuple[str, Any]] = [("$.aduc.contractId", contract_id)]
    for path, key, value, _parent in walk(document):
        if key == "id":
            candidates.append((path, value))
    for path, value in candidates:
        if not iri(value):
            errors.append(error("ADUC-CORE-ID-001", "Core identifier must be an absolute IRI", path))
            continue
        if value in identifiers:
            errors.append(error("ADUC-CORE-ID-002", f"duplicate Core identifier {value}", path))
        identifiers.add(value)
    return identifiers, errors


def validate_references(document: dict[str, Any], identifiers: set[str]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    for path, key, value, _parent in walk(document):
        if isinstance(key, str) and key.endswith("Ref"):
            if not iri(value) or value not in identifiers:
                errors.append(error("ADUC-CORE-REF-001", f"unresolved Core reference {value!r}", path))
        elif isinstance(key, str) and key.endswith("Refs"):
            if not isinstance(value, list) or not all(iri(item) and item in identifiers for item in value):
                errors.append(error("ADUC-CORE-REF-001", "Core reference list contains an unresolved identifier", path))
        elif isinstance(key, str) and (key.endswith("Iri") or key.endswith("Iris")):
            values = value if key.endswith("Iris") else [value]
            if not isinstance(values, list) or not all(iri(item) for item in values):
                errors.append(error("ADUC-CORE-IRI-001", "external vocabulary term must be an absolute IRI", path))

    policy = document.get("policy")
    if isinstance(policy, dict):
        for p_index, policy_record in enumerate(policy.get("policies", [])):
            for r_index, rule in enumerate(policy_record.get("rules", [])):
                duties = rule.get("duties", [])
                if not isinstance(duties, list) or not all(iri(item) and item in identifiers for item in duties):
                    errors.append(error("ADUC-CORE-REF-001", "policy duty reference is unresolved", f"$.policy.policies[{p_index}].rules[{r_index}].duties"))
    return errors


def validate_extensions(document: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    aduc = document.get("aduc", {})
    declarations = aduc.get("extensionDeclarations", []) if isinstance(aduc, dict) else []
    declared: dict[str, dict[str, Any]] = {}
    if not isinstance(declarations, list):
        return [error("ADUC-CORE-EXT-001", "extensionDeclarations must be an array", "$.aduc.extensionDeclarations")]
    for index, declaration in enumerate(declarations):
        path = f"$.aduc.extensionDeclarations[{index}]"
        if not isinstance(declaration, dict) or not iri(declaration.get("namespace")) or not iri(declaration.get("profileIri")):
            errors.append(error("ADUC-CORE-EXT-001", "invalid extension declaration", path))
            continue
        namespace = declaration["namespace"]
        if namespace.startswith("urn:aduc:core:"):
            errors.append(error("ADUC-CORE-EXT-004", "extension must not use the ADUC Core namespace", path + ".namespace"))
        if namespace in declared:
            errors.append(error("ADUC-CORE-EXT-001", "duplicate extension namespace", path + ".namespace"))
        declared[namespace] = declaration
        if declaration.get("required") is True:
            errors.append(error("ADUC-CORE-EXT-003", "reference checker does not support a required extension", path))

    for path, key, value, parent in walk(document):
        if key != "extensions":
            continue
        if not isinstance(value, dict):
            errors.append(error("ADUC-CORE-EXT-001", "extensions payload must be an object", path))
            continue
        host_keys = set(parent) - {"extensions"} if isinstance(parent, dict) else set()
        for namespace, payload in value.items():
            namespace_path = f"{path}.{namespace}"
            if namespace not in declared:
                errors.append(error("ADUC-CORE-EXT-001", "extension namespace is not declared", namespace_path))
            if namespace.startswith("urn:aduc:core:"):
                errors.append(error("ADUC-CORE-EXT-004", "extension payload uses the ADUC Core namespace", namespace_path))
            if not isinstance(payload, dict):
                errors.append(error("ADUC-CORE-EXT-001", "extension namespace payload must be an object", namespace_path))
                continue
            overwritten = host_keys.intersection(payload)
            if overwritten:
                errors.append(error("ADUC-CORE-EXT-002", f"extension overwrites Core term(s): {sorted(overwritten)}", namespace_path))
    return errors


def validate_ownership(document: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    resource = document.get("resource")
    if isinstance(resource, dict):
        forbidden = {"producer", "license", "concept", "conceptIri", "unit", "unitIri", "measurementUncertainty", "policy"}
        for key in forbidden.intersection(resource):
            errors.append(error("ADUC-CORE-OWNER-001", f"resource does not own {key}", f"$.resource.{key}"))

    structure = document.get("structure")
    if isinstance(structure, dict):
        if "externalSchema" in structure:
            errors.append(error("ADUC-CORE-EXTERNAL-001", "embed external schema by reference, not as a copied object", "$.structure.externalSchema"))
        for r_index, record in enumerate(structure.get("records", [])):
            for f_index, field in enumerate(record.get("fields", [])):
                for key in {"concept", "conceptIri", "unit", "unitIri", "temporalRoleIri", "measurementUncertainty"}.intersection(field):
                    errors.append(error("ADUC-CORE-OWNER-001", f"structural field does not own {key}", f"$.structure.records[{r_index}].fields[{f_index}].{key}"))

    semantics = document.get("semantics")
    if isinstance(semantics, dict):
        for index, assertion in enumerate(semantics.get("assertions", [])):
            for key in {"measurementUncertainty", "relativeError", "standardUncertainty", "identityDecision"}.intersection(assertion):
                errors.append(error("ADUC-CORE-OWNER-001", f"semantic assertion does not own {key}", f"$.semantics.assertions[{index}].{key}"))

    context = document.get("context")
    if isinstance(context, dict) and "fields" in context:
        errors.append(error("ADUC-CORE-OWNER-001", "context must reference structural fields rather than redefine them", "$.context.fields"))

    relations = document.get("relations")
    if isinstance(relations, list):
        for index, relation in enumerate(relations):
            if isinstance(relation, dict) and (isinstance(relation.get("subject"), dict) or isinstance(relation.get("object"), dict)):
                errors.append(error("ADUC-CORE-OWNER-001", "relation endpoints must be references, not embedded Core objects", f"$.relations[{index}]"))
    return errors


def validate_safety(document: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    for path, key, value, parent in walk(document):
        if key in HIDDEN_KEYS:
            errors.append(error("ADUC-CORE-HIDDEN-001", "provider- or consumer-specific hidden mapping is forbidden", path))
        if isinstance(parent, dict) and parent.get("generationMethod") == "inferred" and key == "status" and value in {"reviewed", "verified", "canonical"}:
            errors.append(error("ADUC-CORE-AUTH-001", "inferred assertion cannot be promoted silently", path))

    identity = document.get("identity")
    if isinstance(identity, dict):
        for index, assertion in enumerate(identity.get("identityAssertions", [])):
            relation = assertion.get("identityRelationIri", "")
            if assertion.get("decision") == "exactEntity" and isinstance(relation, str) and ("closeMatch" in relation or "possible" in relation.lower()):
                errors.append(error("ADUC-CORE-IDENTITY-001", "probable identity cannot be represented as exact", f"$.identity.identityAssertions[{index}]"))

    policy = document.get("policy")
    if isinstance(policy, dict):
        for p_index, policy_record in enumerate(policy.get("policies", [])):
            for r_index, rule in enumerate(policy_record.get("rules", [])):
                if rule.get("effect") in {"classification", "legalNotice", "recommendation"} and rule.get("machineEvaluable") is True:
                    errors.append(error("ADUC-CORE-POLICY-001", "descriptive or human-only policy statement cannot be executable", f"$.policy.policies[{p_index}].rules[{r_index}]"))
    return errors


def validate_document(document: Any, manifest: dict[str, Any]) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    if not isinstance(document, dict):
        return {"valid": False, "errors": [error("ADUC-CORE-ENVELOPE-001", "Core contract must be an object")]}

    modules = manifest.get("modules", {})
    allowed = set(manifest.get("topLevelOrder", []))
    present = set(document)
    for required in manifest.get("minimumEnvelope", []):
        if required not in document:
            errors.append(error("ADUC-CORE-ENVELOPE-001", f"missing required block {required}", f"$.{required}"))
    for unknown in sorted(present - allowed):
        errors.append(error("ADUC-CORE-ENVELOPE-002", f"unknown top-level block {unknown}", f"$.{unknown}"))

    for name in present.intersection(allowed):
        specification = modules[name]
        expected = specification.get("representation")
        actual = document[name]
        if expected == "object" and not isinstance(actual, dict):
            errors.append(error("ADUC-CORE-CARDINALITY-001", f"{name} must be one object", f"$.{name}"))
        if expected == "array" and not isinstance(actual, list):
            errors.append(error("ADUC-CORE-CARDINALITY-001", f"{name} must be one array", f"$.{name}"))
        for dependency in specification.get("hardDependencies", []):
            if dependency not in document:
                errors.append(error("ADUC-CORE-DEPENDENCY-001", f"{name} requires {dependency}", f"$.{name}"))

    errors.extend(dependency_errors(manifest))

    aduc = document.get("aduc")
    if isinstance(aduc, dict):
        for key in ("contractId", "coreVersion", "modelVersion", "status", "createdAt", "publisher", "conformsTo"):
            if key not in aduc:
                errors.append(error("ADUC-CORE-ENVELOPE-001", f"aduc.{key} is required", f"$.aduc.{key}"))
        if not iri(aduc.get("publisher")):
            errors.append(error("ADUC-CORE-IRI-001", "publisher must be an absolute IRI", "$.aduc.publisher"))
        conforms = aduc.get("conformsTo")
        if not isinstance(conforms, list) or not conforms or not all(iri(item) for item in conforms):
            errors.append(error("ADUC-CORE-IRI-001", "conformsTo must contain absolute IRIs", "$.aduc.conformsTo"))
        if aduc.get("supersedes") == aduc.get("contractId"):
            errors.append(error("ADUC-CORE-VERSION-001", "published contract cannot supersede itself", "$.aduc.supersedes"))

    resource = document.get("resource")
    if isinstance(resource, dict):
        for key in ("id", "kind", "mediaType", "digest"):
            if key not in resource:
                errors.append(error("ADUC-CORE-ENVELOPE-001", f"resource.{key} is required", f"$.resource.{key}"))
        if not HEX64.fullmatch(str(resource.get("digest", ""))):
            errors.append(error("ADUC-CORE-BINDING-001", "resource digest must be lowercase SHA-256 hex", "$.resource.digest"))

    structure = document.get("structure")
    if isinstance(structure, dict):
        for key in ("id", "resourceRef", "representation", "records"):
            if key not in structure:
                errors.append(error("ADUC-CORE-ENVELOPE-001", f"structure.{key} is required", f"$.structure.{key}"))
        if isinstance(resource, dict) and structure.get("resourceRef") != resource.get("id"):
            errors.append(error("ADUC-CORE-REF-002", "structure must bind the exact resource.id", "$.structure.resourceRef"))

    for path, key, value, _parent in walk(document):
        if key in {"digest", "targetDigest"} and not HEX64.fullmatch(str(value)):
            errors.append(error("ADUC-CORE-BINDING-001", "digest must be lowercase SHA-256 hex", path))

    identifiers, id_errors = collect_ids(document)
    errors.extend(id_errors)
    errors.extend(validate_references(document, identifiers))
    errors.extend(validate_extensions(document))
    errors.extend(validate_ownership(document))
    errors.extend(validate_safety(document))

    policy = document.get("policy")
    if isinstance(policy, dict) and isinstance(resource, dict):
        for index, record in enumerate(policy.get("policies", [])):
            if record.get("targetRef") == resource.get("id") and record.get("targetDigest") != resource.get("digest"):
                errors.append(error("ADUC-CORE-BINDING-001", "policy target digest must match bound resource", f"$.policy.policies[{index}].targetDigest"))

    return {"valid": not errors, "errors": errors, "objectCount": len(identifiers)}


def run(example_path: Path, invalid_path: Path, manifest_path: Path) -> dict[str, Any]:
    manifest = load(manifest_path)
    example = load(example_path)
    invalid_suite = load(invalid_path)
    valid_result = validate_document(example, manifest)
    failures: list[dict[str, Any]] = []
    rejected = 0
    for case in invalid_suite.get("cases", []):
        result = validate_document(patch(example, case.get("patch", [])), manifest)
        codes = {item["code"] for item in result.get("errors", [])}
        if not result["valid"] and case.get("code") in codes:
            rejected += 1
        else:
            failures.append({"id": case.get("id"), "expectedCode": case.get("code"), "actual": result})
    if not valid_result["valid"]:
        failures.insert(0, {"id": "complete-model.example.json", "actual": valid_result})
    return {
        "ok": not failures,
        "validExampleAccepted": valid_result["valid"],
        "invalidRejected": rejected,
        "invalidTotal": len(invalid_suite.get("cases", [])),
        "objectCount": valid_result.get("objectCount", 0),
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("example", nargs="?", type=Path, default=DEFAULT_EXAMPLE)
    parser.add_argument("invalid", nargs="?", type=Path, default=DEFAULT_INVALID)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    result = run(args.example, args.invalid, args.manifest)
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"Accepted complete model: {result['validExampleAccepted']}")
        print(f"Rejected invalid models: {result['invalidRejected']}/{result['invalidTotal']}")
        print(f"Addressable objects: {result['objectCount']}")
        if result["failures"]:
            for failure in result["failures"]:
                print(f"FAIL {failure['id']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())