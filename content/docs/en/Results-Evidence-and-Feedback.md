**English** | [中文](Results-Evidence-and-Feedback-zh-CN)

> Applies to DecisioWorks v1.4.0

# Results, evidence, and feedback: from an answer to a decision

A schedule shows that the model produced an arrangement. It does not by itself prove that the arrangement should be executed. Users still need to know which demand is met, which orders are affected, where workload moved, what was sacrificed to reduce changeovers, and what must enter the next cycle.

## Three levels of results

| Level | Question | Examples |
|---|---|---|
| Overall | How does the whole alternative perform? | Satisfaction, shortage, output, workload, objective summary |
| Object | Where does the issue occur? | Work center, product, order, operation, time unit, changeover |
| Audit | Did the configured run produce this result? | Data version, objective direction, material mapping, parameters, status |

Overall metrics help identify priorities, object-level details support business review, and audit records explain how the result was produced. Each level serves a different purpose.

## Keep physical quantities separate from objective scores

Weighted objective scores describe trade-offs; physical time, quantities, and workload come from the corresponding business metrics. When reading Web Cockpit results, check units and granularity before interpreting these values.

Convert time to minutes only when the source unit and conversion basis are known. Expand workload by work center and shortage at the granularity supported by the data and results. If a plan retains only product, operation, work center, and time unit, order-level delivery conclusions require an explicit allocation or linking rule. Total product output alone cannot establish that every order is satisfied.

## Turn results into evidence

Keep dataset and recipe versions, runtime parameters, start and end timestamps, action status, candidate count, selected solution, key business metrics, and a diagnostic ID for later review. Run summaries, configuration fingerprints, and relevant diagnostics can support discussions with partners. Handle order, customer, and equipment details according to your organization's data-sharing requirements.

## From results to feedback

Underproduction, overload, kitting risk, waiting, changeovers, and execution deviation may become PlanBias and then PlanSignal. A signal can influence objectives, local rules, release, or data preparation for the next cycle. Feedback supplies sourced decision material; it does not silently overwrite the plan.

## Compare a baseline with a rerun

Change only a small number of factors and report the benefit, cost, affected objects, tasks that remained stable, and new risks. Showing a better result without input differences and object-level evidence does not provide a complete validation record.

## Common misreadings

- Treating an objective score as actual production output.
- Looking only at average load and overlooking a bottleneck work center.
- Interpreting proven infeasibility as a software crash.
- Keeping result files without the corresponding data and configuration versions.
- Changing many parameters in every run and losing the ability to explain the differences.

Continue with the [End-to-End Scenario Walkthrough](End-to-End-Scenario-Walkthrough) and [Planning and Scheduling](Planning-and-Scheduling-Overview).
