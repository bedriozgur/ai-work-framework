# Content Boundary Inventory

**Status:** Public-core boundary applied for RC2 review; historical exposure remains recorded below.

| Content | Current location | Boundary decision | Action |
|---|---|---|---|
| Universal governance and protocol | Root Markdown files | Public/core candidate | Retain after consistency review |
| Validator, tests, CI, structural templates | `scripts/`, `tests/`, `.github/`, project templates | Public/core candidate | Retain after hardening |
| Personal workflow | Private overlay outside this repository | Private overlay | Removed from the current public tree on 2026-10-21; retained separately by the owner |
| Generic domain profiles and workflows | `agents/` | Authorized public optional domain-pack examples | Retain without personal state, live schedules, customer facts, or private runtime configuration |
| Generic runtime examples | `agents/INFRA-ORCHESTRATOR.md`, `templates/OPENCLAW-PROJECT-MANAGER-PROMPT.md` | Authorized public runtime examples | Retain as policy examples; runtime-specific private configuration remains outside core |
| Grok-derived prompt material | Owner-controlled quarantine outside this repository | Provenance/reuse review required | Removed from the current public tree on 2026-10-21; do not restore without a recorded reuse decision |
| Project-specific schedules, terminology, notification routes, holdings, and decision state | Controlled project/private overlays | Private/project layer | Excluded from current public tree |

The removed files remain reachable in pre-RC2 Git history because this correction does not rewrite public history. See `SECURITY.md` and D-005 in `DECISIONS.md`.
