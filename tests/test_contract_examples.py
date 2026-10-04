import json
import unittest
from pathlib import Path

from services.data.contracts import validate


class ExampleContractTests(unittest.TestCase):
    def test_mock_examples_use_actual_response_schemas_and_states(self):
        root = Path(__file__).resolve().parents[1]/"contracts/v1/examples"
        paths = list(root.glob('*.json'))
        self.assertEqual(len(paths), 7)
        for path in paths:
            schema = path.stem.split('-')[0]
            validate(schema+'.schema.json', json.loads(path.read_text()))
        available = json.loads((root/'metrics-available.json').read_text())
        self.assertEqual(available['metrics'][0]['value'], '7127.78')
        self.assertEqual(available['metrics'][0]['availability'], 'available')
        unavailable = json.loads((root/'metrics-unavailable.json').read_text())
        self.assertIsNone(unavailable['metrics'][0]['value'])
        last_good = json.loads((root/'metrics-last-good.json').read_text())
        self.assertTrue(last_good['freshness']['is_last_good'])
        self.assertEqual(last_good['metrics'][0]['value'], '7127.78')
