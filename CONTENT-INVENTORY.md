# Content Boundary Inventory

**Status:** Current-tree boundary applied for RC2 review; historical exposure and licensing decisions remain recorded below.

| Content | Current location | Boundary decision | Action |
|---|---|---|---|
| Universal governance and protocol | Root Markdown files | Public/core candidate | Retain after consistency review |
| Validator, tests, CI, structural templates | `scripts/`, `tests/`, `.github/`, project templates | Public/core candidate | Retain after hardening |
| Personal workflow | Private overlay outside this repository | Private overlay | Removed from the current public tree on 2026-10-21; retained separately by the owner |
| Domain profiles and workflows | `agents/` | Optional domain-pack candidate | Retain temporarily; measure actual use before migration |
| Host/runtime-specific operational context | `agents/INFRA-ORCHESTRATOR.md`, runtime prompts | Private/runtime layer | Current-tree identifiers removed; runtime-layer migration remains pending |
| Grok-derived prompt material | Owner-controlled quarantine outside this repository | Provenance/reuse review required | Removed from the current public tree on 2026-10-21; do not restore without a recorded reuse decision |
| OpenClaw project-manager prompt | `templates/OPENCLAW-PROJECT-MANAGER-PROMPT.md` | Runtime-specific candidate | Move only after runtime-layer decision |

The removed files remain reachable in pre-RC2 Git history because this correction does not rewrite public history. See `SECURITY.md` and D-005 in `DECISIONS.md`.
