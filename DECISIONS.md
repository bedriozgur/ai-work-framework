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

### Revisit when
Google Drive cannot satisfy a material integration, security, access-control, or operational requirement.
