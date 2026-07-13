#!/usr/bin/env python3
"""Freeze, verify, validate, and evaluate ADUC multi-model conformance runs."""

from __future__ import annotations

import argparse
import hashlib
import json
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

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
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
