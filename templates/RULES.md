# Rules

## Source Precedence
| Data / Evidence | Preferred Source | Fallback | Freshness | Validation | When unavailable |
|---|---|---|---|---|---|
| | | | | | |

## Autonomous Actions
-

## Approval Required
The framework approval floor in `GOVERNANCE.md` always applies. List project-specific additions below; this section cannot remove or narrow the framework floor.

-

## Prohibited Actions
-

## Validation Requirements
-

## Conventions
-

## Failure Behavior
Do not fabricate successful retrieval, execution, or verification. Record the failure, preserve useful work, and identify the blocker or valid fallback.

For retryable reads, define a bounded attempt/time budget. Before retrying a timed-out or ambiguous write, inspect the destination for the prior effect.

## Sensitive Evidence
<!-- Define classifications, approved stores/model providers, and redaction requirements. Never put credentials in project files. -->
-

## Enforcement Register
Written policy is not technical enforcement. Record only controls verified for this project/runtime.

| Control / claimed boundary | Technical mechanism | Verified by | Verified at | Result | Limitations / expiry |
|---|---|---|---|---|---|
| | | | | policy-only | |
