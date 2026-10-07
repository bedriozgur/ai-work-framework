# Recurring Workflow Pattern

A recurring run is successful only when its acceptance criteria pass.

Each run should:
1. load canonical rules and state;
2. verify required sources are available;
3. collect fresh inputs;
4. validate and normalize them;
5. perform the defined analysis/action;
6. run acceptance checks;
7. persist outputs and source timestamps;
8. update state/progress only for verified changes;
9. explicitly report partial or failed runs;
10. leave enough evidence to audit and reproduce the run.

Never treat the existence of an output file as proof that collection or analysis succeeded.
