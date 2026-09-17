"""Validate the complete course, linked downloads and bilingual relationship figures."""
import hashlib
import json
import tempfile
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import build_learning
from sync_data_interface import FILES, published

ROOT = Path(__file__).resolve().parents[1]


class DataInterfaceTests(unittest.TestCase):
    def test_interface_assets_have_one_shared_location(self):
        self.assertTrue((ROOT / 'assets/data-interface/manifest.json').is_file())
        for relative in ('docs/assets/data-interface', 'en/docs/assets/data-interface'):
            self.assertFalse((ROOT / relative).exists(), relative)

    def test_complete_course_and_navigation(self):
        for language in ('zh-CN', 'en'):
            for name in FILES:
                self.assertTrue((ROOT / 'content/learning' / published(name, language)).is_file())
            suffix = '-zh-CN' if language == 'zh-CN' else ''
            for name in ('Learning-Center', 'Learning-Topic-B-Manufacturing-Data'):
                text = (ROOT / 'content/learning' / (name + suffix + '.md')).read_text()
                self.assertIn('Interface-Guide' + suffix + '.md', text)

    def test_download_manifest_and_safe_members(self):
        assets = ROOT / 'assets/data-interface'
        manifest = json.loads((assets / 'manifest.json').read_text())
        self.assertEqual(len(manifest['pages']), 30)
        archive = assets / manifest['download']
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), manifest['archive_sha256'])
        with zipfile.ZipFile(archive) as zipf:
            self.assertEqual(set(zipf.namelist()), {'examples/' + name for name in manifest['example_files']})
            for name, digest in manifest['example_files'].items():
                self.assertFalse(name.startswith('/') or '..' in Path(name).parts)
                self.assertNotIn('internal', Path(name).parts)
                self.assertEqual(hashlib.sha256(zipf.read('examples/' + name)).hexdigest(), digest)
                self.assertEqual(hashlib.sha256((assets / 'examples' / name).read_bytes()).hexdigest(), digest)
        for page in manifest['pages']:
            actual = ROOT / 'content/learning' / page['published']
            self.assertEqual(hashlib.sha256(actual.read_bytes()).hexdigest(), page['published_sha256'])

    def test_figures_are_static_and_complete(self):
        ns = {'s': 'http://www.w3.org/2000/svg'}
        for language in ('zh-CN', 'en'):
            svg = ET.parse(ROOT / f'assets/data-interface/semantic-relationships-{language}.svg')
            groups = svg.findall('.//s:g', ns)
            self.assertEqual(sum(g.get('class') == 'node' for g in groups), 16)
            self.assertEqual(sum(g.get('class') == 'edge' for g in groups), 20)
            prefix = 'learn' if language == 'zh-CN' else 'en/learn'
            text = (ROOT / prefix / 'Interface-Semantics.html').read_text()
            self.assertNotIn('class="mermaid"', text)
            self.assertIn('semantic-relationships-' + language + '.svg', text)

    def test_downloaded_exercises_actually_run(self):
        archive = ROOT / 'assets/data-interface/decisioworks-data-interface-examples.zip'
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(archive) as zipf:
                zipf.extractall(tmp)
            examples = Path(tmp) / 'examples'
            run = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', str(examples), '-v'],
                                 text=True, capture_output=True, timeout=60)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)

    def test_wiki_assets_remain_relative_to_wiki_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            build_learning.export_wiki(ROOT, Path(tmp))
            for path in Path(tmp).glob('Interface-*.md'):
                text = path.read_text()
                self.assertNotIn('../../assets/', text)
                if 'Guide' in path.name or 'Walkthrough' in path.name:
                    self.assertIn('(assets/data-interface/decisioworks-data-interface-examples.zip)', text)


if __name__ == '__main__':
    unittest.main()
