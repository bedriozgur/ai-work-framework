# Project entry point

This project uses the AI Work Framework.

1. Locate and validate the nearest ancestor `project.yaml`.
2. Read the framework protocol at the exact repository commit pinned there.
3. Load only the project files required by the declared profile and current task.

`project.yaml` is authoritative for discovery, profile, framework pin, and control-file paths. This pointer must not duplicate or override project policy.
