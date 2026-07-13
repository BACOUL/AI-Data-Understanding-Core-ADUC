from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = ROOT / "tools" / "aduc_provenance.py"
REFERENCE_PATH = ROOT / "examples" / "provenance" / "reference-cases.json"
INVALID_PATH = ROOT / "examples" / "provenance" / "invalid-cases.json"

spec = importlib.util.spec_from_file_location("aduc_provenance", TOOL_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def pointer_parent(document: Any, pointer: str) -> tuple[Any, str]:
    parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer.split("/")[1:]]
    current = document
    for part in parts[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current, parts[-1]


def apply_operations(case: dict[str, Any], operations: list[dict[str, Any]]) -> dict[str, Any]:
    result = copy.deepcopy(case)
    for operation in operations:
        op = operation["op"]
        if op in {"remove", "replace"}:
            parent, key = pointer_parent(result, operation["path"])
            if op == "remove":
                if isinstance(parent, list):
                    parent.pop(int(key))
                else:
                    parent.pop(key, None)
            elif isinstance(parent, list):
                parent[int(key)] = operation["value"]
            else:
                parent[key] = operation["value"]
        elif op == "append":
            parent, key = pointer_parent(result, operation["path"])
            target = parent[int(key)] if isinstance(parent, list) else parent[key]
            target.append(copy.deepcopy(operation["value"]))
        elif op == "clone-activity":
            cloned = copy.deepcopy(result["activities"][operation["index"]])
            cloned["activityId"] = operation["newId"]
            cloned["startedAt"] = operation["startedAt"]
            cloned["endedAt"] = operation["endedAt"]
            result["activities"].append(cloned)
        elif op == "append-late-use":
            entity = {
                "entityId": "urn:e:late-output",
                "entityType": "urn:aduc:artifact:Data",
                "contentHash": "sha256:4ae9217429bdf8f263d3c9234ee2fcdad82c5f5425cf552f7f873f5f8296e87a",
                "sourceBinding": "urn:b:late-output",
                "lifecycleState": "active",
            }
            result["entities"].append(entity)
            result["activities"].append(
                {
                    "activityId": "urn:activity:late-use",
                    "activityType": "comparison",
                    "method": "urn:aduc:method:late-use",
                    "startedAt": "2026-07-13T12:50:00Z",
                    "endedAt": "2026-07-13T12:50:01Z",
                    "executionMode": "deterministic",
                    "lineageState": "observed",
                    "authorityLevel": "verified",
                    "assertedBy": "urn:org:aduc",
                    "evidence": ["urn:evidence:late-use"],
                    "associatedAgents": [{"agentId": "urn:s:fix", "role": "executor"}],
                    "used": [{"entityId": "urn:e:old", "role": "input"}],
                    "generated": [{"entityId": "urn:e:late-output", "role": "output"}],
                    "execution": {
                        "softwareAgent": "urn:s:fix",
                        "environmentDigest": "sha256:a647ff00382b495ee6708bd88e9cb585ad6f78b6d945071b44db204a88096fa0",
                        "parametersDigest": "sha256:78cf053facfe1429569ff8555c4316a84c5955bc9431e085134b71855214300b",
                    },
                    "reproducibilityClaim": "deterministic",
                    "conflictState": "clear",
                    "lifecycleState": "active",
                }
            )
        else:
            raise AssertionError(f"unsupported fixture operation: {op}")
    return result


class ProvenanceProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.references = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))
        cls.reference_by_id = {case["caseId"]: case for case in cls.references}
        cls.invalid_fixtures = json.loads(INVALID_PATH.read_text(encoding="utf-8"))

    def test_all_reference_cases_are_valid(self) -> None:
        self.assertGreaterEqual(len(self.references), 7)
        for case in self.references:
            with self.subTest(case=case["caseId"]):
                result = module.evaluate_case(case)
                self.assertTrue(result["valid"], result)
                self.assertTrue(result["traceable"], result)

    def test_all_invalid_cases_fail_with_expected_code(self) -> None:
        self.assertGreaterEqual(len(self.invalid_fixtures), 20)
        for item in self.invalid_fixtures:
            with self.subTest(case=item["caseId"]):
                base = self.reference_by_id[item["baseCaseId"]]
                case = apply_operations(base, item["operations"])
                result = module.evaluate_case(case)
                codes = {entry["code"] for entry in result["errors"]}
                self.assertFalse(result["valid"], result)
                self.assertIn(item["expectedCode"], codes, result)

    def test_end_to_end_chain_is_deterministic(self) -> None:
        case = self.reference_by_id["end-to-end-deterministic-lineage"]
        result = module.evaluate_case(case)
        self.assertTrue(result["valid"])
        self.assertEqual(result["disclosureState"], "complete")
        self.assertEqual([entry["claim"] for entry in result["reproducibility"]], ["deterministic"] * 5)

    def test_replayable_model_is_not_called_deterministic(self) -> None:
        result = module.evaluate_case(self.reference_by_id["replayable-model-inference"])
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["reproducibility"][0]["claim"], "replayable")

    def test_partial_and_redacted_cases_emit_warnings(self) -> None:
        for case_id in {"reconstructed-inferred-partial-lineage", "redacted-manual-lineage"}:
            result = module.evaluate_case(self.reference_by_id[case_id])
            self.assertTrue(result["valid"], result)
            self.assertTrue(result["warnings"], result)

    def test_cycle_detection(self) -> None:
        item = next(item for item in self.invalid_fixtures if item["caseId"] == "provenance-cycle")
        result = module.evaluate_case(apply_operations(self.reference_by_id[item["baseCaseId"]], item["operations"]))
        self.assertIn("ADUC-PROV-006", {entry["code"] for entry in result["errors"]})

    def test_cli_accepts_reference_cases(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(TOOL_PATH), str(REFERENCE_PATH)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("VALID", completed.stdout)

    def test_cli_rejects_materialized_invalid_case(self) -> None:
        item = self.invalid_fixtures[0]
        case = apply_operations(self.reference_by_id[item["baseCaseId"]], item["operations"])
        temp_path = ROOT / "tests" / "provenance" / "_invalid_case.tmp.json"
        try:
            temp_path.write_text(json.dumps(case), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(TOOL_PATH), str(temp_path), "--format", "json"],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 1)
            payload = json.loads(completed.stdout)
            self.assertFalse(payload[0]["valid"])
        finally:
            temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
