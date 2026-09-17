# 05 Calculate Cycle Output, Batches, and Processing Time

[中文](Interface-05-Quantity-zh-CN.md) · [Learning guide](Interface-Guide.md) · [Semantic guide](Interface-Semantics.md)

## Define a Processing Cycle First

The bracket example produces four units per stamping cycle, takes 600 seconds per cycle, and uses 20-unit batches. Day-one demand is 80. Assume no initial setup, changeover, or scrap; OEE is 100, with no additional efficiency adjustment.

| Item | Value | Manual calculation |
|---|---:|---|
| `productivity` | 4 units/cycle | One cycle produces four units |
| `batch_size` | 20 units/batch | 20÷4=5 cycles/batch |
| Demand | 80 units | 80÷20=4 batches |
| Processing cycles | 20 | 80÷4 |
| Processing time | 12000 seconds | 20×600=200 minutes |

The result quantity is 80 units, not 20 cycles. Assembly produces one unit per 120-second cycle, requiring 160 minutes for the same 80 units. Use the explicit unit “units/cycle” here. Continuous-output data requires a defined discrete processing unit and time conversion before using this template.

## Two Different Divisibility Checks

`batch_size/productivity` must correspond to whole processing cycles. Four units per cycle and an 18-unit batch would require 4.5 cycles, contradicting whole-cycle processing.

Demand-to-batch divisibility is a business policy. For demand 42 and batches of 20, output 40 leaves a shortage of two and output 60 creates a surplus of 18. If surplus, shortage, or split batches are permitted, state the policy and retain original demand 42. Silently replacing it with 60 would conceal the surplus.

## Joint Output from One Processing Event

Another mold produces A×2, B×2, and C×1 per cycle. A common adaptor `binding` expresses the relationship. Ten cycles produce 20, 20, and 10 units. Against demand 18, 20, and 12, the differences are surplus two, exact fulfillment, and shortage two. Twelve cycles produce 24, 24, and 12, giving surpluses six and four, with C exact.

These are manual candidates. Inventory, dates, cost, and configuration determine the choice. Do not add the same joint-processing time once for every output; confirm that the model accounts for the shared event.

## OEE and Whole Cycles

Assume four units per 20-minute cycle and a 480-minute shift. Applying an 85% efficiency factor once gives 408 minutes. A continuous estimate is 81.6 units; whole-cycle processing permits 20 cycles, or 80 units. With 20-unit batches, this remains four batches. The discrete plan cannot use 81.6 as its output.

The current template defaults OEE to 100, a percentage representation. Lower efficiency can reduce effective capacity or, under an explicit conversion, increase the occupied time needed for the same output. Confirm where the selected model accounts for the loss and count it only once. Entering 85 alone does not establish that it was applied. Retain source data and conversion rules.

## A Different Unit for Continuous Output

For continuous processing, `productivity` can mean output per unit time. At 120 liters/hour, two effective operating hours produce 240 liters under a no-loss teaching assumption. This uses liters/hour rather than the earlier pieces/cycle.

First select a model interpretation that uses that unit. A projection into the current discrete template could explicitly represent a one-hour processing unit as 120 liters and 3,600 seconds. Finer windows require corresponding units and conversion; 120 cannot simply be treated as output from an arbitrary cycle. This is a dimensional example, not a recorded continuous-production solve.

## Exercise and Answer

Change the base cycle duration from 600 to 900 seconds, retaining output and batch size. Eighty units still require 20 cycles, now 18,000 seconds or 300 minutes. Day-one stamping has 360 available minutes, leaving 60. This checks resource-time totals; assembly, materials, and windows still determine full feasibility.

[Previous](Interface-04-Routing.md) · [Next: materials](Interface-06-Materials.md)
