# Architecture Review Reconciliation

**Date:** 2026-10-07

**Canonical repository:** `bedriozgur/ai-work-framework`

**Reviewed public HEAD:** `5d644751ef9b909d0ac792942c71491cd1ebde31`

**Historical Claude R1 base:** `ddc169ba6fd791893f04c1093613c12128cd3a9a`

**Accepted implementation:** `23d9b5064fb4a970b12b14ad6f13f4638785d32e`

## Verdict

The repository at reviewed HEAD was **pilot-capable but not operationally complete**. Its strongest ideas were already sound: durable repo state, explicit evidence and completion honesty, bounded execution, and a simple GitHub/Drive split. The genuine release gap was a missing deterministic entry point and validation contract.

Commit `23d9b50` closes that gap without adopting a state service, lock manager, capability-manifest system, adapter hierarchy, or schema estate. The result is **READY FOR THE NEXT TWO CONTROLLED PILOTS**. It is **NOT V1 READY** until pilot evidence exists and the remaining partial findings are either closed or explicitly accepted as advisory/runtime responsibilities.

## Evidence boundary

- The public repository was cloned and `origin/main` was confirmed at `5d64475` immediately before implementation.
- The historical commit `ddc169b` exists in the repository ancestry. The diff from it to reviewed HEAD changed only `AGENT-OPERATING-PROTOCOL.md`, `AI-PROJECT-OPERATING-FRAMEWORK.md`, and `framework.yaml`.
- The full Claude R1 attachment was available. It contained 22 findings and clearly stated that it reviewed a transported 19-file snapshot, not GitHub itself.
- The later Claude review was available only as its explicit partial summary. It inspected eight root items, no `patterns/`, no `templates/`, and no pinned commit.
- The Kimi material was available as a maintainer-response document. It contains unresolved `[VERIFY]` markers and repeats claims about nonexistent files.
- The raw Gemini review and raw DeepSeek blocked response were not available in the carried conversation. Only the prior conversation's summaries were available. Their claims are therefore adjudicated only where the claimed files or mechanisms can be checked directly; missing wording was not reconstructed.
- The file named `DEEPSEEK-ARCHITECTURE-REVIEW-R1.md` in the later exchange was explicitly produced by Claude Sonnet, not DeepSeek. Filename is not treated as model provenance.

## Finding-by-finding reconciliation

Statuses describe the repository after `23d9b50`; the evidence column also identifies what was true at reviewed HEAD.

| ID | Status | Repo-grounded adjudication |
|---|---|---|
| F-01 deterministic entry point | **RESOLVED** | At `5d64475`, `project.yaml` was referenced but absent. The implementation makes it mandatory, defines nearest-ancestor discovery, supplies templates, pins a 40-character commit, and validates required files (`AGENT-OPERATING-PROTOCOL.md:14-16`, `BOOTSTRAP.md:14-20`, `scripts/validate_project.py:37-104`). |
| F-02 concurrency/stale writes | **PARTIALLY RESOLVED** | The original criticism was correct; booleans were not a procedure. The accepted solution deliberately scopes v0.1 to one canonical-state writer, records `base_commit`, rechecks before write, forbids force-push, and blocks on conflict (`AGENT-OPERATING-PROTOCOL.md:188-202`). Distributed leases, locks, and an append-only state engine are rejected until a real parallel-writer pilot justifies them. |
| F-03 permissions/trust/approval | **PARTIALLY RESOLVED** | Retrieved content is already non-authoritative; enforcement is honestly distinguished from policy. Approval now binds approver, action scope, run, and expiry (`AGENT-OPERATING-PROTOCOL.md:48, 81-93`). Cross-runtime credential enforcement remains outside this documentation repository and must be verified per runtime. |
| F-04 identity and lifecycle | **PARTIALLY RESOLVED** | Stable project-local task, decision, check, run, and state IDs now exist in the protocol/templates. A central registry and lease lifecycle were rejected. Legal state-transition validation remains absent. |
| F-05 state classification/freshness | **PARTIALLY RESOLVED** | The old template could not represent all seven classes. `templates/STATE.md` now records class, evidence, as-of time, and freshness per entry. Expiry is not automatically computed. |
| F-06 verification and two homes | **PARTIALLY RESOLVED** | `CHECKS.md` is now the single definition home for Full projects; tasks reference check IDs and progress records result/evidence (`AGENT-OPERATING-PROTOCOL.md:109-113`, `templates/CHECKS.md`, `templates/PROGRESS.md:27-30`). The validator does not yet prove that COMPLETE has every passing check. |
| F-07 evidence references | **PARTIALLY RESOLVED** | Minimum reference fields are now specified (`AI-PROJECT-OPERATING-FRAMEWORK.md:141-143`). Automated hash/refetch verification is not implemented. This is needed only for pilots claiming exact-byte reproducibility. |
| F-08 sensitive evidence | **PARTIALLY RESOLVED** | The incorrect framework-repository-only scope is fixed; credentials are prohibited in agent-readable files and projects must define locations/redaction (`AGENT-OPERATING-PROTOCOL.md:204-208`). A universal retention/provider policy would be inappropriate without project requirements. |
| F-09 retries/idempotency/recurrence | **PARTIALLY RESOLVED** | Reviewed HEAD already added destination inspection after ambiguous writes. The implementation adds bounded read retries, no blind retry of non-idempotent writes, run IDs, base commits, one-writer preflight, and stable request IDs where supported. A durable intent log is not justified yet. |
| F-10 rollback/audit | **PARTIALLY RESOLVED** | Reviewed HEAD distinguished Git recovery from external side effects. The progress template now records runtime, time, base commit, task, completion, approvals, outputs, verification, blockers, and handoff. Automated rollback and known-good tags remain project/runtime decisions. |
| F-11 handoff inconsistency | **RESOLVED** | Protocol, framework, pattern, progress template, and `framework.yaml` now agree on an always-required eight-field handoff including VERIFICATION (`AGENT-OPERATING-PROTOCOL.md:142-154`; `framework.yaml:24-32`). |
| F-12 precedence ambiguity | **RESOLVED** | The protocol is declared normative; non-overridable invariants are enumerated; project rules may tighten but not loosen them; evidence cannot join the authority chain; same-tier conflict requires explicit supersession or escalation (`AGENT-OPERATING-PROTOCOL.md:6-8, 34-50`; framework lines 76-85). |
| F-13 pin/migrations/adoption order | **PARTIALLY RESOLVED** | Exact commit pinning and pilot-before-v1 order are implemented (`VERSIONING.md:13-23`; framework lines 145-152). Migration automation and remote-ref resolution are premature before the first version transition. |
| F-14 unverifiable review transport | **SUPERSEDED** | The historical Drive snapshot was not independently verifiable. This reconciliation uses an actual Git clone, exact commits, history, full tree, and local diff. A permanent review-bundle generator is not required for normal repository review. |
| F-15 adapters/capability model | **REJECTED** | The observed transport limitation was real, but it does not justify mandatory per-vendor adapters and capability manifests. Boot preflight checks actual tools; `templates/AGENTS.md` is an optional pointer. Add an adapter only after a pilot demonstrates a repeatable runtime-specific gap. |
| F-16 permission vocabulary | **PARTIALLY RESOLVED** | The generic machine term is now `destructive_action`, and the Rules template defines included operations. Some overlapping terms remain because production change, irreversible action, and deletion are not identical risks. A separate taxonomy specification is unnecessary at this size. |
| F-17 stale decisions/self-application | **PARTIALLY RESOLVED** | The stale versioning/storage open items were pruned and the framework decision now contains ID, status, evidence, alternatives, risks, and revisit condition. Requiring this framework repository to pin itself is rejected because a commit cannot contain its own resulting SHA. |
| F-18 profile/baseline inconsistency | **RESOLVED** | Full-profile triggers are now concrete: gated action, recurrence, multiple writers, sensitive data, or explicit acceptance/source governance (`BOOTSTRAP.md:6-12`). The baseline key and prose both say “when practical.” |
| F-19 review-trigger semantics | **STILL OPEN** | The trigger list remains partly judgment-based. Numeric thresholds would create false precision before pilots. Pilot records should show when review was triggered; objective thresholds can be added only if inconsistent decisions are observed. |
| F-20 duplication/overhead | **PARTIALLY RESOLVED** | The protocol is now the normative source and known handoff/profile drift is removed. Some intentional repetition remains for usability. Pilot metrics now measure boot time and resume clarification before any consolidation is attempted. |
| F-21 vendor names in core | **REJECTED** | GitHub and Google Drive are an explicit architecture decision with a revisit condition, not accidental coupling. An abstract storage interface would add indirection without a second supported backend. |
| F-22 no pilot metrics | **RESOLVED** | Adoption now pre-registers boot time, resume clarification, stale-state incidents, validation failures, and human interventions (`AI-PROJECT-OPERATING-FRAMEWORK.md:145-150`). |

## Other review claims

### Claude current partial review

- **Boot/discovery not operational — RESOLVED.** This was the strongest current finding and drove the accepted implementation.
- **Authority trusts location rather than authorship — PARTIALLY RESOLVED.** Evidence cannot become instruction authority and approvals require a recorded decision authority. Authentication of the human/system channel is a platform responsibility and must not be falsely claimed by Markdown.
- **`framework.yaml` mostly unconsumed — STILL OPEN.** The project validator enforces the boot contract, but most behavioral booleans remain reference configuration. Before v1, either make a key mechanically consumed or remove any implication that it is enforced.
- **Eight contradictions — MIXED, MOSTLY RESOLVED.** Handoff fields/requirement, secrets scope, profile source, baseline, source-table shape, state representation, and acceptance-check ownership were aligned. Qualitative review triggers remain open.
- **Reject locks/state log/capability manifests — ACCEPTED.** Git plus an explicit single-writer rule is the proportional pilot design.

### Gemini review

- Claims involving `config/project.yaml`, `patterns/core.md`, or similar paths are **REJECTED**. Those files do not exist at reviewed HEAD, at `ddc169b`, or in the current tree.
- The generic concerns behind schema validation and evidence-as-data were **ACCEPTED IN MODIFIED FORM**: a small project-contract validator and explicit trust boundary were implemented.
- Mandatory lock managers, tool registries, and broad deterministic gating were **REJECTED/DEFERRED** because the review did not ground them in actual repository code or an executable runtime owned by this repository.

### Kimi response

- The response is not independent evidence for nonexistent files; its `[VERIFY]` markers and inherited premises make those commitments **REJECTED**.
- The idea that prompt tags alone are not a security boundary is **ACCEPTED** and already reflected by the policy-versus-enforcement distinction.
- `state_manager.py`, cross-platform file locks, append-only `state_log.jsonl`, per-adapter `capabilities.yaml`, and a red-team harness are **REJECTED FOR NOW**. They solve a production runtime that this repository does not contain and would substantially increase maintenance surface.

### DeepSeek blocked review

The blocked response produced no repository findings, so there is nothing to classify. Its refusal to invent findings is good review behavior but not evidence about the architecture. The later file bearing a DeepSeek filename was authored by Claude and is treated as Claude's partial review.

## Complexity-cost test

Accepted changes prevent concrete failures with low ongoing cost:

1. Missing/ambiguous project discovery → one manifest and one validator.
2. Floating framework behavior → exact commit pin.
3. Silent concurrent overwrite → explicit one-writer scope, base commit, recheck, and BLOCKED conflict outcome.
4. Drift between tasks/checks/handoffs → small project-local IDs and aligned templates.
5. Review-driven bureaucracy → measured pilot overhead before adding more machinery.

Rejected proposals require a service or abstraction before evidence of need: distributed leases, shared append-only state logs, six or more schemas, per-model adapters, capability manifests, storage interfaces, and mandatory review-bundle tooling.

## Smallest coherent next step

Do not add more framework structure now.

1. Tag or otherwise record `23d9b50` as the draft pilot baseline.
2. Run one Lightweight and one Full pilot, each with a `project.yaml` pinned to `23d9b50`.
3. Capture the five registered metrics plus every validator false positive/negative.
4. After both pilots, decide whether F-04/F-05/F-06 need additional mechanical checks and whether unconsumed `framework.yaml` keys should become executable or be removed.
5. Do not declare v1 until that evidence is reviewed and remaining PARTIALLY RESOLVED/STILL OPEN items are explicitly closed or deferred with scope statements.

## Verification performed

- Confirmed reviewed HEAD matched freshly fetched `origin/main` before changes.
- Compared `ddc169b..5d64475` and inspected every tracked file at reviewed HEAD.
- Ran `python3 -m unittest discover -s tests -v`: 5/5 passing.
- Ran Python bytecode compilation for validator and tests.
- Ran `git diff --check`: clean.
- Confirmed validator rejects a moving `main` ref, missing required file, path traversal, and unreplaced placeholders; it accepts valid Lightweight and Full manifests.
