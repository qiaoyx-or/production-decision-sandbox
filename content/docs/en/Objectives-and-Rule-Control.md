**English** | [中文](Objectives-and-Rule-Control-zh-CN)

> Applies to DecisioWorks v1.4.0

# Objectives and rule control: bringing enterprise trade-offs into solving

A central APS challenge is expressing the enterprise trade-offs that guide computation. Delivery, inventory, workload, changeovers, stability, and risk cannot all improve without limit. If the system does not know what matters now or which shop-floor conditions must hold, the result may be mathematically valid but operationally rejected.

## Express three kinds of input separately

| Type | Question | Owner | Examples |
|---|---|---|---|
| Structural constraint | Is it physically or logically possible? | Standard data interface | Route, capacity, shift, BOM, batch |
| Management objective | What should the alternative favor? | `objective_system` | Delivery, workload, waiting, inventory, changeover |
| Scenario rule | How should this situation be controlled? | `marginal_control` | Bottleneck protection, priority window, prohibition, resource quota |

Mixing these inputs into algorithm code obscures their source, makes changes harder to maintain, and weakens result interpretation. Separating them lets each adjustment identify who requested it, which objects it affects, when it applies, and how it influences the result.

## How the objective system works

Objective terms include a semantic name, optimization direction, weight, object scope, granularity, and audit material. A weight represents a relative trade-off; physical cost and quantity remain separate business measures. Before changing a weight, confirm its direction and units, then compare the baseline and rerun at the affected-object level.

## How shop-floor rules enter the model

`marginal_control` carries customer- or site-confirmed rules, bottlenecks, agreed operational decisions, and balancing signals. Examples include protecting a bottleneck work center, limiting the scope of an adjustment, reserving resources for urgent work, or forbidding a particular adjacent changeover. A rule should identify its objects, scope, source, and expiry so that a one-time workaround does not become permanent hidden logic.

Each rule also needs an application mode: a hard constraint restricts feasibility, a soft preference influences trade-offs, and an advisory or feedback signal is handled by a later action. Supported modes depend on the selected capability and its model adapter. Reading a configuration does not prove that it became a solver constraint; check the rule mapping, execution audit, and resulting behavior.

## Resolve conflicting priorities

When delivery conflicts with changeover reduction, or an urgent order conflicts with a freeze window, the system should expose the conflict. Compare objectives, matched rules, and object-level impact, then let the accountable person confirm the trade-off. Optimization makes the conflict and its cost visible so that this choice can be reviewed.

## Configuration and acceptance steps

1. Confirm that the data expresses the required structural constraints.
2. Select a small set of objectives directly relevant to the current problem.
3. Identify each shop-floor rule's objects, scope, source, and validity period.
4. Run a baseline and retain the result evidence.
5. Change only a few objectives or rules before each rerun.
6. Compare business quantities, affected objects, and plan stability rather than the total score alone.

## Common mistakes

- Assuming a larger weight means greater business importance without checking units and scale.
- Turning every piece of shop-floor experience into a permanent hard constraint.
- Using objective weights to compensate for incorrect or missing data.
- Showing an improved objective value without showing what was sacrificed.
- Executing AI-generated rules before the responsible person has reviewed them.

Continue with [Controlled Solving and Engine Adapters](Controlled-Solving-and-Engine-Adapters) and [Trusted Operation and Human Review](Trusted-Operation-and-Human-Review).
