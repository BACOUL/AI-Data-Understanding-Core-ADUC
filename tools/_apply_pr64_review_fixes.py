from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMATTER = ROOT / "tools" / "aduc_core_format.py"
TESTS = ROOT / "tests" / "core_formatter" / "test_aduc_core_formatter.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


formatter = FORMATTER.read_text(encoding="utf-8")
formatter = replace_once(
    formatter,
    '''    except RecursionError as exc:\n        raise FormatterError(\n            "ADUC-FMT-INPUT-005",\n            f"Input exceeds depth {MAX_JSON_DEPTH}.",\n            usage=True,\n        ) from exc\n''',
    '''    except ValueError as exc:\n        raise FormatterError(\n            "ADUC-FMT-INPUT-006",\n            "JSON numeric value exceeds the supported parser limit.",\n            usage=True,\n        ) from exc\n    except RecursionError as exc:\n        raise FormatterError(\n            "ADUC-FMT-INPUT-005",\n            f"Input exceeds depth {MAX_JSON_DEPTH}.",\n            usage=True,\n        ) from exc\n''',
    "oversized-number handling",
)
formatter = replace_once(
    formatter,
    '''    except FormatterError as exc:\n        report["outcome"] = "usageError" if exc.usage else "blocked"\n        report["diagnostics"].append(diagnostic(exc.code, exc.message, path=exc.path))\n        return report, EXIT_USAGE if exc.usage else EXIT_BLOCKED\n''',
    '''    except FormatterError as exc:\n        if report.get("formatted"):\n            report["formatted"] = False\n            report["bytes"]["output"] = None\n            report["bytes"]["sha256"] = None\n        report["outcome"] = "usageError" if exc.usage else "blocked"\n        report["diagnostics"].append(diagnostic(exc.code, exc.message, path=exc.path))\n        return report, EXIT_USAGE if exc.usage else EXIT_BLOCKED\n''',
    "failed-write report reset",
)
FORMATTER.write_text(formatter, encoding="utf-8")

tests = TESTS.read_text(encoding="utf-8")
tests = replace_once(
    tests,
    '''            self.assertEqual(exit_code, formatter.EXIT_USAGE)\n            self.assertFalse(output.exists())\n            self.assertEqual(report["diagnostics"][0]["code"], "ADUC-FMT-OUTPUT-002")\n\n    def test_existing_output_requires_explicit_force(self) -> None:\n''',
    '''            self.assertEqual(exit_code, formatter.EXIT_USAGE)\n            self.assertFalse(report["formatted"])\n            self.assertIsNone(report["bytes"]["output"])\n            self.assertIsNone(report["bytes"]["sha256"])\n            self.assertFalse(output.exists())\n            self.assertEqual(report["diagnostics"][0]["code"], "ADUC-FMT-OUTPUT-002")\n\n    def test_existing_output_requires_explicit_force(self) -> None:\n''',
    "write-failure regression assertions",
)
tests = replace_once(
    tests,
    '''    def test_array_paths_cannot_collide_with_extension_member_names(self) -> None:\n''',
    '''    def test_oversized_integer_is_reported_without_traceback(self) -> None:\n        with tempfile.TemporaryDirectory() as temp:\n            root = Path(temp)\n            document = copy.deepcopy(self.document)\n            payload = document["semantics"]["extensions"]["https://example.org/aduc/ext/hydrology/"]\n            payload["oversizedInteger"] = "OVERSIZED_INTEGER_PLACEHOLDER"\n            source = self.write_unordered(root, document)\n            raw = source.read_text(encoding="utf-8").replace(\n                '"OVERSIZED_INTEGER_PLACEHOLDER"',\n                "1" * 5000,\n            )\n            source.write_text(raw, encoding="utf-8")\n            output = root / "formatted.json"\n\n            report, exit_code = formatter.format_path(source, output)\n\n            self.assertEqual(exit_code, formatter.EXIT_USAGE)\n            self.assertFalse(report["formatted"])\n            self.assertFalse(output.exists())\n            self.assertEqual(report["diagnostics"][0]["code"], "ADUC-FMT-INPUT-006")\n\n    def test_array_paths_cannot_collide_with_extension_member_names(self) -> None:\n''',
    "oversized-integer regression test",
)
TESTS.write_text(tests, encoding="utf-8")
