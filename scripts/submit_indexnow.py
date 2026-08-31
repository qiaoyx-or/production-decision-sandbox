#!/usr/bin/env python3
"""Notify IndexNow about public HTML URLs changed by a Git revision range."""

from __future__ import annotations

import argparse
import json
import subprocess
import urllib.request
from pathlib import Path


BASE_URL = "https://qiaoyx-or.github.io/production-decision-sandbox"
HOST = "qiaoyx-or.github.io"
ENDPOINT = "https://api.indexnow.org/indexnow"


def public_url(path: str) -> str | None:
    normalized = path.replace("\\", "/").lstrip("./")
    if normalized == "index.html":
        return f"{BASE_URL}/"
    if normalized.endswith("/index.html"):
        return f"{BASE_URL}/{normalized[:-10]}"
    if normalized.endswith(".html") and (
        normalized.startswith("docs/") or normalized.startswith("en/docs/")
    ):
        return f"{BASE_URL}/{normalized}"
    return None


def changed_urls(root: Path, base: str, head: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACDMRT", base, head, "--", "*.html"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return sorted({url for name in result.stdout.splitlines() if (url := public_url(name))})


def sitemap_urls(root: Path) -> list[str]:
    import xml.etree.ElementTree as ET

    tree = ET.parse(root / "sitemap.xml")
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [node.text.strip() for node in tree.findall("sm:url/sm:loc", namespace) if node.text]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--base")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--all", action="store_true", help="Submit every canonical URL in sitemap.xml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    key_files = sorted(root.glob("*.txt"))
    key_files = [path for path in key_files if path.stem.isalnum() and 8 <= len(path.stem) <= 128 and path.read_text(encoding="utf-8").strip() == path.stem]
    if len(key_files) != 1:
        raise SystemExit("Expected exactly one IndexNow key file at the site root")
    key_file = key_files[0]

    if args.all:
        urls = sitemap_urls(root)
    elif args.base:
        urls = changed_urls(root, args.base, args.head)
    else:
        raise SystemExit("Provide --base <revision> or use --all")

    if not urls:
        print("IndexNow: no changed public HTML URLs")
        return

    payload = {
        "host": HOST,
        "key": key_file.stem,
        "keyLocation": f"{BASE_URL}/{key_file.name}",
        "urlList": urls,
    }
    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status not in {200, 202}:
            raise SystemExit(f"IndexNow rejected submission: HTTP {response.status}")
        print(f"IndexNow accepted {len(urls)} URL(s): HTTP {response.status}")


if __name__ == "__main__":
    main()
