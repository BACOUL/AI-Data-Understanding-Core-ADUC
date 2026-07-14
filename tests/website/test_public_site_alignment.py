from __future__ import annotations

import json
import re
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WEBSITE = ROOT / "website"
SITE_DATA = WEBSITE / "assets" / "site-data.json"
CANONICAL_BASE = "https://bacoul.github.io/AI-Data-Understanding-Core-ADUC/"

PAGES = {
    "index.html",
    "why-aduc.html",
    "core.html",
    "validate.html",
    "compare.html",
    "trust.html",
    "evidence.html",
    "roadmap.html",
    "docs.html",
    "architecture.html",
    "example.html",
    "specification.html",
}

CANONICAL_DEFINITION = (
    "ADUC is a machine-readable contract that makes a data resource's "
    "structure, meaning, context, identity, provenance, uncertainty, "
    "relations and use conditions explicit, validatable and portable "
    "across AI systems."
)

CORE_BLOCKS = [
    "aduc",
    "resource",
    "structure",
    "semantics",
    "identity",
    "context",
    "provenance",
    "uncertainty",
    "relations",
    "policy",
]

OBSOLETE_PHRASES = [
    "full-Core validator remains planned",
    "full-Core schema remains future",
    "current implementation mainly covers semantics",
    "unified validation and comparison is the next task",
    "unified full-Core validator not implemented",
    "Next action: unified full-Core validator and deterministic comparator",
]

OLD_JSON_SYNTAX = [
    "mappingStatus",
    "semantics.flow",
    "context.timeField",
    '"concept":',
    '"unit":',
]


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.h1 = 0
        self.canonical = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        if tag == "h1":
            self.h1 += 1
        if tag == "link" and values.get("rel") == "canonical":
            self.canonical = values.get("href") or ""


def page_text(name: str) -> str:
    return (WEBSITE / name).read_text(encoding="utf-8")


class PublicSiteAlignmentTests(unittest.TestCase):
    def test_required_pages_exist_and_have_unique_h1(self) -> None:
        for page in PAGES:
            with self.subTest(page=page):
                path = WEBSITE / page
                self.assertTrue(path.is_file(), page)
                parser = LinkParser()
                parser.feed(page_text(page))
                self.assertEqual(parser.h1, 1, page)

    def test_canonical_definition_and_real_commands_are_present(self) -> None:
        home = page_text("index.html")
        docs = page_text("docs.html")
        compare = page_text("compare.html")
        self.assertIn(CANONICAL_DEFINITION, home)
        self.assertIn(
            "python tools/aduc_core.py validate examples/core/complete-model.example.json",
            home + docs,
        )
        self.assertIn(
            "python tools/aduc_core.py compare examples/core/complete-model.example.json examples/core/complete-model.example.json",
            docs,
        )
        self.assertIn("python tools/aduc_core.py compare contract-a.json contract-b.json", compare)

    def test_ten_core_blocks_are_visible(self) -> None:
        combined = page_text("index.html") + page_text("core.html")
        for block in CORE_BLOCKS:
            with self.subTest(block=block):
                self.assertIn(block, combined)

    def test_obsolete_public_claims_and_old_json_syntax_are_absent(self) -> None:
        public_text = "\n".join(page_text(page) for page in PAGES)
        lower = public_text.lower()
        for phrase in OBSOLETE_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase.lower(), lower)
        for field in OLD_JSON_SYNTAX:
            with self.subTest(field=field):
                self.assertNotIn(field, public_text)

    def test_available_in_progress_planned_and_not_proven_are_distinct(self) -> None:
        home = page_text("index.html")
        roadmap = page_text("roadmap.html")
        evidence = page_text("evidence.html")
        self.assertIn("Available now", home)
        self.assertIn("In progress", home)
        self.assertIn("Planned, not available", home)
        self.assertIn("Not proven", home)
        self.assertIn("Active task - Deterministic Core formatter", roadmap)
        self.assertIn("No external two-consumer AI proof has completed.", evidence)
        self.assertIn("No absolute first-world claim is made.", evidence)

    def test_site_data_metrics_match_public_pages(self) -> None:
        data = json.loads(SITE_DATA.read_text(encoding="utf-8"))
        available = data["availableNow"]
        self.assertEqual(available["coreBlocks"], 10)
        self.assertEqual(available["schemaFiles"], 14)
        self.assertEqual(available["validCoreFixtures"], 11)
        self.assertEqual(available["invalidCoreFixtures"], 15)
        self.assertEqual(available["comparisonScenarios"], 24)
        public_metrics = page_text("index.html") + page_text("evidence.html")
        for key in [
            "coreBlocks",
            "schemaFiles",
            "validCoreFixtures",
            "invalidCoreFixtures",
            "comparisonScenarios",
        ]:
            self.assertRegex(public_metrics, rf"\b{available[key]}\b")
        self.assertEqual(data["activeTask"], "deterministic complete-Core contract formatter")
        self.assertTrue(available["semanticProfileMigration"])

    def test_sitemap_and_canonical_urls_are_consistent(self) -> None:
        sitemap = ET.fromstring((WEBSITE / "sitemap.xml").read_text(encoding="utf-8"))
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = {node.text for node in sitemap.findall(".//s:loc", namespace)}
        for page in PAGES:
            if page == "404.html":
                continue
            expected = CANONICAL_BASE if page == "index.html" else CANONICAL_BASE + page
            self.assertIn(expected, locs)
            parser = LinkParser()
            parser.feed(page_text(page))
            self.assertEqual(parser.canonical, expected)

    def test_no_broken_internal_links(self) -> None:
        for page in PAGES:
            parser = LinkParser()
            parser.feed(page_text(page))
            for href in parser.links:
                if href.startswith("http") or href.startswith("mailto:"):
                    continue
                target = href.split("#", 1)[0] or page
                with self.subTest(page=page, href=href):
                    self.assertTrue((WEBSITE / target).exists(), f"{page}: {href}")

    def test_css_keeps_mobile_and_accessibility_guards(self) -> None:
        css = (WEBSITE / "assets" / "styles.css").read_text(encoding="utf-8")
        self.assertIn("prefers-reduced-motion", css)
        self.assertIn(":focus-visible", css)
        self.assertIn("@media(max-width:700px)", css)
        self.assertIsNone(re.search(r"overflow-x\s*:\s*hidden", css))


if __name__ == "__main__":
    unittest.main()
