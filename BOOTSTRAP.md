# Project Bootstrap Specification

## Goal
Create the minimum correct project harness without inventing project facts.

## 1. Select profile

Use **Lightweight** when work is bounded, low-to-moderate consequence, single-writer, has few recurring workflows, and does not require detailed permission/source governance.

Use **Full** when any approval-gated action, recurring automation, multiple writers, sensitive/customer data, or explicit acceptance/source governance is in scope.

When none of the Full triggers is known to apply, start Lightweight and promote as soon as one appears.

## 2. Create required files

Copy `templates/project.yaml` and the templates required by the selected profile. Populate only facts supported by the initiating request or inspected evidence.

`project.yaml` is mandatory. Replace all placeholders, pin the exact framework commit, and run `scripts/validate_project.py` before work begins. Agents locate the project root as the nearest ancestor containing `project.yaml`.

Copy `templates/AGENTS.md` when the target agent automatically loads that file. It is a pointer, not a second source of project policy.

Unknown information must remain UNKNOWN/TBD rather than being guessed.

## 3. Establish project identity

`project.yaml` defines project identity, profile, framework pin, canonical repository, and control-file paths. `PROJECT.md` must minimally define:
- objective;
- scope;
- expected deliverable/outcome;
- authoritative references known at bootstrap.

## 4. Establish initial state

`STATE.md` must contain a verification date and distinguish verified facts from reported/unknown information.

## 5. Full-profile additions

Define:
- permissions and source precedence in `RULES.md`;
- active work in `TASKS.md`;
- acceptance criteria in `CHECKS.md`;
- existing material decisions in `DECISIONS.md`.

## 6. First progress entry

Record bootstrap source, created files, unresolved questions, and the next concrete action.

## 7. Promotion

A Lightweight project should be promoted to Full when recurring automation, multiple agents, consequential actions, complex source rules, or repeated ambiguity makes the extra controls useful.

Promotion adds controls; it must not rewrite verified history.
