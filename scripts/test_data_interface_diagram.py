"""Check graph preservation, connector routing, ports and reproducible rendering."""
import json
import re
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from render_data_interface_diagram import render_diagram

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets/data-interface'
NS = {'s': 'http://www.w3.org/2000/svg'}


def graph(language):
    source = (ASSETS / f'semantic-relationships-{language}.dot').read_text(encoding='utf-8')
    nodes = {key: json.loads(label) for key, label in re.findall(r'^(\w+) \[label=(.*)\];$', source, re.M)}
    edges = re.findall(r'^(\w+) -> (\w+);$', source, re.M)
    return nodes, edges


def groups(svg, kind):
    return svg.findall(f's:g[@class="{kind}"]', NS)


def rectangle(group):
    rect = group.find('s:rect', NS)
    x, y, w, h = (float(rect.get(k)) for k in ('x', 'y', 'width', 'height'))
    return x, y, x + w, y + h


def ports(box):
    l, t, r, b = box
    return {(l, (t+b)/2), (r, (t+b)/2), ((l+r)/2, t), ((l+r)/2, b)}


class DiagramTests(unittest.TestCase):
    def test_semantic_graph_and_aliases_preserved(self):
        for language in ('zh-CN', 'en'):
            with self.subTest(language=language):
                nodes, edges = graph(language)
                svg = ET.parse(ASSETS / f'semantic-relationships-{language}.svg').getroot()
                actual = groups(svg, 'node')
                self.assertEqual({g.get('data-id') for g in actual}, set(nodes))
                self.assertEqual(len(actual), 16)
                self.assertEqual({(g.get('data-from'), g.get('data-to')) for g in groups(svg, 'edge')}, set(edges))
                self.assertEqual(len(groups(svg, 'edge')), 20)
                self.assertEqual({g.get('data-ref') for g in groups(svg, 'reference')}, {'D', 'C', 'K', 'I', 'R'})
                for g in actual:
                    self.assertTrue(g.find('s:title', NS).text.startswith(nodes[g.get('data-id')] + ' / '))

    def test_connectors_are_orthogonal_centered_and_clear(self):
        svg = ET.parse(ASSETS / 'semantic-relationships-en.svg').getroot()
        boxes = {g.get('data-id'): rectangle(g) for g in groups(svg, 'node')}
        aliases = {g.get('data-ref'): rectangle(g) for g in groups(svg, 'reference')}
        for edge in groups(svg, 'edge'):
            left, right = edge.get('data-from'), edge.get('data-to')
            with self.subTest(edge=(left, right)):
                coordinates = list(map(float, re.findall(r'-?\d+(?:\.\d+)?', edge.find('s:path', NS).get('d'))))
                points = list(zip(coordinates[::2], coordinates[1::2]))
                self.assertIn(points[0], ports(boxes[left]))
                self.assertIn(points[-1], ports(aliases[right] if left == 'T' else boxes[right]))
                for (x1, y1), (x2, y2) in zip(points, points[1:]):
                    self.assertTrue(x1 == x2 or y1 == y2)
                    self.assertNotEqual((x1, y1), (x2, y2))
                    for box in list(boxes.values()) + list(aliases.values()):
                        l, t, r, b = box
                        crosses = ((t < y1 < b and max(min(x1, x2), l) < min(max(x1, x2), r)) if y1 == y2 else
                                   (l < x1 < r and max(min(y1, y2), t) < min(max(y1, y2), b)))
                        self.assertFalse(crosses, f'{left}->{right} enters a node interior')

    def test_render_is_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            for language in ('zh-CN', 'en'):
                name = f'semantic-relationships-{language}.svg'
                destination = Path(directory) / name
                render_diagram(*graph(language), destination)
                self.assertEqual(destination.read_bytes(), (ASSETS / name).read_bytes())

    def test_changed_graph_requires_layout_review(self):
        nodes, edges = graph('en')
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'test-en.svg'
            for changed in (edges[:-1], edges + [edges[0]], edges + [('P', 'R')]):
                with self.assertRaises(ValueError):
                    render_diagram(nodes, changed, destination)
            with self.assertRaises(ValueError):
                render_diagram({**nodes, 'NEW': 'New object'}, edges, destination)


if __name__ == '__main__':
    unittest.main()
