"""Run from a DecisioWorks root with its dependencies already installed."""
import argparse
import json
import sys
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('database')
parser.add_argument('--project-root', default=str(Path.cwd()))
args = parser.parse_args()
root = Path(args.project_root).resolve()
if not (root / 'DecisioCore/data_layer/repository.py').is_file():
    raise SystemExit('Use --project-root to select a DecisioWorks directory.')
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / 'DecisioCore'))
from data_layer.repository import load_business_data
from data_layer.preprocessing.pipeline import run_preprocessing_pipeline

data = load_business_data(str(Path(args.database).resolve()), source_type='sqlite')
data, report = run_preprocessing_pipeline(data, {
    'enabled': True,
    'handlers': ['validate_batch_productivity_multiple'],
    'failure_policy': 'error',
})
counts = {key: len(getattr(data, key)) for key in ('demand', 'process', 'capacity', 'bom', 'kitting', 'inventory_limit')}
print(json.dumps({'data_layer_loaded': True, 'preprocessing': report, 'loaded_rows': counts,
                  'solver_executed': False}, indent=2))
