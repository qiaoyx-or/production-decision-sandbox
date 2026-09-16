# H1 Review a Plan from Run Status to Business Conclusion

[中文](Learning-H1-Review-a-Plan-zh-CN.md) · [Learning Center](Learning-Center.md)

## A Result Table Still Requires Judgment
A complete table may be historical input or output from a new run. A successful status may concern request handling alone. Before adopting a plan, review its status, conditions, results and commitments together.

Use the checklist to review execution, conditions, business results and adoption. Match each item to the fields exposed by the page or interface you use.

## Review Five Layers
| Layer | Check | Evidence |
|---|---|---|
| Run identity | Data, configuration, version and request | Run record and associated identity |
| Status | Usable candidates, selected plan and stopping reason | Status and errors |
| Conditions | Enabled constraints, hard/soft treatment and exceptions | Configuration and checks |
| Business results | Quantity, delivery, load and changes | Units and detailed rows |
| Adoption | Executability and approval of measures | Decision and follow-up record |

DecisioCore analysis explains results, while audit and execution records trace actions. Cross-check these against business facts instead of replacing review with one total score.

## Inspect Aggregates and Details
In a teaching observation, overall utilization is 60% but a bottleneck is overloaded in T-2. The aggregate does not disprove the local issue. Inspect load by resource and period, then trace tasks and material restrictions. Review at the granularity of the constraint.

Producing all quantities does not establish on-time delivery. Compare completion times with commitments separately. If a weighted objective is displayed as physical time, establish its definition and units before using it operationally.

## Describe Missing Results Accurately
| Observation | Description |
|---|---|
| Input validation fails | Identify the requirement and missing information |
| Authorization or runtime unavailable | The execution environment is not ready |
| Time exhausted without a candidate | No usable plan was found within this time limit |
| Infeasibility proved | The stated inputs and constraints are infeasible |
| Candidate fails checks | It cannot yet be adopted as a valid result |

Keep the current status and error for an unsuccessful run. If a historical plan is useful, show it separately with its run identifier and date. This preserves both diagnostic information and a reference for operational decisions.

## Confirm the Decision
Record what can be adopted, which conditions need changes and who owns them. Overtime, later delivery and material substitution need explicit approval status. After recalculation, preserve differences from the original and check whether the measure resolved the problem or introduced another cost.

## Exercise and Review
Extract five confirmed facts from an existing stamping or injection case and name three conclusions the record does not establish. For example, 120 output rows do not prove 120 orders, and quantity fulfillment does not prove on-time delivery.

A useful review separates observation, interpretation and decision and identifies the source of each fact.

## Further Reading

[Trusted Operation and Human Review](https://github.com/qiaoyx-or/decisioworks/wiki/Trusted-Operation-and-Human-Review) · [Runtime Status and Limits](https://github.com/qiaoyx-or/decisioworks/wiki/Runtime-Status-Errors-and-Limits-Reference) · [Web Cockpit Guide](https://github.com/qiaoyx-or/decisioworks/wiki/Web-Cockpit-Guide) · [Value Validation and Adoption](https://github.com/qiaoyx-or/decisioworks/wiki/Value-Validation-and-Adoption-Framework)

Worksheets: [Worksheet: Baseline and Adjusted Plan Comparison](Worksheet-Plan-Comparison.md) · [Worksheet: Review and Change Record](Worksheet-Review-and-Change-Record.md)

[Topic H](Learning-Topic-H-Build-Everyday-Decision-Capability.md) · [Previous: Write an AI Agent Task That Can Be Reviewed](Learning-G3-Write-an-Agent-Task.md) · [Next: Move from a Small Trial to Continued Operation](Learning-H2-Move-to-Continued-Operation.md)
