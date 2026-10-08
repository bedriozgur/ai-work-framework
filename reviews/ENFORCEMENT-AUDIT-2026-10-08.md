# Enforcement Audit

**Date:** 2026-10-08

## Decision

Keep only mechanically consumed structural rules in `framework.yaml`. Do not encode behavioral expectations as booleans unless a validator or runtime actually evaluates them.

## Mechanically enforced here

The project validator and CI enforce:

- `project.yaml` exists and uses the supported schema version;
- project ID and profile are valid;
- the framework reference contains an exact 40-character commit SHA;
- placeholders are replaced;
- the selected profile supplies exactly the control-file keys defined by `framework.yaml`;
- mapped control files use project-relative paths, are unique, and exist;
- validator unit tests pass.

## Runtime-enforced when available

These controls belong to the active platform, Git host, operating system, API, or credentials—not to this documentation repository:

- filesystem and sandbox write boundaries;
- credential scope and tool authorization;
- branch protection, force-push restrictions, and required review;
- approval checks at consequential tool invocation;
- external-action idempotency and spending/runtime limits.

Projects must inspect and report whether these controls are actually active. Prompt text does not establish enforcement.

## Semantic or advisory

These rules require agent/human judgment and remain normative protocol rather than machine configuration:

- selecting the smallest useful bounded action;
- judging evidence quality and whether a fallback is weaker;
- assigning VERIFIED, OBSERVED, INFERRED, or other state classes honestly;
- determining whether a baseline or independent review is practical;
- identifying unrelated scope changes;
- deciding whether a handoff is useful rather than merely complete;
- research, architecture, and recommendation quality.

## Removed false signals

The earlier `framework.yaml` contained booleans such as `require_verification`, `recheck_before_write`, and `never_claim_unverified_enforcement`. No code consumed most of them. They duplicated protocol text and could be mistaken for controls. They were removed from the machine contract; the underlying behavioral rules remain in `AGENT-OPERATING-PROTOCOL.md` and `AI-PROJECT-OPERATING-FRAMEWORK.md`.

## Revisit condition

Add a machine key only when its consumer and failure behavior are implemented and tested in the same change.
