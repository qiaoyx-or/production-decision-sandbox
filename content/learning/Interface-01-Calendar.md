# 01 Configure Time, Shifts, and Maintenance

[中文](Interface-01-Calendar-zh-CN.md) · [Learning guide](Interface-Guide.md) · [Semantic guide](Interface-Semantics.md)

## Task and Preparation

Build a two-day planning coordinate with one eight-hour production window per day. The stamping machine has two hours of maintenance on day one; assembly runs normally. You should be able to calculate each resource's daily availability directly from the records.

Confirm the planning origin, dates, shifts, and time zone. The two units represent production windows on consecutive days, not necessarily calendar instants eight hours apart. Keep the date mapping with the source-data mapping.

## Create Time Records

| id | offset | scale (seconds) | status | Business mapping |
|---:|---:|---:|---:|---|
| 1 | 0 | 28800 | 1 | Day-one production window |
| 2 | 1 | 28800 | 1 | Day-two production window |

`id` is referenced by demand, capacity, kitting, and results. `offset` orders periods; `scale` supplies duration. A day-one due date becomes `delivery_time=1`, rather than a calendar string or `offset=0`.

## Record Local Maintenance

Work center 11 is stamping and 12 is assembly. Each combination below becomes one `capacity` row:

| id | time_unit | workcenter | used | Available minutes |
|---:|---:|---:|---:|---:|
| 1 | 1 | 11 | 0.25 | 360 |
| 2 | 1 | 12 | 0 | 480 |
| 3 | 2 | 11 | 0 | 480 |
| 4 | 2 | 12 | 0 | 480 |

Day-one stamping availability is `28800 × (1−0.25) / 60 = 360 minutes`. Maintenance has not been deducted elsewhere. Resources share the global calendar but can have different local occupancy.

## One Shift, Two Shifts, and Overtime

To represent exact operating hours within a 24-hour day, use hourly units with `scale=3600`. Globally closed hours use `status=0`. A two-shift factory can make both shifts globally available, while a single-shift machine uses `used=1` during the second shift. Continuous production needs a global calendar covering the whole day and local maintenance records.

`status=-1` expresses optional time. Confirm how the selected model adopts it. If a resolved calendar is required, create an approved-overtime or no-overtime input view and record the decision. Do not substitute `-1` into the normal-period availability formula.

## Check Your Work

1. Two hours out of eight is 0.25, not 2, 120, or 25.
2. Deduct maintenance once. Merge overlapping unavailable intervals before converting to a fraction.
3. A 360-minute aggregate does not establish that those minutes are continuous. Represent finer periods when an uninterrupted operation must avoid an internal maintenance window.
4. Compare before and after records; only the relevant resource and period should change.

## Exercise and Answer

Extend day-one maintenance to three hours. Change `capacity.id=1` to `used=3/8=0.375`. Availability becomes 300 minutes, a reduction of 60. A 200-minute task still fits in aggregate, but material availability, precedence, and maintenance timing also need review.

[Next: orders and attributes](Interface-02-Demand.md) · [Configuration patterns](Interface-Configurations.md)
