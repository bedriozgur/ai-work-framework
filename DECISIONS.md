# Framework Decisions

## 2026-10-07 — Standard storage architecture

### Decision
Use GitHub as the canonical control/state plane and Google Drive as the standard artifact/evidence/interchange plane. Dropbox is not part of the standard architecture.

### Rationale
The framework needs durable versioned control state plus a common file plane usable for large/binary evidence, deliverables, and cross-agent exchange. Standardizing on one cloud file service reduces duplicated storage paths and ambiguous authority.

### Boundary
- GitHub: framework, rules, state, tasks, decisions, checks, code, configuration, workflows.
- Google Drive: large/binary evidence, source documents, exports, logs/support bundles, deliverables, review packages.
- Exceptions require a concrete project reason.

### Revisit when
Google Drive cannot satisfy a material integration, security, access-control, or operational requirement.
