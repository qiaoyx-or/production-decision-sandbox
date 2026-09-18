"""Render the semantic map with stable ports and an explicit time-reference index."""
import textwrap
import xml.etree.ElementTree as ET

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)

POSITIONS = {
    'T': (160, 236),
    'O': (160, 480), 'D': (430, 480), 'P': (700, 480),
    'A': (970, 480), 'I': (1240, 480),
    'S': (160, 700), 'RT': (700, 700), 'OP': (970, 700), 'B': (1240, 700),
    'W': (430, 920), 'PA': (700, 920), 'M': (1240, 920),
    'C': (430, 1140), 'R': (970, 1140), 'K': (1240, 1140),
}
CODES = {
    'T': 'time_unit', 'O': 'order_info', 'D': 'order_item', 'P': 'product',
    'A': 'property_1 / 2 / 3', 'I': 'inventory_limit', 'RT': 'process_route',
    'OP': 'process', 'PA': 'process_adaptor', 'W': 'workcenter',
    'S': 'shared_resource', 'C': 'capacity', 'B': 'ingredient', 'M': 'material',
    'K': 'kitting_information', 'R': 'planning_result',
}
TIME_TARGETS = ['D', 'C', 'K', 'I', 'R']
REFERENCE_CENTERS = {key: (425 + i * 210, 236) for i, key in enumerate(TIME_TARGETS)}
ROUTES = {
    ('O', 'D'): [(270, 480), (320, 480)],
    ('D', 'P'): [(540, 480), (590, 480)],
    ('P', 'A'): [(810, 480), (860, 480)],
    ('P', 'RT'): [(700, 536), (700, 644)],
    ('P', 'I'): [(700, 424), (700, 392), (1240, 392), (1240, 424)],
    ('RT', 'OP'): [(810, 700), (860, 700)],
    ('OP', 'PA'): [(970, 756), (970, 816), (700, 816), (700, 864)],
    ('PA', 'W'): [(590, 920), (540, 920)],
    ('W', 'C'): [(430, 976), (430, 1084)],
    ('S', 'W'): [(160, 756), (160, 816), (430, 816), (430, 864)],
    ('OP', 'B'): [(1080, 700), (1130, 700)],
    ('B', 'M'): [(1240, 756), (1240, 864)],
    ('M', 'K'): [(1240, 976), (1240, 1084)],
    ('OP', 'R'): [(970, 756), (970, 1084)],
    ('W', 'R'): [(430, 976), (430, 1022), (820, 1022), (820, 1140), (860, 1140)],
}


def element(parent, tag, **attrs):
    return ET.SubElement(parent, f'{{{NS}}}{tag}', {k.replace('_', '-'): str(v) for k, v in attrs.items()})


def text(parent, value, x, y, size=22, weight=400, fill='#17313a', anchor='middle'):
    node = element(parent, 'text', x=x, y=y, font_size=size, font_weight=weight,
                   fill=fill, text_anchor=anchor, dominant_baseline='middle')
    node.text = value


def color(key):
    if key == 'T':
        return '#3264a2', '#eff5ff'
    if key in ('PA', 'W', 'S', 'C'):
        return '#087e72', '#eef9f5'
    if key in ('B', 'M', 'K'):
        return '#a86416', '#fff8ee'
    if key == 'R':
        return '#173f50', '#eef5f8'
    return '#556d89', '#f5f7fb'


def box(parent, key, label, language, reference=False):
    x, y = REFERENCE_CENTERS[key] if reference else POSITIONS[key]
    width, height = (170, 104) if reference else (220, 104 if key == 'T' else 112)
    stroke, fill = ('#7290b8', '#ffffff') if reference else color(key)
    group = element(parent, 'g', **({'class': 'reference', 'data-ref': key} if reference else
                                   {'class': 'node', 'data-id': key}))
    element(group, 'title').text = label + ' / ' + CODES[key]
    element(group, 'rect', x=x-width/2, y=y-height/2, width=width, height=height,
            rx=8, fill=fill, stroke=stroke, stroke_width=1.8)
    size = (19 if language == 'zh-CN' else 17) if reference else (25 if language == 'zh-CN' else 23)
    if language == 'en' and key == 'PA':
        size = 20
    lines = [label] if language == 'zh-CN' else textwrap.wrap(label, 16 if reference else 18, break_long_words=False, break_on_hyphens=False)
    if len(lines) > 2:
        size -= 2
        lines = textwrap.wrap(label, 23, break_long_words=False, break_on_hyphens=False)
    assert len(lines) <= 2, f'Node label needs a layout review: {label}'
    for i, line in enumerate(lines):
        text(group, line, x, y - (22 if len(lines) == 2 else 11) + i * 27,
             size=size, weight=600, fill=stroke)
    text(group, CODES[key], x, y+30, size=13 if reference else 16, fill='#60727b')


def render_diagram(nodes, edges, destination):
    expected = set(ROUTES) | {('T', key) for key in TIME_TARGETS}
    if set(nodes) != set(POSITIONS) or set(edges) != expected or len(edges) != len(expected):
        raise ValueError('The semantic graph changed; review the fixed-layout map before publishing.')
    language = 'zh-CN' if destination.stem.endswith('zh-CN') else 'en'
    zh = language == 'zh-CN'
    svg = ET.Element(f'{{{NS}}}svg', {
        'viewBox': '0 0 1400 1330', 'width': '1400', 'height': '1330',
        'role': 'img', 'aria-labelledby': 'map-title map-description',
        'font-family': "'Noto Sans CJK SC', 'Microsoft YaHei', Arial, sans-serif",
    })
    element(svg, 'title', id='map-title').text = '标准化数据接口体系总图' if zh else 'Standardized data interface system map'
    element(svg, 'desc', id='map-description').text = (
        '顶部时间关联索引与下方同名对象对应。16个业务对象、20条关系；箭头不表示处理顺序。' if zh else
        'The time-reference index points to the same objects in the business map below. Sixteen objects and twenty relationships; arrows do not indicate execution order.')
    defs = element(svg, 'defs')
    for name, fill in [('business-arrow', '#627985'), ('time-arrow', '#7290b8')]:
        marker = element(defs, 'marker', id=name, viewBox='0 0 10 10', refX=9, refY=5,
                         markerWidth=8, markerHeight=8, orient='auto', markerUnits='userSpaceOnUse')
        element(marker, 'path', d='M 1 1 L 9 5 L 1 9 Z', fill=fill)
    element(svg, 'rect', width=1400, height=1330, fill='#ffffff')
    text(svg, '标准化数据接口 · 体系总图' if zh else 'Standardized Data Interface', 50, 56,
         size=34, weight=700, anchor='start')
    text(svg, '统一时间坐标，连接制造业务对象' if zh else 'A common time basis connects manufacturing objects',
         50, 100, size=21, fill='#60727b', anchor='start')
    element(svg, 'rect', x=32, y=128, width=1336, height=190, rx=8, fill='#f4f8fd')
    # Draw connectors before nodes so line ends never cover the labels or borders.
    for left, right in edges:
        time = left == 'T'
        points = [(160, 184), (160, 158), (REFERENCE_CENTERS[right][0], 158),
                  (REFERENCE_CENTERS[right][0], 184)] if time else ROUTES[left, right]
        group = element(svg, 'g', **{'class': 'edge', 'data-from': left, 'data-to': right})
        element(group, 'title').text = left + ' -> ' + right
        path = 'M ' + ' L '.join(f'{x} {y}' for x, y in points)
        element(group, 'path', d=path, fill='none', stroke='#7290b8' if time else '#627985',
                stroke_width=2.4, stroke_linejoin='round', stroke_linecap='round',
                marker_end='url(#time-arrow)' if time else 'url(#business-arrow)')
    for x, y in [(970, 816), (430, 1022)]:
        element(svg, 'circle', cx=x, cy=y, r=3.4, fill='#627985')
    text(svg, '制造业务对象' if zh else 'Manufacturing objects', 50, 358,
         size=23, weight=600, anchor='start')
    for key, label in nodes.items():
        box(svg, key, label, language)
    for key in TIME_TARGETS:
        box(svg, key, nodes[key], language, reference=True)
    element(svg, 'line', x1=50, y1=1240, x2=1350, y2=1240, stroke='#d9e1e5')
    text(svg, '顶部为时间关联索引，与下方同名对象对应；箭头表示关系，不表示处理顺序。' if zh else
         'Time references above point to the same objects below. Arrows show relationships, not execution order.',
         50, 1273, size=19, fill='#60727b', anchor='start')
    text(svg, '属性在模板中对应三个属性表；共享资源本身也由工作中心表达。' if zh else
         'Attributes use three template tables. Shared resources are also represented as work centers.',
         50, 1305, size=19, fill='#60727b', anchor='start')
    ET.indent(svg, space='  ')
    ET.ElementTree(svg).write(destination, encoding='utf-8', xml_declaration=True)
