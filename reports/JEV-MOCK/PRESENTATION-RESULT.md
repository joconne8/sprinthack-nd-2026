# Walkthrough and first-run Jev presentation

User authorized presentation implementation; existing experiment branch and lane. Changed experiments/jev/lab.cjs, lab.html, lab-ui.js, lab.test.cjs, README.md; added walkthrough.cjs. No shared portal, contract, or dashboard changes. No merge/deployment.

Presentation button explicitly selects live Jev and uses the existing predefined synthetic workflow without manufacturing recording evidence or changing the saved recipe. Existing bounded provider, deterministic parameters, approval and file verification remain. Staged browser video is labeled scripted and not training input.

Executed walkthrough.cjs with temporary Playwright ffmpeg encoder. Download independently checked: 256 rows, requested October 1–2 dates, synthetic markers, checksum. Artifacts .runtime/jev-lab/walkthrough.webm, walkthrough.csv, walkthrough-evidence.json. Chrome confirmed 17.52-second 1280x800 video metadata; screenshot .runtime/jev-presentation-preview.png.

Executed lab.test.cjs: exit 0, seven scenario groups pass, including new predefined first-run injected Jev success without recipe, recorded replay/import/duplicate, drift stop, approved and rejected repair, expired session. Logs /private/tmp/jev-presentation-tests.log; evidence /var/folders/1t/r8vbq2ns31z3ld8d_36zw3s40000gn/T/jev-lab-tests-8mdTkS. These tests inject responses and do not prove live API success or speed. Node syntax checks and git diff --check passed.

Temporary test portal stopped. Existing key-configured user lab left running; requires restart to load new server route. Key remains in user's terminal process environment and was not accessed. No live API call was made in this implementation session. Runtime artifacts are local and not committed. Real Jev latency/confidence remain rehearsal limitations.
