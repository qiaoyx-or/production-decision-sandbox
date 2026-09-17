**English** | [中文](Planning-and-Scheduling-Overview-zh-CN)

> Applies to DecisioWorks v1.4.0

# Planning and scheduling: keeping two decision levels aligned

Master planning and detailed scheduling solve different problems. Planning decides what to produce, how much, and when work may be released. Scheduling assigns released, executable work to resources, sequence, and time. Combining everything in one model often makes the plan too detailed and pushes material or management conflicts into the scheduler.

## What master planning owns

Master planning brings together demand, capacity, material availability, inventory, delivery commitments, and execution feedback. It does not seek second-by-second precision for every operation. It identifies underproduction, overload, kitting risk, inventory pressure, and commitment risk, then decides what may be released and what needs to wait, be adjusted, or be escalated.

DecisioWorks can represent these changes as PlanBias records. A bias preserves source, affected object, direction, and impact before anyone overwrites the active plan.

## What detailed scheduling owns

Scheduling receives released, confirmed work packages that meet the material conditions required for that release. Within a local production unit it handles resource assignment, sequence, waiting, idle time, and changeovers. Upstream planning confirms material readiness; if a scheduling capability also supports time-phased material constraints, enable them explicitly. Precise scheduling depends on stable input, while long-term forecasting, procurement commitments, and cross-department coordination belong to the corresponding planning processes.

## Linkage flow

```text
demand, capacity, material, and execution changes
  -> PlanBias -> PlanSignal
  -> objective/rule candidates or release policy
  -> scheduling work package
  -> workload, waiting, changeover, and execution feedback
  -> next planning cycle
```

A PlanSignal routes a planning impact to a receiving action, which may propose an objective change, a local rule, or a release candidate, or retain an alert. Configuration and approval determine whether the proposal enters a later run. Creating a signal does not itself change the plan.

## Freeze, continue, or reconstruct

Disturbance response should not default to global rescheduling. Near-term prepared work may be frozen, still-valid work continued, and only the affected scope reconstructed. Compare solution gain with change scope, shop-floor switching cost, and commitment impact.

## Observe it in the Web cockpit

These steps use an installed DecisioWorks Web Cockpit with the required license configuration. This website provides documentation and historical case records; its sandbox illustrates the workflow.

1. Inspect demand, capacity, kitting, and time units.
2. Run a baseline and review satisfaction, workload, waiting, and shortage.
3. Change an objective or solver parameter supported by the page and rerun. For rule or resource changes, update the corresponding data or recipe and reload it first.
4. Compare what remained stable, what changed, and why.
5. Record cross-cycle issues as inputs to the next planning round.

## Common mistakes

- Treating MPS as a coarse Gantt chart.
- Leaving material shortages and procurement conflicts entirely to the scheduler.
- Overwriting the original plan after an exception without explaining the change.
- Comparing only objective scores rather than plan stability and execution costs.

Continue with the [Stamping Planning Case](Stamping-Planning-Case-Walkthrough) and [Results, Evidence, and Feedback](Results-Evidence-and-Feedback).
