# F2 Preserve Experience in Data Assets and Industry Templates

[中文](Learning-F2-Preserve-Data-Assets-and-Templates-zh-CN.md) · [Learning Center](Learning-Center.md)

## What Can One Integration Leave Behind?
Organizing orders, processes, capacity and materials creates a reviewable description of the business. Even while implementation options are still being assessed, it helps teams agree on meanings, find gaps and avoid repeated preparation. Its value appears through reuse, not database size alone.

Suppose one workshop has completed data integration and wants to transfer the approach to another. The exercise is to document a template another person can understand.

## Data Assets Include Definitions and Checks
| Asset | Preserve | Check during reuse |
|---|---|---|
| Objects and fields | Products, operations, resources and units | Whether matching names mean the same thing |
| Mappings | Sources to standard objects | Referenced products, operations and resources exist and identify the intended objects |
| Rules | Objects, sources, scope and validity | Fit for the new case |
| Orchestration recipes | Actions, sources, objectives and settings | Capabilities, versions and runtime requirements |
| Check examples | Valid and invalid inputs | Whether expected problems are detected |
| Interpretation records | Metrics and trade-off reasons | Whether the reasoning can be reproduced |

Manage templates separately from customer records. Shareable templates can contain definitions, relationships, constructed examples and checks. Confirm the permitted use of actual enterprise data.

## Transfer between Workshops
Compare resources, routes, units produced per operation execution, batches, shifts and materials. The shared interface reduces repeated format work, but another workshop may require different processes or rules.

Workshop A may record demand in units while B orders in cartons. Reuse the object definition and conversion check, not A's packaging factor. A useful data asset makes that difference visible and easy to locate.

## Keep a Lightweight Version Record
Record template version, source description, field changes, associated recipes and checks. After changing material consumption, identify affected products and downstream reviews. A consistent version identity prevents two files named data.db from silently representing different facts.

The DecisioWorks standard interface supplies the common structure. Data checks, recipes and analysis records help applications accumulate experience around it. Partners can organize confirmed mappings and rules into templates and check their processes, units and rules against each new case.

## Exercise and Review
Prepare two pages for an integrated sample: one explaining objects and units, another listing five checks before reuse. Add an invalid example, such as an unresolved product reference, and the expected check result.

The asset is useful when another person can use and inspect it correctly. An unexplained database cannot clearly distinguish stable meanings from adjustable parameters.

## Further Reading

[Design Principles and Differentiation](https://github.com/qiaoyx-or/decisioworks/wiki/Design-Principles-and-Differentiation) · [Architecture Overview](https://github.com/qiaoyx-or/decisioworks/wiki/Architecture-Overview) · [Production Decision Data Assets](https://github.com/qiaoyx-or/decisioworks/wiki/Production-Decision-Data-Assets) · [Ecosystem Overview](https://github.com/qiaoyx-or/decisioworks/wiki/Ecosystem-Overview) · [Partner Onboarding and Integration](https://github.com/qiaoyx-or/decisioworks/wiki/Partner-Onboarding-and-Integration)

Worksheets: [Worksheet: Scenario and Decision Task](Worksheet-Scenario-Brief.md) · [Worksheet: Review and Change Record](Worksheet-Review-and-Change-Record.md)

[Topic F](Learning-Topic-F-Open-Collaboration-and-Evolution.md) · [Previous: Locate the Layer That Should Handle a Change](Learning-F1-Place-Changes-in-the-Right-Layer.md) · [Next: Define Roles for Manufacturers, Consultants and Software Partners](Learning-F3-Define-Ecosystem-Responsibilities.md)
