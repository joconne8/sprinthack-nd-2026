# Shared Goodwill agent context

## Start here
[Delivery hub](https://github.com/joconne8/sprinthack-nd-2026/issues/7) · [Card index](BACKLOG.md) · [Original detailed plan](THREE_PHASE_PLAN.md) · [Machine-readable registry](backlog.json).

## Business understanding
ESTEEM discovery identified connected stakeholder needs: Amanda wants Upright reports retrieved without repeated portal work; Debie wants clear management visibility; downstream summaries/accounting need reliable, traceable inputs. Amanda says Cash Monkey is easier, Upright API access was restricted, and AI must go through Copilot. Her follow-up says the e-commerce manager left and she now has an assistant. Do not claim every stakeholder approved the design.

## Three phases
1. Authorized report acquisition; functional Upright-style HTML replica based on supplied slides for the synthetic demo.
2. Raw archive, typed validation, idempotent/overlap-safe imports, reconciliation, lineage and deterministic metrics.
3. Operations/leadership dashboard plus bounded approved metric tools and later agentic interaction.

## Weekend scope
One acquisition-to-dashboard vertical slice; four-view/two-platform PRD remains the limit unless an approved decision replaces it. ShopGoodwill/eBay are scoped application sources; an Upright-style acquisition export needs explicit authority/mapping to avoid overlap. All records synthetic; replica simulated; other sources visibly not connected. Universal recorder, nine live integrations, production Copilot, autonomous accounting and live deployment are deferred.

## Latest corrections
- Existing draft PR [#1](https://github.com/joconne8/sprinthack-nd-2026/pull/1) adds expanded synthetic data, generator, manifest and tests; open/unmerged when checked. DAT-01 reviews it, not recreates it. Reported PR checks are not independent application verification.
- Original plan revenue-conflict note is historical: PR #1 proposes resolving it; until merged and verified, freeze the PRD convention explicitly. Demo net sales excludes shipping/tax/fees.
- Jev is probabilistic AI with service usage; deterministic replay is separate. External Jev is not implicitly compatible with Copilot-only policy.
- A normal view stores a query; materialized views store refreshed results. Excel does not universally fail at 10,000 rows and can feed dashboards.
- Existing Power BI should be assessed before replacing it.
- Source-row count is not necessarily unique buyers; labor hours are not employee count; sell-through needs a cohort; backlog needs a complete snapshot.
- Nine source amounts must not be summed as revenue: sources may overlap or be expenses/settlements.

## Readiness and workflow
All cards are unassigned/unclaimed. Dependency-bearing tasks are initially labeled blocked; dependency-free cards are backlog. Those labels are planning state, not an evaluation that they can safely execute. Human gates and evidence still apply. Suggested lanes are proposals until claimed. Use backlog→in-progress→review→done with blocked where needed; human acceptance closes issues.

## Claim template
```text
Task ID / issue:
Operator or agent session:
Branch / worktree / base commit:
Dependencies and accepted artifacts checked:
Allowed files / shared-file conflicts:
Test commands and expected evidence:
Deadline / spend cap / max 2 repair attempts:
Human approvals required:
```

## Completion template
```text
Commit / changed files:
Commands actually run + pass/fail:
Evidence and expected-result comparisons:
Unsupported behaviors / tests not run:
Blockers and next human review step:
```

## Contract and file ownership
GOV-03 owns schemas; ENG-01 owns initial scaffold/lockfile/CI; a designated data owner serializes migrations. Frontend can use frozen mocks while backend develops. QA writes independently derived tests. Each agent reports under its own task directory; an orchestrator manages shared state.

## Native Projects access
The GitHub API connection can read/write the repository, but Projects listing returned 403 Resource not accessible by integration. Reauthorization context reported healthy and did not identify a reconnectable scope fix. No native board is claimed created. bootstrap_github_project.py attaches these exact issues with custom fields using authorized local GitHub CLI access; README documents the command and limitations.

## Source links
- [Jack explanation](https://drive.google.com/file/d/1jrBRKAFzJlOVUC7mIsyTH3OrCGY-7qD6/view)
- [Wicks plan](https://drive.google.com/file/d/1gip7aNE1TQdZmqNJQeRlPppVZ5iVuWCT/view)
- [Amanda interview](https://drive.google.com/file/d/1WM1HJVAu_YF-Q48CQDa7SFwnPKg1FPlF/view)
- [Amanda follow-up](https://docs.google.com/document/d/1yveSPTDJ4PUVi1MjMvCP6ovVtyVy-M7UGOeDdDngz7g/edit)
- [Amanda supplied PowerPoint](https://docs.google.com/presentation/d/1vkc_Mr8341bDyKkXOkxcKLMj-Du4rOYt/edit)
- [TypeSafe Jev description](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
Agents may need separately authorized access to external source documents. Do not expose source credentials.
