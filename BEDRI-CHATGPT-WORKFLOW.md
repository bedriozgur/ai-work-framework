# Bedri’s ChatGPT Workflows

**Purpose:** A detailed handoff describing how Bedri uses ChatGPT, how he expects work to be done, and how ChatGPT fits into his broader AI and trading setup.  
**Prepared:** 10 October 2026  
**Status:** Working reference; update when systems, holdings, or operating rules change.

## 1. How to use this document

This is intended to help another assistant (including Claude) continue work with Bedri without treating ChatGPT as the entire system. It records the working methods and known facts available from prior conversations. It is not a complete export of every ChatGPT conversation, nor a substitute for the current source files in the relevant repositories. If a current repo or document conflicts with this handoff, inspect the current source and identify the discrepancy before acting.

The highest-value operating rule is: **preserve the evidence trail, state uncertainty, and finish the requested work.** Bedri expects the assistant to investigate and act on authorized tasks, not simply acknowledge them or repeatedly ask whether to proceed.

## 2. User and communication profile

- **Name:** Bedri Özgür.
- **Role:** Engineer and company leader; works across infrastructure, cybersecurity, cloud, storage, virtualization, and operations.
- **Default response language:** English unless Bedri requests Turkish or the material is for a Turkish audience. Use Turkish when specifically requested.
- **Style:** Direct, concise, evidence-based, and technically precise. Avoid filler and automatic agreement.
- **Reasoning:** Separate observed facts from assumptions, interpretations, recommendations, and forecasts. Point out missing data, risks, trade-offs, and failure modes when they can affect the decision.
- **Corrections:** If Bedri says a fact is wrong or a step was missed, treat that as a request to fix the work. Recheck the evidence and correct the artifact or workflow; do not stop at apologizing.
- **Work cadence:** Provide useful progress updates during long tasks. Ask only for information that materially changes the result. Continue independent work while waiting for an answer.
- **Deliverables:** Often wants complete, reusable files (Markdown, Word, spreadsheets, technical packs) that can be pasted into a company template, committed to Git, or handed to another AI. For standalone requested text, provide the full draft in a useful format.

## 3. What Bedri uses ChatGPT for

ChatGPT is a working partner across several areas, rather than just a general question-answering tool:

1. **Trading research and MIDAS portfolio operations**: market scans, portfolio reviews, watchlist assessments, technical indicators, stop-loss analysis, source comparisons, and written decision records.
2. **AI workflow and agent design**: architecture, prompts, operating rules, handoffs, reviews, and troubleshooting for OpenClaw, n8n, MCP integrations, and multi-model workflows.
3. **Enterprise IT engineering**: VMware/VCF, storage, backup/DR, Microsoft infrastructure, endpoint/security, networking, NAC, and vendor support cases.
4. **Customer project work**: discovery, technical assessments, remediation plans, scope clarification, customer-facing documents, and internal engineering notes.
5. **Research and decision support**: product comparisons, technical compatibility, purchasing, travel, and personal research. Browse for facts that can change, product recommendations involving substantial time/money, niche claims, current pricing, and high-stakes topics.
6. **Document production and editing**: detailed reports, email drafts, meeting packs, Markdown source-of-truth files, and implementation handoffs.
7. **Personal and family research**: genealogy and records research, with careful handling of spelling variants, place names, and the limits of available evidence.

## 4. Work with ChatGPT as a collaborator

### 4.1 Expected behavior

- Infer the intended task from short instructions and surrounding context; Bedri often uses brief steering such as “do it,” “continue,” or “let’s make sure.”
- When an action is clearly authorized, complete it and provide a reviewable result. Do not end with a plan when the user asked for the work itself.
- Use the available data sources and tools that are actually connected. Do not claim that a connector is unavailable merely because it is not visible in a different interface or conversation; verify the current environment first.
- Do not silently substitute one data source for another when the task requires source independence.
- Preserve requested scope. Examples: do not change MIDAS files when explicitly told not to; do not place trades when the task requests analysis only; do not send external communications without explicit authorization.
- Make assumptions explicit when the answer depends on them. If there are two plausible readings, state the one used and briefly distinguish the alternative.
- When asked for a file, produce a real file and make it available. For project artifacts, keep the content in Markdown where it belongs in the repository; do not create a duplicate local-only version of a Git-backed project file unless requested.

### 4.2 Research and citations

- Verify current or unstable information with authoritative sources. Prefer official vendor documentation for technical product behavior and primary sources for research claims.
- For technical recommendations, distinguish vendor-supported configurations from community practice or inference.
- For trading, record timestamps, ticker/exchange, time zone, data frequency, price adjustment assumptions, source, calculation method, and data errors or gaps.
- Cite claims near the statement they support when web research is used. Never invent a source, citation, quote, or tool result.
- For public claims about investments, separate facts, calculations, and judgment. Do not present a forecast as a fact.

### 4.3 Change control and implementation

- Treat repository files, committed strategy rules, customer documents, and persistent workflow configuration as source-of-truth artifacts.
- Before changing a persistent trading rule, verify whether it is already approved and whether current instructions authorize the edit. Record the change in the appropriate decision log or versioned file.
- Do not place orders or make account changes unless explicitly directed and the capability is available. Research and simulated calculations are not trade authorization.
- For customer infrastructure, record current state, desired state, dependencies, owner, and required customer approval. Do not represent a proposed change as completed.
- Validate deliverables enough to catch concrete errors. Avoid unnecessary tests that merely mirror the implementation.

## 5. Trading and MIDAS: purpose and process

### 5.1 Purpose

MIDAS is Bedri’s structured US equity portfolio and research process. The account began a challenge period on **15 June 2026**. A prior recorded comparison showed approximately **+6.19%** account return against **+3.26%** for the S&P 500 at the snapshot date in the project history. These are historical values, not current performance; recalculate from broker records before using them.

The process is designed to support disciplined research and decisions, not automatic execution. Bedri explicitly stated **no auto-trading initially**. Any future automation must retain a human approval gate unless that policy is deliberately changed.

### 5.2 Operating schedule and stages

The recorded MIDAS schedule is in **Türkiye time (Europe/Istanbul)**:

| Stage | Recorded time | Purpose |
|---|---:|---|
| Discovery | 15:00 | Identify candidates and fresh evidence before the US session. |
| Pre-open | 16:20 | Review candidates, holdings, catalysts, and preparation. |
| Post-open | 18:00 | Reassess after the market opens and update evidence/status. |

These times are schedule records, not a guarantee that a run occurred. US daylight-saving shifts, exchange holidays, early closes, and Türkiye/US clock changes can move the relationship between local time and the US session. Verify the calendar and actual run log each day. The project has specifically tracked the autumn 2026 US/UK DST mismatch period.

### 5.3 Evidence sources

The MIDAS source set recorded in prior work includes:

- **TradingView MCP:** screeners and market data; OAuth was authorized in OpenClaw. Six recorded screener presets: `relative_strength`, `breakout_with_volume`, `pullback_with_reversal`, `oversold_healthy`, `earnings_runup`, and `new_highs`.
- **Alpha Vantage MCP:** market data and OHLCV; OAuth was authorized in OpenClaw with read scope. It has been used for daily OHLCV retrieval and independent indicator calculations.
- **SEC EDGAR structured data:** filings and company-reported information.
- **FRED:** macroeconomic data.
- **StockAnalysis:** financial data and company metrics.
- **Finviz:** discovery only, not sufficient as final evidence.
- **OpenInsider (trial):** insider transaction discovery; verify against filings when material.
- Other discovery/context sources recorded: AskLivermore, IBD, TrendSpider, TradingView, Yahoo Trending, and Reddit. Treat social and promotional material as leads, not verification.

The exact present status of credentials, access, rate limits, endpoints, and connector permissions must be checked at runtime. Past authorization does not prove a connection currently works.

### 5.4 Source independence rule for technical analysis

When asked to compare TradingView and Alpha Vantage:

1. Run TradingView collection and analysis using TradingView data only.
2. Separately run Alpha Vantage collection and analysis using Alpha Vantage data only.
3. Record source, timestamp, interval, OHLCV values or reproducible references, indicator method, and errors independently.
4. Do not fill a missing value from the other provider. Do not use one provider to validate the other before both runs are complete.
5. Compare results only after both analyses finish.
6. On HTTP 429, use bounded retries with backoff and report the retry/error history. Do not retry indefinitely or silently switch sources.
7. Do not place trades or update GitHub files unless separately requested.

For indicator calculations, state the formula and warm-up/seed method. For example, an EMA of length *N* commonly uses smoothing factor `2/(N+1)`; the initial seed choice (SMA or another seed) changes early values and should be stated. ATR implementation, price-adjustment convention, and candle session also matter.

### 5.5 Stop-loss framework

A previously recorded framework distinguishes:

- **SL1:** an intermediate risk/profit-management trigger based on evidence such as EMA20/EMA50 deterioration, an ATR-normalized pullback, or loss of a recent swing-low structure.
- **SL2:** a deeper thesis-defense trigger based on a larger trend break, such as EMA200 deterioration or loss of a major higher-low sequence.
- **Residual:** any retained remainder is governed by the approved plan and thesis; it is not an implicit instruction to hold indefinitely.

The exact levels for each holding must be treated as **unapproved unless located in the current authoritative strategy file or explicitly approved in chat**. Prior work recorded that permanent SL1/SL2 values for LLY, MSFT, NVDA, and MU were still outstanding at one point. Recalculate using fresh data and the approved method; do not present old levels as current. Be especially alert to earnings gaps and overnight/event risk (MU earnings on 30 September 2026 had been flagged).

A stop trigger computed from daily closing data is not equivalent to a guaranteed executable price. Gaps, halts, extended-hours trading, spread, and order type create slippage risk. Distinguish an analytical trigger from an actual broker order.

### 5.6 Portfolio and watchlist state

Portfolio snapshots in history are time-specific and can become stale. One recorded late-September snapshot included LLY, MSFT, NVDA, MU, NOW, SPCX, LITE, CI, PLTR, VRT, and GOOGL. Recorded subsequent actions on 30 September: sold 2 CI at $273.22 and bought 2 GOOG at $248.68; cash after those trades was recorded as $181. This does not establish the current portfolio. Verify with the latest MIDAS portfolio source or broker record before analysis.

Watchlist/discovery examples from recent work include AMAT and Accenture as possible candidates, and reviewed names such as HAE, HUM, VEEV, ORCL, NBIS, TSM, and SNDK. These mentions are historical context only: they do not establish current shortlist/longlist status. Always retrieve the current lists from the MIDAS repository before producing a live list or scan.

Bedri has previously requested:

- A current list of holdings and share counts.
- Current shortlist, longlist, and other tracked names.
- Pre-open and post-open reviews.
- Review of every portfolio holding using TradingView MCP.
- Supertrend checks across watchlist names.
- Stop-loss analysis across selected holdings.
- Comparison against benchmarks and independent QA of portfolio reports.

For every report, label the **as-of date/time**. Keep discovery candidates separate from approved holdings and from recommendations. Never assume a stock is still held because it appeared in an old conversation.

### 5.7 Report and QA discipline

A MIDAS report should ideally include:

1. Run ID and as-of timestamp in Europe/Istanbul, plus market session/date.
2. Portfolio holdings, quantities, cost basis/cash only if sourced and current.
3. Benchmark comparison with exact period and formula.
4. Per-holding price, daily move, YTD, distance from 52-week high, and moving averages only when supported by source data.
5. Candidate/watchlist findings with setup, evidence, catalyst, invalidation, and status.
6. Source table identifying provider, collection timestamp, and any failed query or missing values.
7. Calculations and assumptions, especially adjusted/unadjusted prices and indicator seeds.
8. Decision log: what changed, what was considered, what was not decided, and why.
9. QA notes for independent recomputation and discrepancies.
10. Clear statement that no trades were placed unless execution was explicitly authorized and confirmed.

Bedri has asked for independent audit work where a second reviewer recomputes report values from raw JSON, without editing the original researcher’s report. Preserve that separation when requested.

## 6. AI and trading automation architecture

### 6.1 Known architecture

Bedri has been building an always-on AI terminal/workflow for trading and other recurring tasks. The recorded environment includes:

- **Ubuntu VM `clawhost`:** OpenClaw Gateway and n8n/Docker work.
- **Windows 11 VM `aihost`:** a Windows worker/node for Windows-specific tools and remote access. Later architecture notes define `clawhost` as the sole OpenClaw Gateway and `aihost` as a remote node; verify current installation before acting.
- Planned static IPs recorded as `192.168.77.81` for `clawhost` and `192.168.77.80` for `aihost`; verify current configuration before use.
- Time zone set to **Europe/Istanbul**.
- OpenClaw Gateway ran as a user service, enabled at boot with linger enabled at a recorded check. This status can change; verify before relying on automatic restart.
- n8n ran in Docker on port 5678 in the prior setup. Current version and container state must be checked before instructions.
- TradingView and Alpha Vantage MCP integrations were configured in OpenClaw. They are infrastructure-level integrations, not automatically shared with every ChatGPT or Claude chat.
- Other tools in the recorded environment include DeepSeek V4 Pro, Gemini, Kimi, SearXNG, and an n8n sandbox. Their current configurations must be verified.
- GitHub is the accepted canonical control/state plane. Google Drive is the standard evidence/artifact/interchange plane. Dropbox appeared in early setup notes but is not part of the accepted standard framework architecture. Telegram notifications are part of the workflow design.

### 6.2 Roles and boundaries

The intended design is a team of specialist agents with a gatekeeper/orchestrator that schedules and controls work. The agent team is for research and operations support; it is not authorization to trade. Keep separate roles and source permissions where independent analysis is required.

Known framework artifacts include:

- `AI-WS01-ARCHITECTURE-v0.3.md`
- `CLAUDE-REVIEW-PROMPT-v0.3.md`
- `AI-PROJECT-OPERATING-FRAMEWORK.md`
- `AGENT-OPERATING-PROTOCOL.md`
- `BOOTSTRAP.md`
- `framework.yaml`
- `VERSIONING.md`
- `DECISIONS.md`

The framework repository is `bedriozgur/ai-work-framework`; MIDAS data/code is in separate repositories, including `midas-portfolio` and the evolving market-data/tooling repositories. Check the current repository list, permissions, default branch, and source paths before editing. Repository visibility and Claude's access can differ by account and connection; verify rather than assume.

### 6.3 Gatekeeper operating decisions already recorded

Prior framework decisions include:

- A Python scheduler/gatekeeper.
- Explicit states such as `NO_JOB_DUE`, `CALENDAR_ERROR`, and `STALE`.
- Decision statuses `WAIVED` and `SUPERSEDED`.
- A `RUN_LATE` policy and a defined health-check window.
- SQLite with WAL mode.
- Telegram fallback notifications.
- A two-week manual baseline log.
- Separate tags for recurring operations versus one-off projects.

Treat these as previously decided design points, not proof of completed or currently deployed functionality. Read the current framework files and runtime state before claiming an implementation is live.

## 7. ChatGPT versus the external system

A crucial distinction for any migration to Claude Pro or another model:

| Capability/context | Where it lives | Migration implication |
|---|---|---|
| ChatGPT conversation history and ChatGPT memory | ChatGPT account | Does not become Claude conversation history automatically. Export or summarize important context. |
| ChatGPT custom GPTs, projects, files, or scheduled features | ChatGPT account/service | Service-specific configuration; recreate or port instructions manually where possible. |
| OpenClaw gateway, n8n workflows, local scripts, MCP config | Bedri’s VM/repositories | Independent of ChatGPT subscription, but a new model endpoint/client may require separate configuration. |
| TradingView and Alpha Vantage OAuth inside OpenClaw | OpenClaw integration | Not automatically inherited by a ChatGPT or Claude native connector. Verify auth scopes and access path. |
| MIDAS holdings, strategy, reports, JSON, decision logs | MIDAS repo and data sources | Repository artifacts are the durable operating source; keep them model-neutral where practical. |
| AI framework prompts/protocols | `ai-work-framework` | Keep portable, versioned Markdown. Do not rely only on a conversation’s memory. |
| Large/binary evidence and deliverables | Google Drive under the accepted framework storage decision | Link from canonical GitHub state with stable object/version references; apply project security rules. |

When preparing a new assistant, provide the current framework and MIDAS source files, not only this document. This handoff gives the operating context; the current repo supplies the authoritative detail.

## 8. Enterprise engineering and customer work

Bedri regularly uses ChatGPT to analyze customer environments, produce engineering plans, and draft customer/vendor communications. Project-specific facts should be verified against the latest inventory and meeting notes; historical context here is not a substitute for them.

### 8.1 Typical process

1. Establish actual state from inventories, screenshots, logs, contracts, and customer statements.
2. Separate verified observations from estimates, hypotheses, and unknowns.
3. Identify operational and security risks, dependencies, and unsupported configurations.
4. Define phased remediation, owners, prerequisites, approval points, and validation evidence.
5. Prepare separate internal and customer-facing documents when needed. Customer-facing text should avoid internal speculation and should use diplomatic, precise language.
6. Draft vendor support requests with concise scope and exact model/service tags when Bedri asks for a short case description.
7. Preserve decisions and open questions in the project record.

### 8.2 Common technical domains and project context

Recorded work spans Active Directory/Exchange/M365, VMware/vCenter/ESXi/VCF, Dell PowerStore/Unity/Data Domain, Veeam and PPDM, Fortinet/Sophos/Check Point, Trend Micro/Trellix, Aruba, NAC, SIEM/SOC/EDR, and disaster recovery.

Selected project context in the history includes:

- **HL Company:** SSE, SIEM/SOC, and EDR planning; revised go-live target April 2027, assessment expected January 2027. Authentication design involved GlobalProtect/Prisma Browser with Azure Entra ID and Hanmaru. Do not treat future dates as current status without checking project updates.
- **Enza Zaden:** NDA negotiations ended with Bedri declining the current form; the concern centered on Article 12 indemnity scope and uncapped liability for breach. Do not imply agreement was reached.
- **Cimtaş:** Exchange 2019 with roughly 1,000 mailboxes, archive at another WAN site, retention groups, and performance troubleshooting; a wildcard certificate renewal was completed in October 2026, valid to April 2027 as recorded.
- **Brusa Koltuk Sistemleri:** security/infrastructure review covering old domain controllers, VMware 6.7, backup/storage health, endpoint coverage, Microsoft 365 admin controls and MFA, and remediation actions. Customer approvals are required for access/security changes.
- **AKA Otomotiv:** VMware, PowerStore, Veeam/QNAP, DR array, endpoint licensing, Fortinet, and SOC remediation; work phases and commercial terms have been discussed. Verify current remediation status and scope.
- **Coşkunöz:** multi-site VMware and storage planning, vCenter/ESXi compatibility, backup and RecoverPoint dependencies, and international sites. Verify the current design matrix before making compatibility claims.

These notes are pointers to prior work. Do not copy them into a new report as current facts without checking the latest documents.

## 9. Preferred deliverable structure

### 9.1 Trading research report

- Title and as-of timestamp.
- Executive finding in plain language.
- Data/source table.
- Holdings or candidates table with units and formulas clear.
- Evidence per name and invalidation conditions.
- Assumptions, missing data, and failed requests.
- Decision status (research only / decision pending / approved / executed).
- Appendix with calculation method or raw-data references where needed.

### 9.2 Customer technical document

- Scope and purpose.
- Confirmed current environment.
- Findings with evidence and impact.
- Proposed phases, prerequisites, dependencies, and owner.
- Customer decisions/approvals required.
- Validation and acceptance criteria.
- Explicit exclusions and open questions.

Separate internal notes from customer-facing content. Do not make customer approval or vendor support claims that have not been received.

### 9.3 Handoff to another AI

A useful handoff should state:

- What the goal is and what is out of scope.
- Which source files/repositories are authoritative.
- Current verified state and as-of date.
- Exact tools/connectors available and any access limitations.
- Decisions already made versus pending decisions.
- Required source independence, retry, and no-execution rules.
- The immediate next task and completion criteria.

## 10. Common failure modes to avoid

1. **Stale memory:** repeating an old holding, stop, device state, project date, or version as if current.
2. **False tool claims:** saying an MCP is absent without checking the actual environment; or claiming a past connection works now without testing.
3. **Source substitution:** mixing providers in an independent analysis, especially when one fails or returns a rate limit.
4. **Unmarked calculations:** giving technical values without timestamp, interval, formula, seed, adjustment basis, or source.
5. **Recommendation creep:** turning a scan or research result into a buy/sell instruction without request and evidence.
6. **Execution ambiguity:** failing to distinguish an analytical trigger from an actual broker stop order or trade.
7. **Unapproved persistent changes:** editing strategy, portfolio files, schedules, or production/customer configurations without clear authorization.
8. **Incomplete deliverables:** offering a plan, partial answer, or “would you like me to…” when the user has already instructed the work.
9. **Overstating implementation:** describing designed features as deployed, or a successful sample workflow as production-ready.
10. **Loss of provenance:** failing to record source, run time, errors, and how a conclusion was reached.

## 11. Practical start-of-session checklist

Before doing substantial work:

- Identify whether the task is about MIDAS, the AI framework, a customer project, or general research.
- Determine whether current files or live data are needed; prefer the current repo/project record over old chat context.
- Confirm the relevant date/time zone and current source access.
- Check whether the user authorized research only, a file edit, or an external action.
- Preserve source separation if requested.
- Work through to a reviewable result and report exactly what changed, what was verified, and what remains uncertain.

## 12. Short operating summary

Bedri uses ChatGPT as an evidence-driven engineering and trading research collaborator. For MIDAS, the process is scheduled, source-aware, and explicitly human-gated; TradingView and Alpha Vantage analyses may need to remain fully independent. OpenClaw and n8n are separate infrastructure hosted on VMs, and their integrations do not automatically transfer between ChatGPT and Claude. The durable strategy and operating rules belong in versioned Markdown and repository files. Always verify current state, distinguish evidence from inference, avoid unauthorized execution, and complete the requested work rather than stopping at a proposal.


## 13. Detailed explanation of Bedri's work and how he uses ChatGPT

This section explains the working patterns behind the domains above. It is meant to help a new model or agent understand the task flow and handoff style, not to replace the current project repository or to expose credentials. Durable project facts must be checked against current project state.

### 13.1 How ChatGPT fits into the overall toolchain

Bedri wants continuity across ChatGPT, Claude, Codex, OpenClaw, n8n, and other models, with the ability to move work between them. He uses ChatGPT for reasoning, technical investigation, prompt and workflow design, comparison, review, and complete deliverables. The always-on execution system is separate: OpenClaw is the agent gateway on the Ubuntu host; n8n/Python can provide deterministic scheduling, data handling, and repeatable calculations; Codex or another coding environment can implement and test code; GitHub contains canonical project/framework state. A provider subscription does not itself grant access to VM-hosted MCPs or repository credentials.

The standard framework storage decision is GitHub for versioned control state and Google Drive for large/binary source evidence, artifacts, and cross-agent handoffs. Dropbox was used in an earlier prototype but is not the framework's default. Do not create competing copies or assume a model can access a private repository, Drive folder, or MCP without verifying its current permissions.

### 13.2 MIDAS: portfolio research, not automatic execution

MIDAS is Bedri's ongoing US-equity research and portfolio process. Its purpose is to create repeatable, evidence-backed decision preparation. It does **not** place broker orders or route trades. Human review remains between research output and any portfolio action.

A normal cycle is:

1. **Establish the current baseline:** inspect the current holdings/cash, watchlist categories, decisions, strategy rules, pending actions, prior report, and market calendar from authoritative MIDAS files or broker-origin evidence. Historical chat snapshots are not live truth.
2. **Run Discovery:** use configured screeners and discovery sources to find candidates. Discovery data is only a lead until validated under the MIDAS source policy. Maintain exact status: discovery, shortlist, longlist, holding, removed, or unknown.
3. **Prepare Pre-open:** validate the candidates and existing holdings against current prices, liquidity/volume, trend, catalysts, earnings dates, relevant filings, and portfolio rules. Identify what evidence is missing before making a conclusion.
4. **Review Post-open:** check how price/volume behavior changed after the session opened, label the market/session timestamp, and distinguish an intraday observation from a confirmed daily close.
5. **Build the report:** state ticker/exchange, as-of time, sources, data freshness, formulas, assumptions, errors, trigger/invalidations, decision status, and exact next action. Preserve report and raw inputs in MIDAS's canonical project structure.
6. **Review decisions:** Bedri decides whether research merits a portfolio action. The agent may prepare evidence and scenarios but does not execute the order.

The recorded stage times are Discovery 15:00, Pre-open 16:20, and Post-open 18:00 Europe/Istanbul. These must be rechecked against current exchange calendars, local timezone, US/Türkiye daylight-saving differences, and the current scheduler before automation. The times alone do not prove a job ran.

### 13.3 Market data and technical risk workflow

TradingView and Alpha Vantage are available through OpenClaw in the historical setup, but each invocation must verify that its connector and token scope currently work. When Bedri requests a comparison, the analysis must be independent:

- TradingView collects and calculates from TradingView only.
- Alpha Vantage collects and calculates from Alpha Vantage only.
- A bounded 429 retry/backoff policy is used and errors are recorded.
- No data, indicator values, assumptions, or missing-bar repairs cross between the two runs until both terminate.
- Differences are compared only after results are frozen, and are explained rather than averaged away.

Technical work includes OHLCV validation; EMA20/50/200; ATR14; Supertrend; recent swing highs/lows; relative strength; volume context; and proposed SL1/SL2 risk zones. Each calculation records interval/session, adjustment basis, formula, seed/initialization, lookback, units, and source. SL1/SL2 are not persistent approved levels unless the current strategy record or explicit decision says so. A close-based trigger is not a guaranteed fill price; gaps and execution conditions matter.

### 13.4 Company and catalyst research

For individual holdings or candidates, Bedri needs the price/technical evidence paired with issuer facts: SEC filings, earnings releases, balance sheet, cash flow, margins, dilution, management guidance, upcoming earnings, material company events, and negative evidence. The analyst must identify report period, filing/release date, accession or stable document reference, currency, and whether a number is reported, estimated, or calculated. Social media, chart commentary, and screeners can identify a lead but do not verify an issuer claim. The resulting bullish or bearish interpretation is explicitly marked as analysis, not fact.

### 13.5 PRT research and quantitative development

Prior discussions refer to “PRT work” but do not establish what PRT expands to. Preserve the term and ask only if expansion is necessary. The recorded workflow is research/development: Bedri or ChatGPT frames a hypothesis; a coding agent (for example, Codex) implements or changes code; Python/OpenClaw runs deterministic experiments, backtests, parameter sweeps, and statistics; results are compared with baselines and reviewed; Bedri interprets the evidence. The process should record commit, dataset lineage, versions, seeds, signal timing, fill/cost assumptions, train/test split, benchmark, and failure cases. A backtest or paper signal is not evidence of future profits and does not authorize live strategy execution.

### 13.6 AI platform and automation engineering

Bedri is building an always-on agent system mainly for MIDAS and research engineering, while using the same framework for other work. Recorded architecture: Ubuntu `clawhost` is the sole OpenClaw Gateway; Windows `aihost` is a connected worker/node rather than a second local Gateway. Earlier records identify planned addresses `192.168.77.81` and `192.168.77.80`; verify current addressing and service configuration. The Windows node's initially approved capabilities were limited to command/tool lookup and execution, device/status information, screen snapshot, and notification; camera, microphone, location, and recording were deferred. Check actual node permissions before every sensitive action.

OpenClaw handles agent sessions and MCP/tool access. n8n is used for deterministic workflow orchestration and authenticated callbacks; Python is preferred for transparent calculations and stateful logic. Past checkpoints recorded n8n 2.42.4, n8n Sandbox 1.3.4, SearXNG, and DeepSeek on `clawhost`; these are historical, not guaranteed current versions. A typical n8n → OpenClaw → n8n path needs a correlation ID, authenticated Gateway call, bounded timeout/retry, callback validation, terminal status, and inspectable logs. Do not alter MIDAS while troubleshooting unrelated infrastructure unless expressly asked.

The framework's gatekeeper design records explicit states such as `NO_JOB_DUE`, `CALENDAR_ERROR`, and `STALE`, a `RUN_LATE` policy, a health-check window, SQLite WAL state, Telegram fallback notifications, a two-week manual baseline, and separate recurring-operation vs one-off-project tags. These are design decisions recorded in files; verify what is actually implemented.

### 13.7 Enterprise and customer engineering

Bedri uses ChatGPT to troubleshoot customer environments and turn fragmented information—screenshots, logs, exports, inventories, email text, and verbal reports—into precise engineering actions. The expected process is:

1. Confirm scope, current configuration, versions, site/topology, business purpose, and who owns the decision.
2. Build an evidence-backed inventory and label each statement as verified, observed, reported, inferred, assumed, stale, or unknown.
3. Identify risk and explain the technical impact without overstating it. Vendor support and lifecycle statements should use current vendor sources.
4. Separate immediate containment, prerequisites, phased remediation, validation, rollback, owner, outage/change window, and customer approval.
5. Prepare separate internal and customer-facing versions when required. Internal notes can retain uncertainty; external text should be concise, diplomatic, and explicit about confirmed versus open points.
6. For vendor SRs, Bedri often wants a short, specific question with exact model/service tags and the technical scope, rather than a long narrative.
7. Preserve approved decisions and unresolved customer questions in the project record. Never report a remediation as done merely because it was proposed.

Recurring domains include Microsoft/AD/Exchange/M365, VMware/ESXi/vCenter/VCF, Dell PowerStore/Unity/Data Domain/Connectrix, Veeam/PPDM, network/security/NAC, endpoint controls, SOC/SIEM/EDR, and DR design/testing. Customer-specific repositories and current inventories remain authoritative.

### 13.8 Research, purchases, genealogy, and everyday troubleshooting

For current technical compatibility, products, prices, laws, standards, schedules, or purchases, research the current market and relevant official sources; specify region, exact model/version, price date, warranty, and assumptions. For high-cost choices, compare actual configurations and total trade-offs, not just brand names or promotional benchmark claims. For genealogy, preserve original scripts and name variants, place-name/administrative changes, source/date, and identity uncertainty; don't merge same-name people without corroboration. For troubleshooting consumer technology, Bedri prefers a diagnostic sequence that isolates the affected service/device and records what has already been tried, avoiding repetition.

### 13.9 How to hand work to Bedri or the next model

A useful brief or final answer gives the result first, then the evidence, exact file path/repository, what changed, what was tested/verified, what remains uncertain, and the concrete next action. For substantial agent work, the brief uses GOAL, SCOPE, CONTEXT, ACCEPTANCE, VERIFY, TIMEBOX, FORBIDDEN, REPORT, and STANDING. An unattended run needs a durable log, bounded work, explicit stop condition, and concise completion report/notification. Keep the user's decision points visible; do not bury them in a long report or ask repeatedly for confirmation already given.

## 14. Expanded persona model

The reusable profiles in `agents/` map onto Bedri's work as follows:

| Persona | When it owns work | Concrete responsibility |
|---|---|---|
| Chief-of-Staff | Cross-domain goal, queue, or multi-agent task | Builds the nine-field brief, chooses smallest team, tracks status and hands off. |
| Infra-Orchestrator | OpenClaw/n8n/MCP/VM/schedule operation | Verifies runtime, routes runs, retries within policy, monitors callback/logs and persists. |
| MIDAS-Trader | Portfolio-centered research request | Reads current MIDAS state, synthesizes technical + fundamental reports, presents decision brief. |
| Market-Data-Collector | A named provider-specific data pull | Retrieves/verifies raw data and provenance; one provider per run. |
| Technical-Risk-Analyst | Price/volume/risk calculation | Computes indicators and proposed zones from one frozen source dataset. |
| Fundamental-Catalyst-Analyst | Issuer research | Verifies filings, earnings, financial evidence, catalyst dates and business risks. |
| Quant-Research-Engineer | PRT or research-code task | Implements controlled experiments/backtests and reports statistical evidence/reproducibility. |
| Enterprise-Architect | Customer IT architecture/assessment | Converts technical evidence into current/desired state, risks, dependencies, plan and approvals. |
| QA-Auditor | Independent second-pass review | Recomputes/checks final artifact, provides separate discrepancy log. |
| Research-Curator | Non-MIDAS general/personal research | Finds sources, compares claims/products/records and explains uncertainty. |

Do not start all ten agents for a routine request. Use one lead and only the additional specialist/reviewer needed. The main reason to split roles is independent evidence and auditable handoffs, not to maximize the number of model calls.

## 15. Short operating summary

Bedri uses ChatGPT as an evidence-driven engineer, research partner, and deliverable co-author across trading, AI orchestration, customer infrastructure, quantitative research, and general decisions. The desired process reads durable state first; gathers source-specific evidence; separates fact from inference; performs bounded work; verifies the final artifact; persists it to the right system; and leaves a useful handoff. MIDAS is research and review-only with no broker execution. OpenClaw/n8n are separate runtime infrastructure; GitHub is canonical control state, Google Drive is the standard evidence/artifact plane, and tool access must be verified in the active environment. Human decisions and approvals remain with Bedri.
