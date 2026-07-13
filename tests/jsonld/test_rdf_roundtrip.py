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
MODULE_PATH = ROOT / "tools" / "aduc_rdf.py"
CONTEXT_PATH = ROOT / "context" / "aduc-context-0.1.jsonld"
VALID_CASES_PATH = (
    ROOT / "tests" / "fixtures" / "mapping-profile" / "valid" / "cases.json"
)

spec = importlib.util.spec_from_file_location("aduc_rdf", MODULE_PATH)
assert spec and spec.loader
aduc_rdf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aduc_rdf)


class RdfRoundTripTests(unittest.TestCase):
    def published_profiles(self) -> list[tuple[str, dict]]:
        paths = sorted((ROOT / "examples" / "authoring").rglob("*.aduc.json"))
        paths += sorted((ROOT / "examples" / "comparison").rglob("*.aduc.json"))
        return [
            (str(path.relative_to(ROOT)), json.loads(path.read_text(encoding="utf-8")))
            for path in paths
        ]

    def valid_fixture_profiles(self) -> list[tuple[str, dict]]:
        document = json.loads(VALID_CASES_PATH.read_text(encoding="utf-8"))
        return [
            (f"fixture:{case['name']}", case["instance"])
            for case in document["cases"]
        ]

    def all_official_profiles(self) -> list[tuple[str, dict]]:
        return self.published_profiles() + self.valid_fixture_profiles()

    def test_context_contains_protected_expected_mappings(self) -> None:
        context = json.loads(CONTEXT_PATH.read_text(encoding="utf-8"))["@context"]
        self.assertTrue(context["@protected"])
        self.assertEqual(context["@vocab"], "urn:aduc:term:")
        self.assertEqual(context["assertedBy"]["@id"], "prov:wasAttributedTo")
        self.assertEqual(context["assertedAt"]["@id"], "prov:generatedAtTime")
        self.assertEqual(context["evidence"]["@id"], "prov:wasDerivedFrom")
        self.assertEqual(context["supersedes"]["@id"], "prov:wasRevisionOf")
        self.assertEqual(context["confidence"]["@type"], "xsd:decimal")

    def test_every_official_profile_expands_and_round_trips(self) -> None:
        profiles = self.all_official_profiles()
        self.assertEqual(len(profiles), 10)
        for name, profile in profiles:
            with self.subTest(profile=name):
                self.assertEqual(profile["@context"], aduc_rdf.CONTEXT_URI)
                expanded = aduc_rdf.expand_profile(profile)
                self.assertGreater(len(expanded), 0)
                ok, original, round_tripped = aduc_rdf.verify_round_trip(profile)
                self.assertTrue(ok, f"RDF round-trip changed {name}")
                self.assertEqual(original, round_tripped)

    def test_required_graph_evidence_is_preserved(self) -> None:
        for name, profile in self.all_official_profiles():
            with self.subTest(profile=name):
                nquads = aduc_rdf.normalize_profile(profile)
                self.assertIn(f"<{profile['id']}>", nquads)
                self.assertIn(f"<{profile['describes']}>", nquads)
                self.assertIn(f"<{profile['validFor']['source']}>", nquads)
                self.assertIn("<urn:aduc:term:validFor>", nquads)
                self.assertIn("<urn:aduc:term:assertion>", nquads)

                for assertion in profile["assertions"]:
                    self.assertIn(f"<{assertion['id']}>", nquads)
                    self.assertIn(f"<{assertion['semanticTarget']}>", nquads)
                    self.assertIn(f"<{assertion['mappingRelation']}>", nquads)
                    self.assertIn(f"<urn:aduc:term:{assertion['status']}>", nquads)
                    self.assertIn(f"<{assertion['assertedBy']}>", nquads)
                    self.assertIn(
                        "<http://www.w3.org/ns/prov#generatedAtTime>", nquads
                    )
                    for evidence in assertion.get("evidence", []):
                        self.assertIn(f"<{evidence}>", nquads)
                    if "supersedes" in assertion:
                        self.assertIn(f"<{assertion['supersedes']}>", nquads)
                        self.assertIn(
                            "<http://www.w3.org/ns/prov#wasRevisionOf>", nquads
                        )
                    if "confidenceMethod" in assertion:
                        self.assertIn(f"<{assertion['confidenceMethod']}>", nquads)
                        self.assertIn("<urn:aduc:term:confidence>", nquads)

    def test_normalization_is_independent_of_assertion_order(self) -> None:
        profile = deepcopy(self.valid_fixture_profiles()[0][1])
        second = deepcopy(profile["assertions"][0])
        second["id"] = "urn:aduc:assertion:a0"
        second["localReference"] = "records/other"
        second["semanticTarget"] = "https://example.org/concepts/OtherConcept"
        profile["assertions"].append(second)

        original = aduc_rdf.normalize_profile(profile)
        profile["assertions"].reverse()
        reordered = aduc_rdf.normalize_profile(profile)
        self.assertEqual(original, reordered)

    def test_unknown_context_is_rejected_without_network_access(self) -> None:
        profile = deepcopy(self.valid_fixture_profiles()[0][1])
        profile["@context"] = "https://unknown.example/context.jsonld"
        with self.assertRaises(aduc_rdf.AducJsonLdError):
            aduc_rdf.expand_profile(profile)

    def test_cli_exit_codes_and_nquads_output(self) -> None:
        profile = deepcopy(self.valid_fixture_profiles()[0][1])
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            valid_path = temp / "valid.json"
            unknown_context_path = temp / "unknown-context.json"
            broken_path = temp / "broken.json"
            valid_path.write_text(json.dumps(profile), encoding="utf-8")
            unknown = deepcopy(profile)
            unknown["@context"] = "https://unknown.example/context.jsonld"
            unknown_context_path.write_text(json.dumps(unknown), encoding="utf-8")
            broken_path.write_text("{", encoding="utf-8")

            valid_run = subprocess.run(
                [sys.executable, str(MODULE_PATH), str(valid_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(valid_run.returncode, 0, valid_run.stderr)
            self.assertIn("<urn:aduc:assertion:a1>", valid_run.stdout)

            unknown_run = subprocess.run(
                [sys.executable, str(MODULE_PATH), str(unknown_context_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(unknown_run.returncode, 1)
            self.assertIn("ADUC-JSONLD-001", unknown_run.stderr)

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
