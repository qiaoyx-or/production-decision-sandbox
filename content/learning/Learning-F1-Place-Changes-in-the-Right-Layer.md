# F1 Locate the Layer That Should Handle a Change

[中文](Learning-F1-Place-Changes-in-the-Right-Layer-zh-CN.md) · [Learning Center](Learning-Center.md)

## The Key Question Is Where a Change Belongs
A new product may require route and material records. A previously unsupported scheduling structure may require model adaptation. Both are business changes, but the engineering work differs. Layering gives each change a place and makes review scope easier to define.

## Four Parts of DecisioWorks
| Part | Responsibility | Typical changes |
|---|---|---|
| DataSets and the standard interface | Scenario data and manufacturing relationships | Orders, routes, capacity and bills of materials (BOMs) |
| DecisioCore | Data, objectives, rules, orchestration, analysis and linkage | Preferences, industry logic and feedback |
| GOCK | Modeling and optimization | Model or solving capability upgrades |
| Web and other applications | Presentation, operation and interaction | Reports, training pages and workflows |

Within DecisioCore, data integration, objective management (`objective_system`), rule control (`marginal_control`), engine adaptation (`engine_adapters`), result analysis (`analysis`) and planning coordination (`planning_system`) have distinct roles. Its available reference implementation lets developers understand and reuse those connections or implement their own calling layer.

## Map One Change
Suppose a customer wants a display grouped by color and a stronger preference for fewer color changes. These are separate requests. Grouping belongs in the application. The preference requires a color mapping and a supported changeover measure before adjusting the objective. Sorting a table does not change the solver's sequence.

| Change | First check | Recheck after the change |
|---|---|---|
| Processing-time update | Units and process adaptation | Load, delivery and results |
| Delivery preference | Objective measure and direction | Trade-offs, details and audit |
| Temporary resource allowance | Affected object and how the model applies the rule | Enforcement and expiry |
| New result display | Analysis fields and units | Numerical consistency and readability |
| New model capability | Input/output adaptation | Support, status and existing calls |

## Independent Evolution Still Needs Compatibility Checks
Interfaces let modules improve separately. After adding fields, changing units or replacing a model, check input meanings, output structure and existing cases to confirm that the parts still work together. Evolution means adapting on the foundation while preserving the parts that continue to work.

The reference implementation helps partners see what can be reused and what needs adaptation. An application can use its own interface, integration or workflow while invoking optimization through defined connections.

## Exercise and Review
Locate four changes: a new product, a delivery preference, an approval page and a new model capability. Identify one cross-layer effect for each.

An approval page belongs to the application, but if approval determines task release it must connect to planning inputs. Record the primary owner and affected interfaces. Layering provides responsibilities, not complete independence from consequences.

## Further Reading

[Design Principles and Differentiation](https://github.com/qiaoyx-or/decisioworks/wiki/Design-Principles-and-Differentiation) · [Architecture Overview](https://github.com/qiaoyx-or/decisioworks/wiki/Architecture-Overview) · [Production Decision Data Assets](https://github.com/qiaoyx-or/decisioworks/wiki/Production-Decision-Data-Assets) · [Ecosystem Overview](https://github.com/qiaoyx-or/decisioworks/wiki/Ecosystem-Overview) · [Partner Onboarding and Integration](https://github.com/qiaoyx-or/decisioworks/wiki/Partner-Onboarding-and-Integration)

Worksheets: [Worksheet: Scenario and Decision Task](Worksheet-Scenario-Brief.md) · [Worksheet: Review and Change Record](Worksheet-Review-and-Change-Record.md)

[Topic F](Learning-Topic-F-Open-Collaboration-and-Evolution.md) · [Previous: Define the Scope of a Disruption Response](Learning-E3-Scope-a-Disruption-Response.md) · [Next: Preserve Experience in Data Assets and Industry Templates](Learning-F2-Preserve-Data-Assets-and-Templates.md)
