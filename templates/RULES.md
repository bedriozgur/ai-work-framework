# Rules

## Source Precedence
| Data / Evidence | Preferred Source | Fallback | Freshness | Validation | When unavailable |
|---|---|---|---|---|---|
| | | | | | |

## Autonomous Actions
-

## Approval Required
- Destructive actions, including deletion, overwrite, truncation, force-push, and history rewrite
- Production configuration changes
- Production restarts
- External publication or communication
- Purchases
- Financial trades
- Irreversible actions

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
