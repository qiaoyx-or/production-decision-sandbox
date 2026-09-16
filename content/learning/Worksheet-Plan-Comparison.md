# Worksheet: Baseline and Adjusted Plan Comparison

[中文](Worksheet-Plan-Comparison-zh-CN.md) · [Learning Center](Learning-Center.md)

## Record Conditions First
| Condition | Baseline | Adjusted |
|---|---|---|
| Data version and scope | Enter | Enter |
| Recipe and software version | Enter | Enter |
| Constraints and objectives | Enter | Enter |
| Threads, time limit and other conditions | Enter | Enter |
| Stopping status and candidates | Enter | Enter |
| Single or combined change | Baseline definition | Change and reason |

## Record Results
| Measure | Definition, unit and granularity | Baseline | Adjusted | Interpretation |
|---|---|---|---|---|
| Quantity fulfillment | Explicit numerator/denominator | Enter | Enter | Affected objects |
| Delivery or deviation | Source unit and conversion | Enter | Enter | Commitment impact |
| Resource load | Work center and time unit | Enter | Enter | Bottleneck |
| Changes or waiting | Counting scope | Enter | Enter | Trade-off |
| Objective measures | Raw model value, direction and weight | Enter | Enter | Separate from business quantities |

## Conclude
Separate observations, explanations, open questions and next steps. Do not calculate improvement from totals using different weights. Inspect details when aggregates match. Record the status of an unsuccessful run. Show any historical reference plan separately with its version and date.

## Worked Entry: Reading the Injection Case
This entry uses [D2's published run record](Learning-D2-Read-Injection-Molding-Changeovers.md) to demonstrate how to complete the worksheet.

- Conditions: both color and capacity weights changed, so this was a combined adjustment.
- Observation: sequence changes rose from 41 to 46 and circular changes from 6 to 14.
- Interpretation: these two counts show no reduction in changes. Scores of 14.9 and 66.4 use different weights and cannot directly establish an improvement percentage.
- Open question: which cycles and positions changed, and how were the raw objective values scored?
- Next step: design an independent color-only comparison, then add actual status and results after execution.

Replace this example with the records for your own run. Mark missing details as awaiting data rather than entering estimates as measurements.
