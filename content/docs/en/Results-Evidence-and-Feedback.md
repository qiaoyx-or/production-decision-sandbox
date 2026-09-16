**English** | [中文](Results-Evidence-and-Feedback-zh-CN)

> Applies to DecisioWorks v1.4.0

# Results, evidence, and feedback: from an answer to a decision

A schedule shows that the model produced an arrangement. It does not by itself prove that the arrangement should be executed. Users still need to know which demand is met, which orders are affected, where workload moved, what was sacrificed to reduce changeovers, and what must enter the next cycle.

| Level | Question | Examples |
|---|---|---|
| Overall | How does the whole alternative perform? | Satisfaction, shortage, output, workload, objective summary |
| Object | Where does the issue occur? | Work center, product, order, operation, time unit, changeover |
| Audit | Did the configured run produce this result? | Data/recipe version, objective direction, parameters, status |

Weighted objective scores describe trade-offs; physical time, quantities, and workload come from the corresponding business metrics. When reading Web Cockpit results, check units and granularity, then inspect workload by work center and shortages by order or product. Converting time to minutes requires an explicit time unit in the data, not a weighted score.

Keep dataset and recipe versions, runtime parameters, timestamps, action status, candidate count, selected solution, key business metrics, and a diagnostic ID for later review. Run summaries, configuration fingerprints, and relevant diagnostics can support discussions with partners. Handle order, customer, and equipment details according to your organization's data-sharing requirements.

Underproduction, overload, kitting risk, waiting, changeovers, and execution deviation may become PlanBias and then PlanSignal. A signal can influence objectives, local rules, release, or data preparation for the next cycle. Feedback supplies sourced decision material; it does not silently overwrite the plan.

For baseline-versus-rerun comparison, change only a small number of factors and report the benefit, cost, affected objects, stable scope, and new risks. A claim that an optimized result is better without input differences and object-level evidence is incomplete.
