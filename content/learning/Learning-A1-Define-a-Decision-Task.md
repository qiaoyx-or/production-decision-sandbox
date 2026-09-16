# A1 Define a Decision Task from a Delivery Problem

[中文](Learning-A1-Define-a-Decision-Task-zh-CN.md) · [Learning Center](Learning-Center.md)

## Turn “Delivery Dates Keep Moving” into a Defined Task
A request to improve delivery performance is difficult to translate directly into model inputs. Identify the orders, planning period and resources, then state what may change. This gives data preparation and result review a shared subject.

Consider a teaching scenario: a workshop must produce three product families next week, and two work centers share some tooling. Start by defining the decisions, required data and approvals.

## Write a One-Page Scenario Brief
| Item | What to specify |
|---|---|
| Decision objects | Products and quantities from confirmed orders for next week |
| Choices to make | Production quantities by period and resource assignment |
| Fixed commitments | Confirmed due dates and work already started |
| Adjustable conditions | Timing and eligible resources for unreleased work |
| Resource conditions | Work centers, tooling sharing, shifts and maintenance |
| Material conditions | Availability, arrival times and operation requirements |
| Owners | Planning, resource-data and material-data owners |

Clarify what shared tooling means. Can only one machine use it at a time, or is there a daily usage allowance? These are different constraints. Allocating daily quantities also differs from setting exact start and finish times for every operation. Choose the required granularity first.

## Locate the Responsibility in DecisioWorks
DataSets and the standardized interface represent business facts. DecisioCore organizes data checks, objectives and rules. GOCK models and optimizes within those conditions. Web makes inputs and results visible. Select planning or scheduling, then check the objects and constraints that capability accepts.

For fewer changeovers, identify the attributes that define a change and how the model measures its count or setup time. For bottleneck protection, specify the resource, period, limit and how the model applies it. These definitions guide data integration and configuration.

## Define the Output
| Required output | How to review it |
|---|---|
| Plan by period and resource | Trace rows to orders, operations and work centers |
| Demand and delivery risks | Check quantities and completion times separately |
| Bottlenecks and trade-offs | Inspect resource, period and changeover details |
| Measures requiring approval | Identify overtime, later delivery or resource changes and their owners |

Define the denominator of demand fulfillment before running. Decide whether canceled orders are excluded. Without a shared definition, two readers may reach different conclusions from the same result.

## Exercise and Review
Rewrite “we need intelligent scheduling” as a one-page brief. Ask a colleague to name three conditions that could change the result.

A useful brief lets the colleague identify inputs, fixed commitments and permitted changes. Resolve uncertainty about time units, alternative resources or approval authority before proceeding. Keep the brief, object relationships and metric definitions as the common starting point for data and configuration work.

## Further Reading

[Value Validation and Adoption](https://github.com/qiaoyx-or/decisioworks/wiki/Value-Validation-and-Adoption-Framework) · [Typical Value Entry Scenarios](https://github.com/qiaoyx-or/decisioworks/wiki/Typical-Value-Entry-Scenarios)

Worksheets: [Worksheet: Scenario and Decision Task](Worksheet-Scenario-Brief.md) · [Worksheet: Baseline and Adjusted Plan Comparison](Worksheet-Plan-Comparison.md)

[Topic A](Learning-Topic-A-Problem-and-Validation.md) · [Next: Validate First: Design a Useful Planning Comparison](Learning-A2-Design-a-Useful-Planning-Comparison.md)
