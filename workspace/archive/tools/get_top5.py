import json
from pathlib import Path

model_type = 'ridge'

# Load grid search metadata
gridsearch_file = Path(f'csiro-metadata/{model_type}/gridsearch_metadata.json')
with open(gridsearch_file, 'r') as f:
    gridsearch_data = json.load(f)

# Filter valid results and sort by cv_score descending
valid_results = [
    r for r in gridsearch_data
    if r.get('cv_score') is not None
    and not (isinstance(r.get('cv_score'), float) and (r['cv_score'] != r['cv_score']))
]

sorted_data = sorted(valid_results, key=lambda x: x.get('cv_score', -999), reverse=True)
top5 = sorted_data[:5]

print(f"Top 5 {model_type} Models by CV Score:")
print("=" * 80)
model_ids = []
for i, m in enumerate(top5, 1):
    model_id = m['model_id']
    model_ids.append(model_id)
    print(f"Rank {i} (by CV score):")
    print(f"  model_id: {model_id}")
    print(f"  variant_id: {m.get('variant_id', 'N/A')}")
    print(f"  feature_filename: {m['feature_filename']}")
    print(f"  cv_score: {m['cv_score']:.6f}")
    print()

print("=" * 80)
print("For Cell 2c, use model_id values directly:")
print(f"REGRESSION_MODEL_IDS = {model_ids}")
print()
print("These are model_id strings from gridsearch_metadata.json, NOT ranks or indices!")
