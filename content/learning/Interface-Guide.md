# Learning the Standardized Data Interface

[中文](Interface-Guide-zh-CN.md)

[Download the complete exercise pack (SQL, field list, Python scripts, database and CSV files)](../../assets/data-interface/decisioworks-data-interface-examples.zip)

A production model needs to know what to make, how it can be made, which resources it uses, when materials become available, and how much work each period permits. The DecisioWorks standardized data interface organizes these facts as connected business objects.

This course provides a complete semantic guide, nine task-based lessons, and field, relationship, template, and code references. Begin with the system map; use the lessons to build a configuration; consult the field reference for exact storage requirements.

## The Semantic Guide

[DecisioWorks Standardized Data Interface: A Detailed Semantic Guide](Interface-Semantics.md) covers objects, field meanings, time and quantity rules, relationships, and result updates.

## Learn Through Tasks

| Lesson | What you will produce |
|---|---|
| [01 Configure time, shifts, and maintenance](Interface-01-Calendar.md) | Time records, resource occupancy, and an available-time calculation |
| [02 Express orders, products, and attributes](Interface-02-Demand.md) | Staged order deliveries and a product-attribute mapping |
| [03 Configure work centers and shared resources](Interface-03-Resources.md) | Resource hierarchy, sharing relationships, and availability records |
| [04 Configure routes and alternative resources](Interface-04-Routing.md) | Operation precedence, route options, and resource mappings |
| [05 Calculate cycle output, batches, and processing time](Interface-05-Quantity.md) | Quantity conversions, batch checks, and joint-output calculations |
| [06 Configure operation-level materials and availability](Interface-06-Materials.md) | Material requirements, time-phased supply, and a manual feasibility check |
| [07 Translate inventory requirements into cumulative bounds](Interface-07-Inventory.md) | Bounds derived from an inventory balance |
| [08 Import, validate, and load business data](Interface-08-Validation.md) | A mapping sheet, a separate teaching database, and validation results |
| [09 Interpret results and prepare the next planning cycle](Interface-09-Results.md) | Output, time, material checks, and an update checklist |

## References and Practice

- [Complete field reference](Interface-Fields.md): 18 tables and 105 fields in the current standard template, separating business meaning from storage requirements.
- [Relationship and rule reference](Interface-Relationships.md): foreign keys, cardinalities, calculations, and distinctions between similarly named fields.
- [Configuration patterns](Interface-Configurations.md): shifts, continuous production, maintenance, sharing, inventory, and quantity conventions.
- [End-to-end exercise and commands](Interface-Walkthrough.md): a 120-unit requirement, configuration checks, a manually constructed candidate plan, and a maintenance change.

The quantities, resources, and periods in the exercises are teaching data. The supplied program builds a separate database and runs structural checks and manual calculations. Candidate rows are explicitly labeled as manually constructed; solver results must come from an actual run. This separates learning how data is expressed from testing how a model uses it.

For production configuration, use the field definitions and capability documentation that accompany your installed version. The extensible attribute mechanism is not limited to three dimensions; this SQLite template implements three attribute tables.
