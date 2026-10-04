# Contract checks

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
