# Decision: Setup - unanswered_blocking_policy

Date: 2026-06-29
Status: Accepted
Severity: L3
Section: operating_model

## Question
If a blocking question is unanswered, should the agent pause indefinitely, make conservative fallback, or stop the run?

## Answer
Stop or create deferred decision artifacts; do not silently resolve foundational boundary, storage, truth, or interface questions.

## Consequence
Agents must consult this artifact before asking the same question again. If status is Deferred and the issue becomes blocking, create a question in `question_queue/pending/`.
