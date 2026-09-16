# G1 Read and Modify a Capability Orchestration Recipe

[中文](Learning-G1-Read-and-Modify-a-Recipe-zh-CN.md) · [Learning Center](Learning-Center.md)

## Use a Recipe to Describe a Scenario Run
A capability orchestration recipe records capabilities, action order, configuration and expected outputs. It connects business intent with standard actions so pages, scripts and Agents can use the same process.

Read the v1.4.0 production_planning.yaml example. Actual solving requires compatible runtime components, dependencies and authorization. Parameters must also remain within the active limits.

## Read Five Parts
| Part | Find in the example |
|---|---|
| register | Data-acquisition and production registration functions |
| pipeline | Acquisition, constraint parsing, generation, selection, evaluation and output |
| context.inputs | Source, engine type and planning configuration |
| expected_outputs | Best solution, analysis and objective checks |
| safety | Database writes disabled; results use separate files |

If both data_acquisition and production specify a source, keep them consistent when changing datasets. Relative paths follow the project's recipe-loader rules.

## Interpret a Configuration Excerpt
This excerpt shows the constraints and objectives. For execution, use the complete `production_planning.yaml`, including data sources, registration and action order.

```yaml
planning:
  constraints:
    enable_capacity_cons: true
    capacity_soft: true
    enable_demand_cons: true
    demand_cons_mode: 3
    enable_kitting_cons: true
    enable_inventory_cons: false
    CSP: false
  objective:
    job_bias: -0.001
    waittime: 1.0
```

capacity_soft makes capacity a soft condition, while enable_kitting_cons controls material-availability constraints. Use the field definitions for the installed recipe and interface version. Interpret enumerations such as demand_cons_mode using current documentation and parsing behavior, not the number alone.

The recipe uses `initial_objective_overrides` to set the initial `waittime` to zero. Its `objective_candidate_bridge` maps delivery or completion-time intent to an accumulated-waiting objective. This bridge connects a business intent to a measure the model can calculate. Trace initial settings, objective updates and the final audit to see the values actually used; the `objective` block alone does not describe every stage.

## Make One Change
Copy the recipe and record its version and source. Change one supported objective parameter while preserving other conditions. For waittime, first identify where initial overrides and the objective bridge update it, then choose a supported adjustment point. Check the effective configuration after execution. If a later stage overwrites the intended value, revise the comparison design first. Execute through the existing loader and runner, then inspect action history, the selected solution, production_analysis and errors. Use supported independent-output parameters when persistence is needed.

`expected_outputs` lists expected outcomes. Check status and results against each item after execution, or encode the conditions as test assertions. To save JSON results, configure a supported independent output location. Otherwise, check whether the output action was skipped and record that status.

## Exercise and Review
Mark source data, business conditions, objectives and computing limits separately. Identify one proposed change and its check.

Loading, registration, execution and verified output are distinct checkpoints. Use the recipe's script entry point to load and run it. In demonstration pages, use the actions and parameters the page exposes. For workflows with branches or dependencies, consult the corresponding DecisioCore execution interfaces.

## Further Reading

[Standard Actions and Orchestration](https://github.com/qiaoyx-or/decisioworks/wiki/Standard-Actions-and-Orchestration) · [Actions, Recipes and Execution](https://github.com/qiaoyx-or/decisioworks/wiki/Actions-Recipes-and-Execution-Reference) · [Developer Guides](https://github.com/qiaoyx-or/decisioworks/wiki/Developer-Guide-Index) · [Runtime Status and Limits](https://github.com/qiaoyx-or/decisioworks/wiki/Runtime-Status-Errors-and-Limits-Reference)

Worksheets: [Worksheet: Scenario and Decision Task](Worksheet-Scenario-Brief.md) · [Worksheet: Operational Rule and Verification](Worksheet-Operational-Rule.md)

[Topic G](Learning-Topic-G-Actions-Extensions-and-Agents.md) · [Previous: Define Roles for Manufacturers, Consultants and Software Partners](Learning-F3-Define-Ecosystem-Responsibilities.md) · [Next: Extend a Capability with a Clear Calling Interface](Learning-G2-Extend-a-Capability.md)
