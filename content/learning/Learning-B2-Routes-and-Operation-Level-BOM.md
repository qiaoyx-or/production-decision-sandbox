# B2 Process Routes and Operation-Level BOMs

[中文](Learning-B2-Routes-and-Operation-Level-BOM-zh-CN.md) · [Learning Center](Learning-Center.md)

## A Product BOM Also Needs a Manufacturing Sequence
A bill of materials (BOM) identifies required materials; an operation-level BOM identifies where they are consumed. Teaching product P goes through cutting and assembly. Each unit consumes one blank in cutting and two fasteners in assembly. Planning ten units requires knowing that the 20 fasteners are needed at assembly, because their availability can affect when that operation starts.

| Business object | Teaching example | Relationship |
|---|---|---|
| Product | P | product |
| Route | R-P | process_route.product links to P |
| Operations | Cutting 10, assembly 20 | process.route and process.seqno |
| Resources | Cutter WC-C, assembly station WC-A | process_adaptor links operations and work centers |
| Materials | Blank M-1, fastener M-2 | ingredient links an operation to material |

Sequence values 10 and 20 only specify order. Here, one execution of an operation produces one unit. For operations producing several units per execution, record output per execution and the basis of material consumption separately.

## Connect Material Requirements to Their Consumption Point
Suppose ten blanks are available today and 20 fasteners arrive tomorrow. The business may permit cutting today and assembly tomorrow. Whether intermediate inventory, separated operations and cross-period work can be represented depends on the selected model and enabled constraints. Operation-level data provides the place to examine those questions.

Attaching all materials only to the finished product can hide early-operation requirements. Requiring everything at the first operation can prevent work that could otherwise start. Use the real consumption point.

## Review the Data Step by Step
1. Confirm P's route and any candidate routes.
2. Check operation order, outputs and eligible work centers.
3. Trace each ingredient record to a specific operation and material.
4. Check the basis of consumption, including processing cycles or output units.
5. Align material availability with the planning time axis.

This exercise assumes each finished unit passes through each operation once, without losses or co-products. Ten units therefore require ten blanks and 20 fasteners. For multi-output, scrap or co-product cases, first confirm that the selected model can represent the process. Then calculate from output per execution and material consumption. Output per execution is distinct from the proportion of good units produced.

## Place a Change Correctly
Changing fastener consumption from two to three raises the teaching requirement to 30. Update the confirmed operation-material relationship, check availability, then rerun. A larger delivery weight cannot supply the missing ten fasteners.

A route or alternative-resource change also needs an object-level review. Another route may change materials, output per cycle, and processing duration. For continuous processing, also check output per unit time and its units. Replacing a work-center label alone is insufficient.

## Exercise and Suggested Answer
Add a surface-treatment operation consuming 0.2 liters of fluid per unit. Draw the route, resource and material relationships. Under the no-loss assumption, ten units require two liters.

Explain where the fluid is consumed, its unit, its availability and the eligible resources. This establishes structure and hand calculations. Actual planning results require execution with the corresponding constraints enabled.

## Further Reading

[Standardized Data Interface](https://github.com/qiaoyx-or/decisioworks/wiki/Standardized-Data-Interface) · [Data Objects and Fields](https://github.com/qiaoyx-or/decisioworks/wiki/Data-Object-and-Field-Reference) · [Data Readiness and Validation](https://github.com/qiaoyx-or/decisioworks/wiki/Data-Readiness-and-Validation) · [ERP and MES Data Mapping](https://github.com/qiaoyx-or/decisioworks/wiki/ERP-MES-Data-Mapping-Guide)

Worksheets: [Worksheet: Scenario and Decision Task](Worksheet-Scenario-Brief.md)

[Topic B](Learning-Topic-B-Manufacturing-Data.md) · [Previous: From Business Tables to Computable Objects](Learning-B1-Business-Tables-to-Computable-Objects.md) · [Next: Align Time, Capacity and Material Availability](Learning-B3-Align-Time-Capacity-and-Materials.md)
