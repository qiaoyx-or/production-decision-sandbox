# 08 Import, Validate, and Load Business Data

[中文](Interface-08-Validation-zh-CN.md) · [Learning guide](Interface-Guide.md) · [Semantic guide](Interface-Semantics.md)

## Task: Create an Explainable Data Copy

Write the base scenario from the first seven lessons into a separate teaching database, validate its structure and values, and load it through the project data layer. Shared fixtures and alternative machines remain extension exercises rather than implicit base conditions.

## Map the Source First

| Source | Business meaning | Target field | Conversion | Check |
|---|---|---|---|---|
| P-1 on order O-100 | Demanded product | order_item.product | Map P-1 to id=1 | Product exists |
| 80 due on day one | Period delivery requirement | delivery_time/number | Time 1, quantity 80 | Unit is pieces |
| Two maintenance hours | Unavailable share of an eight-hour period | capacity.used | 2÷8=0.25 | Deduct once |
| Four units per ten-minute cycle | Per-cycle parameters | productivity/processing_time | 4 and 600 seconds | Batch 20 is divisible |
| 160 fasteners initially ready | Opening available supply | kitting_information.number | 160 | Separate later increments |

Retain the basis for each conversion, not just column names. A numeric 120 might mean minutes, pieces, or a percentage; a type check alone cannot decide.

## Build and Check

From the supplied `examples` directory:

```bash
python build_example.py --output-dir ./output
python check_example.py ./output/data.db
python test_examples.py
```

The builder refuses to overwrite an existing target database. Use a new output directory for another attempt. The schema comes from the current standard template and contains no customer records. See the [walkthrough](Interface-Walkthrough.md) for generated files and outputs.

Validation starts with tables, field types, primary keys, nullability, and foreign-key declarations. It then checks stored values, referenced objects, time status, occupied fractions, batch divisibility, OEE, the resource hierarchy, operation numbering, and inventory bounds. A readable table can still lack a foreign-key declaration, leaving the database unable to detect invalid references; retain the template's relationship constraints. Quantity and batch columns in this teaching template are integers. Floating-point values must be finite, booleans must be 0 or 1, and OEE uses percentages from 0 to 100. A type error identifies the object, field, and row ID before arithmetic checks are attempted. Missing files and damaged databases produce an error message and a nonzero exit status.

This exercise requires a due period for each delivery demand, a resource for each capacity record, and both an operation and a work center for each adaptor. Result or shared-resource records, when present, also need their associated objects. These exercise-specific requirements do not change the standard schema's nullable fields. Optional inventory bounds, unused attribute slots, and the root work center's parent can remain null.

The output lists executed checks in `checks_performed`, checks blocked by earlier errors in `checks_skipped`, and responsibilities outside this validator in `not_checked`. An `ok: true` result means the listed input checks passed. Demand coverage, full scheduling feasibility, advanced scenario rules, and model solving require separate validation. Negative tests cover invalid stored types, fractional batches, out-of-range values, missing references, and hierarchy cycles.

## Use the Real Project Entry Point

With DecisioWorks dependencies installed, run the companion script from the project root:

```bash
python /path/to/examples/load_with_decisioworks.py /path/to/output/data.db
```

It uses these actual APIs; replace `/path/to` with the real location:

```python
import sys
from pathlib import Path

root = Path.cwd()  # Run from the DecisioWorks project root.
sys.path.insert(0, str(root / "DecisioCore"))
from data_layer.repository import load_business_data
from data_layer.preprocessing.pipeline import run_preprocessing_pipeline

data = load_business_data("/path/to/output/data.db", source_type="sqlite")
data, report = run_preprocessing_pipeline(data, {
    "enabled": True,
    "handlers": ["validate_batch_productivity_multiple"],
    "failure_policy": "error",
})
print(report)
```

Inspect loaded objects and row counts, then select a planning model suited to the scenario. Record the actual capacity, routing, material, inventory, objective, and runtime configuration used in a solve. Complete tables do not substitute for that configuration.

## Exercise and Answer

In a copy, change `used` to 25: the fraction check should reject it. Change a due-period reference to 99: expect a reference error. Change batch size 20 to 18 while retaining output four: expect a divisibility error. Test one change at a time, keeping the correct original. Diagnostics should identify the object and row so that correction returns to the business source.

[Previous](Interface-07-Inventory.md) · [Next: results and updates](Interface-09-Results.md)
