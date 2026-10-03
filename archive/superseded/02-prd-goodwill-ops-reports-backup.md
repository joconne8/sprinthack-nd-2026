PRD 2: GOODWILL MICHIANA REPORT AUTOMATOR (backup)

PROBLEM
Staff build recurring operations reports by hand. Automate them.

GATE: do not start unless Goodwill provides sample source data and 1 or 2 example finished reports by ~2pm Saturday. Ask what tools produce the data (spreadsheets, POS exports, HR system).

USERS
Operations managers who spend hours each week assembling the same reports.

SCOPE (must have)
1. Ingest: upload the source exports (CSV/XLSX).
2. Report templates matching their existing reports, defined as config, not code.
3. Generation agent: cleans data, computes metrics, builds the report (table, chart, short written summary).
4. Validation: totals reconcile with source, row counts match, anomalies flagged.
5. Output: PDF or XLSX in the same layout they use today, plus a one-click "regenerate for next week."
6. Natural language Q&A over the report ("why did store X drop?"), answers cite rows.

NICE TO HAVE
Scheduled runs, email delivery preview, anomaly commentary.

OUT OF SCOPE
Live system integrations, auth, write-back.

DATA
Only real if Goodwill supplies it. If they give none, you would have to invent data, and that kills the pitch. This is why it is the backup.

SUCCESS CRITERIA
Generated report matches the manual one on every number. Time from files to report is seconds.

RISKS
Messy source data eats the schedule; unknown report logic; they may not have a defined metric spec. Mitigate by picking the single most painful report and doing only that.

DEMO SCRIPT
0:00 Show the manual report and how long it takes (ask Goodwill staff for the real figure, quote it as theirs).
1:00 Drop in this week's files.
1:30 Report appears, matches the original.
2:30 Show validation catching a planted error.
3:30 Ask a question, show the cited answer.
4:30 Next week: one click.
5:30 Rollout: start with one report, then template library.
