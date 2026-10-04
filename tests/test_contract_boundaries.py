"""Contract regressions at the UI/import boundary; not independent ENG-04 QA."""
import copy
import json
import unittest
from pathlib import Path

from contracts.build_schemas import SCHEMAS, client_types
from services.data.contracts import DataError, validate


class ContractBoundaryTests(unittest.TestCase):
    def test_generated_types_and_schemas_match_the_structural_source(self):
        root = Path(__file__).resolve().parents[1] / "contracts/v1"
        self.assertEqual((root / "types.ts").read_text(), client_types())
        self.assertEqual({p.stem.removesuffix(".schema") for p in root.glob("*.schema.json")}, set(SCHEMAS))
        for name, expected in SCHEMAS.items():
            actual = json.loads((root / (name + ".schema.json")).read_text())
            actual.pop("$schema")
            actual.pop("title")
            self.assertEqual(actual, expected, name)

    def test_invalid_ui_metrics_cannot_validate(self):
        root = Path(__file__).resolve().parents[1] / "contracts/v1/examples"
        example = json.loads((root / "metrics-available.json").read_text())
        for field, value in [("value", 7127.78), ("value", "7127.780"), ("availability", "unavailable"), ("unit", "EUR")]:
            bad = copy.deepcopy(example)
            bad["metrics"][0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(DataError):
                validate("metrics.schema.json", bad)
        for field, value in [("contract_version", "1.0.0"), ("synthetic", False)]:
            bad = copy.deepcopy(example)
            bad[field] = value
            with self.subTest(field=field), self.assertRaises(DataError):
                validate("metrics.schema.json", bad)

    def test_queries_reject_calendar_errors_unknown_fields_and_unbounded_evidence(self):
        query = {"start_date": "2026-09-30", "end_date": "2026-09-30", "source": "upright_replica"}
        validate("metrics-query.schema.json", query)
        for change in ({"start_date": "2026-02-30"}, {"sql": "select *"}, {"limit": 1}, {"source": ""}):
            with self.subTest(change=change), self.assertRaises(DataError):
                validate("metrics-query.schema.json", {**query, **change})
        evidence = {**query, "run_id": "displayed-run", "offset": 0, "limit": 200}
        validate("evidence-query.schema.json", evidence)
        for change in ({"limit": 0}, {"limit": 201}, {"offset": -1}, {"limit": True}, {"run_id": ""}):
            with self.subTest(change=change), self.assertRaises(DataError):
                validate("evidence-query.schema.json", {**evidence, **change})
        with self.assertRaises(DataError):
            validate("evidence-query.schema.json", query)

    def test_write_envelopes_require_explicit_boolean_and_human_note(self):
        good = {"csv_text": "headers\r\n", "manifest": {}, "allow_corrections": False}
        validate("import-request.schema.json", good)
        for change in ({"allow_corrections": "false"}, {"allow_corrections": 1}, {"file_path": "/etc/passwd"}, {"manifest": []}):
            with self.subTest(change=change), self.assertRaises(DataError):
                validate("import-request.schema.json", {**good, **change})
        for note in ("", "  \n", None, 1):
            with self.subTest(note=note), self.assertRaises(DataError):
                validate("resolution-request.schema.json", {"resolution": note})
        validate("resolution-request.schema.json", {"resolution": "Reviewed original source; missing input remains unavailable."})

    def test_design_only_tools_cannot_request_sql_or_operational_actions(self):
        query = {"start_date": "2026-09-30", "end_date": "2026-09-30", "source": "upright_replica"}
        validate("tool-request.schema.json", {"tool": "get_metrics", "arguments": query})
        validate("tool-request.schema.json", {"tool": "get_evidence", "arguments": {**query, "run_id": "displayed-run"}})
        for tool in ("execute_sql", "rerun_browser", "post_accounting", "send_email"):
            with self.subTest(tool=tool), self.assertRaises(DataError):
                validate("tool-request.schema.json", {"tool": tool, "arguments": query})
