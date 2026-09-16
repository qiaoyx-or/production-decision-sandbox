# E3 Define the Scope of a Disruption Response

[中文](Learning-E3-Scope-a-Disruption-Response-zh-CN.md) · [Learning Center](Learning-Center.md)

## Faster Recalculation Still Needs an Appropriate Scope
After a machine problem, recalculating the entire plan may change tasks with materials prepared, tooling installed or instructions already issued. Alongside computation time, consider the cost of changing execution.

This discussion exercise assumes WC-1 will stop in the afternoon. J1 has started, J2 has materials and tooling confirmed, and J3 is unreleased. Actual freezing and transfer mechanisms depend on the application and model.

## Classify the Work
| Category | Basis | Information to retain |
|---|---|---|
| Freeze | Already executing or expensive to change, where conditions permit | Fixed objects, periods, resources or sequence scope |
| Retain | The existing arrangement remains valid | Original version and conditions supporting it |
| Recalculate | Affected work requires adjustment | Permitted changes, resources, objectives and constraints |

Freezing does not override a physical outage. If started work cannot continue, confirm safe handling and actual shop-floor state before updating inputs. Keeping a plan unchanged cannot restore an unavailable machine.

## Map the Impact
Find tasks overlapping the outage, then follow operation dependencies, shared resources, material allocations and delivery commitments. The effect may extend beyond WC-1 or remain limited to a few unreleased tasks. Record the relationships that justify the recalculation scope.

## Design Two Candidate Responses
Response L retains confirmed work where possible and reschedules affected unreleased tasks. Response W permits broader changes. Compare delivery and output together with changed-task counts, setup preparation, resource coordination and new risks.

Participants first confirm the outage and affected work, then use supported data, rule and planning-linkage interfaces to prepare the two configurations. This exercise uses manual identification and confirmed recalculation; it does not include automatic disruption detection or fully automated reconstruction.

## Explain the Choice
If L meets key commitments with little operational change, it may fit the circumstances. If it cannot accommodate the affected work, broader adjustment may be necessary. Base the choice on constraints, feasibility and implementation cost rather than assuming local changes are always superior.

## Exercise and Review
“Started,” “materials ready” and “unreleased” do not uniquely determine a response. Establish how each task relates to the outage window first.

The following classroom conditions and proposed responses provide a worked example for discussion and review.

| Task | Added condition | Proposed treatment | What would change the decision? |
|---|---|---|---|
| J1 | Expected to finish before the afternoon outage; operations confirms it can continue as planned | Retain the arrangement and track completion | Progress slips into the outage window, requiring a new operational decision |
| J2 | Planned on WC-1 during the outage, with no approved alternative | Hold that arrangement and check recovery time and due date before recalculating | An alternative resource is approved, or the outage window changes |
| J3 | Uses independent WC-2; its materials and tooling are unaffected | Retain the plan and follow the original release checks | A shared tool, predecessor or material allocation proves affected |

Without recovery time, remaining processing and alternative-resource information, list the questions to resolve rather than assigning an unsupported completion time.

Extend the table with affected objects, fixed and adjustable conditions, comparison measures and approvers. After an actual recalculation, check that commitments are preserved and task changes have reasons. Update conditions that no longer hold instead of mechanically retaining the original arrangement.

## Further Reading

[Planning and Scheduling](https://github.com/qiaoyx-or/decisioworks/wiki/Planning-and-Scheduling-Overview) · [Results and Feedback](https://github.com/qiaoyx-or/decisioworks/wiki/Results-Evidence-and-Feedback) · [Component Responsibilities](https://github.com/qiaoyx-or/decisioworks/wiki/Component-Responsibilities)

Worksheets: [Worksheet: Operational Rule and Verification](Worksheet-Operational-Rule.md) · [Worksheet: Review and Change Record](Worksheet-Review-and-Change-Record.md)

[Topic E](Learning-Topic-E-Coordinate-Plans-and-Responses.md) · [Previous: Express Changes as Plan Deviations and Signals](Learning-E2-Deviations-to-Planning-Signals.md) · [Next: Locate the Layer That Should Handle a Change](Learning-F1-Place-Changes-in-the-Right-Layer.md)
