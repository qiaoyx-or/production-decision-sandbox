**English** | [中文](ERP-MES-Data-Mapping-Guide-zh-CN)

> Applies to DecisioWorks v1.4.0

# ERP/MES Data Mapping Guide

ERP, MES, WMS, spreadsheets, and equipment feeds can all provide source data. None is an automatic APS prerequisite. The key is to map source fields into stable business objects and relationships rather than copying source tables into a planning database.

## Four mapping layers

| Layer | Question | Example |
| --- | --- | --- |
| Source | Where is data maintained and how often does it change? | ERP order, MES route, WMS stock |
| Semantics | What does the field mean and what is its unit? | due date, work center, minute, quantity |
| Relationship | How do objects connect and close? | order to product, operation to resource |
| Solving | Which fields become constraints, objectives, or runtime input? | capacity, BOM, readiness, weight |

## Typical source mapping

| Source | Common objects | Key checks |
| --- | --- | --- |
| ERP | orders, products, BOM, purchasing, inventory | version, effective time, unit, due-date meaning |
| MES | routes, operations, equipment, reports, shifts | sequence, eligible resource, cycle time, state |
| WMS | inventory, lot, in-transit, location | available and frozen quantities, timestamp, substitution |
| Excel/CSV | temporary plans, manual rules, master-data supplements | ownership, version, nulls, duplicates |
| Equipment/IIoT | status, failure, output, energy | sampling rate, valid range, aggregation granularity |

## Four relationships that must close

1. Time: due dates, capacity, material readiness, and results share a planning coordinate.
2. Product: orders, products, routes, inventory, and properties connect.
3. Process-capacity: products and operations connect to work centers that have available capacity and valid calendars.
4. Operation-material: operations, material demand, inventory, and readiness connect.

## Integration checklist

Record source and target fields, transformation, unit, owner, update mode, traceable identifiers, enum rules, time rules, quantity rules, and null handling. Complete ContractReady, relationship-closure, and SolverReady checks before solving. When a source system changes, rerun mapping and regression tests.

## When ERP or MES is absent

Start with the standardized template and a minimum dataset owned jointly by business and data teams. Computable business facts matter more than first deploying a complete information system. Existing ERP/MES data requires the same semantic and relationship checks.

Continue with [Standardized Data Interface](Standardized-Data-Interface) and [Data Readiness and Validation](Data-Readiness-and-Validation).
