#!/usr/bin/env python3
"""Expand, normalize, and round-trip ADUC profiles as JSON-LD/RDF."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable

from pyld import jsonld

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from aduc_validate import DEFAULT_SCHEMA_PATH, load_json, validate_profile  # noqa: E402

ROOT = TOOLS_DIR.parent
CONTEXT_URI = "urn:aduc:context:0.1"
DEFAULT_CONTEXT_PATH = ROOT / "context" / "aduc-context-0.1.jsonld"

EXIT_VALID = 0
EXIT_INVALID = 1
EXIT_INPUT_ERROR = 2


class AducJsonLdError(ValueError):
    """Raised when a profile cannot be processed as official ADUC JSON-LD."""


def load_context_document(path: Path = DEFAULT_CONTEXT_PATH) -> dict[str, Any]:
    document = load_json(path)
    if not isinstance(document, dict) or not isinstance(document.get("@context"), dict):
        raise AducJsonLdError(
            f"Context document {path} must contain an object-valued @context."
        )
    return document


def make_document_loader(
    context_document: dict[str, Any],
) -> Callable[[str, dict[str, Any] | None], dict[str, Any]]:
    def loader(
        url: str,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        del options
        if url == CONTEXT_URI:
            return {
                "contextUrl": None,
                "documentUrl": CONTEXT_URI,
                "document": context_document,
            }
        raise jsonld.JsonLdError(
            f"Unsupported JSON-LD document or context: {url}",
            "loading document failed",
            details={"url": url},
            code="loading document failed",
        )

    return loader


def ensure_official_context(profile: Any) -> None:
    if not isinstance(profile, dict):
        raise AducJsonLdError("ADUC profile must be a JSON object.")
    context = profile.get("@context")
    if context != CONTEXT_URI:
        raise AducJsonLdError(
            f"Official ADUC v0.1 processing requires @context {CONTEXT_URI!r}; "
            f"received {context!r}."
        )


def expand_profile(
    profile: Any,
    *,
    context_path: Path = DEFAULT_CONTEXT_PATH,
) -> list[dict[str, Any]]:
    ensure_official_context(profile)
    context_document = load_context_document(context_path)
    loader = make_document_loader(context_document)
    try:
        expanded = jsonld.expand(
            profile,
            options={"documentLoader": loader},
        )
    except jsonld.JsonLdError as error:
        raise AducJsonLdError(str(error)) from error
    if not isinstance(expanded, list):
        raise AducJsonLdError("JSON-LD expansion did not produce a node array.")
    return expanded


def normalize_profile(
    profile: Any,
    *,
    context_path: Path = DEFAULT_CONTEXT_PATH,
) -> str:
    ensure_official_context(profile)
    context_document = load_context_document(context_path)
    loader = make_document_loader(context_document)
    try:
        normalized = jsonld.normalize(
            profile,
            options={
                "algorithm": "URDNA2015",
                "format": "application/n-quads",
                "documentLoader": loader,
            },
        )
    except jsonld.JsonLdError as error:
        raise AducJsonLdError(str(error)) from error
    if not isinstance(normalized, str):
        raise AducJsonLdError("JSON-LD normalization did not produce N-Quads.")
    return normalized


def compact_profile(
    profile: Any,
    *,
    context_path: Path = DEFAULT_CONTEXT_PATH,
) -> dict[str, Any]:
    expanded = expand_profile(profile, context_path=context_path)
    context_document = load_context_document(context_path)
    loader = make_document_loader(context_document)
    try:
        compacted = jsonld.compact(
            expanded,
            context_document["@context"],
            options={"documentLoader": loader},
        )
    except jsonld.JsonLdError as error:
        raise AducJsonLdError(str(error)) from error
    if not isinstance(compacted, dict):
        raise AducJsonLdError("JSON-LD compaction did not produce an object.")
    return compacted


def verify_round_trip(
    profile: Any,
    *,
    context_path: Path = DEFAULT_CONTEXT_PATH,
) -> tuple[bool, str, str]:
    original = normalize_profile(profile, context_path=context_path)
    compacted = compact_profile(profile, context_path=context_path)
    context_document = load_context_document(context_path)
    loader = make_document_loader(context_document)
    try:
        round_tripped = jsonld.normalize(
            compacted,
            options={
                "algorithm": "URDNA2015",
                "format": "application/n-quads",
                "documentLoader": loader,
            },
        )
    except jsonld.JsonLdError as error:
        raise AducJsonLdError(str(error)) from error
    if not isinstance(round_tripped, str):
        raise AducJsonLdError("Round-trip normalization did not produce N-Quads.")
    return original == round_tripped, original, round_tripped


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Expand and normalize an ADUC profile as JSON-LD/RDF."
    )
    parser.add_argument("profile", type=Path)
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA_PATH,
        help="Path to the ADUC mapping-profile JSON Schema",
    )
    parser.add_argument(
        "--context",
        type=Path,
        default=DEFAULT_CONTEXT_PATH,
        help="Path to the pinned ADUC JSON-LD context document",
    )
    parser.add_argument(
        "--format",
        choices=("nquads", "expanded", "compacted"),
        default="nquads",
        dest="output_format",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        profile = load_json(args.profile)
    except FileNotFoundError:
        print("ADUC-INPUT-001: Profile file does not exist.", file=sys.stderr)
        return EXIT_INPUT_ERROR
    except OSError as error:
        print(f"ADUC-INPUT-001: Unable to read profile: {error}", file=sys.stderr)
        return EXIT_INPUT_ERROR
    except json.JSONDecodeError as error:
        print(
            (
                "ADUC-INPUT-002: Invalid JSON at "
                f"line {error.lineno}, column {error.colno}: {error.msg}"
            ),
            file=sys.stderr,
        )
        return EXIT_INPUT_ERROR

    try:
        schema = load_json(args.schema)
    except (OSError, json.JSONDecodeError) as error:
        print(f"ADUC-INPUT-003: Unable to load schema: {error}", file=sys.stderr)
        return EXIT_INPUT_ERROR

    validation = validate_profile(profile, schema, profile_path=str(args.profile))
    if not validation["valid"]:
        print(json.dumps(validation, indent=2, ensure_ascii=False, sort_keys=True))
        return EXIT_INVALID

    try:
        round_trip_ok, normalized, _ = verify_round_trip(
            profile,
            context_path=args.context,
        )
        if not round_trip_ok:
            print(
                "ADUC-JSONLD-002: RDF round-trip changed the normalized graph.",
                file=sys.stderr,
            )
            return EXIT_INVALID

        if args.output_format == "nquads":
            sys.stdout.write(normalized)
        elif args.output_format == "expanded":
            print(
                json.dumps(
                    expand_profile(profile, context_path=args.context),
                    indent=2,
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        else:
            print(
                json.dumps(
                    compact_profile(profile, context_path=args.context),
                    indent=2,
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
    except (AducJsonLdError, OSError, json.JSONDecodeError) as error:
        print(f"ADUC-JSONLD-001: {error}", file=sys.stderr)
        return EXIT_INVALID

    return EXIT_VALID


if __name__ == "__main__":
    sys.exit(main())
