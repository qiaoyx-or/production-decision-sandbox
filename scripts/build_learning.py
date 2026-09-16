#!/usr/bin/env python3
"""Build the bilingual learning center and export its reviewed Markdown to Wiki."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

BASE_URL = "https://qiaoyx-or.github.io/production-decision-sandbox"
WIKI_URL = "https://github.com/qiaoyx-or/decisioworks/wiki"
ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"\]\(([^)]+)\)")


def page_info(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    zh = path.stem.endswith("-zh-CN")
    slug = path.stem.removesuffix("-zh-CN")
    title = text.splitlines()[0].removeprefix("# ").strip()
    if not title or not text.startswith("# "):
        raise ValueError(f"Missing title: {path.name}")
    body = re.sub(r"\A# [^\n]+\n+[^\n]+\n+", "", text, count=1)
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    first = next((p for p in paragraphs if not p.startswith(("#", "|", "-", ">"))), title)
    description = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", first)
    description = re.sub(r"[*\x60]", "", description).replace("\n", " ")
    lesson = re.match(r"Learning-([A-H][1-3])-", slug)
    topic = re.match(r"Learning-Topic-([A-H])-", slug)
    return {
        "source": path.name, "slug": slug, "language": "zh-CN" if zh else "en",
        "title": title, "description": description,
        "kind": "center" if slug == "Learning-Center" else "topic" if topic else "lesson" if lesson else "worksheet",
        "topic": lesson.group(1)[0] if lesson else topic.group(1) if topic else None,
        "id": lesson.group(1) if lesson else None, "body": body,
        "file": "index.html" if slug == "Learning-Center" else slug + ".html",
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def inventory(root: Path) -> list[dict]:
    pages = [page_info(p) for p in sorted((root / "content/learning").glob("*.md"))]
    if len(pages) != 74:
        raise ValueError(f"Expected 74 reviewed pages, found {len(pages)}")
    for language in ("zh-CN", "en"):
        selected = [p for p in pages if p["language"] == language]
        counts = {kind: sum(p["kind"] == kind for p in selected) for kind in ("center", "topic", "lesson", "worksheet")}
        if counts != {"center": 1, "topic": 8, "lesson": 24, "worksheet": 4}:
            raise ValueError(f"Incomplete {language} inventory: {counts}")
    return pages


def local_href(target: dict, language: str) -> str:
    prefix = "./" if target["language"] == language else "../en/learn/" if language == "zh-CN" else "../../learn/"
    return prefix + ("" if target["file"] == "index.html" else target["file"])


def page_url(page: dict) -> str:
    prefix = "learn" if page["language"] == "zh-CN" else "en/learn"
    return f"{BASE_URL}/{prefix}/" + ("" if page["file"] == "index.html" else page["file"])


def render_body(page: dict, pages: list[dict]) -> str:
    result = subprocess.run(["pandoc", "--from=gfm", "--to=html5"], input=page["body"],
                            text=True, capture_output=True, check=True).stdout.strip()
    lookup = {p["source"]: p for p in pages}
    def rewrite(match):
        raw = html.unescape(match.group(1))
        url = urlsplit(raw)
        if url.scheme or url.netloc or not url.path:
            return match.group(0)
        name = unquote(url.path)
        if name not in lookup:
            raise ValueError(f"Unknown local learning link: {page['source']}: {raw}")
        href = local_href(lookup[name], page["language"])
        if url.fragment:
            href += "#" + url.fragment
        return 'href="' + html.escape(href, quote=True) + '"'
    result = re.sub(r'href="([^"]+)"', rewrite, result)
    # Keep wide field tables readable without making the page itself scroll sideways.
    result = re.sub(r"<table>", '<div class="table-scroll" role="region" tabindex="0" aria-label="' +
                    ("数据表" if page["language"] == "zh-CN" else "Data table") + '"><table>', result)
    return result.replace("</table>", "</table></div>")


def template(page: dict, pages: list[dict]) -> str:
    zh = page["language"] == "zh-CN"
    language = page["language"]
    label = lambda cn, en: cn if zh else en
    root = "../" if zh else "../../"
    home = "../"
    other = next(p for p in pages if p["slug"] == page["slug"] and p["language"] != language)
    translated = {p["language"]: page_url(p) for p in (page, other)}
    selected = [p for p in pages if p["language"] == language]
    topics = [p for p in selected if p["kind"] == "topic"]
    active_topic = next((p for p in topics if p["topic"] == page["topic"]), None)
    links = []
    for topic in topics:
        current = ' aria-current="page"' if topic["slug"] == page["slug"] else ""
        links.append(f'<a href="{local_href(topic, language)}"{current}>{html.escape(topic["title"])}</a>')
        if active_topic == topic:
            for lesson in selected:
                if lesson["kind"] == "lesson" and lesson["topic"] == topic["topic"]:
                    current = ' aria-current="page"' if lesson["slug"] == page["slug"] else ""
                    links.append(f'<a class="lesson-link" href="{local_href(lesson, language)}"{current}>{html.escape(lesson["title"])}</a>')
    sidebar = '<a class="contents-home" href="./">' + label("学习中心", "Learning Center") + '</a>' + "".join(links)
    sidebar += '<span class="nav-section">' + label("工作表", "Worksheets") + "</span>"
    sidebar += "".join(f'<a href="{local_href(p, language)}">' + html.escape(p["title"].split("：")[-1].removeprefix("Worksheet: ")) + "</a>" for p in selected if p["kind"] == "worksheet")
    body = render_body(page, pages)
    headings = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body, re.S)
    toc = "".join(f'<a href="#{anchor}">{re.sub("<[^>]+>", "", text)}</a>' for anchor, text in headings)
    breadcrumbs = [(label("首页", "Home"), BASE_URL + ("/" if zh else "/en/")),
                   (label("学习中心", "Learning Center"), BASE_URL + ("/learn/" if zh else "/en/learn/"))]
    if active_topic and page["kind"] != "topic":
        breadcrumbs.append((active_topic["title"], page_url(active_topic)))
    if page["kind"] != "center":
        breadcrumbs.append((page["title"], page_url(page)))
    structured = {
        "@context": "https://schema.org", "@graph": [
            {"@type": "CollectionPage" if page["kind"] in {"center", "topic"} else "TechArticle",
             "headline": page["title"], "description": page["description"], "url": page_url(page),
             "inLanguage": language, "author": {"@type": "Organization", "name": "DecisioWorks", "url": BASE_URL + "/"}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": name, "item": url}
                for i, (name, url) in enumerate(breadcrumbs)]}
        ]}
    crumb = f'<a href="{home}">{label("首页", "Home")}</a><span>/</span>'
    crumb += f'<a href="./">{label("学习中心", "Learning Center")}</a>'
    if active_topic and page["kind"] != "topic":
        crumb += f'<span>/</span><a href="{local_href(active_topic, language)}">{active_topic["topic"]}</a>'
    if page["kind"] != "center":
        crumb += f'<span>/</span><span aria-current="page">{html.escape(page["title"])}</span>'
    image = BASE_URL + "/assets/decisioworks-project-layers" + ("" if zh else "-en") + ".png"
    title = html.escape(page["title"] + " | DecisioWorks")
    description = html.escape(page["description"], quote=True)
    kind = {"center": label("学习路径", "Learning paths"), "topic": label("专题", "Topic"),
            "lesson": label("课程", "Lesson"), "worksheet": label("工作表", "Worksheet")}[page["kind"]]
    return f'''<!doctype html>
<html lang="{language}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <link rel="canonical" href="{page_url(page)}" />
  <link rel="alternate" hreflang="zh-CN" href="{translated['zh-CN']}" />
  <link rel="alternate" hreflang="en" href="{translated['en']}" />
  <link rel="alternate" hreflang="x-default" href="{translated['zh-CN']}" />
  <meta property="og:type" content="{'website' if page['kind'] == 'center' else 'article'}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{page_url(page)}" />
  <meta property="og:image" content="{image}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{description}" />
  <meta name="twitter:image" content="{image}" />
  <link rel="icon" href="{root}assets/decisioworks-logo.png" />
  <link rel="stylesheet" href="./styles.css" />
  <script type="application/ld+json">{json.dumps(structured, ensure_ascii=False).replace('<', '&lt;')}</script>
</head>
<body>
  <a class="skip-link" href="#article">{label("跳到正文", "Skip to content")}</a>
  <header class="learning-header"><div class="shell header-inner">
    <a class="brand" href="{home}"><img src="{root}assets/decisioworks-logo.png" alt="" width="36" height="36" /><strong>DecisioWorks</strong></a>
    <nav aria-label="{label('主导航', 'Main navigation')}">
      <a href="{home}">{label("主页", "Home")}</a>
      <a href="../docs/">{label("文档", "Docs")}</a>
      <a class="language-switch" href="{local_href(other, language)}" lang="{other['language']}" hreflang="{other['language']}">{label("English", "中文")}</a>
    </nav>
  </div></header>
  <div class="shell breadcrumbs" aria-label="{label('面包屑导航', 'Breadcrumb')}">{crumb}</div>
  <div class="shell reading-layout">
    <aside class="sidebar"><nav aria-label="{label('课程目录', 'Course contents')}">{sidebar}</nav></aside>
    <main>
      <details class="mobile-contents"><summary>{label("课程目录", "Course contents")}</summary><nav aria-label="{label('移动端课程目录', 'Mobile course contents')}">{sidebar}</nav></details>
      <article id="article">
        <header class="article-heading"><p class="kicker">{kind}</p><h1>{html.escape(page["title"])}</h1></header>
        <details class="page-contents"><summary>{label("本页内容", "On this page")}</summary><nav>{toc}</nav></details>
        {body}
      </article>
      <footer class="article-footer"><a href="./">{label("返回学习中心", "Back to Learning Center")}</a><a href="{WIKI_URL}/{page['source'][:-3]}">{label("在 Wiki 阅读", "Read on Wiki")}</a></footer>
    </main>
  </div>
  <footer class="site-footer shell"><strong>DecisioWorks</strong><span>{label("从生产问题出发，理解与使用决策能力。", "Learn decision capabilities through production problems.")}</span></footer>
</body>
</html>
'''


def update_sitemap(root: Path, pages: list[dict]) -> None:
    from build_sitemap import build as build_sitemap
    build_sitemap(root)


def export_wiki(root: Path, destination: Path) -> None:
    pages = inventory(root)
    names = {p["source"] for p in pages}
    destination.mkdir(parents=True, exist_ok=True)
    for page in pages:
        def rewrite(match):
            target = urlsplit(match.group(1))
            if not target.scheme and not target.netloc and target.path in names:
                return "](" + target.path[:-3] + ("#" + target.fragment if target.fragment else "") + ")"
            return match.group(0)
        text = (root / "content/learning" / page["source"]).read_text(encoding="utf-8-sig")
        (destination / page["source"]).write_text(MARKDOWN_LINK.sub(rewrite, text), encoding="utf-8")


def build(root: Path, source: Path | None = None, wiki: Path | None = None) -> None:
    if source:
        target = root / "content/learning"
        target.mkdir(parents=True, exist_ok=True)
        for path in source.glob("*.md"):
            if not path.name.startswith("Learning-Home-Entry"):
                (target / path.name).write_text(path.read_text(encoding="utf-8-sig"), encoding="utf-8", newline="\n")
    pages = inventory(root)
    for page in pages:
        directory = root / ("learn" if page["language"] == "zh-CN" else "en/learn")
        directory.mkdir(parents=True, exist_ok=True)
        (directory / page["file"]).write_text(template(page, pages), encoding="utf-8")
        shutil.copy2(root / "scripts/learning.css", directory / "styles.css")
    manifest = [{k: p[k] for k in ("source", "slug", "language", "kind", "topic", "id", "file", "sha256")} for p in pages]
    (root / "content/learning/manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    update_sitemap(root, pages)
    if wiki:
        export_wiki(root, wiki)
    print(f"Built {len(pages)} learning pages (37 per language).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--sync-from", type=Path, help="Reviewed public Markdown directory")
    parser.add_argument("--wiki-output", type=Path, help="Explicit Wiki export directory")
    args = parser.parse_args()
    build(args.project_root.resolve(), args.sync_from, args.wiki_output)
