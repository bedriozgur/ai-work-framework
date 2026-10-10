# Agent Workflow Map

This document defines the default routing between the five reusable profiles. It is a workflow design, not proof that any specific OpenClaw/n8n automation is deployed. Verify and enforce tool permissions in the actual runtime.

## Routing table

| Request type | Lead | Supporting agent | Default sequence |
|---|---|---|---|
| Portfolio, watchlist, scheduled MIDAS scan | Infra-Orchestrator (scheduled routing) or MIDAS-Trader (direct request) | QA-Auditor when required | Verify due/run context → source-specific research → audit → persist/hand off |
| TradingView vs Alpha Vantage independent study | Infra-Orchestrator | MIDAS-Trader with two isolated runs; QA-Auditor after both finish | Run A + Run B independently → freeze outputs → compare → audit |
| OpenClaw, n8n, MCP, scheduler issue | Infra-Orchestrator | QA-Auditor for consequential changes | Read-only diagnosis → bounded fix proposal → approval if needed → execute only approved change → verify |
| Customer infrastructure assessment/design | Enterprise-Architect | QA-Auditor for high impact or explicit review | Gather evidence → classify facts → plan → customer/internal output split → review |
| Product, technology, or personal research | Research-Curator | QA-Auditor when evidence or consequence warrants | Define scope → primary research → compare → synthesize |
| Cross-domain request | Infra-Orchestrator | One domain specialist at a time, plus QA as needed | Split only at clear boundaries; retain one task/run ID and explicit artifact ownership |

## MIDAS two-source sequence

1. Orchestrator validates the task envelope, market date/session, current MIDAS rules, symbols, interval, freshness, and permission boundary.
2. TradingView run collects and computes only TradingView-based results; Alpha Vantage run collects and computes only Alpha Vantage-based results. Separate directories or isolated work contexts are preferred.
3. Each run records raw evidence references, timestamps, formula/seed settings, missing data, and bounded retries.
4. Orchestrator waits for both terminal states. If one fails, preserve the successful run and report the combined task as `PARTIAL` or `BLOCKED`; do not fill gaps with the successful provider.
5. Only after both outputs are frozen may the comparison identify differences and possible causes.
6. QA-Auditor independently checks the final report against both isolated evidence sets and applicable rules.
7. Persist only to the authorized MIDAS destination. This workflow never routes to broker write access.

## Common task envelope

Every handoff should carry:

- `task_id`, `run_id`, and parent run/task ID where applicable.
- Objective and explicit non-goals.
- Project root and exact base revision.
- Input artifact identifiers/revisions and freshness requirements.
- Assigned profile and bounded responsibility.
- Required and prohibited tools/actions.
- Source policy, including isolation labels and fallback rules.
- Deadline, timeout, and maximum attempts.
- Acceptance checks and output format/path.
- Approval status and exact approved scope, if any.

Never pass secrets in prompts or task envelopes. Put operational credentials in the approved secret store/runtime configuration.

## Return envelope

Every agent returns:

- Task/run IDs and assigned profile.
- Status: `COMPLETE`, `PARTIAL`, `BLOCKED`, `FAILED`, or `CANCELLED`.
- Inputs and revisions actually used.
- Work performed and outputs with exact locations.
- Sources/tools actually used, timestamps, retries, and errors.
- Checks performed and evidence for results.
- Assumptions, unknowns, conflicts, and limitations.
- Decisions required from the human.
- One concrete next action.

## Routing and concurrency rules

- One canonical-state writer per project at a time, consistent with the framework protocol.
- Independent read-only source collection may run in parallel only when the boundaries are explicit and outputs remain isolated.
- Do not let QA modify the research artifact. If a finding is accepted, assign a separate correction task and then re-audit the saved revision.
- Do not cascade an unverified result into later agents as if it were established fact. Preserve its evidence classification.
- A prompt-level prohibition is not runtime enforcement. Restrict tools, scopes, credentials, branch access, and network access independently.
- For writes with ambiguous outcomes, inspect the destination before retrying.

## Default failure routing

- **Required source unavailable:** specialist records failure and stops that source run; orchestrator applies only the declared fallback policy.
- **Conflicting evidence:** preserve both results and route to a resolver/reviewer; never average or choose silently.
- **Missing approval:** stop before the consequential action and provide the exact proposed action, effect, risk, and rollback.
- **Stale/invalid state:** stop dependent execution and request refresh or repair.
- **Agent unavailable:** continue only if its role is optional under acceptance criteria; otherwise mark blocked/partial.
- **Timeout:** preserve completed work, inspect any external write destination, record unfinished checks, and return a resumable handoff.
