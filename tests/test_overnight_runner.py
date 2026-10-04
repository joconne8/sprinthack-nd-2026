"""Cancellation and time bounds protect the explicitly requested overnight job."""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from scripts.release.overnight import parse_deadline, run_bounded


class OvernightBoundsTests(unittest.TestCase):
    def test_deadline_is_absolute_and_timezone_required(self):
        self.assertEqual(parse_deadline('2026-10-05T10:00:00-04:00').isoformat(), '2026-10-05T14:00:00+00:00')
        with self.assertRaises(ValueError): parse_deadline('2026-10-05T10:00:00')

    def test_cancelled_and_expired_jobs_never_start(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);stop=root/'STOP';stop.touch();log=root/'run.log'
            self.assertEqual(run_bounded(['missing-executable'],root,log,os.environ,10,stop)['exit_code'],130)
            stop.unlink()
            self.assertEqual(run_bounded(['missing-executable'],root,log,os.environ,0,stop)['exit_code'],124)
            self.assertFalse(log.exists())

    def test_long_running_child_is_terminated_and_logged(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            result=run_bounded([sys.executable,'-c','import time; print("started",flush=True); time.sleep(20)'],root,root/'run.log',os.environ,0.5,root/'STOP')
            self.assertEqual((result['exit_code'],result['cause']),(124,'timeout'))
            self.assertIn('started',(root/'run.log').read_text())
