from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "aduc_conformance.py"
SUITE = ROOT / "conformance" / "full-core" / "0.1"
REFERENCE_ADAPTER = ROOT / "tools" / "aduc_conformance_reference_adapter.py"
DEMO_ADAPTER = ROOT / "tools" / "aduc_conformance_demo_adapter.py"
ADAPTERS = ROOT / "tests" / "core_conformance" / "adapters"

SPEC = importlib.util.spec_from_file_location("aduc_conformance", TOOL)
assert SPEC and SPEC.loader
aduc_conformance = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(aduc_conformance)


def adapter(path: Path) -> list[str]:
    return [sys.executable, str(path)]


class FullCoreConformanceRunnerTests(unittest.TestCase):
    def test_manifest_is_versioned_valid_and_deterministically_ordered(self) -> None:
        manifest = aduc_conformance.load_full_core_suite(SUITE)
        schema = aduc_conformance.load_json(SUITE / "manifest.schema.json")
        Draft202012Validator(schema).validate(manifest)
        ids = [case["id"] for case in manifest["cases"]]
        self.assertEqual(ids, sorted(ids))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), 12)
        self.assertEqual(
            set(manifest["normativeOutcomesPreserved"]),
            {"unknown", "contested", "prohibited", "requiresHumanReview"},
        )

    def test_reference_adapter_passes_as_self_conformance_only(self) -> None:
        report = aduc_conformance.run_full_core_suite(
            SUITE,
            adapter(REFERENCE_ADAPTER),
            evidence_mode="independent",
        )
        self.assertEqual(report["summary"]["pass"], report["summary"]["total"])
        self.assertEqual(report["summary"]["fail"], 0)
        self.assertTrue(report["evidence"]["selfConformance"])
        self.assertFalse(report["evidence"]["independentConformance"])
        self.assertFalse(report["evidence"]["independenceAttested"])
        observed = set()
        for case in report["cases"]:
            actual = case["actual"]
            observed.update(actual.get("profileStatuses", []))
            observed.update(actual.get("assessments", []))
            if actual.get("overall") == "requiresHumanReview":
                observed.add("requiresHumanReview")
            if actual.get("outcome") == "requiresHumanReview":
                observed.add("requiresHumanReview")
            if actual.get("outcome") == "formattedRequiresHumanReview":
                observed.add("requiresHumanReview")
        self.assertTrue({"unknown", "contested", "prohibited", "requiresHumanReview"}.issubset(observed))

    def test_demo_adapter_uses_same_boundary_without_false_independent_proof(self) -> None:
        report = aduc_conformance.run_full_core_suite(
            SUITE,
            adapter(DEMO_ADAPTER),
            evidence_mode="independent",
        )
        self.assertEqual(report["summary"]["pass"], report["summary"]["total"])
        self.assertEqual(report["implementationDeclaration"]["adapterProtocol"], aduc_conformance.FULL_CORE_ADAPTER_PROTOCOL)
        self.assertEqual(report["evidence"]["implementationKind"], "external")
        self.assertFalse(report["evidence"]["independentConformance"])
        self.assertFalse(report["evidence"]["independenceAttested"])

    def test_reports_are_byte_identical_across_two_runs(self) -> None:
        first = aduc_conformance.run_full_core_suite(SUITE, adapter(REFERENCE_ADAPTER), evidence_mode="self")
        second = aduc_conformance.run_full_core_suite(SUITE, adapter(REFERENCE_ADAPTER), evidence_mode="self")
        self.assertEqual(
            aduc_conformance.stable_json_bytes(first),
            aduc_conformance.stable_json_bytes(second),
        )

    def test_invalid_and_incomplete_adapter_responses_are_rejected(self) -> None:
        for name in ("invalid_json_adapter.py", "incomplete_adapter.py"):
            with self.subTest(adapter=name):
                report = aduc_conformance.run_full_core_suite(
                    SUITE,
                    adapter(ADAPTERS / name),
                    evidence_mode="self",
                )
                self.assertEqual(report["summary"]["invalidAdapterResponse"], report["summary"]["total"])
                codes = {
                    diagnostic["code"]
                    for case in report["cases"]
                    for diagnostic in case["diagnostics"]
                }
                self.assertTrue(
                    {
                        "ADUC-CONF-ADAPTER-JSON-001",
                        "ADUC-CONF-ADAPTER-PROTOCOL-001",
                        "ADUC-CONF-ADAPTER-IMPLEMENTATION-001",
                    }
                    & codes,
                    codes,
                )

    def test_timeout_and_large_output_are_reported_without_tracebacks(self) -> None:
        timeout = aduc_conformance.run_full_core_suite(
            SUITE,
            adapter(ADAPTERS / "slow_adapter.py"),
            evidence_mode="self",
        )
        self.assertEqual(timeout["summary"]["timeout"], timeout["summary"]["total"])
        self.assertNotIn("Traceback", json.dumps(timeout))

        large = aduc_conformance.run_full_core_suite(
            SUITE,
            adapter(ADAPTERS / "verbose_adapter.py"),
            evidence_mode="self",
        )
        self.assertEqual(large["summary"]["resourceFailure"], large["summary"]["total"])
        self.assertNotIn("Traceback", json.dumps(large))

    def test_unsupported_capabilities_are_reported_per_case(self) -> None:
        report = aduc_conformance.run_full_core_suite(
            SUITE,
            adapter(ADAPTERS / "unsupported_adapter.py"),
            evidence_mode="self",
        )
        self.assertEqual(report["summary"]["unsupported"], report["summary"]["total"])
        self.assertEqual(report["summary"]["fail"], 0)

    def test_adapter_invocation_never_uses_shell_interpolation(self) -> None:
        payload = {
            "adapterProtocol": aduc_conformance.FULL_CORE_ADAPTER_PROTOCOL,
            "operation": "declareCapabilities",
            "implementation": {"id": "urn:aduc:test:mock", "kind": "external"},
            "capabilities": {"validate": True, "compare": True, "format": True},
        }
        completed = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout=json.dumps(payload),
            stderr="",
        )
        with patch.object(aduc_conformance.subprocess, "run", return_value=completed) as run:
            status, parsed, diagnostics = aduc_conformance.invoke_full_core_adapter(
                ["python", "adapter;not-a-shell-command"],
                "declareCapabilities",
                [],
                timeout_seconds=1,
                max_stdout_bytes=10_000,
            )
        self.assertEqual(status, "pass")
        self.assertEqual(parsed["operation"], "declareCapabilities")
        self.assertEqual(diagnostics, [])
        self.assertFalse(run.call_args.kwargs["shell"])
        self.assertEqual(
            run.call_args.args[0],
            ["python", "adapter;not-a-shell-command", "declareCapabilities"],
        )

    def test_cli_json_and_text_reports(self) -> None:
        json_run = subprocess.run(
            [
                sys.executable,
                str(TOOL),
                "run",
                "--suite",
                str(SUITE),
                "--format",
                "json",
                "--adapter",
                sys.executable,
                str(REFERENCE_ADAPTER),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(json_run.returncode, 0, json_run.stderr + json_run.stdout)
        self.assertEqual(json.loads(json_run.stdout)["summary"]["fail"], 0)

        text_run = subprocess.run(
            [
                sys.executable,
                str(TOOL),
                "run",
                "--suite",
                str(SUITE),
                "--adapter",
                sys.executable,
                str(REFERENCE_ADAPTER),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(text_run.returncode, 0, text_run.stderr + text_run.stdout)
        self.assertIn("ADUC FULL-CORE CONFORMANCE", text_run.stdout)


if __name__ == "__main__":
    unittest.main()
