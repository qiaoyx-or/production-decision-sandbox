# 04 Configure Routes and Alternative Resources

[中文](Interface-04-Routing-zh-CN.md) · [Learning guide](Interface-Guide.md) · [Semantic guide](Interface-Semantics.md)

## Task: Connect a Product to Executable Operations

Bracket P-1 is stamped and then assembled. Create route 101 for product 1, with code `ROUTE-P1` and priority 0. The route references the product through `product`; operations reference it through `route`.

| process.id | route | name | code | operation_number | seqno |
|---:|---:|---|---|---:|---:|
| 1001 | 101 | Stamping | STAMP | 10 | 1 |
| 1002 | 101 | Assembly | ASSEMBLE | 20 | 2 |

Numbers 10 and 20 identify operations; sequence values 1 and 2 express precedence. Separating identity and order lets precedence change without renaming the operations.

## Connect Work Centers

The base configuration uses two mappings, with durations in seconds:

| id | process | workcenter | productivity | batch_size | processing_time | setup_time |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1001 | 11 | 4 | 20 | 600 | 0 |
| 2 | 1002 | 12 | 1 | 20 | 120 | 0 |

Both records use `priority=0`, `wip_buffer_size=120`, `OEE=100`, and `binding=NULL`. Buffer capacity is measured in operation-output units here; check the relevant capability configuration to establish whether it becomes a model restriction.

Trace the order using the actual foreign-key relationships below. Some steps follow references in reverse, from a product to its candidate routes:

```text
order_item.product        -> product.id
process_route.product     -> product.id
process.route             -> process_route.id
process_adaptor.process   -> process.id
process_adaptor.workcenter-> workcenter.id
```

Each referenced identifier needs an actual record.

## Add an Alternative Machine or Route

If stamping can also run on work center 13, add an adaptor with the same `process=1001` and the new resource, using that machine's real output and duration. Keep one operation identity for alternative execution resources.

If the manufacturing method changes the operation chain, such as outsourced forming followed by assembly, create a different route and its operations. Distinguish resource choice for an operation from manufacturing-path choice for a product. Confirm route and resource selection policies separately; alternative resources do not multiply product demand.

## Interpret Equal Sequence Values

For two independent inspection steps in another exercise, use distinct `operation_number` values and equal `seqno` values. This removes precedence between the checks. A common inspector, instrument, or material condition may still prevent simultaneous execution. Match this semantic relationship to the selected model's support for parallel operations.

## Check and Practice

Check route ownership, operation numbering, sequence values, references, and parameters for each resource option. Add surface treatment between stamping and assembly: retain numbers 10 and 20, introduce number 15, and use sequence values 1, 2, and 3. Add a resource mapping and material requirements for the new step. A node in a diagram without an adaptor still lacks an executable resource.

[Previous](Interface-03-Resources.md) · [Next: quantities and duration](Interface-05-Quantity.md)
