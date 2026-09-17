# Object Relationships and Calculation Rules

[中文](Interface-Relationships-zh-CN.md) · [Learning guide](Interface-Guide.md) · [Field reference](Interface-Fields.md)

The field reference shows where values belong. This page explains how records connect and which quantities can be compared. Identify source objects by their business codes, then translate their references into target record IDs.

## 1. Demand and Manufacturing Relationships

| Relationship | Current fields | What to check |
|---|---|---|
| An order contains multiple lines | `order_item.information → order_info.id` | Every line belongs to an existing order; split one product across due periods when needed |
| Multiple demand lines can reference one product | `order_item.product → product.id` | Use the product ID, not the order-line ID |
| A product references records in its attribute dimensions | `product.property_i → property_i.id` | Keep foreign keys, text labels and numeric values distinct |
| A product can have alternative routes | `process_route.product → product.id` | Alternatives are manufacturing choices, not additional demand |
| A route contains operations | `process.route → process_route.id` | `operation_number` identifies an operation within the route; `seqno` defines precedence |
| An operation can run on alternative resources | `process_adaptor.process/workcenter` | Each record describes one operation-resource combination and its parameters |
| An operation uses materials | `ingredient.process/material` | Define the consumption basis and trace each material to its supply |

Equal `seqno` values mean there is no precedence between those operations. They do not need to be made unique. Whether the operations can run simultaneously is a separate resource and material question.

## 2. Time and Resource Relationships

| Reference | Target | Business question |
|---|---|---|
| `order_item.delivery_time` | `time_unit.id` | When is demand due? |
| `capacity.time_unit` | `time_unit.id` | Which period does this resource availability describe? |
| `kitting_information.time_unit` | `time_unit.id` | When can the material be used? |
| `inventory_limit.time_unit` | `time_unit.id` | At which point is cumulative receipt checked? |
| `planning_result.time_unit` | `time_unit.id` | In which period is operation output recorded? |
| `capacity.workcenter` | `workcenter.id` | Which resource has this unavailable fraction? |
| `workcenter.parent_id` | `workcenter.id` | Which organizational node owns the resource? |
| `shared_resource.binding/to` | Two `workcenter.id` values | Which shared resource serves which target resource? |

The resource hierarchy should lead to a root without self-reference or cycles. Check shared-resource links for accidental self-binding as well. A shared resource may serve multiple targets, and a target may depend on multiple shared resources.

Calendar completeness depends on the resources and periods included in a run. When a resource-period record is missing, determine whether availability is unconfigured or covered by an explicit default. Do not assume full availability.

## 3. Materials, Inventory and Results

`kitting_information.material` references a material. `inventory_limit.product` references a product. Keep their inventory meanings distinct: the former describes readiness for operation consumption; the latter constrains cumulative production receipts of a product.

`planning_result.process` leads through the route to the product; `workcenter` identifies the actual resource. In addition to existing individually, the operation and resource should form an allowed combination for the scenario. Delivery quantities must follow the manufacturing path actually selected.

Some references are nullable in the database. A particular exercise or capability may still require them. For example, this course needs both operation and resource references to recalculate its result rows.

## 4. Fields That Share a Name but Not a Meaning

| Field | Object | Meaning |
|---|---|---|
| `binding` | `material` | Dependent material-choice group |
| `binding` | `process_adaptor` | Joint-processing group |
| `binding` | `inventory_limit` | Shared-inventory group |
| `binding` | `shared_resource` | Shared-resource work-center ID; a foreign key |
| `priority` | Order, route, adaptor, BOM | Preference within that object type; check the configured ordering direction |
| `number` | Order line | Demand quantity |
| `number` | Operation BOM | Material requirement on the declared basis |
| `number` | Material readiness | Available quantity on the declared incremental or cumulative basis |
| `number` | Planning result | Operation output quantity |

Equal group numbers do not create cross-table relationships. Material `binding=1` and inventory `binding=1`, for example, are unrelated unless a separate mapping explicitly connects them.

## 5. Quantity and Time Calculations

These calculations assume discrete processing on one resource, with no scrap or setup losses. Define additional conversions when applying OEE, parallel processing, joint output or shared inventory.

| Question | Calculation | Example |
|---|---|---|
| Available time in a normal period | `scale × (1 − used)` | 28,800 seconds × 0.75 = 21,600 seconds |
| Processing cycles | Output ÷ output per cycle | 80 ÷ 4 = 20 cycles |
| Pure processing time | Cycles × cycle duration | 20 × 600 seconds = 200 minutes |
| Whole-batch configuration | Batch ÷ output per cycle must be an integer | 20 ÷ 4 = 5 cycles per batch |
| Material consumption | Operation output × requirement per piece | 80 assembled pieces × 2 fasteners = 160 fasteners |
| Cumulative supply | Opening availability + effective later increments | 80 + 40 = 120 pieces |
| Ending inventory | Opening stock + cumulative receipts − cumulative issues | 20 + 120 − 120 = 20 pieces |

If 80 pieces pass through stamping and assembly, finished output is 80 pieces. Adding the two operation rows gives 160 operation-output records, not 160 finished pieces.

## 6. Complete Three Separate Checks

**Structure:** tables, fields, types, primary keys and foreign keys.

**Business meaning:** units, relationship direction, time coverage, batch rules, supply and inventory conventions.

**Run behavior:** the resource, material and precedence rules actually used by the selected configuration, and whether the output can be checked against them.

The accompanying validator checks a defined subset of structure and business rules for the worked example. Add capability-specific checks for a complete production scenario. Select a suitable [configuration pattern](Interface-Configurations.md), then follow the [worked example](Interface-Walkthrough.md).
