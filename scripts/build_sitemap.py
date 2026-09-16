#!/usr/bin/env python3
"""Generate Google-compatible XML and text sitemaps from public canonical URLs."""

import argparse
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

BASE = "https://qiaoyx-or.github.io/production-decision-sandbox/"
NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []
        self.noindex = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "link" and values.get("rel") == "canonical":
            self.canonicals.append(values.get("href", ""))
        if tag == "meta" and values.get("name", "").lower() in {"robots", "googlebot"}:
            self.noindex |= "noindex" in values.get("content", "").lower()


def public_pages(root):
    pages = [root / relative for relative in ("index.html", "en/index.html", "sandbox/index.html", "en/sandbox/index.html")]
    for prefix in ("docs", "en/docs", "guide", "en/guide", "learn", "en/learn"):
        pages.extend(sorted((root / prefix).glob("*.html")))
    return pages


def build(root):
    urls = []
    for path in public_pages(root):
        metadata = Metadata()
        metadata.feed(path.read_text(encoding="utf-8"))
        if len(metadata.canonicals) != 1 or metadata.noindex:
            raise ValueError(f"Expected one indexable canonical URL: {path.relative_to(root)}")
        url = metadata.canonicals[0]
        relative = path.relative_to(root).as_posix()
        expected = BASE + (relative[:-10] if relative.endswith("index.html") else relative)
        parsed = urlsplit(url)
        if url != expected or parsed.query or parsed.fragment:
            raise ValueError(f"Canonical URL does not match its public path: {relative}")
        urls.append(url)
    if len(urls) != len(set(urls)):
        raise ValueError("Duplicate canonical URL in sitemap")
    ET.register_namespace("", NAMESPACE)
    element = ET.Element(f"{{{NAMESPACE}}}urlset")
    for url in urls:
        entry = ET.SubElement(element, f"{{{NAMESPACE}}}url")
        ET.SubElement(entry, f"{{{NAMESPACE}}}loc").text = url
    # lastmod is optional. Build time does not establish a content-modification date.
    ET.indent(element, space="  ")
    body = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(element, encoding="unicode") + "\n"
    (root / "sitemap.xml").write_text(body, encoding="utf-8", newline="\n")
    (root / "sitemap.txt").write_text("\n".join(urls) + "\n", encoding="utf-8", newline="\n")
    return urls


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    print(f"Built XML and text sitemaps for {len(build(parser.parse_args().project_root))} canonical URLs.")
