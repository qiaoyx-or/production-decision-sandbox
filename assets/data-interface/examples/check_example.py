"""Validate the schema, stored values and business rules of the teaching example."""
import argparse
import json
import math
import sqlite3
from contextlib import closing
from pathlib import Path

FIELDS = json.loads((Path(__file__).parent / 'fields.json').read_text(encoding='utf-8'))
CHECKS = ['schema', 'stored_values', 'references_and_business_rules']
NOT_CHECKED = ['model_configuration', 'demand_coverage', 'detailed_scheduling_feasibility',
               'advanced_scenario_rules', 'solver_execution']
REQUIRED_FOR_EXAMPLE = {
    ('capacity', 'workcenter'), ('order_item', 'delivery_time'),
    ('process_adaptor', 'process'), ('process_adaptor', 'workcenter'),
    ('planning_result', 'process'), ('planning_result', 'workcenter'),
    ('shared_resource', 'binding'), ('shared_resource', 'to'),
}


def stored_value_errors(conn):
    errors = []
    for field in FIELDS:
        table, name, kind = field['table'], field['field'], field['sqlite_type'].upper()
        required = not field['nullable'] or (table, name) in REQUIRED_FOR_EXAMPLE
        for row_id, value in conn.execute(f'SELECT id,"{name}" FROM "{table}"'):
            location = f'{table}.{name} id={row_id}'
            if value is None:
                if required:
                    errors.append(f'required value: {location}')
                continue
            valid = (
                (kind == 'INTEGER' and isinstance(value, int))
                or (kind == 'BOOLEAN' and isinstance(value, int) and value in (0, 1))
                or (kind == 'FLOAT' and isinstance(value, (int, float))
                    and (not isinstance(value, float) or math.isfinite(value)))
                or (kind in ('VARCHAR', 'DATETIME') and isinstance(value, str))
            )
            if not valid:
                label = f'{table} quantity' if name == 'number' else 'stored value type'
                errors.append(f'{label}: {location}, expected {kind}, got {value!r}')
    return errors


def hierarchy_errors(conn):
    parents = dict(conn.execute('SELECT id,parent_id FROM workcenter'))
    completed = set()
    errors = []
    for start in parents:
        path, positions = [], {}
        node = start
        while node is not None and node in parents and node not in completed:
            if node in positions:
                cycle = path[positions[node]:] + [node]
                errors.append('workcenter hierarchy cycle: ' + ' -> '.join(map(str, cycle)))
                break
            positions[node] = len(path)
            path.append(node)
            node = parents[node]
        completed.update(path)
    return errors


def _check(path):
    errors = []
    performed = []
    counts = {}
    def result():
        return {'ok': not errors, 'errors': errors, 'tables': len(counts), 'fields': len(FIELDS),
                'rows': counts, 'scope': 'teaching_structure_and_semantics',
                'checks_performed': performed, 'checks_skipped': [c for c in CHECKS if c not in performed],
                'not_checked': NOT_CHECKED, 'solver_executed': False}
    db = Path(path).resolve()
    with closing(sqlite3.connect(db.as_uri() + '?mode=ro', uri=True)) as conn:
        actual = {x[0] for x in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in sorted({f['table'] for f in FIELDS}):
            if table not in actual:
                errors.append(f'missing table: {table}')
                continue
            got = {x[1]: x for x in conn.execute(f'PRAGMA table_info("{table}")')}
            foreign_keys = {(x[3], x[2], x[4]) for x in conn.execute(f'PRAGMA foreign_key_list("{table}")')}
            for f in (f for f in FIELDS if f['table'] == table):
                if f['field'] not in got:
                    errors.append(f'missing field: {table}.{f["field"]}')
                    continue
                column = got[f['field']]
                if column[2].upper() != f['sqlite_type'].upper():
                    errors.append(f'type mismatch: {table}.{f["field"]}')
                if bool(column[5]) != f['primary_key']:
                    errors.append(f'primary key schema: {table}.{f["field"]}')
                # INTEGER primary keys are non-null even when PRAGMA reports notnull=0.
                nullable = not (column[3] or (column[5] and column[2].upper() == 'INTEGER'))
                if nullable != f['nullable']:
                    errors.append(f'nullability schema: {table}.{f["field"]}')
                if f['foreign_key']:
                    target_table, target_field = f['foreign_key'].split('.')
                    if (f['field'], target_table, target_field) not in foreign_keys:
                        errors.append(f'foreign key schema: {table}.{f["field"]} -> {f["foreign_key"]}')
        performed.append('schema')
        if errors:
            return result()
        counts = {t: conn.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0] for t in sorted({f['table'] for f in FIELDS})}
        errors.extend(stored_value_errors(conn))
        performed.append('stored_values')
        # Do not apply arithmetic or graph rules to values that failed type checks.
        if errors:
            return result()
        for row in conn.execute('PRAGMA foreign_key_check'):
            errors.append(f'foreign key: table={row[0]}, rowid={row[1]}, target={row[2]}')
        rules = {
            'time state or scale': 'SELECT id FROM time_unit WHERE status NOT IN (-1,0,1) OR scale<=0',
            'duplicate time offset': 'SELECT min(id) FROM time_unit GROUP BY offset HAVING count(*)>1',
            'capacity fraction': "SELECT id FROM capacity WHERE typeof(used) NOT IN ('real','integer') OR used<0 OR used>1",
            'duplicate resource period': 'SELECT min(id) FROM capacity GROUP BY workcenter,time_unit HAVING count(*)>1',
            'batch or output quantity': 'SELECT id FROM process_adaptor WHERE productivity<=0 OR batch_size<=0 OR batch_size%productivity!=0',
            'processing duration': 'SELECT id FROM process_adaptor WHERE processing_time<=0 OR setup_time<0',
            'OEE percentage': 'SELECT id FROM process_adaptor WHERE OEE<0 OR OEE>100',
            'WIP capacity': 'SELECT id FROM process_adaptor WHERE wip_buffer_size<0',
            'operation numbering': 'SELECT min(id) FROM process GROUP BY route,operation_number HAVING count(*)>1',
            'inventory bounds': 'SELECT id FROM inventory_limit WHERE lower_bound_acc<0 OR upper_bound_acc<0 OR lower_bound_acc>upper_bound_acc',
            'unmapped operation': 'SELECT id FROM process WHERE NOT EXISTS (SELECT 1 FROM process_adaptor a WHERE a.process=process.id AND a.workcenter IS NOT NULL)',
            'product without route': 'SELECT id FROM order_item WHERE NOT EXISTS (SELECT 1 FROM process_route r WHERE r.product=order_item.product)',
            'route without operation': 'SELECT id FROM process_route WHERE NOT EXISTS (SELECT 1 FROM process p WHERE p.route=process_route.id)',
            'resource type or count': 'SELECT id FROM workcenter WHERE parallelism<=0 OR station_count<=0 OR equipping_time<0',
            'invalid adaptor target': 'SELECT a.id FROM process_adaptor a JOIN workcenter w ON w.id=a.workcenter WHERE a.process IS NULL OR w.type!=0',
        }
        for table in ('order_item', 'ingredient', 'kitting_information', 'planning_result'):
            rules[f'{table} quantity'] = f"SELECT id FROM {table} WHERE typeof(number)!='integer' OR number<0"
        for label, sql in rules.items():
            rows = [x[0] for x in conn.execute(sql)]
            if rows:
                errors.append(f'{label}: ids={rows}')
        errors.extend(hierarchy_errors(conn))
        offsets = [x[0] for x in conn.execute('SELECT offset FROM time_unit ORDER BY offset')]
        if offsets and offsets != list(range(offsets[0], offsets[0] + len(offsets))):
            errors.append('time continuity: this example requires consecutive offsets')
        performed.append('references_and_business_rules')
    return result()


def check(path):
    try:
        return _check(path)
    except (OSError, sqlite3.Error) as exc:
        return {'ok': False, 'errors': [f'cannot validate database: {exc}'],
                'tables': 0, 'fields': len(FIELDS), 'rows': {},
                'scope': 'teaching_structure_and_semantics',
                'checks_performed': [], 'checks_skipped': CHECKS,
                'not_checked': NOT_CHECKED, 'solver_executed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('database')
    result = check(parser.parse_args().database)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['ok'] else 1)
