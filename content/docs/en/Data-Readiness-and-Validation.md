**English** | [中文](Data-Readiness-and-Validation-zh-CN)

> Applies to DecisioWorks v1.4.0

# Data readiness and validation: from importable to decision-ready

Readable data proves only that files and fields are accessible. It does not prove that business relationships are correct or that a model can solve the problem. DecisioWorks separates readiness into stages so defects appear before solver execution.

## Five Acceptance Layers

The table is a framework for reviewing data preparation, not a five-state enumeration returned in sequence by every API. Read the status together with the entry point, data version, and check scope. For example, acquisition modes `contract` and `engine_ready`, and catalog labels `contract_ready` and `solver_ready`, serve different checks.

| Layer | Question | Typical evidence |
|---|---|---|
| ContractReady | Are tables, fields, types, and identifiers recognizable? | Structure and required-field report |
| RelationReady | Do time, product, route, resource, and material links close? | Relationship report |
| ModelReady | Can business facts form model objects and structural constraints? | Capability and constraint inventory |
| SolverReady | Does the specified dataset-and-capability combination pass the entry point's integration checks? | Capability, configuration, and readiness report; assess solution feasibility from the actual run |
| DecisionReady | Can people explain, compare, and confirm the result? | Drill-down evidence and review record |

These layers check different risks. ContractReady does not replace relationship and capability checks. SolverReady does not guarantee that a new run will find a feasible solution or prove optimality.

## Check four relationship chains

1. **Time**: due dates, capacity, material readiness, and results share consistent `time_unit` references, fractions, and time units.
2. **Product**: order lines, routes, inventory, and attributes refer to the same product identity.
3. **Routing and capacity**: a product connects through its route, operations, and `process_adaptor` records to executable work centers.
4. **Materials**: operation-level material demand links to the corresponding material, inventory, or readiness records.

## Check values and units

- `capacity.used` is an occupied or unavailable fraction from 0 to 1. For example, 0.25 means 25% is already occupied or unavailable. It is an input, not utilization calculated from the new plan.
- Demand, batch size, and output per cycle use consistent output units. Continuous production also needs an explicit time basis.
- Processing times, due times, and calendars must specify their units.
- Objective weights express trade-offs; they are not physical workload, shortage, or time values.
- Enumerations and status codes need an explicit mapping from the source system to the standard semantics.

## Handle validation failures

Failures should identify the object, field, or relationship and propose a repair direction. Mapping code must not silently invent defaults merely to make a solve pass. If a business default is approved, retain its source and assumption.

## Integrate ERP and MES data

Map business objects before system columns. Orders may come from ERP, execution and equipment states from MES, and inventory or incoming materials from WMS or procurement. The standardized interface brings them into shared semantics without making one source system an absolute APS prerequisite.

## Retain the acceptance record

Retain data version, mapping rules, row counts, relationship errors, units, readiness state, and unresolved issues. Confirm that the data and configuration are SolverReady before solving. This means the inputs are prepared; finding a feasible solution still depends on the constraints and the solving process.

Continue with the [Data Object and Field Reference](Data-Object-and-Field-Reference) and [ERP/MES Data Mapping Guide](ERP-MES-Data-Mapping-Guide).
