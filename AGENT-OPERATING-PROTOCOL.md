# Agent Operating Protocol

**Status:** Draft v0.1  
**Applies to:** reasoning models, execution agents, coding agents, scheduled agents, and human-supervised AI workflows.

## 1. Purpose

This protocol defines how an agent enters, executes work in, verifies, persists, and exits a framework-managed project. Project-specific rules take precedence over framework defaults, but may not silently weaken mandatory safety, evidence, or honesty requirements.

## 2. Entry / Boot Protocol

Before substantial work:

1. Locate the project root.
2. Read `project.yaml` when present.
3. Determine framework version and project profile.
4. Read `PROJECT.md`.
5. For Full projects, read `RULES.md`.
6. Read `STATE.md`.
7. Identify the active task from `TASKS.md` or the explicit user request.
8. Read the most recent relevant `PROGRESS.md` entries.
9. Read relevant `DECISIONS.md` entries.
10. Load task-specific `CHECKS.md`.
11. Identify required evidence sources and freshness requirements.
12. Determine whether the intended actions are autonomous or approval-gated.

Do not begin execution if a missing mandatory input makes safe or correct execution impossible. Report the blocker instead.

## 3. Authority Order

When instructions conflict, use this project-level order:

1. applicable platform/system safety and security constraints;
2. explicit current human instruction;
3. project `RULES.md`;
4. accepted project decisions;
5. project `PROJECT.md`;
6. current verified `STATE.md`;
7. active task definition;
8. framework defaults;
9. historical progress/context.

Historical notes never override verified current state.

## 4. State Classification

Agents must distinguish:

- **VERIFIED** — supported by current evidence.
- **OBSERVED** — directly seen but not yet fully validated.
- **REPORTED** — supplied by a person/system but not independently verified.
- **INFERRED** — reasoned from evidence.
- **ASSUMED** — temporarily accepted to proceed.
- **STALE** — previously valid but outside freshness requirements.
- **UNKNOWN** — not established.

Do not promote an item to VERIFIED without appropriate evidence.

## 5. Planning

Before execution, establish:
- requested outcome;
- current baseline;
- constraints;
- required sources;
- approval boundary;
- acceptance checks;
- smallest useful bounded action.

Prefer reversible and non-destructive steps.

## 6. Execution

During execution:
- use designated primary sources;
- identify fallbacks explicitly;
- preserve useful successful work;
- avoid unrelated changes;
- record material failures;
- do not fabricate retrieval, execution, validation, or success;
- stop at approval boundaries.

Where practical, change one material variable at a time during troubleshooting.

## 7. Verification

A generated result is not self-verifying.

Verification may include:
- deterministic tests;
- syntax/configuration validation;
- re-reading saved artifacts;
- comparison with authoritative sources;
- freshness checks;
- before/after comparison;
- independent model/reviewer pass;
- human confirmation where required.

Failed checks must remain failed until corrected or explicitly accepted by the decision authority.

## 8. Persistence

Persist only information worth carrying forward.

Update:
- `STATE.md` for verified current-state changes;
- `PROGRESS.md` for operational history and handoff;
- `DECISIONS.md` for material decisions;
- `TASKS.md` for task status;
- output/evidence references where applicable.

Do not rewrite historical records merely to make the current result look clean.

## 9. Completion States

Every substantial task ends in one of:

- **COMPLETE** — all mandatory acceptance criteria passed.
- **PARTIAL** — useful work completed but one or more required criteria remain.
- **BLOCKED** — execution cannot proceed without missing evidence, access, dependency, or approval.
- **FAILED** — attempted execution did not achieve the required outcome.
- **CANCELLED** — decision authority stopped the task.

Never report COMPLETE merely because an output exists.

## 10. Handoff

A resumable handoff contains:
- TASK
- CONSTRAINTS
- OUTPUTS
- COMPLETED
- VERIFICATION
- DECISIONS
- OPEN ISSUES
- NEXT ACTION

The next agent must inspect authoritative artifacts rather than trusting the handoff summary alone.

## 11. Failure and Fallback Rules

### Source unavailable
Record the failure. Use a fallback only if allowed. Mark the fallback and any confidence impact.

### Stale evidence
Do not present stale data as current. Refresh it or label it.

### Conflicting evidence
Preserve the conflict, compare authority/freshness, attempt resolution, and escalate if material uncertainty remains.

### Validation failure
Correct and re-run. Do not weaken the check merely to obtain a pass.

### Missing project file
For optional files, continue if safe. For mandatory files, either bootstrap them according to the project profile or stop if doing so would require inventing project facts.

### Tool failure
Preserve successful prior steps. Retry only when reasonable. Avoid uncontrolled retry loops.

### Approval required
Stop before the consequential action and present the exact proposed action, expected effect, risk, and rollback where applicable.

## 12. Concurrency

Before writing canonical state:
- check whether relevant state changed since it was loaded;
- avoid blind overwrite;
- reconcile conflicting edits;
- prefer append-only progress/history where practical.

A later timestamp alone does not make one agent's conclusion authoritative.

## 13. Sensitive Information

Do not copy secrets, credentials, tokens, personal data, or customer-sensitive evidence into framework repositories unless explicitly required and permitted.

Prefer references to controlled storage for sensitive or large evidence.

## 14. Review Triggers

Use stronger or independent review when one or more applies:
- production impact;
- destructive/irreversible action;
- financial consequence;
- conflicting evidence;
- low confidence;
- novel architecture;
- large scope;
- security impact;
- contractual/legal consequence;
- user explicitly requests independent review.

## 15. Exit Protocol

Before ending:
1. determine completion state;
2. run required checks;
3. persist verified state;
4. update task status;
5. record material decisions/failures;
6. write resumable handoff;
7. state whether approval or another dependency is required.

The objective is not to maximize autonomous activity. It is to maximize correct, auditable, resumable progress.
