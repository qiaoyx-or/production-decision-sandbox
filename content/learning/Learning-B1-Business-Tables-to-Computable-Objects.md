# B1 From Business Tables to Computable Objects

[中文](Learning-B1-Business-Tables-to-Computable-Objects-zh-CN.md) · [Learning Center](Learning-Center.md)

## Identical Column Names Can Mean Different Things
A quantity may refer to ordered units, cartons or the remaining balance. A date may mean order entry, promised delivery or expected material arrival. Define the business meaning before mapping fields. Enterprise resource planning (ERP) systems, manufacturing execution systems (MES), spreadsheets and manually prepared records can all be sources; the required meanings and relationships remain consistent.

Use teaching order O-7: product P-1, demand of 120 units, due in time unit T-3. The table illustrates semantic mapping. Actual identifier types depend on the data template.

| Source information | Standard object or field | Check |
|---|---|---|
| Product P-1 | product and order_item.product | The order references an existing product |
| Remaining demand of 120 units | order_item.number | Delivered quantities have been handled consistently |
| Promised due time T-3 | order_item.delivery_time | It resolves to time_unit and means the required completion point |
| Product color “blue” | Product attribute slot and business mapping | The slot representing color is explicit |

## Check Relationships, Not Just Rows
Resolve the product from the order, then trace its route, ordered operations and eligible work centers. When material constraints apply, connect operation requirements to material availability. Nonempty cells cannot repair a broken reference.

Keep original values, interpreted values and conversion rules. For 12 cartons containing ten units each, confirm the packaging rule before converting to 120 units. If the factor is unknown, obtain it rather than assuming one.

## What Makes the Data Computable?
| Check | Example | Response |
|---|---|---|
| Identifier consistency | An order references a missing product | Repair the mapping or complete master data |
| Explicit units | Units and cartons are mixed | Apply a documented conversion |
| Time alignment | A due date has no matching time unit | Inspect the calendar mapping |
| Executable route | An operation has no eligible work center | Confirm the actual resource choices |
| Quantities and batches | Demand is not a batch-size multiple | Confirm whether split batches, residual demand or overproduction are allowed, then check the selected model |

DecisioCore data_layer converts sources into shared business objects for planning and scheduling. Structural validation and solving readiness are separate stages. `ContractReady` means the applicable data-interface checks have passed. `SolverReady` means the data and selected solving capability have passed the checks defined by that report. Read the scenario, version and check scope alongside the status, then use the actual run to assess the plan's feasibility.

## Make One Change
Change O-7's source quantity to 12 cartons, with ten units per carton. Standardized demand remains 120 units, but the mapping explanation changes. If packaging changes later, update the mapping and checks rather than asking the solver to infer the meaning.

## Exercise and Review
Create a five-column record: source field, business meaning, standard object, conversion and check. Ask a business colleague to explain an apparently simple field.

If a mapped due date actually means material arrival, the mapping is wrong even though its type is valid. A useful record preserves definitions, sources and confirmation so another reader can review it independently.

## Further Reading

[Standardized Data Interface](https://github.com/qiaoyx-or/decisioworks/wiki/Standardized-Data-Interface) · [Data Objects and Fields](https://github.com/qiaoyx-or/decisioworks/wiki/Data-Object-and-Field-Reference) · [Data Readiness and Validation](https://github.com/qiaoyx-or/decisioworks/wiki/Data-Readiness-and-Validation) · [ERP and MES Data Mapping](https://github.com/qiaoyx-or/decisioworks/wiki/ERP-MES-Data-Mapping-Guide)

Worksheets: [Worksheet: Scenario and Decision Task](Worksheet-Scenario-Brief.md)

[Topic B](Learning-Topic-B-Manufacturing-Data.md) · [Previous: Compare Two Plans on the Same Basis](Learning-A3-Compare-Plans-on-the-Same-Basis.md) · [Next: Process Routes and Operation-Level BOMs](Learning-B2-Routes-and-Operation-Level-BOM.md)
