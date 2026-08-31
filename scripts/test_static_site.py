#!/usr/bin/env python3
"""Validate local links, resources, and essential metadata for the static Pages site."""

from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.ids: list[str] = []
        self.h1_count = 0
        self.title_count = 0
        self.description_count = 0
        self.canonical_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.links.append(("href", values["href"] or ""))
        if tag in {"img", "script"} and values.get("src"):
            self.links.append(("src", values["src"] or ""))
        if tag == "link" and values.get("href"):
            self.links.append(("href", values["href"] or ""))
        if values.get("id"):
            self.ids.append(values["id"] or "")
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.title_count += 1
        if tag == "meta" and values.get("name") == "description" and values.get("content"):
            self.description_count += 1
        if tag == "link" and values.get("rel") == "canonical" and values.get("href"):
            self.canonical_count += 1


def local_target(root: Path, page: Path, raw_url: str) -> Path | None:
    if not raw_url or raw_url.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None
    parsed = urlsplit(raw_url)
    if parsed.scheme or parsed.netloc:
        return None
    path = unquote(parsed.path)
    target = (root / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
    if not path or path.endswith("/"):
        target = target / "index.html"
    return target.resolve()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []
    pages = [
        root / "index.html",
        root / "en" / "index.html",
        root / "sandbox" / "index.html",
        root / "en" / "sandbox" / "index.html",
        *sorted((root / "docs").glob("*.html")),
        *sorted((root / "en" / "docs").glob("*.html")),
    ]
    for page in pages:
        if ".git" in page.parts:
            continue
        parsed = PageParser()
        parsed.feed(page.read_text(encoding="utf-8"))
        rel = page.relative_to(root)
        if parsed.title_count != 1:
            errors.append(f"{rel}: expected one title, found {parsed.title_count}")
        if parsed.description_count != 1:
            errors.append(f"{rel}: expected one meta description, found {parsed.description_count}")
        if parsed.canonical_count != 1:
            errors.append(f"{rel}: expected one canonical link, found {parsed.canonical_count}")
        if parsed.h1_count != 1:
            errors.append(f"{rel}: expected one h1, found {parsed.h1_count}")
        if page.parent.name == "docs" and page.name != "index.html":
            source_text = page.read_text(encoding="utf-8")
            if source_text.count('class="breadcrumbs"') != 1:
                errors.append(f"{rel}: expected one visible breadcrumb")
            if source_text.count('class="related-docs"') != 1:
                errors.append(f"{rel}: expected one related-documents section")
            related_match = re.search(r'<section class="related-docs">.*?<div>(.*?)</div></section>', source_text, re.S)
            if not related_match or related_match.group(1).count("<a ") != 3:
                errors.append(f"{rel}: expected three related-document links")
            json_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', source_text, re.S)
            try:
                structured_data = json.loads(json_match.group(1)) if json_match else None
            except json.JSONDecodeError as exc:
                errors.append(f"{rel}: invalid JSON-LD: {exc}")
            else:
                if not structured_data or structured_data.get("@type") != "BreadcrumbList":
                    errors.append(f"{rel}: missing BreadcrumbList JSON-LD")
                elif len(structured_data.get("itemListElement", [])) != 3:
                    errors.append(f"{rel}: expected three BreadcrumbList items")
        duplicates = sorted({item for item in parsed.ids if parsed.ids.count(item) > 1})
        if duplicates:
            errors.append(f"{rel}: duplicate ids {duplicates}")
        for attribute, raw_url in parsed.links:
            target = local_target(root, page, raw_url)
            if target and not target.exists():
                errors.append(f"{rel}: missing {attribute} target {raw_url}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"OK: validated metadata, structure, and local assets across {len(pages)} public HTML pages")


if __name__ == "__main__":
    main()
