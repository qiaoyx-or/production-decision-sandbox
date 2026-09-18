#!/usr/bin/env python3
"""Import the reviewed bilingual data-interface course into the static learning center."""
import argparse
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path
from urllib.parse import urlsplit

from render_data_interface_diagram import render_diagram

FILES = {
    'index.md': 'Interface-Guide', 'semantics.md': 'Interface-Semantics',
    'field-reference.md': 'Interface-Fields', 'relationship-reference.md': 'Interface-Relationships',
    'configuration-patterns.md': 'Interface-Configurations', 'walkthrough.md': 'Interface-Walkthrough',
    '01-calendar.md': 'Interface-01-Calendar', '02-demand.md': 'Interface-02-Demand',
    '03-resources.md': 'Interface-03-Resources', '04-routing.md': 'Interface-04-Routing',
    '05-quantity.md': 'Interface-05-Quantity', '06-materials.md': 'Interface-06-Materials',
    '07-inventory.md': 'Interface-07-Inventory', '08-validation.md': 'Interface-08-Validation',
    '09-results.md': 'Interface-09-Results',
}


def published(name, language):
    return FILES[name] + ('-zh-CN' if language == 'zh-CN' else '') + '.md'


def diagram(source, destination):
    # This course uses only directed object references; fail on a new syntax rather than drop it.
    match = re.search(r'```mermaid\s*\nflowchart TB\n(.*?)\n```', source, re.S)
    if not match:
        raise ValueError('Missing semantic relationship diagram')
    nodes, edges = {}, []
    token = r'([A-Z]+)(?:\[([^\]]+)\])?'
    for line in match[1].splitlines():
        link = re.fullmatch(r'\s*' + token + r'\s*-->\s*' + token + r'\s*', line)
        if not link:
            raise ValueError(f'Unsupported relationship diagram syntax: {line}')
        left, left_label, right, right_label = link.groups()
        for key, label in [(left, left_label), (right, right_label)]:
            if label:
                nodes[key] = label
        edges.append((left, right))
    if any(a not in nodes or b not in nodes for a, b in edges):
        raise ValueError('Relationship diagram has an undefined object')
    dot = ['digraph Interface {', 'graph [rankdir=TB, bgcolor="white", pad=0.25, nodesep=0.35, ranksep=0.55];',
           'node [shape=box, style="rounded,filled", fillcolor="#f1f8f6", color="#148474", fontname="Noto Sans CJK SC", fontsize=16, margin="0.15,0.12"];',
           'edge [color="#637a83", penwidth=1.3, arrowsize=0.65];']
    dot.extend(f'{key} [label={json.dumps(label, ensure_ascii=False)}];' for key, label in nodes.items())
    dot.extend(f'{a} -> {b};' for a, b in edges)
    dot.append('}')
    destination.with_suffix('.dot').write_text('\n'.join(dot) + '\n', encoding='utf-8')
    render_diagram(nodes, edges, destination)
    return match.group(0)


def sync(source, root):
    source, root = source.resolve(), root.resolve()
    target = root / 'content/learning'
    assets = root / 'assets/data-interface'
    target.mkdir(parents=True, exist_ok=True)
    assets.mkdir(parents=True, exist_ok=True)
    entries = []
    example_root = source / 'examples'
    for path in sorted(example_root.rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts and path.suffix in {'.py', '.sql', '.json', '.csv', '.db'}:
            relative = path.relative_to(example_root)
            dest = assets / 'examples' / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, dest)
            entries.append((relative.as_posix(), path.read_bytes()))
    archive = assets / 'decisioworks-data-interface-examples.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        for name, data in entries:
            info = zipfile.ZipInfo('examples/' + name, date_time=(2026, 9, 17, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            zipf.writestr(info, data)
    records = []
    for language in ('zh-CN', 'en'):
        actual = {p.name for p in (source / language).glob('*.md')}
        if actual != set(FILES):
            raise ValueError(f'Unexpected {language} course inventory: {actual ^ set(FILES)}')
        for name in FILES:
            original = (source / language / name).read_text(encoding='utf-8-sig')
            def link(match):
                raw = match.group(1)
                parsed = urlsplit(raw)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    return match.group(0)
                path = parsed.path
                if path.startswith('../examples/'):
                    if path.endswith('/'):
                        path = '../../assets/data-interface/decisioworks-data-interface-examples.zip'
                    else:
                        path = '../../assets/data-interface/examples/' + path[len('../examples/'):]
                else:
                    lang = 'en' if path.startswith('../en/') else 'zh-CN' if path.startswith('../zh-CN/') else language
                    path = published(Path(path).name, lang)
                return '](' + path + ('#' + parsed.fragment if parsed.fragment else '') + ')'
            text = re.sub(r'\]\(([^)]+)\)', link, original)
            if name == 'semantics.md':
                filename = f'semantic-relationships-{language}.svg'
                block = diagram(text, assets / filename)
                alt = '标准化数据接口对象关系' if language == 'zh-CN' else 'Standardized data-interface object relationships'
                text = text.replace(block, f'[{"查看原尺寸关系图" if language == "zh-CN" else "Open the full-size relationship diagram"}](../../assets/data-interface/{filename})\n\n![{alt}](../../assets/data-interface/{filename})')
            if name in ('index.md', 'walkthrough.md'):
                label = '下载完整练习包（SQL、字段清单、Python脚本、数据库及CSV）' if language == 'zh-CN' else 'Download the complete exercise pack (SQL, field list, Python scripts, database and CSV files)'
                lines = text.splitlines()
                lines[4:4] = [f'[{label}](../../assets/data-interface/{archive.name})', '']
                text = '\n'.join(lines) + '\n'
            text = text.replace('[示例输出目录](', '[完整示例下载](').replace('[sample output directory](', '[complete example download](')
            dest = target / published(name, language)
            dest.write_text(text, encoding='utf-8', newline='\n')
            records.append({'source': f'{language}/{name}', 'published': dest.name,
                            'source_sha256': hashlib.sha256(original.encode()).hexdigest(),
                            'published_sha256': hashlib.sha256(dest.read_bytes()).hexdigest()})
    manifest = {'pages': records, 'download': archive.name,
                'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
                'example_files': {name: hashlib.sha256(data).hexdigest() for name, data in entries}}
    (assets / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Imported {len(records)} bilingual pages and {len(entries)} exercise files.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True, help='Reviewed course public directory')
    parser.add_argument('--project-root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    sync(args.source, args.project_root)
