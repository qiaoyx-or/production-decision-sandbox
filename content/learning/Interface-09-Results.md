# 09 Interpret Results and Prepare the Next Planning Cycle

[中文](Interface-09-Results-zh-CN.md) · [Learning guide](Interface-Guide.md) · [Semantic guide](Interface-Semantics.md)

## Task: Recover Business Meaning from Operation Results

This is a manually constructed candidate for calculation, not solver output. The base database keeps `planning_result` empty; candidate rows are stored separately in CSV.

| workcenter | time_unit | process | number |
|---:|---:|---:|---:|
| 11 | 1 | 1001 | 80 |
| 12 | 1 | 1002 | 80 |
| 11 | 2 | 1001 | 40 |
| 12 | 2 | 1002 | 40 |

Resolve each operation to its route and product. Assembly is the final operation, so deliveries correspond to 80 and 40. The four rows total 240 operation-output units, not 240 finished deliveries.

## Recover Time and Material Usage

| Period and resource | Output | Units/cycle | Cycles | Seconds/cycle | Processing minutes |
|---|---:|---:|---:|---:|---:|
| Day-one stamping | 80 | 4 | 20 | 600 | 200 |
| Day-one assembly | 80 | 1 | 80 | 120 | 160 |
| Day-two stamping | 40 | 4 | 10 | 600 | 100 |
| Day-two assembly | 40 | 1 | 40 | 120 | 80 |

Consumption is 80 blanks and 160 fasteners on day one, then another 40 and 80. Check cumulative consumption against cumulative supply. With opening finished stock 20 and issues 80 then 40, ending finished inventory is 20 on both days.

These calculations assume no initial setup, changeovers, scrap, or additional OEE adjustment. Add applicable time from the adopted records and rules when checking real results. Read `value_1/2/3` using the scenario's definition; cycle number and sequence position are scenario-specific interpretations.

## A Maintenance Change

Extending day-one stamping maintenance from two to three hours reduces available time from 360 to 300 minutes. The 200-minute stamping load still fits in aggregate. If maintenance occurs at the start of the shift and all 80 units needed on day one must finish stamping before any assembly starts, with no overlap between operations, continuous execution needs `180+200+160=540 minutes`, exceeding eight hours. The two-hour-maintenance version needs 480 minutes.

Transferring all 80 units together is an additional assumption, not a consequence of `batch_size=20`. Confirm the processing batch and transfer batch separately. If each completed batch of 20 can move to assembly, with no transport or setup losses and both machines able to operate concurrently, the four batches finish at minutes 270, 320, 370, and 420. The 420-minute and 540-minute calculations use different transfer rules; neither is a solver run.

A resource-load check therefore does not establish that the entire operation chain fits within the shift. Transfer batches, overlapping production, or changed windows need explicit scenario rules and model support. Result review needs both aggregate quantities and operation-level detail.

## Prepare the Next Input

1. Separate executed, committed, and adjustable work; retain the original plan.
2. Update remaining demand using actual deliveries, rather than planned completion.
3. Update available materials using actual consumption, receipts, and blocked quantities.
4. Carry forward necessary resource commitments without counting maintenance twice.
5. When the planning origin moves, rebuild every time reference, not just result numbering.
6. Record configuration differences before starting the next capability run.

## Exercise and Answer

Day one promised 80 but delivered only 60. If the cumulative commitment is unchanged, day-two remaining delivery is 60: the original 40 plus backlog 20. This does not automatically mean 60 new units must be produced. Review finished stock, work in process, completed but undelivered quantities, and inventory policy. Treating delivery backlog as new production can duplicate output.

[Previous](Interface-08-Validation.md) · [Walkthrough](Interface-Walkthrough.md) · [Relationship reference](Interface-Relationships.md)
