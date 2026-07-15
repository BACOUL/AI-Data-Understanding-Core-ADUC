from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AMENDMENT = ROOT / "docs" / "decisions" / "ADR-0004A-full-core-scope-reconciliation.md"
HORIZONS = ROOT / "docs" / "project" / "SOURCE_AND_EXTENSION_HORIZONS.md"
NEXT_ACTION = ROOT / "docs" / "roadmap" / "NEXT_ACTION.md"
CORE_SPEC = ROOT / "spec" / "ADUC_CORE_SPEC_0_1.md"


class ScopeReconciliationTests(unittest.TestCase):
    def test_global_scope_precedence_is_explicit(self) -> None:
        text = AMENDMENT.read_text(encoding="utf-8")
        required = [
            "ADR-0004 governs the global project scope",
            "ADR-0002 is superseded only where",
            "Decisions preserved from ADR-0002",
            "semantic-mapping profile remains a supported experimental input",
            "reuse of maintained standards rather than duplication",
            "no silent promotion",
            "prohibition of hidden provider-specific mappings",
        ]
        for value in required:
            with self.subTest(value=value):
                self.assertIn(value, text)

    def test_json_csv_is_initial_proof_not_permanent_limit(self) -> None:
        text = HORIZONS.read_text(encoding="utf-8")
        required = [
            "Horizon A — Long-term Core mission",
            "Horizon B — Initial proof boundary",
            "Horizon C — Future source profiles and extensions",
            "They are not the permanent limit of ADUC",
            "API Profile",
            "Database / SQL Profile",
            "Live Event and Sensor Profile",
            "Document and Media Profile",
            "Scientific Data Profile",
            "Agent Memory Profile",
            "Situation & Action Extension",
        ]
        for value in required:
            with self.subTest(value=value):
                self.assertIn(value, text)

    def test_structure_remains_binding_layer_not_replacement(self) -> None:
        text = HORIZONS.read_text(encoding="utf-8")
        self.assertIn("stable interoperability index and binding layer", text)
        self.assertIn(
            "must not become a renamed replacement for JSON Schema, Croissant, CSVW, OpenAPI, SQL catalogs",
            text,
        )
        self.assertIn("ADUC owns the binding, qualification and safe cross-module behavior", text)

        core = CORE_SPEC.read_text(encoding="utf-8")
        self.assertIn("JSON Schema, Croissant, CSVW and OpenAPI descriptions are referenced", core)
        self.assertIn("ADUC composes established standards", core)

    def test_active_conformance_task_is_not_replaced(self) -> None:
        text = NEXT_ACTION.read_text(encoding="utf-8")
        self.assertIn("provider-neutral full-Core conformance runner", text)
        self.assertIn("validators, comparators and formatters", text)
        self.assertIn("JSON/CSV compiler remains blocked", text)
        self.assertNotIn("Database / SQL Profile", text)
        self.assertNotIn("Document and Media Profile", text)


if __name__ == "__main__":
    unittest.main()
