# 07 Translate Inventory Requirements into Cumulative Bounds

[中文](Interface-07-Inventory-zh-CN.md) · [Learning guide](Interface-Guide.md) · [Semantic guide](Interface-Semantics.md)

## Task: Derive Fields from an Inventory Balance

Opening bracket stock is 20. Each day's ending stock must remain between 20 and 100. Issues are 80 on day one and another 40 on day two, with no other receipts. Translate these requirements into cumulative production bounds in `inventory_limit`.

This exercise checks period-end inventory. If storage capacity must hold at every instant within a shift, use finer time representation and receipt/issue ordering. End-of-day bounds do not establish within-day feasibility.

## Calculate the Bounds

Let P(t) be cumulative production receipts and D(t) cumulative issues. Inventory is `20+P(t)−D(t)`. Applying `20 ≤ 20+P(t)−D(t) ≤ 100` gives `D(t) ≤ P(t) ≤ D(t)+80`.

| Period | Period issues | Cumulative issues D(t) | Cumulative production minimum | Cumulative production maximum |
|---:|---:|---:|---:|---:|
| 1 | 80 | 80 | 80 | 160 |
| 2 | 40 | 120 | 120 | 200 |

Write:

| id | product | time_unit | binding | lower_bound_acc | upper_bound_acc | urgency |
|---:|---:|---:|---|---:|---:|---:|
| 1 | 1 | 1 | NULL | 80 | 160 | 0 |
| 2 | 1 | 2 | NULL | 120 | 200 | 0 |

The lower bounds 80 and 120 are already cumulative; do not add them to 200. Keep opening stock and the issue plan in source records or mapping evidence. The standard table carries the derived limits.

## Check in Reverse

Candidate production of 80 then 40 gives cumulative outputs 80 and 120. Ending inventory is 20 on both days. Producing only 60 on day one leaves zero stock, below the required 20; meeting the two-day total later cannot repair the first-day violation.

If other cumulative receipts E(t) exist, subtract them from both bounds. `NULL` means unspecified. A lower bound of zero explicitly permits zero cumulative production and has a different meaning.

## Shared Inventory and Urgency

A common `binding` expresses shared inventory. Allocation requires comparable units: one large box and one small box may occupy different space. Use volume, pallet positions, or documented equivalents. `urgency` carries urgency or turnover-related information; its effect on selection belongs to the adopted policy.

## Exercise and Answer

Change opening stock to 30, retaining everything else. Day-one bounds become 70 and 150; day-two bounds become 110 and 190. A negative upper bound indicates that even zero production exceeds storage capacity and must not be silently clamped to zero. A negative lower bound may become zero when production is nonnegative.

The current data layer expresses and validates these bounds. For an actual solve, check the chosen model's inventory rules and compare runs that change one inventory condition. A populated field alone does not establish that a constraint was enforced.

[Previous](Interface-06-Materials.md) · [Next: import and validation](Interface-08-Validation.md)
