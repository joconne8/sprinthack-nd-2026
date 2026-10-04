"""Mutation evidence: each seeded defect must make an independent ledger check fail.

Defects are injected with unittest.mock only for the duration of one test; no
implementation file is edited. A defect that passes the checks is a QA gap.
"""
import tempfile
import unittest
from unittest import mock
from uuid import uuid4

import services.data.importer as importer
from services.data.contracts import cents
from services.data.importer import Pipeline
from tests.acceptance.test_independent_ledger import check_buyer_store_keys, check_core_ledger, check_coverage_gap

REAL_NORMALIZE = importer.normalize


def defective_normalize(change):
    def wrapper(row, *args, **kwargs):
        record = REAL_NORMALIZE(row, *args, **kwargs)
        change(record, row)
        return record
    return wrapper


def ignore_refunds(record, row):
    record["refund_cents"] = 0


def include_shipping_tax_fees(record, row):
    record["gross_cents"] += sum(cents(row[k]) for k in ("shipping_collected", "sales_tax", "marketplace_fee"))


def use_source_net_field(record, row):
    record["gross_cents"], record["refund_cents"] = cents(row["net_sales"]), 0


def unstable_business_key(record, row):
    # Duplicate-count defect: identity includes a per-import nonce, so re-sent rows count again.
    record["record_key"] += "#" + uuid4().hex


def ignore_store_identity(record, row):
    record["warnings"] = [w for w in record["warnings"] if w not in ("missing_store", "unmapped_store")]
    record["store_id"] = record["store_id"] or "GW-001"


def always_complete(windows, start, end):
    from datetime import date, timedelta
    days, cursor = [], date.fromisoformat(start)
    while cursor <= date.fromisoformat(end):
        days.append(str(cursor))
        cursor += timedelta(days=1)
    return {"expected_days": days, "complete_days": days, "missing_or_partial_days": [], "state": "complete"}


class SeededDefectTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.pipeline = Pipeline(self.tmp.name)

    def assertCaught(self, check):
        with self.assertRaises(AssertionError):
            check(self, self.pipeline)

    def test_unmodified_implementation_passes_the_same_checks(self):
        for check in (check_core_ledger, check_coverage_gap, check_buyer_store_keys):
            with self.subTest(check.__name__):
                self.pipeline = Pipeline(tempfile.mkdtemp(dir=self.tmp.name))
                check(self, self.pipeline)

    def test_wrong_formula_ignoring_refunds_is_caught(self):
        with mock.patch.object(importer, "normalize", defective_normalize(ignore_refunds)):
            self.assertCaught(check_core_ledger)

    def test_wrong_formula_including_shipping_tax_fees_is_caught(self):
        with mock.patch.object(importer, "normalize", defective_normalize(include_shipping_tax_fees)):
            self.assertCaught(check_core_ledger)

    def test_wrong_formula_using_source_net_field_is_caught(self):
        with mock.patch.object(importer, "normalize", defective_normalize(use_source_net_field)):
            self.assertCaught(check_core_ledger)

    def test_duplicate_counting_is_caught(self):
        with mock.patch.object(importer, "normalize", defective_normalize(unstable_business_key)):
            self.assertCaught(check_core_ledger)

    def test_false_complete_coverage_is_caught(self):
        with mock.patch("services.metrics.query.covered_days", always_complete):
            self.assertCaught(check_coverage_gap)

    def test_guessed_store_mapping_is_caught(self):
        with mock.patch.object(importer, "normalize", defective_normalize(ignore_store_identity)):
            self.assertCaught(check_buyer_store_keys)


if __name__ == "__main__":
    unittest.main()
