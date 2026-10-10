# AI Work Framework

A reusable operating framework for AI-assisted projects.

The framework defines how reasoning models, execution agents, tools, evidence, durable project state, verification, permissions, and handoffs work together. Live project state remains in each project's own repository or controlled workspace.

## Core loop

**Read state → understand task → inspect evidence → choose a bounded action → execute → verify → persist → hand off.**

## Profiles

**Lightweight:** `project.yaml`, `PROJECT.md`, `STATE.md`, `PROGRESS.md`.

**Full:** adds `RULES.md`, `TASKS.md`, `DECISIONS.md`, and `CHECKS.md` to the same manifest.

See `AI-PROJECT-OPERATING-FRAMEWORK.md` for the governing model and `templates/` for reusable project files.

## Reusable agent profiles

The [`agents/` directory](agents/README.md) contains model-neutral profiles for MIDAS trading research, infrastructure orchestration, enterprise architecture, independent QA, and research curation. The profiles define behavioral contracts and handoffs; runtime tools, permissions, source isolation, and approval controls must be configured separately.

## Start a project

1. Copy `templates/project.yaml` and the files required by its profile.
2. Replace every placeholder in `project.yaml`, including the exact framework commit.
3. Optionally copy `templates/AGENTS.md` for agents that automatically load that file.
4. Run `python3 scripts/validate_project.py /path/to/project`.

`project.yaml` is the discovery entry point. In v0.1 it uses JSON syntax, which is valid YAML 1.2, so the validator has no third-party parser dependency.

`framework.yaml` uses the same format and contains only the structural profile contract consumed by the validator. Behavioral requirements live in the protocol; they are not technical controls unless the active runtime enforces them.

For the Full profile, add `rules`, `tasks`, `decisions`, and `checks` to the `files` object, mapped to `RULES.md`, `TASKS.md`, `DECISIONS.md`, and `CHECKS.md` respectively.

## Principle

Conversation history is context, not authoritative project state. Verified facts, decisions, acceptance criteria, and resumable progress belong in the project workspace.
