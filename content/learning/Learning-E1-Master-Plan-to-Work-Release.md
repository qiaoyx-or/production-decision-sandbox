# E1 From the Master Plan to Work Release and Scheduling

[中文](Learning-E1-Master-Plan-to-Work-Release-zh-CN.md) · [Learning Center](Learning-Center.md)

## Two Levels Answer Different Questions
Master production planning (MPS) coordinates what to produce, how much and in which periods. A release policy uses that plan together with resource and material readiness to determine which tasks enter scheduling. Scheduling then refines resources and sequence within confirmed tasks. Explicit handoff conditions let local scheduling focus on executable work.

In a teaching scenario, next week's demand is 100 units of A. Materials cover 60 units now; the remaining 40 must wait. Whether partial release is allowed depends on batch rules and commitments. Material availability alone does not authorize splitting the order.

## Check before Release
| Condition | Information to pass |
|---|---|
| Identity | Source order, product or task reference |
| Quantity | Released amount, unit and remaining demand |
| Time | Allowed start window, due date and frozen-work requirements |
| Resources | Work center or approved alternatives |
| Process and materials | Route, batches and upstream readiness confirmation |
| Traceability | Data and plan versions used |

These are business review dimensions. Use the actual interface definition for release-package fields. Preserve source references so scheduling feedback can be traced to the plan.

## Understand the DecisioWorks Handoff
planning_system organizes planning analysis and deviation signals into linkage information, which can support proposed objective or rule changes, release policies and scheduling inputs. Scheduling uses a model and constraints appropriate for local resources. In the standard injection sample, material conditions are confirmed upstream while local scheduling focuses on tasks and attribute changes.

Review successful scheduling together with satisfied release conditions. An incorrect upstream material confirmation cannot be repaired simply by inspecting the sequence.

## Keep Local Detail and Return Relevant Feedback
Scheduling may reveal changeover pressure, waiting or local load that was not explicit in the master plan. Return the impact by object and period, then consider release quantities, objectives or resources. Each level needs enough information for its decision, rather than every detail copied everywhere.

| Local observation | Useful upstream feedback |
|---|---|
| A resource cannot accommodate released work | Object, period and capacity gap |
| Changeover cost rises substantially | Task group, cost definition and grouping options |
| Material confirmation changes | Affected tasks and earliest availability |

## Exercise and Review
First identify the missing conditions. Is splitting allowed? What minimum size and multiples apply? Do resources, availability and delivery commitments permit partial release?

For a hand calculation, add explicit classroom assumptions: demand is 100 units of A and materials cover only 60. Partial releases use multiples of 20 with a minimum batch of 20. Resources and timing are confirmed, commitments permit partial release, and planning continues to track unreleased demand.

| Release policy | Release now (units) | Hold for later release (units) | Calculation or reason |
|---|---:|---:|---|
| Batches of 20 | 60 | 40 | Materials cover three 20-unit batches; other release conditions are confirmed |
| One full batch of 100 | 0 | 100 | Materials do not cover the full batch, so all demand remains unreleased |

These are release quantities calculated from stated assumptions, not a sequence or an actual solver result. If the minimum batch becomes 80, materials for 60 no longer permit the first release, even when other conditions are satisfied.

Complete a release record with source references, released quantity, remaining demand, time and resource scope, and the approver. Scheduling uses the released work; planning tracks the rest. Material-ready quantities that remain unreleased should not be recorded as work already started.

## Further Reading

[Planning and Scheduling](https://github.com/qiaoyx-or/decisioworks/wiki/Planning-and-Scheduling-Overview) · [Results and Feedback](https://github.com/qiaoyx-or/decisioworks/wiki/Results-Evidence-and-Feedback) · [Component Responsibilities](https://github.com/qiaoyx-or/decisioworks/wiki/Component-Responsibilities)

Worksheets: [Worksheet: Operational Rule and Verification](Worksheet-Operational-Rule.md) · [Worksheet: Review and Change Record](Worksheet-Review-and-Change-Record.md)

[Topic E](Learning-Topic-E-Coordinate-Plans-and-Responses.md) · [Previous: Choose Cases by Their Data Characteristics](Learning-D3-Select-Cases-by-Data-Characteristics.md) · [Next: Express Changes as Plan Deviations and Signals](Learning-E2-Deviations-to-Planning-Signals.md)
