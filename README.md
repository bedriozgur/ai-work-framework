# AI Work Framework

A reusable operating framework for AI-assisted projects.

The framework defines how reasoning models, execution agents, tools, evidence, durable project state, verification, permissions, and handoffs work together. Live project state remains in each project's own repository or controlled workspace.

## Core loop

**Read state → understand task → inspect evidence → choose a bounded action → execute → verify → persist → hand off.**

## Profiles

**Lightweight:** `PROJECT.md`, `STATE.md`, `PROGRESS.md`.

**Full:** adds `RULES.md`, `TASKS.md`, `DECISIONS.md`, and `CHECKS.md`.

See `AI-PROJECT-OPERATING-FRAMEWORK.md` for the governing model and `templates/` for reusable project files.

## Principle

Conversation history is context, not authoritative project state. Verified facts, decisions, acceptance criteria, and resumable progress belong in the project workspace.
