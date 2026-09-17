import sqlite3
import json
import subprocess
import sys
from contextlib import closing
import tempfile
import unittest
from pathlib import Path

from build_example import build
from check_example import check
from calculate_candidate import calculate

NEGATIVE_CASES = [
    ('UPDATE capacity SET used=25 WHERE id=1;', 'capacity fraction'),
    ('UPDATE order_item SET delivery_time=99 WHERE id=1;', 'foreign key'),
    ('UPDATE process_adaptor SET batch_size=18 WHERE id=1;', 'batch or output'),
    ('UPDATE time_unit SET status=2 WHERE id=1;', 'time state'),
    ('UPDATE time_unit SET scale=0 WHERE id=1;', 'time state'),
    ('UPDATE inventory_limit SET lower_bound_acc=999 WHERE id=1;', 'inventory bounds'),
    ('UPDATE process SET operation_number=10 WHERE id=1002;', 'operation numbering'),
    ('UPDATE product SET property_1=99 WHERE id=1;', 'foreign key'),
    ('UPDATE time_unit SET offset=0 WHERE id=2;', 'duplicate time'),
    ('UPDATE ingredient SET number=0.2 WHERE id=1;', 'ingredient quantity'),
    ('UPDATE order_item SET number=-1 WHERE id=1;', 'order_item quantity'),
    ('UPDATE time_unit SET offset=4 WHERE id=2;', 'time continuity'),
    ("UPDATE time_unit SET scale='eight hours' WHERE id=1;", 'time_unit.scale id=1'),
    ("UPDATE process_adaptor SET processing_time='ten minutes' WHERE id=1;", 'process_adaptor.processing_time id=1'),
    ('UPDATE process_adaptor SET productivity=4.5 WHERE id=1;', 'process_adaptor.productivity id=1'),
    ('UPDATE process_adaptor SET batch_size=20.5 WHERE id=1;', 'process_adaptor.batch_size id=1'),
    ('UPDATE process_adaptor SET OEE=150 WHERE id=1;', 'OEE percentage'),
    ('UPDATE workcenter SET parent_id=id WHERE id=11;', 'hierarchy cycle'),
    ('UPDATE capacity SET workcenter=NULL WHERE id=1;', 'required value: capacity.workcenter id=1'),
    ('UPDATE order_item SET delivery_time=NULL WHERE id=1;', 'required value: order_item.delivery_time id=1'),
    ('UPDATE workcenter SET parent_id=12 WHERE id=11; UPDATE workcenter SET parent_id=11 WHERE id=12;', 'hierarchy cycle'),
    ('UPDATE workcenter SET parent_id=99 WHERE id=11;', 'foreign key'),
    ('UPDATE process_adaptor SET OEE=-1 WHERE id=1;', 'OEE percentage'),
    ('UPDATE process_adaptor SET processing_time=1e999 WHERE id=1;', 'process_adaptor.processing_time id=1'),
    ('UPDATE property_1 SET is_key=2 WHERE id=1;', 'property_1.is_key id=1'),
    ("UPDATE time_unit SET offset='tomorrow' WHERE id=2;", 'time_unit.offset id=2'),
    ("UPDATE capacity SET used='25%' WHERE id=1;", 'capacity.used id=1'),
    ('UPDATE process_adaptor SET workcenter=NULL WHERE id=1;', 'required value: process_adaptor.workcenter id=1'),
    ('UPDATE process_adaptor SET process=NULL WHERE id=1;', 'required value: process_adaptor.process id=1'),
    ('UPDATE process_adaptor SET wip_buffer_size=-1 WHERE id=1;', 'WIP capacity'),
]


class TeachingContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp.name)
        self.db = build(self.folder)

    def tearDown(self):
        self.temp.cleanup()

    def mutate(self, sql):
        with closing(sqlite3.connect(self.db)) as conn:
            conn.executescript(sql)

    def test_base(self):
        result = check(self.db)
        self.assertTrue(result['ok'], result)
        self.assertEqual((result['tables'], result['fields']), (18, 105))
        self.assertEqual(result['rows']['planning_result'], 0)

    def test_no_overwrite(self):
        with self.assertRaises(FileExistsError):
            build(self.folder)

    def test_candidate(self):
        r = calculate(self.folder)
        self.assertTrue(r['aggregate_checks_passed'])
        self.assertEqual([x['processing_minutes'] for x in r['workload']], [200, 160, 100, 80])
        self.assertEqual([x['ending_inventory'] for x in r['inventory']], [20, 20])
        self.assertFalse(r['solver_executed'])
        self.assertFalse(r['full_scheduling_feasibility_proven'])

    def test_maintenance_update(self):
        self.mutate('UPDATE capacity SET used=0.375 WHERE id=1;')
        r = calculate(self.folder)
        self.assertEqual(r['workload'][0]['available_minutes'], 300)
        self.assertEqual(r['three_hour_maintenance_chain_minutes'], 540)

    def test_complete_third_period(self):
        folder = self.folder / 'three-periods'
        build(folder, third_period=True)
        self.assertTrue(check(folder / 'data.db')['ok'])
        result = calculate(folder)
        self.assertTrue(result['aggregate_checks_passed'], result)
        self.assertEqual([r['ending_inventory'] for r in result['inventory']], [20, 20, 20])
        self.assertEqual([r['cumulative_output'] for r in result['inventory']], [80, 80, 120])
        self.assertTrue(result['issues_match_due_quantities'])

    def test_partial_extension_reports_missing_files_and_records(self):
        self.mutate('INSERT INTO time_unit VALUES(3,2,28800,1); UPDATE order_item SET delivery_time=3 WHERE id=2;')
        result = calculate(self.folder)
        self.assertFalse(result['ok'])
        self.assertIn('period_issues: expected 3', result['errors'][0])
        path = self.folder / 'scenario.json'
        facts = json.loads(path.read_text())
        facts['period_issues'] = [80, 0, 40]
        path.write_text(json.dumps(facts))
        self.assertIn('inventory_limit:', calculate(self.folder)['errors'][0])
        self.mutate('INSERT INTO inventory_limit (id,product,time_unit,lower_bound_acc,upper_bound_acc,urgency) VALUES(3,1,3,120,200,0);')
        self.assertIn('capacity:', calculate(self.folder)['errors'][0])

    def test_demand_changes_are_visible_without_claiming_coverage(self):
        self.mutate('UPDATE order_item SET number=400 WHERE id=2;')
        result = calculate(self.folder)
        self.assertTrue(result['aggregate_checks_passed'])
        self.assertFalse(result['issues_match_due_quantities'])
        self.assertFalse(result['demand_coverage_checked'])
        self.assertEqual(result['demand_issue_comparison'][1]['difference'], -360)

    def test_calculator_rejects_unsupported_profile(self):
        self.mutate('UPDATE process_adaptor SET setup_time=60 WHERE id=1;')
        self.assertFalse(calculate(self.folder)['ok'])
        self.assertIn('setup_time=0', calculate(self.folder)['errors'][0])

    def test_calculator_rejects_empty_and_malformed_candidate(self):
        path = self.folder / 'manual_candidate.csv'
        for text in ['workcenter,time_unit,process,number\n', 'workcenter,time_unit,process,number\n11,1,1001,hello\n',
                     'workcenter,time_unit,process,number\n11,99,1001,80\n']:
            path.write_text(text)
            self.assertFalse(calculate(self.folder)['ok'])

    def test_calculator_cli_returns_json_on_error(self):
        (self.folder / 'scenario.json').write_text('{broken')
        run = subprocess.run([sys.executable, str(Path(__file__).with_name('calculate_candidate.py')), str(self.folder)],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 1)
        self.assertFalse(json.loads(run.stdout)['ok'])
        self.assertNotIn('Traceback', run.stderr + run.stdout)

    def test_calculator_rejects_imbalanced_operations(self):
        path = self.folder / 'manual_candidate.csv'
        path.write_text(path.read_text().replace('1001,80', '1001,40'))
        self.assertIn('equal output', calculate(self.folder)['errors'][0])

    def test_calculator_rejects_invalid_issue_quantity(self):
        path = self.folder / 'scenario.json'
        facts = json.loads(path.read_text())
        for value in [-1, '40', None, float('inf')]:
            facts['period_issues'][1] = value
            path.write_text(json.dumps(facts))
            self.assertFalse(calculate(self.folder)['ok'])

    def test_transfer_batch_assumption(self):
        stamp_end = 180
        assembly_end = 0
        finishes = []
        for _ in range(4):
            stamp_end += (20 // 4) * 600 / 60
            assembly_end = max(stamp_end, assembly_end) + 20 * 120 / 60
            finishes.append(assembly_end)
        self.assertEqual(finishes, [270, 320, 370, 420])
        self.assertEqual(180 + 80 / 4 * 600 / 60 + 80 * 120 / 60, 540)

    def test_equal_seqno_is_allowed(self):
        self.mutate('UPDATE process SET seqno=1;')
        self.assertTrue(check(self.db)['ok'])

    def test_nonmultiple_demand_is_not_universally_rejected(self):
        self.mutate('UPDATE order_item SET number=42 WHERE id=1;')
        self.assertTrue(check(self.db)['ok'])

    def test_null_inventory_bounds(self):
        self.mutate('UPDATE inventory_limit SET upper_bound_acc=NULL,lower_bound_acc=NULL;')
        self.assertTrue(check(self.db)['ok'])

    def test_allowed_optional_values(self):
        self.mutate('UPDATE product SET property_2=NULL,property_3=NULL,vin=NULL; '
                    'UPDATE material SET substitute=NULL,binding=NULL,extend=NULL; '
                    'UPDATE workcenter SET parent_id=NULL WHERE id=10; '
                    'UPDATE process_adaptor SET binding=NULL;')
        self.assertTrue(check(self.db)['ok'])

    def test_boundary_values(self):
        self.mutate('UPDATE capacity SET used=1 WHERE id=1; UPDATE capacity SET used=0 WHERE id=2; '
                    'UPDATE process_adaptor SET OEE=0 WHERE id=1; '
                    'UPDATE process_adaptor SET OEE=100 WHERE id=2; '
                    'UPDATE time_unit SET status=-1 WHERE id=2;')
        self.assertTrue(check(self.db)['ok'])

    def test_declared_check_scope(self):
        result = check(self.db)
        self.assertEqual(result['checks_skipped'], [])
        self.assertIn('detailed_scheduling_feasibility', result['not_checked'])
        self.mutate("UPDATE time_unit SET scale='eight hours' WHERE id=1;")
        result = check(self.db)
        self.assertFalse(result['ok'])
        self.assertIn('references_and_business_rules', result['checks_skipped'])

    def test_missing_structure_returns_error(self):
        self.mutate('DROP TABLE planning_result;')
        result = check(self.db)
        self.assertFalse(result['ok'])
        self.assertIn('missing table: planning_result', result['errors'])

    def replace_capacity_schema(self, columns):
        with closing(sqlite3.connect(self.db)) as conn:
            rows = conn.execute('SELECT * FROM capacity').fetchall()
            conn.execute('DROP TABLE capacity')
            conn.execute('CREATE TABLE capacity (' + columns + ')')
            conn.executemany('INSERT INTO capacity VALUES (?,?,?,?)', rows)
            conn.commit()

    def test_missing_foreign_key_declaration_is_rejected(self):
        self.replace_capacity_schema('id INTEGER NOT NULL PRIMARY KEY, time_unit INTEGER NOT NULL, '
                                     'used FLOAT NOT NULL, workcenter INTEGER REFERENCES workcenter(id)')
        self.mutate('UPDATE capacity SET time_unit=999 WHERE id=1;')
        result = check(self.db)
        self.assertFalse(result['ok'])
        self.assertIn('foreign key schema: capacity.time_unit -> time_unit.id', result['errors'])
        self.assertEqual(result['checks_performed'], ['schema'])

    def test_missing_primary_key_is_rejected(self):
        self.replace_capacity_schema('id INTEGER NOT NULL, time_unit INTEGER NOT NULL REFERENCES time_unit(id), '
                                     'used FLOAT NOT NULL, workcenter INTEGER REFERENCES workcenter(id)')
        result = check(self.db)
        self.assertFalse(result['ok'])
        self.assertIn('primary key schema: capacity.id', result['errors'])

    def test_nullability_schema_is_checked(self):
        self.replace_capacity_schema('id INTEGER NOT NULL PRIMARY KEY, time_unit INTEGER NOT NULL REFERENCES time_unit(id), '
                                     'used FLOAT, workcenter INTEGER REFERENCES workcenter(id)')
        result = check(self.db)
        self.assertFalse(result['ok'])
        self.assertIn('nullability schema: capacity.used', result['errors'])

    def test_unreadable_database_returns_structured_error(self):
        corrupt = self.folder / 'corrupt.db'
        corrupt.write_text('This is not a SQLite database.')
        missing = self.folder / 'missing.db'
        for path in (corrupt, missing):
            with self.subTest(path=path.name):
                self.assertFalse(check(path)['ok'])
                run = subprocess.run([sys.executable, str(Path(__file__).with_name('check_example.py')), str(path)],
                                     capture_output=True, text=True)
                self.assertEqual(run.returncode, 1)
                self.assertFalse(json.loads(run.stdout)['ok'])
                self.assertNotIn('Traceback', run.stdout + run.stderr)
        self.assertFalse(missing.exists())

    def test_negative_cases(self):
        for i, (sql, expected) in enumerate(NEGATIVE_CASES):
            with self.subTest(expected=expected):
                target = build(self.folder / f'negative-{i}')
                with closing(sqlite3.connect(target)) as conn:
                    conn.executescript(sql)
                result = check(target)
                self.assertFalse(result['ok'])
                self.assertIn(expected, ' '.join(result['errors']))


if __name__ == '__main__':
    unittest.main(verbosity=2)
