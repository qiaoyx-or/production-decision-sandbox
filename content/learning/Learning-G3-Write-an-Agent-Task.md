# G3 Write an AI Agent Task That Can Be Reviewed

[中文](Learning-G3-Write-an-Agent-Task-zh-CN.md) · [Learning Center](Learning-Center.md)

## Turn Intent into a Defined Task
“Optimize my schedule” omits data, permitted actions and evaluation criteria. A reviewable Agent task identifies the sample, allowed changes, required outputs and human confirmation points.

Use the standard injection sample in two stages. First prepare a configuration diff that changes only the `color` weight, together with pre-run checks. After approval, an authorized runtime executes the comparison. Save configuration proposals separately from run results.

## Example Task Definition
| Item | Content |
|---|---|
| Task | Compare one color-weight change with the same data and constraints |
| Inputs | Confirmed production_scheduling version and field definitions |
| May change | The color weight, with its value specified by the requester |
| Keep fixed | capacity weight, work center, 40×3 structure, constraints and data |
| Resource limits | Read from the runtime being used |
| Stage 1 output | Configuration diff and pre-run checks, clearly marked as not yet run |
| Stage 2 output | Actual run status, result comparison and interpretation |
| Human review | Before execution and before operational adoption |

Keep authorization files in the execution environment; the task package only needs information for preparing the configuration. Confirm what data may be shared before using an external Agent service.

## Ask Specific Questions
Have the Agent explain which business attribute color maps to, what capacity means in this recipe, which records prove execution, how to compare different weights, and how to describe the absence of a usable plan.

These questions encourage use of the structured inputs rather than assumptions from general scheduling knowledge. If capacity is interpreted as machine availability, correct the interpretation and configuration before continuing.

## Distinguish Three Outputs
| Type | Label and review |
|---|---|
| Configuration proposal | Not executed; inspect parameters and differences |
| Execution request | Record recipient, input version and computing limits |
| Run result | Actual status, actions and result evidence |

Match the request to its run identifier, then inspect candidates, the selected solution and the source of each measure. Trace the result explanation to the actual configuration and output records.

Where a workbench supports task-package export, pass the task, context, expected results and permitted actions to the chosen Agent. A user or configured integration then invokes it and reviews the response. Export prepares the information; invocation is a separate step.

## A Task Prompt to Adapt
This is a natural-language task for an Agent, not an executable API request. The requester supplies the bracketed values. Resolve missing values before proceeding.

```text
Task: Prepare an injection-scheduling comparison that changes only the
color objective weight. Do not start solving yet.
Inputs: data version [supply]; production_scheduling recipe version [supply];
field definitions [provide]; active runtime parameter limits [provide].
Change: color from [baseline value] to [requested value].
Keep fixed: data, constraints, capacity weight, work center, sequence length,
cycle count, thread count and time limit.
Check: in this sample, color maps to property_1; the capacity objective
relates to container volume in property_3, not machine capacity.
Return: baseline/proposed configuration diff, parameter checks, missing
information and questions requiring confirmation.
Pause if a field is unknown, a limit is exceeded or a fixed item must change.
After approval, the prepared runtime runs baseline and adjusted configurations.
Only then report actual status, sequences, both change counts and objective measures.
```

For a reading check, reject a proposal that also changes the capacity weight. Flag a missing requested color value for confirmation. If all checks pass, the configuration can go to the person responsible for execution. None of those statuses establishes an improved result before the runs occur.

## Exercise and Review
Write a task and two rejection conditions: a request outside permitted parameter limits, and an attempt to change unauthorized data or fields. Add a normal acceptance condition: only the specified weight changes and all fixed items remain consistent.

Submit the task, configuration diff, checks and status explanation. The Agent helps organize work; enterprise users use the evidence to decide whether the configuration and plan can be adopted.

## Further Reading

[Standard Actions and Orchestration](https://github.com/qiaoyx-or/decisioworks/wiki/Standard-Actions-and-Orchestration) · [Actions, Recipes and Execution](https://github.com/qiaoyx-or/decisioworks/wiki/Actions-Recipes-and-Execution-Reference) · [Developer Guides](https://github.com/qiaoyx-or/decisioworks/wiki/Developer-Guide-Index) · [Runtime Status and Limits](https://github.com/qiaoyx-or/decisioworks/wiki/Runtime-Status-Errors-and-Limits-Reference)

Worksheets: [Worksheet: Scenario and Decision Task](Worksheet-Scenario-Brief.md) · [Worksheet: Operational Rule and Verification](Worksheet-Operational-Rule.md)

[Topic G](Learning-Topic-G-Actions-Extensions-and-Agents.md) · [Previous: Extend a Capability with a Clear Calling Interface](Learning-G2-Extend-a-Capability.md) · [Next: Review a Plan from Run Status to Business Conclusion](Learning-H1-Review-a-Plan.md)
