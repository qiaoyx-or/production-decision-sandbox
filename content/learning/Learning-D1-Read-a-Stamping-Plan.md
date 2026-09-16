# D1 Stamping Planning: Read Demand, Capacity and Materials Together

[中文](Learning-D1-Read-a-Stamping-Plan-zh-CN.md) · [Learning Center](Learning-Center.md)

## Trace Order Demand to Resources and Materials
A stamping plan must align demand by period with work-center capacity and material availability at each operation. This case uses `StampingWorkshop/data.db` and the `production_planning` orchestration recipe to examine those relationships through inputs, configuration and results.

The recorded run took place on 2026-08-31 using DecisioWorks v1.4.0 with commercial Enterprise authorization. The tables retain that run's parameters and measurements.

## Inputs Extend beyond an Order Table
| Object | Recorded size | Role |
|---|---:|---|
| Order details | 1,920 rows | Products, due times and quantities |
| Capacity | 50 rows | Resource availability by time |
| Operation-material relationships (ingredient) | 38 rows | Materials required at each operation |
| Material availability | 500 rows | Available quantities and timing |
| Time units | 25 | Shared input and output coordinate |
| Work centers | 3 | Resource scope |

Trace one order through its product, route, operations and eligible resources, then inspect material conditions. Use row counts to check import completeness, then verify references to confirm that orders connect to the intended resources and materials.

## Configuration and Processing
The record enables capacity, demand and material-availability constraints. Capacity is soft and inventory constraints are disabled. Baseline weights are job_bias=-0.001 and waittime=1.0. The request uses 16 threads and a 120-second limit. These describe the recorded run; current use follows the installed release and authorization.

Actions acquire data, parse constraints, generate and select a solution, evaluate it and optionally output results. Persistence uses a separate result file rather than overwriting the standard business database.

## Read the Comparison
| Item | Baseline | Adjusted |
|---|---:|---:|
| job_bias weight | -0.001 | -0.003 |
| waittime weight | 1.0 | 2.0 |
| API status | ok | ok |
| API elapsed seconds | 14.41 | 14.29 |
| Result rows | 66 | 66 |
| Total demand/output | 680500/680500 | 680500/680500 |
| Final shortage | 0 | 0 |
| Weighted job_bias contribution | -7854.678 | -23564.034 |

The baseline reports available capacity of 1188000, processing load of 371588.48 and planned load including setup and waiting of 377080.42, with reported utilization around 31.74%. These retain the report's measurement basis and are not converted to minutes here.

Both runs selected candidates that passed the recorded validity checks. Here, “best” means the selected candidate from that run, without a claim of proven global optimality. The listed aggregates are unchanged. Match rows by business identifiers to compare quantities and completion times, then check those times against due dates. As two weights changed together, this record describes their combined adjustment.

## Keep Screenshot and API Evidence Separate
The reference includes actual input, baseline and comparison screenshots. Those page runs used two threads and 60 seconds and form a separate execution group. Keep each group's configuration and results together rather than inserting screenshot values into the API table.

## Exercise and Review
**Reading exercise: check two values using only the figures above.**

| Check | Hand calculation | Interpretation |
|---|---|---|
| Overall utilization | 377080.42 ÷ 1188000 × 100 ≈ 31.74% | Matches the reported aggregate; period-level detail is still needed to identify local overload |
| Planned minus processing load | 377080.42 − 371588.48 = 5491.94 | Under the report's definitions, the difference involves setup and waiting; it does not separate their individual values |

These calculations use the published record and retain its original load units. The table supplies no conversion to minutes.

A suitable conclusion is: “Both runs report total output of 680500 and zero final shortage. Those two quantity measures agree. On-time completion, local overload and task-timing changes require detailed records.”

**Runtime exercise: obtain the detailed results first.** Within one run group, choose a work center and period. Record demand, capacity, materials, output and open questions. If only aggregates are available, mark this step as awaiting detail rather than inferring missing rows.

For a follow-up comparison, change only waittime. Hold data, constraints, other objectives and computing conditions constant, and check the effective objective configuration. Save the new run's status, results and detailed differences before assessing the effect.

## Further Reading

[Stamping Planning Case](https://github.com/qiaoyx-or/decisioworks/wiki/Stamping-Planning-Case-Walkthrough) · [Injection-Molding Scheduling Case](https://github.com/qiaoyx-or/decisioworks/wiki/Injection-Molding-Scheduling-Case-Walkthrough) · [End-to-End Scenario](https://github.com/qiaoyx-or/decisioworks/wiki/End-to-End-Scenario-Walkthrough) · [Scenarios and Pain Points](https://github.com/qiaoyx-or/decisioworks/wiki/Scenarios-and-Pain-Points)

Worksheets: [Worksheet: Baseline and Adjusted Plan Comparison](Worksheet-Plan-Comparison.md)

[Topic D](Learning-Topic-D-Read-Real-Planning-Cases.md) · [Previous: Turn Shop-Floor Experience into Checkable Rules](Learning-C3-Turn-Experience-into-Rules.md) · [Next: Injection Molding: Explain Attributes and Changeovers](Learning-D2-Read-Injection-Molding-Changeovers.md)
