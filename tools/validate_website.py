#!/usr/bin/env python3
"""Validate the static ADUC public website."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
WEBSITE = ROOT / "website"
SITE_DATA = WEBSITE / "assets" / "site-data.json"
EXAMPLE = ROOT / "examples" / "core" / "complete-model.example.json"
CANONICAL_BASE = "https://bacoul.github.io/AI-Data-Understanding-Core-ADUC/"

REQUIRED_PAGES = {
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

NAV_TARGETS = {
    "index.html",
    "why-aduc.html",
    "core.html",
    "validate.html",
    "compare.html",
    "trust.html",
    "evidence.html",
    "roadmap.html",
    "docs.html",
}

CORE_BLOCKS = {
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
}

OBSOLETE_CLAIMS = [
    "full-core validator remains planned",
    "full-core schema remains future",
    "current implementation mainly covers semantics",
    "unified validation and comparison is the next task",
    "unified full-core validator not implemented",
    "complete core schema, compiler and full interoperability proof remain future gates",
    "next action: unified full-core validator and deterministic comparator",
]

OLD_EXAMPLE_FIELDS = [
    "mappingStatus",
    "semantics.flow",
    "context.timeField",
    '"concept":',
    '"unit":',
]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.ids: set[str] = set()
        self.nav_links: set[str] = set()
        self.h1_count = 0
        self.h2_count = 0
        self.has_html_en = False
        self.has_title = False
        self.has_description = False
        self.has_canonical = False
        self.canonical_href = ""
        self.has_stylesheet = False
        self.has_viewport = False
        self.has_og = False
        self.has_twitter = False
        self.has_json_ld = False
        self.json_ld_text: list[str] = []
        self._in_title = False
        self._title_text: list[str] = []
        self._in_json_ld = False
        self._in_nav = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html" and values.get("lang") == "en":
            self.has_html_en = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "h2":
            self.h2_count += 1
        if "id" in values and values["id"]:
            self.ids.add(values["id"] or "")
        if tag == "nav" and values.get("aria-label") == "Primary navigation":
            self._in_nav = True
        if tag == "a" and values.get("href"):
            href = values["href"] or ""
            self.links.append(href)
            if self._in_nav:
                self.nav_links.add(href)
        if tag == "link":
            rel = values.get("rel", "") or ""
            href = values.get("href", "") or ""
            if "canonical" in rel.split():
                self.has_canonical = bool(href)
                self.canonical_href = href
            if "stylesheet" in rel.split():
                self.has_stylesheet = bool(href)
        if tag == "meta":
            if values.get("name") == "viewport":
                self.has_viewport = True
            if values.get("name") == "description":
                self.has_description = bool(values.get("content"))
            if (values.get("property") or "").startswith("og:"):
                self.has_og = True
            if (values.get("name") or "").startswith("twitter:"):
                self.has_twitter = True
        if tag == "script" and values.get("type") == "application/ld+json":
            self.has_json_ld = True
            self._in_json_ld = True
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
            self.has_title = bool("".join(self._title_text).strip())
        if tag == "script":
            self._in_json_ld = False
        if tag == "nav":
            self._in_nav = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_text.append(data)
        if self._in_json_ld:
            self.json_ld_text.append(data)


def page_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def resolve_internal_link(page: Path, href: str) -> tuple[Path, str | None] | None:
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc or href.startswith("mailto:"):
        return None
    if href.startswith("#"):
        return page, parsed.fragment or None
    target = (page.parent / parsed.path).resolve()
    return target, parsed.fragment or None


def validate_page(page: Path, site_data: dict[str, object], parsed_pages: dict[Path, PageParser]) -> list[str]:
    errors: list[str] = []
    parser = PageParser()
    text = page_text(page)
    parser.feed(text)
    parsed_pages[page.resolve()] = parser

    checks = {
        "html lang=en": parser.has_html_en,
        "viewport": parser.has_viewport,
        "non-empty title": parser.has_title,
        "meta description": parser.has_description,
        "canonical link": parser.has_canonical,
        "stylesheet": parser.has_stylesheet,
        "Open Graph metadata": parser.has_og,
        "Twitter metadata": parser.has_twitter,
        "JSON-LD": parser.has_json_ld,
        "one H1": parser.h1_count == 1,
        "at least one H2": parser.h2_count >= 1,
    }
    for label, passed in checks.items():
        if not passed:
            errors.append(f"{page.relative_to(ROOT)}: missing or invalid {label}")

    expected = CANONICAL_BASE if page.name == "index.html" else f"{CANONICAL_BASE}{page.name}"
    if parser.canonical_href != expected:
        errors.append(
            f"{page.relative_to(ROOT)}: canonical {parser.canonical_href!r} != {expected!r}"
        )

    missing_nav = sorted(NAV_TARGETS - parser.nav_links)
    if missing_nav:
        errors.append(
            f"{page.relative_to(ROOT)}: primary navigation missing {', '.join(missing_nav)}"
        )

    lowered = text.lower()
    for claim in OBSOLETE_CLAIMS:
        if claim in lowered:
            errors.append(f"{page.relative_to(ROOT)}: obsolete claim present: {claim}")
    for field in OLD_EXAMPLE_FIELDS:
        if field in text:
            errors.append(f"{page.relative_to(ROOT)}: old invalid example field present: {field}")

    if "not yet a recognized standard" not in lowered:
        errors.append(f"{page.relative_to(ROOT)}: missing Working Draft disclaimer")

    if page.name in {"index.html", "core.html"}:
        missing_blocks = sorted(block for block in CORE_BLOCKS if block not in text)
        if missing_blocks:
            errors.append(
                f"{page.relative_to(ROOT)}: missing Core block names {', '.join(missing_blocks)}"
            )

    if page.name in {"index.html", "docs.html", "validate.html"} and (
        "python tools/aduc_core.py validate examples/core/complete-model.example.json" not in text
    ):
        errors.append(f"{page.relative_to(ROOT)}: missing real validation command")
    if page.name in {"docs.html", "compare.html"} and (
        "python tools/aduc_core.py compare" not in text
    ):
        errors.append(f"{page.relative_to(ROOT)}: missing real comparison command")

    available = site_data.get("availableNow", {})
    if isinstance(available, dict):
        required_values = [
            str(available.get("coreBlocks")),
            str(available.get("schemaFiles")),
            str(available.get("validCoreFixtures")),
            str(available.get("invalidCoreFixtures")),
            str(available.get("comparisonScenarios")),
        ]
        if page.name in {"index.html", "evidence.html"}:
            for value in required_values:
                if value and value not in text:
                    errors.append(f"{page.relative_to(ROOT)}: missing site-data metric {value}")

    if parser.json_ld_text:
        try:
            json.loads("".join(parser.json_ld_text))
        except json.JSONDecodeError as exc:
            errors.append(f"{page.relative_to(ROOT)}: invalid JSON-LD: {exc}")

    return errors


def validate_links(parsed_pages: dict[Path, PageParser]) -> list[str]:
    errors: list[str] = []
    for page, parser in parsed_pages.items():
        for href in parser.links:
            resolved = resolve_internal_link(page, href)
            if resolved is None:
                continue
            target, fragment = resolved
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                errors.append(f"{page.relative_to(ROOT)}: broken internal link {href!r}")
                continue
            if fragment and target.suffix == ".html":
                target_parser = parsed_pages.get(target.resolve())
                if target_parser is None:
                    target_parser = PageParser()
                    target_parser.feed(page_text(target))
                    parsed_pages[target.resolve()] = target_parser
                if fragment not in target_parser.ids:
                    errors.append(
                        f"{page.relative_to(ROOT)}: missing fragment #{fragment} in "
                        f"{target.relative_to(ROOT)}"
                    )
    return errors


def validate_sitemap() -> list[str]:
    errors: list[str] = []
    sitemap = WEBSITE / "sitemap.xml"
    if not sitemap.exists():
        return ["Missing website/sitemap.xml"]
    root = ET.fromstring(page_text(sitemap))
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = {loc.text for loc in root.findall(".//s:loc", namespace)}
    expected = {
        CANONICAL_BASE if name == "index.html" else f"{CANONICAL_BASE}{name}"
        for name in REQUIRED_PAGES
        if name != "404.html"
    }
    missing = sorted(expected - locs)
    extra = sorted(loc for loc in locs - expected if loc)
    if missing:
        errors.append(f"sitemap.xml: missing {', '.join(missing)}")
    if extra:
        errors.append(f"sitemap.xml: unexpected {', '.join(extra)}")
    return errors


def validate_example() -> list[str]:
    if not EXAMPLE.exists():
        return [f"Missing Core example: {EXAMPLE.relative_to(ROOT)}"]
    document = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        return [f"{EXAMPLE.relative_to(ROOT)} must contain a JSON object"]
    missing = sorted(CORE_BLOCKS - set(document))
    if missing:
        return [f"{EXAMPLE.relative_to(ROOT)}: missing Core blocks {', '.join(missing)}"]
    version = document.get("aduc", {}).get("coreVersion")
    if version != "0.1.0-alpha.0":
        return [f"{EXAMPLE.relative_to(ROOT)}: expected coreVersion 0.1.0-alpha.0"]
    return []


def validate_css() -> list[str]:
    css = page_text(WEBSITE / "assets" / "styles.css")
    errors: list[str] = []
    if "prefers-reduced-motion" not in css:
        errors.append("website/assets/styles.css: missing prefers-reduced-motion")
    if re.search(r"overflow-x\s*:\s*hidden", css):
        errors.append("website/assets/styles.css: hides horizontal overflow globally")
    return errors


def main() -> int:
    errors: list[str] = []
    if not SITE_DATA.exists():
        errors.append("Missing website/assets/site-data.json")
        site_data: dict[str, object] = {}
    else:
        site_data = json.loads(SITE_DATA.read_text(encoding="utf-8"))
        if site_data.get("canonicalBase") != CANONICAL_BASE:
            errors.append("site-data canonicalBase does not match public canonical")
        if site_data.get("activeTask") != "deterministic complete-Core contract formatter":
            errors.append("site-data activeTask is not the deterministic Core formatter")
        available = site_data.get("availableNow", {})
        if not isinstance(available, dict) or available.get("semanticProfileMigration") is not True:
            errors.append("site-data does not mark semantic-profile migration as available")

    existing_pages = {path.name for path in WEBSITE.glob("*.html")}
    missing_pages = sorted(REQUIRED_PAGES - existing_pages)
    if missing_pages:
        errors.append(f"Missing website pages: {', '.join(missing_pages)}")

    for required in [
        WEBSITE / "assets" / "styles.css",
        WEBSITE / "assets" / "app.js",
        WEBSITE / "robots.txt",
        WEBSITE / "sitemap.xml",
        WEBSITE / ".nojekyll",
    ]:
        if not required.exists():
            errors.append(f"Missing website artifact: {required.relative_to(ROOT)}")

    parsed_pages: dict[Path, PageParser] = {}
    for page_name in sorted(REQUIRED_PAGES):
        page = WEBSITE / page_name
        if page.exists():
            errors.extend(validate_page(page, site_data, parsed_pages))

    errors.extend(validate_links(parsed_pages))
    errors.extend(validate_sitemap())
    errors.extend(validate_example())
    errors.extend(validate_css())

    robots = WEBSITE / "robots.txt"
    if robots.exists() and f"Sitemap: {CANONICAL_BASE}sitemap.xml" not in page_text(robots):
        errors.append("robots.txt: sitemap URL does not match canonical base")

    if errors:
        print("Website validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Validated {len(REQUIRED_PAGES)} public pages, metadata, canonical URLs, "
        "sitemap, internal links, Core claims, site-data metrics, and examples."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
