from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = ROOT / "tools" / "aduc_time.py"
EXAMPLES = ROOT / "examples" / "time"

spec = importlib.util.spec_from_file_location("aduc_time", TOOL_PATH)
assert spec and spec.loader
aduc_time = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aduc_time)


class TemporalProfileTests(unittest.TestCase):
    def test_reference_cases_pass(self) -> None:
        failures, reports = aduc_time.evaluate_case_file(EXAMPLES / "reference-cases.json")
        self.assertEqual(failures, 0, reports)
        self.assertEqual(len(reports), 9)

    def test_invalid_cases_are_rejected_for_declared_reasons(self) -> None:
        failures, reports = aduc_time.evaluate_case_file(EXAMPLES / "invalid-cases.json")
        self.assertEqual(failures, 0, reports)
        self.assertEqual(len(reports), 15)

    def test_reference_local_time_resolves_to_utc(self) -> None:
        document = json.loads((EXAMPLES / "reference-cases.json").read_text(encoding="utf-8"))
        case = dict(next(item for item in document["cases"] if item["caseId"] == "french-local-resolves-to-utc"))
        case["timezoneRegistry"] = document["timezoneRegistry"]
        result = aduc_time.evaluate_case(case)
        self.assertTrue(result["valid"])
        self.assertEqual(result["result"]["instantUtc"], "2026-07-13T12:00:00Z")
        self.assertEqual(result["result"]["utcOffset"], "+02:00")

    def test_ambiguous_time_requires_occurrence(self) -> None:
        document = json.loads((EXAMPLES / "invalid-cases.json").read_text(encoding="utf-8"))
        case = dict(next(item for item in document["cases"] if item["caseId"] == "ambiguous-without-occurrence"))
        case["timezoneRegistry"] = document["timezoneRegistry"]
        result = aduc_time.evaluate_case(case)
        self.assertFalse(result["valid"])
        self.assertIn("ADUC-TZ-004", {item["code"] for item in result["errors"]})

    def test_nonexistent_time_is_rejected(self) -> None:
        document = json.loads((EXAMPLES / "invalid-cases.json").read_text(encoding="utf-8"))
        case = dict(next(item for item in document["cases"] if item["caseId"] == "nonexistent-civil-time"))
        case["timezoneRegistry"] = document["timezoneRegistry"]
        result = aduc_time.evaluate_case(case)
        self.assertFalse(result["valid"])
        self.assertIn("ADUC-TZ-005", {item["code"] for item in result["errors"]})

    def test_exact_and_calendar_durations_remain_distinct(self) -> None:
        document = json.loads((EXAMPLES / "reference-cases.json").read_text(encoding="utf-8"))
        exact = dict(next(item for item in document["cases"] if item["caseId"] == "exact-duration-fifteen-minutes"))
        calendar = dict(next(item for item in document["cases"] if item["caseId"] == "calendar-month-preserved"))
        exact["timezoneRegistry"] = document["timezoneRegistry"]
        calendar["timezoneRegistry"] = document["timezoneRegistry"]
        exact_result = aduc_time.evaluate_case(exact)
        calendar_result = aduc_time.evaluate_case(calendar)
        self.assertEqual(exact_result["result"]["exactSeconds"], 900)
        self.assertEqual(calendar_result["result"]["conversionStatus"], "contextRequired")

    def test_cli_passes_both_case_files(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(TOOL_PATH),
                str(EXAMPLES / "reference-cases.json"),
                str(EXAMPLES / "invalid-cases.json"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("24 passed; 0 failed", completed.stdout)


if __name__ == "__main__":
    unittest.main()
