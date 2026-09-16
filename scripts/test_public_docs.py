#!/usr/bin/env python3
"""Check public Markdown hygiene and synchronization with generated documents."""
from pathlib import Path
import re
import shutil
import subprocess
import unittest
from urllib.parse import unquote, urlsplit

import build_docs


ROOT = Path(__file__).resolve().parents[1]
INTERNAL = {"DESIGN.md", "GITHUB_PAGES_DESIGN.md", "docs/V0.2_SERVICE_SCOPE.md"}
EXCLUDED_DIRS = {".git", "node_modules", "__pycache__", ".venv", "dist"}
EDITORIAL = (
    "转化型能力", "转化漏斗", "V0.2 规划重点", "V0.2 模块边界",
    "本轮没有生成截图", "待补截图", "页面复现时还发现", "已写入验证记录",
    "public conversion funnel", "the ui reproduction also exposed",
)
PRIVATE_PATTERNS = {
    "personal Linux home": re.compile(r"/home/(?!<|path(?:/|$))[A-Za-z0-9_.-]+/"),
    "personal Windows home": re.compile(r"[A-Za-z]:[\\/]Users[\\/](?!<)[^\\/\s]+[\\/]", re.I),
    "workspace drive": re.compile(r"[A-Za-z]:[\\/]workspace[\\/]", re.I),
    "private key block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |ENCRYPTED )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})"),
}


def public_markdown():
    return sorted(
        p for p in ROOT.rglob("*.md")
        if not EXCLUDED_DIRS.intersection(p.relative_to(ROOT).parts)
        and p.relative_to(ROOT).as_posix() not in INTERNAL
    )


class PublicDocumentationTests(unittest.TestCase):
    def test_public_copy_has_no_known_editorial_or_private_material(self):
        for path in public_markdown():
            text = path.read_text(encoding="utf-8-sig")
            with self.subTest(document=path.relative_to(ROOT)):
                for marker in EDITORIAL:
                    self.assertNotIn(marker.casefold(), text.casefold())
                for label, pattern in PRIVATE_PATTERNS.items():
                    self.assertIsNone(pattern.search(text), label)

    def test_internal_plans_remain_excluded(self):
        rules = set(ROOT.joinpath(".gitignore").read_text(encoding="utf-8").splitlines())
        for rel in INTERNAL:
            self.assertIn("/" + rel, rules)
        if (ROOT / ".git").exists():
            tracked = subprocess.check_output(
                ["git", "-C", str(ROOT), "ls-files", "--", *sorted(INTERNAL)], text=True
            )
            self.assertEqual(tracked.strip(), "", "Internal plans must remain untracked")
        public_text = "\n".join(
            p.read_text(encoding="utf-8-sig") for p in public_markdown()
        )
        for rel in INTERNAL:
            self.assertNotIn(rel, public_text, "Public docs link to an internal plan")

    def test_repository_document_links(self):
        for path in public_markdown():
            # Wiki-style article/image links are resolved by build_docs and
            # checked in the generated HTML by test_static_site.py.
            if path.is_relative_to(ROOT / "content" / "docs"):
                continue
            for href in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8-sig")):
                parts = urlsplit(href)
                if parts.scheme or parts.netloc or not parts.path:
                    continue
                target = (path.parent / unquote(parts.path)).resolve()
                with self.subTest(document=path.relative_to(ROOT), link=href):
                    self.assertTrue(target.is_relative_to(ROOT), "Link escapes repository")
                    self.assertTrue(target.exists(), "Missing linked document")

    def test_bilingual_document_inventory(self):
        expected = {item["slug"] + ".md" for item in build_docs.ARTICLES}
        for language in ("en", "zh-CN"):
            self.assertEqual(
                {p.name for p in (ROOT / "content" / "docs" / language).glob("*.md")}, expected
            )

    def test_generated_documents_match_sources(self):
        self.assertIsNotNone(shutil.which("pandoc"), "Pandoc is required for document synchronization checks")
        selected = {item["slug"] for item in build_docs.ARTICLES}
        for language, source_dir, output_dir in (
            ("zh", "content/docs/zh-CN", "docs"),
            ("en", "content/docs/en", "en/docs"),
        ):
            self.assertEqual(
                ROOT.joinpath(output_dir, "index.html").read_text(encoding="utf-8"),
                build_docs.index_template(language),
            )
            for article in build_docs.ARTICLES:
                with self.subTest(language=language, article=article["slug"]):
                    source = ROOT / source_dir / (article["slug"] + ".md")
                    body = build_docs.rewrite_links(build_docs.render_markdown(source), language, selected)
                    expected = build_docs.article_template(article, language, body)
                    actual = ROOT.joinpath(output_dir, article["slug"] + ".html").read_text(encoding="utf-8")
                    self.assertEqual(actual, expected, "Rebuild the document center after editing Markdown")


if __name__ == "__main__":
    unittest.main()
