# E2 Express Changes as Plan Deviations and Signals

[中文](Learning-E2-Deviations-to-Planning-Signals-zh-CN.md) · [Learning Center](Learning-Center.md)

## Describe the Change before Acting
“Material is late” describes an event. A planner also needs the affected orders, operations, quantities and periods. Link the event to business objects before selecting a response.

The teaching periods T1, T2 and T3 are in chronological order. Consider this event: material M was expected in T2 and is now confirmed for T3. Operation OP-1 needs it in T2. First inspect its task quantities and possible alternatives, then describe the planning impact.

## Distinguish Four Records
| Record | Purpose | Information in this example |
|---|---|---|
| Business change | Updated fact | M's arrival time and source |
| PlanBias | Impact relative to the plan | Objects, periods, direction and quantities |
| PlanSignal | Route impact to a recipient | Receiving capability, priority and proposed direction |
| Follow-up measure | Execution or pending confirmation | Release adjustment, proposed objective change, rule or coordination |

The table explains the business meaning of each record. When calling an interface, use its documented types and fields for the selected version.

## Follow the Linkage Recipe
The `planning_system_linkage` orchestration recipe performs planning and analysis before the `impact_analysis` action. Follow the planning analysis in `production_analysis.planning`, the linkage report in `planning_system.linkage_report`, and the `plan_biases` and `plan_signals` records to trace how the same business change is handled.

`PlanBias` is produced during execution and is managed separately from the standard input tables in `data.db`. For long-term storage, save it in the application's result records with the source-data version and run identifier.

## Keep the Decision between Signal and Action
A deviation may lead to monitoring, reduced near-term release, a proposed objective change or a purchasing check. Record the proposal, approval and actual handling separately so participants know who acts next.

Review the analysis output, recipient, adoption status and processing result in order. After an objective change is adopted, check the actual configuration and rerun. Until then, retain it as a proposal awaiting confirmation.

## Aggregate without Losing Traceability
One delay may affect several orders. Aggregation supports prioritization, but preserve the path from order to operation, material and period. If availability later recovers, distinguish updated records so the impact is not counted twice.

## Exercise and Suggested Answer
For the teaching event, identify affected objects, information sources, two possible measures and their approvers. Write an accurate statement when no measure has yet been executed.

For example: material risk has been identified for operation OP-1 in T2, and a proposed release-time change awaits the planning owner's confirmation. After execution, record the actual released tasks, timing and planning results to evaluate the measure.

## Further Reading

[Planning and Scheduling](https://github.com/qiaoyx-or/decisioworks/wiki/Planning-and-Scheduling-Overview) · [Results and Feedback](https://github.com/qiaoyx-or/decisioworks/wiki/Results-Evidence-and-Feedback) · [Component Responsibilities](https://github.com/qiaoyx-or/decisioworks/wiki/Component-Responsibilities)

Worksheets: [Worksheet: Operational Rule and Verification](Worksheet-Operational-Rule.md) · [Worksheet: Review and Change Record](Worksheet-Review-and-Change-Record.md)

[Topic E](Learning-Topic-E-Coordinate-Plans-and-Responses.md) · [Previous: From the Master Plan to Work Release and Scheduling](Learning-E1-Master-Plan-to-Work-Release.md) · [Next: Define the Scope of a Disruption Response](Learning-E3-Scope-a-Disruption-Response.md)
