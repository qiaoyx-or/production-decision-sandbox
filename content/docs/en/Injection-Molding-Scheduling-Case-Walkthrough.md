**English** | [简体中文](Injection-Molding-Scheduling-Case-Walkthrough-zh-CN)

> Applies to DecisioWorks v1.4.0

# Injection-molding scheduling case: bringing color, cap type, and capacity into changeover decisions

This case uses `InjectionMoldingWorkshop/data.db` and the official `production_scheduling` recipe. A read-only inspection on 2026-08-31 returned SQLite integrity `ok` and found 37 demand lines, 2 work centers, 115 materials, 418 process adaptors, and 120 existing result rows.

The recipe maps standard property slots to color, cap type, and container capacity. This keeps the model connected to business meaning instead of guessing meaning from storage positions.

The circular-sequence configuration enables capacity, demand, inventory, sequence-changeover, and circular-changeover constraints. Adjacent tasks use color for sequence changeovers; reused-capacity cycles use container capacity for circular state changes. Preprocessing validates integer fields and batch multiples before solving.

The reference configuration uses work center 2, sequence length 40, three cycles, objective weights color 0.1 and capacity 1, and a request of 16 threads for 60 seconds. These are sample settings, not universal injection-molding recommendations.

Acceptance goes beyond the existence of a sequence.

| Output | How to read it | Acceptance question |
|---|---|---|
| Schedule sequence | Tasks by work center and cycle | Are scope and sequence length correct? |
| Demand coverage | Compare all 37 demand lines | Are any tasks missing or duplicated? |
| Sequence changeover | Count adjacent color changes | What was sacrificed to reduce changes? |
| Circular changeover | Inspect capacity state across cycle boundaries | Do reused cycles connect consistently? |
| Batch audit | Compare rate and demand multiples | Did preprocessing catch inconsistency? |
| Objective-material audit | Verify color and capacity direction | Did configured weights enter solving correctly? |

For a rerun, change only a small number of color/capacity weights, sequence length, or cycle-count settings.

On 2026-08-31, real A/B runs were completed in an isolated commercial-edition copy under a valid `Enterprise` license. Both API runs used 16 threads with a 60-second solve limit and returned `ok`, one candidate, a valid best solution, 120 result records, 12 action events, and no errors. The baseline completed in 66.57 seconds and the adjusted run in 66.50 seconds. These elapsed values include Web API processing and should not be read as solver-only time.

With `color=0.1` and `capacity=1.0`, the baseline analysis reported 41 sequence changes, 6 circular changes, and a weighted changeover cost of 14.9. With `color=0.8` and `capacity=1.5`, the adjusted run reported 46 sequence changes, 14 circular changes, and a weighted cost of 66.4. Direction audits passed in both runs, and the analysis values matched the GOCK objective-material values.

The result shows why a rerun must be reviewed through business measures. Native objective units include material-specific and empty-state transitions, while changed weights alter the relative cost of competing trade-offs. A weight expresses a decision preference; changes in any displayed metric still depend on the data, constraints, and competing objectives.

![Real injection-molding input data](assets/enterprise-real-run-20260831/injection_input_data.jpg)

![Real injection-molding baseline result](assets/enterprise-real-run-20260831/injection_baseline_result.jpg)

![Injection-molding baseline versus adjusted run](assets/enterprise-real-run-20260831/injection_ab_compare.jpg)

The UI reproduction also exposed a configuration mismatch: the teaching catalog requested two threads, while the dataset's public default was 16. The two-thread run failed; after the request was aligned with the 16-thread dataset default, both baseline and adjusted runs completed successfully. The mismatch, correction, and results are retained in the validation record. Public evidence contains only the runtime configuration, status, and result summary; customer data, performance, and business acceptance remain part of deployment validation.

The API evidence and UI screenshots come from separate real executions. Parallel search can return different feasible sequences, so the screenshot counts are not expected to match the API summary item by item. Each A/B comparison is evaluated only within its own execution environment and parameter baseline.

