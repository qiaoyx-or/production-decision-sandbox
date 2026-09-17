# Configuration Patterns: From Shop-Floor Arrangements to Data

[中文](Interface-Configurations-zh-CN.md) · [Learning guide](Interface-Guide.md)

Before choosing a pattern, establish the planning time granularity, distinguish global changes from resource-specific changes, and decide whether aggregate quantities or exact timing must be controlled. The patterns can be combined. Tables below show only relevant fields; complete records follow the [field reference](Interface-Fields.md).

## 1. Single-Shift, Double-Shift and Continuous Production

For illustration, divide a day into 24 hourly units, each with `scale=3600`. The table groups adjacent hours for readability; actual data has one record per hour.

| Arrangement | Example normal operating periods | Remaining periods |
|---|---|---|
| One eight-hour shift | 08:00–12:00 and 13:00–17:00 | Use `status=0` for a global shutdown |
| Two eight-hour shifts | 00:00–08:00 and 08:00–16:00 | Closed from 16:00–24:00 |
| Continuous production | 00:00–24:00 | Record equipment-specific downtime separately |
| Weekday production | Apply the selected shifts Monday through Friday | Weekends are closed or explicitly optional |

These hours are illustrative. Map actual breaks, handovers, overnight shifts and weekly calendars. If machine A works one shift and B works two, the shared time axis should cover both. Record A's local closure through its `capacity.used`, rather than shutting down the global calendar.

`status=-1` can express overtime awaiting a decision. Before a run that requires a fixed calendar, confirm the optional periods being used and retain the reason.

## 2. Representing Maintenance

For two hours of maintenance within an aggregated eight-hour period:

| Table | Relevant values |
|---|---|
| `time_unit` | `id=1, offset=0, scale=28800, status=1` |
| `capacity` | `workcenter=11, time_unit=1, used=0.25` |

Six hours remain. Three hours of maintenance changes `used` to 0.375 and leaves five hours. If an existing two-hour task overlaps two-hour maintenance by one hour, total unavailability is three hours, not four.

To prohibit processing specifically from 10:00–12:00, mark those resource-hour records fully unavailable, or use a scheduling configuration with explicit downtime windows. An aggregate 25% loss does not reveal whether downtime occurs at the start, middle or end of a shift.

## 3. Alternative Machines and Shared Tooling

An operation can have two `process_adaptor` records pointing to machines 11 and 13. Output per cycle, duration, batch size and priority may differ. Preserve the alternatives in the data and let the selected capability's resource-choice policy process them.

If the machines share one tool, represent the tool as work center 20:

| shared_resource.binding | shared_resource.to |
|---:|---:|
| 20 | 11 |
| 20 | 13 |

Record its availability separately as `capacity(workcenter=20, time_unit=1, used=0.5)`. Two machines each available for eight hours do not create sixteen simultaneous hours of tool availability. Whether the tool is held continuously and how much each piece occupies it must match the selected capability configuration.

## 4. One Processing Cycle, Multiple Outputs

A mold produces two A pieces, two B pieces and one C piece per cycle. The corresponding adaptor records share a joint-processing group. Ten cycles produce 20, 20 and 10 pieces.

Against demand of 18, 20 and 12, the differences are two surplus A pieces, no B difference and two missing C pieces. Running two more cycles depends on the trade-off between extra A/B inventory and C shortage. Count a shared cycle once when calculating resource occupancy; apply the declared material-consumption basis without duplicating shared processing time.

## 5. Converting Cumulative Supply to Increments

Suppose the source reports cumulative availability of 80 and 120 pieces, while the input chain sums period increments:

| Period | Source cumulative quantity | Readiness increment written | Cumulative quantity used |
|---|---:|---:|---:|
| 1 | 80 | 80 | 80 |
| 2 | 120 | 40 | 120 |

Writing 80 and 120 and then summing them incorrectly creates 200 available pieces. If the second record is remaining stock instead, account for consumption, commitments and holds before conversion. Subtracting two stock snapshots is insufficient.

For a material hold or cancelled delivery, rebuild the future availability curve and apply the agreed handling of reductions. This course's nonnegative-increment example does not accept unexplained negative records.

## 6. Converting Stock Targets to Cumulative Production Bounds

Opening stock is 20 pieces, the stock range is 20–100, and issues are 80 followed by 40:

| Checkpoint | Cumulative issues | Cumulative production minimum | Cumulative production maximum |
|---|---:|---:|---:|
| End of period 1 | 80 | 80 | 160 |
| End of period 2 | 120 | 120 | 200 |

Write each pair as the product's bounds at that point. They are cumulative checkpoints: adding 80 and 120 does not give the second-period minimum. Issues occurring before production receipts may require finer time representation.

## 7. Using an Integer Template with Other Units

A process consumes 0.2 liters of coating per piece, but the current `ingredient.number` field is integer-valued. Use milliliters consistently: write 200 per piece, and convert supply, inventory and result descriptions to the same unit. Forty liters becomes 40,000 milliliters, enough for 200 pieces.

Record the source unit, target unit, conversion factor and rounding policy. Do not rely on SQLite's permissive storage to preserve decimals in integer columns throughout loading and solving.

## 8. Checking a Chosen Pattern

Document the business condition, interface records, expected calculation, model adoption and result check. Verify a small example by hand before scaling the dataset. The [worked example](Interface-Walkthrough.md) provides structure checks and an actual data-layer loading procedure.
