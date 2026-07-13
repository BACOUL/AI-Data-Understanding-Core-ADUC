from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "aduc_compare.py"
SCHEMA_PATH = ROOT / "schema" / "aduc-mapping-profile.schema.json"

spec = importlib.util.spec_from_file_location("aduc_compare", MODULE_PATH)
assert spec and spec.loader
aduc_compare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aduc_compare)

EXACT = "http://www.w3.org/2004/02/skos/core#exactMatch"
CLOSE = "http://www.w3.org/2004/02/skos/core#closeMatch"


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def make_profile(
    profile_id: str,
    local_reference: str,
    target: str,
    *,
    status: str = "reviewed",
    relation: str = EXACT,
    assertion_id: str = "urn:aduc:assertion:one",
    asserted_by: str = "urn:person:reviewer",
) -> dict:
    assertion = {
        "id": assertion_id,
        "localReference": local_reference,
        "semanticTarget": target,
        "mappingRelation": relation,
        "status": status,
        "assertedBy": asserted_by,
        "assertedAt": "2026-07-13T12:00:00Z",
    }
    if status == "inferred":
        assertion.update(
            {
                "confidence": 0.8,
                "confidenceMethod": "urn:method:test",
                "evidence": ["urn:evidence:test"],
            }
        )
    elif status == "contested":
        assertion["evidence"] = ["urn:evidence:challenge"]

    suffix = profile_id.rsplit(":", 1)[-1]
    return {
        "@context": "https://example.org/aduc/context/0.1",
        "id": profile_id,
        "conformsTo": "urn:aduc:profile:0.1",
        "describes": f"https://example.org/schema/{suffix}",
        "validFor": {
            "source": f"https://example.org/source/{suffix}",
            "version": "1",
        },
        "referenceScheme": "json-pointer",
        "issuedAt": "2026-07-13T12:05:00Z",
        "assertions": [assertion],
    }


class ComparatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = load_schema()
        self.target = "https://example.org/quantity/MotorTemperature"

    def compare(self, profile_a: dict, profile_b: dict) -> dict:
        return aduc_compare.compare_profiles(
            profile_a,
            profile_b,
            self.schema,
            path_a="a.json",
            path_b="b.json",
            trusted_authorities_b={"urn:org:publisher"},
        )

    def test_different_local_names_are_comparable_from_shared_target(self) -> None:
        profile_a = make_profile(
            "urn:aduc:profile:a",
            "/properties/temp_moteur",
            self.target,
        )
        profile_b = make_profile(
            "urn:aduc:profile:b",
            "/properties/motor_temp",
            self.target,
            status="canonical",
            assertion_id="urn:aduc:assertion:two",
            asserted_by="urn:org:publisher",
        )
        report = self.compare(profile_a, profile_b)
        self.assertTrue(report["valid"])
        self.assertEqual(report["summary"]["comparable"], 1)
        self.assertEqual(report["matches"][0]["classification"], "comparable")
        self.assertEqual(
            report["matches"][0]["profileA"]["localReference"],
            "/properties/temp_moteur",
        )
        self.assertEqual(
            report["matches"][0]["profileB"]["localReference"],
            "/properties/motor_temp",
        )

    def test_close_match_remains_candidate(self) -> None:
        profile_a = make_profile(
            "urn:aduc:profile:a",
            "/properties/a",
            self.target,
            relation=CLOSE,
        )
        profile_b = make_profile(
            "urn:aduc:profile:b",
            "/properties/b",
            self.target,
            assertion_id="urn:aduc:assertion:two",
        )
        report = self.compare(profile_a, profile_b)
        self.assertEqual(report["matches"][0]["classification"], "candidate")
        self.assertIn("not skos:exactMatch", report["matches"][0]["reasons"][0])

    def test_inferred_exact_match_remains_candidate(self) -> None:
        profile_a = make_profile(
            "urn:aduc:profile:a",
            "/properties/a",
            self.target,
            status="inferred",
        )
        profile_b = make_profile(
            "urn:aduc:profile:b",
            "/properties/b",
            self.target,
            assertion_id="urn:aduc:assertion:two",
        )
        report = self.compare(profile_a, profile_b)
        self.assertEqual(report["matches"][0]["classification"], "candidate")
        self.assertIn("inferred", report["matches"][0]["reasons"][0])

    def test_contested_mapping_blocks_comparison(self) -> None:
        profile_a = make_profile(
            "urn:aduc:profile:a",
            "/properties/a",
            self.target,
            status="contested",
        )
        profile_b = make_profile(
            "urn:aduc:profile:b",
            "/properties/b",
            self.target,
            assertion_id="urn:aduc:assertion:two",
        )
        report = self.compare(profile_a, profile_b)
        self.assertEqual(report["summary"]["blocked"], 1)
        self.assertEqual(report["matches"][0]["classification"], "blocked")

    def test_same_local_name_with_different_targets_is_not_matched(self) -> None:
        profile_a = make_profile(
            "urn:aduc:profile:a",
            "/properties/temperature",
            "https://example.org/quantity/AirTemperature",
        )
        profile_b = make_profile(
            "urn:aduc:profile:b",
            "/properties/temperature",
            "https://example.org/quantity/ColorTemperature",
            assertion_id="urn:aduc:assertion:two",
        )
        report = self.compare(profile_a, profile_b)
        self.assertEqual(report["matches"], [])
        self.assertEqual(report["summary"]["unmappedA"], 1)
        self.assertEqual(report["summary"]["unmappedB"], 1)

    def test_missing_dimensions_are_not_evaluated(self) -> None:
        profile_a = make_profile(
            "urn:aduc:profile:a",
            "/properties/a",
            self.target,
        )
        profile_b = make_profile(
            "urn:aduc:profile:b",
            "/properties/b",
            self.target,
            assertion_id="urn:aduc:assertion:two",
        )
        report = self.compare(profile_a, profile_b)
        self.assertEqual(
            {value["status"] for value in report["dimensions"].values()},
            {"notEvaluated"},
        )

    def test_json_serialization_is_deterministic(self) -> None:
        profile_a = make_profile(
            "urn:aduc:profile:a",
            "/properties/a",
            self.target,
        )
        second_a = deepcopy(profile_a["assertions"][0])
        second_a["id"] = "urn:aduc:assertion:zero"
        second_a["localReference"] = "/properties/zero"
        profile_a["assertions"].insert(0, second_a)

        profile_b = make_profile(
            "urn:aduc:profile:b",
            "/properties/b",
            self.target,
            assertion_id="urn:aduc:assertion:two",
        )
        first = self.compare(profile_a, profile_b)
        profile_a["assertions"].reverse()
        second = self.compare(profile_a, profile_b)
        self.assertEqual(
            aduc_compare.serialize_json(first),
            aduc_compare.serialize_json(second),
        )

    def test_invalid_profile_blocks_comparison(self) -> None:
        profile_a = make_profile(
            "urn:aduc:profile:a",
            "/properties/a",
            self.target,
            status="inferred",
        )
        profile_a["assertions"][0].pop("confidence")
        profile_b = make_profile(
            "urn:aduc:profile:b",
            "/properties/b",
            self.target,
            assertion_id="urn:aduc:assertion:two",
        )
        report = self.compare(profile_a, profile_b)
        self.assertFalse(report["valid"])
        self.assertGreater(report["profileA"]["validation"]["summary"]["errors"], 0)

    def test_cli_exit_codes_and_json_output(self) -> None:
        profile_a = make_profile(
            "urn:aduc:profile:a",
            "/properties/temp_moteur",
            self.target,
        )
        profile_b = make_profile(
            "urn:aduc:profile:b",
            "/properties/motor_temp",
            self.target,
            status="canonical",
            assertion_id="urn:aduc:assertion:two",
            asserted_by="urn:org:publisher",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            path_a = temp / "a.json"
            path_b = temp / "b.json"
            broken = temp / "broken.json"
            path_a.write_text(json.dumps(profile_a), encoding="utf-8")
            path_b.write_text(json.dumps(profile_b), encoding="utf-8")
            broken.write_text("{", encoding="utf-8")

            valid_run = subprocess.run(
                [
                    sys.executable,
                    str(MODULE_PATH),
                    str(path_a),
                    str(path_b),
                    "--format",
                    "json",
                    "--trusted-authority-b",
                    "urn:org:publisher",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(valid_run.returncode, 0, valid_run.stderr)
            self.assertEqual(
                json.loads(valid_run.stdout)["summary"]["comparable"],
                1,
            )

            invalid_profile = deepcopy(profile_a)
            invalid_profile["assertions"][0]["status"] = "inferred"
            path_a.write_text(json.dumps(invalid_profile), encoding="utf-8")
            invalid_run = subprocess.run(
                [sys.executable, str(MODULE_PATH), str(path_a), str(path_b)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(invalid_run.returncode, 1)

            input_run = subprocess.run(
                [sys.executable, str(MODULE_PATH), str(broken), str(path_b)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(input_run.returncode, 2)


if __name__ == "__main__":
    unittest.main()
