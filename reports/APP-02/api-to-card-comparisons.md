# API to leadership card comparisons

Actual same-scope API/UI observations are in [comparisons.json](../takeover/browser/comparisons.json). The card preserves the API decimal value and formats currency without calculating revenue in JavaScript.

| Source/date/filter | API value | UI text |
|---|---|---|
| Upright replica, 2026-09-30, all platforms/stores | 7127.78 | $7,127.78 |
| Same date, eBay + GW-001 | 0.00 | $0.00 |
| Same date, GoodwillBooks | 0.00 | $0.00 |

The zero scopes are within a verified complete report. Cash Monkey with no imported report is Unavailable; empty initial state and strategic margin/labor/other missing inputs also remain Unavailable. Failed imports retain 7127.78 with a last-good warning. Injected API outage clears cards and exposes its error; it never substitutes demo values.

[Desktop screenshot](../takeover/browser/leadership.png) and [mobile screenshot](../takeover/browser/mobile.png) were visually inspected. Browser assertions also cover filters, exact definitions/coverage states, no horizontal overflow and no script errors. Alternate report dates reach real import separately. These checks establish developer API consistency; independent financial/dashboard acceptance belongs to Jack mc.
