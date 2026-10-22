# Framework Versioning

## Policy

The framework uses semantic-style versions once v1.0 is declared.

- **PATCH** — clarification or compatible template/check improvement.
- **MINOR** — backward-compatible capability, pattern, or optional protocol addition.
- **MAJOR** — incompatible protocol, required-file, state-semantics, or permission-model change.

Until v1.0, the framework remains Draft and may change incompatibly.

Every pilot or release candidate must use an annotated tag. A branch name or untagged working tree is not a release identifier. Generated deployment instructions record the exact canonical-source commit and source-file hashes; the deployment artifact may be committed in a subsequent packaging commit because a Git commit cannot contain its own resulting SHA.

## Project adoption

Each managed project must record the framework version and exact framework commit it adopted in `project.yaml`. A moving branch name is not a reproducible pin. Framework updates do not automatically rewrite project-specific rules or state.

An upgrade should:
1. compare the project's adopted version with the target;
2. identify required migrations;
3. preserve project-specific content;
4. apply structural changes;
5. validate required files/checks;
6. record the migration in project progress.

Pre-1.0 releases also require a changelog entry and an explicit migration note for incompatible governance, profile, manifest, or validator behavior.

## Principle

Templates are starting points, not centrally synchronized copies. A framework upgrade must never overwrite local project decisions merely because a template changed.
