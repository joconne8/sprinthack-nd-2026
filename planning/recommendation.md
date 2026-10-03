SPRINTHACK RECOMMENDATION

PICK: Pod A, Beacon Health credentialing tool.
BACKUP: Pod B, Goodwill ops reports, but only if they hand you real sample reports at kickoff.
AVOID: both DIU problems unless your builder is strong in radio or crypto.

Constraint: ~28 hours of build time, code freeze 4pm Sunday, 12 min per team at demo. Small team, agents write most code.

SCORING (my judgment, 1 = bad, 5 = good)
                    Demo   Data    Build risk   Fit to you   Total
Beacon credentials   5      4        4            5           18
Goodwill reports     4      2        4            4           14
DIU comms metadata   3      3        2            2           10
DIU RF spectrum      4      3        2            1           10

WHY BEACON WINS
1. Demo story is instant. A manager sees a red/amber/green board of staff, expiring licenses, and an alert fired. Judges get it in 20 seconds. No explaining needed.
2. The data is mostly public and real. Federal sources exist for NPI lookups (NPPES registry API) and exclusion checks (OIG LEIE list, downloadable CSV). Verify both are reachable on the venue wifi in the first hour. You can show real lookups on real public providers while the roster itself is synthetic.
3. It plays to your strengths: workflow, agents, GTM, product story. It is an agent-orchestration problem (check many sources, reconcile, decide, notify), not a research problem.
4. The sponsor needs a product, not a model. You can pitch it as a thing a hospital buys, which is where your GTM background wins the room.
5. JP Burford judges Pod A. He is an ex-WebMD engineering director and 2x YC CTO. He will value a working, well-scoped thing and a clear buyer over a clever model.

BUILD RISK TO ADMIT
- State licensing boards differ and many have captchas or no API. Do not promise 50 states. Do 1 or 2 states for real, fixtures for the rest, and say so on stage.
- Ask Beacon in the room at kickoff: which credentials matter most (state license, DEA, board cert, BLS/ACLS, malpractice, exclusion list), and which they check today. That one answer sets your scope.
- No real staff data will exist. Use synthetic staff and label them synthetic.

WHY NOT GOODWILL
Good problem, bad unknown. It is only strong if they give you real sample reports and source data today. If they do, the demo (before: hours of manual work, after: one click) is also strong. Ask at kickoff. If no sample data by ~2pm, drop it.

WHY NOT DIU
Hiding metadata on LoRa or direct-to-cell is a networking and crypto research problem. A simulation will look like a toy to technical judges and hard to prove "hidden." RF spectrum analysis needs SDR signal knowledge and public captures that are large and messy. Both are demo-able only to a narrow audience, and neither uses your edge.

DECISION RULE
1. Kickoff Q&A: get answers from Beacon (and Goodwill sample data if offered).
2. By end of hour 2, commit. Do not switch after that.
3. Office hours (today from 3pm, tomorrow from 1pm): book a Beacon mentor slot and a Replit or ClickUp mentor for tooling help.

FILES
01 PRD Beacon, 02 PRD Goodwill, 03 PRD DIU metadata, 04 PRD DIU RF, 05 agentic build plan.
