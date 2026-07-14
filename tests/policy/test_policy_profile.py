from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "aduc_policy.py"
EXAMPLES = ROOT / "examples" / "policy"
SPEC = importlib.util.spec_from_file_location("aduc_policy", TOOL)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class PolicyProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reference = json.loads((EXAMPLES / "reference-cases.json").read_text(encoding="utf-8"))
        cls.invalid = json.loads((EXAMPLES / "invalid-cases.json").read_text(encoding="utf-8"))
        cls.registry, errors = module.registry(cls.reference["registry"], EXAMPLES)
        assert cls.registry is not None, errors
        cls.by_id = {
            case["id"]: module.materialize(cls.reference, case)
            for case in cls.reference["cases"]
        }
        cls.invalid_by_id = {
            case["id"]: module.patch(cls.by_id[case["base"]], case["patch"])
            for case in cls.invalid["cases"]
        }

    def test_reference_and_invalid_suites(self) -> None:
        result = module.run(EXAMPLES / "reference-cases.json", EXAMPLES / "invalid-cases.json")
        self.assertTrue(result["ok"], result["failures"])
        self.assertEqual(result["referenceAccepted"], 20)
        self.assertEqual(result["invalidRejected"], 32)

    def test_permission_and_prohibition_precedence(self) -> None:
        permit = module.evaluate(self.by_id["permit-research"], self.registry)
        deny = module.evaluate(self.by_id["prohibition-overrides"], self.registry)
        self.assertEqual(permit["result"]["outcome"], "permit")
        self.assertEqual(deny["result"]["outcome"], "deny")
        self.assertEqual(deny["result"]["reason"], "prohibition")

    def test_pre_use_duty_requires_bound_evidence(self) -> None:
        satisfied = module.evaluate(self.by_id["pre-duty-satisfied"], self.registry)
        missing = module.evaluate(self.by_id["pre-duty-unsatisfied"], self.registry)
        self.assertEqual(satisfied["result"]["outcome"], "permit")
        self.assertEqual(missing["result"]["outcome"], "deny")
        self.assertEqual(missing["result"]["reason"], "unsatisfiedPreUseDuty")

    def test_post_use_duty_remains_visible(self) -> None:
        result = module.evaluate(self.by_id["post-duty-outstanding"], self.registry)
        self.assertEqual(result["result"]["outcome"], "permit")
        self.assertEqual(result["result"]["outstandingDuties"], ["urn:rule:delete"])

    def test_open_and_closed_policy_modes(self) -> None:
        open_result = module.evaluate(self.by_id["open-unknown"], self.registry)
        closed_result = module.evaluate(self.by_id["closed-default-deny"], self.registry)
        self.assertEqual(open_result["result"]["outcome"], "indeterminate")
        self.assertEqual(closed_result["result"]["outcome"], "deny")

    def test_public_classification_is_not_permission(self) -> None:
        result = module.evaluate(self.by_id["public-is-not-permission"], self.registry)
        self.assertEqual(result["result"]["outcome"], "indeterminate")

    def test_human_only_and_incomplete_policies_require_review(self) -> None:
        cases = [self.by_id[case_id] for case_id in (
            "legal-notice-review",
            "partial-policy-review",
            "inferred-policy-review",
            "contested-policy-review",
            "external-governance-review",
        )]
        cases.extend([
            module.patch(self.by_id["permit-research"], [["set", ["policy", "disclosure"], "redacted"]]),
            module.patch(self.by_id["permit-research"], [["set", ["policy", "life"], "deprecated"]]),
        ])
        for case in cases:
            result = module.evaluate(case, self.registry)
            self.assertEqual(result["result"]["outcome"], "requiresHumanReview")

    def test_target_and_temporal_scope(self) -> None:
        different = module.evaluate(self.by_id["different-target"], self.registry)
        expired = module.evaluate(self.by_id["expired-policy"], self.registry)
        wrong_version = module.evaluate(self.invalid_by_id["request-wrong-version"], self.registry)
        self.assertEqual(different["result"]["outcome"], "notApplicable")
        self.assertEqual(expired["result"]["outcome"], "deny")
        self.assertIn("ADUC-POL-TARGET-002", {item["code"] for item in wrong_version["errors"]})

    def test_named_parties_and_controlled_purposes(self) -> None:
        result = module.evaluate(self.by_id["named-parties-permit"], self.registry)
        local = module.evaluate(self.invalid_by_id["local-assignee"], self.registry)
        free_text = module.evaluate(self.invalid_by_id["free-text-purpose"], self.registry)
        scoped = module.patch(self.by_id["permit-research"], [
            ["set", ["policy", "rules", 0, "spatial"], "urn:place:france"],
            ["set", ["policy", "rules", 0, "environment"], "urn:aduc:environment:research"],
        ])
        wrong_place = module.patch(scoped, [["set", ["request", "spatial"], "urn:place:germany"]])
        wrong_environment = module.patch(scoped, [["set", ["request", "environment"], "urn:aduc:environment:production"]])
        self.assertEqual(result["result"]["outcome"], "permit")
        self.assertEqual(module.evaluate(scoped, self.registry)["result"]["outcome"], "permit")
        self.assertEqual(module.evaluate(wrong_place, self.registry)["result"]["outcome"], "indeterminate")
        self.assertEqual(module.evaluate(wrong_environment, self.registry)["result"]["outcome"], "indeterminate")
        self.assertIn("ADUC-POL-PARTY-001", {item["code"] for item in local["errors"]})
        self.assertIn("ADUC-POL-PURPOSE-001", {item["code"] for item in free_text["errors"]})

    def test_consent_and_composition_require_evidence(self) -> None:
        consent = module.evaluate(self.by_id["consent-evidence-permit"], self.registry)
        missing_consent = module.evaluate(self.invalid_by_id["consent-without-evidence"], self.registry)
        composed = module.evaluate(self.by_id["resolved-composition"], self.registry)
        unresolved = module.evaluate(self.invalid_by_id["unresolved-inheritance"], self.registry)
        self.assertEqual(consent["result"]["outcome"], "permit")
        self.assertIn("ADUC-POL-CLAIM-001", {item["code"] for item in missing_consent["errors"]})
        self.assertEqual(composed["result"]["outcome"], "permit")
        self.assertIn("ADUC-POL-COMPOSE-001", {item["code"] for item in unresolved["errors"]})

    def test_export_is_deterministic(self) -> None:
        first = module.evaluate(self.by_id["deterministic-export"], self.registry)
        second = module.evaluate(self.by_id["deterministic-export"], self.registry)
        self.assertEqual(first["result"]["jsonld"], second["result"]["jsonld"])
        self.assertEqual(first["result"]["policies"], 1)
        self.assertEqual(first["result"]["rules"], 2)

    def test_unsafe_shortcuts_are_rejected(self) -> None:
        expected = {
            "inferred-without-confidence": "ADUC-POL-AUTH-002",
            "legal-notice-made-executable": "ADUC-POL-LEGAL-001",
            "duty-satisfied-without-evidence": "ADUC-POL-DUTY-002",
            "compliance-without-assessment": "ADUC-POL-CLAIM-001",
        }
        for case_id, code in expected.items():
            with self.subTest(case_id=case_id):
                result = module.evaluate(self.invalid_by_id[case_id], self.registry)
                self.assertIn(code, {item["code"] for item in result["errors"]})

    def test_cli(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(TOOL),
                str(EXAMPLES / "reference-cases.json"),
                str(EXAMPLES / "invalid-cases.json"),
                "--format",
                "json",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertTrue(result["ok"])
        self.assertEqual(result["referenceAccepted"], 20)
        self.assertEqual(result["invalidRejected"], 32)


if __name__ == "__main__":
    unittest.main()
