#!/usr/bin/env python3
"""Validate local links in docs/index.html."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
INDEX_PATH = DOCS_DIR / "index.html"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return

        attributes = dict(attrs)
        href = attributes.get("href")
        if href:
            self.links.append(href)


def is_external(href: str) -> bool:
    parsed = urlparse(href)
    return bool(parsed.scheme or parsed.netloc)


def validate_links() -> list[str]:
    parser = LinkParser()
    parser.feed(INDEX_PATH.read_text(encoding="utf-8"))

    errors: list[str] = []
    for href in parser.links:
        if href.startswith("#") or is_external(href):
            continue

        target = (INDEX_PATH.parent / href).resolve()
        try:
            target.relative_to(ROOT)
        except ValueError:
            errors.append(f"{href}: resolves outside repository: {target}")
            continue

        if not target.exists():
            errors.append(f"{href}: missing target: {target.relative_to(ROOT)}")

    return errors


def main() -> int:
    errors = validate_links()
    if errors:
        print("Docs link validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Docs links validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
