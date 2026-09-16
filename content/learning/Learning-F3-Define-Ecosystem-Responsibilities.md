# F3 Define Roles for Manufacturers, Consultants and Software Partners

[中文](Learning-F3-Define-Ecosystem-Responsibilities-zh-CN.md) · [Learning Center](Learning-Center.md)

## Work on One Problem with Different Contributions
Manufacturers own production facts, commitments and operational decisions. Consultants structure objectives, conflicts and improvement methods. Software partners connect data, interfaces and runtime environments. DecisioWorks provides reusable production-decision capabilities. Shared objects and clear handoffs connect these contributions.

For this exercise, aim to reduce shop-floor disruption after plan changes. Identify the work that should remain stable, the changes that are acceptable and who approves operational adjustments.

## Organize Roles by Inputs and Outputs
| Role | Provides | Confirms |
|---|---|---|
| Planning and shop-floor team | Tasks, actual conditions and frozen commitments | Trade-offs and execution arrangements |
| Data owner | Definitions, update frequency and quality checks | Whether data represents current facts |
| Consultant | Diagnosis, measures and comparison method | Business meaning and method |
| Software/integration partner | Adaptation, interface, execution and records | Interfaces, versions and exception handling |
| Toolkit integration owner | Selects and configures DecisioWorks data, orchestration, solving and analysis capabilities | Inputs, outputs, version requirements and scenario fit |
| Agent developer | Task organization, configuration assistance and explanation interfaces | Permitted actions and review points |

One team may hold several roles. Assign an owner and recipient to each deliverable and include the corresponding approvals in the agreed work plan.

## Build a Shared Language through a Baseline Comparison
The manufacturer specifies commitments to preserve and permitted changes. The consultant defines measures and comparison conditions. The integration partner connects inputs to the toolkit and keeps run records. Review results by object: what changed, why and whether the change is worth adopting.

For missing data, ask its owner to confirm the source. For an objective without a supported model measure, business and technical participants choose an appropriate representation. For overtime, the authorized operational owner decides. Assigning each question makes progress possible.

## Preserve Partner Expertise
Industry mappings, configuration templates, checklists and interpretation methods can become lasting partner assets. The available DecisioCore reference implementation offers calling patterns to study and extend. Partners can build industry applications and organize their shop-floor knowledge into rules and workflows.

As scope expands, participants can reuse shared concepts while checking each new case's data, responsibilities and capability fit. Open collaboration provides reusable foundations and room for professional expertise.

## Exercise and Review
Assign five deliverables: scenario brief, input mapping, comparison configuration, run record and result approval. Give each an owner, recipient and acceptance condition.

Where the answer says “joint responsibility,” identify who supplies facts, verifies transformation and approves execution. The record should tell the next participant what to receive, inspect and pass on.

## Further Reading

[Design Principles and Differentiation](https://github.com/qiaoyx-or/decisioworks/wiki/Design-Principles-and-Differentiation) · [Architecture Overview](https://github.com/qiaoyx-or/decisioworks/wiki/Architecture-Overview) · [Production Decision Data Assets](https://github.com/qiaoyx-or/decisioworks/wiki/Production-Decision-Data-Assets) · [Ecosystem Overview](https://github.com/qiaoyx-or/decisioworks/wiki/Ecosystem-Overview) · [Partner Onboarding and Integration](https://github.com/qiaoyx-or/decisioworks/wiki/Partner-Onboarding-and-Integration)

Worksheets: [Worksheet: Scenario and Decision Task](Worksheet-Scenario-Brief.md) · [Worksheet: Review and Change Record](Worksheet-Review-and-Change-Record.md)

[Topic F](Learning-Topic-F-Open-Collaboration-and-Evolution.md) · [Previous: Preserve Experience in Data Assets and Industry Templates](Learning-F2-Preserve-Data-Assets-and-Templates.md) · [Next: Read and Modify a Capability Orchestration Recipe](Learning-G1-Read-and-Modify-a-Recipe.md)
