#!/usr/bin/env python3
"""Build bilingual, JavaScript-free customer guides from curated content."""

import html
import json
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

BASE = "https://qiaoyx-or.github.io/production-decision-sandbox"
ROOT = Path(__file__).resolve().parents[1]
SLUGS = ("index", "stamping", "injection-molding", "partners")


def esc(value):
    return html.escape(str(value), quote=True)


def render_block(block, asset_root, language):
    kind = block["type"]
    if kind == "p":
        return f'<p>{esc(block["text"])}</p>'
    if kind == "note":
        return f'<aside class="evidence-note"><strong>{esc(block["title"])}</strong><p>{esc(block["text"])}</p></aside>'
    if kind == "list":
        return '<ul class="guide-list">' + "".join(f"<li>{esc(item)}</li>" for item in block["items"]) + "</ul>"
    if kind == "table":
        heads = "".join(f'<th scope="col">{esc(cell)}</th>' for cell in block["heads"])
        rows = "".join("<tr>" + "".join(
            f'<th scope="row">{esc(cell)}</th>' if i == 0 else f"<td>{esc(cell)}</td>"
            for i, cell in enumerate(row)) + "</tr>" for row in block["rows"])
        return f'<div class="table-scroll" tabindex="0" role="region" aria-label="{esc(block["caption"])}"><table><caption>{esc(block["caption"])}</caption><thead><tr>{heads}</tr></thead><tbody>{rows}</tbody></table></div>'
    if kind == "figure":
        src = f'{asset_root}assets/guide/{block["file"]}'
        zoom = "查看原图" if language == "zh-CN" else "Open full-size image"
        return f'<figure class="guide-figure"><a href="{src}" target="_blank" rel="noreferrer" aria-label="{zoom}: {esc(block["alt"])}"><img src="{src}" width="{block["width"]}" height="{block["height"]}" loading="lazy" decoding="async" alt="{esc(block["alt"])}"></a><figcaption>{esc(block["caption"])} <a href="{src}" target="_blank" rel="noreferrer">{zoom} ↗</a></figcaption></figure>'
    if kind == "links":
        return '<div class="reading-links">' + "".join(f'<a href="{esc(item["href"])}"><strong>{esc(item["title"])}</strong><span>{esc(item["text"])}</span><b aria-hidden="true">→</b></a>' for item in block["items"]) + "</div>"
    raise ValueError(f"Unknown block type: {kind}")


def build():
    for language in ("zh-CN", "en"):
        data = json.loads((ROOT / "content" / "guides" / f"{language}.json").read_text(encoding="utf-8"))
        zh = language == "zh-CN"
        asset_root = "../" if zh else "../../"
        home = "../"
        folder = ROOT / ("guide" if zh else "en/guide")
        folder.mkdir(parents=True, exist_ok=True)
        labels = data["labels"]
        for slug in SLUGS:
            page = data["pages"][slug]
            suffix = "" if slug == "index" else f"{slug}.html"
            zh_url, en_url = f"{BASE}/guide/{suffix}", f"{BASE}/en/guide/{suffix}"
            canonical = zh_url if zh else en_url
            other = f"../en/guide/{suffix}" if zh else f"../../guide/{suffix}"
            title = f'{page["title"]} | DecisioWorks'
            navigation = ""
            for item in SLUGS:
                target = "" if item == "index" else item + ".html"
                current = ' aria-current="page"' if item == slug else ""
                navigation += f'<a href="./{target}"{current}>{esc(data["pages"][item]["short"])}</a>'
            toc = "".join(f'<a href="#{section["id"]}">{esc(section["title"])}</a>' for section in page["sections"])
            sections = "".join(f'<section id="{section["id"]}" class="guide-section"><h2>{esc(section["title"])}</h2>' + "".join(render_block(b, asset_root, language) for b in section["blocks"]) + "</section>" for section in page["sections"])
            schema = {
                "@context": "https://schema.org", "@type": "TechArticle",
                "headline": page["title"], "description": page["intro"],
                "inLanguage": language, "url": canonical,
                "isPartOf": {"@type": "WebSite", "name": "DecisioWorks", "url": BASE + "/"}
            }
            markup = f'''<!doctype html>
<html lang="{language}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(page["intro"])}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="zh-CN" href="{zh_url}">
  <link rel="alternate" hreflang="en" href="{en_url}">
  <link rel="alternate" hreflang="x-default" href="{zh_url}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(page["intro"])}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{BASE}/assets/guide/brand-hero.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(page["intro"])}">
  <meta name="twitter:image" content="{BASE}/assets/guide/brand-hero.png">
  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
  <link rel="icon" href="{asset_root}assets/decisioworks-logo.png">
  <link rel="stylesheet" href="{asset_root}guide/styles.css?v=20260916">
</head>
<body>
  <a class="skip-link" href="#main">{esc(labels["skip"])}</a>
  <header class="guide-header"><div class="guide-shell header-row">
    <a class="guide-brand" href="{home}"><img src="{asset_root}assets/decisioworks-logo.png" width="36" height="36" alt=""><strong>DecisioWorks</strong></a>
    <nav aria-label="{esc(labels["mainnav"])}"><a href="{home}">{esc(labels["home"])}</a><a href="../docs/">{esc(labels["docs"])}</a><a class="language-link" href="{other}" lang="{"en" if zh else "zh-CN"}">{"EN" if zh else "中文"}</a></nav>
  </div></header>
  <main id="main">
    <div class="guide-shell">
      <nav class="guide-path" aria-label="{esc(labels["breadcrumb"])}"><a href="{home}">{esc(labels["home"])}</a><span aria-hidden="true">/</span><a href="./">{esc(labels["guide"])}</a></nav>
      <div class="guide-heading"><p class="eyebrow">{esc(page["eyebrow"])}</p><h1>{esc(page["title"])}</h1><p class="guide-intro">{esc(page["intro"])}</p><p class="record-label">{esc(page["context"])}</p></div>
      <nav class="guide-tabs" aria-label="{esc(labels["guidenav"])}">{navigation}</nav>
      <div class="guide-layout"><aside class="guide-toc"><strong>{esc(labels["onpage"])}</strong><nav aria-label="{esc(labels["onpage"])}">{toc}</nav></aside><article>{sections}<div class="guide-next"><a href="./">{esc(labels["back"])}</a><a href="../#whitepapers">{esc(labels["whitepapers"])} →</a></div></article></div>
    </div>
  </main>
  <footer class="guide-footer"><div class="guide-shell"><strong>DecisioWorks</strong><p>{esc(labels["footer"])}</p><a href="../#contact">{esc(labels["contact"])} →</a></div></footer>
</body>
</html>
'''
            (folder / f"{slug}.html").write_text(markup, encoding="utf-8", newline="\n")
    print("Built 8 static bilingual guide pages.")
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", namespace)
    sitemap = ET.parse(ROOT / "sitemap.xml")
    known = {node.text for node in sitemap.findall(f".//{{{namespace}}}loc")}
    for prefix in ("guide", "en/guide"):
        for slug in SLUGS:
            url = f'{BASE}/{prefix}/{"" if slug == "index" else slug + ".html"}'
            if url not in known:
                entry = ET.SubElement(sitemap.getroot(), f"{{{namespace}}}url")
                ET.SubElement(entry, f"{{{namespace}}}loc").text = url
                ET.SubElement(entry, f"{{{namespace}}}lastmod").text = date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', f'<urlset xmlns="{namespace}">']
    refreshed = {f"{BASE}/{suffix}" for suffix in ("", "en/", "sandbox/", "en/sandbox/")}
    for entry in sitemap.getroot():
        url = entry.find(f"{{{namespace}}}loc").text
        lastmod = entry.find(f"{{{namespace}}}lastmod").text
        if url in refreshed:
            lastmod = date.today().isoformat()
        lines.append(f"  <url><loc>{esc(url)}</loc><lastmod>{esc(lastmod)}</lastmod></url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    build()
