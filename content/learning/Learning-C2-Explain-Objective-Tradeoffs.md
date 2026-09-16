# C2 Explain the Trade-Offs between Objectives

[中文](Learning-C2-Explain-Objective-Tradeoffs-zh-CN.md) · [Learning Center](Learning-Center.md)

## Describe the Cost Before Selecting the Objective
Planners seek reliable delivery, workshops seek fewer changeovers, and inventory teams seek less stock. Objective names are a start. Define what each measure counts, which objects it covers and how alternatives will be compared.

In a teaching scenario, one plan produces early with more inventory but fewer changeovers. Another produces closer to due dates with less inventory and more changes. Weights express the organization's choice; they do not make that choice unnecessary.

## Build an Objective Definition
| Item | Specify |
|---|---|
| Business intent | For example, fewer color changes between adjacent tasks |
| Scope | Work center, tasks and planning period |
| Business measure | Change count, setup duration or another defined quantity |
| Objective measure | A raw model value used in scoring, such as accumulated waiting or changeover cost; called an objective material in the technical reference |
| Direction and weight | Minimization or maximization and relative coefficient |
| Review | Business measures, details and objective-measure check |

DecisioWorks organizes these definitions through its objective system, while engine adaptation connects supported model measures. Before configuring an objective, identify the measure supported by the selected engine and how it represents the business intent.

## Design an Injection-Molding Experiment
The sample maps the business name `color` to `property_1` and `container_capacity` to `property_3`. Its objective named capacity relates to the container-capacity attribute and circular changeovers; it does not mean machine availability.

Copy the baseline and change only the color weight. Keep data, constraints, other weights, work center, sequence length and cycle count unchanged. Record thread and time requests within the current authorization limits. After execution, inspect sequence changes, circular changes and their objective measures separately.

## Interpret the Observation
| Observation | Check next |
|---|---|
| Score changes but business quantities do not | Whether only weighted contributions changed |
| Aggregates stay the same | Whether object-level sequences or timing changed |
| One measure improves and another worsens | Whether that trade-off matches the intent |
| Results vary substantially | Computing limits, stopping status and repeated runs |
| No usable plan | Data, constraints and status before discussing weights |

With bounded search and interacting objectives, inspect both model scoring and displayed counts. They may include different events, such as transitions between empty and occupied positions. Trade-offs among objectives and search limits also affect the result, so review the actual sequence after changing a weight.

## Exercise and Review
Expand “fewer changeovers” into a scope, a changeover measure and a review method. State which measures improved, stayed the same or worsened, and identify the associated trade-offs. If no improvement was observed, report that directly. When using the published injection A/B record, state that two weights changed together. It evaluates that combination, not the isolated effect of color.

Keep the objective definition and a comparison conclusion that identifies conditions, measures and affected objects.

## Further Reading

[Objectives and Rule Control](https://github.com/qiaoyx-or/decisioworks/wiki/Objectives-and-Rule-Control) · [Controlled Solving and Engine Adapters](https://github.com/qiaoyx-or/decisioworks/wiki/Controlled-Solving-and-Engine-Adapters) · [Trusted Operation and Human Review](https://github.com/qiaoyx-or/decisioworks/wiki/Trusted-Operation-and-Human-Review)

Worksheets: [Worksheet: Baseline and Adjusted Plan Comparison](Worksheet-Plan-Comparison.md) · [Worksheet: Operational Rule and Verification](Worksheet-Operational-Rule.md)

[Topic C](Learning-Topic-C-Objectives-and-Operational-Rules.md) · [Previous: Distinguish Facts, Constraints and Preferences](Learning-C1-Facts-Constraints-and-Preferences.md) · [Next: Turn Shop-Floor Experience into Checkable Rules](Learning-C3-Turn-Experience-into-Rules.md)
