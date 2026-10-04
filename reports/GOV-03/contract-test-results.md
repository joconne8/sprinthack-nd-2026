# GOV-03 contract test results

Run on 2026-10-04 (UTC) on Windows 11. Node is not installed, so the checks ran on VS Code's bundled runtime
(`ELECTRON_RUN_AS_NODE=1`, reporting Node v24.21.0). Full output: `contract-run.log`.

```bash
ELECTRON_RUN_AS_NODE=1 "/c/Users/lando/AppData/Local/Programs/Microsoft VS Code/Code.exe" contracts/tests/validate-contracts.cjs
```

## Result: 58 passed, 0 failed (exit 0)

| Group | Checks | Result |
| --- | --- | --- |
| Validator self-tests: type lists, oneOf exclusivity, if/then, additionalProperties, date and date-time formats, `$ref` sibling guard, cent arithmetic | 16 | pass |
| Schema lint: every node uses supported keywords; every `$ref` resolves | 1 (66 definitions) | pass |
| Valid fixtures pass the schema and the semantic rules | 23 examples + `expected-reports.json` | pass |
| Cross-file: `MetricResult.available` value equals its drilldown's `displayed_value` | 1 | pass |
| Invalid fixtures rejected, each for its intended reason (first error recorded in the log) | 14 | pass |
| Replica CSV SHA-256 equals its manifest | 1 | pass |
| Translated replica manifest fails only on `reporting_timezone` | 1 | pass, recorded as a **known gap** |

Every top-level contract has at least one valid example.

## Acceptance tests from the GOV-03 packet

| Packet acceptance test | Evidence | Status |
| --- | --- | --- |
| Browser output enters the importer without undocumented translation | The translation is documented in `compatibility-notes.md` table 1 and replayed on the real replica file. After translation, the only failure is the timezone, which needs a one-line replica change. | Met for the documented translation. **Blocked on Hugh's timezone change** for real files to pass. |
| Frontend and tool fixtures validate against the same schemas as backend responses | All fixtures are in one bundle, shared by mocks, tools and backend tests. No frontend or backend exists yet to test against it. | Met for fixtures. Implementation-side tests belong to the APP and DAT lanes. |
| Schema versions, compatibility policy and tests cover duplicate, late, malformed and missing-source cases | `contract_version` plus the semver policy (`planning/contracts.md` §9), and fixtures for each case: `duplicate-noop`, `late-correction`, `malformed-unreconciled`, `with-rejections`, `partial-missing-day`, `stale-last-good`, `SourceCoverage` | Met |

## Negative control

Changing one amount in `MetricResult.available.json` from `74.50` to `74.51` produced `57 passed, 1 failed` with exit code 1
(`negative-control-run.log`). Restoring the file gave `58 passed, 0 failed` again. So the harness can fail.

## Not run

- **A standard JSON Schema validator** (for example ajv). There is no package manifest yet; ENG-01 owns dependencies. The bundled checker covers only the keywords this bundle uses, and it refuses anything else.
- **Type generation and generated clients** (ENG-01).
- **API and UI contract tests** against real implementations. None exist yet (DAT-06, APP-01..03).
- **Python fixture tests** (`goodwill/synthetic-data`), because Python is not installed. GOV-03 does not change those files.
