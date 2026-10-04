# Contracts

Shared data, API and tool contracts. Owner: Jack OC (GOV-03). Design and rules: [planning/contracts.md](../planning/contracts.md).

| Path | What it is |
| --- | --- |
| `v1/goodwill-contracts.schema.json` | JSON Schema draft-07 bundle. Validate against `#/definitions/<Name>` |
| `v1/expected-reports.json` | Reports expected per reporting date |
| `v1/examples/valid/` | Shared fixtures for development mocks and contract tests. File name prefix = definition name |
| `v1/examples/invalid/` | Shapes that must be rejected |
| `tests/validate-contracts.cjs` | Contract checks (no dependencies) |
| `sources/acquisition-classes.md` | Hugh's ING-05 draft; reconciled into v1 (see `reports/GOV-03/compatibility-notes.md`) |

Run the checks from the repository root:

```bash
node contracts/tests/validate-contracts.cjs
# Without Node installed, VS Code's bundled runtime works:
ELECTRON_RUN_AS_NODE=1 "<path to VS Code>/Code.exe" contracts/tests/validate-contracts.cjs
```

Change a contract through a PR that updates the schema, its examples and this check together. Jack OC reviews.
