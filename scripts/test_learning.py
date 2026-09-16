#!/usr/bin/env python3
"""Check bilingual learning content, generated pages, anchors and Wiki export."""

import json
import re
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

import build_learning as learning
from test_static_site import PageParser, local_target

ROOT = Path(__file__).resolve().parents[1]


class LearningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = learning.inventory(ROOT)
        cls.parsed = {}
        for page in cls.pages:
            path = ROOT / ("learn" if page["language"] == "zh-CN" else "en/learn") / page["file"]
            parser = PageParser()
            parser.feed(path.read_text(encoding="utf-8"))
            cls.parsed[path.resolve()] = parser

    def test_manifest_and_translation_pairs(self):
        manifest = json.loads((ROOT / "content/learning/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(manifest), 74)
        hashes = {item["source"]: item["sha256"] for item in manifest}
        for page in self.pages:
            self.assertEqual(hashes[page["source"]], page["sha256"])
            other = [p for p in self.pages if p["slug"] == page["slug"] and p["language"] != page["language"]]
            self.assertEqual(len(other), 1)
        self.assertFalse(any("Home-Entry" in item["source"] for item in manifest))

    def test_generated_pages_match_reviewed_content(self):
        for page in self.pages:
            path = ROOT / ("learn" if page["language"] == "zh-CN" else "en/learn") / page["file"]
            with self.subTest(page=page["source"]):
                self.assertEqual(path.read_text(encoding="utf-8"), learning.template(page, self.pages))
                self.assertEqual((path.parent / "styles.css").read_bytes(), (ROOT / "scripts/learning.css").read_bytes())

    def test_links_and_fragments(self):
        for path, parser in self.parsed.items():
            for _, raw in parser.links:
                url = urlsplit(raw)
                if url.scheme or url.netloc:
                    continue
                target = local_target(ROOT, path, raw) if url.path else path
                if target and target.suffix == ".html":
                    self.assertTrue(target.exists(), str(target))
                    if target not in self.parsed:
                        parsed = PageParser()
                        parsed.feed(target.read_text(encoding="utf-8"))
                    else:
                        parsed = self.parsed[target]
                    if url.fragment:
                        self.assertIn(unquote(url.fragment), parsed.ids, (str(path), raw))

    def test_language_link_is_reciprocal(self):
        for page in self.pages:
            path = ROOT / ("learn" if page["language"] == "zh-CN" else "en/learn") / page["file"]
            text = path.read_text(encoding="utf-8")
            other = next(p for p in self.pages if p["slug"] == page["slug"] and p["language"] != page["language"])
            self.assertIn(f'class="language-switch" href="{learning.local_href(other, page["language"])}"', text)

    def test_sitemap_contains_every_learning_url_once(self):
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [n.text for n in ET.parse(ROOT / "sitemap.xml").findall("sm:url/sm:loc", ns)]
        self.assertEqual(len(urls), len(set(urls)))
        for page in self.pages:
            self.assertEqual(urls.count(learning.page_url(page)), 1)

    def test_wiki_export_preserves_prose(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp)
            learning.export_wiki(ROOT, destination)
            self.assertEqual(len(list(destination.glob("*.md"))), 74)
            for page in self.pages:
                original = (ROOT / "content/learning" / page["source"]).read_text(encoding="utf-8-sig")
                exported = (destination / page["source"]).read_text(encoding="utf-8")
                self.assertEqual(re.sub(r"\]\([^)]+\)", "]()", original),
                                 re.sub(r"\]\([^)]+\)", "]()", exported))
                self.assertNotRegex(exported, r"\]\((?:Learning-|Worksheet-)[^)]+\.md\)")

    def test_learning_urls_are_in_indexnow_scope(self):
        from submit_indexnow import public_url
        for page in self.pages:
            prefix = "learn/" if page["language"] == "zh-CN" else "en/learn/"
            self.assertEqual(public_url(prefix + page["file"]), learning.page_url(page))
        for private_page in ("workbench/index.html", "apps/web/index.html", "draft.html"):
            self.assertIsNone(public_url(private_page))


if __name__ == "__main__":
    unittest.main()
