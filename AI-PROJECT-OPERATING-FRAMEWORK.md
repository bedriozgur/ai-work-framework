# AI Project Operating Framework

**Status:** Draft v0.1

## Objective
Create a durable project harness allowing different AI models and execution agents to work from the same verified state, use appropriate tools, validate work, and leave a clean handoff.

> **Read state → understand task → inspect evidence → choose a bounded action → execute → verify → persist → hand off.**

Conversation history is useful context but is not the authoritative store for important project state.

## Architecture
### Decision authority
The human defines objectives, constraints, priorities, and approval boundaries and remains the authority for consequential actions.

### Reasoning and review plane
ChatGPT, Claude, and other reasoning models perform planning, analysis, diagnosis, architecture, challenge, comparison, and review. Models may disagree about conclusions; they should not disagree merely because they received stale or different project state.

### Execution plane
OpenClaw, Codex, Claude Code, scripts, automation, scheduled workflows, and MCP-connected agents collect data, run repeatable analysis, create artifacts, validate results, and update approved project state.

### Evidence and integration plane
MCPs, APIs, CLIs, vendor documentation, logs, support bundles, exports, GitHub, Drive/Dropbox, and specialist data providers are evidence sources and action interfaces. A configured primary source must not be silently replaced by a weaker source.

### Durable state
Important facts, decisions, procedures, evidence, and progress must survive model changes, new chats, agent restarts, machine changes, and context-window limits.

## Project profiles
### Lightweight
Use for bounded or moderately complex projects:
- `PROJECT.md`
- `STATE.md`
- `PROGRESS.md`

### Full
Use for recurring, consequential, multi-agent, or automation-heavy projects:
- `PROJECT.md`
- `RULES.md`
- `STATE.md`
- `TASKS.md`
- `PROGRESS.md`
- `DECISIONS.md`
- `CHECKS.md`

Add `sources/`, `outputs/`, and `logs/` only when useful.

## File responsibilities
**PROJECT.md** — objective, scope, architecture, constraints, deliverables, terminology.

**RULES.md** — durable operating rules, source precedence, permissions, prohibited actions, validation requirements, conventions.

**STATE.md** — current verified state. Historical observations must be distinguishable from current facts.

**TASKS.md** — pending work, priority, dependencies, blockers, acceptance conditions.

**PROGRESS.md** — chronological operational record: work performed, results, failed attempts, verification, and next concrete action.

**DECISIONS.md** — material decisions, evidence, alternatives, rationale, date, and revisit conditions.

**CHECKS.md** — observable completion criteria. A task is not complete merely because an agent produced text.

## Standard execution loop
1. **Load context.** Read project definition, rules, current state, task, recent progress, and referenced evidence.
2. **Establish baseline.** Capture current condition before changing it when practical.
3. **Select one bounded action.** Prefer the smallest action that materially advances the task.
4. **Execute.** Use designated tools and sources; record material retrieval failures.
5. **Verify.** Run relevant checks. Use a distinct review pass where consequence or ambiguity warrants it.
6. **Correct.** Fix failures rather than weakening acceptance criteria.
7. **Persist.** Save useful output, verified state changes, material decisions, progress, and blockers.
8. **Hand off.** Leave enough information for another agent or future session to resume immediately.

## Permissions
Normally autonomous, subject to project rules: reading, evidence collection, analysis, non-destructive queries, working artifacts, validation, and approved project-file updates.

Normally approval-gated: deletion, production changes, production restarts, external publication/communication, purchases, financial trades, and irreversible actions.

Project-specific rules override defaults.

## Source discipline
For important data categories define:
1. preferred source;
2. acceptable fallback;
3. freshness requirement;
4. validation rule;
5. behavior when unavailable.

Never fabricate a successful collection. Identify material fallbacks explicitly.

## Review
Separate generation from verification when cost or risk justifies it. Review should test evidence and acceptance criteria, not merely whether output looks plausible.

## Completion contract
Completion reports state output/location, checks performed, passes/failures, sources actually used, unresolved uncertainty, blockers, and next action when incomplete. Partial completion is preferable to unsupported success.

## Handoff contract
Record:
- **TASK** — requested work.
- **CONSTRAINTS** — active rules and limitations.
- **OUTPUTS** — exact saved artifacts/paths.
- **COMPLETED** — verified work.
- **DECISIONS** — material choices and evidence.
- **OPEN ISSUES** — failures, uncertainty, blockers.
- **NEXT ACTION** — one concrete resumable step.

On resumption, inspect referenced artifacts rather than relying only on the summary.

## Storage strategy
This repository stores reusable methodology, templates, and patterns. It must not become a central store for every project's live state.

Each project keeps project-specific state in its own repository or controlled workspace. Large binaries, raw logs, and sensitive evidence may live outside Git with stable references and metadata where appropriate. Customer-sensitive information requires project-appropriate access controls.

## Adoption
1. Finalize the framework.
2. Create reusable templates and patterns.
3. Pilot on two materially different projects.
4. Measure useful discipline versus bureaucracy.
5. Simplify.
6. Adopt for new substantial projects.
7. Migrate existing projects when they become active or benefit warrants it.

## Design principles
- Durable state beats conversational memory for project truth.
- Evidence beats unsupported assertions.
- Separate verified current state from historical observations.
- Prefer bounded actions and observable results.
- Preserve successful work.
- Record failed approaches when doing so prevents repetition.
- Never weaken checks merely to obtain a pass.
- Use deeper review where ambiguity or consequence warrants it.
- Keep procedures reusable and project facts local.
- Prefer simple structures over framework complexity.
- Make models replaceable rather than making the system depend on one model.
- Improve evaluation and execution loops before making prompts progressively larger.

## Open design decisions
- framework versioning and upgrade policy;
- exact criteria for lightweight versus full profile;
- handling customer-sensitive evidence;
- GitHub versus Drive/Dropbox boundaries;
- how OpenClaw discovers and loads project harnesses;
- how reasoning models receive canonical state;
- which checks should be automated;
- how templates evolve without overwriting project-specific rules.
