# 02 Express Orders, Products, and Attributes

[中文](Interface-02-Demand-zh-CN.md) · [Learning guide](Interface-Guide.md) · [Semantic guide](Interface-Semantics.md)

## Turn One Order into Schedulable Requirements

A customer needs 120 blue brackets: 80 on day one and 40 on day two. Keep one order identity while expressing two due-date requirements.

Create product P-1 with record `id=1`. A product attribute column references an attribute record; it does not store the word “Blue” directly.

| Table | id | name | code | value | is_key |
|---|---:|---|---|---:|---:|
| property_1 | 1 | Color | BLUE | 1 | 1 |

| product.id | name | code | vin | property_1 | property_2 | property_3 |
|---:|---|---|---|---:|---|---|
| 1 | Blue bracket | P-1 | FIN-P1 | 1 | NULL | NULL |

Here, `property_1` represents color. The name identifies the dimension, code BLUE identifies blue, and numeric value 1 is its stable numeric representation. `vin` identifies the finished item to which the product belongs without determining assembly quantities. Key attributes distinguish products in demand. If a rule uses color, also confirm that the attribute has been loaded.

## Create a Header and Two Lines

Order 1 in `order_info` has code `O-100`, description “Staged delivery of blue brackets,” and priority 0. Its creation time may retain the source timestamp.

| order_item.id | information | product | delivery_time | number |
|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 80 |
| 2 | 1 | 1 | 2 | 40 |

`information=1` references the header; `product=1` references the product; `delivery_time` references lesson one's periods. Enter 80 and 40, rather than cumulative quantities 80 and 120. Any cumulative fulfillment calculation belongs to the subsequent model interpretation.

## Map an Attribute to a Business Name

This data-acquisition fragment maps `color` to the attribute position used in this scenario:

```yaml
context:
  inputs:
    data_acquisition:
      property_mappings:
        color: property_1
```

It is part of a capability-orchestration recipe, which combines data, parameters, and actions into a workflow; it is not a complete solving recipe. Another scenario may place color in a different attribute table while retaining the same explicit business meaning.

## Check Your Work

Resolve all header, product, time, and attribute references. Confirm that the lines total 120 units and that cancellations or deliveries have been handled consistently. Keep ID-to-code conversion in the source mapping; the string `P-1` cannot replace the integer product foreign key.

Different products on one order need separate product records. Do not mix color and customer grade in one attribute position. Adding dimensions requires coordinated template and loading changes; three tables are the current representation, not a design limit.

## Exercise and Answer

The customer moves the second delivery to day three. Add a valid third time unit, then change the second line's `delivery_time` to its ID. Quantity remains 40. A nonexistent due-period reference is invalid even when total demand is correct.

That step checks the order-to-time reference only. To recalculate inventory, materials and capacity, update the related files below as well. Order demand, expected stock issues and candidate output are separate objects. This exercise issues goods on their due dates; that assumption is not universal.

| File or table | Change for the three-period exercise |
|---|---|
| `time_unit`, `order_item` | Add `(id=3, offset=2, scale=28800, status=1)`; move line 2's due time to 3 |
| `capacity` | Add period 3 for work centers 11 and 12, each with `used=0` |
| `scenario.json` | Set `period_issues` to `[80,0,40]` in `time_unit.offset` order; opening stock remains 20 |
| `inventory_limit` | Cumulative production lower bounds: 80,80,120; upper bounds: 160,160,200, representing ending stock between 20 and 100 |
| `kitting_information` | Keep period 2 arrivals of 40 and 80; period 3 increments are zero, not cumulative supply of 120 and 240 |
| `manual_candidate.csv` | Move both 40-unit period 2 output rows to period 3; no production in period 2 |

From the `examples` directory, build a complete extension in a separate folder:

```bash
python build_example.py --third-period --output-dir ./third-period-example
python check_example.py ./third-period-example/data.db
python calculate_candidate.py ./third-period-example
```

The builder applies the [three-period SQL changes](../../assets/data-interface/examples/third-period.sql) and updates JSON, candidate CSV and table CSV files together. It refuses to overwrite an existing database. When editing manually, maintain every item in the table. Editing an exported CSV does not automatically update `data.db`.

Expected cumulative output is 80,80,120, with ending stock of 20 in every period. Both `aggregate_checks_passed` and `issues_match_due_quantities` are `true`. There are no period 2 candidate rows; period 3 stamping and assembly take 100 and 80 minutes respectively. These are manual calculations, not solver results.

Adding only a time unit produces an `errors` message identifying the issue-plan length. Extending only the issue plan then identifies missing inventory limits or capacity records. Changing only the second order quantity from 40 to 400 produces a `-360` difference in `demand_issue_comparison`; unchanged inventory arithmetic does not mean demand was met.

[Previous](Interface-01-Calendar.md) · [Next: resources](Interface-03-Resources.md)
