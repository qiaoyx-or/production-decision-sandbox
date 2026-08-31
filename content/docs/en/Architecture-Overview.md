**English** | [简体中文](Architecture-Overview-zh-CN)

> Applies to DecisioWorks v1.4.0

# Architecture Overview

DecisioWorks uses `Scene × Business × Model × Solver` as its top-level logic and consists of four cooperating project layers. The layers explain responsibility; the runtime path explains how one decision cycle moves through the system. They should not be read as the same one-way pipeline.

1. **DataSets** stores industry scenarios and standardized data-interface instances. It answers how the business is represented accurately.
2. **GOCK** provides model construction and optimization. It answers how a plan is produced within explicit constraints and objectives.
3. **DecisioCore** connects data, objectives, rules, models, results, and feedback. It answers how a plan becomes part of a production decision.
4. **Web Cockpit** displays input, configuration, execution, output, and evidence. It makes capabilities visible and operable.

Documentation, tooling, containers, tests, and release governance support all four layers. Each layer can evolve independently while stable interfaces, analysis results, and feedback signals preserve linkage.

## Project layers are not runtime order

DataSets, GOCK, DecisioCore, and Web Cockpit describe responsibilities. A typical run is closer to:

```text
DataSets
   ↓ business objects and structural constraints
DecisioCore: validation, objectives, rules, and standard actions
   ↓ model configuration and controlled parameters
GOCK: model construction and optimization
   ↓ planning result and runtime state
DecisioCore: analysis, explanation, deviation, and feedback
   ↓
Web Cockpit / API / next planning cycle
```

DecisioCore participates before and after solving. Before solving, it organizes model input; after solving, it breaks planning output into business metrics, object-level details, and input to the next decision cycle.

## Why the architecture is layered

Manufacturing scenarios change continuously, but different changes belong in different places. Fields and relationships belong to the data layer. Management preferences belong to objective governance. Shop-floor experience belongs to rule control. Process changes belong to orchestration. Model upgrades belong to the solving layer. Layering keeps each change in its responsible location while preserving linkage through stable interfaces.

## Top-level logic: Scene × Business × Model × Solver

- **Scene** defines the industry context, data scope, and business boundary.
- **Business** expresses orders, routes, capacity, materials, objectives, and rules.
- **Model** converts business facts into a solvable structure.
- **Solver** executes computation within controlled parameters and authorization scope.

The four project layers jointly implement this logic. DataSets provides scenarios and templates, DecisioCore organizes the production-decision chain, GOCK provides modeling and optimization, and Web supports operation, presentation, and validation.

Continue with [Component Responsibilities](Component-Responsibilities) and [Standard Actions and Orchestration](Standard-Actions-and-Orchestration).
