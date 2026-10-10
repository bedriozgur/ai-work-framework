# Agent Workflow Map

This map describes intended role routing; it is not proof that an OpenClaw, n8n, or direct-model workflow is deployed. Runtime tools, credentials, serialization, approval gates, and logs must be verified separately.

## Responsibility model

- **Chief-of-Staff** owns cross-domain intake, task framing, queue visibility, specialist assignment, and final handoff. It does not own specialist technical conclusions.
- **Infra-Orchestrator** owns the AI/automation execution environment: OpenClaw, n8n, MCPs, VM/service state, scheduling, retries, callback handling, and workflow observability.
- **Domain specialists** own bounded evidence work within their profile.
- **QA-Auditor** independently checks a final artifact and returns a separate audit record.
- **Bedri** retains portfolio/capital decisions, customer approvals, and other consequential human decisions.

For a direct request clearly addressed to a specialist, that specialist may lead without a Chief-of-Staff pass. For recurring jobs, Infra-Orchestrator may start the run directly from the authorized schedule and rules.

## Routing table

| Work | Lead | Supporting profiles | Sequence |
|---|---|---|---|
| Daily MIDAS scan/portfolio review | MIDAS-Trader or scheduled Infra-Orchestrator | Market-Data-Collector, Technical-Risk-Analyst, Fundamental-Catalyst-Analyst; QA-Auditor when required | Verify current state/calendar → collect by source → analyze by domain → synthesize → audit → persist and notify |
| TV vs Alpha Vantage independent analysis | MIDAS-Trader or Chief-of-Staff | Two isolated Collector instances; two isolated Technical-Risk-Analyst instances; QA-Auditor | Run A and B independently → freeze both → compare → audit → report |
| PRT research/code/backtest | Chief-of-Staff or direct request | Quant-Research-Engineer; QA-Auditor as warranted | Approved hypothesis/spec → implement/test → baseline and out-of-sample evaluation → independent check → report |
| OpenClaw/n8n/MCP/scheduler or VM issue | Infra-Orchestrator | QA-Auditor for material change | Read-only diagnosis → bounded proposal → approval if needed → authorized change → verify runtime and recovery |
| Customer infrastructure assessment/design | Chief-of-Staff for broad program; otherwise Enterprise-Architect | Research-Curator for vendor evidence; QA-Auditor for consequential findings | Inventory/evidence → classify → design/remediation → customer/internal outputs → review |
| Product, technical, genealogy, or other general research | Research-Curator | QA-Auditor when evidence or consequence warrants | Scope → primary research → compare → synthesize → source list |
| Cross-domain work | Chief-of-Staff | One accountable specialist per separable work package | Brief each package → preserve dependencies/owners → integrate verified results → hand off |

## MIDAS workflow

### A. Scheduled review

1. The scheduler or Infra-Orchestrator determines whether a run is due from the current approved schedule, exchange calendar, local timezone, and holiday/early-close rules. The recorded weekday stage times are Discovery 15:00, Pre-open 16:20, and Post-open 18:00 Europe/Istanbul. Treat these as schedule definitions, not proof of run completion. Do not move them without an authorized project change.
2. Check the US Eastern offset, Europe/Istanbul time, exchange holiday/early-close calendar, and actual expected regular-session open for that date. The US regular session normally opens at 09:30 Eastern. During US daylight time, 16:20 Istanbul is 10 minutes before open and 18:00 is 90 minutes after; during US standard time, 16:20 is 70 minutes before and 18:00 is 30 minutes after. Discovery at 15:00 also shifts relative to open. Report actual minutes-to-open/after-open with each run; if the existing timing no longer fits the operational purpose, propose a schedule change for approval.
2. MIDAS-Trader loads the current portfolio, cash, shortlist/longlist, strategy, open decisions, report schema, and prior run state from the MIDAS project sources.
3. The appropriate collector obtains the configured discovery/price/fundamental evidence. Screening sources remain discovery-only where project rules say so.
4. Technical and fundamental analysts return separate evidence-backed work products. Candidate status remains distinct from holding status and an approved decision.
5. MIDAS-Trader prepares the portfolio-context synthesis and decision candidates. Bedri reviews and decides.
6. QA-Auditor checks material calculations, source and freshness markers, and final report content when required.
7. Authorized artifacts are saved to the MIDAS repository; run state/logs are updated; Telegram or other notifications report status and links, not unsupported conclusions.

### B. Independent provider analysis

1. Assign separate task IDs/run IDs and enforce separate tool allowlists for TradingView and Alpha Vantage.
2. Each Market-Data-Collector retrieves only from its assigned provider and preserves raw evidence.
3. Each Technical-Risk-Analyst uses only its assigned provider's frozen dataset. Do not pass Run A's derived values, missing-data decisions, or assumptions into Run B.
4. Each run independently terminates as complete, partial, blocked, or failed. Bounded 429 retries and errors are recorded.
5. Compare only after both outputs have been frozen. Explain differences; do not average values or select a preferred source silently.
6. QA reviews the comparison and final saved report. A failed provider run stays visible; no provider fills its gaps unless the task's explicit source policy allowed it.
7. No broker integration, order routing, or execution is part of MIDAS.

### C. MIDAS research outputs

Reports should state run/as-of time and timezone; symbols and venue; source and freshness; raw evidence reference; calculations/formulas/seeds/units; errors and gaps; candidate/holding/decision status; limits; verification; and next action. Proposed SL1/SL2 zones are analytical triggers unless separately found in an approved current strategy record. A research report never implies an order was placed.

## PRT research-engineering workflow

“PRT” is preserved as Bedri's term; do not expand the acronym without an authoritative definition.

1. Bedri/assistant records a specific research question or hypothesis and what would falsify it.
2. Quant-Research-Engineer locates the project code, dataset, base commit, and current test/run instructions.
3. Agree on signal timing, fills, costs/slippage, corporate actions, universe/survivorship, train/test periods, benchmark, metrics, and compute/time limits before interpreting results.
4. Implement a bounded experiment in a branch or sandbox; record versions, seeds, commands, and data lineage.
5. Run deterministic tests and a baseline comparison; report out-of-sample results, drawdowns, transaction costs, parameter sensitivity, and failure cases.
6. QA-Auditor independently checks the final commit and material statistics when warranted.
7. Bedri interprets findings and decides whether to continue research. No automation schedules live strategies or places orders.

## AI platform and automation workflow

- Chief-of-Staff converts cross-domain goals into owned packages.
- Infra-Orchestrator verifies actual runtime: host role, Gateway endpoint/auth, n8n connectivity, MCP health/scope, schedule/calendar, callback, timeouts, retry budget, and logs.
- OpenClaw runs configured specialist/tool workflows; n8n handles only the deterministic orchestration functions assigned to it. Do not presume an architecture's implementation state from a plan.
- Python is used for deterministic transforms, indicators, and backtests where a transparent reproducible calculation is preferable to model reasoning.
- GitHub stores canonical framework/project control state. Google Drive is the standard artifact/evidence/interchange plane under the accepted framework decision. Dropbox is not part of the standard framework architecture.
- Telegram carries notifications/fallbacks; messages must reflect verified run status and should not expose secrets or unnecessary evidence.

## Enterprise/customer engineering workflow

1. Chief-of-Staff identifies customer/project, scope, output audience, and authority.
2. Enterprise-Architect inventories evidence and classifies each claim as VERIFIED, OBSERVED, REPORTED, INFERRED, ASSUMED, STALE, or UNKNOWN.
3. It checks vendor support from current primary documentation and records exact model/version/region/configuration. Silence in a compatibility matrix is not automatically a vendor rejection.
4. It creates current-state/desired-state gaps, risk, dependencies, phase, owner, precondition, approval, implementation outline, rollback, and validation.
5. Internal engineering notes and customer-facing proposal are separated when needed.
6. QA checks high-impact findings, calculations, support claims, and final text.
7. A proposed remediation remains a proposal until the customer/Bedri approval and implementation evidence are recorded.

## General research and deliverable workflow

Research-Curator defines scope, researches current primary sources, captures citations and dates, compares conflicting evidence, and returns an answer or document with confidence and gaps. For a report or document, use the appropriate output format and verify the final saved version. Customer communications, purchases, bookings, publication, or sending are separate actions and require explicit authorization.

## Task brief and return envelope

Each assignment carries the nine-field brief:

- **GOAL** — one observable result.
- **SCOPE** — included/excluded work and target artifact.
- **CONTEXT** — project state, sources, revisions, and constraints.
- **ACCEPTANCE** — observable completion conditions.
- **VERIFY** — checks and evidence.
- **TIMEBOX** — deadline, timeout, retry/budget limit.
- **FORBIDDEN** — prohibited sources, tools, writes, or actions.
- **REPORT** — output schema/location and status fields.
- **STANDING** — durable rules and decisions.

Every return contains task/run IDs, status (`COMPLETE`, `PARTIAL`, `BLOCKED`, `FAILED`, `CANCELLED`), inputs/revisions used, actions, output references, sources/tools/timestamps/retries, checks, evidence, assumptions/conflicts, decision requests, and one next action. If the task is unattended, include a run log and concise human-readable completion summary.

## Concurrency and failure rules

- One writer for canonical project state at a time. Independent read-only collection can run concurrently only with explicit data/source isolation.
- QA never edits the research artifact. Create a separate correction task, save a new revision, and re-audit.
- A prompt-level restriction is not enforcement; use runtime tool/credential/network/branch controls.
- Required source unavailable → keep successful work, mark the run partial/blocked, and apply only a declared fallback.
- Conflicting evidence → preserve both claims and route for resolution; never choose silently.
- Missing approval → stop before the side effect and give exact action/effect/risk/rollback.
- Timed-out or ambiguous write → inspect the destination before retry.
- Agent/model unavailable → proceed only if that role is optional under acceptance checks.
- Stop cleanly at limits; persist outputs and leave a resumable next action.
