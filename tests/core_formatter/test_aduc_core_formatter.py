from __future__ import annotations

import copy
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import aduc_core_format as formatter  # noqa: E402


COMPLETE = ROOT / "examples" / "core" / "complete-model.example.json"


def reverse_objects(value):
    if isinstance(value, dict):
        return {key: reverse_objects(value[key]) for key in reversed(list(value))}
    if isinstance(value, list):
        return [reverse_objects(item) for item in value]
    return value


class CompleteContractFormatterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.document = json.loads(COMPLETE.read_text(encoding="utf-8"))

    def write_unordered(self, directory: Path, document=None) -> Path:
        path = directory / "input.json"
        payload = reverse_objects(document if document is not None else self.document)
        path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        return path

    def test_formats_and_revalidates_complete_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = self.write_unordered(root)
            output = root / "formatted.json"
            report, exit_code = formatter.format_path(source, output)

            self.assertIn(exit_code, {formatter.EXIT_FORMATTED, formatter.EXIT_HUMAN_REVIEW})
            self.assertTrue(report["formatted"])
            self.assertTrue(report["preservation"]["semanticEqual"])
            self.assertTrue(report["preservation"]["arrayOrderPreserved"])
            self.assertTrue(report["outputValidation"]["valid"])
            self.assertTrue(output.exists())

    def test_formatting_is_byte_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = self.write_unordered(root)
            first = root / "first.json"
            second = root / "second.json"

            first_report, first_exit = formatter.format_path(source, first)
            second_report, second_exit = formatter.format_path(first, second)

            self.assertIn(first_exit, {formatter.EXIT_FORMATTED, formatter.EXIT_HUMAN_REVIEW})
            self.assertEqual(first_exit, second_exit)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(first_report["bytes"]["sha256"], second_report["bytes"]["sha256"])

    def test_top_level_and_nested_objects_have_stable_order(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = self.write_unordered(root)
            output = root / "formatted.json"
            formatter.format_path(source, output)
            formatted = output.read_text(encoding="utf-8")

            top_positions = [formatted.index(f'  "{name}":') for name in formatter.TOP_LEVEL_ORDER]
            self.assertEqual(top_positions, sorted(top_positions))
            aduc = json.loads(formatted, object_pairs_hook=list)[0][1]
            keys = [item[0] for item in aduc]
            self.assertEqual(keys, sorted(keys))

    def test_array_order_is_never_changed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            expected = [
                item["id"] for item in self.document["structure"]["records"][0]["fields"]
            ]
            source = self.write_unordered(root)
            output = root / "formatted.json"
            formatter.format_path(source, output)
            actual = [
                item["id"]
                for item in json.loads(output.read_text(encoding="utf-8"))["structure"]["records"][0]["fields"]
            ]
            self.assertEqual(actual, expected)

    def test_duplicate_object_member_is_rejected_before_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "duplicate.json"
            source.write_text(
                '{"aduc":{},"aduc":{},"resource":{},"structure":{}}',
                encoding="utf-8",
            )
            output = root / "formatted.json"
            report, exit_code = formatter.format_path(source, output)

            self.assertEqual(exit_code, formatter.EXIT_USAGE)
            self.assertFalse(output.exists())
            self.assertEqual(report["diagnostics"][0]["code"], "ADUC-FMT-INPUT-002")

    def test_invalid_contract_is_not_repaired_or_written(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "invalid.json"
            source.write_text('{"aduc":{},"resource":{},"structure":{}}', encoding="utf-8")
            output = root / "formatted.json"
            report, exit_code = formatter.format_path(source, output)

            self.assertEqual(exit_code, formatter.EXIT_BLOCKED)
            self.assertFalse(report["formatted"])
            self.assertFalse(output.exists())
            self.assertEqual(report["diagnostics"][0]["code"], "ADUC-FMT-VALIDATION-001")

    def test_human_review_outcome_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            document = copy.deepcopy(self.document)
            document["policy"]["policies"][0]["disclosure"] = "redacted"
            source = self.write_unordered(root, document)
            output = root / "formatted.json"
            report, exit_code = formatter.format_path(source, output)

            self.assertEqual(exit_code, formatter.EXIT_HUMAN_REVIEW)
            self.assertEqual(report["outcome"], "formattedRequiresHumanReview")
            self.assertEqual(report["inputValidation"]["outcome"], "requiresHumanReview")
            self.assertEqual(report["outputValidation"]["outcome"], "requiresHumanReview")

    def test_unicode_numbers_and_extension_payload_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            document = copy.deepcopy(self.document)
            payload = document["semantics"]["extensions"]["https://example.org/aduc/ext/hydrology/"]
            payload.update(
                {
                    "label": "Débit Δ — 東京",
                    "decimalValue": 1.23,
                    "largeValue": 100,
                    "negativeZero": -0.0,
                }
            )
            source = self.write_unordered(root, document)
            raw = source.read_text(encoding="utf-8")
            raw = raw.replace('"decimalValue":1.23', '"decimalValue":1.2300')
            raw = raw.replace('"largeValue":100', '"largeValue":1e2')
            raw = raw.replace('"negativeZero":-0.0', '"negativeZero":-0.000')
            source.write_text(raw, encoding="utf-8")
            output = root / "formatted.json"
            report, exit_code = formatter.format_path(source, output)
            rendered = output.read_text(encoding="utf-8")

            self.assertIn(exit_code, {formatter.EXIT_FORMATTED, formatter.EXIT_HUMAN_REVIEW})
            self.assertTrue(report["preservation"]["semanticEqual"])
            self.assertIn("Débit Δ — 東京", rendered)
            self.assertIn('"decimalValue": 1.23', rendered)
            self.assertIn('"largeValue": 100', rendered)
            self.assertIn('"negativeZero": -0', rendered)

    def test_existing_output_requires_explicit_force(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = self.write_unordered(root)
            output = root / "formatted.json"
            output.write_text("sentinel", encoding="utf-8")
            report, exit_code = formatter.format_path(source, output)

            self.assertEqual(exit_code, formatter.EXIT_USAGE)
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")
            self.assertEqual(report["diagnostics"][0]["code"], "ADUC-FMT-OUTPUT-002")


    def test_frozen_formatter_fixtures(self) -> None:
        fixture_root = ROOT / "examples" / "core" / "formatting"
        suite = json.loads((fixture_root / "cases.json").read_text(encoding="utf-8"))
        for case in suite["cases"]:
            with self.subTest(case=case["id"]), tempfile.TemporaryDirectory() as temp:
                output = Path(temp) / "formatted.json"
                report, exit_code = formatter.format_path(fixture_root / case["input"], output)
                self.assertEqual(report["outcome"], case["expectedOutcome"])
                if "expectedCode" in case:
                    self.assertEqual(exit_code, formatter.EXIT_USAGE)
                    self.assertEqual(report["diagnostics"][0]["code"], case["expectedCode"])
                    self.assertFalse(output.exists())
                else:
                    expected = (fixture_root / case["expectedOutput"]).read_bytes()
                    self.assertEqual(output.read_bytes(), expected)

    def test_cli_emits_stable_json_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = self.write_unordered(root)
            output = root / "formatted.json"
            stream = io.StringIO()
            with redirect_stdout(stream):
                exit_code = formatter.main(
                    [str(source), "--output", str(output), "--report-format", "json"]
                )
            report = json.loads(stream.getvalue())

            self.assertIn(exit_code, {formatter.EXIT_FORMATTED, formatter.EXIT_HUMAN_REVIEW})
            self.assertEqual(report["reportVersion"], formatter.REPORT_VERSION)
            self.assertEqual(report["formatterVersion"], formatter.FORMATTER_VERSION)
            self.assertEqual(report["ordering"]["arrays"], "preserved")
            self.assertEqual(report["bytes"]["sha256"], formatter.hashlib.sha256(output.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
