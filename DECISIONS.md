# Framework Decisions

## D-001 — 2026-10-07 — Standard storage architecture

- **Status:** accepted
- **Approved by:** not recorded in the original entry
- **Supersedes:** none

### Decision
Use GitHub as the canonical control/state plane and Google Drive as the standard artifact/evidence/interchange plane. Dropbox is not part of the standard architecture.

### Evidence
The framework requires versioned, diffable control state plus a file plane that can carry large and binary artifacts across agents.

### Alternatives Considered
- Store all state and artifacts in GitHub.
- Use multiple cloud file services as peers.

### Rationale
The framework needs durable versioned control state plus a common file plane usable for large/binary evidence, deliverables, and cross-agent exchange. Standardizing on one cloud file service reduces duplicated storage paths and ambiguous authority.

### Boundary
- GitHub: framework, rules, state, tasks, decisions, checks, code, configuration, workflows.
- Google Drive: large/binary evidence, source documents, exports, logs/support bundles, deliverables, review packages.
- Exceptions require a concrete project reason.

### Risks / Tradeoffs
Drive objects may be mutable, so decision-critical references require stable identifiers and, when exact-byte reproducibility matters, a content hash.

### Reconciliation with earlier project notes
A continuity note created on 2026-10-05 suggested Dropbox as a portable-document route for some workflows. This decision was accepted on 2026-10-07 and sets the global default. The earlier note is historical and is not silently migrated or deleted by this decision. A project may document a Dropbox exception when it has a concrete access or integration need; the project must still identify its canonical source of truth and avoid treating Dropbox as a peer authority.

### Revisit when
Google Drive cannot satisfy a material integration, security, access-control, or operational requirement.

## D-002 — 2026-10-20 — Canonical governance and approval floor

- **Status:** accepted for P0 implementation
- **Approved by:** Bedri
- **Supersedes:** duplicated authority, invariant, approval, assignment-envelope, and QA-vocabulary definitions

### Decision
Use `GOVERNANCE.md` as the single normative source for authority, invariants, the non-shrinkable approval floor, task classification, assignment envelopes, delegation evidence, and QA verdicts. Projects and domain profiles may strengthen these rules but may not weaken them.

### Evidence
Claude R2 identified directly conflicting lists across the protocol, framework, personal workflow, templates, and profiles. Local inspection confirmed the conflicts.

### Rationale
One canonical source reduces drift and makes generated deployment instructions reviewable.

### Revisit When
A controlled pilot identifies a governance concept that cannot be represented without ambiguity.

## D-003 — 2026-10-20 — Separate impact from coordination

- **Status:** accepted for P0 implementation
- **Approved by:** Bedri
- **Supersedes:** proposed compact L0-L3 classification

### Decision
Use two axes: `I0`-`I2` for consequence/approval and `C0`-`C2` for execution coordination. Approval follows impact and the approval floor. Delegation follows coordination need.

### Evidence
The L0-L3 proposal mixed technical complexity, delegation need, and consequence, allowing inconsistent classification.

### Alternatives Considered
- Consequence-only L0-L3.
- Preserve the mixed L0-L3 ladder.

### Rationale
The two axes prevent complex read-only work from being mistaken for consequential action and prevent technically simple production changes from being downgraded.

### Revisit When
Pilot users cannot apply the axes consistently or the extra field creates measurable overhead without preventing errors.

## D-004 — 2026-10-20 — Core, domain, runtime, and private content boundaries

- **Status:** accepted in principle; migration pending
- **Approved by:** Bedri
- **Supersedes:** none

### Decision
Keep universal governance, lifecycle, structural templates, validation, and tests in the core. Treat domain profiles as optional packs, runtime prompts as runtime-layer artifacts, and personal/host/customer-adjacent content as a private overlay. Do not delete or move existing domain material until inventory, provenance, reuse, and migration decisions are complete.

### Evidence
The public repository contained internal infrastructure identifiers, personal workflow material, runtime-specific prompts, and third-party-derived templates alongside universal policy.

### Risks / Tradeoffs
Splitting content too early could break existing references. Leaving it mixed increases disclosure, licensing, and maintenance risk.

### Revisit When
The content inventory and repository visibility/licensing decision are complete.

## D-005 — 2026-10-21 — Current-tree quarantine and historical exposure

- **Status:** accepted for the RC2 correction round
- **Approved by:** Bedri
- **Supersedes:** D-004's temporary retention of personal and unresolved Grok-derived material in the public core

### Decision
Remove the personal workflow handoff and two unresolved Grok-derived prompt documents from the current public repository tree. Preserve owner-controlled copies outside the repository while provenance, reuse, and private-overlay placement are decided. Do not rewrite Git history in this correction round.

### Evidence
The repository is public. The P0 fresh review confirmed that the new public-boundary policy conflicted with the current tree and that a removed private-network address remained reachable in baseline history.

### Rationale
Current-tree quarantine reduces continued distribution without treating a destructive history rewrite as an automatic consequence. The history limitation remains visible rather than being described as remediated.

### Revisit When
Before a final public release, or immediately if review identifies credentials, customer-confidential information, or material licensing risk in reachable history.
