from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "aduc_conformance.py"
VALIDATOR_PATH = ROOT / "tools" / "aduc_validate.py"
PACKAGE_PATH = ROOT / "examples" / "conformance" / "package"
EXPECTED_PATH = ROOT / "examples" / "conformance" / "expected.json"
RESULT_A_PATH = (
    ROOT / "examples" / "conformance" / "results" / "illustrative-a.normalized.json"
)
RESULT_B_PATH = (
    ROOT / "examples" / "conformance" / "results" / "illustrative-b.normalized.json"
)
RESULT_SCHEMA_PATH = ROOT / "schema" / "model-conformance-result.schema.json"
PROFILE_SCHEMA_PATH = ROOT / "schema" / "aduc-mapping-profile.schema.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


aduc_conformance = load_module("aduc_conformance", MODULE_PATH)
aduc_validate = load_module("aduc_validate_for_conformance", VALIDATOR_PATH)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class ConformanceHarnessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.result_schema = load_json(RESULT_SCHEMA_PATH)
        self.profile_schema = load_json(PROFILE_SCHEMA_PATH)
        self.expected = load_json(EXPECTED_PATH)
        self.package_report = aduc_conformance.verify_package(PACKAGE_PATH)
        self.result_a = load_json(RESULT_A_PATH)
        self.result_b = load_json(RESULT_B_PATH)

    def test_committed_package_manifest_verifies(self) -> None:
        self.assertTrue(self.package_report["valid"], self.package_report["errors"])
        self.assertEqual(
            self.package_report["packageDigest"],
            "sha256:de17a4ab6b6f26d961de1e791e256f8e33b51fa2ffc4518d230add6b46a3892f",
        )
        self.assertEqual(len(self.package_report["files"]), 3)

    def test_freeze_is_deterministic_and_tampering_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            package = Path(temp_dir) / "package"
            shutil.copytree(PACKAGE_PATH, package)
            first = aduc_conformance.freeze_package(package)
            second = aduc_conformance.freeze_package(package)
            self.assertEqual(first, second)
            self.assertEqual(first["packageDigest"], self.package_report["packageDigest"])

            with (package / "instructions.md").open("a", encoding="utf-8") as handle:
                handle.write("tampered\n")
            report = aduc_conformance.verify_package(package)
            self.assertFalse(report["valid"])
            self.assertTrue(
                any("instructions.md" in error for error in report["errors"])
            )

    def test_every_embedded_profile_is_valid_aduc(self) -> None:
        cases = load_json(PACKAGE_PATH / "cases.json")["cases"]
        self.assertEqual(len(cases), 6)
        for case in cases:
            for side in ("sourceA", "sourceB"):
                with self.subTest(scenario=case["scenarioId"], side=side):
                    report = aduc_validate.validate_profile(
                        case[side]["profile"], self.profile_schema
                    )
                    self.assertTrue(report["valid"], report["errors"])

    def test_illustrative_results_validate_and_raw_hashes_verify(self) -> None:
        for path, result in (
            (RESULT_A_PATH, self.result_a),
            (RESULT_B_PATH, self.result_b),
        ):
            with self.subTest(result=path.name):
                report = aduc_conformance.validate_result(
                    result,
                    self.result_schema,
                    package_digest=self.package_report["packageDigest"],
                    result_path=path,
                )
                self.assertTrue(report["valid"], report["errors"])
                self.assertTrue(report["rawOutputVerified"])

    def test_illustrative_agreement_never_proves_interoperability(self) -> None:
        report = aduc_conformance.evaluate(
            [(RESULT_A_PATH, self.result_a), (RESULT_B_PATH, self.result_b)],
            package_report=self.package_report,
            schema=self.result_schema,
            expected=self.expected,
        )
        summary = report["summary"]
        self.assertTrue(summary["semanticAgreement"])
        self.assertEqual(summary["expectedPasses"], 2)
        self.assertEqual(summary["qualifyingExternalRuns"], 0)
        self.assertFalse(summary["interoperabilityProven"])

    def test_semantic_disagreement_is_detected(self) -> None:
        disagreeing = deepcopy(self.result_b)
        disagreeing["results"][0]["classification"] = "candidate"
        report = aduc_conformance.evaluate(
            [(RESULT_A_PATH, self.result_a), (RESULT_B_PATH, disagreeing)],
            package_report=self.package_report,
            schema=self.result_schema,
            expected=self.expected,
        )
        self.assertFalse(report["summary"]["semanticAgreement"])
        self.assertEqual(report["summary"]["expectedPasses"], 1)
        self.assertFalse(report["summary"]["interoperabilityProven"])

    def test_two_distinct_external_runs_can_qualify(self) -> None:
        external_a = deepcopy(self.result_a)
        external_b = deepcopy(self.result_b)
        external_a["run"]["kind"] = "external"
        external_b["run"]["kind"] = "external"
        report = aduc_conformance.evaluate(
            [(RESULT_A_PATH, external_a), (RESULT_B_PATH, external_b)],
            package_report=self.package_report,
            schema=self.result_schema,
            expected=self.expected,
        )
        summary = report["summary"]
        self.assertEqual(summary["qualifyingExternalRuns"], 2)
        self.assertEqual(summary["distinctQualifyingProviders"], 2)
        self.assertTrue(summary["interoperabilityProven"])

    def test_duplicate_or_missing_scenarios_fail_validation(self) -> None:
        invalid = deepcopy(self.result_a)
        invalid["results"][1] = deepcopy(invalid["results"][0])
        report = aduc_conformance.validate_result(
            invalid,
            self.result_schema,
            package_digest=self.package_report["packageDigest"],
            result_path=RESULT_A_PATH,
        )
        self.assertFalse(report["valid"])
        self.assertTrue(any("scenario" in error for error in report["errors"]))

    def test_cli_verification_and_evaluation(self) -> None:
        verify_run = subprocess.run(
            [sys.executable, str(MODULE_PATH), "verify-package", str(PACKAGE_PATH)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(verify_run.returncode, 0, verify_run.stderr)
        self.assertTrue(json.loads(verify_run.stdout)["valid"])

        evaluate_run = subprocess.run(
            [
                sys.executable,
                str(MODULE_PATH),
                "evaluate",
                str(RESULT_A_PATH),
                str(RESULT_B_PATH),
                "--package",
                str(PACKAGE_PATH),
                "--expected",
                str(EXPECTED_PATH),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(evaluate_run.returncode, 0, evaluate_run.stderr)
        report = json.loads(evaluate_run.stdout)
        self.assertFalse(report["summary"]["interoperabilityProven"])


if __name__ == "__main__":
    unittest.main()
