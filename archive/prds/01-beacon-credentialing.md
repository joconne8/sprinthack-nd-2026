PRD 1: BEACON HEALTH CREDENTIAL WATCH (recommended)

PROBLEM
Check clinical staff credentials against public sources, track expirations, alert managers and HR.

USERS
- HR / credentialing coordinator: needs a single view of who is current, expiring, or flagged.
- Department manager: needs a heads-up when someone on the schedule is about to lapse.

SCOPE FOR SUNDAY (must have)
1. Staff roster import (CSV): name, NPI, role, state, license number, license expiry, other certs.
2. Automated verification agents:
   a. NPI check against the NPPES registry API (name, taxonomy, status matches roster).
   b. Exclusion check against the OIG LEIE list (downloaded CSV, matched locally).
   c. State license check for 1 or 2 states (live if scrapable, else fixtures; label which).
3. Expiration tracker: 90 / 60 / 30 / 0 day buckets from roster dates.
4. Dashboard: red / amber / green per person, drill-in showing each source, what was checked, timestamp, evidence link.
5. Alerts: generated email/Slack-style messages to manager and HR (send to a demo inbox or show a preview; do not email real people).
6. Audit log: every check with source and time.

NICE TO HAVE
- Discrepancy explanation by an LLM ("name mismatch: roster says Jon, registry says Jonathan, likely same, confidence medium, needs human").
- DEA and board certification stubs.
- Weekly digest.

OUT OF SCOPE
All 50 states, real PHI, real HR system integration, auth.

DATA
Synthetic roster of 20 to 30 staff. Seed some on purpose: 3 expiring soon, 1 expired, 1 NPI mismatch, 1 on the exclusion list. Use a real public provider for the live lookup demo only if the sources return one; never put a real person on a fake "excluded" record. Make the excluded one a fully fictional name and say it is a test record.

SUCCESS CRITERIA
- Upload roster, board populates in under 60 seconds.
- At least 2 live public-source checks work on stage.
- Every flag shows its evidence.

RISKS AND MITIGATION
- State board blocked or captcha: fixtures plus an honest label.
- API down at demo: record a backup video Sunday 2pm and cache responses.
- LLM wrongly clears someone: LLM may explain, never decide. Status comes from deterministic rules, ambiguous cases go to "needs human."

SUGGESTED STACK
Next.js or a Python FastAPI plus simple frontend, SQLite, background job queue. Keep it boring.

DEMO SCRIPT (about 7 min, adjust to the 12 min slot)
0:00 The pain: one coordinator, spreadsheets, a lapse means a nurse cannot work or the hospital is exposed.
0:45 Upload roster. Board fills.
1:30 Click the exclusion-list hit. Show evidence, source, time.
2:30 Click the mismatch. Show the agent reasoning and the "needs human" call.
3:30 Show the 30-day bucket and the generated alert to the manager.
4:30 Show audit log.
5:00 Buyer and rollout: who pays, what it replaces, pilot with one department.
6:00 Honest limits: 2 states live, rest fixtures, here is the roadmap.
