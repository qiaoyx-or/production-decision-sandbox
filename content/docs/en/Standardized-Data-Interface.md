**English** | [中文](Standardized-Data-Interface-zh-CN)

> Applies to DecisioWorks v1.4.0

# Standardized Data Interface

A standardized data interface does more than align fields: it turns business facts into computable structures.

## Core objects

Orders, products, routes, operations, work centers, capacity, calendars, shifts, maintenance, materials, operation-level BOM, inventory, kitting information, and planning results are connected through explicit keys, time coordinates, and relationships.

## Four relationship chains

1. Time: delivery, capacity, kitting, and results share one planning coordinate.
2. Product: orders, routes, inventory, and properties refer to consistent products.
3. Process and capacity: products traverse routes and operations to resources with valid capacity and calendars.
4. Material and kitting: material conditions bind to operations and planning levels.

The scenario `data.db` is a testable interface template. Complete fields are only the beginning; closed relationships, consistent semantics, and active structural constraints determine solver readiness.

## Design principle: complete fields are only the beginning

The hard part of APS data onboarding is not importing tables. It is proving that time, product, process-capacity, and material-readiness relationships close correctly. Data enters production decisions only when objects, relationships, units, and constraint semantics agree.

## Typical uses

- without ERP or MES, use `data.db` as a standard interface template to organize a scenario quickly;
- with ERP or MES, map source data into shared business semantics and reduce integration friction;
- represent shifts, maintenance, shared resources, lot sizes, yield, and operation-level BOM;
- provide common inputs for master planning, scheduling, material readiness, and AI Agent onboarding.

## Differentiation

Many interfaces stop when fields can be transferred. DecisioWorks distinguishes readable structure, closed business relationships, and solver readiness. The interface is therefore both a data entry point and the first stage of business modeling and constraint construction.
