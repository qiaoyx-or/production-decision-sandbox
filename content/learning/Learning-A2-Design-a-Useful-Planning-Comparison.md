# A2 Validate First: Design a Useful Planning Comparison

[中文](Learning-A2-Design-a-Useful-Planning-Comparison-zh-CN.md) · [Learning Center](Learning-Center.md)

One machine, two orders and a maintenance window. This small scenario illustrates why a plan comparison starts by explaining how conditions have changed, before interpreting a system's result.

This lesson develops three judgments: whether current conditions permit on-time completion, what a change affects, and which data, configuration or management decision could address it.

The exercise uses teaching data, with processing time and available capacity calculated by hand from the stated conditions. The second half uses existing recorded cases to explain how to conduct a similar comparison in DecisioWorks.

## 1. State the Decision

Two orders must be completed today on work center WC-1. Each product has one operation and can only use WC-1. The machine processes one batch at a time. All required materials and other resources are available. Both orders are due by the end of today.

The exercise has only one planning period: today. Production cannot be moved to an earlier period. Each product forms one complete batch that runs continuously. No initial setup is needed. Changing from A to B or B to A takes 40 minutes and occupies WC-1. There are no other changeovers.

The baseline uses today's normal working time, the stated quantities and the specified process. Overtime, alternative equipment, batch splitting and later delivery require separate decisions and have not been included.

## 2. Input Data

### Orders and Processing Conditions

| Order | Product | Quantity (units) | Processing time (minutes/unit) | Work center | Due |
|---|---|---:|---:|---|---|
| O-1 | A | 20 | 10 | WC-1 | End of today |
| O-2 | B | 20 | 11 | WC-1 | End of today |

### Calendar and Change

| Condition | Baseline | With maintenance |
|---|---:|---:|
| Gross shift time before maintenance (minutes) | 480 | 480 |
| Planned maintenance (minutes) | 0 | 30 |
| Net available time (minutes) | 480 | 450 |
| One changeover between products (minutes) | 40 | 40 |

Maintenance occurs before production starts, leaving 450 continuous minutes. If it occurred in the middle of production, the exercise would also need to check whether continuous batches fit around the maintenance window. Total available time alone would answer only part of that question.

These business tables explain the calculation. When preparing `data.db`, also provide the object identifiers, time units and process-resource relationships required by the standard interface.

## 3. Separate Facts, Constraints and Possible Measures

| Category | In this exercise | Meaning |
|---|---|---|
| Business facts | Order quantities, processing times and maintenance period | Conditions that the data must represent accurately |
| Required conditions | All quantities completed today, no overlapping use of the machine, continuous batches | The basis for assessing whether current commitments can be met |
| Preferences to compare | Sequence choices or other supported objectives among feasible plans | Trade-offs to examine when feasible alternatives exist |
| Measures requiring approval | Overtime, later delivery, alternative resources or batch changes | Options whose practical feasibility must be confirmed before updating data and configuration |

Hard constraints prohibit violations. Soft constraints allow deviations at a defined cost. If capacity is modeled as a soft constraint and a candidate plan is returned, inspect whether it includes overload and how that overload would be handled in practice.

## 4. Check the Arithmetic First

Product A requires `20 × 10 = 200` minutes. Product B requires `20 × 11 = 220` minutes. Including one 40-minute changeover, total occupancy is 460 minutes.

| Check | Baseline | With maintenance |
|---|---:|---:|
| Processing time (minutes) | 420 | 420 |
| Changeover time (minutes) | 40 | 40 |
| Total occupancy (minutes) | 460 | 460 |
| Net available time (minutes) | 480 | 450 |
| Spare time or shortfall (minutes) | 20 spare | 10 short |

The baseline has a simple feasible sequence: run A for 200 minutes, change over for 40 minutes, then run B for 220 minutes. The total is 460 minutes. After maintenance is added, either sequence still needs 460 minutes, but only 450 continuous minutes are available. Under the stated conditions, both full-quantity and same-day commitments cannot be met together.

This conclusion applies to the simplified conditions of this exercise. Multiple operations, alternative resources, batch splitting and different calendars require additional relationship and time-window checks.

## 5. Apply the Method in DecisioWorks

Choose the existing [stamping planning case](https://github.com/qiaoyx-or/decisioworks/wiki/Stamping-Planning-Case-Walkthrough) or [injection-molding scheduling case](https://github.com/qiaoyx-or/decisioworks/wiki/Injection-Molding-Scheduling-Case-Walkthrough). Establish a baseline, then select one change supported by that case and its interface. An orchestration recipe specifies the actions, settings and data used for execution and later review.

| Step | Action | Record to keep |
|---|---|---|
| 1. Confirm the question | State the planning period, objects and condition to compare | Scenario brief |
| 2. Inspect the inputs | Check units, processes, capacity and material relationships in a copy of the sample | Data version, relevant tables and checks |
| 3. Confirm configuration | Record enabled constraints, objectives, computing resources and allowed run time | Baseline configuration |
| 4. Run the baseline | Use the page or recipe entry point supported by the case | Status, action history, result tables and analysis |
| 5. Change one condition | Modify a supported objective parameter, or change a business condition in a separate data copy | The change, its reason and the revised version |
| 6. Compare and explain | Check status and constraints before business measures and detailed rows | Conclusions, decisions requiring confirmation and the next step |

In the Scenario Lab, use the configuration exposed by the page to run a baseline and adjust parameters. For calendar or process-data changes, work on a separate data copy and use the integration and execution entry point supported by that scenario. Keep parameter experiments separate from changes to business data.

For an objective-parameter comparison, keep the input data unchanged. For a data change such as maintenance, preserve the original copy and keep other parameters consistent where possible. Keep thread counts, time limits and other execution conditions consistent; repeat runs where appropriate to assess stability.

## 6. Read the Result in Order

1. **Status:** was a usable plan produced? If not, was infeasibility proved, did time run out, or was there an input, environment or authorization issue?
2. **Conditions:** which constraints were active? Were overload, lateness or unmet demand allowed?
3. **Business measures:** how much was produced or left short, when was work completed, and how much resource time was used?
4. **Objectives and details:** how did weights influence the trade-off, and which orders or work centers changed?
5. **Decision:** can the plan be executed, and who must confirm any measures it requires?

Objective totals calculated with different weights use different evaluation scales. Compare actual business measures first. If comparing total scores is useful, evaluate both results with the same objective definitions, directions and weights.

## 7. Exercises and Suggested Answers

| Exercise | Suggested answer |
|---|---|
| Will increasing the delivery-objective weight tenfold remove the 10-minute shortfall? | A weight expresses preference; it does not add time. With full quantity and delivery enforced as hard conditions, the shortfall remains. If deviations are allowed, explain where the unmet requirement moves |
| Will producing B before A solve the problem? | Both changeover directions take 40 minutes here, so total occupancy stays the same. Recalculate if directional changeover times differ in another case |
| After 10 extra minutes are approved, what still needs confirmation? | Here, confirm that the extra time extends the existing 450-minute window continuously and that staffing and materials remain available. The resulting 460 minutes accommodate the stated sequence. Other cases also need checks on their operations and resources |
| If a program finds no plan in 60 seconds, can the result be described as a business infeasibility? | Inspect its status and proof information. Search time exhaustion and proven infeasibility must be described separately |
| If all quantities are produced after the change, can that be described as improved delivery? | Completion times must also be compared with due dates. Measure quantity fulfillment and on-time delivery separately |

## 8. Carry the Learning into Implementation

This exercise leaves three reusable assets: a way to describe production conditions in data, a fair comparison method, and a process for deciding what to do with the result.

As the scope expands to more orders or resources, the same data checks and comparison method can be used again. During regular operation, changes to maintenance, objectives or rules can build on the recorded work. DecisioWorks supplies data, configuration, execution and analysis capabilities; manufacturers and partners connect them to their own processes and confirm the operational decisions.

## Further Reading

[Value Validation and Adoption](https://github.com/qiaoyx-or/decisioworks/wiki/Value-Validation-and-Adoption-Framework) · [Typical Value Entry Scenarios](https://github.com/qiaoyx-or/decisioworks/wiki/Typical-Value-Entry-Scenarios)

Worksheets: [Worksheet: Scenario and Decision Task](Worksheet-Scenario-Brief.md) · [Worksheet: Baseline and Adjusted Plan Comparison](Worksheet-Plan-Comparison.md)

[Topic A](Learning-Topic-A-Problem-and-Validation.md) · [Previous: Define a Decision Task from a Delivery Problem](Learning-A1-Define-a-Decision-Task.md) · [Next: Compare Two Plans on the Same Basis](Learning-A3-Compare-Plans-on-the-Same-Basis.md)
