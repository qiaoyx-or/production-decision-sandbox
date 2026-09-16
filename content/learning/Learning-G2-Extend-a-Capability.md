# G2 Extend a Capability with a Clear Calling Interface

[中文](Learning-G2-Extend-a-Capability-zh-CN.md) · [Learning Center](Learning-Center.md)

## Choose What You Are Extending
A summary by order category usually belongs in analysis. A new constraint accepted by a solver may involve constraint handling or engine adaptation. Decide whether the change concerns data, rules, objectives, analysis or the engine before choosing its entry point.

The development exercise adds a result-review summary using existing analysis and order categories. Start by defining the extension's inputs, outputs and checks.

## Define Inputs and Outputs
| Item | Definition |
|---|---|
| Inputs | Results, order-category mapping and metric definitions |
| Outputs | Category totals, unmatched records and measurement basis |
| Result location | A separate key under ctx.derived, without overwriting other analysis |
| Failure | Missing required mapping or unresolved units |
| Skip | The application explicitly disables optional summarization |
| Side effects | No source-data or selected-solution mutation |

First check whether results can be linked to orders. If output is aggregated by product, operation or period and several orders share a product, an explicit allocation is needed. Without it, keep the original granularity and report records that cannot be attributed to orders. Read fields from the actual object structure and list unclassified orders separately so category totals can be reconciled with the overall amount.

## Use the Standard Extension Pattern
A handler is the function performing the business logic. Its ctx argument holds this execution's inputs, intermediate results and state. The developer guide supports handler(ctx) or handler(ctx, params), returning DecisionContext or ActionResult. CapabilityRegistry associates a handler with an appropriate standard action, and execution records its invocation and result.

Entries have versions, priorities and enabled states. Default resolution selects the enabled implementation with the highest priority. Raising priority can therefore replace an existing action implementation rather than append a step. Inspect action semantics and selection. To preserve existing evaluation, use an appropriate composition or separate invocation supported by the project.

## Keep Registration, Discovery and Recipes Aligned
1. Provide a lightweight registration function without loading business data or starting a solve at import time.
2. Match handler inputs and outputs to the action.
3. Update the capability description and applicability.
4. Provide a minimal recipe or calling example.
5. Check registration, resolution, invocation, errors and results.

Singletons suit thread-safe services without per-request state. Keep solve objects and customer data in request contexts so tasks remain isolated.

## Test Normal and Error Cases
| Input | Expected behavior |
|---|---|
| Complete categories and units | Category totals match the overall amount |
| Unknown categories | Report them or fail according to the definition |
| Required results missing | Structured failure |
| Optional feature disabled | Explicit skip |
| Two different requests | Independent outputs |

If upstream processing provides no valid result, return the appropriate error or skip status. Summarize only data from the current run, and preserve the existing structured handling of authorization and input errors.

## Exercise and Review
Produce the extension description, input/output table, registration strategy and five checks. Explain the action choice and how existing analysis continues to run.

Completion requires the intended handler to be selected, correct measures, understandable errors and consistent existing behavior. Successful import alone does not establish a working extension.

## Further Reading

[Standard Actions and Orchestration](https://github.com/qiaoyx-or/decisioworks/wiki/Standard-Actions-and-Orchestration) · [Actions, Recipes and Execution](https://github.com/qiaoyx-or/decisioworks/wiki/Actions-Recipes-and-Execution-Reference) · [Developer Guides](https://github.com/qiaoyx-or/decisioworks/wiki/Developer-Guide-Index) · [Runtime Status and Limits](https://github.com/qiaoyx-or/decisioworks/wiki/Runtime-Status-Errors-and-Limits-Reference)

Worksheets: [Worksheet: Scenario and Decision Task](Worksheet-Scenario-Brief.md) · [Worksheet: Operational Rule and Verification](Worksheet-Operational-Rule.md)

[Topic G](Learning-Topic-G-Actions-Extensions-and-Agents.md) · [Previous: Read and Modify a Capability Orchestration Recipe](Learning-G1-Read-and-Modify-a-Recipe.md) · [Next: Write an AI Agent Task That Can Be Reviewed](Learning-G3-Write-an-Agent-Task.md)
