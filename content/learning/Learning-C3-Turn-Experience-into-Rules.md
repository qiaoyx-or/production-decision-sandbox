# C3 Turn Shop-Floor Experience into Checkable Rules

[中文](Learning-C3-Turn-Experience-into-Rules-zh-CN.md) · [Learning Center](Learning-Center.md)

## Experience Needs an Object, Scope and Reason
“Give this unreliable machine less work” contains useful judgment but lacks an executable definition. Specify affected products and periods, the reduction and the review date. Clear rules make experience easier to reuse, review and discuss.

| Rule record | Teaching example |
|---|---|
| Object | WC-2, today's second period |
| Basis | A confirmed equipment-condition check |
| Measure | Use an approved allocation limit |
| Validity | This period; renew or remove after review |
| Owners | Equipment owner confirms facts; planning owner confirms allocation |
| Checks | Limit input, actual allocation and exceptions |

Use the record to confirm the rule's meaning, then map it to the fields required by the selected interface.

## Locate marginal_control
The `marginal_control` module represents operational rules and control requirements and produces impact analysis. The `marginalization_analysis` orchestration recipe demonstrates `boundary_control`: object keys identify the control scope, `lower_bound` and `upper_bound` set limits, and `variable_indices` identifies the corresponding optimization variables.

`variable_indices` identifies variable positions, not production quantities. An `upper_bound` of 300 means at most 300 units only when the selected variable represents that object's production quantity in those units. Confirm the object mapping, variable units and model support before applying the rule.

## Follow Four Checkpoints
1. **Expression:** the record identifies source, object, validity and units.
2. **Analysis:** the control input is parsed and its report matches the object.
3. **Application:** check that the capability or adapter reads the rule and adds it to the model or follow-up processing.
4. **Result:** compare constraint settings, execution records and object-level results. A result that happens to satisfy a limit does not by itself establish that the limit was applied.

This analysis recipe produces a control report. To affect solving, the appropriate capability must also apply the rule as an objective-change proposal or an explicit constraint; other signals may become tasks for a person. Trace the report, configuration and execution records to establish what was actually applied.

## Handle Conflict and Expiry
A new limit may conflict with delivery requirements. Keep the affected objects, periods and quantities visible, then consider alternative resources, later delivery or other measures. When rules coexist, state priority and approval arrangements rather than silently overwriting a conflict.

Review rules when they expire. If a temporary equipment problem ends but its restriction remains, the system continues using obsolete conditions. Managing the rule's lifetime is part of operational governance.

## Exercise and Suggested Answer
Turn “prioritize the key customer” into a rule record and describe a possible conflict with frozen work. Decide whether priority means a preference or a mandatory resource or timing condition.

Provide one normal check and one counterexample, such as the restriction no longer applying after expiry. If the current interface only produces a recommendation, describe it as awaiting confirmation rather than as a completed adjustment.

## Further Reading

[Objectives and Rule Control](https://github.com/qiaoyx-or/decisioworks/wiki/Objectives-and-Rule-Control) · [Controlled Solving and Engine Adapters](https://github.com/qiaoyx-or/decisioworks/wiki/Controlled-Solving-and-Engine-Adapters) · [Trusted Operation and Human Review](https://github.com/qiaoyx-or/decisioworks/wiki/Trusted-Operation-and-Human-Review)

Worksheets: [Worksheet: Baseline and Adjusted Plan Comparison](Worksheet-Plan-Comparison.md) · [Worksheet: Operational Rule and Verification](Worksheet-Operational-Rule.md)

[Topic C](Learning-Topic-C-Objectives-and-Operational-Rules.md) · [Previous: Explain the Trade-Offs between Objectives](Learning-C2-Explain-Objective-Tradeoffs.md) · [Next: Stamping Planning: Read Demand, Capacity and Materials Together](Learning-D1-Read-a-Stamping-Plan.md)
