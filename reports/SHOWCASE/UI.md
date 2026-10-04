# Showcase UI — ready for integration review

Operator: Codex/Peyton, bounded UI worker. Branch `peyton/aimsigh-showcase`,
shared worktree `/private/tmp/aimsigh-showcase`, base `3a8c734`. Allowed lane:
`apps/showcase/` and `reports/SHOWCASE/UI*`. Root owns all HTTP entrypoints,
contracts, migrations, recorder instrumentation, and data calculations.

User-approved scope and frozen API: `CLAIM.md` / `CONTRACT.md`. Source basis:
the October 4 DEMO PLAN, Aimsigh pitch, and PLAN §6. Current user decisions
authorize richer metrics, workbook delivery, local recording, and model-free
questions with explicitly invented matched sample inputs.

## Implemented

- Cream/forest-green Georgia/Arial workspace with Collect, Verify & Deliver,
  and Understand views. The existing dashboard is unchanged.
- Published-snapshot metrics, daily canvas chart/PNG, comparison, source/store/
  platform breakdowns, source-local buyer counts, and missing-input disclosures.
  Canvas chart scaling uses numerical conversion solely for drawing; financial
  totals and ratios arrive as backend decimal strings. Missing dates break the
  plotted line, rather than implying uninterrupted coverage.
- Shared scope filters, request cancellation/generation guards, clear loading,
  partial/unavailable/error states, and removal of stale selection values after
  an API failure.
- Pinned sales/input evidence dialog and pagination. All report fields render
  via text nodes. Citation URLs are restricted to the same-origin showcase API.
- Teams-style local channel, typed supported-question chips, read-only questions,
  real canvas summary attachment, and tool/snapshot/citation metadata.
- Actual recorder UI with iframe source/origin/session/nonce checks, serialized
  recorded actions, review/approve flow, selectable approved recipes, new-date
  replay, actual browser frames/events, and collection exception history.
- Snapshot-pinned workbook/CSV/dictionary links, nine-source register, actual
  SQLite relationship labels and integration boundary explanation.
- Separately dated August inventory view via the existing API. Unprepared
  inventory stays visibly unavailable; it is never joined to September sales.

## Commands and observed results

`node --check apps/showcase/app.js` using installed Node 22.14.0: PASS.

`node /private/tmp/showcase-ui-preview.cjs`: PASS, twice (second run after chart
and source-count changes), zero browser page errors. This isolated Chrome
preview intercepts requests with frozen contract responses. Verified cards,
actual canvas summary PNG, platform-dependent unavailability, sales/input
evidence, unsupported questions, and no horizontal overflow at 390px. Desktop
and mobile screenshots were visually inspected:
`/private/tmp/showcase-ui-desktop.png`, `/private/tmp/showcase-ui-mobile.png`.

Chrome initially failed to launch inside the sandbox; the authorized local
browser run succeeded with escalation. `git diff --check`: PASS.

## Limits / integration handoff

The preview is a UI contract check, **not** evidence of portal acquisition,
importer arithmetic, or a real workbook. Independent QA owns the actual
end-to-end browser test in `tests/showcase_browser.cjs`; API/backend wiring was
still in progress when this report was written. Recorder and replay depend on
root's actual same-origin portal instrumentation and API. No external messages,
models, services, production access, or Git commits were performed by this lane.

Stable selectors are the semantic controls and IDs in `apps/showcase/index.html`.
Metrics expose `data-metric-id` and their exact backend value in `data-value`.
Human integration/acceptance remains required.

## Real API integration follow-up

Actual preview: `http://127.0.0.1:8091/showcase`, root-prepared verified
September 1–29 checkpoint. The independent end-to-end acceptance found a
390px overflow during the desktop-to-mobile transition. Inspection reproduced
the 394px document width: the deliver grid and workbook labels imposed a
minimum content width. The UI now permits grid children to shrink and wraps
download labels and long snapshot IDs.

An additional 320px check identified comparison-card and customer-table minimum
widths; root explicitly authorized one focused repair. Comparisons stack below
360px and the customer table scrolls within its panel.

`node /private/tmp/showcase-ui-real-validation.cjs`: PASS using the real
loopback API, installed Chrome, and actual prepared sample data. Verified:

- All three views at 390px and 320px: document width equals viewport width.
- Daily summary scope is September 30–30; its label and chart make that date
  explicit. Questions retain the selected dashboard scope.
- Supporting records provide actionable archived original CSV and matching
  manifest links. Both requests returned HTTP 200; inspected CSV was 249,040
  bytes and manifest identified `cash_monkey_replica`.
- Zero browser page errors. Actual desktop and 390px/320px screenshots:
  `/private/tmp/showcase-ui-real-desktop.png`,
  `/private/tmp/showcase-ui-real-390.png`, `/private/tmp/showcase-ui-real-320.png`.
- Monthly workbook control is disabled until both September feeds have complete
  coverage, matching backend `export_incomplete` behavior.

This follow-up verifies the actual UI, daily scope, downloads, and responsive
repair. Full recorded acquisition/replay/failure recovery is independently
tested by the QA lane, whose final integration rerun follows these changes.
