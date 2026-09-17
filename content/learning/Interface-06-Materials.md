# 06 Configure Operation-Level Materials and Availability

[中文](Interface-06-Materials-zh-CN.md) · [Learning guide](Interface-Guide.md) · [Semantic guide](Interface-Semantics.md)

## Task: Place Consumption at the Correct Operation

Each bracket consumes one blank during stamping and two fasteners during assembly. Coefficients are per unit of operation output, with no scrap. Create materials 1 (BLANK) and 2 (FASTENER), then enter `ingredient`:

| id | process | material | number | priority |
|---:|---:|---:|---:|---:|
| 1 | 1001 | 1 | 1 | 0 |
| 2 | 1002 | 2 | 2 | 0 |

Eighty brackets require 80 blanks and 160 fasteners. Stamping produces four units per cycle, so 20 cycles still consume 80 blanks. Multiplying 20 cycles by one blank would understate demand by a factor of four.

## Time-Phase Supply

This lesson uses opening ready quantity followed by newly available quantities. Enter these increments:

| id | time_unit | material | number |
|---:|---:|---:|---:|
| 1 | 1 | 1 | 80 |
| 2 | 1 | 2 | 160 |
| 3 | 2 | 1 | 40 |
| 4 | 2 | 2 | 80 |

Cumulative supply is 80 blanks and 160 fasteners on day one, then 120 and 240 on day two. Compare cumulative consumption against supply on the same basis. Source cumulative supply snapshots of 80 and 120 become increments 80 and 40 before entering a cumulatively summed input chain; summing 80 and 120 again would incorrectly give 200.

Explain both availability at a point in time and how period rows are stored. If stock snapshots already deduct consumption, simple differencing does not yield supply receipts. Reconstruct availability from opening stock, confirmed receipts, consumption, and blocked quantities.

For blanks, assume zero opening inventory, supply and consumption before each checkpoint, and no blocked stock or losses:

| Checkpoint | New availability in the period (this example's input) | Cumulative supply | Cumulative consumption | Stock after consumption |
|---|---:|---:|---:|---:|
| End of day one | 80 | 80 | 80 | 0 |
| End of day two | 40 | 120 | 120 | 0 |

Here 80 and 40 are execution inputs, 80 and 120 are cumulative supply, and 0 and 0 are remaining stock. They are not interchangeable. An unchanged stock balance does not mean that no material arrived on day two.

## Locate the Affected Operation

If day-one fasteners fall to 120 and day-two receipts rise to 120, day-one assembly is limited to 60 units while two-day supply remains 240. Enough blanks do not establish assembly readiness. Stamping 80 and holding 20 intermediates depends on buffers, precedence, and planning policy.

For an arrival during a shift, use finer periods and specify whether material becomes usable at a window's start or end. A shift-level row alone cannot distinguish morning from afternoon availability.

## Substitutes and Dependent Choices

Two alternative fasteners can share a `material.substitute` group, with `ingredient.priority` expressing a supply preference. Coordinated wheel-and-tire choices use a material dependency. A selection policy must interpret substitutes, dependencies, and priorities; adding all alternative stock together while ignoring specifications would lose the relationship.

`vendor` records the supplier. `extend` is a reserved extension field, for example for supplier priority. Define its meaning, allowed values, and interpretation before use. A reference mapping is needed only when the extension is explicitly designed as a reference.

## Exercise and Answer

Add surface treatment consuming 0.2 liters per item. With integer quantity fields, use milliliters consistently: coefficient 200 and requirement 2000 for ten items. Supply must also be in milliliters. Record the unit in the mapping documentation. Converting only the BOM would introduce a factor-of-1000 error.

[Previous](Interface-05-Quantity.md) · [Next: inventory](Interface-07-Inventory.md)
