# C1 Distinguish Facts, Constraints and Preferences

[中文](Learning-C1-Facts-Constraints-and-Preferences-zh-CN.md) · [Learning Center](Learning-Center.md)

## One Shop-Floor Request Can Contain Several Decisions
“Give this machine less work today and prioritize a key customer” combines potentially different meanings. The first part may reflect maintenance or a risk preference. The second may mean a firm delivery commitment or a sequencing preference. Clarifying the reason prevents every judgment from becoming a permanent restriction.

Use six statements from a teaching workshop.

| Statement | Initial classification | Clarify |
|---|---|---|
| WC-1 can only process A | Resource and routing fact | Approved alternative routes |
| WC-1 has two hours of maintenance today | Calendar fact | Whether capacity already reflects it |
| Schedule at most 300 units of A today | Management rule or model constraint | Reason, object and effective period |
| Prefer fewer color changes | Objective preference | Color mapping, changeover measure and optimization direction |
| Keep started tasks unchanged | Execution-stability rule | Frozen fields and duration |
| Approve overtime when overloaded | Operational action | Approver and additional availability |

## Map the Meaning to the Toolkit
The standardized interface represents processes, resources, calendars, quantities and materials. objective_system organizes objective direction, weights and scope. marginal_control handles explicit rules, allowances and operational control information. A rule also needs appropriate adaptation and execution checks to affect solving.

Classify by meaning, not wording. A 300-unit limit caused by physical capability belongs in resource data. The same limit arising from a current allocation agreement needs a scope and expiry. Its origin determines how it should be maintained.

## Separate Hard Conditions from Costs
A hard condition must hold for every accepted plan. A soft condition allows deviation and represents its cost through defined penalties or objective measures. Soft capacity can produce an overloaded candidate; the user needs to see the affected resource and period and decide how it could be handled.

Objective weights do not automatically enlarge the feasible set. If every commitment has a hard deadline and resources are insufficient, increasing a delivery weight cannot resolve the conflict.

## Prepare a Configuration Record
For each requirement, record the original statement, confirmed meaning, data or configuration location, scope, owner and review method. Keep the business rationale readable while retaining exact field and interface names.

After changing a rule, check whether the same limit remains in data, a recipe or the application. Duplicated restrictions can explain why relaxing one setting appears to have no effect.

## Exercise and Suggested Answer
Split “prioritize the urgent order without changing started work” into two requirements. Specify the urgent order and its deadline, then define what remains frozen. If they conflict, show the resource and period conflict and ask the responsible person which commitment can change.

Produce a requirements classification table. A reader should understand why each item belongs where it does and who updates it when the business changes.

## Further Reading

[Objectives and Rule Control](https://github.com/qiaoyx-or/decisioworks/wiki/Objectives-and-Rule-Control) · [Controlled Solving and Engine Adapters](https://github.com/qiaoyx-or/decisioworks/wiki/Controlled-Solving-and-Engine-Adapters) · [Trusted Operation and Human Review](https://github.com/qiaoyx-or/decisioworks/wiki/Trusted-Operation-and-Human-Review)

Worksheets: [Worksheet: Baseline and Adjusted Plan Comparison](Worksheet-Plan-Comparison.md) · [Worksheet: Operational Rule and Verification](Worksheet-Operational-Rule.md)

[Topic C](Learning-Topic-C-Objectives-and-Operational-Rules.md) · [Previous: Align Time, Capacity and Material Availability](Learning-B3-Align-Time-Capacity-and-Materials.md) · [Next: Explain the Trade-Offs between Objectives](Learning-C2-Explain-Objective-Tradeoffs.md)
