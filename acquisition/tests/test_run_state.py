import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from run_state import execute


def seq(*types):
    calls = []
    def f(n):
        calls.append(n); t = types[min(n - 1, len(types) - 1)]
        return {"ok": True} if t == "ok" else {"ok": False, "type": t, "detail": "d"}
    return f, calls


class RunStateTests(unittest.TestCase):
    def test_retries_then_succeeds_once(self):
        f, calls = seq("timeout", "timeout", "ok"); s = execute("r", f)
        self.assertEqual((s.status, len(calls), s.delivered), ("succeeded", 3, True))
    def test_retries_bounded(self):
        f, calls = seq("timeout"); s = execute("r", f, max_attempts=3)
        self.assertEqual((s.status, len(calls)), ("failed_retriable_exhausted", 3))
    def test_auth_and_policy_never_retried(self):
        for t in ("expired_session", "mfa", "captcha", "access_denied"):
            f, calls = seq(t); s = execute("r", f)
            self.assertEqual((s.status, len(calls)), ("needs_human", 1), t)
            self.assertTrue(s.owner_role and s.cause)
    def test_unknown_failure_fails_closed(self):
        f, calls = seq("surprise"); self.assertEqual(execute("r", f).status, "failed_permanent"); self.assertEqual(len(calls), 1)
    def test_deadline_stops_retry(self):
        t = iter([0, 0, 1000, 1000]); f, calls = seq("timeout")
        s = execute("r", f, deadline_s=600, clock=lambda: next(t))
        self.assertEqual((s.status, len(calls)), ("failed_retriable_exhausted", 1))
    def test_success_not_repeated(self):
        f, calls = seq("ok"); execute("r", f); self.assertEqual(len(calls), 1)

if __name__ == "__main__": unittest.main()
