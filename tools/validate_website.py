#!/usr/bin/env python3
"""Validate the static ADUC website and the first full-Core draft example."""

from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
WEBSITE = ROOT / "website"
EXAMPLE = ROOT / "examples" / "basic-json" / "river-r42.aduc.json"

REQUIRED_PAGES = {
    "index.html",
    "specification.html",
    "architecture.html",
    "roadmap.html",
    "example.html",
    "docs.html",
}

REQUIRED_CORE_BLOCKS = {
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


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.ids: set[str] = set()
        self.has_html_en = False
        self.has_title = False
        self.has_description = False
        self.has_canonical = False
        self.has_stylesheet = False
        self.has_script = False
        self._in_title = False
        self._title_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html" and values.get("lang") == "en":
            self.has_html_en = True
        if "id" in values and values["id"]:
            self.ids.add(values["id"] or "")
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        if tag == "link":
            rel = values.get("rel", "") or ""
            href = values.get("href", "") or ""
            if "canonical" in rel.split():
                self.has_canonical = bool(href)
            if "stylesheet" in rel.split():
                self.has_stylesheet = bool(href)
        if tag == "meta" and values.get("name") == "description":
            self.has_description = bool(values.get("content"))
        if tag == "script" and values.get("src"):
            self.has_script = True
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
            self.has_title = bool("".join(self._title_text).strip())

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_text.append(data)


def resolve_internal_link(page: Path, href: str) -> tuple[Path, str | None] | None:
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc or href.startswith("mailto:"):
        return None
    if href.startswith("#"):
        return page, parsed.fragment or None
    target = (page.parent / parsed.path).resolve()
    return target, parsed.fragment or None


def validate_page(page: Path, parsed_pages: dict[Path, PageParser]) -> list[str]:
    errors: list[str] = []
    parser = PageParser()
    parser.feed(page.read_text(encoding="utf-8"))
    parsed_pages[page.resolve()] = parser

    checks = {
        "html lang=en": parser.has_html_en,
        "non-empty title": parser.has_title,
        "meta description": parser.has_description,
        "canonical link": parser.has_canonical,
        "stylesheet": parser.has_stylesheet,
        "script": parser.has_script,
    }
    for label, passed in checks.items():
        if not passed:
            errors.append(f"{page.relative_to(ROOT)}: missing {label}")

    text = page.read_text(encoding="utf-8").lower()
    if "not yet a recognized standard" not in text:
        errors.append(
            f"{page.relative_to(ROOT)}: missing public working-draft disclaimer"
        )
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
                errors.append(
                    f"{page.relative_to(ROOT)}: broken internal link {href!r}"
                )
                continue
            if fragment and target.suffix == ".html":
                target_parser = parsed_pages.get(target.resolve())
                if target_parser is None:
                    target_parser = PageParser()
                    target_parser.feed(target.read_text(encoding="utf-8"))
                    parsed_pages[target.resolve()] = target_parser
                if fragment not in target_parser.ids:
                    errors.append(
                        f"{page.relative_to(ROOT)}: missing fragment #{fragment} in "
                        f"{target.relative_to(ROOT)}"
                    )
    return errors


def validate_example() -> list[str]:
    errors: list[str] = []
    if not EXAMPLE.exists():
        return [f"Missing full-Core example: {EXAMPLE.relative_to(ROOT)}"]
    document = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        return [f"{EXAMPLE.relative_to(ROOT)} must contain a JSON object"]
    missing = sorted(REQUIRED_CORE_BLOCKS - set(document))
    extra_check = document.get("aduc", {}).get("version") if isinstance(document.get("aduc"), dict) else None
    if missing:
        errors.append(
            f"{EXAMPLE.relative_to(ROOT)}: missing Core blocks {', '.join(missing)}"
        )
    if extra_check != "0.1.0-draft":
        errors.append(
            f"{EXAMPLE.relative_to(ROOT)}: expected aduc.version '0.1.0-draft'"
        )
    return errors


def main() -> int:
    errors: list[str] = []
    missing_pages = sorted(REQUIRED_PAGES - {path.name for path in WEBSITE.glob("*.html")})
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
            errors.extend(validate_page(page, parsed_pages))

    errors.extend(validate_links(parsed_pages))
    errors.extend(validate_example())

    if errors:
        print("Website validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Validated {len(REQUIRED_PAGES)} English website pages, internal links, "
        "metadata, deployment artifacts, and the ten-block full-Core example."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
