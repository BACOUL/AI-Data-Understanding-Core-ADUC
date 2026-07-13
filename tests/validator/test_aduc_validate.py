from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "aduc_validate.py"
SCHEMA_PATH = ROOT / "schema" / "aduc-mapping-profile.schema.json"

spec = importlib.util.spec_from_file_location("aduc_validate", MODULE_PATH)
assert spec and spec.loader
aduc_validate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aduc_validate)


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def base_profile() -> dict:
    return {
        "@context": "https://example.org/aduc/context/0.1",
        "id": "urn:aduc:profile:test",
        "conformsTo": "urn:aduc:profile:0.1",
        "describes": "https://data.example.org/croissant/source-v1",
        "validFor": {
            "source": "https://data.example.org/croissant/source",
            "version": "1",
        },
        "referenceScheme": "croissant-field-id",
        "issuedAt": "2026-07-13T12:00:00Z",
        "assertions": [
            {
                "id": "urn:aduc:assertion:a1",
                "localReference": "records/flow",
                "semanticTarget": "https://example.org/concepts/WaterDischarge",
                "mappingRelation": (
                    "http://www.w3.org/2004/02/skos/core#exactMatch"
                ),
                "status": "inferred",
                "confidence": 0.91,
                "confidenceMethod": "urn:method:mapper-v1",
                "assertedBy": "urn:model:mapper:1",
                "assertedAt": "2026-07-13T11:58:00Z",
                "evidence": ["urn:evidence:unit", "urn:evidence:docs"],
            }
        ],
    }


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = load_schema()

    def codes(self, report: dict, key: str = "errors") -> set[str]:
        return {issue["code"] for issue in report[key]}

    def test_valid_inferred_profile(self) -> None:
        report = aduc_validate.validate_profile(base_profile(), self.schema)
        self.assertTrue(report["valid"])
        self.assertEqual(report["summary"], {"errors": 0, "warnings": 0})

    def test_duplicate_assertion_id(self) -> None:
        profile = base_profile()
        duplicate = dict(profile["assertions"][0])
        duplicate["localReference"] = "records/other"
        profile["assertions"].append(duplicate)
        report = aduc_validate.validate_profile(profile, self.schema)
        self.assertIn("ADUC-DOC-001", self.codes(report))

    def test_self_supersedes(self) -> None:
        profile = base_profile()
        assertion = profile["assertions"][0]
        assertion["supersedes"] = assertion["id"]
        report = aduc_validate.validate_profile(profile, self.schema)
        self.assertIn("ADUC-LIFE-001", self.codes(report))

    def test_supersedes_cycle(self) -> None:
        profile = base_profile()
        first = profile["assertions"][0]
        first["id"] = "urn:aduc:assertion:a"
        first["supersedes"] = "urn:aduc:assertion:b"
        second = dict(first)
        second["id"] = "urn:aduc:assertion:b"
        second["supersedes"] = "urn:aduc:assertion:a"
        second["localReference"] = "records/other"
        profile["assertions"].append(second)
        report = aduc_validate.validate_profile(profile, self.schema)
        self.assertIn("ADUC-LIFE-002", self.codes(report))

    def test_canonical_conflict(self) -> None:
        profile = base_profile()
        first = profile["assertions"][0]
        first.update(
            {
                "status": "canonical",
                "assertedBy": "urn:org:publisher",
            }
        )
        first.pop("confidence")
        first.pop("confidenceMethod")
        first.pop("evidence")
        second = dict(first)
        second["id"] = "urn:aduc:assertion:a2"
        second["semanticTarget"] = "https://example.org/concepts/VolumeFlowRate"
        profile["assertions"].append(second)
        report = aduc_validate.validate_profile(
            profile, self.schema, trusted_authorities={"urn:org:publisher"}
        )
        self.assertIn("ADUC-CONFLICT-001", self.codes(report))

    def test_untrusted_canonical_authority_warning(self) -> None:
        profile = base_profile()
        assertion = profile["assertions"][0]
        assertion.update({"status": "canonical", "assertedBy": "urn:org:publisher"})
        assertion.pop("confidence")
        assertion.pop("confidenceMethod")
        assertion.pop("evidence")
        report = aduc_validate.validate_profile(profile, self.schema)
        self.assertTrue(report["valid"])
        self.assertIn("ADUC-TRUST-001", self.codes(report, "warnings"))

        trusted = aduc_validate.validate_profile(
            profile, self.schema, trusted_authorities={"urn:org:publisher"}
        )
        self.assertNotIn("ADUC-TRUST-001", self.codes(trusted, "warnings"))

    def test_schema_error(self) -> None:
        profile = base_profile()
        profile["assertions"][0].pop("confidence")
        report = aduc_validate.validate_profile(profile, self.schema)
        self.assertFalse(report["valid"])
        self.assertIn("ADUC-SCHEMA-001", self.codes(report))

    def test_cli_json_report_and_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            valid_path = temp / "valid.json"
            invalid_path = temp / "invalid.json"
            broken_path = temp / "broken.json"
            valid_path.write_text(json.dumps(base_profile()), encoding="utf-8")
            invalid = base_profile()
            invalid["assertions"][0].pop("confidence")
            invalid_path.write_text(json.dumps(invalid), encoding="utf-8")
            broken_path.write_text("{", encoding="utf-8")

            valid_run = subprocess.run(
                [
                    sys.executable,
                    str(MODULE_PATH),
                    str(valid_path),
                    "--format",
                    "json",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(valid_run.returncode, 0, valid_run.stderr)
            self.assertTrue(json.loads(valid_run.stdout)["valid"])

            invalid_run = subprocess.run(
                [sys.executable, str(MODULE_PATH), str(invalid_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(invalid_run.returncode, 1)

            broken_run = subprocess.run(
                [sys.executable, str(MODULE_PATH), str(broken_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(broken_run.returncode, 2)


if __name__ == "__main__":
    unittest.main()
