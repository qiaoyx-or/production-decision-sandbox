"""Recalculate the single-product, two-operation teaching candidate, not a schedule."""
import argparse
import csv
import json
import math
import sqlite3
from contextlib import closing
from pathlib import Path

from check_example import check


class InputError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InputError(message)


def quantity(value, label):
    require(type(value) in (int, float) and math.isfinite(value) and value >= 0,
            f'{label}: expected a finite nonnegative number')
    return value


def preflight(folder, conn):
    validation = check(folder / 'data.db')
    require(validation['ok'], 'data.db: ' + '; '.join(validation['errors']))
    facts = json.loads((folder / 'scenario.json').read_text(encoding='utf-8'))
    require(isinstance(facts, dict), 'scenario.json: expected an object')
    periods = conn.execute('SELECT id,scale,status FROM time_unit ORDER BY offset').fetchall()
    require(periods and all(p[2] == 1 for p in periods),
            'time_unit: this exercise requires normal production periods (status=1)')
    issues = facts.get('period_issues')
    require(isinstance(issues, list) and len(issues) == len(periods),
            f'scenario.json.period_issues: expected {len(periods)} entries in time_unit.offset order')
    for i, value in enumerate(issues):
        quantity(value, f'scenario.json.period_issues[{i}]')
    quantity(facts.get('opening_finished_stock'), 'scenario.json.opening_finished_stock')
    require(facts.get('time_unit') == 'seconds', 'scenario.json.time_unit: expected seconds')
    require(conn.execute('SELECT id FROM product').fetchall() == [(1,)],
            'product: this exercise supports only product id=1')
    routes = conn.execute('SELECT id FROM process_route WHERE product=1').fetchall()
    require(len(routes) == 1, 'process_route: this exercise requires one route')
    operations = conn.execute('SELECT id,seqno FROM process WHERE route=? ORDER BY seqno', routes[0]).fetchall()
    require(len(operations) == 2 and operations[0][1] < operations[1][1],
            'process: this exercise requires two sequential operations with distinct seqno')
    require(not conn.execute('SELECT 1 FROM shared_resource LIMIT 1').fetchone(),
            'shared_resource: shared resources require a different calculation/model')
    require(not conn.execute('SELECT 1 FROM material WHERE substitute IS NOT NULL OR binding IS NOT NULL LIMIT 1').fetchone(),
            'material: substitutes and joint use require a different calculation/model')
    adaptors = {}
    for process, _ in operations:
        rows = conn.execute('SELECT workcenter,productivity,processing_time,setup_time,OEE,binding FROM process_adaptor WHERE process=?', (process,)).fetchall()
        require(len(rows) == 1, f'process_adaptor: process={process} requires exactly one adaptor')
        resource, productivity, duration, setup, oee, binding = rows[0]
        require(setup == 0 and oee == 100 and binding is None,
                f'process_adaptor: process={process} requires setup_time=0, OEE=100 and no binding')
        adaptors[process] = (resource, productivity, duration)
    require(len({a[0] for a in adaptors.values()}) == 2,
            'process_adaptor: the two operations need distinct resources for this exercise')
    for time, _, _ in periods:
        bounds = conn.execute('SELECT lower_bound_acc,upper_bound_acc FROM inventory_limit WHERE product=1 AND time_unit=?', (time,)).fetchall()
        require(len(bounds) == 1, f'inventory_limit: expected one row for product=1, time_unit={time}')
        for resource, _, _ in adaptors.values():
            rows = conn.execute('SELECT used FROM capacity WHERE time_unit=? AND workcenter=?', (time, resource)).fetchall()
            require(len(rows) == 1, f'capacity: expected one row for workcenter={resource}, time_unit={time}')
    candidate = []
    seen = set()
    with (folder / 'manual_candidate.csv').open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        require(reader.fieldnames == ['workcenter', 'time_unit', 'process', 'number'],
                'manual_candidate.csv: expected workcenter,time_unit,process,number columns')
        for line, row in enumerate(reader, 2):
            try:
                row = {k: int(v) for k, v in row.items()}
            except (TypeError, ValueError):
                raise InputError(f'manual_candidate.csv line {line}: all four values must be integers') from None
            require(row['number'] >= 0, f'manual_candidate.csv line {line}: negative output')
            require(row['time_unit'] in {p[0] for p in periods}, f'manual_candidate.csv line {line}: unknown time_unit')
            adaptor = adaptors.get(row['process'])
            require(adaptor is not None and row['workcenter'] == adaptor[0],
                    f'manual_candidate.csv line {line}: process/workcenter does not match the route')
            require(row['number'] % adaptor[1] == 0,
                    f'manual_candidate.csv line {line}: output must be a multiple of productivity')
            key = row['time_unit'], row['process'], row['workcenter']
            require(key not in seen, f'manual_candidate.csv line {line}: duplicate resource/period/operation')
            seen.add(key)
            candidate.append(row)
    require(candidate, 'manual_candidate.csv: provide at least one candidate row')
    return facts, periods, operations, adaptors, candidate


def calculate(folder):
    folder = Path(folder).resolve()
    scope = {'evidence_type': 'manual_candidate_recalculation', 'solver_executed': False,
             'full_scheduling_feasibility_proven': False, 'demand_coverage_checked': False,
             'not_checked': ['order_allocation_and_on_time_delivery', 'detailed_scheduling_feasibility',
                             'batch_dispatch_and_WIP_limits', 'advanced_resource_or_material_rules']}
    try:
        with closing(sqlite3.connect((folder / 'data.db').as_uri() + '?mode=ro', uri=True)) as conn:
            facts, periods, operations, adaptors, candidate = preflight(folder, conn)
            details, materials, inventories, comparisons = [], [], [], []
            supply, consumption = {}, {}
            cumulative_output = cumulative_issues = 0
            for position, (time, scale, _) in enumerate(periods):
                for material, number in conn.execute('SELECT material,number FROM kitting_information WHERE time_unit=?', (time,)):
                    supply[material] = supply.get(material, 0) + number
                operation_output = {p[0]: 0 for p in operations}
                for row in (r for r in candidate if r['time_unit'] == time):
                    resource, productivity, duration = adaptors[row['process']]
                    used = conn.execute('SELECT used FROM capacity WHERE time_unit=? AND workcenter=?', (time, resource)).fetchone()[0]
                    cycles = row['number'] // productivity
                    details.append({**row, 'cycles': cycles, 'processing_minutes': cycles * duration / 60,
                                    'available_minutes': scale * (1 - used) / 60})
                    operation_output[row['process']] += row['number']
                    for material, coefficient in conn.execute('SELECT material,number FROM ingredient WHERE process=?', (row['process'],)):
                        consumption[material] = consumption.get(material, 0) + row['number'] * coefficient
                require(len(set(operation_output.values())) == 1,
                        f'manual_candidate.csv time_unit={time}: this exercise requires equal output of both operations in each period (no opening WIP)')
                for material in sorted(set(supply) | set(consumption)):
                    available, used = supply.get(material, 0), consumption.get(material, 0)
                    materials.append({'time_unit': time, 'material': material, 'cumulative_supply': available,
                                      'cumulative_consumption': used, 'within_supply': used <= available})
                cumulative_output += operation_output[operations[-1][0]]
                cumulative_issues += facts['period_issues'][position]
                stock = facts['opening_finished_stock'] + cumulative_output - cumulative_issues
                low, high = conn.execute('SELECT lower_bound_acc,upper_bound_acc FROM inventory_limit WHERE product=1 AND time_unit=?', (time,)).fetchone()
                inventories.append({'time_unit': time, 'cumulative_output': cumulative_output,
                                    'ending_inventory': stock, 'within_bounds': stock >= 0 and
                                    (low is None or low <= cumulative_output) and (high is None or cumulative_output <= high)})
                demand = conn.execute('SELECT coalesce(sum(number),0) FROM order_item WHERE product=1 AND delivery_time=?', (time,)).fetchone()[0]
                comparisons.append({'time_unit': time, 'order_demand': demand,
                                    'assumed_issues': facts['period_issues'][position],
                                    'difference': facts['period_issues'][position] - demand})
            chain = sum(d['processing_minutes'] for d in details if d['time_unit'] == periods[0][0])
        return {**scope, 'ok': True, 'errors': [], 'workload': details, 'materials': materials,
                'inventory': inventories, 'demand_issue_comparison': comparisons,
                'issues_match_due_quantities': all(c['difference'] == 0 for c in comparisons),
                'aggregate_checks_passed': all(d['processing_minutes'] <= d['available_minutes'] for d in details)
                    and all(m['within_supply'] for m in materials) and all(i['within_bounds'] for i in inventories),
                'chain_assumptions': 'first_period_hypothetical_120_or_180_minute_start_maintenance_then_serial_operations_without_overlap',
                'baseline_no_overlap_chain_minutes': 120 + chain,
                'three_hour_maintenance_chain_minutes': 180 + chain}
    except (InputError, OSError, sqlite3.Error, json.JSONDecodeError, csv.Error) as exc:
        return {**scope, 'ok': False, 'aggregate_checks_passed': False, 'errors': [str(exc)]}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder')
    result = calculate(parser.parse_args().folder)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['aggregate_checks_passed'] else 1)
