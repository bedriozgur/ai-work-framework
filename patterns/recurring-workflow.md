# Recurring Workflow Pattern

A recurring run is successful only when its acceptance criteria pass.

Each run should:
1. assign a run ID, record the base commit, and confirm no other canonical-state writer is active;
2. load canonical rules and state;
3. verify required sources are available;
4. collect fresh inputs;
5. validate and normalize them;
6. perform the defined analysis/action, using stable request IDs for writes when supported;
7. run acceptance checks;
8. persist outputs and source timestamps;
9. update state/progress only for verified changes;
10. explicitly report partial or failed runs;
11. leave enough evidence to audit and reproduce the run.

Never treat the existence of an output file as proof that collection or analysis succeeded.
