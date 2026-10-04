from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

from services.data.contracts import REPORTING_ZONE, day


def source_window(metadata):
    zone = ZoneInfo(metadata["reporting_timezone"])
    start = datetime.combine(day(metadata["requested_start_date"]), time(), zone)
    end = datetime.combine(day(metadata["requested_end_date"]) + timedelta(days=1), time(), zone)
    return start.astimezone(timezone.utc).isoformat(), end.astimezone(timezone.utc).isoformat()


def covered_days(windows, start, end):
    """Union intervals; cross-zone edge days are partial unless fully covered."""
    expected = []
    covered = []
    zone = ZoneInfo(REPORTING_ZONE)
    cursor = day(start)
    intervals = sorted((datetime.fromisoformat(w["starts_at"]), datetime.fromisoformat(w["ends_at"])) for w in windows)
    while cursor <= day(end):
        expected.append(str(cursor))
        lower = datetime.combine(cursor, time(), zone).astimezone(timezone.utc)
        upper = datetime.combine(cursor + timedelta(days=1), time(), zone).astimezone(timezone.utc)
        reach = lower
        for left, right in intervals:
            if left <= reach:
                reach = max(reach, right)
        if reach >= upper:
            covered.append(str(cursor))
        cursor += timedelta(days=1)
    return {"expected_days": expected, "complete_days": covered,
            "missing_or_partial_days": [d for d in expected if d not in covered],
            "state": "complete" if expected == covered else "partial" if windows else "unavailable"}
