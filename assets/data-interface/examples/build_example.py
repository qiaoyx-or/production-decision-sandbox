"""Build a separate teaching database. Uses Python's standard library only."""
import argparse
import csv
import json
import sqlite3
from contextlib import closing
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANDIDATE = [(11, 1, 1001, 80), (12, 1, 1002, 80),
             (11, 2, 1001, 40), (12, 2, 1002, 40)]


def build(output_dir, third_period=False):
    output = Path(output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    target = output / 'data.db'
    if target.exists():
        raise FileExistsError(f'Refusing to overwrite {target}; choose a new output directory.')
    with closing(sqlite3.connect(':memory:')) as source:
        source.executescript((ROOT / 'schema.sql').read_text(encoding='utf-8'))
        source.executescript((ROOT / 'base.sql').read_text(encoding='utf-8'))
        if third_period:
            source.executescript((ROOT / 'third-period.sql').read_text(encoding='utf-8'))
        source.commit()
        assert source.execute('PRAGMA foreign_key_check').fetchall() == []
        with closing(sqlite3.connect(target)) as dest:
            source.backup(dest)
        for table in sorted({x['table'] for x in json.loads((ROOT / 'fields.json').read_text(encoding='utf-8'))}):
            cursor = source.execute(f'SELECT * FROM "{table}" ORDER BY id')
            with (output / f'{table}.csv').open('w', newline='', encoding='utf-8') as stream:
                writer = csv.writer(stream)
                writer.writerow([x[0] for x in cursor.description])
                writer.writerows(cursor.fetchall())
    with (output / 'manual_candidate.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream)
        writer.writerow(['workcenter', 'time_unit', 'process', 'number'])
        writer.writerows([(w, 3 if t == 2 else t, p, n) for w, t, p, n in CANDIDATE]
                         if third_period else CANDIDATE)
    facts = {'evidence_type': 'synthetic_teaching_data_and_manual_candidate',
             'solver_executed': False, 'planning_result_rows': 0,
             'quantity_unit': 'piece', 'material_units': {'BLANK': 'piece', 'FASTENER': 'piece'},
             'time_unit': 'seconds', 'opening_finished_stock': 20,
             'period_issues': [80, 40], 'minimum_finished_stock': 20, 'maximum_finished_stock': 100,
             'supply_storage': 'opening_availability_then_period_increments',
             'assumptions': ['no_scrap', 'no_setup_or_changeover', 'OEE_100', 'single_resource_per_operation'],
             'candidate': 'manual_candidate.csv'}
    if third_period:
        facts['period_issues'] = [80, 0, 40]
    (output / 'scenario.json').write_text(json.dumps(facts, indent=2) + '\n', encoding='utf-8')
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--third-period', action='store_true', help='Build the complete lesson 02 extension in a new folder')
    args = parser.parse_args()
    print(build(args.output_dir, third_period=args.third_period))
