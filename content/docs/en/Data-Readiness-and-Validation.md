**English** | [中文](Data-Readiness-and-Validation-zh-CN)

> Applies to DecisioWorks v1.4.0

# Data readiness and validation: from importable to decision-ready

Readable data proves only that files and fields are accessible. It does not prove that business relationships are correct or that a model can solve the problem. DecisioWorks separates readiness into stages so defects appear before solver execution.

| State | Question | Typical evidence |
|---|---|---|
| ContractReady | Are tables, fields, types, and identifiers recognizable? | Structure and required-field report |
| RelationReady | Do time, product, route, resource, and material links close? | Relationship report |
| ModelReady | Can business facts form model objects and structural constraints? | Capability and constraint inventory |
| SolverReady | Can objectives, rules, and runtime settings form a solvable request? | Recipe check and objective-material audit |
| DecisionReady | Can people explain, compare, and confirm the result? | Drill-down evidence and review record |

These are acceptance states, not project-progress labels. A dataset may be ContractReady while missing the route, capacity, or objective material needed for SolverReady.

Validation follows four chains: a common time coordinate; consistent product identity; route-operation-resource closure; and operation-level material demand connected to availability. It also checks units and ranges. `capacity.used` is a 0-to-1 utilization ratio, objective weights are not physical quantities, and time or quantity fields require explicit units.

Failures should identify the object, field, or relationship and propose a repair direction. Mapping code must not silently invent defaults merely to make a solve pass. If a business default is approved, retain its source and assumption.

For ERP/MES integration, map business objects before system columns. Demand may come from ERP, execution state from MES, and availability from WMS or procurement. The standardized interface brings them into shared semantics without making one source system an absolute APS prerequisite.

Retain data version, mapping rules, row counts, relationship errors, units, readiness state, and unresolved issues. Only SolverReady datasets should appear as directly runnable scenarios.
