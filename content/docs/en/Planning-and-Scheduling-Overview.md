**English** | [中文](Planning-and-Scheduling-Overview-zh-CN)

> Applies to DecisioWorks v1.4.0

# Planning and scheduling: keeping two decision levels aligned

Master planning and detailed scheduling solve different problems. Planning decides what to produce, how much, and when work may be released. Scheduling assigns released, executable work to resources, sequence, and time. Combining everything in one model often makes the plan too detailed and pushes material or management conflicts into the scheduler.

## What master planning owns

Master planning brings together demand, capacity, material availability, inventory, delivery commitments, and execution feedback. It identifies underproduction, overload, kitting risk, inventory pressure, and commitment risk, then decides what may be released and what requires review.

DecisioWorks can represent these changes as PlanBias records. A bias preserves source, affected object, direction, and impact before anyone overwrites the active plan.

## What detailed scheduling owns

Scheduling receives released, confirmed, materially ready work packages. Within a local production unit it handles resource assignment, sequence, waiting, idle time, and changeovers. Precise scheduling depends on stable input and should not absorb long-term forecasting, procurement commitments, or cross-department negotiation.

## Linkage flow

```text
demand, capacity, material, and execution changes
  -> PlanBias -> PlanSignal
  -> objective/rule candidates or release policy
  -> scheduling work package
  -> workload, waiting, changeover, and execution feedback
  -> next planning cycle
```

A PlanSignal can adjust an objective, create a local rule, influence release, or remain an alert. Change therefore enters the decision process before it modifies the plan.

## Freeze, continue, or reconstruct

Disturbance response should not default to global rescheduling. Near-term prepared work may be frozen, still-valid work continued, and only the affected scope reconstructed. Compare solution gain with change scope, shop-floor switching cost, and commitment impact.

## Observe it in the Web cockpit

1. Inspect demand, capacity, kitting, and time units.
2. Run a baseline and review satisfaction, workload, waiting, and shortage.
3. Change one objective, rule, or resource condition and rerun.
4. Compare what remained stable, what changed, and why.
5. Record cross-cycle issues as inputs to the next planning round.

Common mistakes include treating MPS as a coarse Gantt chart, leaving procurement conflicts to scheduling, overwriting plans without an explanation, and comparing scores without considering execution stability.
