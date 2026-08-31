#!/usr/bin/env python3
"""Build the public DecisioWorks documentation center from curated Wiki sources."""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
from pathlib import Path


ARTICLES = [
    {
        "slug": "What-Is-DecisioWorks",
        "group": "overview",
        "zh_title": "DecisioWorks 是什么",
        "en_title": "What Is DecisioWorks",
        "zh_summary": "理解生产决策工具包的定位、核心能力与差异化价值。",
        "en_summary": "Understand the toolkit's positioning, core capabilities, and differentiated value.",
    },
    {
        "slug": "Scenarios-and-Pain-Points",
        "group": "overview",
        "zh_title": "生产决策场景与痛点",
        "en_title": "Production Decision Scenarios and Pain Points",
        "zh_summary": "从计划、排程、齐套、瓶颈与扰动响应理解制造企业的共同难题。",
        "en_summary": "Explore shared manufacturing challenges across planning, scheduling, readiness, bottlenecks, and disruptions.",
    },
    {
        "slug": "Architecture-Overview",
        "group": "overview",
        "zh_title": "DecisioWorks 架构概览",
        "en_title": "DecisioWorks Architecture Overview",
        "zh_summary": "梳理 DataSets、DecisioCore、GOCK 与 Web 的职责及协作关系。",
        "en_summary": "See how DataSets, DecisioCore, GOCK, and the Web layer work together.",
    },
    {
        "slug": "Standardized-Data-Interface",
        "group": "data",
        "zh_title": "标准化数据接口",
        "en_title": "Standardized Data Interface",
        "zh_summary": "把订单、工艺、产能、物料和时间关系转化为可计算业务结构。",
        "en_summary": "Turn orders, routes, capacity, materials, and time relationships into computable business structures.",
    },
    {
        "slug": "ERP-MES-Data-Mapping-Guide",
        "group": "data",
        "zh_title": "ERP/MES 数据映射指南",
        "en_title": "ERP/MES Data Mapping Guide",
        "zh_summary": "从来源字段走向统一语义、关系闭合与求解输入。",
        "en_summary": "Move from source fields to shared semantics, closed relationships, and solver inputs.",
    },
    {
        "slug": "Data-Readiness-and-Validation",
        "group": "data",
        "zh_title": "数据准备度与验证",
        "en_title": "Data Readiness and Validation",
        "zh_summary": "区分可读取、关系完整与可进入求解链路的不同阶段。",
        "en_summary": "Distinguish readable data, relationship integrity, and true solver readiness.",
    },
    {
        "slug": "Objectives-and-Rule-Control",
        "group": "decision",
        "zh_title": "目标与规则控制",
        "en_title": "Objectives and Rule Control",
        "zh_summary": "让交期、负荷、库存、切换和现场规则进入受控求解。",
        "en_summary": "Bring delivery, load, inventory, changeovers, and site rules into controlled solving.",
    },
    {
        "slug": "Planning-and-Scheduling-Overview",
        "group": "decision",
        "zh_title": "计划与排程概览",
        "en_title": "Planning and Scheduling Overview",
        "zh_summary": "理解主生产计划、任务释放和作业排程之间的职责分工。",
        "en_summary": "Understand the roles of master planning, task release, and job scheduling.",
    },
    {
        "slug": "Results-Evidence-and-Feedback",
        "group": "decision",
        "zh_title": "结果、证据与反馈",
        "en_title": "Results, Evidence, and Feedback",
        "zh_summary": "从汇总指标追溯到业务对象，并把偏差带入下一轮决策。",
        "en_summary": "Trace aggregate metrics to business objects and carry deviations into the next cycle.",
    },
    {
        "slug": "Stamping-Planning-Case-Walkthrough",
        "group": "case",
        "zh_title": "冲压计划案例",
        "en_title": "Stamping Planning Case Walkthrough",
        "zh_summary": "查看需求、产能、物料如何形成基线计划与调整结果。",
        "en_summary": "See how demand, capacity, and materials shape a baseline plan and adjusted result.",
    },
    {
        "slug": "Injection-Molding-Scheduling-Case-Walkthrough",
        "group": "case",
        "zh_title": "注塑排程案例",
        "en_title": "Injection-Molding Scheduling Case Walkthrough",
        "zh_summary": "展示设备、模具、班制、维护与切换约束下的真实排程过程。",
        "en_summary": "Follow a real scheduling flow with equipment, molds, shifts, maintenance, and changeovers.",
    },
    {
        "slug": "Research-and-Commercial-Editions",
        "group": "case",
        "zh_title": "研究版与商业版",
        "en_title": "Research and Commercial Editions",
        "zh_summary": "了解公开评估、场景验证与正式商业运行的适用范围。",
        "en_summary": "Understand the scope of public evaluation, scenario validation, and commercial operation.",
    },
]

GROUPS = {
    "zh": [
        ("overview", "认识 DecisioWorks", "从定位、行业问题与项目结构建立整体认识。"),
        ("data", "数据进入决策", "让来源数据形成一致、完整、可计算的业务表达。"),
        ("decision", "目标、计划与反馈", "把管理取舍、计划协同和结果证据组织起来。"),
        ("case", "案例与版本", "通过真实场景和版本边界理解使用方式。"),
    ],
    "en": [
        ("overview", "Understand DecisioWorks", "Build a complete view of the positioning, industry problems, and architecture."),
        ("data", "Bring Data into Decisions", "Turn source data into consistent, complete, and computable business representation."),
        ("decision", "Objectives, Planning, and Feedback", "Connect management trade-offs, planning coordination, and result evidence."),
        ("case", "Cases and Editions", "Understand practical use through real scenarios and clear edition boundaries."),
    ],
}

BASE_URL = "https://qiaoyx-or.github.io/production-decision-sandbox"
WIKI_URL = "https://github.com/qiaoyx-or/decisioworks/wiki"


def strip_wiki_language_line(text: str) -> str:
    lines = text.splitlines()
    if lines and (
        lines[0].startswith(("**English**", "**简体中文**", "**中文**", "[English]", "[简体中文]", "[中文]"))
        or ("English" in lines[0] and ("中文" in lines[0] or "zh-CN" in lines[0]))
    ):
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines.pop(0)
    return "\n".join(lines) + "\n"


def render_markdown(source: Path) -> str:
    text = strip_wiki_language_line(source.read_text(encoding="utf-8"))
    result = subprocess.run(
        ["pandoc", "--from=gfm", "--to=html5"],
        input=text,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout


def rewrite_links(body: str, language: str, selected: set[str]) -> str:
    def replace(match: re.Match[str]) -> str:
        href = html.unescape(match.group(1))
        if href.startswith(("http://", "https://", "mailto:", "#", "/")):
            return match.group(0)
        target, suffix = (href.split("#", 1) + [""])[:2]
        target = target.removesuffix(".md")
        bare = target.removesuffix("-zh-CN")
        if bare in selected:
            resolved = f"{bare}.html"
            if suffix:
                resolved += f"#{suffix}"
        else:
            resolved = f"{WIKI_URL}/{target}"
            if suffix:
                resolved += f"#{suffix}"
        return f'href="{html.escape(resolved, quote=True)}"'

    body = re.sub(r'href="([^"]+)"', replace, body)
    if language == "en":
        body = body.replace('src="assets/', 'src="assets/')
    return body


def article_template(article: dict[str, str], language: str, body: str) -> str:
    is_zh = language == "zh"
    title = article["zh_title" if is_zh else "en_title"]
    summary = article["zh_summary" if is_zh else "en_summary"]
    lang_code = "zh-CN" if is_zh else "en"
    root = "../" if is_zh else "../../"
    docs_home = "./"
    other_href = f"../en/docs/{article['slug']}.html" if is_zh else f"../../docs/{article['slug']}.html"
    other_label = "EN" if is_zh else "中"
    other_lang = "en" if is_zh else "zh-CN"
    canonical = f"{BASE_URL}/{'docs' if is_zh else 'en/docs'}/{article['slug']}.html"
    zh_url = f"{BASE_URL}/docs/{article['slug']}.html"
    en_url = f"{BASE_URL}/en/docs/{article['slug']}.html"
    back = "文档中心" if is_zh else "Documentation"
    home = "产品主页" if is_zh else "Product Home"
    wiki = "完整 Wiki" if is_zh else "Full Wiki"
    footer = "制造业生产决策工具包" if is_zh else "Manufacturing Production Decision Toolkit"
    return f'''<!doctype html>
<html lang="{lang_code}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{html.escape(summary, quote=True)}" />
  <meta name="theme-color" content="#f3f7fb" />
  <link rel="canonical" href="{canonical}" />
  <link rel="alternate" hreflang="zh-CN" href="{zh_url}" />
  <link rel="alternate" hreflang="en" href="{en_url}" />
  <link rel="alternate" hreflang="x-default" href="{zh_url}" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{html.escape(title, quote=True)} | DecisioWorks" />
  <meta property="og:description" content="{html.escape(summary, quote=True)}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{BASE_URL}/assets/decisioworks-project-layers{'-en' if not is_zh else ''}.png" />
  <title>{html.escape(title)} | DecisioWorks</title>
  <link rel="icon" href="{root}assets/decisioworks-logo.png" />
  <link rel="stylesheet" href="./styles.css?v=20260831-1" />
</head>
<body>
  <a class="skip-link" href="#article">{'跳到正文' if is_zh else 'Skip to article'}</a>
  <header class="docs-header">
    <div class="docs-shell docs-nav">
      <a class="docs-brand" href="{root}"><img src="{root}assets/decisioworks-logo.png" alt="" /><span><strong>DecisioWorks</strong><small>{footer}</small></span></a>
      <nav aria-label="{'文档导航' if is_zh else 'Documentation navigation'}">
        <a href="{docs_home}">{back}</a><a href="{root}">{home}</a><a href="{WIKI_URL}" target="_blank" rel="noreferrer">{wiki}</a><a href="{other_href}" lang="{other_lang}">{other_label}</a>
      </nav>
    </div>
  </header>
  <main class="docs-shell article-layout">
    <aside class="article-aside"><a href="./">← {back}</a><p>{summary}</p></aside>
    <article class="doc-article" id="article">{body}</article>
  </main>
  <footer class="docs-footer"><div class="docs-shell"><strong>DecisioWorks</strong><span>{footer}</span></div></footer>
</body>
</html>
'''


def index_template(language: str) -> str:
    is_zh = language == "zh"
    lang_code = "zh-CN" if is_zh else "en"
    root = "../" if is_zh else "../../"
    canonical = f"{BASE_URL}/{'docs' if is_zh else 'en/docs'}/"
    other = "../en/docs/" if is_zh else "../../docs/"
    title = "DecisioWorks 文档中心" if is_zh else "DecisioWorks Documentation"
    intro = "从行业问题、数据准备和决策机制进入真实案例，系统理解 DecisioWorks 的定位、方法与使用边界。" if is_zh else "Move from industry problems, data readiness, and decision mechanisms into real cases, with a structured view of DecisioWorks positioning, methods, and operating scope."
    cards = []
    for group, group_title, group_summary in GROUPS[language]:
        articles = [item for item in ARTICLES if item["group"] == group]
        card_html = "".join(
            f'''<a class="doc-card" href="{item['slug']}.html"><span>{html.escape(group_title)}</span><h3>{html.escape(item['zh_title' if is_zh else 'en_title'])}</h3><p>{html.escape(item['zh_summary' if is_zh else 'en_summary'])}</p><b>{'阅读文档' if is_zh else 'Read document'} →</b></a>'''
            for item in articles
        )
        cards.append(f'''<section class="doc-group"><div class="group-heading"><h2>{html.escape(group_title)}</h2><p>{html.escape(group_summary)}</p></div><div class="doc-grid">{card_html}</div></section>''')
    zh_url = f"{BASE_URL}/docs/"
    en_url = f"{BASE_URL}/en/docs/"
    return f'''<!doctype html>
<html lang="{lang_code}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{html.escape(intro, quote=True)}" />
  <meta name="theme-color" content="#f3f7fb" />
  <link rel="canonical" href="{canonical}" />
  <link rel="alternate" hreflang="zh-CN" href="{zh_url}" />
  <link rel="alternate" hreflang="en" href="{en_url}" />
  <link rel="alternate" hreflang="x-default" href="{zh_url}" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{html.escape(intro, quote=True)}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{BASE_URL}/assets/decisioworks-project-layers{'-en' if not is_zh else ''}.png" />
  <title>{title}</title>
  <link rel="icon" href="{root}assets/decisioworks-logo.png" />
  <link rel="stylesheet" href="./styles.css?v=20260831-1" />
</head>
<body>
  <a class="skip-link" href="#main">{'跳到主要内容' if is_zh else 'Skip to main content'}</a>
  <header class="docs-header"><div class="docs-shell docs-nav"><a class="docs-brand" href="{root}"><img src="{root}assets/decisioworks-logo.png" alt="" /><span><strong>DecisioWorks</strong><small>{'生产决策工具包' if is_zh else 'Production Decision Toolkit'}</small></span></a><nav><a href="{root}">{'产品主页' if is_zh else 'Product Home'}</a><a href="{WIKI_URL}" target="_blank" rel="noreferrer">{'完整 Wiki' if is_zh else 'Full Wiki'}</a><a href="{other}" lang="{'en' if is_zh else 'zh-CN'}">{'EN' if is_zh else '中'}</a></nav></div></header>
  <main id="main">
    <section class="docs-hero"><div class="docs-shell"><p class="eyebrow">DECISIOWORKS DOCUMENTATION</p><h1>{title}</h1><p>{intro}</p><dl><div><dt>12</dt><dd>{'核心专题' if is_zh else 'Core topics'}</dd></div><div><dt>2</dt><dd>{'真实案例' if is_zh else 'Real cases'}</dd></div><div><dt>中 / EN</dt><dd>{'双语文档' if is_zh else 'Bilingual docs'}</dd></div></dl></div></section>
    <div class="docs-shell groups">{''.join(cards)}</div>
    <section class="docs-cta"><div class="docs-shell"><div><h2>{'需要更完整的技术参考？' if is_zh else 'Need the complete technical reference?'}</h2><p>{'GitHub Wiki 包含完整架构、字段、运行、集成和支持文档。' if is_zh else 'The GitHub Wiki contains the complete architecture, field, runtime, integration, and support documentation.'}</p></div><a href="{WIKI_URL}" target="_blank" rel="noreferrer">{'打开完整 Wiki' if is_zh else 'Open full Wiki'} →</a></div></section>
  </main>
  <footer class="docs-footer"><div class="docs-shell"><strong>DecisioWorks</strong><span>{'制造业生产决策工具包' if is_zh else 'Manufacturing Production Decision Toolkit'}</span></div></footer>
</body>
</html>
'''


CSS = r''':root{color-scheme:light;--ink:#10233d;--muted:#526985;--line:#cbd8e8;--surface:#fff;--canvas:#f3f7fb;--navy:#0c2743;--blue:#2468dc;--cyan:#0aaec7;--green:#079b70;--orange:#e18108;--purple:#7254d6;--shadow:0 16px 38px rgba(14,40,69,.08);font-family:Inter,"Segoe UI","Microsoft YaHei",system-ui,sans-serif}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--ink);background:var(--canvas);letter-spacing:0}a{color:inherit;text-decoration:none}img{display:block;max-width:100%}.docs-shell{width:min(1160px,calc(100% - 48px));margin:0 auto}.skip-link{position:fixed;left:16px;top:-60px;z-index:99;padding:10px 14px;background:#fff;border:1px solid var(--line)}.skip-link:focus{top:12px}.docs-header{position:sticky;top:0;z-index:20;background:rgba(243,247,251,.97);border-bottom:1px solid rgba(153,174,198,.5);backdrop-filter:blur(12px)}.docs-nav{min-height:70px;display:flex;align-items:center;justify-content:space-between;gap:28px}.docs-brand{display:inline-flex;align-items:center;gap:11px}.docs-brand img{width:38px;height:38px;border-radius:50%}.docs-brand span{display:grid;line-height:1.08}.docs-brand strong{font-size:17px}.docs-brand small{margin-top:5px;color:var(--muted);font-size:11px}.docs-nav nav{display:flex;align-items:center;gap:24px;color:#314a68;font-size:14px;font-weight:700}.docs-nav nav a:hover{color:var(--blue)}.eyebrow{margin:0 0 18px;color:var(--cyan);font-size:12px;font-weight:800;letter-spacing:.12em}.docs-hero{padding:90px 0 76px;color:#fff;background:var(--navy);border-bottom:7px solid var(--cyan)}.docs-hero h1{max-width:900px;margin:0;font-size:clamp(44px,6vw,74px);line-height:1.08}.docs-hero>div>p:last-of-type{max-width:820px;margin:24px 0 0;color:#c2d2e1;font-size:18px;line-height:1.8}.docs-hero dl{display:flex;width:fit-content;margin:36px 0 0;border:1px solid rgba(255,255,255,.2)}.docs-hero dl div{min-width:145px;padding:14px 18px;border-right:1px solid rgba(255,255,255,.2)}.docs-hero dl div:last-child{border-right:0}.docs-hero dt{font-size:21px;font-weight:800}.docs-hero dd{margin:5px 0 0;color:#a9bfd2;font-size:11px}.groups{padding:76px 0 90px}.doc-group{display:grid;grid-template-columns:270px 1fr;gap:46px;padding:44px 0;border-bottom:1px solid var(--line)}.doc-group:first-child{padding-top:0}.group-heading h2{margin:0;font-size:28px}.group-heading p{margin:14px 0 0;color:var(--muted);font-size:14px;line-height:1.75}.doc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.doc-card{display:flex;min-height:250px;flex-direction:column;padding:23px;background:#fff;border:1px solid var(--line);border-top:4px solid var(--blue);border-radius:5px;box-shadow:0 8px 20px rgba(21,49,80,.04);transition:transform .18s ease,border-color .18s ease}.doc-card:hover{transform:translateY(-3px);border-color:#8eacd0}.doc-card>span{color:var(--blue);font-size:10px;font-weight:800}.doc-card h3{margin:35px 0 13px;font-size:20px;line-height:1.35}.doc-card p{margin:0;color:var(--muted);font-size:13px;line-height:1.7}.doc-card b{margin-top:auto;padding-top:20px;color:var(--blue);font-size:12px}.docs-cta{padding:58px 0;color:#fff;background:var(--blue)}.docs-cta>div{display:flex;align-items:center;justify-content:space-between;gap:34px}.docs-cta h2{margin:0;font-size:30px}.docs-cta p{margin:10px 0 0;color:#dce9fb}.docs-cta a{padding:13px 17px;background:#fff;color:var(--blue);border-radius:4px;font-weight:800}.docs-footer{padding:38px 0;color:#a9bed1;background:#071b2f}.docs-footer>div{display:flex;justify-content:space-between;gap:20px}.docs-footer strong{color:#fff}.article-layout{display:grid;grid-template-columns:230px minmax(0,760px);justify-content:center;gap:58px;padding:70px 0 100px}.article-aside{position:sticky;top:105px;align-self:start;padding:18px 0;border-top:3px solid var(--blue);border-bottom:1px solid var(--line)}.article-aside>a{color:var(--blue);font-size:13px;font-weight:800}.article-aside p{margin:20px 0 0;color:var(--muted);font-size:13px;line-height:1.7}.doc-article{min-width:0;padding:0 0 30px}.doc-article h1{margin:0 0 28px;font-size:clamp(38px,5vw,58px);line-height:1.12}.doc-article h2{margin:50px 0 18px;padding-top:8px;font-size:28px;line-height:1.3;border-top:1px solid var(--line)}.doc-article h3{margin:32px 0 14px;font-size:20px}.doc-article p,.doc-article li{color:#354e6a;font-size:16px;line-height:1.85}.doc-article strong{color:var(--ink)}.doc-article a{color:var(--blue);text-decoration:underline;text-underline-offset:3px}.doc-article blockquote{margin:0 0 30px;padding:13px 18px;color:#3c5874;background:#eaf2fa;border-left:4px solid var(--cyan)}.doc-article blockquote p{margin:0;font-size:13px}.doc-article ul,.doc-article ol{padding-left:24px}.doc-article li+li{margin-top:8px}.doc-article code{padding:2px 5px;background:#e8eef5;border-radius:3px;font-size:.9em}.doc-article pre{overflow:auto;padding:18px;color:#e7f0f8;background:#0b2239;border-radius:4px}.doc-article pre code{padding:0;background:transparent}.doc-article table{display:block;width:100%;overflow-x:auto;border-collapse:collapse;margin:24px 0}.doc-article th,.doc-article td{min-width:120px;padding:11px 12px;border:1px solid var(--line);font-size:13px;line-height:1.55;text-align:left}.doc-article th{background:#e9f0f7}.doc-article img{margin:26px auto;border:1px solid var(--line)}@media(max-width:920px){.doc-group{grid-template-columns:1fr}.doc-grid{grid-template-columns:repeat(2,1fr)}.article-layout{grid-template-columns:1fr;gap:25px}.article-aside{position:static;display:grid;grid-template-columns:auto 1fr;gap:20px;align-items:start}.article-aside p{margin:0}}@media(max-width:680px){.docs-shell{width:min(100% - 28px,1160px)}.docs-nav{min-height:64px}.docs-brand small{display:none}.docs-nav nav{gap:12px;font-size:12px}.docs-nav nav a[href*="github.com"]{display:none}.docs-hero{padding:64px 0 52px}.docs-hero h1{font-size:40px}.docs-hero>div>p:last-of-type{font-size:15px}.docs-hero dl{width:100%;display:grid;grid-template-columns:repeat(3,1fr)}.docs-hero dl div{min-width:0;padding:12px 9px}.doc-grid{grid-template-columns:1fr}.doc-card{min-height:220px}.docs-cta>div,.docs-footer>div{align-items:flex-start;flex-direction:column}.docs-cta a{width:100%;text-align:center}.article-layout{padding-top:42px}.article-aside{grid-template-columns:1fr}.doc-article h1{font-size:36px;overflow-wrap:anywhere}.doc-article h2{font-size:25px}.doc-article p,.doc-article li{font-size:15px}.docs-nav nav a:nth-child(2){display:none}}'''


def copy_sources(wiki_publish: Path, content_root: Path) -> None:
    (content_root / "en").mkdir(parents=True, exist_ok=True)
    (content_root / "zh-CN").mkdir(parents=True, exist_ok=True)
    for article in ARTICLES:
        slug = article["slug"]
        shutil.copy2(wiki_publish / f"{slug}.md", content_root / "en" / f"{slug}.md")
        shutil.copy2(wiki_publish / f"{slug}-zh-CN.md", content_root / "zh-CN" / f"{slug}.md")


def build(project_root: Path, wiki_publish: Path | None) -> None:
    content_root = project_root / "content" / "docs"
    if wiki_publish:
        copy_sources(wiki_publish, content_root)
    selected = {article["slug"] for article in ARTICLES}
    for language, source_dir, output_dir in (
        ("zh", content_root / "zh-CN", project_root / "docs"),
        ("en", content_root / "en", project_root / "en" / "docs"),
    ):
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "styles.css").write_text(CSS + "\n", encoding="utf-8")
        (output_dir / "index.html").write_text(index_template(language), encoding="utf-8")
        for article in ARTICLES:
            source = source_dir / f"{article['slug']}.md"
            body = rewrite_links(render_markdown(source), language, selected)
            (output_dir / f"{article['slug']}.html").write_text(
                article_template(article, language, body), encoding="utf-8"
            )
        asset_source = (wiki_publish or (project_root.parent / "wiki" / "publish")) / "assets"
        if asset_source.exists():
            shutil.copytree(asset_source, output_dir / "assets", dirs_exist_ok=True)

    sitemap_urls = [
        f"{BASE_URL}/",
        f"{BASE_URL}/sandbox/",
        f"{BASE_URL}/en/",
        f"{BASE_URL}/en/sandbox/",
        f"{BASE_URL}/docs/",
        f"{BASE_URL}/en/docs/",
    ]
    for article in ARTICLES:
        sitemap_urls.append(f"{BASE_URL}/docs/{article['slug']}.html")
        sitemap_urls.append(f"{BASE_URL}/en/docs/{article['slug']}.html")
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap.extend(f"  <url><loc>{url}</loc></url>" for url in sitemap_urls)
    sitemap.append("</urlset>")
    (project_root / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--sync-from-wiki", type=Path)
    args = parser.parse_args()
    build(args.project_root.resolve(), args.sync_from_wiki.resolve() if args.sync_from_wiki else None)


if __name__ == "__main__":
    main()
