# DAT-01 review recommendation

Keep the existing merged PR #1 fixtures. Do not regenerate a competing pack or
merge the fixture contribution again. Supplied integrity/regeneration tests pass
at `b329c0fece37c1694b4d84c0c55e609dc931f854`.

Before accepting DAT-01:

1. Jack OC records acceptance or amendments to the GOV-02 scope/metric dictionary,
   with accepted commit, reviewed evidence and reviewer.
2. Fixture/contract owners resolve the seven shipping rows missing stores that
   are absent from the exception ledger. Decide between extending the ledger
   and explicit related-row exception provenance; no guessed store repair.
3. QA independently reviews the source-specific control totals and exception
   policies. Generated manifest agreement alone is not independent acceptance.
4. Confirm the reporting-timezone and refund-as-of conventions, keeping source
   payout columns distinct from demo net sales.

Before DAT-02 implementation, Jack OC provides GOV-03 import/metric/coverage
contracts and ENG-01 accepted scaffold/runtime commands, with exact reserved
data paths. Hugh's acquisition handoff must preserve exact bytes and manifest.
The September replica and August fixtures require an explicit adapter decision.
Update: the later combined-lane user authorization permitted those local setup
decisions. `planning/contracts.md` now documents distinct fixture/replica source
adapters, currency/timezone rules and propagated exception lineage. The final
354 fixture checks pass; no fixture bytes were altered.

After prerequisites and each predecessor are accepted, Peyton's core sequence
is DAT-02 → DAT-03 → DAT-04 → DAT-05 → DAT-06 → DAT-08.
DAT-07 is optional after core acceptance. DAT-09 is a pilot design packet and
does not authorize live execution. No later task is represented as implemented
by this review.

The original preparatory block is retained above as history. DAT-01 is now ready
for review under the combined session, alongside the actual importer test evidence.
No GitHub claim, task status change, push, merge, or production action was made.
