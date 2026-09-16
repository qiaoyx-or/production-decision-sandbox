# B3 Align Time, Capacity and Material Availability

[中文](Learning-B3-Align-Time-Capacity-and-Materials-zh-CN.md) · [Learning Center](Learning-Center.md)

## “Capacity Is Available Today” Needs a Definition
A shift has 480 minutes, existing work uses 25%, and maintenance needs 30 minutes. How much remains? Check whether the 480 minutes already excludes maintenance, what the percentage uses as its denominator, and whether maintenance overlaps existing work.

For this hand-calculated teaching example, 480 minutes is gross shift time, the 25% is measured against it, and maintenance does not overlap existing work. Remaining time is 480 × (1−0.25) −30 = 330 minutes. This calculation applies to those assumptions; other capacity definitions require the corresponding conversion.

## Align Four Kinds of Time
| Information | Related object | Check |
|---|---|---|
| Order due time | order_item.delivery_time | Resolves to a time unit |
| Resource availability | capacity and shift/calendar data | Scope, scale and reductions are defined |
| Material availability | kitting_information.time_unit | Arrival timing and quantity units are clear |
| Plan output | planning_result.time_unit | Uses the same time axis as inputs |

time_unit.id is a reference identifier. offset and scale explain position and scale. Consecutive IDs do not automatically mean days and cannot be converted to minutes without the scenario's time definition.

## Keep Ratios, Quantities and Time Separate
capacity.used uses a ratio between zero and one: 25% is 0.25. Neither 25 nor 120 minutes expresses the same field meaning. Storage, calculation and percentage display need a consistent convention.

| Condition | Review |
|---|---|
| Shifts already produce net capacity | Check whether maintenance was already deducted |
| Parallel stations are included in capacity | Avoid multiplying station count again |
| Materials arrive tomorrow | Align arrival with the consuming operation, not just total demand |
| Results are needed in minutes | Establish the native unit and conversion first |

## Inspect a DecisioWorks Case
Read the time, capacity, material-availability and result tables. Select one work center and one time unit, then trace the related orders and materials. Inspect specific periods and key materials as well as total spare capacity to find shortages hidden by averages.

Use a data copy for changes. Modify one confirmed maintenance arrangement, inspect the capacity-generation rule and data difference, then run the corresponding planning capability. Review that period's load, waiting and unmet demand rather than relying on average utilization.

## Exercise and Suggested Answer
Under the 330-minute assumptions, a new task requiring 360 minutes leaves a 30-minute shortfall. Check whether additional time or another resource can be approved. Also inspect uninterrupted-processing requirements and maintenance windows so that any added time is actually usable for the task.

If the original 480 minutes already excluded maintenance, the calculation would be wrong. Keep the result together with its definitions so another reader can reproduce it under the same assumptions.

## Further Reading

[Standardized Data Interface](https://github.com/qiaoyx-or/decisioworks/wiki/Standardized-Data-Interface) · [Data Objects and Fields](https://github.com/qiaoyx-or/decisioworks/wiki/Data-Object-and-Field-Reference) · [Data Readiness and Validation](https://github.com/qiaoyx-or/decisioworks/wiki/Data-Readiness-and-Validation) · [ERP and MES Data Mapping](https://github.com/qiaoyx-or/decisioworks/wiki/ERP-MES-Data-Mapping-Guide)

Worksheets: [Worksheet: Scenario and Decision Task](Worksheet-Scenario-Brief.md)

[Topic B](Learning-Topic-B-Manufacturing-Data.md) · [Previous: Process Routes and Operation-Level BOMs](Learning-B2-Routes-and-Operation-Level-BOM.md) · [Next: Distinguish Facts, Constraints and Preferences](Learning-C1-Facts-Constraints-and-Preferences.md)
