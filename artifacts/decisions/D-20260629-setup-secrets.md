# Decision: Setup - secrets

Date: 2026-06-29
Status: Accepted
Severity: L4
Section: governance

## Question
Will the project handle secrets/API keys/credentials? If yes, specify where they should live.

## Answer
No secrets, API keys, or credentials in V1. If future implementation requires credentials, they must live outside git and be governed by a decision artifact before use.

## Consequence
Agents must consult this artifact before asking the same question again. If status is Deferred and the issue becomes blocking, create a question in `question_queue/pending/`.
