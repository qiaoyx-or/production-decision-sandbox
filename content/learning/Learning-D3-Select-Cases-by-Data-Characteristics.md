# D3 Choose Cases by Their Data Characteristics

[中文](Learning-D3-Select-Cases-by-Data-Characteristics-zh-CN.md) · [Learning Center](Learning-Center.md)

## An Industry Name Provides Context
Within machining, one case may allocate daily quantities, another sequence multiple operations, and a third focus on batch sizes and subcontracting. Select an example from the decision and available data rather than the industry label alone.

Start by describing the production structure below, then compare the data requirements and model capabilities.

## Build a Scenario Profile
| Dimension | Record | Why it matters |
|---|---|---|
| Decision granularity | Period quantities or precise sequence | Planning and scheduling use different capabilities |
| Process structure | Fixed routes, alternatives or cyclic sequences | Determines model structure |
| Resources | Single machines, parallel resources, shared tooling | Defines resource relationships |
| Batches | Fixed sizes, multiples and multiple outputs | Affects quantities and integer consistency |
| Changeovers | Color, specification, tooling and direction | Requires attribute mappings and changeover-cost definitions |
| Time | Shifts, maintenance, due dates and frozen work | Defines windows and stability |
| Materials | Operation consumption, arrivals and inventory | Determines upstream checks or modeled conditions |

Keep the profile concise but identify a supporting table, field or business confirmation. A dataset without shared-tooling information cannot be assumed to enforce that restriction because of its industry.

## Transfer from a Similar Case
The stamping sample teaches period demand, capacity and material checks. The injection sample teaches attribute-driven circular sequencing. Compare these structures before replacing names and values.

| Match | Next step |
|---|---|
| Structure and constraints match | Integrate a copy, verify units and rules, then run |
| Structure matches but fields or mappings are missing | Complete the data before chain validation |
| A required rule lacks an effective interface | Define the extension and checks, then adapt a small scope |
| Decision structure differs substantially | Select another capability or model |

SolverReady refers to the dataset-and-capability combination and the scope of its report. It does not imply that any other model can solve the same data.

## Make a Selection
Teaching scenario X has daily demand, operation-level materials and capacity; its immediate question is daily quantities. Scenario Y has released tasks, color attributes and reused cycles; its question is ordering within those cycles. X can start with the planning example, Y with circular sequencing. If Y also includes complex reentrant routes, confirm whether the model represents them.

## Exercise and Review
First profile X and Y above: select period-quantity planning for X and a circular-sequence case for Y, listing the conditions still to confirm for each.

When datasets are available, profile three and identify the closest existing example for each. List reusable parts, required changes and unresolved conditions.

Base the answer on data relationships and decision structure. “Both make automotive parts” does not establish fit. Shared resource, time or changeover structures provide a testable basis for reuse.

## Further Reading

[Stamping Planning Case](https://github.com/qiaoyx-or/decisioworks/wiki/Stamping-Planning-Case-Walkthrough) · [Injection-Molding Scheduling Case](https://github.com/qiaoyx-or/decisioworks/wiki/Injection-Molding-Scheduling-Case-Walkthrough) · [End-to-End Scenario](https://github.com/qiaoyx-or/decisioworks/wiki/End-to-End-Scenario-Walkthrough) · [Scenarios and Pain Points](https://github.com/qiaoyx-or/decisioworks/wiki/Scenarios-and-Pain-Points)

Worksheets: [Worksheet: Baseline and Adjusted Plan Comparison](Worksheet-Plan-Comparison.md)

[Topic D](Learning-Topic-D-Read-Real-Planning-Cases.md) · [Previous: Injection Molding: Explain Attributes and Changeovers](Learning-D2-Read-Injection-Molding-Changeovers.md) · [Next: From the Master Plan to Work Release and Scheduling](Learning-E1-Master-Plan-to-Work-Release.md)
