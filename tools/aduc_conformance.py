#!/usr/bin/env python3
"""Freeze, verify, validate, and evaluate ADUC multi-model conformance runs."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULT_SCHEMA = ROOT / "schema" / "model-conformance-result.schema.json"
DEFAULT_EXPECTED = ROOT / "examples" / "conformance" / "expected.json"
MANIFEST_NAME = "manifest.json"
MANIFEST_PROTOCOL = "urn:aduc:conformance-package-manifest:0.1"
REPORT_PROTOCOL = "urn:aduc:conformance-evaluation:0.1"
REQUIRED_SCENARIOS = {
    "exact-different-names",
    "inferred-candidate",
    "close-match-candidate",
    "contested-blocked",
    "same-name-different-targets",
    "missing-dimensions",
}

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_INPUT = 2

FULL_CORE_REPORT_VERSION = "0.1.0"
FULL_CORE_SUITE_PROTOCOL = "urn:aduc:full-core-conformance-suite:0.1"
FULL_CORE_ADAPTER_PROTOCOL = "urn:aduc:full-core-conformance-adapter:0.1"
FULL_CORE_RESULT_ORDER = {
    "pass": 0,
    "fail": 1,
    "unsupported": 2,
    "invalidAdapterResponse": 3,
    "timeout": 4,
    "resourceFailure": 5,
}
FULL_CORE_OUTCOMES = {
    "unknown",
    "contested",
    "prohibited",
    "requiresHumanReview",
}
DEFAULT_FULL_CORE_SUITE = ROOT / "conformance" / "full-core" / "0.1"
DEFAULT_ADAPTER_TIMEOUT_SECONDS = 5
DEFAULT_ADAPTER_OUTPUT_BYTES = 200_000


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def inventory(package_dir: Path) -> list[dict[str, Any]]:
    files: list[dict[str, Any]] = []
    for path in sorted(package_dir.rglob("*")):
        if not path.is_file() or path.name == MANIFEST_NAME:
            continue
        relative = path.relative_to(package_dir).as_posix()
        data = path.read_bytes()
        files.append(
            {
                "path": relative,
                "size": len(data),
                "sha256": sha256_bytes(data),
            }
        )
    return files


def compute_package_digest(files: Iterable[dict[str, Any]]) -> str:
    payload = b"".join(
        (
            str(item["path"]).encode("utf-8")
            + b"\0"
            + str(item["sha256"]).encode("ascii")
            + b"\n"
        )
        for item in sorted(files, key=lambda item: str(item["path"]))
    )
    return sha256_bytes(payload)


def freeze_package(package_dir: Path) -> dict[str, Any]:
    files = inventory(package_dir)
    if not files:
        raise ValueError("Conformance package contains no files.")
    manifest = {
        "protocol": MANIFEST_PROTOCOL,
        "packageId": "urn:aduc:conformance-package:0.1",
        "files": files,
        "packageDigest": compute_package_digest(files),
    }
    manifest_path = package_dir / MANIFEST_NAME
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def verify_package(package_dir: Path) -> dict[str, Any]:
    manifest_path = package_dir / MANIFEST_NAME
    errors: list[str] = []
    if not manifest_path.exists():
        return {
            "valid": False,
            "packageDigest": None,
            "errors": ["manifest.json is missing"],
        }
    manifest = load_json(manifest_path)
    if not isinstance(manifest, dict):
        return {
            "valid": False,
            "packageDigest": None,
            "errors": ["manifest.json must contain an object"],
        }
    if manifest.get("protocol") != MANIFEST_PROTOCOL:
        errors.append("manifest protocol is invalid")
    recorded_files = manifest.get("files")
    if not isinstance(recorded_files, list):
        errors.append("manifest files must be an array")
        recorded_files = []
    actual_files = inventory(package_dir)
    if recorded_files != actual_files:
        recorded_by_path = {
            str(item.get("path")): item
            for item in recorded_files
            if isinstance(item, dict)
        }
        actual_by_path = {str(item["path"]): item for item in actual_files}
        for path in sorted(set(recorded_by_path) | set(actual_by_path)):
            if path not in recorded_by_path:
                errors.append(f"unrecorded package file: {path}")
            elif path not in actual_by_path:
                errors.append(f"recorded package file is missing: {path}")
            elif recorded_by_path[path] != actual_by_path[path]:
                errors.append(f"package file changed: {path}")
    actual_digest = compute_package_digest(actual_files)
    if manifest.get("packageDigest") != actual_digest:
        errors.append("package digest does not match the current inventory")
    return {
        "valid": not errors,
        "packageDigest": actual_digest,
        "errors": errors,
        "files": actual_files,
    }


def schema_errors(instance: Any, schema: dict[str, Any]) -> list[str]:
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: [str(part) for part in error.absolute_path],
    )
    output: list[str] = []
    for error in errors:
        path = "/" + "/".join(str(part) for part in error.absolute_path)
        output.append(f"{path or '/'}: {error.message}")
    return output


def canonical_scenario(result: dict[str, Any]) -> dict[str, Any]:
    item = json.loads(json.dumps(result))
    item["reasons"] = sorted(item.get("reasons", []))
    item["evidence"] = sorted(item.get("evidence", []))
    return item


def canonical_results(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        (canonical_scenario(item) for item in results),
        key=lambda item: item["scenarioId"],
    )


def validate_result(
    result: Any,
    schema: dict[str, Any],
    *,
    package_digest: str,
    result_path: Path | None = None,
) -> dict[str, Any]:
    errors = schema_errors(result, schema)
    warnings: list[str] = []
    raw_verified = False

    if isinstance(result, dict):
        run = result.get("run")
        if isinstance(run, dict) and run.get("packageDigest") != package_digest:
            errors.append("run.packageDigest does not match the verified package")
        results = result.get("results")
        if isinstance(results, list):
            ids = [
                item.get("scenarioId")
                for item in results
                if isinstance(item, dict)
            ]
            if len(ids) != len(set(ids)):
                errors.append("scenario IDs must be unique")
            if set(ids) != REQUIRED_SCENARIOS:
                missing = sorted(REQUIRED_SCENARIOS - set(ids))
                extra = sorted(set(ids) - REQUIRED_SCENARIOS)
                if missing:
                    errors.append("missing scenarios: " + ", ".join(missing))
                if extra:
                    errors.append("unexpected scenarios: " + ", ".join(extra))

        raw = result.get("rawOutput")
        if isinstance(raw, dict) and result_path is not None:
            raw_path_value = raw.get("path")
            expected_hash = raw.get("sha256")
            if isinstance(raw_path_value, str) and isinstance(expected_hash, str):
                raw_path = (result_path.parent / raw_path_value).resolve()
                try:
                    raw_path.relative_to(result_path.parent.resolve())
                except ValueError:
                    errors.append("raw output path escapes the result directory")
                else:
                    if not raw_path.exists():
                        errors.append(f"raw output file is missing: {raw_path_value}")
                    elif sha256_file(raw_path) != expected_hash:
                        errors.append(f"raw output digest mismatch: {raw_path_value}")
                    else:
                        raw_verified = True
        elif result_path is None:
            warnings.append("raw output digest was not verified without a result path")

    return {
        "valid": not errors,
        "errors": sorted(errors),
        "warnings": sorted(warnings),
        "rawOutputVerified": raw_verified,
    }


def expected_match(result: dict[str, Any], expected: dict[str, Any]) -> bool:
    return canonical_results(result["results"]) == canonical_results(expected["results"])


def evaluate(
    result_items: list[tuple[Path, dict[str, Any]]],
    *,
    package_report: dict[str, Any],
    schema: dict[str, Any],
    expected: dict[str, Any],
) -> dict[str, Any]:
    package_digest = str(package_report["packageDigest"])
    runs: list[dict[str, Any]] = []
    for path, result in result_items:
        validation = validate_result(
            result,
            schema,
            package_digest=package_digest,
            result_path=path,
        )
        matches_expected = validation["valid"] and expected_match(result, expected)
        run = result.get("run", {}) if isinstance(result, dict) else {}
        qualifying = bool(
            validation["valid"]
            and matches_expected
            and validation["rawOutputVerified"]
            and run.get("kind") == "external"
            and run.get("externalContextUsed") is False
        )
        runs.append(
            {
                "path": str(path),
                "runId": run.get("runId"),
                "kind": run.get("kind"),
                "provider": run.get("provider"),
                "implementation": run.get("implementation"),
                "model": run.get("model"),
                "valid": validation["valid"],
                "matchesExpected": matches_expected,
                "rawOutputVerified": validation["rawOutputVerified"],
                "qualifying": qualifying,
                "errors": validation["errors"],
                "warnings": validation["warnings"],
            }
        )

    valid_semantic_results = [
        canonical_results(result["results"])
        for (_, result), run in zip(result_items, runs)
        if run["valid"]
    ]
    semantic_agreement = bool(valid_semantic_results) and all(
        item == valid_semantic_results[0] for item in valid_semantic_results[1:]
    )
    qualifying_runs = [run for run in runs if run["qualifying"]]
    providers = {run["provider"] for run in qualifying_runs if run["provider"]}
    implementations = {
        run["implementation"]
        for run in qualifying_runs
        if run["implementation"]
    }
    independent_count = max(len(providers), len(implementations))
    interoperability_proven = bool(
        len(qualifying_runs) >= 2
        and independent_count >= 2
        and semantic_agreement
        and all(run["matchesExpected"] for run in qualifying_runs)
    )

    return {
        "protocol": REPORT_PROTOCOL,
        "packageValid": bool(package_report["valid"]),
        "packageDigest": package_digest,
        "runs": runs,
        "summary": {
            "totalRuns": len(runs),
            "validRuns": sum(run["valid"] for run in runs),
            "expectedPasses": sum(run["matchesExpected"] for run in runs),
            "qualifyingExternalRuns": len(qualifying_runs),
            "distinctQualifyingProviders": len(providers),
            "distinctQualifyingImplementations": len(implementations),
            "semanticAgreement": semantic_agreement,
            "interoperabilityProven": interoperability_proven,
        },
    }


def stable_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def sha256_json(value: Any) -> str:
    return "sha256:" + hashlib.sha256(stable_json_bytes(value)).hexdigest()


def load_full_core_suite(suite_dir: Path) -> dict[str, Any]:
    manifest = load_json(suite_dir / "manifest.json")
    if not isinstance(manifest, dict):
        raise ValueError("Full-Core conformance manifest must be an object.")
    if manifest.get("protocol") != FULL_CORE_SUITE_PROTOCOL:
        raise ValueError("Full-Core conformance manifest protocol is invalid.")
    cases = manifest.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Full-Core conformance manifest must contain cases.")
    ids = [case.get("id") for case in cases if isinstance(case, dict)]
    if len(ids) != len(cases) or len(ids) != len(set(ids)):
        raise ValueError("Full-Core conformance case identifiers must be unique strings.")
    manifest["cases"] = sorted(cases, key=lambda item: str(item["id"]))
    return manifest


def adapter_resource_limits(manifest: dict[str, Any]) -> tuple[float, int]:
    limits = manifest.get("resourceLimits", {}) if isinstance(manifest, dict) else {}
    timeout = limits.get("timeoutSeconds", DEFAULT_ADAPTER_TIMEOUT_SECONDS)
    output = limits.get("maxStdoutBytes", DEFAULT_ADAPTER_OUTPUT_BYTES)
    try:
        timeout_value = float(timeout)
        output_value = int(output)
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid conformance resource limits.") from exc
    return timeout_value, output_value


def invoke_full_core_adapter(
    adapter_command: list[str],
    operation: str,
    args: list[str],
    *,
    timeout_seconds: float,
    max_stdout_bytes: int,
) -> tuple[str, dict[str, Any] | None, list[dict[str, str]]]:
    diagnostics: list[dict[str, str]] = []
    try:
        completed = subprocess.run(
            [*adapter_command, operation, *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            shell=False,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return "timeout", None, [
            {
                "code": "ADUC-CONF-ADAPTER-TIMEOUT",
                "message": "Adapter invocation exceeded the conformance timeout.",
            }
        ]
    except OSError as exc:
        return "resourceFailure", None, [
            {
                "code": "ADUC-CONF-ADAPTER-EXEC-001",
                "message": f"Adapter could not be executed: {exc}",
            }
        ]

    stdout = completed.stdout or ""
    stderr = completed.stderr or ""
    if len(stdout.encode("utf-8")) > max_stdout_bytes:
        return "resourceFailure", None, [
            {
                "code": "ADUC-CONF-ADAPTER-RESOURCE-001",
                "message": "Adapter stdout exceeded the conformance output limit.",
            }
        ]
    if len(stderr.encode("utf-8")) > max_stdout_bytes:
        diagnostics.append(
            {
                "code": "ADUC-CONF-ADAPTER-STDERR-001",
                "message": "Adapter stderr exceeded the advisory conformance output limit.",
            }
        )
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        return "invalidAdapterResponse", None, [
            {
                "code": "ADUC-CONF-ADAPTER-JSON-001",
                "message": "Adapter response is not valid JSON.",
            }
        ]
    if not isinstance(payload, dict):
        return "invalidAdapterResponse", None, [
            {
                "code": "ADUC-CONF-ADAPTER-SHAPE-001",
                "message": "Adapter response must be a JSON object.",
            }
        ]
    payload.setdefault("processExitCode", completed.returncode)
    return "pass", payload, diagnostics


def validate_adapter_response(payload: dict[str, Any] | None, operation: str) -> list[dict[str, str]]:
    if not isinstance(payload, dict):
        return [{"code": "ADUC-CONF-ADAPTER-SHAPE-001", "message": "Adapter response is missing."}]
    diagnostics: list[dict[str, str]] = []
    if payload.get("adapterProtocol") != FULL_CORE_ADAPTER_PROTOCOL:
        diagnostics.append(
            {
                "code": "ADUC-CONF-ADAPTER-PROTOCOL-001",
                "message": "Adapter protocol is missing or unsupported.",
            }
        )
    if payload.get("operation") != operation:
        diagnostics.append(
            {
                "code": "ADUC-CONF-ADAPTER-OPERATION-001",
                "message": "Adapter response operation does not match the request.",
            }
        )
    if not isinstance(payload.get("implementation"), dict):
        diagnostics.append(
            {
                "code": "ADUC-CONF-ADAPTER-IMPLEMENTATION-001",
                "message": "Adapter response must declare an implementation object.",
            }
        )
    if operation != "declareCapabilities":
        if not isinstance(payload.get("report"), dict):
            diagnostics.append(
                {
                    "code": "ADUC-CONF-ADAPTER-REPORT-001",
                    "message": "Adapter operation response must contain a report object.",
                }
            )
        if not isinstance(payload.get("exitCode"), int):
            diagnostics.append(
                {
                    "code": "ADUC-CONF-ADAPTER-EXIT-001",
                    "message": "Adapter operation response must contain an integer exitCode.",
                }
            )
    elif not isinstance(payload.get("capabilities"), dict):
        diagnostics.append(
            {
                "code": "ADUC-CONF-ADAPTER-CAPABILITIES-001",
                "message": "Adapter declaration must contain capabilities.",
            }
        )
    return diagnostics


def declared_capability(declaration: dict[str, Any] | None, capability: str) -> bool:
    if not isinstance(declaration, dict):
        return False
    capabilities = declaration.get("capabilities")
    return isinstance(capabilities, dict) and capabilities.get(capability) is True


def expected_matches(case: dict[str, Any], payload: dict[str, Any]) -> tuple[bool, list[dict[str, str]], dict[str, Any]]:
    expected = case.get("expected", {}) if isinstance(case.get("expected"), dict) else {}
    report = payload.get("report", {}) if isinstance(payload.get("report"), dict) else {}
    actual = {
        "exitCode": payload.get("exitCode"),
        "outcome": report.get("outcome"),
    }
    diagnostics: list[dict[str, str]] = []

    if "exitCode" in expected and payload.get("exitCode") != expected["exitCode"]:
        diagnostics.append({"code": "ADUC-CONF-EXPECTED-EXIT-001", "message": "Adapter exit code differed from expected."})
    if "outcome" in expected and report.get("outcome") != expected["outcome"]:
        diagnostics.append({"code": "ADUC-CONF-EXPECTED-OUTCOME-001", "message": "Report outcome differed from expected."})

    operation = case.get("operation")
    if operation == "validate":
        actual["valid"] = report.get("valid")
        if "valid" in expected and report.get("valid") is not expected["valid"]:
            diagnostics.append({"code": "ADUC-CONF-EXPECTED-VALID-001", "message": "Validation validity differed from expected."})
        expected_codes = set(expected.get("diagnosticCodes", []))
        actual_codes = {
            item.get("code")
            for item in report.get("diagnostics", [])
            if isinstance(item, dict)
        }
        actual["diagnosticCodes"] = sorted(code for code in actual_codes if isinstance(code, str))
        missing_codes = sorted(expected_codes - actual_codes)
        if missing_codes:
            diagnostics.append({"code": "ADUC-CONF-EXPECTED-DIAGNOSTIC-001", "message": "Missing expected diagnostic codes: " + ", ".join(missing_codes)})
        profile_statuses = {
            item.get("status")
            for item in report.get("profileEvaluations", [])
            if isinstance(item, dict)
        }
        actual["profileStatuses"] = sorted(status for status in profile_statuses if isinstance(status, str))
    elif operation == "compare":
        actual["overall"] = report.get("overall")
        actual["overallAssessment"] = report.get("overallAssessment")
        if "overall" in expected and report.get("overall") != expected["overall"]:
            diagnostics.append({"code": "ADUC-CONF-EXPECTED-OVERALL-001", "message": "Comparison overall differed from expected."})
        if "overallAssessment" in expected and report.get("overallAssessment") != expected["overallAssessment"]:
            diagnostics.append({"code": "ADUC-CONF-EXPECTED-ASSESSMENT-001", "message": "Comparison assessment differed from expected."})
        expected_codes = set(expected.get("changeCodes", []))
        actual_codes = {
            item.get("code")
            for item in report.get("changes", [])
            if isinstance(item, dict)
        }
        actual["changeCodes"] = sorted(code for code in actual_codes if isinstance(code, str))
        missing_codes = sorted(expected_codes - actual_codes)
        if missing_codes:
            diagnostics.append({"code": "ADUC-CONF-EXPECTED-CHANGE-001", "message": "Missing expected change codes: " + ", ".join(missing_codes)})
        assessments = {
            item.get("assessment")
            for item in report.get("changes", [])
            if isinstance(item, dict)
        }
        if report.get("overallAssessment"):
            assessments.add(report.get("overallAssessment"))
        actual["assessments"] = sorted(value for value in assessments if isinstance(value, str))
        missing_assessments = sorted(set(expected.get("assessments", [])) - assessments)
        if missing_assessments:
            diagnostics.append({"code": "ADUC-CONF-EXPECTED-ASSESSMENT-002", "message": "Missing expected assessments: " + ", ".join(missing_assessments)})
    elif operation == "format":
        actual["formatted"] = report.get("formatted")
        actual["sha256"] = payload.get("formattedSha256")
        if "formatted" in expected and report.get("formatted") is not expected["formatted"]:
            diagnostics.append({"code": "ADUC-CONF-EXPECTED-FORMATTED-001", "message": "Formatter result differed from expected."})

    preserved = set(expected.get("preserveOutcomes", []))
    if preserved:
        visible = set()
        visible.update(str(value) for value in actual.values() if isinstance(value, str))
        if "formattedRequiresHumanReview" in visible:
            visible.add("requiresHumanReview")
        for key in ("profileStatuses", "assessments"):
            visible.update(str(value) for value in actual.get(key, []))
        if not preserved <= visible:
            diagnostics.append({"code": "ADUC-CONF-EXPECTED-PRESERVE-001", "message": "Expected review or safety outcome was not preserved."})

    return not diagnostics, diagnostics, actual


def run_full_core_case(
    suite_dir: Path,
    case: dict[str, Any],
    adapter_command: list[str],
    declaration: dict[str, Any] | None,
    *,
    timeout_seconds: float,
    max_stdout_bytes: int,
) -> dict[str, Any]:
    operation = str(case["operation"])
    capability = str(case.get("requiredCapability", operation))
    base_result = {
        "id": case["id"],
        "version": case.get("version"),
        "operation": operation,
        "class": case.get("class"),
        "requiredCapability": capability,
        "result": "fail",
        "expected": case.get("expected", {}),
        "actual": {},
        "diagnostics": [],
    }
    if not declared_capability(declaration, capability):
        base_result["result"] = "unsupported"
        base_result["diagnostics"] = [
            {
                "code": "ADUC-CONF-CAPABILITY-UNSUPPORTED",
                "message": f"Adapter did not declare required capability {capability!r}.",
            }
        ]
        return base_result

    inputs = case.get("inputs", {}) if isinstance(case.get("inputs"), dict) else {}
    args: list[str] = []
    if operation == "validate":
        args = [str((suite_dir / str(inputs["contract"])).resolve())]
    elif operation == "compare":
        args = [
            str((suite_dir / str(inputs["left"])).resolve()),
            str((suite_dir / str(inputs["right"])).resolve()),
        ]
    elif operation == "format":
        args = [str((suite_dir / str(inputs["contract"])).resolve())]
    else:
        base_result["result"] = "fail"
        base_result["diagnostics"] = [{"code": "ADUC-CONF-MANIFEST-OPERATION-001", "message": "Unsupported case operation."}]
        return base_result

    status, payload, diagnostics = invoke_full_core_adapter(
        adapter_command,
        operation,
        args,
        timeout_seconds=timeout_seconds,
        max_stdout_bytes=max_stdout_bytes,
    )
    if status != "pass":
        base_result["result"] = status
        base_result["diagnostics"] = diagnostics
        return base_result

    response_diagnostics = validate_adapter_response(payload, operation)
    if response_diagnostics:
        base_result["result"] = "invalidAdapterResponse"
        base_result["diagnostics"] = response_diagnostics
        return base_result

    assert payload is not None
    if payload.get("status") == "unsupported":
        base_result["result"] = "unsupported"
        base_result["actual"] = {"status": "unsupported"}
        return base_result

    matched, expected_diagnostics, actual = expected_matches(case, payload)
    base_result["actual"] = actual
    base_result["diagnostics"] = expected_diagnostics
    base_result["result"] = "pass" if matched else "fail"
    return base_result


def summarize_full_core_cases(cases: list[dict[str, Any]]) -> dict[str, int]:
    summary = {name: 0 for name in FULL_CORE_RESULT_ORDER}
    for case in cases:
        result = str(case.get("result"))
        summary[result] = summary.get(result, 0) + 1
    summary["total"] = len(cases)
    return summary


def implementation_kind(declaration: dict[str, Any] | None) -> str:
    implementation = declaration.get("implementation", {}) if isinstance(declaration, dict) else {}
    kind = implementation.get("kind") if isinstance(implementation, dict) else None
    return str(kind or "unknown")


def has_independence_attestation(declaration: dict[str, Any] | None) -> bool:
    if not isinstance(declaration, dict):
        return False
    attestation = declaration.get("independenceAttestation")
    return (
        isinstance(attestation, dict)
        and attestation.get("genuineSeparateImplementation") is True
        and isinstance(attestation.get("scope"), str)
        and bool(attestation.get("scope"))
    )


def run_full_core_suite(
    suite_dir: Path,
    adapter_command: list[str],
    *,
    evidence_mode: str,
) -> dict[str, Any]:
    manifest = load_full_core_suite(suite_dir)
    timeout_seconds, max_stdout_bytes = adapter_resource_limits(manifest)
    declaration_status, declaration, declaration_diagnostics = invoke_full_core_adapter(
        adapter_command,
        "declareCapabilities",
        [],
        timeout_seconds=timeout_seconds,
        max_stdout_bytes=max_stdout_bytes,
    )
    declaration_errors = (
        declaration_diagnostics
        if declaration_status != "pass"
        else validate_adapter_response(declaration, "declareCapabilities")
    )
    if declaration_status != "pass" or declaration_errors:
        cases = [
            {
                "id": case["id"],
                "version": case.get("version"),
                "operation": case.get("operation"),
                "class": case.get("class"),
                "requiredCapability": case.get("requiredCapability"),
                "result": declaration_status if declaration_status != "pass" else "invalidAdapterResponse",
                "expected": case.get("expected", {}),
                "actual": {},
                "diagnostics": declaration_errors,
            }
            for case in manifest["cases"]
        ]
        declaration = declaration if isinstance(declaration, dict) else None
    else:
        cases = [
            run_full_core_case(
                suite_dir,
                case,
                adapter_command,
                declaration,
                timeout_seconds=timeout_seconds,
                max_stdout_bytes=max_stdout_bytes,
            )
            for case in manifest["cases"]
        ]

    summary = summarize_full_core_cases(cases)
    kind = implementation_kind(declaration)
    independent = (
        evidence_mode == "independent"
        and kind == "external"
        and has_independence_attestation(declaration)
        and summary.get("fail", 0) == 0
        and summary.get("invalidAdapterResponse", 0) == 0
        and summary.get("timeout", 0) == 0
        and summary.get("resourceFailure", 0) == 0
    )
    report = {
        "reportVersion": FULL_CORE_REPORT_VERSION,
        "protocol": "urn:aduc:full-core-conformance-report:0.1",
        "suite": {
            "id": manifest.get("suiteId"),
            "version": manifest.get("suiteVersion"),
            "manifestDigest": sha256_json(manifest),
        },
        "adapterProtocol": FULL_CORE_ADAPTER_PROTOCOL,
        "implementationDeclaration": declaration or {},
        "claimedConformanceClasses": (
            declaration.get("capabilities", {}).get("classes", [])
            if isinstance(declaration, dict) and isinstance(declaration.get("capabilities"), dict)
            else []
        ),
        "evidence": {
            "mode": evidence_mode,
            "implementationKind": kind,
            "independenceAttested": has_independence_attestation(declaration),
            "selfConformance": kind in {"reference", "self"},
            "independentConformance": independent,
            "claimBoundary": (
                "Reference or self runs are implementation self-conformance only."
                if kind in {"reference", "self"}
                else "Independent conformance requires a genuinely separate implementation and passing frozen suite evidence."
            ),
        },
        "summary": summary,
        "cases": sorted(
            cases,
            key=lambda item: (
                FULL_CORE_RESULT_ORDER.get(str(item.get("result")), 99),
                str(item.get("operation")),
                str(item.get("id")),
            ),
        ),
    }
    return report


def render_full_core_text(report: dict[str, Any]) -> str:
    suite = report.get("suite", {})
    evidence = report.get("evidence", {})
    summary = report.get("summary", {})
    lines = [
        f"ADUC FULL-CORE CONFORMANCE {suite.get('id')} {suite.get('version')}",
        f"Mode: {evidence.get('mode')} independent={str(evidence.get('independentConformance')).lower()}",
        "Summary: "
        + ", ".join(
            f"{key}={summary.get(key, 0)}"
            for key in ("pass", "fail", "unsupported", "invalidAdapterResponse", "timeout", "resourceFailure")
        ),
    ]
    for case in report.get("cases", []):
        lines.append(f"{str(case['result']).upper()} {case['id']} {case['operation']}")
        for diagnostic in case.get("diagnostics", []):
            lines.append(f"  {diagnostic.get('code')}: {diagnostic.get('message')}")
    return "\n".join(lines) + "\n"


def print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    freeze = subparsers.add_parser("freeze")
    freeze.add_argument("package", type=Path)

    verify = subparsers.add_parser("verify-package")
    verify.add_argument("package", type=Path)

    validate = subparsers.add_parser("validate-result")
    validate.add_argument("result", type=Path)
    validate.add_argument("--package", type=Path, required=True)
    validate.add_argument("--schema", type=Path, default=DEFAULT_RESULT_SCHEMA)

    evaluate_parser = subparsers.add_parser("evaluate")
    evaluate_parser.add_argument("results", nargs="+", type=Path)
    evaluate_parser.add_argument("--package", type=Path, required=True)
    evaluate_parser.add_argument("--expected", type=Path, default=DEFAULT_EXPECTED)
    evaluate_parser.add_argument("--schema", type=Path, default=DEFAULT_RESULT_SCHEMA)
    evaluate_parser.add_argument("--output", type=Path)

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--suite", type=Path, default=DEFAULT_FULL_CORE_SUITE)
    run_parser.add_argument(
        "--evidence-mode",
        choices=("self", "independent"),
        default="self",
    )
    run_parser.add_argument("--format", choices=("json", "text"), default="text")
    run_parser.add_argument("--output", type=Path)
    run_parser.add_argument(
        "--adapter",
        nargs="+",
        required=True,
        help="Adapter command as an argv list. Keep this option last.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "run":
            report = run_full_core_suite(
                args.suite,
                args.adapter,
                evidence_mode=args.evidence_mode,
            )
            if args.format == "json":
                text = stable_json_bytes(report).decode("utf-8")
            else:
                text = render_full_core_text(report)
            if args.output:
                args.output.write_text(text, encoding="utf-8")
            else:
                sys.stdout.write(text)
            summary = report.get("summary", {})
            blocking = sum(
                int(summary.get(key, 0))
                for key in ("fail", "invalidAdapterResponse", "timeout", "resourceFailure")
            )
            unsupported = int(summary.get("unsupported", 0))
            return EXIT_PASS if blocking == 0 and unsupported == 0 else EXIT_FAIL

        if args.command == "freeze":
            report = freeze_package(args.package)
            print_json(report)
            return EXIT_PASS

        package_report = verify_package(args.package)
        if args.command == "verify-package":
            print_json(package_report)
            return EXIT_PASS if package_report["valid"] else EXIT_FAIL

        if not package_report["valid"]:
            print_json(package_report)
            return EXIT_FAIL

        schema = load_json(args.schema)
        if args.command == "validate-result":
            result = load_json(args.result)
            report = validate_result(
                result,
                schema,
                package_digest=str(package_report["packageDigest"]),
                result_path=args.result,
            )
            print_json(report)
            return EXIT_PASS if report["valid"] else EXIT_FAIL

        expected = load_json(args.expected)
        result_items = [(path, load_json(path)) for path in args.results]
        report = evaluate(
            result_items,
            package_report=package_report,
            schema=schema,
            expected=expected,
        )
        text = json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(text, encoding="utf-8")
        sys.stdout.write(text)
        all_results_valid = all(run["valid"] for run in report["runs"])
        return EXIT_PASS if all_results_valid else EXIT_FAIL

    except (OSError, json.JSONDecodeError, ValueError) as error:
        print_json({"valid": False, "error": str(error)})
        return EXIT_INPUT

    return EXIT_INPUT


if __name__ == "__main__":
    sys.exit(main())
