# ING-06 (optional Jev evaluation): BLOCKED

Needs ING-02 accepted and GOV-04, plus confirmed access and approval to use Jev for a synthetic-only experiment. Neither was found; AGENTS.md says Jev and Copilot approvals are not assumed. No model was called and no provider was substituted.
When unblocked: keep deterministic replay as the baseline (`acquisition/run_skill.cjs`), put a decision provider behind an interface, fail closed on low confidence, never label a scripted provider as Jev, and report decision latency separately from full report time.
