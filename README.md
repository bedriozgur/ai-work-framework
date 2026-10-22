# AI Work Framework

A reusable operating framework for AI-assisted projects.

The framework defines how reasoning models, execution agents, tools, evidence, durable project state, verification, permissions, and handoffs work together. Live project state remains in each project's own repository or controlled workspace.

`GOVERNANCE.md` is the normative source for authority, invariants, the approval floor, task classification, assignment envelopes, delegation evidence, and QA verdicts. `AGENT-OPERATING-PROTOCOL.md` defines the execution lifecycle. Other files must link to, not redefine, those concepts.

## Core loop

**Read state → understand task → inspect evidence → choose a bounded action → execute → verify → persist → hand off.**

## Profiles

**Lightweight:** `project.yaml`, `PROJECT.md`, `STATE.md`, `PROGRESS.md`.

**Full:** adds `RULES.md`, `TASKS.md`, `DECISIONS.md`, and `CHECKS.md` to the same manifest.

See `GOVERNANCE.md` for mandatory governance, `AI-PROJECT-OPERATING-FRAMEWORK.md` for the architecture model, and `templates/` for reusable project files.

## Reusable agent profiles

The [`agents/` directory](agents/README.md) contains ten model-neutral profiles: cross-domain coordination, infrastructure orchestration, MIDAS portfolio synthesis, source-isolated data collection, technical risk, issuer fundamentals/catalysts, quantitative research engineering, enterprise architecture, QA, and general research. These documents define behavior and handoffs; runtime tools, permissions, source isolation, and approval controls must be configured separately. User-specific workflow context belongs in a private overlay, not this public core.

Public profiles are generic examples. Live schedules, personal authority, holdings, notification routes, customer facts, project-specific terminology, and private runtime configuration belong in controlled project or private overlays.

## Start a project

1. Copy `templates/project.yaml` and the files required by its profile.
2. Replace every placeholder in `project.yaml`, including the exact framework commit.
3. Optionally copy `templates/AGENTS.md` for agents that automatically load that file.
4. From a framework checkout that contains the pinned commit, run `python3 scripts/validate_project.py /path/to/project`. Use `--framework-repo` to name another local clone. For offline validation, create a snapshot with `scripts/create_framework_snapshot.py`, transport its printed `SNAPSHOT_JSON_SHA256` through a trusted channel separate from the snapshot, and supply both `--framework-snapshot` and `--framework-snapshot-sha256`.

`project.yaml` is the discovery entry point. It uses JSON syntax, which is valid YAML 1.2, so the validator has no third-party parser dependency.

`framework.yaml` uses the same format and contains only the structural profile contract consumed by the validator. Behavioral requirements live in governance and protocol documents; they are not technical controls unless the active runtime enforces them.

`deploy/COMPACT-INSTRUCTIONS.md` is generated from canonical governance sources. Its header records the source commit and source-file hashes. Verify it with `python3 scripts/generate_compact_instructions.py --check`; do not edit it manually.

An offline snapshot is authentic only to the extent that the separately obtained metadata digest is trusted. A digest stored or transported with the snapshot provides corruption detection, not independent provenance.

For the Full profile, add `rules`, `tasks`, `decisions`, and `checks` to the `files` object, mapped to `RULES.md`, `TASKS.md`, `DECISIONS.md`, and `CHECKS.md` respectively.

## Principle

Conversation history is context, not authoritative project state. Verified facts, decisions, acceptance criteria, and resumable progress belong in the project workspace.
