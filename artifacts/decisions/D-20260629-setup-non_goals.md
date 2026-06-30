# Decision: Setup - non_goals

Date: 2026-06-29
Status: Accepted
Severity: L2
Section: identity

## Question
What should this project explicitly not try to do in v1?

## Answer
No runtime implementation in V1. No APIs, graph computation, database deployment, visualization, report generation, hypotheses, forecasting, recommendations, or ownership/duplication of MacroForge observational datasets.

## Consequence
Agents must consult this artifact before asking the same question again. If status is Deferred and the issue becomes blocking, create a question in `question_queue/pending/`.
