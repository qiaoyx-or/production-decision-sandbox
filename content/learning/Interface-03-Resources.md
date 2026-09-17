# 03 Configure Work Centers and Shared Resources

[中文](Interface-03-Resources-zh-CN.md) · [Learning guide](Interface-Guide.md) · [Semantic guide](Interface-Semantics.md)

## Task: Make Resource Relationships Checkable

A shop contains stamping machines A and B and an assembly station. Both machines depend on one fixture. Express organizational ownership, machine availability, and fixture capacity separately.

| workcenter.id | name | code | parent_id | type | station_count | parallelism | equipping_time |
|---:|---|---|---:|---:|---:|---:|---:|
| 10 | Shop | SHOP | NULL | 1 | 1 | 1 | 0 |
| 11 | Stamping A | PRESS-A | 10 | 0 | 1 | 1 | 0 |
| 12 | Assembly | ASSEMBLY | 10 | 0 | 1 | 1 | 0 |
| 13 | Stamping B | PRESS-B | 10 | 0 | 1 | 1 | 0 |
| 20 | Shared fixture | FIXTURE | 10 | 0 | 1 | 1 | 0 |

These are extension records for this lesson. The end-to-end base database uses the shop, stamping A, and assembly; the other records extend it. The shop is an organizational node. Its scalar defaults do not create another set of executable capacity.

Hierarchy also supports common-attribute inheritance, rules at different levels, and aggregate analysis. A shop may define a shared calendar convention while each machine adds its own maintenance. Configuration applies shop-level rules to the participating resources, and analysis aggregates machine-level loads. The teaching table establishes parent relationships; automatic inheritance and rule expansion require the relevant capability. A shop's aggregate load does not create another machine's capacity.

## Keep Links and Availability Separate

`shared_resource` stores the relationships:

| id | binding | to |
|---:|---:|---:|
| 1 | 20 | 11 |
| 2 | 20 | 13 |

`capacity` stores the fixture's own availability:

| id | time_unit | workcenter | used |
|---:|---:|---:|---:|
| 5 | 1 | 20 | 0 |
| 6 | 2 | 20 | 0.5 |

On day two the fixture has half a shift available. Two links do not create two separate half-shifts. `shared_resource` has no `time_unit` or `used` column; availability is reached through the resource work center.

## Find a Conflict Manually

If A needs the fixture for three hours on day two and B needs it for two, their five-hour total exceeds four available hours by one. Eight available machine-hours on each machine do not make the combined plan feasible. Even after the aggregate fits, actual uses must not overlap.

This lesson defines the data and checks the conflict manually. For an actual solve to exclude the conflict, confirm that the model configuration adopts the shared relationship and inspect its result.

## Distinguish Three Relationships

- `parent_id`: organizational ownership, or “belongs to.”
- `process_adaptor`: executable resource compatibility, or “can run on.”
- `shared_resource`: resource dependence, or “also needs.”

`station_count` describes stations; `parallelism` describes parallel units. Solver threads do not represent production resources, and station and parallel counts must not multiply time twice without a valid model interpretation.

## Exercise and Answer

For a second independent fixture, create its resource and calendar, then define which machines can use it. If both fixtures still require the same operator, represent that shared person as well; capacity does not automatically double. Every dependency should resolve to a resource and its time-phased availability.

[Previous](Interface-02-Demand.md) · [Next: routes](Interface-04-Routing.md)
