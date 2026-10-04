"""Developer collection/controller regressions; independent QA stays in its lane."""
import json
import tempfile
import threading
import time
import unittest
from pathlib import Path

from acquisition.controller import AcquisitionManager
from acquisition.intake import IntakeRejected, intake, submit
from services.data.contracts import DataError
from services.data.importer import Pipeline
from services.metrics.query import metric_response
from tests.helpers import payload, row


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pipeline = Pipeline(self.root / 'state')
        self.data, self.manifest = payload([row(), row('B','20.00','2.00')])
        self.file = self.root / 'download.csv'
        self.file.write_bytes(self.data)

    def manager(self, fn):
        manager = AcquisitionManager(self.pipeline, 'http://127.0.0.1:4173', attempt_fn=fn)
        self.addCleanup(manager.close)
        return manager

    def success(self, record, number):
        return {'ok': True, 'type': 'ok', 'file': str(self.file), 'manifest': self.manifest}

    def wait(self, manager, run):
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            value = manager.get(run['run_id'])
            if value['status'] not in ('pending','running'):
                return value
            time.sleep(.01)
        self.fail('Controller did not finish')

    def test_verified_handoff_replay_and_persisted_last_success(self):
        manager = self.manager(self.success)
        request={'start_date':'2026-09-30','end_date':'2026-09-30'}
        first=self.wait(manager,manager.start(request))
        self.assertEqual(first['status'],'succeeded')
        self.assertEqual(first['import_state'],'imported')
        self.assertEqual(first['coverage_state'],'complete')
        self.assertEqual(first['checksum'],self.manifest['file_checksum'])
        second=self.wait(manager,manager.start(request))
        self.assertEqual(second['import_state'],'duplicate_noop')
        result=metric_response(self.pipeline,'2026-09-30','2026-09-30','upright_replica')
        self.assertEqual(result['metrics'][0]['value'],'27.00')
        self.assertIsNotNone(manager.history()['last_success_at'])
        with self.pipeline.db() as db:
            stored=json.loads(db.execute('SELECT manifest_json FROM import_batches WHERE id=?',(first['batch_id'],)).fetchone()[0])
        self.assertEqual(stored['acquisition_run_id'],first['run_id'])
        self.assertEqual(manager.get(first['run_id'])['batch_id'],first['batch_id'])

    def test_transient_retry_then_one_import_and_auth_no_retry(self):
        attempts=[]
        def flaky(record,number):
            attempts.append(number)
            return {'ok':False,'type':'timeout'} if number==1 else self.success(record,number)
        manager=self.manager(flaky)
        value=self.wait(manager,manager.start({'start_date':'2026-09-30','end_date':'2026-09-30'}))
        self.assertEqual(value['status'],'succeeded');self.assertEqual(attempts,[1,2])
        self.assertEqual(len(self.pipeline.batches()),1)
        denied=self.manager(lambda *_:{'ok':False,'type':'expired_session','detail':'Reset synthetic session'})
        value=self.wait(denied,denied.start({'start_date':'2026-09-30','end_date':'2026-09-30'}))
        self.assertEqual(value['status'],'needs_human');self.assertEqual(len(value['attempts']),1)
        self.assertEqual(value['import_state'],'not_submitted');self.assertEqual(len(self.pipeline.batches()),1)

    def test_busy_period_and_failed_verification_fail_closed(self):
        release=threading.Event()
        def blocked(*args):release.wait(2);return {'ok':False,'type':'report_unavailable'}
        manager=self.manager(blocked)
        run=manager.start({'start_date':'2026-09-30','end_date':'2026-09-30'})
        try:
            with self.assertRaises(DataError):manager.start({'start_date':'2026-09-30','end_date':'2026-09-30'})
        finally:release.set()
        self.assertEqual(self.wait(manager,run)['status'],'needs_human')
        for change in ({'start_date':'2026-02-30'},{'end_date':'2026-09-29'},{'start_date':'2025-09-30'},{'end_date':'2026-12-31'},{'portal_url':'https://vendor.example'}):
            with self.subTest(change=change),self.assertRaises(DataError):
                manager.start({'start_date':'2026-09-30','end_date':'2026-09-30',**change})
        self.file.write_bytes(self.data+b'broken')
        invalid=self.manager(self.success)
        value=self.wait(invalid,invalid.start({'start_date':'2026-09-30','end_date':'2026-09-30'}))
        self.assertEqual(value['status'],'needs_human');self.assertIsNone(value['batch_id'])
        self.assertEqual(self.pipeline.batches(),[])

    def test_intake_filters_survive_and_tampered_archive_cannot_submit(self):
        manifest={**self.manifest,'channels':['eBay']}
        record=intake(self.file,manifest,'safe-run','2026-09-30','2026-09-30','upright_replica','paid_orders',self.root/'archive')
        submit(record,self.pipeline)
        metrics=metric_response(self.pipeline,'2026-09-30','2026-09-30','upright_replica')
        self.assertEqual(metrics['metrics'][0]['availability'],'partial')
        self.assertNotEqual(metrics['coverage']['state'],'complete')
        archive=Path(record['artifact_ref']);archive.chmod(0o600);archive.write_bytes(b'tampered')
        with self.assertRaises(IntakeRejected):submit(record,self.pipeline)
        with self.assertRaises(IntakeRejected):
            intake(self.file,self.manifest,'../escape','2026-09-30','2026-09-30','upright_replica','paid_orders',self.root/'archive')

    def test_restart_retains_finished_history_and_marks_interrupted_run(self):
        manager=self.manager(self.success)
        run=self.wait(manager,manager.start({'start_date':'2026-09-30','end_date':'2026-09-30'}))
        interrupted={**run,'run_id':'a'*32,'status':'running','stage':'importing','finished_at':None}
        manager._save(interrupted)
        recovered=self.manager(self.success)
        saved=recovered.get('a'*32)
        self.assertEqual(saved['status'],'needs_human')
        self.assertEqual(saved['batch_id'],run['batch_id'])
        self.assertEqual(saved['import_state'],'imported')
        self.assertEqual(recovered.get(run['run_id'])['status'],'succeeded')
