# Decision: Setup - model_policy

Date: 2026-06-29
Status: Accepted
Severity: L2
Section: model_routing

## Question
Model policy: smallest sufficient, fastest, highest quality, or project-specific?

## Answer
smallest sufficient model/tool for routine artifact edits; cloud reasoning only for high-ambiguity architecture reviews.

## Consequence
Agents must consult this artifact before asking the same question again. If status is Deferred and the issue becomes blocking, create a question in `question_queue/pending/`.
