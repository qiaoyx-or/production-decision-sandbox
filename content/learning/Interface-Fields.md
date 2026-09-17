# Complete Field Reference

[中文](Interface-Fields-zh-CN.md) · [Semantic guide](Interface-Semantics.md)

This reference covers 18 tables and 105 fields in the current standard SQLite template. Business meaning comes from the semantic system; types, nullability, and object defaults describe this implementation. Object defaults belong to ORM construction, not automatic database defaults during raw SQL insertion. The supplied SQL specifies required values explicitly. Nullable storage does not make a relationship optional for every scenario.

Interpret quantity units alongside the scenario unit mapping. OEE defaults to 100 as a percentage; capacity.used is a fraction from 0 to 1. Confirm model adoption through capability configuration and execution evidence.

## capacity

| Field | Storage type | Nullable | Object default | Unit | Meaning |
|---|---|---|---|---|---|
| `id` | INTEGER | No | `generated key` | identifier | Record primary key for references. |
| `time_unit` | INTEGER | No | `none` | foreign key | Capacity period referencing time_unit.id. → `time_unit.id` |
| `used` | FLOAT | No | `0.0` | fraction | Occupied or unavailable fraction [0,1]; normal-period availability is scale×(1−used). |
| `workcenter` | INTEGER | Yes | `None` | foreign key | Resource owning the capacity, referencing workcenter.id. → `workcenter.id` |

## ingredient

| Field | Storage type | Nullable | Object default | Unit | Meaning |
|---|---|---|---|---|---|
| `id` | INTEGER | No | `generated key` | identifier | Record primary key for references. |
| `process` | INTEGER | No | `none` | foreign key | Consuming operation referencing process.id. → `process.id` |
| `material` | INTEGER | No | `none` | foreign key | Required material referencing material.id. → `material.id` |
| `number` | INTEGER | No | `0` | material units per output unit | Operation material coefficient; this course uses one unit of operation output, consistent with output and supply units. |
| `priority` | INTEGER | No | `0` | priority | Preference among substitute supplies, applied by the relevant selection policy. |

## inventory_limit

| Field | Storage type | Nullable | Object default | Unit | Meaning |
|---|---|---|---|---|---|
| `id` | INTEGER | No | `generated key` | identifier | Record primary key for references. |
| `product` | INTEGER | No | `none` | foreign key | Constrained product referencing product.id. → `product.id` |
| `time_unit` | INTEGER | No | `none` | foreign key | Period of the bound referencing time_unit.id. → `time_unit.id` |
| `binding` | INTEGER | Yes | `None` | group id | Common value denotes shared inventory, with explicit units and allocation. |
| `upper_bound_acc` | INTEGER | Yes | `None` | cumulative product units | Cumulative production-receipt ceiling derived from opening stock, flows, and capacity; null means unspecified. |
| `urgency` | FLOAT | No | `0.0` | declared scale | Urgency or turnover-related value interpreted by the business policy. |
| `lower_bound_acc` | INTEGER | Yes | `None` | cumulative product units | Cumulative production-receipt floor derived from safety-stock or similar requirements; null means unspecified. |

## kitting_information

| Field | Storage type | Nullable | Object default | Unit | Meaning |
|---|---|---|---|---|---|
| `id` | INTEGER | No | `generated key` | identifier | Record primary key for references. |
| `time_unit` | INTEGER | No | `none` | foreign key | Availability period referencing time_unit.id. → `time_unit.id` |
| `material` | INTEGER | No | `none` | foreign key | Ready material referencing material.id. → `material.id` |
| `number` | INTEGER | No | `0` | material units | Ready quantity; the cumulative-input exercise uses opening availability and later increments, not repeated cumulative snapshots. |

## material

| Field | Storage type | Nullable | Object default | Unit | Meaning |
|---|---|---|---|---|---|
| `id` | INTEGER | No | `generated key` | identifier | Record primary key for references. |
| `code` | VARCHAR | No | `''` | code | Business material code. |
| `name` | VARCHAR | No | `''` | text | Material name. |
| `vendor` | VARCHAR | No | `''` | code or text | Supplier information. |
| `substitute` | INTEGER | Yes | `None` | group id | Common value identifies substitutes; null indicates no substitute group. |
| `binding` | INTEGER | Yes | `None` | group id | Material dependency or coordinated selection relationship, with a defined interpretation and policy. |
| `extend` | INTEGER | Yes | `None` | extension-specific | Reserved extension, for example supplier priority; currently an integer, with meaning and allowed values defined before use. |

## order_info

| Field | Storage type | Nullable | Object default | Unit | Meaning |
|---|---|---|---|---|---|
| `id` | INTEGER | No | `generated key` | identifier | Record primary key for references. |
| `description` | VARCHAR | No | `''` | text | Order description. |
| `priority` | INTEGER | No | `0` | priority | Order-header priority; the adopting policy defines its ordering direction. |
| `code` | VARCHAR | Yes | `''` | code | Business order code. |
| `created_at` | DATETIME | Yes | `None` | timestamp | Order creation timestamp, retained rather than mapped to a planning time unit. |

## order_item

| Field | Storage type | Nullable | Object default | Unit | Meaning |
|---|---|---|---|---|---|
| `id` | INTEGER | No | `generated key` | identifier | Record primary key for references. |
| `product` | INTEGER | No | `none` | foreign key | Demanded product referencing product.id; the design name production_id denotes this product reference. → `product.id` |
| `information` | INTEGER | No | `none` | foreign key | Parent order referencing order_info.id; corresponds to order_information_id. → `order_info.id` |
| `delivery_time` | INTEGER | Yes | `None` | foreign key | Due-period reference to time_unit.id; a dated requirement needs a valid reference. → `time_unit.id` |
| `number` | INTEGER | No | `0` | product units | Quantity for this delivery requirement; record period requirements without duplicating cumulative totals. |

## planning_result

| Field | Storage type | Nullable | Object default | Unit | Meaning |
|---|---|---|---|---|---|
| `id` | INTEGER | No | `generated key` | identifier | Record primary key for references. |
| `workcenter` | INTEGER | Yes | `None` | foreign key | workcenter.id executing the planned work. → `workcenter.id` |
| `time_unit` | INTEGER | No | `None` | foreign key | Execution period referencing time_unit.id. → `time_unit.id` |
| `process` | INTEGER | Yes | `None` | foreign key | Executed operation referencing process.id; a documented empty sequence slot may use null. → `process.id` |
| `number` | INTEGER | No | `0` | operation-output units | Planned output, not cycle count; sums across operations are not finished deliveries. |
| `value_1` | INTEGER | No | `0` | scenario-specific | Extension field; a circular schedule may define a cycle number. |
| `value_2` | INTEGER | No | `0` | scenario-specific | Extension field; a circular schedule may define a sequence position. |
| `value_3` | INTEGER | No | `0` | scenario-specific | Reserved extension field; define its meaning before use. |

## process

| Field | Storage type | Nullable | Object default | Unit | Meaning |
|---|---|---|---|---|---|
| `id` | INTEGER | No | `generated key` | identifier | Record primary key for references. |
| `route` | INTEGER | No | `none` | foreign key | Owning route referencing process_route.id. → `process_route.id` |
| `name` | VARCHAR | No | `''` | text | Operation name. |
| `code` | VARCHAR | Yes | `''` | code | Business operation code. |
| `operation_number` | INTEGER | No | `1` | number | Operation number within a route; separate from execution order and checked for route-level uniqueness. |
| `seqno` | INTEGER | No | `1` | sequence | Precedence value; equal values mean no precedence, while concurrency depends on other conditions. |

## process_adaptor

| Field | Storage type | Nullable | Object default | Unit | Meaning |
|---|---|---|---|---|---|
| `id` | INTEGER | No | `generated key` | identifier | Record primary key for references. |
| `process` | INTEGER | Yes | `None` | foreign key | Mapped operation referencing process.id. → `process.id` |
| `workcenter` | INTEGER | Yes | `None` | foreign key | Compatible execution resource referencing workcenter.id. → `workcenter.id` |
| `priority` | INTEGER | No | `0` | priority | Priority of this resource option for the operation. |
| `wip_buffer_size` | INTEGER | No | `0` | declared quantity unit | WIP buffer capacity; check the model meaning of zero and how the limit is applied. |
| `productivity` | INTEGER | No | `1` | units per cycle | Per-cycle output in the current discrete template; a continuous interpretation requires an explicit rate conversion. |
| `processing_time` | FLOAT | No | `0.0` | seconds per cycle | Standard duration per cycle; convert source cycle or rate data to this basis. |
| `setup_time` | FLOAT | No | `0.0` | seconds | Operation changeover time; specify whether initial setup is included. |
| `batch_size` | INTEGER | No | `1` | product units | Batch quantity, an integer multiple of per-cycle output. |
| `OEE` | INTEGER | No | `100` | percent | Overall equipment effectiveness; current default 100, with the loss-accounting layer specified by configuration. |
| `binding` | INTEGER | Yes | `None` | group id | Equal values join jointly processed operations; null or a singleton does not form a multi-operation group. |

## process_route

| Field | Storage type | Nullable | Object default | Unit | Meaning |
|---|---|---|---|---|---|
| `id` | INTEGER | No | `generated key` | identifier | Record primary key for references. |
| `product` | INTEGER | No | `none` | foreign key | Route owner referencing product.id; one product can have multiple routes. → `product.id` |
| `name` | VARCHAR | No | `''` | text | Route name. |
| `code` | VARCHAR | No | `''` | code | Business route code. |
| `priority` | INTEGER | No | `0` | priority | Route-selection priority interpreted by the routing policy. |
| `description` | VARCHAR | Yes | `''` | text | Business description of the route. |

## product

| Field | Storage type | Nullable | Object default | Unit | Meaning |
|---|---|---|---|---|---|
| `id` | INTEGER | No | `generated key` | identifier | Record primary key for references. |
| `name` | VARCHAR | No | `''` | text | Name of a finished item, intermediate item, or component. |
| `code` | VARCHAR | No | `''` | code | Business product code, managed separately from record id. |
| `vin` | VARCHAR | Yes | `''` | code | Unique code of the finished item to which the product belongs; it does not define assembly quantities by itself. |
| `property_1` | INTEGER | Yes | `None` | foreign key | References property_1.id; declare its business dimension for the scenario. → `property_1.id` |
| `property_2` | INTEGER | Yes | `None` | foreign key | References property_2.id as another classification dimension. → `property_2.id` |
| `property_3` | INTEGER | Yes | `None` | foreign key | References property_3.id; null means no associated value in this dimension. → `property_3.id` |

## property_1

| Field | Storage type | Nullable | Object default | Unit | Meaning |
|---|---|---|---|---|---|
| `id` | INTEGER | No | `generated key` | identifier | Record primary key for references. |
| `name` | VARCHAR | No | `''` | text | Attribute name, such as model, configuration or color; interpreted with its code and value. |
| `code` | VARCHAR | Yes | `''` | code | Attribute code with stable classification and mapping within the scenario. |
| `value` | FLOAT | Yes | `None` | dimension-specific | Numeric attribute value; the current SQLite type is FLOAT, with text labels in name and code. |
| `is_key` | BOOLEAN | No | `False` | boolean | Marks an attribute needed to distinguish demanded products; the current loader uses it to select attribute fields. |

## property_2

| Field | Storage type | Nullable | Object default | Unit | Meaning |
|---|---|---|---|---|---|
| `id` | INTEGER | No | `generated key` | identifier | Record primary key for references. |
| `name` | VARCHAR | No | `''` | text | Attribute name, such as model, configuration or color; interpreted with its code and value. |
| `code` | VARCHAR | Yes | `''` | code | Attribute code with stable classification and mapping within the scenario. |
| `value` | FLOAT | Yes | `None` | dimension-specific | Numeric attribute value; the current SQLite type is FLOAT, with text labels in name and code. |
| `is_key` | BOOLEAN | No | `False` | boolean | Marks an attribute needed to distinguish demanded products; the current loader uses it to select attribute fields. |

## property_3

| Field | Storage type | Nullable | Object default | Unit | Meaning |
|---|---|---|---|---|---|
| `id` | INTEGER | No | `generated key` | identifier | Record primary key for references. |
| `name` | VARCHAR | No | `''` | text | Attribute name, such as model, configuration or color; interpreted with its code and value. |
| `code` | VARCHAR | Yes | `''` | code | Attribute code with stable classification and mapping within the scenario. |
| `value` | FLOAT | Yes | `None` | dimension-specific | Numeric attribute value; the current SQLite type is FLOAT, with text labels in name and code. |
| `is_key` | BOOLEAN | No | `False` | boolean | Marks an attribute needed to distinguish demanded products; the current loader uses it to select attribute fields. |

## shared_resource

| Field | Storage type | Nullable | Object default | Unit | Meaning |
|---|---|---|---|---|---|
| `id` | INTEGER | No | `generated key` | identifier | Record primary key for references. |
| `binding` | INTEGER | Yes | `None` | foreign key | workcenter.id representing the shared resource itself. → `workcenter.id` |
| `to` | INTEGER | Yes | `None` | foreign key | Target workcenter.id depending on the resource. → `workcenter.id` |

## time_unit

| Field | Storage type | Nullable | Object default | Unit | Meaning |
|---|---|---|---|---|---|
| `id` | INTEGER | No | `generated key` | identifier | Record primary key for references. |
| `offset` | INTEGER | No | `0` | order | Sequence offset from the planning origin; distinct from the primary key. |
| `scale` | INTEGER | No | `8 * 60 * 60` | seconds | Period length: 3600 for an hour, 28800 for an eight-hour window. |
| `status` | INTEGER | No | `1` | state | 1 normal, 0 unavailable, -1 special or optional; specify how optional time is adopted. |

## workcenter

| Field | Storage type | Nullable | Object default | Unit | Meaning |
|---|---|---|---|---|---|
| `id` | INTEGER | No | `generated key` | identifier | Record primary key for references. |
| `name` | VARCHAR | No | `''` | text | Work-center name, such as a machine, team, area, subcontractor, or organization. |
| `code` | VARCHAR | Yes | `''` | code | Business resource code. |
| `type` | INTEGER | No | `0` | category | 0 for a leaf node; nonzero for a non-leaf. |
| `parallelism` | INTEGER | No | `1` | parallel units | Number of parallel units, modeled separately from station count. |
| `station_count` | INTEGER | No | `1` | stations | Station count, interpreted for the actual structure such as a furnace or circular line. |
| `equipping_time` | FLOAT | No | `0` | duration | Work-center preparation duration; seconds in this course, accounted separately from operation changeovers. |
| `parent_id` | INTEGER | Yes | `None` | foreign key | Parent workcenter.id; null for a root. → `workcenter.id` |

## Naming and Extensions

`order_information → order_info`; `order_information_id → information`; `product_id → product`; `time_unit_id → time_unit` (or `delivery_time` for an order due date); `route_id → route`; `process_id → process`; `material_id → material`; `workcenter_id → workcenter`; `parent → parent_id`.

The attribute mechanism extends to property_n; three tables are an implementation choice. decision_node is an engineering extension outside these 18 standard tables. Map or extend source information such as scrap, yield, or approval times explicitly rather than changing standard field meanings.

## Representation Differences Between Design Examples and the Current Template

The semantic guide defines business meaning; the template records actual storage requirements. Interpret these differences explicitly rather than changing documented types or defaults to make them appear identical.

| Field | Structural design example | Current template | Usage requirement |
|---|---|---|---|
| `process_adaptor.OEE` | FLOAT, default 100 | INTEGER, default 100 | Define precision and conversion for fractional percentages; do not silently truncate |
| `process_adaptor.wip_buffer_size` | Default 1 | Default 0 | Establish the meaning of zero; do not assume unlimited capacity |
| `property_i.value` | Default 0 | Nullable, default None | Distinguish missing values from zero |
| `property_i.is_key` | Default NULL | Non-null, default False | Distinguish unspecified from non-key and check loading |
| `product.vin/property_i` | Non-null examples with extensible attributes | Nullable vin and three attribute references | Distinguish unused dimensions from missing required data |
| `process_adaptor.process/workcenter`, `capacity.workcenter` | Non-null example foreign keys | Nullable | Executable tasks and capacity still need complete resource relationships |
| `planning_result.workcenter/process` | Non-null example foreign keys | Nullable | Distinguish valid operation results from documented empty slots |

This is not an exhaustive physical-schema diff. Table names, column names, and database forms can be mapped while preserving business meanings.

[Relationships and rules](Interface-Relationships.md) · [Patterns](Interface-Configurations.md) · [Teaching database](Interface-Walkthrough.md)
