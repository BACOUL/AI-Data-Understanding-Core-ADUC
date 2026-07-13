#!/usr/bin/env python3
"""Evaluate ADUC source-description and immutable-binding reference cases."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXAMPLES = ROOT / "examples" / "source-description"

HEX_64 = re.compile(r"^[0-9a-f]{64}$")
BINDING_MODES = {"content", "description", "content-and-description"}
DESCRIPTION_KINDS = {"croissant", "json-schema", "openapi", "dcat", "custom"}
REFERENCE_SCHEMES = {
    "json-pointer",
    "croissant-field-id",
    "csv-header",
    "openapi-operation-ref",
    "openapi-schema-pointer",
    "dcat-resource-iri",
    "custom-iri",
}
CSV_DIALECT_FIELDS = {
    "encoding",
    "delimiter",
    "quoteChar",
    "headerRow",
    "headerPolicy",
    "uniqueHeaders",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    """Canonicalize the RFC 8785-safe subset used by official fixtures.

    Production implementations must use a complete RFC 8785 implementation.
    The reference fixtures intentionally avoid floating-point values and other
    cases where Python's standard serializer could differ from ECMAScript JCS.
    """

    def reject_float(item: Any) -> None:
        if isinstance(item, float):
            raise ValueError("reference JCS evaluator does not accept floats")
        if isinstance(item, list):
            for child in item:
                reject_float(child)
        elif isinstance(item, dict):
            for key, child in item.items():
                if not isinstance(key, str):
                    raise ValueError("JSON object keys must be strings")
                reject_float(child)

    reject_float(value)
    text = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return text.encode("utf-8")


def error(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


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


def validate_digest(digest: Any, expected_scope: str | None = None) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    if not isinstance(digest, dict):
        return [error("ADUC-BIND-003", "digest object is required")]
    if digest.get("algorithm") != "sha-256":
        errors.append(error("ADUC-BIND-003", "only sha-256 is supported in v0.1"))
    value = digest.get("value")
    if not isinstance(value, str) or not HEX_64.fullmatch(value):
        errors.append(error("ADUC-BIND-003", "digest value must be 64 lowercase hexadecimal characters"))
    scope = digest.get("scope")
    if scope not in {"raw-bytes", "jcs"}:
        errors.append(error("ADUC-BIND-003", "digest scope must be raw-bytes or jcs"))
    if expected_scope and scope != expected_scope:
        errors.append(error("ADUC-BIND-003", f"digest scope must be {expected_scope}"))
    return errors


def resolve_json_pointer(document: Any, pointer: str) -> Any:
    if pointer == "":
        return document
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ValueError("invalid JSON Pointer syntax")
    current = document
    for token in pointer.split("/")[1:]:
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            if token not in current:
                raise KeyError(token)
            current = current[token]
        elif isinstance(current, list):
            if token == "-" or not token.isdigit() or (len(token) > 1 and token.startswith("0")):
                raise KeyError(token)
            index = int(token)
            if index >= len(current):
                raise KeyError(token)
            current = current[index]
        else:
            raise KeyError(token)
    return current


def find_jsonld_id(value: Any, target: str) -> int:
    count = 0
    if isinstance(value, dict):
        if value.get("@id") == target:
            count += 1
        for child in value.values():
            count += find_jsonld_id(child, target)
    elif isinstance(value, list):
        for child in value:
            count += find_jsonld_id(child, target)
    return count


def verify_subject(
    subject: Any,
    *,
    root: Path,
    mismatch_code: str,
    required: bool,
    description: bool,
) -> tuple[Any | None, bytes | None, list[dict[str, str]]]:
    errors: list[dict[str, str]] = []
    if not isinstance(subject, dict):
        if required:
            errors.append(error("ADUC-BIND-003", "required binding subject is missing"))
        return None, None, errors

    identifier = subject.get("identifier")
    media_type = subject.get("mediaType")
    if not isinstance(identifier, str) or not identifier:
        errors.append(error("ADUC-BIND-003", "subject identifier is required"))
    if not isinstance(media_type, str) or not media_type:
        errors.append(error("ADUC-BIND-003", "subject mediaType is required"))

    location = subject.get("location")
    embedded_present = "embedded" in subject
    if description:
        if (location is None) == (not embedded_present):
            errors.append(error("ADUC-BIND-003", "description requires exactly one of location or embedded"))
    elif location is None:
        errors.append(error("ADUC-BIND-003", "resource location is required by the reference evaluator"))

    expected_scope = "jcs" if embedded_present else "raw-bytes"
    errors.extend(validate_digest(subject.get("digest"), expected_scope))
    if errors:
        return None, None, errors

    parsed: Any | None = None
    raw: bytes | None = None
    if embedded_present:
        parsed = subject.get("embedded")
        if not isinstance(parsed, (dict, list)):
            return None, None, [error("ADUC-BIND-003", "embedded description must be a JSON object or array")]
        try:
            raw = canonical_json_bytes(parsed)
        except ValueError as exc:
            return None, None, [error("ADUC-BIND-003", str(exc))]
    else:
        if not isinstance(location, str) or not location:
            return None, None, [error("ADUC-BIND-003", "location must be a non-empty string")]
        local_path = safe_local_path(root, location)
        if local_path is None or not local_path.exists():
            return None, None, [error("ADUC-BIND-005", f"required subject is unavailable: {location}")]
        raw = local_path.read_bytes()
        if description or media_type.endswith("json") or "+json" in media_type:
            try:
                parsed = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                if description:
                    return None, raw, [error("ADUC-BIND-004", "description could not be parsed as JSON")]

    actual = sha256_bytes(raw)
    expected = subject["digest"]["value"]
    if actual != expected:
        return parsed, raw, [error(mismatch_code, f"digest mismatch: expected {expected}, got {actual}")]
    return parsed, raw, []


def verify_description_identity(description: dict[str, Any], parsed: Any) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    if not isinstance(parsed, dict):
        return [error("ADUC-BIND-004", "description root must be an object")]

    kind = description.get("kind")
    if kind not in DESCRIPTION_KINDS:
        return [error("ADUC-BIND-004", f"unsupported description kind: {kind}")]
    conforms_to = description.get("conformsTo")
    if not isinstance(conforms_to, str) or not conforms_to:
        errors.append(error("ADUC-BIND-003", "description conformsTo is required"))
    identifier = description.get("identifier")
    version = description.get("version")

    if kind == "json-schema":
        if parsed.get("$id") != identifier:
            errors.append(error("ADUC-BIND-004", "JSON Schema $id does not match description identifier"))
        if parsed.get("$schema") != conforms_to:
            errors.append(error("ADUC-BIND-004", "JSON Schema dialect does not match conformsTo"))
        if version and isinstance(identifier, str) and version not in identifier:
            errors.append(error("ADUC-BIND-004", "declared JSON Schema version is not represented by the bound identifier"))

    elif kind == "openapi":
        if parsed.get("$self") != identifier:
            errors.append(error("ADUC-BIND-004", "OpenAPI $self does not match description identifier"))
        info = parsed.get("info")
        parsed_version = info.get("version") if isinstance(info, dict) else None
        if version and parsed_version != version:
            errors.append(error("ADUC-BIND-004", "OpenAPI info.version does not match description version"))
        openapi_version = parsed.get("openapi")
        if not isinstance(openapi_version, str) or openapi_version not in conforms_to:
            errors.append(error("ADUC-BIND-004", "OpenAPI version does not match conformsTo"))

    elif kind == "custom":
        if parsed.get("$id") != identifier:
            errors.append(error("ADUC-BIND-004", "custom description $id does not match description identifier"))
        if parsed.get("conformsTo") != conforms_to:
            errors.append(error("ADUC-BIND-004", "custom description conformsTo mismatch"))
        if not version or parsed.get("version") != version:
            errors.append(error("ADUC-DESC-002", "custom description requires matching explicit version"))

    elif kind == "croissant":
        root_id = parsed.get("@id") or parsed.get("url")
        if root_id != identifier:
            errors.append(error("ADUC-BIND-004", "Croissant dataset identifier mismatch"))
        declared = parsed.get("conformsTo") or parsed.get("dct:conformsTo")
        values = declared if isinstance(declared, list) else [declared]
        if conforms_to not in values:
            errors.append(error("ADUC-BIND-004", "Croissant conformsTo mismatch"))

    elif kind == "dcat":
        if parsed.get("@id") != identifier:
            errors.append(error("ADUC-BIND-004", "DCAT resource identifier mismatch"))

    return errors


def parse_csv_headers(description: dict[str, Any]) -> tuple[list[str] | None, list[dict[str, str]]]:
    dialect = description.get("dialect")
    headers = description.get("headers")
    if not isinstance(dialect, dict) or not CSV_DIALECT_FIELDS.issubset(dialect):
        return None, [error("ADUC-REF-004", "CSV dialect is incomplete")]
    if dialect.get("headerPolicy") != "exact-codepoints" or dialect.get("uniqueHeaders") is not True:
        return None, [error("ADUC-REF-004", "CSV dialect must require exact code points and unique headers")]
    if not isinstance(headers, list) or not all(isinstance(item, str) for item in headers):
        return None, [error("ADUC-REF-004", "CSV description headers must be an array of strings")]
    if len(headers) != len(set(headers)):
        return headers, [error("ADUC-REF-003", "CSV headers are duplicated")]
    return headers, []


def verify_csv_resource_headers(
    resource_raw: bytes | None,
    description: dict[str, Any],
    declared_headers: list[str],
) -> list[dict[str, str]]:
    if resource_raw is None:
        return []
    dialect = description["dialect"]
    try:
        text = resource_raw.decode(dialect["encoding"])
        reader = csv.reader(
            io.StringIO(text),
            delimiter=dialect["delimiter"],
            quotechar=dialect["quoteChar"],
        )
        rows = list(reader)
        header_index = int(dialect["headerRow"]) - 1
        actual_headers = rows[header_index]
    except (UnicodeDecodeError, csv.Error, ValueError, IndexError, TypeError) as exc:
        return [error("ADUC-REF-004", f"CSV header could not be parsed: {exc}")]
    if actual_headers != declared_headers:
        return [error("ADUC-BIND-004", "CSV resource headers do not match the bound description")]
    return []


def verify_local_references(
    references: Any,
    *,
    resource_parsed: Any,
    resource_raw: bytes | None,
    description_parsed: Any,
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    if references is None:
        return errors
    if not isinstance(references, list):
        return [error("ADUC-REF-002", "localReferences must be an array")]

    csv_headers: list[str] | None = None
    csv_checked = False
    for index, reference in enumerate(references):
        if not isinstance(reference, dict):
            errors.append(error("ADUC-REF-002", f"reference {index} must be an object"))
            continue
        scheme = reference.get("scheme")
        base = reference.get("base")
        value = reference.get("value")
        if scheme not in REFERENCE_SCHEMES or base not in {"resource", "description"} or not isinstance(value, str):
            errors.append(error("ADUC-REF-002", f"reference {index} lacks a supported scheme, base, or value"))
            continue
        document = description_parsed if base == "description" else resource_parsed

        try:
            if scheme == "json-pointer":
                resolve_json_pointer(document, value)

            elif scheme == "openapi-operation-ref":
                if not value.startswith("#"):
                    raise ValueError("reference implementation requires a same-document operation fragment")
                fragment = unquote(value[1:])
                target = resolve_json_pointer(document, fragment)
                if not isinstance(target, dict) or "responses" not in target:
                    raise ValueError("reference does not resolve to an Operation Object")

            elif scheme == "croissant-field-id":
                if find_jsonld_id(document, value) != 1:
                    raise ValueError("Croissant field IRI must resolve exactly once")

            elif scheme == "csv-header":
                if not isinstance(description_parsed, dict):
                    raise ValueError("CSV description is unavailable")
                if not csv_checked:
                    csv_headers, csv_errors = parse_csv_headers(description_parsed)
                    errors.extend(csv_errors)
                    if csv_headers is not None and not csv_errors:
                        errors.extend(verify_csv_resource_headers(resource_raw, description_parsed, csv_headers))
                    csv_checked = True
                if csv_headers is None or value not in csv_headers:
                    raise ValueError("CSV header does not resolve")

            elif scheme in {"openapi-schema-pointer", "custom-iri", "dcat-resource-iri"}:
                raise ValueError(f"{scheme} is specified but not implemented by the reference evaluator")

        except (KeyError, TypeError, ValueError) as exc:
            errors.append(error("ADUC-REF-001", f"reference {index} failed: {exc}"))

    return errors


def evaluate_binding(binding: Any, root: Path) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    if not isinstance(binding, dict):
        return {"valid": False, "errors": [error("ADUC-BIND-003", "binding must be an object")]}

    mode = binding.get("bindingMode")
    if mode not in BINDING_MODES:
        return {"valid": False, "errors": [error("ADUC-BIND-003", "unsupported bindingMode")]}

    resource_required = mode in {"content", "content-and-description"}
    description_required = mode in {"description", "content-and-description"}

    resource_parsed, resource_raw, resource_errors = verify_subject(
        binding.get("resource"),
        root=root,
        mismatch_code="ADUC-BIND-001",
        required=resource_required,
        description=False,
    )
    errors.extend(resource_errors)

    description_subject = binding.get("description")
    description_parsed, _, description_errors = verify_subject(
        description_subject,
        root=root,
        mismatch_code="ADUC-BIND-002",
        required=description_required,
        description=True,
    )
    errors.extend(description_errors)

    if isinstance(description_subject, dict) and description_parsed is not None and not description_errors:
        errors.extend(verify_description_identity(description_subject, description_parsed))

    copied = binding.get("copiedStructure")
    if isinstance(copied, dict) and copied.get("conflictsWithDescription") is True:
        errors.append(error("ADUC-DESC-001", "copied structure conflicts with the authoritative description"))

    if not errors or not any(item["code"].startswith("ADUC-BIND") for item in errors):
        errors.extend(
            verify_local_references(
                binding.get("localReferences"),
                resource_parsed=resource_parsed,
                resource_raw=resource_raw,
                description_parsed=description_parsed,
            )
        )

    unique = {(item["code"], item["message"]): item for item in errors}
    sorted_errors = sorted(unique.values(), key=lambda item: (item["code"], item["message"]))
    return {
        "valid": not sorted_errors,
        "errors": sorted_errors,
    }


def evaluate_cases(path: Path, examples_root: Path = DEFAULT_EXAMPLES) -> dict[str, Any]:
    document = load_json(path)
    cases = document.get("cases") if isinstance(document, dict) else None
    if not isinstance(cases, list):
        raise ValueError("case document must contain a cases array")

    results: list[dict[str, Any]] = []
    suite_matches = True
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("each case must be an object")
        case_id = case.get("caseId")
        base_directory = case.get("baseDirectory", ".")
        if not isinstance(case_id, str) or not isinstance(base_directory, str):
            raise ValueError("caseId and baseDirectory must be strings")
        root = safe_local_path(examples_root, base_directory)
        if root is None:
            report = {"valid": False, "errors": [error("ADUC-BIND-005", "case base directory escapes examples root")]}
        else:
            report = evaluate_binding(case.get("binding"), root)
        expected_valid = case.get("expectedValid")
        expected_error = case.get("expectedError")
        codes = {item["code"] for item in report["errors"]}
        matches = report["valid"] is expected_valid and (
            expected_error is None or expected_error in codes
        )
        suite_matches = suite_matches and matches
        results.append(
            {
                "caseId": case_id,
                "expectedValid": expected_valid,
                "expectedError": expected_error,
                "matchesExpectation": matches,
                **report,
            }
        )

    return {
        "protocol": "urn:aduc:source-binding-evaluation:0.1",
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
