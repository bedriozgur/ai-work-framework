# Changelog

All notable framework changes will be recorded here. The project remains pre-1.0; compatibility is not guaranteed, but migrations must still be explicit.

## Unreleased — P0 hardening

### Added

- Canonical governance source for authority, invariants, approval floor, classification, assignment envelope, delegation evidence, and QA verdicts.
- Security and content-boundary documentation.
- Validator defenses for duplicate keys, path portability, repository escapes, unresolved pins, and unfilled control templates.
- Compact-instruction generation and provenance verification tooling.

### Changed

- Removed private infrastructure identifiers from reusable agent documentation.
- Profile-specific boot behavior no longer requires Full-only files for Lightweight projects.
- Existing bounded Work runs are described as orchestration demonstrations, not harness or production-enforcement validation.
- Personal workflow and unresolved Grok-derived prompt material were removed from the current public tree and preserved separately pending provenance/reuse decisions.
- Offline snapshot validation now requires a trusted out-of-band metadata digest.
- Empty profile contracts are rejected instead of disabling structural validation.
- Agent and runtime profiles now use the canonical governance assignment, approval, handoff, and QA-independence contracts.
- Public domain profiles were generalized; live schedules, personal authority, notification routes, and project terminology moved to controlled project overlays.

### Migration

- Replace legacy L0–L3 task labels with the two-axis `I0`–`I2` impact and `C0`–`C2` coordination classification.
- Add the framework approval floor to every project; project rules may add gates but may not remove it.
- Update task briefs and run returns to the canonical assignment envelope in `GOVERNANCE.md`.
- Record exact framework release/tag and generated-instruction provenance before the next controlled pilot.
- Existing offline snapshot consumers must pass `--framework-snapshot-sha256`; recreate snapshots whose repository identity was not verified against the source clone.
