# Contract checks

Completion evidence: `../integration/completion-verification.json` and
`completion-logs/`. Sixteen schema artifacts and generated TypeScript types
share one structural source. Strict TypeScript compilation and client boundary
tests pass. HTTP requests/responses validate import, metrics/evidence filters,
batch lists/staging rows, exception resolution, health and error contracts.
Negative checks reject floats/invalid decimal money, incompatible envelopes,
unavailable-with-value, impossible dates, unknown filters, non-boolean correction
approval, missing run identity, oversized pages and unsafe proposed tool actions.
Seven existing mock examples still validate. Tool execution remains deferred.

The original foundation results below are retained as historical evidence.

Shared JSON schemas validate actual import, metric, evidence, inventory and
error outputs. Seven supplied mock examples use these same shapes, including
available, partial, unavailable, failed import and stale last-good.

Foundation tests check invalid response types, non-decimal financial strings,
synthetic=false, unavailable-with-number, missing source inputs and namespace
versions. Schema regeneration is byte-identical. Actual results are in
`../integration/logs/foundation-tests.log` and `../integration/verification.json`.
The stdlib runtime validator implements the structural keywords used by these
schemas; it does not claim general-purpose JSON Schema coverage.

TypeScript declarations/client are supplied for Landon; local compilation was
not run because Node is unavailable. React/browser validation is still required
in the frontend checkout.
