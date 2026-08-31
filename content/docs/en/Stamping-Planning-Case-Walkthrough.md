**English** | [简体中文](Stamping-Planning-Case-Walkthrough-zh-CN)

> Applies to DecisioWorks v1.4.0

# Stamping planning case: from 1,920 order lines to a controlled planning chain

This case uses the reference `StampingWorkshop/data.db` and the official `production_planning` recipe. A read-only inspection on 2026-08-31 returned SQLite integrity `ok` and found 1,920 order lines, 50 capacity records, 38 operation-level material links, 500 kitting records, 25 time units, and 3 work centers.

Orders provide product, due time, and quantity. Routes and operations connect products to work centers. `ingredient` binds material demand to operations, `kitting_information` provides material availability by time, and `capacity.used` represents an existing utilization ratio.

The recipe enables capacity, demand, and kitting constraints, uses soft capacity, and leaves inventory constraints disabled. Its objective uses `job_bias=-0.001` and `waittime=1.0`. The configured solver request is 16 threads and 120 seconds, subject to edition and license limits.

The action chain is acquisition → constraint parsing → generation → selection → evaluation → optional dispatch.

| Output | How to read it | Acceptance question |
|---|---|---|
| Planning result | Quantity by time, work center, and operation | Does it cover demand on the shared time coordinate? |
| Delivery bias | Drill down to product or order | Is risk caused by quantity, timing, or release? |
| Workload | Compare aggregate and time-unit detail | Does an average hide a bottleneck? |
| Idle and waiting | Use an explicit time unit | Is it caused by kitting, capacity, or trade-off? |
| Objective-material audit | Verify direction, weight, and meaning | Has a weighted value been confused with a physical quantity? |

Baseline and rerun comparisons should keep the data version fixed, change only a few objectives, rules, or resource conditions, and retain the configuration difference.

On 2026-08-31, a fresh run was completed in an isolated commercial-edition copy under a valid `Enterprise` license. The API baseline used 16 threads with a 120-second limit and returned `ok` in 14.41 seconds. The adjusted run kept the same data, constraints, and compute settings, changing only `job_bias` from `-0.001` to `-0.003` and `waittime` from `1.0` to `2.0`; it returned `ok` in 14.29 seconds. Both runs produced one candidate, a valid best solution, 66 result records, 12 action events, and no errors.

For the baseline, total demand and output were both 680,500, final shortage was zero, and fulfilment was 100%. Available capacity was 1,188,000; processing load was 371,588.48; planned load including setup and waiting was 377,080.42; utilization was about 31.74%. The weight change did not alter these planning quantities, while the weighted `job_bias` contribution changed from `-7,854.678` to `-23,564.034`. This is useful evidence in its own right: a weight can enter the objective correctly without forcing a different plan when the current data and constraints still support the same solution.

![Real stamping input data](assets/enterprise-real-run-20260831/stamping_input_data.jpg)

![Real stamping baseline result](assets/enterprise-real-run-20260831/stamping_baseline_result.jpg)

![Stamping baseline versus adjusted run](assets/enterprise-real-run-20260831/stamping_ab_compare.jpg)

The screenshots were produced by loading and running the Commercial Edition Scenario Lab. The UI reproduction completed with its teaching configuration of two threads and 60 seconds; the API evidence used the 16-thread, 120-second configuration stated above. The public run record retains the version, license tier, parameters, metrics, and file hashes. These results verify the release and reference scenario chain; customer environments still require data, performance, and business acceptance.

