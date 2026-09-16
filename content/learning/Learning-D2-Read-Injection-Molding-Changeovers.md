# D2 Injection Molding: Explain Attributes and Changeovers

[中文](Learning-D2-Read-Injection-Molding-Changeovers-zh-CN.md) · [Learning Center](Learning-Center.md)

## Read the Sequence through Business Attributes
This lesson examines the existing 2026-08-31 v1.4.0 Enterprise run for InjectionMoldingWorkshop/data.db. It explains how attributes affect sequencing and why objective scores and displayed counts need separate review.

| Input | Recorded content |
|---|---|
| Demand | 37 rows |
| Work centers | 2 available; this run selects work-center ID 2 |
| Materials | 115 |
| Process adaptors | 418 |
| Historical input results | 120 rows, separate from new output |
| Mappings | Color: color→property_1; cap type: cap_type→property_2; container volume: container_capacity→property_3 |

container_capacity describes the product's container volume. The sample objective named capacity relates to this attribute, not to machine availability.

## Configuration Defines the Comparison
The circular-sequence configuration uses 40 positions and three cycles. Capacity, demand, inventory, sequence-changeover and circular-changeover constraints are enabled. Local scheduling receives work whose material conditions have been confirmed upstream. Preprocessing checks integer fields and batch multiples and stops on inconsistency.

Sequence changes concern adjacent task colors. Circular changes relate to container-capacity states across reused cycles. Keep those definitions separate rather than labeling their sum as a number of mold changes.

## Read the Recorded A/B Results
Both API requests use 16 threads and a 60-second limit. Both return `ok`, select a candidate that passed the recorded validity checks and produce 120 new result rows. Selecting a candidate is distinct from proving global optimality.

| Item | Baseline | Adjusted |
|---|---:|---:|
| color weight | 0.1 | 0.8 |
| capacity weight | 1.0 | 1.5 |
| Sequence changes | 41 | 46 |
| Circular changes | 6 | 14 |
| Weighted changeover cost | 14.9 | 66.4 |
| Total API elapsed seconds | 66.57 | 66.50 |

API elapsed time includes outer processing and is not pure solver time. The scores use different weights, so they do not directly yield an improvement percentage. Displayed counts and model scoring use different definitions. This case's scoring also involves transitions between empty and occupied positions. Reproducing 14.9 therefore requires the raw objective values, not just the displayed counts of 41 and 6. “Weighted cost” is an objective score, not a monetary expense.

## Interpret This Adjustment
Both changeover counts increased after the combined weight adjustment. The recorded direction audits passed, meaning that objective directions and mappings met those checks, rather than that business performance improved. Inspect each cycle and the scoring details to locate the attribute changes that incurred costs. To study color alone, hold the capacity weight constant in a separate comparison.

The reference screenshots and API evidence belong to separate run groups. Failure at two threads and success at 16 in the recorded environment is an observation about that environment, not a universal thread threshold.

## Exercise and Review
**Reading exercise: explain what happened to the two change counts.**

| Check | Hand calculation | Supported observation |
|---|---|---|
| Sequence-change difference | 46 − 41 = 5 | Five more changes after adjustment |
| Circular-change difference | 14 − 6 = 8 | Eight more changes after adjustment |

A suitable conclusion is: “After both weights changed, sequence and circular change counts increased. On these two displayed measures, the adjustment did not reduce changes. Further assessment requires sequences, raw objective measures and business requirements.” Report the counts separately, rather than combining them into mold changes. Scores of 14.9 and 66.4 use different weights and do not establish an improvement percentage.

**Runtime exercise: design and execute a color-only comparison.** Hold the data version, capacity weight, constraints, work center, 40×3 structure and computing limits constant. Keep actual status, full sequences, both change counts and objective measures.

If totals match, inspect cycles, positions and products. If no usable plan appears, inspect the stopping reason. This single-variable experiment requires a separate run; the combined-adjustment record above cannot supply its results.

## Further Reading

[Stamping Planning Case](https://github.com/qiaoyx-or/decisioworks/wiki/Stamping-Planning-Case-Walkthrough) · [Injection-Molding Scheduling Case](https://github.com/qiaoyx-or/decisioworks/wiki/Injection-Molding-Scheduling-Case-Walkthrough) · [End-to-End Scenario](https://github.com/qiaoyx-or/decisioworks/wiki/End-to-End-Scenario-Walkthrough) · [Scenarios and Pain Points](https://github.com/qiaoyx-or/decisioworks/wiki/Scenarios-and-Pain-Points)

Worksheets: [Worksheet: Baseline and Adjusted Plan Comparison](Worksheet-Plan-Comparison.md)

[Topic D](Learning-Topic-D-Read-Real-Planning-Cases.md) · [Previous: Stamping Planning: Read Demand, Capacity and Materials Together](Learning-D1-Read-a-Stamping-Plan.md) · [Next: Choose Cases by Their Data Characteristics](Learning-D3-Select-Cases-by-Data-Characteristics.md)
