# A3 Compare Two Plans on the Same Basis

[中文](Learning-A3-Compare-Plans-on-the-Same-Basis-zh-CN.md) · [Learning Center](Learning-Center.md)

## A Score Changed. What Else Changed?
An objective total combines preferences. Changing weights changes the evaluation scale, so the score alone cannot establish business improvement. The following teaching plans use scores calculated by hand from the stated formulas.

| Plan | Late orders | Changeovers | Evaluation 1: late ×10 + changes | Evaluation 2: late ×20 + changes |
|---|---:|---:|---:|---:|
| P | 2 | 4 | 24 | 44 |
| Q | 1 | 9 | 19 | 29 |

Lower is better in both evaluations. Compare P and Q within one evaluation. Comparing P's 24 with Q's 29 mixes scales. The operational trade-off is one fewer late order at the cost of five additional changeovers.

## Establish Comparable Conditions
Record data versions, order scope, time scale, enabled constraints and computing limits so differences between runs can be identified. When studying one objective parameter, hold other conditions constant where possible. If business data changes, retain both versions and explain why.

| Layer | Record | Question |
|---|---|---|
| Inputs | Data version and object scope | Are these the same tasks? |
| Configuration | Objectives, rules and resource settings | What else changed? |
| Status | Candidates, stopping reason and feasibility checks | Are both results usable? |
| Business measures | Quantities, time, load and changeovers | Which objects improve or bear a cost? |
| Objective measures | Raw values, direction, weights and contributions | Were preferences applied as configured? |

Objective measures (called objective materials in the technical reference) are raw measures used to evaluate a plan, such as accumulated waiting or a defined changeover measure. Weighted contributions reflect how those measures enter the score with the configured direction, scale and weight. Inspect the raw value before its weighted contribution.

## Inspect Details as Well as Totals
DecisioWorks analysis supports both aggregate and detailed review. Unchanged total workload can hide overload in one period. Unchanged output quantity can hide different completion dates. Match results by business keys such as work center, time unit, operation or order, rather than display row number.

Confirm time units before converting values. Weighted job_bias is not directly a delay measured in minutes. A name containing “time” still requires its native unit and conversion rule. To rescore two plans on a common basis, use each plan's own raw values with the same metric definitions, units, directions, normalization and weights. The plans' measured values need not be equal.

## Account for Search Variability
A bounded search may produce different feasible plans. Record whether a usable solution exists and why the run stopped. To assess stability, repeat runs with the same software version, environment and computing limits, and report the range of results. Record random seeds where the interface supports them. A better result in one comparison is evidence about that comparison, not every future run.

## Exercise and Suggested Answer
Add an evaluation of late orders ×3 plus changeovers. P scores 10 and Q scores 12, so this preference favors P. Choosing in practice still requires understanding the consequences of lateness.

Produce a comparison record listing fixed conditions, the change, business measures, affected objects and interpretation. If the conclusion only says “the score fell, therefore the plan improved,” add the scoring basis and the operational trade-off.

## Further Reading

[Value Validation and Adoption](https://github.com/qiaoyx-or/decisioworks/wiki/Value-Validation-and-Adoption-Framework) · [Typical Value Entry Scenarios](https://github.com/qiaoyx-or/decisioworks/wiki/Typical-Value-Entry-Scenarios)

Worksheets: [Worksheet: Scenario and Decision Task](Worksheet-Scenario-Brief.md) · [Worksheet: Baseline and Adjusted Plan Comparison](Worksheet-Plan-Comparison.md)

[Topic A](Learning-Topic-A-Problem-and-Validation.md) · [Previous: Validate First: Design a Useful Planning Comparison](Learning-A2-Design-a-Useful-Planning-Comparison.md) · [Next: From Business Tables to Computable Objects](Learning-B1-Business-Tables-to-Computable-Objects.md)
