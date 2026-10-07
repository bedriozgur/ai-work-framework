# Project Bootstrap Specification

## Goal
Create the minimum correct project harness without inventing project facts.

## 1. Select profile

Use **Lightweight** when work is bounded, low-to-moderate consequence, has few recurring workflows, and does not require detailed permission/source governance.

Use **Full** when work is recurring, multi-agent, automation-heavy, consequential, source-sensitive, or requires explicit acceptance/approval rules.

When uncertain, start Lightweight and promote later.

## 2. Create required files

Copy the appropriate templates. Populate only facts supported by the initiating request or inspected evidence.

Unknown information must remain UNKNOWN/TBD rather than being guessed.

## 3. Establish project identity

`PROJECT.md` must minimally define:
- objective;
- scope;
- expected deliverable/outcome;
- profile;
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
