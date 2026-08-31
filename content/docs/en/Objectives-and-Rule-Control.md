**English** | [中文](Objectives-and-Rule-Control-zh-CN)

> Applies to DecisioWorks v1.4.0

# Objectives and rule control: bringing enterprise trade-offs into solving

A central APS challenge is expressing the enterprise trade-offs that guide computation. Delivery, inventory, workload, changeovers, stability, and risk cannot all improve without limit. If the system does not know what matters now or which shop-floor conditions must hold, the result may be mathematically valid but operationally rejected.

| Type | Question | Owner | Examples |
|---|---|---|---|
| Structural constraint | Is it physically or logically possible? | Standard data interface | Route, capacity, shift, BOM, batch |
| Management objective | What should the alternative favor? | `objective_system` | Delivery, workload, waiting, inventory, changeover |
| Scenario rule | What must this situation respect? | `marginal_control` | Bottleneck protection, priority window, prohibition, resource quota |

Separating these types preserves source, scope, effective time, and result interpretation. Objective terms include semantic name, direction, weight, object scope, granularity, and audit material. A weight represents relative trade-off; physical cost and quantity remain separate business measures.

`marginal_control` carries customer- or site-confirmed rules, bottlenecks, consensus, and balancing signals. A rule should identify its objects, scope, source, and expiry so that a one-time workaround does not become permanent hidden logic.

When delivery conflicts with changeover reduction, or an urgent order conflicts with a freeze window, the system should expose the conflict. Compare objectives, matched rules, and object-level impact, then let the accountable person confirm the trade-off.

Configure by validating structural constraints first, selecting a small set of relevant objectives, scoping rules, running a baseline, changing only a few factors, and comparing business quantities and stability rather than a score alone.
