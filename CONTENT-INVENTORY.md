# Content Boundary Inventory

**Status:** Review required before public release.

| Content | Current location | Boundary decision | Action |
|---|---|---|---|
| Universal governance and protocol | Root Markdown files | Public/core candidate | Retain after consistency review |
| Validator, tests, CI, structural templates | `scripts/`, `tests/`, `.github/`, project templates | Public/core candidate | Retain after hardening |
| Personal workflow | `BEDRI-CHATGPT-WORKFLOW.md` | Private overlay candidate | Do not expand; decide move before release |
| Domain profiles and workflows | `agents/` | Optional domain-pack candidate | Retain temporarily; measure actual use before migration |
| Host/runtime-specific operational context | `agents/INFRA-ORCHESTRATOR.md`, runtime prompts | Private/runtime layer | Remove identifiers from core; migrate after decision |
| Grok-derived prompt material | `templates/GROK-BOT-PROMPT-RAW.md`, `templates/MIDAS-X-RESEARCH-DESK-GROK-BOT.md` | Provenance/reuse review required | Quarantine from a public release until reviewed |
| OpenClaw project-manager prompt | `templates/OPENCLAW-PROJECT-MANAGER-PROMPT.md` | Runtime-specific candidate | Move only after runtime-layer decision |

No file move or deletion is implied by this inventory. Those actions require a recorded boundary/licensing decision.
