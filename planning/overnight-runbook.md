# Bounded overnight verification

Peyton explicitly requested overnight code execution through October 5, 2026, 10 a.m. Eastern
(14:00 UTC). The runner executes tests on a frozen clean Git checkout; it does not change code.
Human reviewer: Peyton, with the team integrator reviewing the release PR.

```sh
python3 scripts/release/overnight.py --source /path/to/frozen-clean-checkout \
  --output .runtime/overnight --node /absolute/path/to/node \
  --node-modules /absolute/path/to/tools/verification/node_modules \
  --until 2026-10-05T10:00:00-04:00
```

Add `--chrome-path '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'` to use installed Chrome.
`--dry-run` records the plan without running checks. The actual source path, PID, commit,
UTC deadline and every executed command are recorded in `.runtime/overnight/status.json`.

Every hour: full Python suite including real browser acceptance, acquisition unit suite,
and required report/artifact references. At most 36 cycles; each job at most 90 seconds
and at most the remaining deadline. Two consecutive failed cycles, changed source bytes,
STOP, signal, cycle cap or deadline end the run. Outputs are isolated per cycle.
No models, paid services, network integrations, code edits, pushes or merges occur.

Cancel safely:

```sh
touch .runtime/overnight/STOP
```

The STOP file cancels even an active child process group. TERM/INT also request cancellation.
Read `status.json` and `cycle-*/1.log`; a planned or waiting run is not a completed future test.
The Mac must remain powered, plugged in and with its lid open. A process-bound `caffeinate -i`
prevents idle sleep while the runner is alive; it cannot prevent shutdown or lid sleep.
Cancellation/timeout/deadline tests: `python3 -m unittest tests.test_overnight_runner -v`.
This replaces the proposed coding-agent automation with the explicitly requested bounded local checks.
