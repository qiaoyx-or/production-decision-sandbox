"""Regression checks for the static bilingual customer guides."""

import json
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

from test_static_site import PageParser, local_target

ROOT = Path(__file__).resolve().parents[1]
SLUGS = ("index", "stamping", "injection-molding", "partners")


class GuideTests(unittest.TestCase):
    def test_bilingual_structure_and_numbers(self):
        zh, en = [json.loads((ROOT / "content/guides" / f"{lang}.json").read_text(encoding="utf-8")) for lang in ("zh-CN", "en")]
        self.assertEqual(set(zh["pages"]), set(SLUGS))
        self.assertEqual(set(en["pages"]), set(SLUGS))
        for slug in SLUGS:
            left, right = zh["pages"][slug]["sections"], en["pages"][slug]["sections"]
            self.assertEqual([s["id"] for s in left], [s["id"] for s in right])
            for a, b in zip(left, right):
                self.assertEqual([x["type"] for x in a["blocks"]], [x["type"] for x in b["blocks"]])
                for x, y in zip(a["blocks"], b["blocks"]):
                    if x["type"] == "table":
                        self.assertEqual(len(x["rows"]), len(y["rows"]))
                        numbers = lambda v: re.findall(r"-?\d[\d,.]*%?", json.dumps(v, ensure_ascii=False))
                        self.assertEqual(numbers(x["rows"]), numbers(y["rows"]), (slug, a["id"]))

    def test_static_pages_and_fragments(self):
        for language in ("", "en/"):
            for slug in SLUGS:
                page = ROOT / language / "guide" / f"{slug}.html"
                source = page.read_text(encoding="utf-8")
                parsed = PageParser()
                parsed.feed(source)
                self.assertNotRegex(source, r"<(?:form|input|button|iframe)\b")
                self.assertNotRegex(source, r"<script\s+src=")
                for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S):
                    self.assertEqual(json.loads(block)["@type"], "TechArticle")
                for _, url in parsed.links:
                    parts = urlsplit(url)
                    if parts.scheme or parts.netloc:
                        continue
                    target = page if url.startswith("#") else local_target(ROOT, page, url)
                    self.assertTrue(target and target.exists(), (page, url))
                    if parts.fragment and target.suffix == ".html":
                        target_parser = PageParser()
                        target_parser.feed(target.read_text(encoding="utf-8"))
                        self.assertIn(unquote(parts.fragment), target_parser.ids, (page, url))
                self.assertNotIn("/home/qiaoyx", source)
                self.assertNotIn("D:\\workspace", source)
                if language:
                    visible = re.sub(r"<[^>]+>", "", source)
                    self.assertEqual(set(re.findall(r"[\u4e00-\u9fff]", visible)), set("中文"))

    def test_home_sections_preserved(self):
        expected = ["capability", "architecture", "sandbox-preview", "examples", "ecosystem", "whitepapers", "editions", "contact"]
        for relative in ("index.html", "en/index.html"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertEqual(re.findall(r'<section[^>]* id="([^"]+)"', text), expected)
            self.assertIn("assets/guide/brand-hero.png", text)
            self.assertIn('href="./guide/"', text)
            self.assertIn('href="./sandbox/"', text)

    def test_sitemap_routes(self):
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [n.text for n in ET.parse(ROOT / "sitemap.xml").findall(".//s:loc", ns)]
        self.assertEqual(len(urls), len(set(urls)))
        for prefix in ("guide", "en/guide"):
            for slug in SLUGS:
                suffix = "" if slug == "index" else f"{slug}.html"
                self.assertTrue(any(u.endswith(f"/{prefix}/{suffix}") for u in urls))


if __name__ == "__main__":
    unittest.main()
