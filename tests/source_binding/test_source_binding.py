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
MODULE_PATH = ROOT / "tools" / "aduc_source_binding.py"
EXAMPLES = ROOT / "examples" / "source-description"
VALID_CASES = EXAMPLES / "reference-cases.json"
INVALID_CASES = EXAMPLES / "invalid-cases.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


source_binding = load_module("aduc_source_binding", MODULE_PATH)


class SourceBindingTests(unittest.TestCase):
    def test_reference_cases_pass(self) -> None:
        report = source_binding.evaluate_cases(VALID_CASES)
        self.assertTrue(report["valid"], report)
        self.assertEqual(len(report["results"]), 3)
        self.assertTrue(all(item["valid"] for item in report["results"]))

    def test_required_counterexamples_are_rejected(self) -> None:
        report = source_binding.evaluate_cases(INVALID_CASES)
        self.assertTrue(report["valid"], report)
        self.assertEqual(len(report["results"]), 10)
        self.assertTrue(all(not item["valid"] for item in report["results"]))
        self.assertTrue(all(item["matchesExpectation"] for item in report["results"]))

    def test_resource_tampering_is_detected(self) -> None:
        document = json.loads(VALID_CASES.read_text(encoding="utf-8"))
        case = deepcopy(document["cases"][0])
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            json_dir = temp_root / "json"
            shutil.copytree(EXAMPLES / "json", json_dir)
            with (json_dir / "river-data.json").open("a", encoding="utf-8") as handle:
                handle.write(" ")
            report = source_binding.evaluate_binding(case["binding"], json_dir)
        codes = {item["code"] for item in report["errors"]}
        self.assertFalse(report["valid"])
        self.assertIn("ADUC-BIND-001", codes)

    def test_json_pointer_escape_order_matches_rfc6901(self) -> None:
        document = {"a/b": {"~key": 42}}
        value = source_binding.resolve_json_pointer(document, "/a~1b/~0key")
        self.assertEqual(value, 42)
        with self.assertRaises(KeyError):
            source_binding.resolve_json_pointer(document, "/missing")

    def test_canonical_fixture_digest_is_key_order_independent(self) -> None:
        left = {"b": "value", "a": {"z": True, "x": 1}}
        right = {"a": {"x": 1, "z": True}, "b": "value"}
        self.assertEqual(
            source_binding.sha256_bytes(source_binding.canonical_json_bytes(left)),
            source_binding.sha256_bytes(source_binding.canonical_json_bytes(right)),
        )

    def test_path_escape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.assertIsNone(source_binding.safe_local_path(root, "../outside.json"))

    def test_cli_accepts_both_official_case_files(self) -> None:
        run = subprocess.run(
            [
                sys.executable,
                str(MODULE_PATH),
                str(VALID_CASES),
                str(INVALID_CASES),
                "--compact",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(run.returncode, 0, run.stderr or run.stdout)
        report = json.loads(run.stdout)
        self.assertTrue(report["valid"])


if __name__ == "__main__":
    unittest.main()
