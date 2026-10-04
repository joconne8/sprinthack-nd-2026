"""ING-04 draft: bounded retry and run-state classification for acquisition runs.

Pure logic, no I/O or sleeping, so it is deterministic to test. A caller supplies the
attempt function and clock. Auth/policy failures are never retried.
"""
from dataclasses import dataclass, field

RETRIABLE = {"timeout", "download_failed"}                       # transient: delayed generation, flaky download
HUMAN_REQUIRED = {"expired_session": "Goodwill operator (re-authenticate)",
                  "mfa": "Goodwill operator", "captcha": "Goodwill operator",
                  "access_denied": "Goodwill IT / provider owner",
                  "label_changed": "Acquisition maintainer (reviewed revalidation)",
                  "wrong_page": "Acquisition maintainer"}
PERMANENT = {"host_not_allowed", "bad_params"}


@dataclass
class RunState:
    run_id: str
    status: str = "pending"           # pending|running|succeeded|failed_retriable_exhausted|needs_human|failed_permanent
    attempts: list = field(default_factory=list)
    cause: str = ""
    owner_role: str = ""
    delivered: bool = False           # set once; retries can never deliver twice


def execute(run_id, attempt_fn, max_attempts=3, deadline_s=600, clock=lambda: 0.0):
    """attempt_fn(n) -> typed result dict with ok/type. Stops at max_attempts or deadline."""
    st = RunState(run_id)
    start = clock()
    for n in range(1, max_attempts + 1):
        if clock() - start > deadline_s:
            st.status, st.cause, st.owner_role = "failed_retriable_exhausted", "deadline exceeded", "Acquisition maintainer"
            return st
        st.status = "running"
        res = attempt_fn(n)
        st.attempts.append({"n": n, "type": res.get("type"), "ok": res.get("ok", False)})
        if res.get("ok"):
            if st.delivered:
                raise RuntimeError("duplicate delivery prevented")
            st.status, st.delivered = "succeeded", True
            return st
        t = res.get("type")
        if t in HUMAN_REQUIRED:
            st.status, st.cause, st.owner_role = "needs_human", f"{t}: {res.get('detail', '')}", HUMAN_REQUIRED[t]
            return st
        if t in PERMANENT or t not in RETRIABLE:   # unknown types fail closed
            st.status, st.cause, st.owner_role = "failed_permanent", f"{t}: {res.get('detail', '')}", "Acquisition maintainer"
            return st
    st.status, st.cause, st.owner_role = "failed_retriable_exhausted", f"{max_attempts} attempts: last {st.attempts[-1]['type']}", "Acquisition maintainer"
    return st
