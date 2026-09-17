# Worked Example: Inputs, Checks and Adjustments for 120 Brackets

[中文](Interface-Walkthrough-zh-CN.md) · [Learning guide](Interface-Guide.md)

[Download the complete exercise pack (SQL, field list, Python scripts, database and CSV files)](../../assets/data-interface/decisioworks-data-interface-examples.zip)

This example connects time, demand, routing, resources, materials and inventory through two operations: stamping and assembly. It produces a loadable teaching database, table files and quantity calculations, without changing your business database.

## 1. Business Conditions

| Item | Condition |
|---|---|
| Product | P-1 blue bracket |
| Order | 80 pieces in period 1 and 40 in period 2 |
| Time | Two normal eight-hour production periods, 28,800 seconds each |
| Stamping | Machine 11; four pieces per 600-second cycle; batch 20 |
| Assembly | Resource 12; one piece per 120-second cycle; batch 20 |
| Maintenance | Two hours unavailable on stamping in period 1; `used=0.25` |
| BOM | One blank per stamped piece; two fasteners per assembled piece |
| Supply | Initially 80 blanks and 160 fasteners; another 40 and 80 in period 2 |
| Finished inventory | Opening stock 20; ending range 20–100; issues of 80 and 40 |
| Simplifications | No scrap, no setup loss, OEE 100, no alternative resources |

The periods represent two production windows. When mapping real dates, also retain the planning origin, shift times and nonworking intervals.

## 2. Prepare the Files

From the supplied `examples` directory, use Python 3.10 or later. The base scripts use only the standard library. On Linux, use `python3` instead of `python` if that is how your environment is configured.

```bash
python build_example.py --output-dir ./my-first-example
python check_example.py ./my-first-example/data.db
python calculate_candidate.py ./my-first-example
python test_examples.py
```

The builder creates:

| File | Purpose |
|---|---|
| `data.db` | Teaching database with 18 standard tables |
| CSV named after each table | Inspect and compare inputs; the initial result CSV has only a header |
| `manual_candidate.csv` | Four manually constructed operation-output rows |
| `scenario.json` | Units, supply convention, opening inventory, independent per-period stock issues in `period_issues`, and simplifications |

An existing `data.db` stops the builder; choose another directory. You may also inspect the supplied [sample output](../../assets/data-interface/decisioworks-data-interface-examples.zip) before rebuilding from SQL. The business records are the same.

## 3. Check the Inputs

`check_example.py` should report `ok: true`, 18 tables and 105 fields. There are two order lines, two operations, two adaptors, four capacity rows, two BOM rows, four readiness rows and two inventory-limit rows.

`planning_result` has zero rows. The manual candidate is stored separately and is never written into the input database as an actual solver result.

Use this query in a SQLite viewer to inspect how demand reaches its operations:

```sql
SELECT oi.id AS order_line, p.code AS product_code,
       oi.delivery_time, oi.number AS demand_quantity,
       r.code AS route_code, op.code AS operation_code, op.seqno
FROM order_item oi
JOIN product p ON p.id = oi.product
JOIN process_route r ON r.product = p.id
JOIN process op ON op.route = r.id
ORDER BY oi.id, r.id, op.seqno;
```

The query returns four rows: each of two demand lines joins to two operations. Do not sum the repeated demand values into additional demand.

## 4. Load the Example into DecisioWorks

With DecisioWorks and its dependencies available, run from any directory:

```bash
python /path/to/examples/load_with_decisioworks.py /path/to/my-first-example/data.db --project-root /path/to/DecisioWorks
```

Replace the three paths with actual locations. The script sets up the project import paths, calls `load_business_data`, and runs `validate_batch_productivity_multiple`.

The verified loaded counts are `demand=2`, `process=2`, `capacity=4`, `bom=2`, `kitting=4` and `inventory_limit=2`, with preprocessing status `ok`. This confirms data-layer loading; the step does not execute a solver.

## 5. Recalculate the Manual Candidate

| Resource | Period | Operation | Output pieces | Cycles | Processing minutes |
|---:|---:|---|---:|---:|---:|
| 11 | 1 | Stamping | 80 | 20 | 200 |
| 12 | 1 | Assembly | 80 | 80 | 160 |
| 11 | 2 | Stamping | 40 | 10 | 100 |
| 12 | 2 | Assembly | 40 | 40 | 80 |

Stamping has 360 available minutes in period 1; all other resource-period combinations have 480. Cumulative consumption is 120 blanks and 240 fasteners, matching supply. Ending finished stock is 20 in each period; cumulative production is 80 and then 120.

The calculator should return `aggregate_checks_passed: true`. It also retains `solver_executed: false` and `full_scheduling_feasibility_proven: false`: the calculation checks aggregate relationships in this candidate, not every timing, transport, changeover or overlap condition.

`ok` means the inputs meet this calculator's requirements. `aggregate_checks_passed` covers resource, material and inventory totals. `demand_issue_comparison` lists order demand, assumed stock issues and their difference by period. `issues_match_due_quantities` compares those two quantity series only; it does not prove order allocation or on-time delivery, so `demand_coverage_checked` remains `false`. Missing records or unsupported inputs produce `ok: false`, diagnostic `errors` and a nonzero exit code.

## 6. Why Maintenance Changes Require Another Check

Build a separate exercise copy:

```bash
python build_example.py --output-dir ./three-hour-maintenance
```

Execute this SQL in the copy:

```sql
UPDATE capacity SET used=0.375
WHERE workcenter=11 AND time_unit=1;
```

Run validation and calculation again. Stamping availability falls to 300 minutes, still enough for its 200 processing minutes.

Now add these assumptions: maintenance occurs at shift start, all stamping finishes before assembly starts, and the operations do not overlap. Originally the chain needs 120+200+160=480 minutes. Longer maintenance raises it to 180+200+160=540 minutes. Individual resource totals passing their checks does not establish that the complete routing fits within eight hours.

Choose a business response: allow confirmed transfer-batch overlap, adjust supply and start times, revise delivery arrangements, or enable optional time. Run the appropriate scheduling capability with the selected conditions and check its actual output.

## 7. Move from the Exercise to Your Data

Begin with small changes that retain the example's object relationships. When changing due dates or the number of periods, follow [lesson 02](Interface-02-Demand.md) to update the issue plan, inventory limits, resource calendars, supply and candidate output together. Table CSV exports are for inspection; calculations read `data.db`. Record the source, units, expected change and check result.

This manual calculator supports product `id=1`, one route, two sequential operations on separate resources, one adaptor per operation, OEE100 and no setup loss. Quantities are discrete units, both operations produce equal quantities in each period, and there is no opening work in progress. All periods must be normal production periods. You can add periods using the complete procedure; alternate routes, shared resources, substitute materials, joint processing, optional time and advanced batch rules require another calculation or model. Batch dispatch, WIP capacity, order allocation and detailed timing feasibility need separate checks through the relevant model.

Changing demand does not automatically change the stock-issue assumptions in `scenario.json` or the output in `manual_candidate.csv`. Explain the difference before revising the order, issue plan or candidate. For a business case outside the stated scope, retain field and relationship checks and use the appropriate DecisioWorks model and run configuration rather than treating this manual report as full acceptance.

Useful review materials include input tables, source mappings, rule configuration, run records, result tables and before/after explanations. Use the [field reference](Interface-Fields.md) for storage details and the [semantic guide](Interface-Semantics.md) for business relationships.
