"""Local lab bridge into the existing verified intake/import/metrics pipeline."""
import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from acquisition.intake import intake, submit
from services.data.importer import Pipeline
from services.metrics.query import metric_response, evidence_response

request = json.load(sys.stdin)
result = request['result']
if result.get('ok') is not True:
    raise ValueError('Only verified acquisition results can be imported')
root = Path(request['state_root'])
manifest = result['manifest']
record = intake(result['file'], manifest, str(uuid.uuid4()),
                manifest['requested_start_date'], manifest['requested_end_date'],
                'upright_replica', 'paid_orders', root / 'acquired')
pipeline = Pipeline(root)
batch, _ = submit(record, pipeline)
metrics = metric_response(pipeline, manifest['requested_start_date'],
                          manifest['requested_end_date'], 'upright_replica')
evidence = evidence_response(pipeline, metrics['metric_run_id'],
                            manifest['requested_start_date'], manifest['requested_end_date'],
                            'upright_replica', limit=5) if metrics.get('metric_run_id') else None
print(json.dumps({'batch': batch, 'metrics': metrics, 'evidence': evidence}))
