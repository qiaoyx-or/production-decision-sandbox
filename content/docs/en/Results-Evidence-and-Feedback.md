**English** | [中文](Results-Evidence-and-Feedback-zh-CN)

> Applies to DecisioWorks v1.4.0

# Results, evidence, and feedback: from an answer to a decision

A schedule shows that the model produced an arrangement. It does not by itself prove that the arrangement should be executed. Users still need to know which demand is met, which orders are affected, where workload moved, what was sacrificed to reduce changeovers, and what must enter the next cycle.

| Level | Question | Examples |
|---|---|---|
| Portfolio | How does the whole alternative perform? | Satisfaction, shortage, output, workload, objective summary |
| Object | Where does the issue occur? | Work center, product, order, operation, time unit, changeover |
| Audit | Did the configured run produce this result? | Data/recipe version, objective direction, parameters, status |

Weighted objective scores are not physical minutes, quantities, or utilization. The Web cockpit should show objective material alongside readable business quantities with units and object granularity.

Evidence should retain dataset and recipe versions, runtime parameters, timestamps, action status, candidate count, selected solution, key business metrics, and a diagnostic ID. Public evidence should use redacted run summaries, configuration fingerprints, and only the diagnostic information required for review.

Underproduction, overload, kitting risk, waiting, changeovers, and execution deviation may become PlanBias and then PlanSignal. A signal can influence objectives, local rules, release, or data preparation for the next cycle. Feedback supplies sourced decision material; it does not silently overwrite the plan.

For baseline-versus-rerun comparison, change only a small number of factors and report the benefit, cost, affected objects, stable scope, and new risks. A claim that an optimized result is better without input differences and object-level evidence is incomplete.
